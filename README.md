# ophac -- Order Preserving Hierarachical Agglomerative Clustering
The code in this project realises the theory described in [this article](https://link.springer.com/article/10.1007/s10994-021-06125-0).</br>
The functionality provided is that of _**order preserving hierarchical agglomerative clustering of partially ordered sets**_.

The [ophac wiki](https://bitbucket.org/Bakkelund/ophac/wiki/Home) provides examples of how to use the library (link to the old repo at bitbucket).

## Licensing

The software in this package is released under the [GNU Lesser General Public License](https://www.gnu.org/licenses/lgpl-3.0.en.html).

## Platform requirements
`ophac` runs on **python 3.0** or greater, and makes use of the following python libraries:

* numpy
* scipy

## Installation

### From PyPI
```bash
pip install ophac
```

### Local installation
Best done in a local virtual environment:
```bash
> python -m venv venv
> source venv/bin/activate
> pip install -e .
```

## Source

The full source is available from <https://github.com/danielbakkelund/ophac>.