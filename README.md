# scapy

Generation of UDP-Notif packages via scapy (python)

1) make sure you have scapy and python installed (with matching versions)

2) place simulation.py in the same directory as run_scapy

3) place message.json file in parent directory

4) open terminal in said parent directory, and execute run.sh script as root, with the appropriate arguments

SYNTAX : sudo ./run.sh IPV4 @source IPV4 @destination INT sourcePort INT destinationPort INT packetAmount

EXAMPLE : sudo ./run.sh 192.0.2.4 192.0.2.2 9340 9341 10
