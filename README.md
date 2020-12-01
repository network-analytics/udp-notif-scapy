# scapy

This program implement the generation and forwarding of UDP-Notif packets according to the draft-ietf-netconf-udp-notif-01. It lets you build a traffic simulation with many parameters, which you can provide as arguments to generator.py.

Necessary arguments :
w.x.y.z       (IPV4)      source ip address                           0 <= w,x,y,z <= 255
w.x.y.z       (IPV4)      destination ip address                      0 <= w,x,y,z <= 255
x             (INT)       source port                                 1000 < x < 10000
x             (INT)       destination port                            1000 < x < 10000

Optional arguments :
-i x          (INT)       initial observation domain id               x >= 0                                              default 0
-a x          (INT)       amount of additional observation domains    x >= 0                                              default 0
-t s          (STR)       type of payload data                        s = ints or s = json or s = rand                    default ints
-n x          (INT)       amount of messages to send                  x >= 1                                              default 1
-m x          (INT)       maximum transmission unit                   16 < x < 65535                                      default 1500
-s f          (FLOAT)     sleep time between two messages             x > 0                                               default 0
-l f          (FLOAT)     segment loss probability                    0 <= x < 1                                          default 0
-r x          (INT)       forward segments in random order            x = 0 or x = 1                                      default 0
-d s          (STR)       information display                         s = control or s = headers or s = everything        default control

Examples :

sudo python3 generator.py 0.0.0.0 127.0.0.1 3456 3457

1 segment of size 12 + 1024 with a payload of integers, from observation domain 0, with no loss probability, displaying control messages only

sudo python3 generator.py 0.0.0.0 127.0.0.1 3456 3457 -n 2 -r 1 -t json -i 10 -a 1 -l 0.1 -s 1 -d headers

2 messages of 5 shuffled segments of size 1500 with a json payload, from observation domains 10 and 11, with 0.1 loss probability and 1 second sleep time between messages, displaying control messages and segment headers
