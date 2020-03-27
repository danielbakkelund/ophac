
import ophac.hac         as hac
import ophac.dendrogram
import matplotlib.pyplot as plt

'''
Clustering five point set with the following
strict partial order:

 0 --> 1 --> 4
  \          
   \         
    \-->3--> 2

'''

# Number of elemennts
N = 5

# Distance matrix (upper triangular values)
dists = [5.8, 4.2, 6.9, 2.6,
         6.7, 1.7, 7.2,
         1.9, 5.6,
         7.6]

# Dissimilarity object
M  = hac.DistMatrix(dists)

# Order relations (arrows in the diagram)
rel = [(0,1),(0,3),(1,4),(3,2)]

# Partial order object
Q = hac.Quivers(relation=rel, n=N)

# Clustering algorithm with single linkage
hc = hac.HAC('single')

#Run the clustering
ac = hc.generate(M,Q)

# Plot the result
fig,ax = plt.subplots(1,1)

ophac.dendrogram.plot(ac[0], N)

plt.show()

