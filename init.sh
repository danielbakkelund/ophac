#!/bin/bash
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


XLIBS=xlibs

if test ! -d ${XLIBS}; then
    echo "Creating directory ${XLIBS}."
    mkdir ${XLIBS}

    echo 'Cloning unit test framework.'
    (cd ${XLIBS}; git clone --branch rev01 https://Bakkelund@bitbucket.org/Bakkelund/upyt.git)
fi

if test ! -d tmp; then
    echo "Creating tmp directory."
    mkdir tmp
fi

echo Building C++ extensions
(cd cpp; make)

echo 'Remember to source "setPyPath.sh" to set the python path.'

exit 0

