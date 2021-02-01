ps aux | grep "python3 generator.py" | grep -v "grep" | awk '{print $2}' > pids

for i in `cat pids` ; do echo $i ; kill -9 $i ; done