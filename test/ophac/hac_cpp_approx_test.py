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


import upyt.unittest    as ut
import ophac.hac_approx as unhac
import ophac.dtypes     as dt

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

        hc = unhac.HACUntied('single')
        ac = hc.generate(dt.DistMatrix(dists), mode='approx', seed=42)
        
        expJoins = [(1,3),(1,2),(0,2),(0,1)]
        expDists = [1.7, 1.9, 2.6, 4.2]
        expAc    = dt.AC(expJoins, expDists)

        self.assertEquals(expAc, ac)

    def testCompletion(self):
        import ophac.ultrametric as ult
        import ophac.dtypes      as dt
        
        D = dt.DistMatrix([1,2,3])
        G = dt.Quivers([[2],[],[]])
        L = 'single'
        K = 2.0

        hc  = unhac.HACUntied(L)
        ac = hc.generate(D,G, mode='approx', seed=42)
        
        expectedUltrametric = dt.DistMatrix([1.0, 3.0, 3.0])
        actualUltrametric   = ult.ultrametric(ac, 3,K)
        self.assertEquals(expectedUltrametric, actualUltrametric)

    def testCmpToHAC(self):
        import ophac.hac        as hac
        import ophac.hac_approx as unhac
        import ophac.rnd        as rnd

        D,G = rnd.randomOrderedDissimSpace(N=100,p=0.01,t=1)

        for L in ['single', 'complete']:
            cl_hc  = hac.HAC(L)
            cl_acs = cl_hc.generate(D,G)
            self.assertEquals(1,len(cl_acs), 'classic hac witb %s linkage failed' % L)

            un_hc = unhac.HACUntied(L)
            un_ac = un_hc.generate(D,G, mode='approx', seed=42)

            self.assertEquals(cl_acs[0], un_ac, 'failed for %s linkage' % L)
