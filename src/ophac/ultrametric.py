'''
Convert agglomerative clustering to ultrametric
'''

def ultrametric(ac,N,maxDist):
    '''
    ac      - The ophac.dtypes.AgglomerativeClustering object from HC
    N       - The number of elements being clustered
    maxDist - The inter-component distance to be assigned to non-mergable components.
              it is adviced that this is set to the set diameter under the given
              dissimilarity measure.
    returns a ophac.dtypes.DistMatrix representing an ultrametric over the N elements.
    '''
    import ophac.dtypes as clst
    import itertools

    for i in range(1,len(ac)):
        if not ac.dists[i-1] <= ac.dists[i]:
            raise AssertionError('Join distances not monotone:' + \
                                     ('d[%d]=%1.4f vs d[%d]=%1.4f. %s' % \
                                          (i-1,ac.dists[i-1],i,ac.dists[i],str(ac))))

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
            U.dists[k] = maxDist
        P = P.merge(i,j)

    if U.max() > maxDist: #no ultrametric...
        raise Exception('Will not produce a valid ultrametric: ' +
                        'Max ultrametric distance:%1.3f Given maxDist:%1.3f. ' %\
                        (U.max(),maxDist))

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

def norm(ac,N,K,p):
    '''
    Computes the p-norm of the (partial) dendrogram.
    ac - AgglomerativeClustering object
    N  - Number of elements in the base space
    K  - Completion level
    p  - order of the norm
    '''
    try:

        import ophac.dtypes as dt
        A = (K**p)*(N*(N-1)//2)
        B = 0
        P = dt.Partition(n=N)
        for ((i,j),d) in zip(ac.joins,ac.dists):
            a = P[i]
            b = P[j]
            B += (K**p - d**p)*len(a)*len(b)
            P = P.merge(i,j)
        return (2**(1.0/p))*((A - B)**(1.0/p))

    except OverflowError:
        U = ultrametric(ac,N,K)
        return U.norm(p)
