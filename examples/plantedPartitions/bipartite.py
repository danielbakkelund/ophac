
import ophac.rnd  as rnd
import ophac.hac  as hac
import ophac.args as args
import numpy      as np
import itertools
import matplotlib.pyplot as plt

args = args.args(kws={'N':int,'p':float,'dEq':float,
                      'dDiff':float,'s':float, 'L':str, 'plot':bool},
                 defaults={'N':5,'p':0.8,'dEq':0.1,
                           'dDiff':1.0,'s':0.01, 'L':'complete', 'plot':False})
args.parse()

Q0     = hac.Quivers([[3],[4,5],[5],[],[],[]])
M,Q,P0 = rnd.plantedPartition(Q0, args.N, args.p, args.dEq, args.dDiff, args.s)

hc  = hac.HAC(args.L)
acs = hc.generate(M,Q)
ac  = acs[0]
print('%d results.' % len(acs))

fig,axs = plt.subplots(1,len(acs))
if len(acs) == 1:
    axs = [axs]
    
for ac,ax in zip(acs,axs):
    print('%d joins.' % len(ac))
    
    PP = [hac.merge(hac.Partition(n=len(Q)), ac.joins[:i+1]) for i in range(len(ac))]
    print('Minimal partition has %d blocks.' % len(PP[-1]))
    i  = np.argwhere(np.array([len(P) for P in PP]) == len(P0))[0][0]
    print('Number match at merge', i+1, 'with dist', ac.dists[i])
    P1 = PP[i]
    QQ = [hac.merge(Q, ac.joins[:i+1]) for i in range(len(ac))]
    Q1 = QQ[i]

    print('Planted :', P0)
    print('Obtained:', P1)
    print('Planted :', Q0)
    print('Obtained:', Q1)

    if P1 == P0:
        print('Planted partition recovered exactly.')

    if Q1 == Q0:
        print('Induced order recovered exactly.')

    def jaccard(a,b):
        if len(a) == 0 and len(b) == 0:
            return 1.0
        if len(a) == 0 or len(b) == 0:
            return 0.0
            
        sa = set(a)
        sb = set(b)
        return len(sa & sb)/len(sa | sb)

    def match(Pa,Pb):
        assert len(Pa) == len(Pb)
        match = 0.0
        for x,y in zip(Pa,Pb):
            match += jaccard(x,y)

        return match/len(Pa)

    def bestMatch(p0,p1):
        bm = 0.0
        for perm in itertools.permutations(p1):
            permMatch = match(p0,perm)
            bm = max(permMatch,bm)

        return bm
        


    if P1 != P0:
        print('The partitions match up to %1.4f under permutations.' % bestMatch(P0.data, P1.data))

    if Q1 != Q0:
        print('The orders match up to %1.4f under permutations.' % bestMatch(Q0.quivers, Q1.quivers))


    if args.plot:
        X = np.array(range(len(ac)))
        ax.plot(X,ac.dists)
        xtick = [str(len(P)) for P in PP[1:]]
        ax.set_xticks(X)
        ax.set_xticklabels(X+1)
        ax.set_xlabel('Join number')
        ax.set_ylabel('Dissimiarity')

    
if args.plot:
    plt.tight_layout()
    plt.show()

