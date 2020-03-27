
import ophac.hac         as hac
import ophac.dendrogram  as dend
import ophac.rnd         as rnd
import matplotlib.pyplot as plt

rnd.seed()

# Number of elements
N = 50

# Probability of two random elements to be comparable,
# that is, for a,b in the range [0,19], the probability
# of having an arrow a -> b or b -> a is p.
p = 0.05

# The expected number of tied pairs for each value level
# in the dissimilarity measure
t  = 2

# Generate the dissimilairy measure M and the strict
# partial order Q
M,Q = rnd.randomOrderedDissimSpace(N=N,p=p,t=t)

# Generate a clustering algorithm with complete linkage
hc = hac.HAC('complete')

# Do the clustering -- possibly several best solutions
acs = hc.generate(M,Q)

# Plot the result
fig,axs = plt.subplots(1,len(acs))

# For some stupid reason, the response type from plt.subplots
# depends on the second parameter
if len(acs) == 1:
    axs = [axs]

for ac,ax in zip(acs, axs):
    dend.plot(ac,N,ax=ax)

plt.show()
