#!/bin/bash

CONTAINER_LIST=$(docker ps | grep "unyte/scapy" | awk '{print $1}')

echo "Stopping all unyte/scapy containers $CONTAINER_LIST"
docker stop $CONTAINER_LIST
