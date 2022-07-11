#!/bin/bash

perl -pi -e 's/\[//g' tmp_ORDER.txt
perl -pi -e 's/\]//g' tmp_ORDER.txt
perl -pi -e 's/,//g' tmp_ORDER.txt

sed -e '/MAGMOM/ {' -e 'r tmp_MAGMOM.txt' -e 'd' -e '}' -i INCAR_tst
sed -e "s/CHANGE/$(<tmp_ORDER.txt sed -e 's/[\&/]/\\&/g' -e 's/$/\\n/' | tr -d '\n')/g" -i INCAR_tst
