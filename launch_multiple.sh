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
sudo python3 main.py -n $message 192.168.42.34 192.168.42.34 6666 8081 &
sudo python3 main.py -n $message 192.168.42.34 192.168.42.34 5321 8081 &
sudo python3 main.py -n $message 192.168.42.34 192.168.42.34 5322 8081 &
sudo python3 main.py -n $message 192.168.42.34 192.168.42.34 5323 8081 &
#sudo python3 main.py -n $message 192.168.42.34 192.168.42.34 5322 8081 &
#sudo python3 main.py -n $message 192.168.42.34 192.168.42.34 5323 8081 &
#sudo python3 main.py -n $message 192.168.42.34 192.168.42.34 5320 8081 &
#sudo python3 main.py -n $message 192.168.42.34 192.168.42.34 5321 8081 &