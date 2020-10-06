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


import upyt.unittest   as ut
import ophac.hierarchy as hierarchy
import ophac.dtypes    as dt

class TestNoLinkageSmoke(ut.UnitTest):
    '''
    Smoke test of facade.
    '''

    def test_fig3_5_SL_NoSmoke(self):
        '''
        Figure 3.5 in Jain and Dubes (1988)
        '''
        N     = 5
        dists = [5.8, 4.2, 6.9, 2.6,
                 6.7, 1.7, 7.2,
                 1.9, 5.6,
                 7.6]

        ac = hierarchy.linkage(dists, L='single')
        self.assertTrue(len(ac) == 1)
        
        expJoins = [(1,3),(1,2),(0,2),(0,1)]
        expDists = [1.7, 1.9, 2.6, 4.2]
        expAc    = dt.AC(expJoins, expDists)

        self.assertEquals(expAc, ac[0])

    def testCompletion(self):
        import ophac.ultrametric as ult
        
        D = [1,2,3]
        G = [[2],[],[]]
        L = 'single'
        K = 2.0

        acs = hierarchy.linkage(D,G,L,K=K)
        self.assertEquals(1, len(acs), 'Too many results.')
        
        expectedUltrametric = dt.DistMatrix([1.0, 3.0, 3.0])
        actualUltrametric   = ult.ultrametric(acs[0], 3, K)
        self.assertEquals(expectedUltrametric, actualUltrametric)

class TestNoParallelLinkageSmoke(ut.UnitTest):
    '''
    Smoke test of facade.
    '''

    def test_fig3_5_SL_NoSmoke(self):
        '''
        Figure 3.5 in Jain and Dubes (1988)
        '''
        N     = 5
        dists = [5.8, 4.2, 6.9, 2.6,
                 6.7, 1.7, 7.2,
                 1.9, 5.6,
                 7.6]
        L='single'

        acs = hierarchy.approx_linkage(dists,L=L,n=10,procs=4)
        self.assertTrue(len(acs) == 1)

        expJoins = [(1,3),(1,2),(0,2),(0,1)]
        expDists = [1.7, 1.9, 2.6, 4.2]
        expAc    = dt.AC(expJoins, expDists)

        self.assertEquals(expAc, acs[0])

    def testCompletion(self):
        import ophac.ultrametric as ult
        
        D = [1,2,3]
        G = [[2],[],[]]
        L = 'single'
        K = 2.0

        acs = hierarchy.approx_linkage(D,G,L,K=K)
        self.assertEquals(1, len(acs), 'Too many results.')
        
        expectedUltrametric = dt.DistMatrix([1.0, 3.0, 3.0])
        actualUltrametric   = ult.ultrametric(acs[0], 3, K)
        self.assertEquals(expectedUltrametric, actualUltrametric)
