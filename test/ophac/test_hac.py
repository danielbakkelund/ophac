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

import unittest          as ut
import ophac.hac         as hac
import ophac.ultrametric as ult

class TestNonOrderedClustering(ut.TestCase):

    
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

        self.assertEqual(expAc, ac[0])

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

        self.assertEqual(expAc, ac[0])

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
        
        self.assertEqual(1, len(acs), 'Wrong number of results (%s)' % str(acs))
        
        expected = hac.AC(joins=[(0,2),(1,2)],dists=[1.0,1.5])
        self.assertEqual(expected, acs[0])

    def testReproduceUltrametric(self):
        uData = [1, 2, 2, 3, 3,
                 2, 2, 3, 3,
                 1, 3, 3,
                 3, 3,
                 2]
        U = hac.DistMatrix(uData)

        L = ['single', 'average', 'complete']
        for lnk in L:
            hc   = hac.HAC(lnk)
            acs  = hc.generate(U)
            ults = [ult.ultrametric(ac, U.n, 1e-12) for ac in acs]
            self.assertTrue(U in ults, 'Failed for %s linkage' % lnk)

    def testCompletions(self):
        M = hac.DistMatrix([1,2,3])
        Q = hac.Quivers([[2],[],[]])

        L  = 'single'
        k0 = 0.1
        k1 = 0.2
        k2 = 2.0
        U0 = hac.DistMatrix([1.0, 1.1, 1.1])
        U1 = hac.DistMatrix([1.0, 1.2, 1.2])
        U2 = hac.DistMatrix([1.0, 3.0, 3.0])

        data = ((k0,U0),(k1,U1),(k2,U2))
        for dK,expU in data:
            hc  = hac.HAC(L,dK=dK)
            acs = hc.generate(M,Q)
            self.assertEqual(1, len(acs), 'too many results for dK=' + str(dK))
            U   = ult.ultrametric(acs[0], 3, dK)
            self.assertEqual(expU,U)
        
