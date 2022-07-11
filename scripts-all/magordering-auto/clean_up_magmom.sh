#!/bin/bash

# for getting rid of the brackets and commas within the tmp_ORDER.txt file
perl -pi -e 's/\[//g' tmp_ORDER.txt
perl -pi -e 's/\]//g' tmp_ORDER.txt
perl -pi -e 's/,//g' tmp_ORDER.txt

sed -e '/MAGMOM/ {' -e 'r MAGMOM_change.txt' -e 'd' -e '}' -i INCAR # this replaces the entire line which contains MAGMOM within the INCAR file with "MAGMOM = CHANGE"
sed -e "s/CHANGE/$(<tmp_ORDER.txt sed -e 's/[\&/]/\\&/g' -e 's/$/\\n/' | tr -d '\n')/g" -i INCAR # this replaces the "CHANGE" that we just added with the magnetic ordering for the corresponding POSCAR file