#!/bin/bash

ENGINE=docker

if [ -z "$1" ] || [ "$1" == "docker" ] || [[ "$1" != "docker" && "$1" != "podman" ]]; then
    echo -e "Using default \e[1m\e[32mdocker \e[0mengine"
elif [ "$1" == "podman" ]; then
    echo -e "Using \e[1m\e[32mpodman \e[0mengine"
    ENGINE=podman
fi

if [ ! -d "tmp" ] 
then
    mkdir tmp
    echo "Creating tmp directory for docker context"
fi

cp -r ../src tmp/src

echo "Deleting src cache"
rm -rf tmp/src/*/__pycache__ tmp/src/*/*/__pycache__

$ENGINE build . -t unyte/scapy

echo "Removing tmp"
rm -r tmp
