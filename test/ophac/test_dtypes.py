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

import ophac.dtypes as clst
import unittest as ut

class PartitonTest(ut.TestCase):

    def testMerge(self):
        p0 = clst.Partition(n=6)

        p1 = p0.merge(2,5)
        e1 = clst.Partition(data=[[0],[1],[2,5],[3],[4]])
        self.assertEqual(e1, p1)

        p2 = p1.merge(0,3)
        e2 = clst.Partition(data=[[0,3],[1],[2,5],[4]])
        self.assertEqual(e2, p2)

        p3 = p2.merge(1,2)
        e3 = clst.Partition(data=[[0,3],[1,2,5],[4]])
        self.assertEqual(e3, p3)

        p4 = p3.merge(1,2)
        e4 = clst.Partition(data=[[0,3],[1,2,4,5]])
        self.assertEqual(e4, p4)

        p5 = p4.merge(0,1)
        e5 = clst.Partition(data=[[0,1,2,3,4,5]])
        self.assertEqual(e5, p5)

    def testEqualsOrNotOperators(self):
        p0 = clst.Partition(n=6)
        p1 = clst.Partition(n=6)
        p0 = p0.merge(2,3)
        p1 = p1.merge(2,3)
        self.assertTrue(p1 == p0)
        self.assertFalse(p1 != p0)

        p2 = p0.merge(0,1)
        self.assertTrue(p1 != p2)
        self.assertFalse(p1 == p2)
        

    def testContainmentAndAccess(self):
        p = clst.Partition(n=6).merge(2,4)
        self.assertTrue([0] in p)
        self.assertTrue([2,4] in p)
        self.assertFalse([2] in p)

        self.assertEqual([2,4], p[2])
        self.assertEqual([5], p[4])

class DistMatrixTest(ut.TestCase):

    def testFromDissim(self):
        dMap = {(0,1):1.0, (2,3):1.5, (4,5):1.0}
        dist = lambda i,j : dMap.get((i,j), 8.0)
        res  = clst.DistMatrix.fromDissimilarity(6, dist)

        exp = clst.DistMatrix([1.0, 8.0, 8.0, 8.0, 8.0,
                               8.0, 8.0, 8.0, 8.0,
                               1.5, 8.0, 8.0,
                               8.0, 8.0,
                               1.0])

        self.assertEqual(exp,res)

    def testNorm(self):
        import math
        M = clst.DistMatrix([1, 1, 1,
                             1, 1,
                             1])
        self.assertEqual(12, M.norm(1))
        self.assertEqual(math.sqrt(12), M.norm(2))
        
        N = M/M.norm(3)
        self.assertEqual(1.0, N.norm(3))

    def testInSet(self):
        M1 = clst.DistMatrix([1,2,3,4,5,6])
        M2 = clst.DistMatrix([1,2,3,4,5,6])
        S  = set([M1,M2])
        self.assertEqual(1, len(S), 'Should only have one element here.')

        M1 = clst.DistMatrix([1,2,3,4,5,6])
        M2 = clst.DistMatrix([1,1,3,4,5,6])
        S  = set([M1,M2])
        self.assertEqual(2, len(S), 'Should have two elements here.')
        

    def testSum(self):
        M1 = clst.DistMatrix([1,2,3,4,5,6])
        M2 = clst.DistMatrix([2,3,4,5,6,7])
        M3 = clst.DistMatrix([3,5,7,9,11,13])
        self.assertEqual(M3, M1+M2)

        M4 = clst.DistMatrix([1,1,1,1,1,1])
        self.assertEqual(M4, M2-M1)


    def testScalarMult(self):
        M1 = clst.DistMatrix([1,2,3,4,5,6])
        M2 = clst.DistMatrix([3,6,9,12,15,18])
        self.assertEqual(M2, M1*3, 'Right mult failed.')
        self.assertEqual(M2, 3*M1, 'Left mult failed')

    def testScalarDiv(self):
        M1 = clst.DistMatrix([3,6,9,12,15,18])
        M2 = clst.DistMatrix([1,2,3,4,5,6])
        self.assertEqual(M2, M1/3)

class BasicLinkageTest(ut.TestCase):

    def testSlMerge(self):
        dMap = {(0,1):1.0, (2,3):1.5, (4,5):1.0}
        dist = lambda i,j : dMap.get((i,j), 8.0)
        M    = clst.DistMatrix.fromDissimilarity(6, dist)
        lnk  = clst.BasicLinkage(clst.SingleLinkage())

        M_01 = lnk(0, 1, M)
        E_01 = clst.DistMatrix([8.0, 8.0, 8.0, 8.0,
                                1.5, 8.0, 8.0,
                                8.0, 8.0,
                                1.0])
        self.assertEqual(E_01, M_01, 'M_01')

        M_01_45 = lnk(3,4,M_01)
        E_01_45 = clst.DistMatrix([8.0, 8.0, 8.0,
                                   1.5, 8.0, 
                                   8.0])
        self.assertEqual(E_01_45, M_01_45, 'M_01_45')


class QuiversTest(ut.TestCase):

    def testQuiversPath(self):
        n = 5
        rel = [[0,1],[0,2],[1,3],[2,3],[2,4]]
        Q = clst.Quivers(n=n,relation=rel)

        hasPaths = [(0,1),(0,3),(0,2),(2,3),(1,3),(0,4)]
        for a,b in hasPaths:
            self.assertTrue(Q.hasPath(a,b),'%d->%d' % (a,b))

        noPaths = [(1,2),(3,1),(2,0),(4,2),(1,4),(3,4)]
        for a,b in noPaths:
            self.assertTrue(not Q.hasPath(a,b), 'not %d->%d' % (a,b))

    def testQuiversLoop(self):
        n   = 4
        rel = [(0,1),(0,2),(1,3),(2,3),(0,0)]
        Q   = clst.Quivers(n=n, relation=rel)
        self.assertTrue(Q.hasCycle())

    def testTransitiveClosureOfTotalOrder(self):
        n   = 5
        rel = [(0,1),(1,2),(2,3),(3,4)]
        exp = [[1,2,3,4],[2,3,4],[3,4],[4],[]]
        Q   = clst.Quivers(n=n, relation=rel).transitiveClosure()
        res = [Q[i] for i in range(len(Q))]
        self.assertEqual(exp,res)

    def testTransitiveClosureOfDiamondPlusIsolatedVertex(self):
        n   = 5
        rel = [(0,1),(0,2),(1,3),(2,3)]
        exp = [[1,2,3],[3],[3],[],[]]
        Q   = clst.Quivers(n=n, relation=rel).transitiveClosure()
        res = [Q[i] for i in range(len(Q))]
        self.assertEqual(exp,res)

    def testTransitiveClosureWithCycle(self):
        n   = 4
        rel = [(0,1),(1,2),(2,3),(3,0)]
        exp = [[0,1,2,3]]*4
        Q   = clst.Quivers(n=n,relation=rel).transitiveClosure(lenient=True)
        res = Q.quivers
        self.assertEqual(exp,res)
        
class AggClustTest(ut.TestCase):

    def testGetItem(self):
        joins = [(1,2),(4,5),(0,1),(3,9)]
        dists = [1,2,3,4]
        ac    = clst.AgglomerativeClustering(joins,dists)
        for i in range(len(ac)):
            eac = clst.AgglomerativeClustering(joins[:i], dists[:i])
            self.assertEqual(eac, ac[:i])
