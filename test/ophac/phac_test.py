
import upyt.unittest as ut
import ophac.phac    as phac

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
        P1  = phac.plusTransformation(P0,i,j)

        expected = phac.DistMatrix([2/7, 3/7,
                                    2/7])

        self.assertEquals(expected, P1)
