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

'''
Convert agglomerative clustering to ultrametric
'''

def ultrametric(ac,N,eps=1e-12):
    '''
    ac  - The ophac.dtypes.AgglomerativeClustering object from HC
    N   - The number of elements being clustered
    eps - The ultrametric completion threshold. Defaults to 1e-12.
    returns a ophac.dtypes.DistMatrix representing an ultrametric over the N elements.
    '''
    import ophac.dtypes as clst
    import itertools

    for i in range(1,len(ac)):
        if not ac.dists[i-1] <= ac.dists[i]:
            raise AssertionError('Join distances not monotone:' + \
                                     ('d[%d]=%1.4f vs d[%d]=%1.4f. %s' % \
                                          (i-1,ac.dists[i-1],i,ac.dists[i],str(ac))))


    K = ac.dists[-1] + eps
    L = N*(N-1)//2
    P = clst.Partition(n=N)
    U = clst.DistMatrix([-1]*L)

    for (i,j),dist in zip(ac.joins,ac.dists):
        pi = P[i]
        pj = P[j]
        for a,b in itertools.product(pi,pj):
            if a < b:
                i1 = a
                i2 = b
            else:
                i1 = b
                i2 = a
            k = U.toLinearIndex(i1,i2)
            U.dists[k] = dist
        P = P.merge(i,j)

    basePartition = P

    while len(P) > 1:
        i,j = (len(P)-2,len(P)-1)
        for a,b in itertools.product(P[i],P[j]):
            if a < b:
                i1 = a
                i2 = b
            else:
                i1 = b
                i2 = a
            k = U.toLinearIndex(i1,i2)
            U.dists[k] = K
        P = P.merge(i,j)

    if U.max() > K: #no ultrametric...
        raise Exception('Will not produce a valid ultrametric: ' +
                        'Max ultrametric distance:%1.3f Given diam(ac) + eps = %1.3f. ' %\
                        (U.max(),K))

    if U.min() < 0: # Not all values are assigned
        raise Exception('Not all values are assigned.')

    U._basePartition = basePartition

    return U

def clone(U):
    '''
    Clones an ultrametric
    '''
    import ophac.dtypes as dt
    U2 = dt.DistMatrix(U)
    U2._basePartition = U._basePartition
    return U2
