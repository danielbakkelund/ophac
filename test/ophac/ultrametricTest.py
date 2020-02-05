
import ophac.ultrametric as ultrametric
import ophac.dtypes      as clust2
import upyt.unittest     as ut

class UltrametricTest(ut.UnitTest):

    def testConvert(self):
        N = 6
        diam  = 4
        joins = [(0,2),(0,1),(1,3),(1,2)]
        dists = [1,1,2,3]
        ultra = [1,1,4,4,4,
                 1,4,4,4,
                 4,4,4,
                 3,2,
                 3]

        ac = clust2.AgglomerativeClustering(joins,dists)
        Mu = ultrametric.ultrametric(ac,N,diam)

        expected = clust2.DistMatrix(ultra)

        self.assertEquals(expected, Mu)

    def testNorm(self):
        pairs = [(7,8),(4,5),(0,1),(0,1)]
        dists = [1,2,3,4]
        ac = clust2.AgglomerativeClustering(joins=pairs,dists=dists)
        U  = ultrametric.ultrametric(ac,9,5)
        
        self.assertEquals(U.norm(1), ultrametric.norm(ac,9,5,1), '1-norm')
        self.assertEquals(U.norm(2), ultrametric.norm(ac,9,5,2), '2-norm')
        self.assertEquals(U.norm(3), ultrametric.norm(ac,9,5,3), '3-norm')

    def testNormReducibleDendrogram(self):
        pairs = [(7,8),(4,5),(0,1),(0,1)]
        dists = [1,2,2,4]
        ac = clust2.AgglomerativeClustering(joins=pairs,dists=dists)
        U  = ultrametric.ultrametric(ac,9,5)
        
        self.assertEquals(U.norm(1), ultrametric.norm(ac,9,5,1), '1-norm')
        self.assertEquals(U.norm(2), ultrametric.norm(ac,9,5,2), '2-norm')
        self.assertEquals(U.norm(3), ultrametric.norm(ac,9,5,3), '3-norm')
