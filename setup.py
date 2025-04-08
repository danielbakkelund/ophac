# # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # #
# Copyright 2025 Daniel Bakkelund
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

import setuptools
import os
import re
from glob import glob
from setuptools import setup, find_packages
from pybind11.setup_helpers import Pybind11Extension, build_ext

def get_version():
    version_file = os.path.join("src", "ophac", "_version.py")
    with open(version_file) as f:
        content = f.read()
    match = re.search(r'__version__\s*=\s*["\']([^"\']+)["\']', content)
    if not match:
        raise RuntimeError("Unable to find version string in _version.py")
    return match.group(1)

version = get_version()

ext_modules = [
    Pybind11Extension(
        "ophac_cpp",  # Name of the extension module
        sources=sorted(glob("src/cpp/**/*.cpp", recursive=True)),
        include_dirs=["src/cpp"],
        cxx_std=17,
    )
]

with open("README.md", "r") as fh:
    long_description = fh.read()

setuptools.setup(
    name='ophac',
    version=version,  # Use the version variable defined above
    author='Daniel Bakkelund',
    author_email='daniel_bakkelund@hotmail.com',
    description='Order Preserving Hierarchical Agglomerative Clustering',
    long_description=long_description,
    long_description_content_type='text/markdown',
    url='https://bitbucket.org/Bakkelund/ophac/src/v04/',
    packages=setuptools.find_packages(where="src"),
    package_dir={"": "src"},
    ext_modules=ext_modules,
    cmdclass={"build_ext": build_ext},  # Add this line
    classifiers=[
        'Programming Language :: Python :: 3',
        'License :: OSI Approved :: GNU Lesser General Public License v3 or later (LGPLv3+)',
        'Development Status :: 3 - Alpha',
        'Operating System :: OS Independent',
    ],
    python_requires='>=3.0',
    install_requires=[
        'numpy',
        'scipy'
    ],
    zip_safe=False
)
