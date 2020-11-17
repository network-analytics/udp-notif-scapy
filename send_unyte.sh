#!/bin/bash

# Run as root
if [ "$EUID" -ne 0 ]
then
  echo "Please run as root."
  exit
fi

# Get all script args in a single string
args="$*"

# If pcap exist, removes it
if [ -f "filtered.pcap" ]
then
  rm filtered.pcap
else
  echo "No filtered.pcap file to remove."
fi

# Call the python script with sudo and the path to access scapy
sudo env PATH=$PATH python3 generator.py $args
