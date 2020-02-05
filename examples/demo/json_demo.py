
import matplotlib.pyplot  as plt

import ophac.hac          as hac
import ophac.json_support as jsn
import ophac.dendrogram   as dnd

inputFname='examples/demo/input.json'
M,Q = jsn.loadDissimSpace(fname=inputFname)

print('%d point space' % len(Q))

hc_sl  = hac.HAC('single')
acs_sl = hc_sl.generate(M,Q)

hc_al  = hac.HAC('average')
acs_al = hc_al.generate(M,Q)

hc_cl  = hac.HAC('complete')
acs_cl = hc_cl.generate(M,Q)

mx = max(acs_sl[0].dists[-1],
         acs_al[0].dists[-1],
         acs_cl[0].dists[-1])
         
print('mx: %1.3f' % mx)

fig,ax = plt.subplots(1,3)

dnd.plot(acs_sl[0], len(Q), ax=ax[0])
ax[0].set_title('single linkage')
ax[0].set_ylim([0,1])

print('#SL -> %d' % len(hac.merge(hac.Partition(n=13), acs_sl[0].joins)))
print('#AL -> %d' % len(hac.merge(hac.Partition(n=13), acs_al[0].joins)))
print('#CL -> %d' % len(hac.merge(hac.Partition(n=13), acs_cl[0].joins)))

dnd.plot(acs_al[0], len(Q), ax=ax[1])
ax[1].set_title('average linkage')
ax[1].set_ylim([0,1])

dnd.plot(acs_cl[0], len(Q), ax=ax[2])
ax[2].set_title('complete linkage')
ax[2].set_ylim([0,1])

plt.tight_layout()
plt.show()
