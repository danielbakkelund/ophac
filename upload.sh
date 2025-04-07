#!/bin/sh

rm -rf dist

cp ../README.md .

python3 setup.py sdist

if ! test "$?" -eq "0"; then
    echo "Generating dist failed."
    exit 42
fi

python3 -m twine upload dist/*

rm -f README.md

