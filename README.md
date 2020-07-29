### Copyright 2020 Daniel Bakkelund

 This program is free software: you can redistribute it and/or modify
 it under the terms of the GNU Lesser General Public License as published by
 the Free Software Foundation, either version 3 of the License, or
 (at your option) any later version.<br>
 This program is distributed in the hope that it will be useful,
 but WITHOUT ANY WARRANTY; without even the implied warranty of
 MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
 GNU Lesser General Public License for more details.<br>
 You should have received a copy of the GNU Lesser General Public License
 along with this program.  If not, see <https://www.gnu.org/licenses/>.

# Dependencies:
 * numpy
 * matplotlib

The library is made to run on python 3.x

The code can be used as-is, just place the src directory in your PYTHONPATH.

However, if you want to have a look at the examples, you should
follow the below recipe.

# Installing (for developers or if you want to view the examples)

## 1) Run
   >init.sh

This script downloads the repository <https://bitbucket.org/Bakkelund/upyt>
containing the unit test library that has been used for the development
of ophac.

## 2) Source the script setPyPath.sh:
   <code>>source setPyPath.sh</code>

The script sets the PYTHONPATH environment variable. The script is
written for UX like platforms, and may work for older versions of
Cygwin as well. The directories to add to PYTHONPATH are as follows
(in case you have to do it manually):

`./src`<br>
`./test`<br>
`./xlibs/upyt/src`<br>

Remember that in PYTHONPATH you must specify these as absolute paths.

## 3) Now, try running
   `>python -um upyt.discover`

This should make your prompt look something along the lines

<code>
>python -um upyt.discover <br>
------------------------------------------------------------------------<br>
Running 21 tests.<br>
------------------------------------------------------------------------<br>
.....................<br>
------------------------------------------------------------------------<br>
Ran 21 tests in 0.017 s.<br>
------------------------------------------------------------------------<br>
SUCCEEDED!!!<br>
------------------------------------------------------------------------<br>
</code>

## 4) Now, try running
   `>python -u examples/demo/json_demo.py`

This should present a window containing three partial dendrograms.
It is the clusterings of the data in Section 6 of the article.
The example also shows how to load data from a file (json).

## 5) Now, try running
   `>python -u examples/random/random_demo.py`

This may take a while. The program generates random data models and runs
order preserving clustering using complete linkage. At the end of the run,
a 3d-plot shows the correlation between set-sizes, number of ties and running times.

The above command runs one sample for each configuration. By running

   `>python -u examples/random/random_demo.py 5`

you can have 5 samples generated for each configuration, but the running time
will be five times longer, on average.

# Data model

For documentation about the data model on a high level, take a look in
the file datamodel.md, found in the same directory as this README file.
