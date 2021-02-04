#!/bin/bash

ENGINE=docker

if [ -z "$1" ] || [ "$1" == "docker" ] || [[ "$1" != "docker" && "$1" != "podman" ]]; then
    echo -e "Using default \e[1m\e[32mdocker \e[0mengine"
elif [ "$1" == "podman" ]; then
    echo -e "Using \e[1m\e[32mpodman \e[0mengine"
    ENGINE=podman
fi

CONTAINER_LIST=$($ENGINE ps | grep "unyte/scapy" | awk '{print $1}')

echo "Stopping all unyte/scapy containers $CONTAINER_LIST"
$ENGINE stop $CONTAINER_LIST
