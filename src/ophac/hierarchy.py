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

def _getLogger(thing):
    import logging
    return logging.getLogger(__name__ + '.' + thing.__name__)

def linkage(D, G=None, L='complete', p=1, K=1.0e-12):
    '''
    Performs order preserving hierarchical clustering.
    
    D - Condensed dissimilarity measure. That is, for a set of N elements,
        D is a 1-dimensional array of N(N-1)/2 elements, corresponding to the
        upper half of the dissimilarity matrix laid out row-wise.
    G - Order relation given as a jagged 2D-array as follows:
        if A = G[i] is the i-th array in G, then, for each k in A this is 
        interpreted as i<k in the strict partial order. Default is None,
        meaning that the hierarchical clustering will be performed without
        regard to any order relation.
    L - Linkage function. One of 'single', 'complete' or 'average'.
        Default is 'complete'.
    p - Order of norm. A number greater or equal to 1. Defaults to 1.
    K - The epsilon of the ultrametric completion. Defaults to 1.0e-12.

    The method returns a list of ophac.dtypes.AgglomerativeClusering (AC) objects, 
    each object has two members: "dists" and "joins". The joins hold the order 
    of merges of the clustering, the the dists are the distances for the 
    different joins.

    The AC objects can be passed on as follows to obtain relevant information.
    In the following, ac is an AC object, N is the number of elements in the base set
    and K is the ultrametric completion distance (epsilon). Unless you have used
    a non-default value of K, this may be omitted.

    * To create the corresponding ultrametric:
    import ophaq.ultrametric as ult
    U = ult.ultrametric(ac, N, K)

    * To obtain the k-th partition
    import ophaq.dtypes as dt
    kthPartition = dt.merge(dt.Partition(n=N), ac.joins[:k])

    * To obtain the k-th induced order relation
    import ophac.dtypes as dt
    kthInducedOrder = dt.merge(dt.Quivers(G), ac.joins[:k])

    * To plot the corresponding (partial) dendrogram
    import matplotlib.pyplot as plt
    import ophaq.dendrogram  as dend
    fix,ax = plt.subplots(1,1)
    dend.plot(ac, N, ax=ax)
    plt.show()

    The  dend.plot(...) method uses scipy.cluster.hierarchy.dendrogram for 
    the plotting, and passes any additional arguments on to that method.
    '''
    import ophac.hac as hac
    import numpy     as np
    import time
    
    log = _getLogger(linkage)

    if np.min(D) < 0:
        msg = 'Negative dissimilarity coefficients detected.'
        log.error(msg)
        raise ValueError(msg)
    
    M = hac.DistMatrix(D)
    log.info('Clustering %d elements.', M.n)
    Q = None
    if G:
        Q = hac.Quivers(G)
    else:
        log.info('No order relation specified.')
        Q = hac.Quivers(relation=[], n=M.n)

    start    = time.time()
    hc       = hac.HAC(lnk=L, ord=p, dK=K)
    acs      = hc.generate(M,Q)
    duration = time.time() - start
    log.info('Produced %d equivalent clusterings in %1.3f s.', len(acs), duration)
    return acs

    
