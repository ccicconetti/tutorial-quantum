#!/bin/bash

FORMAT=png

if [ ! -e qcircuit.sty ] ; then
  wget https://raw.githubusercontent.com/CQuIC/qcircuit/master/qcircuit.sty
fi

for i in *.py ; do
  outfile=${i/.py/.$FORMAT}
  if [ "$outfile" -ot "$i" ] ; then
    FORMAT=$FORMAT python $i
  fi
done
