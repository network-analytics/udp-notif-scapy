#!/bin/bash

## USAGE: sudo ./performance.sh <instances> <messages> <big|small> <dest_IP> <dest_port>

# Run as root
if [ "$EUID" -ne 0 ];
then
  echo "Please run as root."
  exit
fi

# Arguments
DEST_IP="192.168.0.17"
DEST_PORT="8081"
MESSAGES=100
INSTANCES=20
JSON=big   # big or small json file

NB_ARGS=$#
if [ $NB_ARGS = 6 ] || [ $NB_ARGS = 7 ];
then
  INSTANCES=$1
  MESSAGES=$2
  JSON=$3
  VLEN=$4
  DEST_IP=$5
  DEST_PORT=$6
else
  echo -e "\e[1m\e[33mUsing default parameters. Use all 5 or 6 parameters if needed.\e[39m\e[0m"
fi

if [ $NB_ARGS = 7 ] && [ "$7" = "-y" ];
then
  PASS_CONFIRM=true
else 
  PASS_CONFIRM=false
fi

# if json --> 1 message = 5 segments
PACKETS_PER_MESSAGE=5

CURRENT_FOLDER=$(dirname "$0")
SOURCE_FOLDER=$CURRENT_FOLDER/../src

TOTAL_MSG_TO_SEND=0

if [ $JSON = "big" ]
then
  TOTAL_MSG_TO_SEND=$((MESSAGES * PACKETS_PER_MESSAGE * INSTANCES))
else
  TOTAL_MSG_TO_SEND=$((MESSAGES * INSTANCES))
fi

echo -e "Sending messages to \e[1m\\e[36m$DEST_IP:$DEST_PORT\e[0m";
echo -e "Using \e[1m\\e[36m$JSON\e[0m json file";
echo -e "Launching \e[1m\\e[36m$INSTANCES\e[0m instances of scapy";
echo -e "Summary for every scapy: \e[1m\e[36m$MESSAGES\e[0m messages, \e[1m\e[36m$(($MESSAGES * $PACKETS_PER_MESSAGE))\e[0m packets will be sent for every scapy. "
echo -e "Total messages to send: \e[1m\e[36m$(($MESSAGES * $INSTANCES))\e[0m messages will be sent"
echo -e "Total packets to send: \e[1m\e[36m$(($TOTAL_MSG_TO_SEND))\e[0m packets will be sent"
if [ $PASS_CONFIRM = false ]
then
  read -p "Are you sure? [y/n]: " -r;
else
  REPLY=y
fi

if [[ $REPLY =~ ^[Yy]$ ]] 
then

  for i in `seq 0 $(($INSTANCES - 1))` ;
  do 
    IP_LAST=$(($i % 255))
    ADDITIONAL_ID=$(($MESSAGES * $i))
    sudo python3 $SOURCE_FOLDER/main.py -n $MESSAGES -s big -i $ADDITIONAL_ID -a $MESSAGES 192.168.42.$IP_LAST $DEST_IP 8080 $DEST_PORT &
  done
  echo -e "\e[1m\\e[36m$INSTANCES\e[0m have been launched";
  wait
  
  # Sending last messages to stop client_performance client
  echo "Sending $VLEN messages with observation_domain_id 49993648"
  for i in `seq 0 $(($VLEN - 1))` ;
  do 
    sudo python3 $SOURCE_FOLDER/main.py -n 1 -s small -i 49993648 192.168.42.$IP_LAST $DEST_IP 8080 $DEST_PORT
  done
else 
  echo -e "Operation cancelled: \e[1m\e[31mNo scapys have been launched"
fi

