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

Dependencies:
 * numpy
 * matplotlib

The code is made to run on both python 2.7+ and  python 3.x

The code can be used as-is, but if you want to have a look at the examples,
you should follow the below recipe.

The examples assume python 3.x.

1) Run               init.sh
2) Source the script setPyPath.sh
3) Try running
   >python -um upyt.discover

This should make your prompt look something along the lines

[dev:ophac] python -um upyt.discover
--------------------------------------------------------------------------------
Running 21 tests.
--------------------------------------------------------------------------------
.....................
--------------------------------------------------------------------------------
Ran 21 tests in 0.017 s.
--------------------------------------------------------------------------------
SUCCEEDED!!!
--------------------------------------------------------------------------------

4) Now, try running
   >python -u examples/demo/json_demo.py

This should present a window containing three partial dendrograms.
It is the clusterings of the data in Section 6 of the article.
The example also shows how to load data from a file (json).

5) Now, try runninng
   >python -u examples/random/random_demo.py 

This may take a while. The program generates random data models and runs
order preserving clustering using complete linkage. At the end of the run,
a 3d-plot shows the correlation between set-sizes, number of ties and running times.

The above command runs one sample for each configuration. By running

   >python -u examples/random/random_demo.py 5

you can have 5 samples generated for each configuratio, but the running time
will be fife times longer, on average.

###############################################################################

For documentation about the data model on a high level, take a look in
the file datamodel.txt, found in the same directory as this README file.
