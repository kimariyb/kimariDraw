#!/bin/bash
for file in *.out; do
    Multiwfn "$file" < commands.txt > /dev/null
    rm -f "${file%.*}.txt"
    mv spectrum_curve.txt "${file%.*}.txt"
done
rm -f spectrum_line.txt