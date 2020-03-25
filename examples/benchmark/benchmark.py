import ophac.hac as hac
import time
import datetime
import sys

def getInput(prompt='>'):
    try:
        return raw_input(prompt)
    except NameError as e:
        return input(prompt)

with open('examples/benchmark/M.dat', 'r') as inf:
    M = eval(inf.readline())
with open('examples/benchmark/Q.dat', 'r') as inf:
    Q = eval(inf.readline())

L      = ['date', 'single', 'average', 'complete']
T      = [str(datetime.date.today())]
format = lambda x : '%1.1f' % x
for lnk in L[1:]:
    print(lnk + ' linkage...')
    hc = hac.HAC(lnk)
    start = time.time()
    hc.generate(M,Q)
    duration = time.time() - start
    T.append(format(duration))
    print('duration: %s s.' % T[-1])

mlen = 0    
with open('examples/benchmark/log.csv', 'r') as inf:
    line = inf.readline()
    while line != '':
        print(line.strip().replace(',','\t'))
        mlen = max(mlen, len(line))
        line = inf.readline()
                
print('-'*(mlen+15)) # Compensate for tab stops
print('\t'.join(T))

print('\nAppend to log [y/n] ?')
if getInput() in ['y','Y']:
    print('Please provide a comment:')
    cmt = getInput('>')
    T.append(cmt)
    with open('examples/benchmark/log.csv', 'a') as outf:
        outf.write(','.join(T) + '\n')

