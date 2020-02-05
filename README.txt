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
   >python demo/article_sample.py

If this seems to run as you expect, you may have a look in the file
 
    demo/exampleUsage.py

for an example of how to make use of the functionality in this repo.
