'''
Module for generation of random data structures.
'''

def seed(s=None):
    import time
    import numpy.random as rnd
    import random
    if s is None:
        s = int(time.time())
        rnd.seed(s)
        random.seed(s)
    else:
        rnd.seed(s)
        random.seed(s)

def randomOrderedDissimSpace(N,p,t,d1=1,steps=[1]):
    '''
    Returns a strictly ordered set of N elements where the probability
    for (i,j) in R is p, and where the expected number of ties on
    each value level is t.

    return (Q,M)
    '''
    return (randomOrder(N,p), 
            randomDissimilarity(N,t,d1,steps))

def randomOrder(N,p):
    '''
    Generates an order where the initial comparability
    matrix has exactly probability p for two elements to
    be comparable; i.e. sum(Q)/(N*(N-1)/2)=p.
    '''
    import ophac.dtypes as dt
    import numpy        as np
    from numpy.random import permutation as perm
    n      = int(round(N*(N-1)//2*p))
    q      = np.zeros((N*(N-1)//2,), dtype=int)
    q[0:n] = 1
    q      = perm(q)
    quivs  = [list() for _ in range(N)]
    M      = dt.DistMatrix(list(q))
    for i in range(N):
        for j in range(i+1,N):
            if M[i,j] == 1:
                quivs[i].append(j)

    return dt.Quivers(quivs)
    

def randomOrder_old(N,p):
    import ophac.dtypes as dt
    from random import random as rnd
    from numpy.random import permutation as permute

    assert 0 <= p and p <= 1

    perm = permute(range(N))
    q    = [[] for _ in range(N)]
    for i in range(N):
        for j in range(i+1,N):
            if rnd() <= p:
                q[perm[i]].append(perm[j])

    return dt.Quivers(quivers=q)


def randomDissimilarity(N,n,d1=1,steps=[1],scale=0.0):
    '''
    N     - Number of elements
    n     - The expected value of number of equal values on each
            dendrogram level following a uniform distribution.
    d1    - The lowest value in the dissimilarity matrix.
            Default: 1
    steps - Array of increments to be cycled
            Default: [1]
    scale - Standard deviaton of normal noise to add to the distances.
            Default: 0.0
    '''
    from ophac.dtypes     import DistMatrix
    from numpy.random     import random      as rnd
    from numpy.random     import permutation as perm
    from numpy.random     import normal      as noise
    import itertools

    M = N*(N-1)//2
    indices = list(range(0,M))
    result  = [-1]*M
    
    incs = itertools.cycle(steps)
    val  = d1
    while len(indices) > 0:
        m = max(1,int(rnd()*n*2))
        k = min(m,M)
        L = min(len(indices),k)
        I = perm(len(indices))[:L]
        I = sorted(I, reverse=True)
        for i in I:
            result[indices[i]] = val + noise(scale=scale)
            del indices[i]
        val += next(incs)

    return DistMatrix(result)


def genRandomUltrametrics(L,N,p,t,C):
    '''
    Generates C ultrametrics by clustering random orders
    using the specified linkage.
    L   - Linkage model
    N   - Number of elements in sample
    p   - Probability of an edge
    t   - Expected tie number
    C   - Number of samples to produce
    '''
    import ophac.ultrametric as ult
    import ophac.hac         as hac
    import logging

    log = logging.getLogger(__name__ + genRandomUltrametrics.__name__)
    log.warning('DEPRECATED --- use genRandomUltrametric(...) in stead.')
    
    result = []
    hc     = hac.HAC(L)
    for _ in range(C):
        Q,M = randomOrderedDissimSpace(N,p,t)
        ac  = hc.generate(Q,M)[0]
        result.append(ult.ultrametric(ac,N,M.max()))
    return result


def randomDendrogram(N,t):
    '''
    Generates dendrograms.
    N   - Number of elements in sample
    t   - Expected tie ratio
    '''
    import ophac.dtypes                      as dt
    import ophac.ultrametric                 as ult
    from numpy.random     import random      as rnd
    from numpy.random     import permutation as perm
    
    M     = N*(N-1)//2
    X     = dt.Partition(n=N)
    joins = []
    dists = []
    
    dist = 1.0
    while len(X) > 1:
        eTies = len(X)*t
        m = max(2,int(rnd()*eTies*2))
        k = min(m,M)
        L = min(len(X),k)
        I = perm(len(X))[:L]
        I = sorted(I)
        i0 = I[0]
        for i in I[1:][::-1]:
            joins.append((i0,i))
            dists.append(dist)
            X = X.merge(i0,i)
        dist += 1

    return dt.AC(joins,dists)

def randomUltrametric(N,t):
    '''
    Generates C ultrametrics by clustering random orders
    using the specified linkage.
    N   - Number of elements in sample
    t   - Expected tie ratio
    C   - Number of ultrametrics to produce
    '''
    import ophac.dtypes      as dt
    import ophac.ultrametric as ult

    ac = randomDendrogram(N,t)
    assert len(ac) == N-1
    return ult.ultrametric(ac, N, ac.dists[-1])
        
def random2ClusterDissimilarity(n,dist,var):
    import numpy.linalg as npl
    import ophac.dtypes as dt
    C1,C2,C,pi = _gen2DClusters(dist,var,n)
    dists = []
    for i in range(len(C)):
        for j in range(i+1,len(C)):
            dists.append(npl.norm(C[i,:] - C[j,:]))

    return dt.DistMatrix(dists),C1,C2,pi

def _genCluster(center, var, n):
    import numpy as np
    from numpy.random import multivariate_normal as mult_norm 
    covar = np.eye(len(center))*var
    return mult_norm(center, covar, size=n)
    
def _gen2DClusters(d,var,n):
    '''
    d   - distance between clusters
    var - variance in locations
    n   - size of each cluster
    '''
    import numpy as np
    N1 = n//2
    N2 = n - N1
    C0 = _genCluster([0,0], var, N1)
    C1 = _genCluster([d,0], var, N2)
    C  = np.concatenate((C0,C1))
    
    pi = np.random.permutation(C.shape[0])
    CC = np.zeros_like(C)
    for i in range(C.shape[0]):
        CC[pi[i],:] = C[i,:]

    return C0,C1,CC,pi
