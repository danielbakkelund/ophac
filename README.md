
# ophac – Order Preserving Hierarchical Agglomerative Clustering

This library implements the algorithms described in the article
[Order-Preserving Hierarchical Clustering](https://link.springer.com/article/10.1007/s10994-021-06125-0).
It provides functionality for performing **order-preserving hierarchical agglomerative clustering** on partially ordered sets.

See the [ophac wiki](https://bitbucket.org/Bakkelund/ophac/wiki/Home) for usage examples and additional context (linked from the old Bitbucket repository).

## License

This project is released under the [GNU Lesser General Public License v3.0](https://www.gnu.org/licenses/lgpl-3.0.en.html).

## Requirements

`ophac` requires **Python 3.6+** and the following libraries:

- `numpy`
- `scipy`

## Installation

### From PyPI (recommended)

Precompiled wheels are available for common platforms. Just run:

```bash
pip install ophac
```

###  Local Installation (for development)

Use a virtual environment to avoid polluting your system Python:

```bash
python -m venv venv
source venv/bin/activate
pip install -e .
```

##  Building from Source (for unsupported platforms)

If you're on a platform without a prebuilt wheel (e.g., unusual Linux distro or Python version), `pip` will try to build `ophac` from source.

To build successfully, you must have:

- A **C++17-compatible compiler** (e.g., GCC ≥ 7, Clang ≥ 5, or MSVC ≥ 2017)
- Python development headers (e.g., `python3-dev` or equivalent)
- Build tools like `make`, `cmake` (if needed)

Make sure `pip`, `setuptools`, and `wheel` are up to date:

```bash
pip install --upgrade pip setuptools wheel
```

Then install:

```bash
pip install ophac
```

If building fails, you can clone the repository and install locally with:

```bash
git clone https://github.com/danielbakkelund/ophac.git
cd ophac
pip install .
```
