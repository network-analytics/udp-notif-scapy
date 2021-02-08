# Scapy

This program implement the generation and forwarding of UDP-Notif packets according to the draft-ietf-netconf-udp-notif-01. It lets you build a traffic simulation with many parameters, which you can provide as arguments to main.py.

## Installing dependencies (tested on python3)
- `pip install -r src/requirements.txt`

## Usage
Necessary arguments :

w.x.y.z (IPV4) source ip address, 0 <= w,x,y,z <= 255

w.x.y.z (IPV4) destination ip address, 0 <= w,x,y,z <= 255

x (INT) source port, 1000 < x < 10000

x (INT) destination port, 1000 < x < 10000


Optional arguments :

`--initial-domain x` or `-i x` : (INT) initial observation domain id, x >= 0, default 0

`--additional-domains x` or `-a x` : (INT) amount of additional observation domains, x >= 0, default 0

`--message-size s` or `-s s` : (STR) size of payload data, s = small or s = big, default small

`--message-amount x` or `-n x` : (INT) amount of messages to send, x >= 1, default 1

`--mtu x` or `-m x` : (INT) maximum transmission unit, 16 < x < 65535, default 1500

`--waiting-time f` or `-w f` : (FLOAT) waiting time (in seconds) between two messages, x > 0, default 0

`--probability-of-loss f` or `-p f` : (FLOAT) segment loss probability, 0 <= x < 1, default 0

`--random-order x` or `-r x` : (INT) forward segments in random order, x = 0 or x = 1, default 0

`--logging-level s` or `-l s` : (STR) logging level, s = none or s = warning or s = info or s = debug, default warning

`--capture x` or `-c x` : (INT) Set to 1 if you need a wireshark capture of the forwarded packets, x = 1 or x = 0, default 0

Examples :

`sudo python3 src/main.py 192.0.2.66 192.0.2.66 3456 3457`

1 segment of size 12 + 716 with a small json payload, from observation domain 0, with no loss probability, displaying control messages only

`sudo python3 src/main.py 192.0.2.66 192.0.2.66 3456 3457 -n 2 -r 1 -s big -i 10 -a 1 -p 0.1 -w 0.1 -l info`

2 messages of 5 shuffled segments of size 1500 with a json payload, from observation domains 10 and 11, with 0.1 loss probability and 0.1 second wait time between messages, displaying control messages and segment headers

## Docker container
See [Docker docs](docker)

## Launch multiple simulations
- `./launch_multiple.sh <number_messages>` : launches multiple instances of the generator simuling multiple source ips and ports
