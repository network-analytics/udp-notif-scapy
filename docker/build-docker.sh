#!/bin/bash

if [ ! -d "tmp" ] 
then
    mkdir tmp
    echo "Creating tmp directory for docker context"
fi

cp -r ../src tmp/src

echo "Deleting src cache"
rm -rf tmp/src/*/__pycache__ tmp/src/*/*/__pycache__

docker build . -t unyte/scapy

echo "Removing tmp"
rm -r tmp
