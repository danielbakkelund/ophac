
# ophac – Order Preserving Hierarchical Agglomerative Clustering

**Version:** 0.5.2
**Python:** 3.10+

This library implements the algorithms described in the article
[Order-Preserving Hierarchical Clustering](https://link.springer.com/article/10.1007/s10994-021-06125-0).
It provides functionality for performing **order-preserving hierarchical agglomerative clustering** on partially ordered sets.

See the [ophac wiki](https://bitbucket.org/Bakkelund/ophac/wiki/Home) for usage examples and additional context (linked from the old Bitbucket repository).

## License

This project is released under the [GNU Lesser General Public License v3.0](https://www.gnu.org/licenses/lgpl-3.0.en.html).

## Requirements

`ophac` requires:

- Python 3.10 or newer
- `numpy` (runtime)
- `scipy` is **optional**, and only required for plotting-related utilities

##  From PyPI (recommended)

Install the core package:

```bash
pip install ophac
```

If you want to use the optional **plotting features**, install with extras:

```bash
pip install ophac[plot]
```

### Local Installation (for development)

Use a virtual environment to avoid polluting your system Python:

```bash
python -m venv venv
source venv/bin/activate
pip install -e ".[plot]"  # omit [plot] if plotting is not needed
```

##  Building from Source (for unsupported platforms)

If you're on a platform without a prebuilt wheel (e.g., unusual Linux distro or Python version), `pip` will try to build `ophac` from source.

You'll need:

- A **C++17-compatible compiler** (e.g., GCC ≥ 7, Clang ≥ 5, or MSVC ≥ 2017)
- Python development headers (e.g., `python3-dev`)
- Build tools like `make`, `cmake` (if required)

Ensure `pip`, `setuptools`, and `wheel` are up to date:

```bash
pip install --upgrade pip setuptools wheel
```

Then install:

```bash
pip install ophac
```

If building fails, you can clone the repository and install locally:

```bash
git clone https://github.com/danielbakkelund/ophac.git
cd ophac
pip install .
```

## Optional Plotting

Some functions provide visualization support (e.g., dendrograms). To enable these, install with the `plot` extra:

```bash
pip install ophac[plot]
```

This will install `scipy` as an additional dependency.
