#!/bin/sh

echo "cpu_idle" > iostat_cpu.csv
iostat -cx 1 | awk '$1 ~ /^[1234567890]?[1234567890]\.[1234567890][1234567890]$/ { print $6; fflush();}' >> iostat_cpu.csv
