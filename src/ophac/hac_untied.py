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

from   ophac.dtypes import *
import ophac.ultrametric as ult


def _getLogger(x):
    import logging
    return logging.getLogger(__name__ + '.' + x.__name__)

def HACUntied(lnk):
    import os
    cpp_exe_ev = 'OPHAC_CPP_EXE'
    cpp_dir_ev = 'OPHAC_CPP_FILEDIR'
    if cpp_exe_ev in os.environ and cpp_dir_ev in os.environ:
        from numpy.random import randint
        cpp_exe = os.environ[cpp_exe_ev]
        cpp_dir = os.environ[cpp_dir_ev]
        return HACUntied_cpp(lnk,cpp_exe,cpp_dir)
    else:
        return HACUntied_python(lnk)

class HACUntied_cpp:

    def __init__(self,lnk,cpp_exe,cpp_dir):
        self.log     = _getLogger(HACUntied_cpp)
        self.lnk     = lnk
        self.cpp_exe = cpp_exe
        self.cpp_dir = cpp_dir
        self.log.info('Instantiated with L:%s exe:%s dir:%s',
                      lnk, cpp_exe, cpp_dir)

    def generate(self,dissim,order=None):
        import json
        import os
        import time
        import os.path    as path
        import subprocess as sp
        import uuid

        if order is None:
            order = Quivers(n=dissim.n,relation=[])

        data = {'D':dissim.dists,
                'Q':order.quivers,
                'L':self.lnk,
                'mode':'untied'}

        token  = str(uuid.uuid1())
        ofname = path.join(self.cpp_dir, token + '_input.json')
        ifname = path.join(self.cpp_dir, token + '_result.json')
        
        with open(ofname, 'w') as outf:
            json.dump(data,outf,indent=3)

        self.log.info('Running c++ ophac %s --> %s', ofname, ifname)
        cpp_start = time.time()
        process   = sp.Popen([self.cpp_exe, ofname, ifname], stdout=sp.PIPE, stderr=sp.PIPE)
        std,err   = process.communicate()
        if process.returncode != 0:
            raise Exception('C++ ophac exited with return code %d' %
                            process.returncode)

        if len(std) > 0:
            self.log.info('C++ output:\n%s', std)
        if len(err) > 0:
            self.log.error('C++ error output:\n%s', err)
        
        self.log.info('C++ ophac completed in %1.3f s.', time.time() - cpp_start)

        with open(ifname, 'r') as inf:
            result = json.load(inf)
        
        dists = result['dists']
        joins = [tuple(x) for x in result['joins']]

        os.remove(ofname)
        os.remove(ifname)
        
        return AC(dists=dists,joins=joins)

            
        
class HACUntied_python:

    def __init__(self, lnk):
        '''
        lnk  - Linkage model; one of 'single', 'average' or 'complete'.
        '''
        self.log    = _getLogger(HACUntied_python)
        self.lnk    = lnk
        self._setLinkageFunctionFactory()
        self.log.info('Instantiated with lnk=%s.', lnk)

    def _setLinkageFunctionFactory(self):
        lnkFact = None
        if self.lnk == 'single':
            lnkFact = lambda sizes : BasicLinkage(SingleLinkage())
        elif self.lnk == 'complete':
            lnkFact = lambda sizes : BasicLinkage(CompleteLinkage())
        elif self.lnk == 'average':
            lnkFact = lambda sizes : BasicLinkage(AverageLinkage(sizes))
        else:
            raise Exception('Unknown linkage: "%s"' % self.lnk)

        self._getLinkageFunction = lnkFact

    def generate(self,dissim,order=None):
        '''
        dissim - Dissimilarity measure of type ophac.dtypes.DistMatrix 
        order  - Order relation of type ophac.dtypes.Quivers, 
                 or None for non-ordered clustering.
        '''
        if order is None:
            order = Quivers(n=dissim.n, relation=[])

        P0   = Partition(n=dissim.n)        
        return self._exploreChains(dissim, order, P0, AC())
        
    def _exploreChains(self, dissim, order, partition, ac0):
        '''
        dissim    - dissimilarity measure for the current partition
        order     - Quivers object for the current partition
        partition - Current partition
        ac0       - AgglomerativeClustering object leading up to the 
                    current partition
        '''
        self.log.debug('Exploring set of %d elements.', len(partition))

        if len(order) == 1:
            self.log.debug('Trivial partition reached.')
            return ac0
    
        # Find minimal dissimilarity level to merge on
        dispair = None
        for (d,pair) in dissim.getSortedIndexPairs():
            if dispair is not None:
                break # Has one!

            a,b = pair
            if order.canMerge(a,b):
                self.log.debug('Mergeable pair (%d,%d) of dissim %1.3f found.',
                               a, b, dissim[a,b])
                dispair = (d,pair)

        if dispair is None:
            self.log.debug('No further mergeable pairs --- maximal element reached')
            return ac0
        
        # Get current linkage
        linker = self._getLinkageFunction([len(x) for x in partition])
        
        (dist,(a,b)) = dispair
        self.log.debug('Merging (%d,%d) at dissim %1.3f.', a, b, dist)
        D2  = linker(a,b,dissim)
        P2  = partition.merge(a,b)
        O2  = order.merge(a,b)
        ac2 = ac0 + AC(joins=[(a,b)], dists=[dist])
        if len(ac2) > 1:
            assert ac2.dists[-2] <= ac2.dists[-1]

        return self._exploreChains(D2, O2, P2, ac2)

