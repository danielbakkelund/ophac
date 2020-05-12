
import upyt.unittest as ut
import ophac.phac    as phac
import numpy         as np

class PlustTransformTest(ut.UnitTest):

    def test_T_inv(self):
        i,j = 2,4

        self.assertEquals([(0,1)],phac._T_inv(i,j,0,1))
        self.assertEquals([(0,2),(0,4)],phac._T_inv(i,j,0,2))
        self.assertEquals([(2,5),(4,5)],phac._T_inv(i,j,2,4))
        self.assertEquals([(2,3),(3,4)],phac._T_inv(i,j,2,3))
        self.assertEquals([(3,5)],phac._T_inv(i,j,3,4))
        self.assertEquals([(5,6)],phac._T_inv(i,j,4,5))

    def test_transform(self):
        P0 = phac.DistMatrix([0.1, 0.2, 0.3,
                              0.2, 0.1,
                              0.1])
        i,j = 0,3
        P1  = phac._plusTransformation(P0,i,j)

        expected = phac.DistMatrix([2/7, 3/7,
                                    2/7])

        diff = np.max(np.abs((expected - P1).dists))
        self.assertTrue(diff < 1e-8)

class PHAC_Test(ut.UnitTest):

    def testNoOrder(self):
        P0 = phac.DistMatrix([0.1, 0.2, 0.3,
                              0.2, 0.1,
                              0.1])

        hc = phac.PHAC('+')
        acs = hc.generate(P0)
        self.assertEquals(1, len(acs), 'Too many results')

        expJoins = [(0,3),(0,2),(0,1)]
        expDists = [1-3/10, 1-3/7*3/10, 1-3/7*3/10]

        self.assertEquals(expJoins, acs[0].joins, 'Wrong joins')
        self.assertAllClose(expDists, acs[0].dists, msg='Wrong join probabilities')
        

    def testBimodalDist(self):
        '''
        Distribution that has two disjoint (p=0) sets of elements
        '''
        p = [ 5.751e-02, 1.735e-02, 3.114e-02, 0.000e+00, 1.076e-02, 2.833e-02,
              3.289e-02, 2.321e-02, 1.020e-02, 9.302e-03, 2.104e-02, 0.000e+00,
              2.851e-02, 4.843e-02, 1.075e-02, 4.311e-02, 2.637e-02, 5.362e-02,
              0.000e+00, 4.088e-02, 2.436e-02, 4.852e-02, 2.859e-02, 1.003e-02,
              0.000e+00, 3.180e-02, 3.387e-02, 2.025e-02, 4.524e-02, 2.908e-02,
              0.000e+00, 0.000e+00, 0.000e+00, 0.000e+00, 0.000e+00, 2.597e-02,
              2.653e-02, 1.114e-02, 3.978e-02, 2.184e-02, 4.647e-02, 1.133e-03,
              8.623e-03, 2.282e-02, 3.054e-02]
        P0 = phac.DistMatrix(p)
        hc = phac.PHAC('+')
        ac = hc.generate(P0)
        self.assertEquals(1, len(ac), 'more than one result')
        ac = ac[0]

        self.assertEquals(P0.n-1, len(ac), 'Too shallow hac.')
        
        for i in range(len(ac)-1):
            self.assertTrue(ac.dists[i] <= ac.dists[i+1], 'Failed with %f >= %f for i=%d and i+1=%d' %
                            (ac.dists[i], ac.dists[i+1], i, i+1))
    
    
