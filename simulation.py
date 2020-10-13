#!/usr/bin/python
 
import sys
import json
import random as rd
from scapy.all import *

message = "{\"hello\":\"Tom\"}"
#	message = json.dumps(open("../message.json", 'r').read())
#	message = json.loads(message)
#	print(message)

nSenders = 5 # 4 senders actually, 0 being used as an error detector

mgids = []
for i in range(nSenders): mgids.append(2**((i) * 8) - 1) # create an array of message generator ids

index = {}
for i in range(nSenders): index[mgids[i]] = 0 # dictionary with key = message generator ids and values = message id increment

class UDPN(Packet):
	name = "UDPN"
	fields_desc = [	BitField("ver", 0, 3), # Version
					BitField("spa", 0, 1), # Space
					BitField("eTyp", 2, 4), # Encoding Type
					BitField("hLen", 12, 8), # Header Length
					BitField("mLen", 12 + len(message), 16), # Message Length
					BitField("msgGenID", 0, 32), # Message-Generator-ID
					BitField("msgID", index[0], 32), # Message ID
					StrField("nMsg", message), ] # Notification Message

def simulate(source, destination, sourcePort, destinationPort, nPackets):
	for i in range(nPackets):
		sender = mgids[rd.randint(1, 4)]
		packet = IP(src = source, dst = destination)/UDP()/UDPN()
		packet.sport = sourcePort
		packet.dport = destinationPort
		packet[UDPN].msgGenID = sender
		packet[UDPN].msgID = index[sender]
		index[sender] += 1
		packet.show()
		send(packet)
		# wireshark(packet)
	return

#	simulate("192.0.2.4", "192.0.2.2", 9340, 9341, 10)

simulate(str(sys.argv[1]), str(sys.argv[2]), int(sys.argv[3]), int(sys.argv[4]), int(sys.argv[5])) # python3 simulation.py "192.0.2.4" "192.0.2.2" 6000 6001 1