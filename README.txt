To get the repo up and running, do as follows:

First, notice that this code runs best under python 3.x

1) Run    init.sh
2) Source setPyPath.sh

3) Try runninng
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

4) Now, try runnning
   >python examples/demo/json_demo.py

This should present a window containing three partial dendrograms.
It is the clusterings of the data in Section 6 of the article.
The example also shows how to load data from a file (json).

###############################################################################

For documentation about the data model on a high level, take a look in
the file datamodel.txt, found in the same directory as this README file.
