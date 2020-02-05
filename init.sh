#!/bin/bash

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

echo 'Remember to source "setPyPath.sh" to set the python path.'

exit 0

