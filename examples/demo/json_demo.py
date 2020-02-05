
import matplotlib.pyplot  as plt
import numpy              as np

import ophac.hac          as hac
import ophac.json_support as jsn
import ophac.dendrogram   as dnd

inputFname='examples/demo/input.json'
M,Q = jsn.loadDissimSpace(fname=inputFname)

dK = 1e-12

hc_sl  = hac.HAC('single', dK=dK)
acs_sl = hc_sl.generate(M,Q)

hc_al  = hac.HAC('average', dK=dK)
acs_al = hc_al.generate(M,Q)

hc_cl  = hac.HAC('complete', dK=dK)
acs_cl = hc_cl.generate(M,Q)

mx = max(acs_sl[0].dists[-1],
         acs_al[0].dists[-1],
         acs_cl[0].dists[-1])
         

fig,ax = plt.subplots(2,2)
ax     = np.reshape(ax, (4,))
dnd.plot(acs_sl[0], len(Q), ax=ax[0])
ax[0].set_title('single linkage')
ax[0].set_ylim([0,1])

dnd.plot(acs_al[0], len(Q), ax=ax[1])
ax[1].set_title('average linkage')
ax[1].set_ylim([0,1])

dnd.plot(acs_cl[0], len(Q), ax=ax[2])
ax[2].set_title('complete linkage')
ax[2].set_ylim([0,1])

plt.tight_layout()
plt.show()
