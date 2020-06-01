# # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # 
# Copyright 2020 Daniel Bakkelund
#
# This program is free software: you can redistribute it and/or modify
# it under the terms of the GNU Lesser General Public License as published by
# the Free Software Foundation, either version 3 of the License, or
# (at your option) any later version.
# 
# This program is distributed in the hope that it will be useful,
# but WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
# GNU Lesser General Public License for more details.
# 
# You should have received a copy of the GNU Lesser General Public License
# along with this program.  If not, see <https://www.gnu.org/licenses/>.
# # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # 

from   ophac.dtypes import *
import ophac.ultrametric as ult
import numpy as np

def _getLogger(x):
    import logging
    return logging.getLogger(__name__ + '.' + x.__name__)

def _s_inv(i,j,k):
    if k < j:
        return k
    else:
        return k+1

def _T_inv(i,j,a,b):
    assert i < j
    assert a < b

    srt = lambda a,b : tuple(sorted([a,b ]))
    
    if b == i:
        return [srt(a,i), srt(a,j)]
    elif a == i:
        y = _s_inv(i,j,b)
        return [srt(i,y),srt(j,y)]
    else:
        return [(_s_inv(i,j,a),
                 _s_inv(i,j,b))]

def _plusTransformation(P0,i,j):
    assert i<j
    n  = P0.n-1
    C  = (1-P0[i,j])
    P1 = DistMatrix([0]*(n*(n-1)//2))
    for a in range(n):
        for b in range(a+1,n):
            inv_img = _T_inv(i,j,a,b)
            for x,y in inv_img:
                P1[a,b] = P1[a,b] + P0[x,y]/C

    return P1

def _pAC(ac):
    if len(ac) == 0:
        return ac
    mp = [0]*len(ac)
    mp[0] = ac.dists[0]
    for i in range(1,len(ac)):
        mp[i] = mp[i-1]*ac.dists[i]

    ip = [1-p for p in mp]
    return AC(joins=ac.joins, dists=ip)

def _acProb(ac):
    pac = _pAC(ac)
    return np.product(ac.dists)

def _pUltrametric(ac,N):
    ac2 = _pAC(ac)
    dK  = 1
    if len(ac2) > 0:
        dK  = 1 - ac2.dists[-1]
    return ult.ultrametric(ac2,N,dK)
    
    
class PHAC:

    def __init__(self, trans):
        '''
        trans  - Probability transformation - one of '+'.
        '''
        self.log          = _getLogger(PHAC)
        self.trans        = trans
        self._setTransformation()
        self.log.info('Instantiated with transform=%s.', trans)

    def _setTransformation(self):
        assert self.trans == '+'
        self._transform = _plusTransformation
        
    def _initClustering(self,P0):
        self.N        = P0.n
        self.bestProb = 0.0  # Highest probability so far
        self.acs      = []   # Best chains

    def generate(self,probs):
        '''
        probs  - Probabilities for pair agglomerations
        '''
        self._initClustering(probs)
        self._exploreChains(probs, AC())
        return self._pickBest()
        
    def _exploreChains(self, P1, ac1):
        '''
        P1        - Probabilities for merging blocks
        ac0       - AgglomerativeClustering object leading up to the 
                    current partition
        '''
        self.log.debug('Exploring %d block partition.', P1.n)

        if P1.n == 1:
            self.log.debug('Trivial partition reached.')
            self._registerCandidate(ac1)
            return 

        P     = np.array(P1.dists)
        p     = np.max(P)
        I     = np.argwhere(P == p).flatten()
        pairs = [P1.toMatrixIndex(i) for i in I]
        
        for a,b in pairs:
            self.log.debug('Merging (%d,%d) at probability %1.3f.',
                           a, b, p)
            P2  = self._transform(P1,a,b)
            ac2 = ac1 + AC(joins=[(a,b)], dists=[p])
            self._exploreChains(P2, ac2)

        return
    
    def _registerCandidate(self, ac):
        assert len(ac) == self.N-1
        prob = _acProb(ac)
        
        if prob < self.bestProb:
            # discard candidate
            return

        if prob > self.bestProb:
            self.log.info('New best candidate at probability %1.3e', prob)
            self.acs      = [_pAC(ac)]
            self.bestProb = prob
        else:
            # Same probability
            self.acs.append(_pAC(ac))

    def _pickBest(self):
        self.log.info('Finding best of %d dendrograms.', len(self.acs))

        class _MySet(set):
            def add(self,x):
                n = len(self)
                set.add(self,x)
                return len(self) > n
        
        # Remove duplicate ultrametric ACs
        acs2 = []
        ults = _MySet()
        for ac in self.acs:
            U = _pUltrametric(ac, self.N)
            if ults.add(U):
                acs2.append(ac)

        self.log.info('Returning %d unique solutions, having P=%1.3e',
                      len(acs2), np.product(acs2[0].dists))
        return acs2
