
import ophac.hac         as hac
import ophac.ultrametric as ult
import ophac.rnd         as rnd
import ophac.args        as args

import numpy as np
import time
rnd.seed(int(time.time()))

args = args.args(kws={'N':int, 't':float, 'p':float, 'C':int, 'L':str},
                 defaults={'N':20, 't':4, 'p':0.0, 'C':10, 'L':'complete'},)
args.parse()


def cluster(dists, quivs, link, pred):
    M   = hac.DistMatrix(dists)
    Q   = hac.Quivers(quivs)
    hc0 = hac.HAC(link, pred=pred)
    s0  = time.time()
    ac0 = hc0.generate(M,Q)
    T   = time.time() - s0
    if link == 'average':
        acd = [(ac.joins, roundDists(ac.dists)) for ac in ac0]
    else:
        acd = [(ac.joins, ac.dists) for ac in ac0]
    return T, acd

def roundDists(dists, precision=4):
    return [round(x, precision) for x in dists]

def setsAreEqual(u0s, u1s, eps=0.1):
    if len(u0s) != len(u1s):
        return False

    minDiff = 1e12
    for u in u0s:
        for v in u1s:
            diff = np.max(np.abs((u-v).dists))
            if diff < minDiff:
                minDiff = diff

    return minDiff <= eps

T0 = []
T1 = []
for c in range(args.C):
    print('---   #%3d   ---' % (c+1))
    M,Q = rnd.randomOrderedDissimSpace(args.N, args.p, args.t)

    d0, acd0 = cluster(M.dists, Q.quivers, args.L, False)
    ac0      = [hac.AC(x[0],x[1]) for x in acd0]
    T0.append(d0)
    print('d0: %1.1f s.' % d0)

    d1, acd1 = cluster(M.dists, Q.quivers, args.L, True)
    ac1      = [hac.AC(x[0],x[1]) for x in acd1]
    T1.append(d1)
    print('d1: %1.1f s.' % d1)

    u0 = set([ult.ultrametric(ac, args.N) for ac in ac0])
    u1 = set([ult.ultrametric(ac, args.N) for ac in ac1])

    if not setsAreEqual(u0,u1):
        msg = '---------------  DIFF  -------------------\n'
        msg += 'Different number of solutions %s vs %d.\n' % (len(u0), len(u1))
        msg += str(M) + '\n'
        msg += str(Q) + '\n'
        msg += 'AC0: ' + str(ac0) + '\n'
        msg += 'AC1: ' + str(ac1) + '\n'
        msg += '------------------------------------------'
        print(msg)
    else:
        print('solutions: %d' % len(u0))


print(args)
print('Total time w/o  partial order reduction: %1.1f s. (median: %1.3f s.)' % 
      (np.sum(T0), np.median(T0)))
print('Total time with partial order reduction: %1.1f s. (median: %1.3f s.)' % 
      (np.sum(T1), np.median(T1)))

