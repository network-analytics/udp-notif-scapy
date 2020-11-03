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
    print("---- FLOAT probability to drop a packet / segment")
    exit(0)
    return
    
udpnhl = 12 # udp-notif header length
ohl = 4 # option header length

nSenders = 4
mgids = []
for i in range(nSenders): mgids.append(2**((i) * 8) - 1) # create an array of message generator ids
index = {}
for i in range(nSenders): index[mgids[i]] = 0 # dictionary with key = message generator ids and values = message id increment

class UDPN(Packet):
    name = "UDPN"
    fields_desc = [ BitField("ver", 0, 3), # Version
                    BitField("spa", 0, 1), # Space
                    BitField("eTyp", 1, 4), # Encoding Type
                    BitField("hLen", udpnhl, 8), # Header Length
                    BitField("mLen", udpnhl, 16), # Message Length
                    BitField("msgGenID", 0, 32), # Message-Generator-ID
                    BitField("msgID", 0, 32), ] # Message ID
                    
class OPT(Packet):
    name = "OPT"
    fields_desc = [ BitField("type", 1, 8), # Type
                    BitField("optlen", ohl, 8), # Length
                    BitField("fraNum", 0, 15), # Fragment Number
                    BitField("L", 0, 1), ] # Last
                    
class PAYLOAD(Packet):
    name = "PAYLOAD"
    fields_desc = [ StrField("msg", "idle"), ] # Notification Message
                

def generate(source, destination, sourcePort, destinationPort, nMessages, mtu, sleepTime):
    
    # MESSAGE GENERATION
    if str(sys.argv[8]) == "json":
        message = json.dumps(open("../message.json", 'r').read()); message = json.loads(message)
    elif str(sys.argv[8]) == "ints":
        message = "0123456789"
        for n in range(10):
            message += message # 2**10 times the integers string
    elif str(sys.argv[8]) == "rand":
        message = "0123456789"
        for m in range(rd.randint(6, 12)):
            message += message # 2**randint(1,9) times the integers string
    else:
        error()
    
    maxl = mtu - udpnhl # maximum UDP length minus header bytes
    for i in range(nMessages):
        
        # CHANGE MESSAGE IF GENERATION MUST BE RANDOM
        if str(sys.argv[8]) == "rand":
            message = "0123456789"
            for k in range(rd.randint(6, 12)):
                message += message
                
        if i != 0: time.sleep(sleepTime)
        sender = mgids[rd.randint(0, 3)]
        
        # CASE WITH SEGMENTATION
        if len(message) > maxl:
            maxl = mtu - udpnhl - ohl
            packet = IP(src = source, dst = destination)/UDP()/UDPN()/OPT()/PAYLOAD()
            packet[PAYLOAD].msg = message
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
                    
                # DISPLAY USEFUL INFORMATION
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
                print("segment ", j, " optlen = ", segment[OPT].optlen)
                print("segment ", j, " L = ", segment[OPT].L)
                if float(sys.argv[9]) == 0:
                    send(segment)
                    wrpcap('filtered.pcap', segment, append=True)
                elif rd.randint(1, int(1 / float(sys.argv[9]))) != 1:
                    send(segment)
                    wrpcap('filtered.pcap', segment, append=True)
                else:
                    print("\n\n\nSEGMENT DROPPED\n\n\n")
        # CASE WITHOUT SEGMENTATION
        else:
            packet = IP(src = source, dst = destination)/UDP()/UDPN()/PAYLOAD()
            packet.sport = sourcePort
            packet.dport = destinationPort
            packet[PAYLOAD].msg = message
            packet[UDPN].mLen = packet[UDPN].hLen + len(packet[PAYLOAD].msg)
            packet[UDPN].msgGenID = sender
            packet[UDPN].msgID = index[sender]
            index[sender] += 1
            
            # DISPLAY USEFUL INFORMATION
            # packet.show()
            # packet[UDPN].show()
            print("packet mLen = ", packet[UDPN].mLen)
            print("packet msgGenID = ",packet[UDPN].msgGenID)
            print("packet msgID ", packet[UDPN].msgID)
            print("packet msg = ", packet[PAYLOAD].msg.decode())
            if float(sys.argv[9]) == 0:
                send(packet)
                wrpcap('filtered.pcap', packet, append=True)
            elif rd.randint(1, int(1 / float(sys.argv[9]))) != 1:
                send(packet)
                wrpcap('filtered.pcap', packet, append=True)
            else:
                print("\n\n\nPACKET DROPPED\n\n\n")
        print("Notification message ", str(i), " sent")
    return

generate(str(sys.argv[1]), str(sys.argv[2]), int(sys.argv[3]), int(sys.argv[4]), int(sys.argv[5]), int(sys.argv[6]), int(sys.argv[7]))