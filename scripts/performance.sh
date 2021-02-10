#!/bin/bash

# Run as root
if [ "$EUID" -ne 0 ]
then
  echo "Please run as root."
  exit
fi

# Arguments
MESSAGES=100
DEST_IP="192.168.0.17"
DEST_PORT="8081"
INSTANCES=200

# if json --> 1 message = 5 segments
PACKETS_PER_MESSAGE=5
SOURCE_FOLDER=../src

echo -e "Sending messages to \e[1m\\e[36m$DEST_IP:$DEST_PORT\e[0m";
echo -e "Launching \e[1m\\e[36m$INSTANCES\e[0m instances of scapy";
echo -e "Summary: \e[1m\e[36m$MESSAGES\e[0m messages, \e[1m\e[36m$(($MESSAGES * $PACKETS_PER_MESSAGE))\e[0m packets will be sent for every scapy. "
echo -e "Total packets to send: \e[1m\e[36m$(($MESSAGES * $PACKETS_PER_MESSAGE * $INSTANCES))\e[0m packets will be sent"
read -p "Are you sure? [y/n]: " -r;

if [[ $REPLY =~ ^[Yy]$ ]] 
then

  for i in `seq 0 $(($INSTANCES - 1))` ;
  do 
    IP_LAST=$(($i % 255))
    ADDITIONAL_ID=$(($MESSAGES * $i))
    sudo python3 $SOURCE_FOLDER/main.py -n $MESSAGES -s big -i $ADDITIONAL_ID -a $MESSAGES 192.168.42.$IP_LAST $DEST_IP 8080 $DEST_PORT &
  done
  echo -e "\e[1m\\e[36m$INSTANCES\e[0m have been launched";
else 
  echo -e "Operation cancelled: \e[1m\e[31mNo scapys have been launched"
fi

