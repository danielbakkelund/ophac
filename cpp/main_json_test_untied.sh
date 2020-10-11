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

INPUT_FILE='._json_input.json'
OUTPUT_FILE='._json_output.json'
EXPECT_FILE='._json_expect.json'

PROGRAM='./release/lib/ophac_untied'

echo Testing JSON file interface with fig 3.5 + CL

TEST_OK=1

echo Generating input file ${INPUT_FILE}
echo '{' > ${INPUT_FILE}
echo '  "D":[5.8, 4.2, 6.9, 2.6,6.7, 1.7, 7.2,1.9, 5.6,7.6],' >> ${INPUT_FILE}
echo '  "Q":[[],[],[],[],[]],' >> ${INPUT_FILE}
echo '  "L":"complete",' >> ${INPUT_FILE}
echo '  "mode":"untied"' >> ${INPUT_FILE}
echo '}' >> ${INPUT_FILE}

echo Generating expected file ${EXPECTED_FILE}
echo '{' > ${EXPECT_FILE}
echo ' "dists":[1.7, 2.6, 5.6, 7.6],' >> ${EXPECT_FILE}
echo ' "joins":[[1,3],[0,3],[0,2],[0,1]]' >> ${EXPECT_FILE}
echo '}' >> ${EXPECT_FILE}

echo Running ${PROGRAM}
${PROGRAM} ${INPUT_FILE} ${OUTPUT_FILE}

if ! test "$?" -eq "0"; then
    echo ERROR::: C++ program crashed.
    exit 666
fi

echo Comparing ${OUTPUT_FILE} to ${EXPECTED_FILE}
python3 test/json_cmp.py ${EXPECT_FILE} ${OUTPUT_FILE}
TEST_OK=${?}

if ! test "$TEST_OK" -eq "0"; then
    echo ERROR::: ${EXPECT_FILE} and ${OUTPUT_FILE} differ.
    exit ${TEST_OK}
fi

rm -f ${INPUT_FILE} ${OUTPUT_FILE} ${EXPECT_FILE}

echo SUCCESS!!!
exit 0
