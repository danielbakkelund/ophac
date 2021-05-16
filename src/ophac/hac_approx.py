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

def HACUntied(lnk):
    log = _getLogger(HACUntied)    
    cpp = True
    try:
        import ophac_cpp
        log.info('C++ extension available.')
    except ModuleNotFoundError as e:
        log.warning('C++ extension not available.')
        cpp = False
    
    if cpp:
        log.info('Using C++ extension.')
        return HACUntied_cpp(lnk)
    else:
        log.info('Using python implementation.')
        return HACUntied_python(lnk)

class HACUntied_cpp:
       
    def __init__(self,lnk):
        self.log     = _getLogger(HACUntied_cpp)
        self.lnk     = lnk
        self.log.info('Instantiated with L:%s', lnk)

    def generate(self,dissim,order=None,mode='untied',**kwargs):
        import time
        import ophac_cpp    as cpp
        import numpy        as np
        import numpy.random as rnd

        CPP_MAX_UINT = 4294967294

        if 'seed' in kwargs:
            self.seed_used = cpp.seed(kwargs['seed'])
        else:
            self.seed_used = cpp.seed(int(rnd.randint(CPP_MAX_UINT)))
        
        self.log.info('Running on %d element space with mode %s and seed %d.',
                      dissim.n, mode, self.seed_used)

        dd = dissim.dists
        qq = [list() for _ in np.arange(dissim.n)]        
        if order:
            qq = order.quivers
            
        cpp_start = time.time()
        ac = None
        if mode == 'approx':
            ac = cpp.linkage_approx(dd,qq,self.lnk)
        else:
            assert mode == 'untied'
            ac = cpp.linkage_untied(dd,qq,self.lnk)

        self.log.info('C++ ophac (%s) completed in %1.3f s.',
                      mode, time.time() - cpp_start)

        dists,joins = zip(*ac)
        return AC(dists=dists,joins=joins)

            
        
class HACUntied_python:

    def __init__(self, lnk):
        '''
        lnk  - Linkage model; one of 'single', 'average' or 'complete'.
        '''
        self.log    = _getLogger(HACUntied_python)
        self.lnk    = lnk
        self._setLinkageFunctionFactory()
        self.log.info('Instantiated with lnk=%s.', lnk)

    def _setLinkageFunctionFactory(self):
        lnkFact = None
        if self.lnk == 'single':
            lnkFact = lambda sizes : BasicLinkage(SingleLinkage())
        elif self.lnk == 'complete':
            lnkFact = lambda sizes : BasicLinkage(CompleteLinkage())
        elif self.lnk == 'average':
            lnkFact = lambda sizes : BasicLinkage(AverageLinkage(sizes))
        else:
            raise Exception('Unknown linkage: "%s"' % self.lnk)

        self._getLinkageFunction = lnkFact

    def generate(self,dissim,order=None,mode='untied'):
        '''
        dissim - Dissimilarity measure of type ophac.dtypes.DistMatrix 
        order  - Order relation of type ophac.dtypes.Quivers, 
                 or None for non-ordered clustering.
        '''
        if mode != 'untied':
            raise Exception('Only untied mode is available in python.')
        
        if order is None:
            order = Quivers(n=dissim.n, relation=[])

        P0   = Partition(n=dissim.n)        
        return self._exploreChains(dissim, order, P0, AC())
        
    def _exploreChains(self, dissim, order, partition, ac0):
        '''
        dissim    - dissimilarity measure for the current partition
        order     - Quivers object for the current partition
        partition - Current partition
        ac0       - AgglomerativeClustering object leading up to the 
                    current partition
        '''
        self.log.debug('Exploring set of %d elements.', len(partition))

        if len(order) == 1:
            self.log.debug('Trivial partition reached.')
            return ac0
    
        # Find minimal dissimilarity level to merge on
        dispair = None
        for (d,pair) in dissim.getSortedIndexPairs():
            if dispair is not None:
                break # Has one!

            a,b = pair
            if order.canMerge(a,b):
                self.log.debug('Mergeable pair (%d,%d) of dissim %1.3f found.',
                               a, b, dissim[a,b])
                dispair = (d,pair)

        if dispair is None:
            self.log.debug('No further mergeable pairs --- maximal element reached')
            return ac0
        
        # Get current linkage
        linker = self._getLinkageFunction([len(x) for x in partition])
        
        (dist,(a,b)) = dispair
        self.log.debug('Merging (%d,%d) at dissim %1.3f.', a, b, dist)
        D2  = linker(a,b,dissim)
        P2  = partition.merge(a,b)
        O2  = order.merge(a,b)
        ac2 = ac0 + AC(joins=[(a,b)], dists=[dist])
        if len(ac2) > 1:
            assert ac2.dists[-2] <= ac2.dists[-1]

        return self._exploreChains(D2, O2, P2, ac2)

