#!/bin/bash

ps aux | grep "python3 ../src/main.py" | grep -v "grep" | awk '{print $2}' > pids.txt

for i in `cat pids` ; do echo "Killing $i" ; kill -9 $i ; done

rm pids.txt
