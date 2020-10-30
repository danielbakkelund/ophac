
import upyt.unittest as ut
import ophac.rnd     as rnd
import numpy         as np

class TestStuff(ut.UnitTest):

    def testAcyclic(self):
        for _ in range(300):
            for p in np.linspace(0.01,0.5,10):
                Q = rnd.randomOrder(30,p)
                self.assertFalse(Q.hasCycle(), Q)
