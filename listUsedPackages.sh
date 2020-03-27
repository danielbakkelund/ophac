
REPORT=`find src examples -name '*.py' -exec grep -H 'import' {}  \; | \
	     sed 's/^\([^:]*\): *import *\([^ ]*\).*/\2/g' | \
	     sed 's/^\([^:]*\): *from *\([^ ]*\).*/\2/' | \
	     sort -u `

echo 'usages:'
export IFS=' '
echo $REPORT | while read pair; do
    echo $pair
done
