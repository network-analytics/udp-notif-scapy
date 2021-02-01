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

echo "Sending $message messages"
sudo python3 generator.py -n $message 192.168.0.1 192.168.0.17 3450 8081 &
sudo python3 generator.py -n $message 168.170.0.2 192.168.0.17 4000 8081 &
sudo python3 generator.py -n $message 10.180.0.3 192.168.0.17 5320 8081 &
sudo python3 generator.py -n $message 10.180.0.3 192.168.0.17 5321 8081 &
sudo python3 generator.py -n $message 10.180.0.3 192.168.0.17 5322 8081 &
sudo python3 generator.py -n $message 10.180.0.3 192.168.0.17 5323 8081 &
sudo python3 generator.py -n $message 120.2.1.4 192.168.0.17 6520 8081 &
sudo python3 generator.py -n $message 120.2.1.4 192.168.0.17 6521 8081 &
sudo python3 generator.py -n $message 120.2.1.4 192.168.0.17 6522 8081 &
sudo python3 generator.py -n $message 120.2.1.4 192.168.0.17 6523 8081 &
sudo python3 generator.py -n $message 120.2.1.4 192.168.0.17 6524 8081 &
