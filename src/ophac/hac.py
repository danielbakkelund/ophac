
from   ophac.dtypes import *
import ophac.ultrametric as ult


def _getLogger(x):
    import logging
    return logging.getLogger(__name__ + '.' + x.__name__)

class HAC:

    def __init__(self, lnk, ord=1, dK=1e-12):
        '''
        lnk - Linkage model; one of 'single', 'average' or 'complete'.
        ord - The norm-order to use. Default is 1.0.
        dK  - The increment to apply for the ultrametric completion.
        '''
        self.log          = _getLogger(HAC)
        self.lnk          = lnk
        self.ord          = ord
        self.dK           = dK
        self._setLinkageFunctionFactory()
        self.log.info('Instantiated with lnk=%s and ord=%1.3f.', lnk, ord)

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

    def _initClustering(self, dissim, quivers):
        assert len(quivers) == dissim.n
        self.acs = []
        self.N   = len(quivers)

    def _pickBest(self):
        import numpy as np
        self.log.info('Finding best of %d dendrograms.', len(self.acs))

        if len(self.acs) == 1:
            self.log.info('Returning unique solution.')
            return self.acs

        K0 = np.max([ac.dists[-1] for ac in self.acs])
        K  = K0 + self.dK # Pick a very small increment --- due to floating point
                          # precision, this is the best we can hope for
        norm     = lambda ac : ult.ultrametric(ac, self.N, K).norm(self.ord)
        self.acs = sorted(self.acs, key=norm)
        best     = norm(self.acs[0])
        i        = 1
        while i < len(self.acs) and norm(self.acs[i]) == best:
            i += 1

        self.log.info('Returning %d bests with norms %1.3f', i, norm(self.acs[0]))

        return self.acs[:i]

    def generate(self,dissim,order=None):
        '''
        dissim - Dissimilarity measure of type ophac.dtypes.DistMatrix 
        order  - Order relation of type ophac.dtypes.Quivers, 
                 or None for non-ordered clustering.
        '''
        if order is None:
            order = Quivers(n=dissim.n, relation=[])

        self._initClustering(dissim, order)
        self._exploreChains(dissim, order, 
                            Partition(n=self.N), AgglomerativeClustering())
        return self._pickBest()
    
    
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
            self.acs.append(ac0)
            return 
    
        # Find minimal dissimilarity level to merge on
        chunks = dissim.getChunkedIndexPairs()
        chunk  = None
        for _ch in chunks[::-1]:
            if chunk is not None:
                break
            for a,b in _ch.pairs:
                if order.canMerge(a,b):
                    self.log.debug('Mergeable pair (%d,%d) of dissim %1.3f found.',
                                   a, b, _ch.dist)
                    chunk = _ch
                    break

        if chunk is None:
            self.log.debug('No further mergeable pairs --- maximal element reached')
            self.acs.append(ac0)
            return 

        # Get current linkage
        linker = self._getLinkageFunction([len(x) for x in partition])

        merged = False
        for a,b in chunk.pairs:
            if order.canMerge(a,b):
                self.log.debug('Merging (%d,%d) at dissim %1.3f.', a, b, chunk.dist)
                D2  = linker(a,b,dissim)
                P2  = partition.merge(a,b)
                O2  = order.merge(a,b)
                ac2 = ac0 + AgglomerativeClustering(joins=[(a,b)], dists=[chunk.dist])
                if len(ac2) > 1:
                    assert ac2.dists[-2] <= ac2.dists[-1]
                self._exploreChains(D2, O2, P2, ac2)
                merged = True

        assert merged

        return
