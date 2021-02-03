#!/bin/bash

mkdir src

cp -r ../src src
rm -rf src/**/__pycache__

# docker build . -t unyte/scapy
