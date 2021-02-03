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

SOURCE_FOLDER=../src

# Call the python script with sudo and the path to access scapy
sudo  /usr/bin/python3 $SOURCE_FOLDER/main.py 192.0.2.4 192.0.2.2 9340 9341 $args