def approx_linkage(D, G=None, L='single', n=10, mode='rndpick', procs=4, p=1, K=1e-12):
    '''
    Produces an order preserving hierarchical clustering of (M,Q) using parallel 
    processing with a number of processes and a number of samples to generate.

    The algorithm applies a level of noise to the dissimilarity measure to ensure 
    there are no initial tied connections, causing each run to be a polynomial 
    time algorithm for all linkage models. The clusterings are run in parallel, 
    and the returned resulst is the set of optimal clusterings.

    For each optimal (noise perturbated) solution, a de-noised version is produced
    by re-playing the joins on the original dissimilarity measure.
    
    n      - The number of samples to run.
    procs  - Number of processes to run in parallel. Defaults to 4.
    mode   - The approximation mode to use.
             untied  - add noise to the dissimilarity and run un-tied
             rndpick - resolve ties by picking a random pair
             Default is rndpick.

    For the other parameters, se "linkage".

    Returns a list of AC objects, one for each equivalently optimal solution.
    In general, it is expeted that there is only one optimal solution, due to
    the noise added to the dissimilarities, but then again...
    '''
    import multiprocessing as mp
    import numpy           as np
    import ophac.hac       as hac
    import time

    log = _getLogger(approx_linkage)

    if np.min(D) < 0:
        msg = 'Negative dissimilarity coefficients detected.'
        log.error(msg)
        raise ValueError(msg)

    
    # Convert types to serialisable ones
    mm = D
    if isinstance(mm,hac.DistMatrix):
        mm = mm.dists

    log.info('Clustering %d elements %d times using %d processors.',
            hac.DistMatrix(mm).n, n, procs)

    qq = G
    if isinstance(qq,hac.Quivers):
        qq = G.quivers

    if qq is None:
        qq = [list()]*hac.DistMatrix(mm).n
        
    approx_method = None
    if mode == 'untied':
        approx_method = _untied_linkage
    elif mode == 'rndpick':
        approx_method = _rndpick_linkage
    else:
        raise Exception('Unknown approximation mode: "' +  mode + '"')

    CPP_MAX_UINT = 4294967294
    
    seed = np.random.randint(CPP_MAX_UINT, size=n)
    data = [(mm,qq,L,int(s)) for s in seed]
    with mp.Pool(processes=procs) as pool:
        results = pool.map(approx_method, data)

    acs      = [hac.AC(j,d) for j,d,_ in results]
    d0       = hac.DistMatrix(mm)

    result = hac._pickBest(d0, acs=acs, ord=p, dK=K)
    if len(result) > 1:
        log.warning('Random clustering resulted in %d equivalent results.', len(result))
        
    return result

def _rndpick_linkage(XX):
    import ophac.dtypes     as dt
    import ophac.hac_approx as hac
    import time
    
    mm,qq,lnk,seed = XX
    log = _getLogger(_rndpick_linkage)
    stt = time.time()
    D   = dt.DistMatrix(mm)
    Q   = dt.Quivers(qq)
    hc  = hac.HACUntied(lnk)
    ac  = hc.generate(D,Q,mode='approx',seed=seed)
    log.info('Time: %1.4f s.', time.time() - stt)
    return (ac.joins,ac.dists,hc.seed_used)

def _p_linkage(XX):
    _getLogger(_p_linkage).warning('Deprecated. use ophac.hierarchy._untied_linkage')
    return _untied_linkage(XX)

def _untied_linkage(XX):
    '''
    Parallel method called by pool.map.
    TODO: consider [gaussian] noise about zero. The current solution
          moves the mass center of the dissimilarity.
    '''
    import numpy            as np
    import ophac.hac_untied as hac
    import time
    
    mm,qq,lnk,_ = XX
    log = _getLogger(_untied_linkage)
    stt = time.time()
    
    N = hac.DistMatrix(mm).n
    
    dd0  = np.array(sorted(set(mm)), dtype=float)
    seps = dd0[1:] - dd0[:-1]
    sep  = np.min(seps)

    srt = time.time()
    rnd = np.random.random(np.shape(mm)) * (sep/(3*N))
    rnt = time.time() - srt

    Q = None
    if qq is not None:
        Q = hac.Quivers(qq)

    M   = hac.DistMatrix(list(mm + rnd))
    hc  = hac.HACUntied(lnk)
    prt = time.time() - stt
    sht = time.time()
    ac  = hc.generate(M,Q,mode='untied')
    ttm = time.time() - sht
    log.info('Time: %1.4f s. (random generation: %1.4f s, prep. time: %1.4f s.)' % \
             (ttm,rnt,prt))

    denoised = list(_dists(ac.joins,mm,lnk))
    return (ac.joins,denoised,ac.seed_used)

def _dists(joins,D,L,precision=30):
    '''
    Produces the join distances for the given joins and the dissimilarity
    for the linkage method specified.

    precision - number of decimals to round off

    Is used to produce un-noised join distancs returned by _p_linkage.
    '''
    import ophac.dtypes as dt
    import numpy        as np

    if not isinstance(D,dt.DistMatrix):
        D = dt.DistMatrix(D)
    
    dists = []
    lfact = dt.getLinkageFactory(L)
    sizes = [1]*D.n
    D1    = dt.DistMatrix(D)    
    for i,j in joins:
        lnk = lfact(sizes)
        d   = D1[i,j]
        D1  = lnk(i,j,D1)
        sizes[i] += sizes[j]
        del sizes[j]

        dists.append(d)

    return np.round(dists, decimals=precision)

