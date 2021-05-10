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

import ophac.ultrametric as ult
import ophac.dtypes      as dt
import upyt.unittest     as ut

class UltrametricTest(ut.TestCase):

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

        ac = dt.AgglomerativeClustering(joins,dists)
        Mu = ult.ultrametric(ac,N)

        expected = dt.DistMatrix(ultra)

        self.assertEqual(expected, Mu)

    def testInjectivity(self):
        '''
        Check that K0 = 1e-12 is sufficient for injectivity in the
        range we typically work.
        '''
        N   = 4
        ac1 = dt.AgglomerativeClustering(joins=[(1,2)], dists=[1.0])
        ac2 = dt.AgglomerativeClustering(joins=[(2,3),(0,1)], dists=[1.0,1.0])
        U1  = ult.ultrametric(ac1, N, 1e-12)
        U2  = ult.ultrametric(ac2, N, 1e-12)
        self.assertTrue(U1 != U2)

    def testToPartitionChain(self):
        dists = [
            1, 1, 3, 3,
            1, 3, 3,
            3, 3,
            2
            ]

        expectedData = [
            [[0],[1],[2],[3],[4]],
            [[0,1,2],[3],[4]],
            [[0,1,2],[3,4]],
            [[0,1,2,3,4]]
            ]

        expectedRhos = [0,1,2,3]
        expected = [dt.Partition(data) for data in expectedData]        
        resQ, resRho = ult.toPartitionChain(dt.DistMatrix(dists))

        self.assertEqual(expected, resQ, 'Wrong partitions')
        self.assertEqual(expectedRhos, resRho, 'Wrong partitions')

    def testToPartitionChain2(self):
        dists = [
            1, 1, 2, 2,
            1, 2, 2,
            2, 2,
            1
            ]

        expectedData = [
            [[0],[1],[2],[3],[4]],
            [[0,1,2],[3,4]],
            [[0,1,2,3,4]]
            ]

        expectedRhos = [0,1,2]
        expected = [dt.Partition(data) for data in expectedData]        
        resQ, resRho = ult.toPartitionChain(dt.DistMatrix(dists))

        self.assertEqual(expected, resQ, 'Wrong partitions')
        self.assertEqual(expectedRhos, resRho, 'Wrong partitions')

    def testTreeIdentical(self):
        uDists1 = [
            1, 1, 2, 2,
            1, 2, 2,
            2, 2,
            1
            ]
        uDists2 = [
            1, 1, 2, 2,
            1, 2, 2,
            2, 2,
            1.5
            ]

        self.assertTrue(ult.treeIdentical(dt.DistMatrix(uDists1), 
                                          dt.DistMatrix(uDists1)),
                        'Wrong when equal')

        self.assertFalse(ult.treeIdentical(dt.DistMatrix(uDists1), 
                                          dt.DistMatrix(uDists2)),
                         'Wrong when different')
    
    def testExtendStepWise_fig3_5_SL(self):
        '''
        Figure 3.5 in Jain and Dubes (1988)
        '''
        N     = 5
        joins = [(1,3),(1,2),(0,2),(0,1)]
        dists = [1.7, 1.9, 2.6, 4.2]

        class wrp:
            def __init__(self,U):
                self.U = U
            def __eq__(self,x):
                return (self.U-x.U).norm() < 1e-3
            def __str__(self):
                frm = lambda x : '%1.3f' % x
                return str(list(map(frm,self.U.dists)))
        
        dK = 1.0e-2
        ac = dt.AC()
        U  = ult.ultrametric(ac,N,dK)
        P  = dt.Partition(n=N)
        for i in range(len(dists)):
            P  = P.merge(*joins[i])
            U  = ult.extend(U, P, dists[i], dK)
            ac = ac + dt.AC(joins[i:i+1], dists[i:i+1])
            eU = ult.ultrametric(ac, N, dK)
            self.assertEqual(eU, U, #wrp(eU), wrp(U),
                              'Failed at merge i=%d with P=%s' % (i,str(P)))
