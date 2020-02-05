#!/bin/bash

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
