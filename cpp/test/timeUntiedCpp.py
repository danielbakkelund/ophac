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

import ophac.args       as args
import ophac.rnd        as rnd
import ophac.hac_untied as hac
import time
import json
import os
import subprocess

args=args.args(kws={'n':int,'p':float,'L':str},
               defaults={'n':200,'p':0.02,'L':'single'})
args.parse()

print(args)

program='./release/lib/ophac_untied'

print('Generating random space...')
rnd.seed()
rnd_start = time.time()
D,Q = rnd.randomOrderedDissimSpace(N=args.n, p=args.p, t=1)
rnd_time = time.time() - rnd_start
print('Random space generation took %1.3f s.' % rnd_time)


input_fname  = '._input.json'
result_fname = '._result.json'

print('Running C++ clustering...')
start = time.time()
data = {'D':D.dists,
        'Q':Q.quivers,
        'L':args.L,
        'mode':'untied'}

with open(input_fname, 'w') as outf:
    json.dump(data,outf)

cpp_start = time.time()
process = subprocess.Popen([program, input_fname, result_fname],
                           stdout=subprocess.PIPE, 
                           stderr=subprocess.PIPE)
stdout, stderr = process.communicate()
stdout, stderr
cpp_time = time.time() - cpp_start

with open(result_fname, 'r') as inf:
    result = json.load(inf)

print('Time: %1.3f s.' % cpp_time)
