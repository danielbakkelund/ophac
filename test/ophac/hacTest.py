
import upyt.unittest as ut
import ophac.hac     as hac

class TestNonOrderedClustering(ut.UnitTest):

    
    def test_fig3_5_SL(self):
        '''
        Figure 3.5 in Jain and Dubes (1988)
        '''
        N     = 5
        dists = [5.8, 4.2, 6.9, 2.6,
                 6.7, 1.7, 7.2,
                 1.9, 5.6,
                 7.6]
        M  = hac.DistMatrix(dists)
        hc = hac.HAC('single')
        ac = hc.generate(M)
        self.assertTrue(len(ac) == 1)
        
        expJoins = [(1,3),(1,2),(0,2),(0,1)]
        expDists = [1.7, 1.9, 2.6, 4.2]
        expAc    = hac.AgglomerativeClustering(expJoins, expDists)

        self.assertEquals(expAc, ac[0])

    def test_fig3_5_CL(self):
        '''
        Figure 3.5 in Jain and Dubes (1988)
        '''
        N     = 5
        dists = [5.8, 4.2, 6.9, 2.6,
                 6.7, 1.7, 7.2,
                 1.9, 5.6,
                 7.6]
        M  = hac.DistMatrix(dists)
        hc = hac.HAC('complete')
        ac = hc.generate(M)
        self.assertTrue(len(ac) == 1)
        
        expJoins = [(1,3),(0,3),(0,2),(0,1)]
        expDists = [1.7, 2.6, 5.6, 7.6]
        expAc    = hac.AgglomerativeClustering(expJoins, expDists)

        self.assertEquals(expAc, ac[0])

    def test_ex_4_2_CL(self):
        '''
        Example 4.2 from the article.
        '''
        N = 4
        R = [[0,1],[2,3]]
        Q = hac.Quivers(n=N,relation=R)
        D = hac.DistMatrix([2.0, 1.0, 1.3,
                            1.0, 1.5,
                            2.0])
        hc  = hac.HAC('complete')
        acs = hc.generate(D,Q)
        
        self.assertEquals(1, len(acs), 'Wrong number of results (%s)' % str(acs))
        
        expected = hac.AC(joins=[(0,2),(1,2)],dists=[1.0,1.5])
        self.assertEquals(expected, acs[0])
