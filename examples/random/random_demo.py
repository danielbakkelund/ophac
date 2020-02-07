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
import time
import sys

import ophac.hac as hac
import ophac.rnd as rnd

rnd.seed()

N = [10, 20, 30, 40] # Set sizes
P = 0.1              # Probability for two random elements to be directly comparable
T = [1,2,3,4]        # Expected number of ties pr level in the dissimilarity

N,T = np.meshgrid(N,T)

C = 1 # Number of samples for each combination
if len(sys.argv) > 1:
    C = int(sys.argv[1])
    totRuns = N.shape[0]*N.shape[1]*C
    print('Running %d samples for each combination, a total of %d runs.' % (C,totRuns))
    print('Expected running time: %d s.' % (C*20))

Z   = np.zeros((N.shape[0],N.shape[1],C), dtype=float)

allStart = time.time()
numRuns  = N.shape[0]*N.shape[1]*C
reportAt = np.linspace(0,numRuns,10, dtype=int)
runNo    = 0

for c in range(C):
    for i in range(N.shape[0]):
        for j in range(N.shape[1]):

            ######################################################
            # This is where we generate random data
            # N - Number of elements in the ordered set
            # P - Probability of two elements in the set to be
            #     directly comparable
            # T - Expected number of ties pr dissimilarity level
            #     in the generated dissimilarity measure

            Q,M = rnd.randomOrderedDissimSpace(N[i,j],P,T[i,j])

            #
            ######################################################

            hc  = hac.HAC('complete')

            sys.stdout.write('N=%d T=%d --> ' % (N[i,j],T[i,j]))
            start = time.time()
            hc.generate(M,Q)
            duration = time.time() - start
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
print('Total duration: %1.3f s.' % allDuration)

plt.show()
