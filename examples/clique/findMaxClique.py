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

'''
This file provides a demonstration of how ophac can be used to find a largest
clique in an undirected graph G=(V,E).
Note that this is an NP-hard problem, so there is little point in running the
demonstration using large datasets...
'''

import ophac.hac         as hac
import ophac.ultrametric as ult
import numpy             as np

# number of vertices
N = 8 

# Edges
# We only specify edges from smallest index to largest.
E = [(0,1),(0,5),
     (1,2),(1,3),
     (2,4),
     (3,4),(3,6),(3,7),
     (4,6),(4,7),
     (5,7),
     (6,7)]


# Graph layout:
# 0 ---- 1 ---- 2
# |      |      |
# |      |      |
# 5      3 ---- 4
#  \     |\   / |
#    \   |  X   |
#      \ |/   \ |
#        7 ---- 6

# This leaves us with maximal clique: 
clique = [3,4,6,7]

# Disimilarity is 1 if there is an edge between
# elements, and 2 otherwise.
def dissim(i,j):
    if i == j:
        return 0.0
    a = min(i,j)
    b = max(i,j)
    if (a,b) in E:
        return 1.0
    else:
        return 2.0
        
# Input dissimilarity measure
D = hac.DistMatrix.fromDissimilarity(N, dissim)

# Use complete linkage
algo = hac.HAC('average')

# Call generate with only a dissimilarity measure
# --> clustering without order relation
solutions = algo.generate(D)

# Compute corresponding ultrametrics
ultrametrics = set([ult.ultrametric(s, N, 1) for s in solutions])

# Should only be one solution
assert len(ultrametrics) == 1

# Convert to numpy array
U = ultrametrics.pop().toNumpyArray()

# Boolean matrix with True whenever U == 1
B = U == 1.0

# Find row with max number of ones
row = B.sum(axis=1).argmax()

# Find clique in row
found = [row]
for j in range(row+1,N):
    if B[row,j]:
        found.append(j)

print('Expected clique: %s' % str(clique))
print('Found    clique: %s' % str(found))
