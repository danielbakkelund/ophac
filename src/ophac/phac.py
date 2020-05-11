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
                
def _pUltrametric(ac,N):
    Md = 0
    if len(ac) > 0:
        Md = ac.dists[-1] - 1e-12
    dK = 1 - Md
    return ult.ultrametric(ac, N, dK)

class PHAC:

    def __init__(self, trans, ord=1, dK=1e-12, pred=True, cutoff=True):
        '''
        trans  - Probability transformation - one of '+'.
        ord    - The norm-order to use. Default is 1.0.
        dK     - The increment to apply for the ultrametric completion.
        pred   - Use partial order reduction? Default is True.
        cutoff - Use fit detorieration cutoff. Defaut it True
        '''
        self.log          = _getLogger(PHAC)
        self.trans        = trans
        self.ord          = ord
        self.dK           = dK
        self.pred         = pred
        self.cutoff       = cutoff
        self._setTransformation()
        self.log.info('Instantiated with transform=%s and ord=%1.3f.', trans, ord)

    def _setTransformation(self):
        assert self.trans == '+'
        self._transform = _plusTransformation
        
    def _initClustering(self, P0, quivers):
        assert len(quivers) == P0.n

        self.N  = len(quivers)
        self.P0 = P0

        ac0  = AgglomerativeClustering()
        U0   = _pUltrametric(ac0, self.N)
        norm = U0.norm(self.ord)

        self.bestNorm = norm       # Closest ultrametric
        self.acs      = [ac0]      # Maximal best chains
        self.ults     = set([U0])  # Visited ultrametrics

    def generate(self,probs,order=None):
        '''
        probs  - Probabilities for pair agglomerations
        order  - Order relation of type ophac.dtypes.Quivers, 
                 or None for non-ordered clustering.
        '''
        if order is None:
            order = Quivers(n=probs.n, relation=[])

        self._initClustering(probs, order)
        
        self._exploreChains(probs, order, self.acs[-1], self.bestNorm)

        return self._pickBest()
        
    def _exploreChains(self, P1, order, ac0, lastDiff):
        '''
        P1        - Probabilities for merging blocks
        order     - Quivers object for the current partition
        ac0       - AgglomerativeClustering object leading up to the 
                    current partition
        '''
        self.log.debug('Exploring %d block partition.', len(order))

        if len(order) == 1:
            self.log.debug('Trivial partition reached.')
            self._registerCandidate(ac0)
            return 
    
        # Find maximal probability to merge on
        chunks = P1.getChunkedIndexPairs()
        chunk  = None
        for _ch in chunks:
            if chunk is not None:
                break
            for a,b in _ch.pairs:
                if order.canMerge(a,b):
                    self.log.debug('Mergeable pair (%d,%d) of p=%1.3f found.',
                                   a, b, _ch.dist)
                    chunk = _ch
                    break

        if chunk is None:
            self.log.debug('No further mergeable pairs --- maximal element reached')
            self._registerCandidate(ac0)
            return 

        merged = False
        for a,b in chunk.pairs:
            if order.canMerge(a,b):
                self.log.debug('Merging (%d,%d) at probability %1.3f.',
                               a, b, chunk.dist)
                P2  = self._transform(P1,a,b)
                O2  = order.merge(a,b)
                ac2 = ac0 + AC(joins=[(a,b)], dists=[chunk.dist])
                merged = True
                if len(ac2) > 1:
                    assert ac2.dists[-2] <= ac2.dists[-1]
                diff, better = self._checkVisit(ac2, lastDiff)
                if better:
                    self._exploreChains(P2, O2, ac2, diff)

        assert merged

        return

    def _checkVisit(self, ac, lastDiff):
        '''
        Returns true if this chain should be attempted extended.
        '''
        U  = _pUltrametric(ac, self.N)
        
        if self.pred:
            l0 = len(self.ults)
            self.ults.add(U)
            l1 = len(self.ults)
            if l0 == l1:
                # Already visited this state
                return (None,False)

        if not self.cutoff:
            return (0,True)
        
        diff   = U.norm(self.ord)
        better = diff <= lastDiff or diff <= self.bestNorm
        return (diff, better)

    def _registerCandidate(self, ac):
        U    = _pUltrametric(ac, self.N)
        norm = U.norm(self.ord)

        if norm > self.bestNorm:
            # discard candidate
            return

        if norm < self.bestNorm:
            self.log.info('New best candidate at norm %1.3e', norm)
            self.acs      = [ac]
            self.bestNorm = norm
        else:
            # Same norm
            self.acs.append(ac)

    def _pickBest(self):
        import numpy as np
        self.log.info('Finding best of %d dendrograms.', len(self.acs))

        class _MySet(set):
            def add(self,x):
                n0 = len(self)
                set.add(self,x)
                return len(self) > n0
        
        if len(self.acs) == 1:
            self.log.info('Returning unique solution.')
            return self.acs

        # Remove duplicate ultrametric ACs
        acs2 = []
        ults = _MySet()
        for ac in self.acs:
            U = _pUltrametric(ac, self.N)
            if ults.add(U):
                acs2.append(ac)
        self.acs = acs2

        norm = lambda ac : _pUltrametric(ac, self.N).norm(self.ord)
        acs  = sorted(self.acs, key=norm)
        best = norm(acs[0])
        i    = 1
        while i < len(acs) and norm(acs[i]) == best:
            i += 1

        self.log.info('Returning %d bests with fitting error %1.3f', i, norm(acs[0]))

        return acs[:i]
