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

import ophac.ultrametric as ultrametric
import ophac.dtypes      as clust2
import upyt.unittest     as ut

class UltrametricTest(ut.UnitTest):

    def testConvert(self):
        K     = 3 + 1e-12
        N     = 6
        diam  = 4
        joins = [(0,2),(0,1),(1,3),(1,2)]
        dists = [1,1,2,3]
        ultra = [1,1,K,K,K,
                 1,K,K,K,
                 K,K,K,
                 3,2,
                 3]

        ac = clust2.AgglomerativeClustering(joins,dists)
        Mu = ultrametric.ultrametric(ac,N)

        expected = clust2.DistMatrix(ultra)

        self.assertEquals(expected, Mu)

    def testInjectivity(self):
        '''
        Check that K0 = 1e-12 is sufficient for injectivity in the
        range we typically work.
        '''
        N   = 4
        ac1 = clust2.AgglomerativeClustering(joins=[(1,2)], dists=[1.0])
        ac2 = clust2.AgglomerativeClustering(joins=[(2,3),(0,1)], dists=[1.0,1.0])
        U1  = ultrametric.ultrametric(ac1, N, 1e-12)
        U2  = ultrametric.ultrametric(ac2, N, 1e-12)
        self.assertTrue(U1 != U2)
