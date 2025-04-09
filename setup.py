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

from setuptools import setup
from pybind11.setup_helpers import Pybind11Extension, build_ext
import os
import re
from glob import glob

def get_version():
    version_file = os.path.join("src", "ophac", "_version.py")
    with open(version_file) as f:
        content = f.read()
    match = re.search(r'__version__\s*=\s*["\']([^"\']+)["\']', content)
    if not match:
        raise RuntimeError("Unable to find version string in _version.py")
    return match.group(1)

ext_modules = [
    Pybind11Extension(
        "ophac_cpp",
        sources=sorted(glob("src/cpp/**/*.cpp", recursive=True)),
        include_dirs=["src/cpp"],
        cxx_std=17,
    )
]

setup(
    version=get_version(),
    ext_modules=ext_modules,
    cmdclass={"build_ext": build_ext},
)
