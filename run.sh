#!/bin/bash

cd scapy
rm filtered.pcap
python3 generator.py $1 $2 $3 $4 $5 $6 $7 $8 $9
cd ..