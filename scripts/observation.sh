#!/bin/bash

# Run as root
if [ "$EUID" -ne 0 ]
then
  echo "Please run as root."
  exit
fi

# if json --> 1 message = 5 segments
MESSAGES=1000

DEST_IP="192.168.0.17"
DEST_PORT="8081"

SOURCE_FOLDER=../src

echo "Sending $MESSAGES messages"

sudo python3 $SOURCE_FOLDER/main.py -n $MESSAGES -s big -i 0 -a $MESSAGES 192.168.42.1 $DEST_IP 8080 $DEST_PORT &
sudo python3 $SOURCE_FOLDER/main.py -n $MESSAGES -s big -i 1000 -a $MESSAGES 192.168.42.2 $DEST_IP 8080 $DEST_PORT &
sudo python3 $SOURCE_FOLDER/main.py -n $MESSAGES -s big -i 2000 -a $MESSAGES 192.168.42.3 $DEST_IP 8080 $DEST_PORT &
sudo python3 $SOURCE_FOLDER/main.py -n $MESSAGES -s big -i 3000 -a $MESSAGES 192.168.42.4 $DEST_IP 8080 $DEST_PORT &
sudo python3 $SOURCE_FOLDER/main.py -n $MESSAGES -s big -i 4000 -a $MESSAGES 192.168.42.5 $DEST_IP 8080 $DEST_PORT &
sudo python3 $SOURCE_FOLDER/main.py -n $MESSAGES -s big -i 5000 -a $MESSAGES 192.168.42.6 $DEST_IP 8080 $DEST_PORT &
sudo python3 $SOURCE_FOLDER/main.py -n $MESSAGES -s big -i 6000 -a $MESSAGES 192.168.42.7 $DEST_IP 8080 $DEST_PORT &
sudo python3 $SOURCE_FOLDER/main.py -n $MESSAGES -s big -i 7000 -a $MESSAGES 192.168.42.8 $DEST_IP 8080 $DEST_PORT &
sudo python3 $SOURCE_FOLDER/main.py -n $MESSAGES -s big -i 8000 -a $MESSAGES 192.168.42.9 $DEST_IP 8080 $DEST_PORT &
sudo python3 $SOURCE_FOLDER/main.py -n $MESSAGES -s big -i 9000 -a $MESSAGES 192.168.42.10 $DEST_IP 8080 $DEST_PORT &

##################### 10 ###################### 
sudo python3 $SOURCE_FOLDER/main.py -n $MESSAGES -s big -i 10000 -a $MESSAGES 192.168.42.11 $DEST_IP 8080 $DEST_PORT &
sudo python3 $SOURCE_FOLDER/main.py -n $MESSAGES -s big -i 11000 -a $MESSAGES 192.168.42.12 $DEST_IP 8080 $DEST_PORT &
sudo python3 $SOURCE_FOLDER/main.py -n $MESSAGES -s big -i 12000 -a $MESSAGES 192.168.42.13 $DEST_IP 8080 $DEST_PORT &
sudo python3 $SOURCE_FOLDER/main.py -n $MESSAGES -s big -i 13000 -a $MESSAGES 192.168.42.14 $DEST_IP 8080 $DEST_PORT &
sudo python3 $SOURCE_FOLDER/main.py -n $MESSAGES -s big -i 14000 -a $MESSAGES 192.168.42.15 $DEST_IP 8080 $DEST_PORT &
sudo python3 $SOURCE_FOLDER/main.py -n $MESSAGES -s big -i 15000 -a $MESSAGES 192.168.42.16 $DEST_IP 8080 $DEST_PORT &
sudo python3 $SOURCE_FOLDER/main.py -n $MESSAGES -s big -i 16000 -a $MESSAGES 192.168.42.17 $DEST_IP 8080 $DEST_PORT &
sudo python3 $SOURCE_FOLDER/main.py -n $MESSAGES -s big -i 17000 -a $MESSAGES 192.168.42.18 $DEST_IP 8080 $DEST_PORT &
sudo python3 $SOURCE_FOLDER/main.py -n $MESSAGES -s big -i 18000 -a $MESSAGES 192.168.42.19 $DEST_IP 8080 $DEST_PORT &
sudo python3 $SOURCE_FOLDER/main.py -n $MESSAGES -s big -i 19000 -a $MESSAGES 192.168.42.20 $DEST_IP 8080 $DEST_PORT &

##################### 20 ###################### 
sudo python3 $SOURCE_FOLDER/main.py -n $MESSAGES -s big -i 10000 -a $MESSAGES 192.168.42.11 $DEST_IP 8080 $DEST_PORT &
sudo python3 $SOURCE_FOLDER/main.py -n $MESSAGES -s big -i 11000 -a $MESSAGES 192.168.42.12 $DEST_IP 8080 $DEST_PORT &
sudo python3 $SOURCE_FOLDER/main.py -n $MESSAGES -s big -i 12000 -a $MESSAGES 192.168.42.13 $DEST_IP 8080 $DEST_PORT &
sudo python3 $SOURCE_FOLDER/main.py -n $MESSAGES -s big -i 13000 -a $MESSAGES 192.168.42.14 $DEST_IP 8080 $DEST_PORT &
sudo python3 $SOURCE_FOLDER/main.py -n $MESSAGES -s big -i 14000 -a $MESSAGES 192.168.42.15 $DEST_IP 8080 $DEST_PORT &
sudo python3 $SOURCE_FOLDER/main.py -n $MESSAGES -s big -i 15000 -a $MESSAGES 192.168.42.16 $DEST_IP 8080 $DEST_PORT &
sudo python3 $SOURCE_FOLDER/main.py -n $MESSAGES -s big -i 16000 -a $MESSAGES 192.168.42.17 $DEST_IP 8080 $DEST_PORT &
sudo python3 $SOURCE_FOLDER/main.py -n $MESSAGES -s big -i 17000 -a $MESSAGES 192.168.42.18 $DEST_IP 8080 $DEST_PORT &
sudo python3 $SOURCE_FOLDER/main.py -n $MESSAGES -s big -i 18000 -a $MESSAGES 192.168.42.19 $DEST_IP 8080 $DEST_PORT &
sudo python3 $SOURCE_FOLDER/main.py -n $MESSAGES -s big -i 19000 -a $MESSAGES 192.168.42.20 $DEST_IP 8080 $DEST_PORT &

#################### 30 ###################### 