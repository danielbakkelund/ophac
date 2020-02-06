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

OSNAME=`uname -s`

if [[ $OSNAME == CYGWIN* ]]; then
    echo "Cygwin detected."
    CYGW=0
else
    echo "Assuming $OSNAME has Unix-style path layout."
    CYGW=1
fi

# Relative path to unit test framework.
UPYT_HOME=${PWD}'/xlibs/upyt'

# upyt dir
UPYT_ABS_SRC="unset"
cd $UPYT_HOME
if test "$CYGW" -eq "0"; then
    UPYT_ABS_SRC=`cygpath -a -w $PWD/src`
    UPYT_ABS_SRC=${UPYT_ABS_SRC//\\/\\\\}
else
    UPYT_ABS_SRC=${PWD}/src
fi
cd - > /dev/null


# Current dir
if test "$CYGW" -eq "0"; then
    P=`cygpath -a -w $PWD/src`
    PP=${P//\\/\\\\}
    T=`cygpath -a -w $PWD/test`
    TP=${T//\\/\\\\}
    T=`cygpath -a -w $PWD/systest`
    TP=${T//\\/\\\\}
    export PYTHONPATH=${PP}';'${TP}';'${UPYT_ABS_SRC}
else
    export PYTHONPATH=${PWD}/src':'${PWD}/test':'${UPYT_ABS_SRC}':'${PWD}/systest
fi

echo "PYTHONPATH=$PYTHONPATH"
