#!/bin/bash

ps aux | grep "python3 main.py" | grep -v "grep" | awk '{print $2}' > pids

for i in `cat pids` ; do echo "Killing $i" ; kill -9 $i ; done

rm pids
