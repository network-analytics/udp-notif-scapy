#!/bin/bash

cd scapy
rm filtered.pcap
python3 simulation.py $1 $2 $3 $4 $5 $6 $7 $8 $9
cd ..