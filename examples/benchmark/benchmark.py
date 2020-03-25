import ophac.hac as hac
import time
import datetime

with open('examples/benchmark/M.dat', 'r') as inf:
    M = eval(inf.readline())
with open('examples/benchmark/Q.dat', 'r') as inf:
    Q = eval(inf.readline())

L      = ['date', 'single', 'average', 'complete']
T      = [str(datetime.date.today())]
format = lambda x : '%1.0f' % x
for lnk in L[1:]:
    print(lnk + ' linkage...')
    hc = hac.HAC(lnk)
    start = time.time()
    hc.generate(M,Q)
    duration = time.time() - start
    print('duration: %1.0f s.' % duration)
    T.append(format(duration))

mlen = 0    
with open('examples/benchmark/log.csv', 'r') as inf:
    line = inf.readline()
    while line != '':
        print(line.strip().replace(',','\t'))
        mlen = max(mlen, len(line))
        line = inf.readline()
                
print('-'*mlen)
print('\t'.join(T))

print('\nAppend to log [y/n] ?')
if raw_input() in ['y','Y']:
    with open('examples/benchmark/log.csv', 'a') as outf:
        outf.write(','.join(T) + '\n')

