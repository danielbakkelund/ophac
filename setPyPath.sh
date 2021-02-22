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

if test -e ${PWD}'/xlibs/upyt' ; then

    # Relative path to unit test framework.
    UPYT_HOME=${PWD}'/xlibs/upyt'

    # upyt dir
    UPYT_ABS_SRC="unset"
    cd $UPYT_HOME
    UPYT_ABS_SRC=${PWD}/src
    cd - > /dev/null


    # Current dir
    export PYTHONPATH=${PWD}/src':'${PWD}/test':'${UPYT_ABS_SRC}':'${PWD}/systest
    
    export PYTHONPATH=${PYTHONPATH}:${PWD}/cpp/release/lib

    echo "PYTHONPATH=$PYTHONPATH"

else # not exists xlibs
    echo '##################### ERROR #########################'
    echo 'You must run ./init.sh prior to sourcing this script.'
fi
