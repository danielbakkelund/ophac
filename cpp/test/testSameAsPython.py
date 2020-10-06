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


import ophac.rnd        as rnd
import ophac.hac_untied as hac
import time
import json
import os
import subprocess as sp

def run_cpp(D,Q,L):
    print('Running C++ clustering...')
    program='./release/lib/ophac_untied'
    input_fname  = '._input.json'
    result_fname = '._result.json'
    
    start = time.time()
    data = {'D':D.dists,
            'Q':Q.quivers,
            'L':L,
            'mode':'untied'}

    with open(input_fname, 'w') as outf:
        json.dump(data,outf)

    cpp_start = time.time()
    proc  = sp.Popen([program, input_fname, result_fname],
                     stdout=sp.PIPE)
    sdata = proc.communicate()[0]

    if proc.returncode != 0:
        raise Exception('Sub-process erred: %s' % str(sdata))

    with open(result_fname, 'r') as inf:
        result = json.load(inf)

    os.remove(input_fname)
    os.remove(result_fname)
        
    cpp_time = time.time() - cpp_start
    print('C++ time: %1.3f s.' % cpp_time)

    ac = hac.AC(dists=result['dists'],
                joins=[tuple(j) for j in result['joins']])
    return ac, cpp_time

def run_python(D,Q,L):
    print('Running ophac HACUntied...')
    py_start = time.time()
    hc = hac.HACUntied(L)
    ac = hc.generate(D,Q)
    py_time = time.time() - py_start
    print('python time: %1.3f s.' % py_time)
    return ac,py_time

def report_diff(cpp,py):
    if cpp.joins != py.joins:
        print('Difference in joins.')
        if len(cpp) != len(py):
            print('Different lengthts!')

    if cpp.dists != py.dists:
        if len(cpp) == len(py):
            import numpy as np
            print('Difference in dists.')
            diff = np.array(cpp.dists) - np.array(py.dists)
            print('Max diff: %1.3e' % np.max(np.abs(diff)))
            
if __name__=='__main__':
    import numpy as np
    
    rnd.seed()

    pyt  = []
    cppt = []
    
    for n in [50,100,200]:
        for p in [0.01,0.05,0.1]:
            for L in ['single','complete']:#,'average']:
                print('N:%d p:%1.3f L:%s' % (n,p,L))
                D,Q = rnd.randomOrderedDissimSpace(N=n,p=p,t=1)
                ac_cpp,tcpp = run_cpp(D,Q,L)
                ac_py,tpy  = run_python(D,Q,L)

                pyt.append(tpy)
                cppt.append(tcpp)

                if ac_cpp != ac_py:
                    print('ERROR.')
                    #print(D)
                    #print(Q)
                    report_diff(ac_cpp,ac_py)
                    print('ac_cpp\n', ac_cpp)
                    print('ac_py\n', ac_py)
                    exit(666)

    print('Jubel!')

    pyt   = np.array(pyt)
    cppt  = np.array(cppt)
    ratio = cppt / pyt
    print('Time ratios cpp/py: min:%1.4f max:%1.4f mean:%1.4f median:%1.4f' %
          (np.min(ratio), np.max(ratio), np.mean(ratio), np.median(ratio)))
