#!/usr/bin/python
import sys
import json
import random as rd
from scapy.all import *

def error():
    print("ERROR : wrong arguments, acceptable values are :")
    print("---- IPV4  source (w.x.y.z)")
    print("---- IPV4  destination (w.x.y.z)")
    print("---- INT   source port (1000 < x < 10 000)")
    print("---- INT   destination port (1000 < y < 10 000, y != x)")
    print("---- INT   packet amount, (x > 0)")
    print("---- INT   MTU, (x > 18 if segmentation, x > 12 if single-packet message)")
    print("---- FLOAT sleep time in seconds, (x >= 0)")
    print("---- STR   message type, (x = ints or x = json)")
    print("---- INT   integers amount if previous arg is ints, (x >= 1, amount will be 10 * 2**x)")
    exit(0)
    return

if str(sys.argv[8]) == "json":
    message = json.dumps(open("../message.json", 'r').read()); message = json.loads(message)
elif str(sys.argv[8]) == "ints":
    message = "0123456789"
    for i in range(int(sys.argv[9])): message += message # 2**arg9 times the integers string
else:
    error()
    
udpnhl = 12 # udp-notif header length
ohl = 6 # option header length

nSenders = 4
mgids = []
for i in range(nSenders): mgids.append(2**((i) * 8) - 1) # create an array of message generator ids
index = {}
for i in range(nSenders): index[mgids[i]] = 0 # dictionary with key = message generator ids and values = message id increment

class UDPN(Packet):
    name = "UDPN"
    fields_desc = [ BitField("ver", 0, 3), # Version
                    BitField("spa", 0, 1), # Space
                    BitField("eTyp", 2, 4), # Encoding Type
                    BitField("hLen", udpnhl, 8), # Header Length
                    BitField("mLen", udpnhl + len(message), 16), # Message Length
                    BitField("msgGenID", 0, 32), # Message-Generator-ID
                    BitField("msgID", index[0], 32), ] # Message ID
                    
class OPT(Packet):
    name = "OPT"
    fields_desc = [ BitField("type", 1, 8), # Type
                    BitField("len", ohl, 8), # Length
                    BitField("fraNum", 0, 31), # Fragment Number
                    BitField("L", 0, 1), ] # Last
                    
class PAYLOAD(Packet):
    name = "PAYLOAD"
    fields_desc = [ StrField("msg", message), ] # Notification Message
                

def simulate(source, destination, sourcePort, destinationPort, nMessages, mtu, sleepTime):
    maxl = mtu - udpnhl # maximum UDP length minus UDPN header bytes 2**16 - 1 - UDPN header bytes - OPT header bytes
    if len(message) > maxl:
        maxl = mtu - udpnhl - ohl
    if maxl <= 0: error()
    for i in range(nMessages):
        if i != 0: time.sleep(sleepTime)
        sender = mgids[rd.randint(0, 3)]
        if len(message) > maxl:
            packet = IP(src = source, dst = destination)/UDP()/UDPN()/OPT()/PAYLOAD()
            msg = packet[PAYLOAD].msg
            nSegments = len(msg) // maxl
            if len(msg) % maxl != 0: nSegments += 1 # if the whole division has a remainder, there will be one more segment that will not be full (this is the general case of course)
            for j in range(nSegments):
                segment = packet
                segment.sport = sourcePort
                segment.dport = destinationPort
                segment[UDPN].msgGenID = sender
                segment[UDPN].msgID = index[sender]
                segment[UDPN].hLen = udpnhl + ohl
                segment[OPT].fraNum = j
                if (len(msg[maxl * j:]) > maxl): # if the message string from maxl * j to its end is bigger than max packet size, it isn't the last one
                    segment[PAYLOAD].msg = msg[maxl * j:maxl * (j + 1)] # then evaluate a full message size in the string
                    segment[UDPN].mLen = segment[UDPN].hLen + len(segment[PAYLOAD].msg)
                else: # now it is the last one
                    segment[PAYLOAD].msg = msg[maxl * j:] # then evalutate whatever remains in the string, since it is equal to or lower than maxl * i
                    segment[UDPN].mLen = segment[UDPN].hLen + len(segment[PAYLOAD].msg)
                    segment[OPT].L = 1 # change last value
                    index[sender] += 1 # increment index after sending the last segment of message
                # segment.show()
                # segment[UDPN].show()
                # segment[OPT].show()
                print("segment ", j, " hLen = ", segment[UDPN].hLen)
                print("segment ", j, " mLen = ", segment[UDPN].mLen)
                print("segment ", j, " msgGenID = ", segment[UDPN].msgGenID)
                print("segment ", j, " msgID ", segment[UDPN].msgID)
                print("segment ", j, " msg = ", segment[PAYLOAD].msg.decode())
                print("segment ", j, " type = ", segment[OPT].type)
                print("segment ", j, " fraNum = ", segment[OPT].fraNum)
                print("segment ", j, " optlen = ", segment[OPT].len)
                print("segment ", j, " L = ", segment[OPT].L)
                send(segment)
                wrpcap('filtered.pcap', segment, append=True)
        else:
            packet = IP(src = source, dst = destination)/UDP()/UDPN()/PAYLOAD()
            packet.sport = sourcePort
            packet.dport = destinationPort
            packet[UDPN].msgGenID = sender
            packet[UDPN].msgID = index[sender]
            index[sender] += 1
            # packet.show()
            # packet[UDPN].show()
            print("packet mLen = ", packet[UDPN].mLen)
            print("packet msgGenID = ",packet[UDPN].msgGenID)
            print("packet msgID ", packet[UDPN].msgID)
            print("packet msg = ", packet[PAYLOAD].msg.decode())
            send(packet)
            wrpcap('filtered.pcap', packet, append=True)
        print("Notification message ", str(i), " sent")
    return

simulate(str(sys.argv[1]), str(sys.argv[2]), int(sys.argv[3]), int(sys.argv[4]), int(sys.argv[5]), int(sys.argv[6]), int(sys.argv[7]))
#   python3 simulation.py "192.0.2.4" "192.0.2.2" 6000 6001 1
#   simulate("192.0.2.4", "192.0.2.2", 9340, 9341, 10)