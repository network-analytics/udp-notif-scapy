#!/bin/bash

ENGINE=docker

if [ -z "$1" ] || [ "$1" == "docker" ] || [[ "$1" != "docker" && "$1" != "podman" ]]; then
    echo -e "Using default \e[1m\e[32mdocker \e[0mengine"
elif [ "$1" == "podman" ]; then
    echo -e "Using \e[1m\e[32mpodman \e[0mengine"
    ENGINE=podman
fi

MESSAGES=1000

DEST_IP="192.168.0.17"
DEST_PORT="8081"

echo "Sending $MESSAGES messages"
$ENGINE run -d unyte/scapy:latest python3 src/main.py -n $MESSAGES -t json -d headers -l 0.5 -i 0 -a $MESSAGES 192.168.42.1 $DEST_IP 8080 $DEST_PORT
$ENGINE run -d unyte/scapy:latest python3 src/main.py -n $MESSAGES -t json -l 0.5 -i 1000 -a $MESSAGES 192.168.42.2 $DEST_IP 8080 $DEST_PORT &
$ENGINE run -d unyte/scapy:latest python3 src/main.py -n $MESSAGES -t json -l 0.5 -i 2000 -a $MESSAGES 192.168.42.3 $DEST_IP 8080 $DEST_PORT &
$ENGINE run -d unyte/scapy:latest python3 src/main.py -n $MESSAGES -t json -l 0.5 -i 3000 -a $MESSAGES 192.168.42.4 $DEST_IP 8080 $DEST_PORT &
$ENGINE run -d unyte/scapy:latest python3 src/main.py -n $MESSAGES -t json -i 4000 -a $MESSAGES 192.168.42.5 $DEST_IP 8080 $DEST_PORT &
$ENGINE run -d unyte/scapy:latest python3 src/main.py -n $MESSAGES -t json -i 5000 -a $MESSAGES 192.168.42.6 $DEST_IP 8080 $DEST_PORT &
$ENGINE run -d unyte/scapy:latest python3 src/main.py -n $MESSAGES -t json -i 6000 -a $MESSAGES 192.168.42.7 $DEST_IP 8080 $DEST_PORT &
$ENGINE run -d unyte/scapy:latest python3 src/main.py -n $MESSAGES -t json -i 7000 -a $MESSAGES 192.168.42.8 $DEST_IP 8080 $DEST_PORT &
# $ENGINE run -d unyte/scapy:latest python3 src/main.py -n $MESSAGES -t json -i 8000 -a $MESSAGES 192.168.42.9 $DEST_IP 8080 $DEST_PORT &
# $ENGINE run -d unyte/scapy:latest python3 src/main.py -n $MESSAGES -t json -i 9000 -a $MESSAGES 192.168.42.10 $DEST_IP 8080 $DEST_PORT &
# $ENGINE run -d unyte/scapy:latest python3 src/main.py -n $MESSAGES -t json -i 10000 -a $MESSAGES 192.168.42.11 $DEST_IP 8080 $DEST_PORT &
# $ENGINE run -d unyte/scapy:latest python3 src/main.py -n $MESSAGES -t json -i 11000 -a $MESSAGES 192.168.42.11 $DEST_IP 8080 $DEST_PORT &
# $ENGINE run -d unyte/scapy:latest python3 src/main.py -n $MESSAGES -t json -i 12000 -a $MESSAGES 192.168.42.11 $DEST_IP 8080 $DEST_PORT &
# $ENGINE run -d unyte/scapy:latest python3 src/main.py -n $MESSAGES -t json -i 13000 -a $MESSAGES 192.168.42.11 $DEST_IP 8080 $DEST_PORT &
# $ENGINE run -d unyte/scapy:latest python3 src/main.py -n $MESSAGES -t json -i 14000 -a $MESSAGES 192.168.42.11 $DEST_IP 8080 $DEST_PORT &
# $ENGINE run -d unyte/scapy:latest python3 src/main.py -n $MESSAGES -t json -i 15000 -a $MESSAGES 192.168.42.11 $DEST_IP 8080 $DEST_PORT &
# $ENGINE run -d unyte/scapy:latest python3 src/main.py -n $MESSAGES -t json -i 16000 -a $MESSAGES 192.168.42.11 $DEST_IP 8080 $DEST_PORT &
# $ENGINE run -d unyte/scapy:latest python3 src/main.py -n $MESSAGES -t json -i 17000 -a $MESSAGES 192.168.42.11 $DEST_IP 8080 $DEST_PORT &
