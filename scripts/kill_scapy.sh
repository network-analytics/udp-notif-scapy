#!/bin/bash

SCAPY_PROCESSES=$(ps aux | grep "python3 ../src/main.py" | grep -v "grep" | awk '{print $2}')

for i in $SCAPY_PROCESSES ;
do 
    echo "Killing $i process";
    kill -9 $i;
done