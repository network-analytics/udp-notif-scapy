#!/bin/bash

# Run as root
if [ "$EUID" -ne 0 ]
then
  echo "Please run as root."
  exit
fi

message=1

if [ -z $1 ] 
then
  echo "Number messages set to 1"
  message=1
else
  message=$1
fi

DEST_IP="192.168.42.34"
DEST_PORT="8081"

echo "Sending $message messages"
sudo python3 main.py -n $message 192.168.42.34 $DEST_IP 6666 $DEST_PORT &
sudo python3 main.py -n $message 192.168.42.34 $DEST_IP 5321 $DEST_PORT &
sudo python3 main.py -n $message 192.168.42.34 $DEST_IP 5322 $DEST_PORT &
sudo python3 main.py -n $message 192.168.42.34 $DEST_IP 5323 $DEST_PORT &
# sudo python3 main.py -n $message 192.168.42.34 $DEST_IP 5322 $DEST_PORT &
# sudo python3 main.py -n $message 192.168.42.34 $DEST_IP 5323 $DEST_PORT &
# sudo python3 main.py -n $message 192.168.42.34 $DEST_IP 5320 $DEST_PORT &
# sudo python3 main.py -n $message 192.168.42.34 $DEST_IP 5321 $DEST_PORT &
