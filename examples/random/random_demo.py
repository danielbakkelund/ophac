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

from mpl_toolkits.mplot3d import Axes3D
import matplotlib.pyplot  as plt
import numpy              as np
import multiprocessing    as mp
import time
import logging
import sys

import ophac.hac  as hac
import ophac.rnd  as rnd
import ophac.args as args

args = args.args(kws={'N':list, 'P':float, 'T':list, 'C':int, 'L':str,
                      'logLevel':str, 'numProcs':int},
                 defaults={'N':[25,75,125,200], 
                           'T':[1,2,3,4], 'L':'complete',
                           'P':0.1, 'C':1, 'logLevel':'ERROR',
                           'numProcs':4})
args.parse()
print(args)

N = args.N
T = args.T
P = args.P
C = args.C

logging.basicConfig(level=getattr(logging, args.logLevel.upper()))
rnd.seed()

N,T = np.meshgrid(N,T)

totRuns = N.shape[0]*N.shape[1]*C
print('Running %d samples for each combination, a total of %d runs.' % (C,totRuns))
print('Expected running time: %d s.' % (C*31))

Z   = np.zeros((N.shape[0],N.shape[1],C), dtype=float)

allStart = time.time()
numRuns  = N.shape[0]*N.shape[1]*C
reportAt = np.linspace(0,numRuns,10, dtype=int)
runNo    = 0

def runClustering(dists, quivs, i, j, c):
    M = hac.DistMatrix(dists)
    Q = hac.Quivers(quivs)
    hc = hac.HAC(args.L)
    start = time.time()
    hc.generate(M,Q)
    return (i,j,c, time.time() - start)

def genSpace(i,j,c):
    n = N[i,j]
    p = P
    t = T[i,j]

    ######################################################
    # This is where we generate random data
    # N - Number of elements in the ordered set
    # p - Probability of two elements in the set to be
    #     directly comparable
    # t - Expected number of ties pr dissimilarity level
    #     in the generated dissimilarity measure

    M,Q = rnd.randomOrderedDissimSpace(n,p,t)

    print('N: %d t: %d #sp(M): %d' % 
          (n,t,len(M.spectrum(False))))

    # M - The generated dissimilarity measure (DistMatrix)
    # Q - The generated ordered set (Quivers)
    ######################################################

    return M.dists, Q.quivers, i, j, c

pool = mp.Pool(processes=args.numProcs)

print('Generating spaces...')
MQ   = []
ress = []
for c in range(C):
    for i in range(N.shape[0]):
        for j in range(N.shape[1]):
            ress.append(pool.apply_async(genSpace, (i,j,c)))
                    
for res in ress:
    dists,quivs,i,j,c = res.get()
    MQ.append([i,j,c,
               hac.DistMatrix(dists), 
               hac.Quivers(quivs)])

MQ = sorted(MQ, key=lambda x : x[3].n, reverse=True)

print('Clustering...')
ress = []    
for i,j,c,M,Q in MQ:
    ress.append(pool.apply_async(runClustering, (M.dists, Q.quivers, i, j, c)))

for res in ress:
    i,j,c,duration = res.get()
    sys.stdout.write('N=%d T=%d --> ' % (N[i,j],T[i,j]))
    Z[i,j,c] = duration
    print('%1.3f s.' % duration)
    runNo += 1
    if runNo in reportAt:
        perRun = runNo/numRuns*100
        print('%1.1f %% of runs completed.' % perRun)

# Compute mean durations
Z = np.median(Z, axis=2)

fig = plt.figure()
ax  = fig.gca(projection='3d')
ax.set_xlabel('# elements in set')
ax.set_ylabel('# ties pr level')
ax.set_zlabel('median duration (s.)')

ax.text2D(0.05, 0.95, 
          'Execution times after %d samples in each data point' % C,
          transform=ax.transAxes)

surf = ax.plot_wireframe(N,T,Z, cmap='rainbow')

allDuration = time.time() - allStart
print('Accumulated clustering time: %1.3f s.' % Z.sum())
print('Total running time         : %1.3f s.' % allDuration)

plt.show()
