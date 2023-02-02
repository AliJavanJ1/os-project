#!/bin/sh

echo "readMB, writeMB" > iostat_disk.csv
iostat -x 1 -m | awk '/sda/ { print $3 "," $9; fflush();} ' >> iostat_disk.csv
