#!/bin/bash

# get all script args in a single string
args="$*"

echo "$SCAPY_FOLDER_PATH"

# is the env var set ? 
if [ -z "$SCAPY_FOLDER_PATH" ]
then
  echo "Set the SCAPY_FOLDER_PATH env var before"
  exit
else

  # Copy the script to the right folder 
  cp ./generator.py $SCAPY_FOLDER_PATH/gen.py

  # Copy the message to the right folder
  cp ./message.json $SCAPY_FOLDER_PATH/../message.json

  cd $SCAPY_FOLDER_PATH
  rm filtered.pcap

  # Call the python script
  python3 gen.py $args

  # Remove the copied files
  rm gen.py
  cd ..
  rm message.json

fi