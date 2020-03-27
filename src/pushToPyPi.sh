#!/bin/sh
# # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # 
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
# # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # 

URL='--repository-url https://test.pypi.org/legacy/'

DELETE='build dist ophac.egg-info'

if test ! -e 'ophac'; then
    echo 'The script must be executed in the src folder.'
    exit 666
fi

if test "$1" == "PROD"; then
    echo 'Push to production PyPi?'
    read YN
    if test "$YN" == "y"; then
	URL=''
    fi
else
    echo 'Do you have your token ready?'
    read YN
    if test "$YN" != "y"; then
	exit 1
    fi
fi

CONTINUE=0

python3 setup.py sdist bdist_wheel
if test "$?" -ne "0"; then
    echo 'Error encountered.'
    CONNTINUE=1
fi

if test "$CONTINUE"; then
    (exec python3 -m twine upload $URL dist/*)
    if test "#?" -ne "0"; then
	echo 'Error encountered.'
	CONTINUE=1
    fi
fi

echo 'Delete generated files?'
read YN
if test "$YN" == "y"; then
    echo 'Deleting:'
    for fname in $DELETE; do
	rm -rfv $fname
    done
fi

exit $CONTINUE
