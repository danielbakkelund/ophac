import ophac.hac as hac
import time
import datetime

with open('examples/benchmark/M.dat', 'r') as inf:
    M = eval(inf.readline())
with open('examples/benchmark/Q.dat', 'r') as inf:
    Q = eval(inf.readline())

L = ['single', 'average', 'complete']
T = []
for lnk in L:
    print(lnk + ' linkage...')
    hc = hac.HAC(lnk)
    start = time.time()
    hc.generate(M,Q)
    duration = time.time() - start
    print('duration: %1.0f s.' % duration)
    T.append(duration)

frm  = lambda x : '%1.0f' % x
date = str(datetime.date.today())

L.insert(0, 'date')
T = map(frm, T)
T.insert(0, date)
print('summary:')
print(','.join(L))
print(','.join(T))
