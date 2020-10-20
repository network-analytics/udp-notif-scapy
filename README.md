# scapy

Generation of UDP-Notif packages via scapy (python)

1) make sure you have scapy and python installed (with matching versions)

2) place simulation.py in the same directory as run_scapy

3) place message.json file in parent directory

4) open terminal in said parent directory, and execute run.sh script as root, with the appropriate arguments

SYNTAX :

sudo ./run.sh IPV4 source (w.x.y.z), IPV4 destination (w.x.y.z), INT source port (1000 < x < 10 000), INT destination port (1000 < y < 10 000, y != x), INT packet amount, (x > 0), INT MTU (x > 18 if segmentation, x > 12 if single-packet message), FLOAT sleep time, (x >= 0), STR message type (x = ints or x = json), INT integers amount if previous arg is ints (x >= 1, amount will be 10 * 2 ** x)

EXAMPLES :

sudo ./run.sh 192.0.2.4 192.0.2.2 9340 9341 1 1500 1 ints 10

Sends 1 notification message made of 10 * 2 ** 10 integers, from 192.0.2.4 on port 9340 to 192.0.2.2 on port 9341, with a 1-second sleeptime between messages. The message is made of 10240 integers, and the segmented header size is 18, which implies a payload size of 1482. Therefore, the expected outcome is 7 segments.

sudo ./run.sh 192.0.2.4 192.0.2.2 9340 9341 2 9000 1 json

Sends 3 notification messages made from a json file, from 192.0.2.4 on port 9340 to 192.0.2.2 on port 9341, with a 1-second sleeptime between messages. Depending on the json's size, we can expect several segments, or a single packet.