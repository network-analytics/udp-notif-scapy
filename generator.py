#!/usr/bin/python
import os
import sys
import json
import time
import argparse
import random as rd
from scapy.all import *

udpnhl = 12  # udp-notif header length
ohl = 4  # option header length

nSenders = 4
mgids = []
for i in range(nSenders):
    mgids.append(2**((i) * 8) - 1)  # create an array of message generator ids
index = {}
for i in range(nSenders):
    # dictionary with key = message generator ids and values = message id increment
    index[mgids[i]] = 0


class UDPN(Packet):
    name = "UDPN"
    fields_desc = [BitField("ver", 0, 3),  # Version ver
                   BitField("spa", 0, 1),  # Space spa
                   BitField("eTyp", 1, 4),  # Encoding Type encTyp
                   BitField("hLen", udpnhl, 8),  # Header Length heaLen
                   BitField("mLen", udpnhl, 16),  # Message Length msgLen
                   BitField("msgGenID", 0, 32),  # Message-Generator-ID genID
                   BitField("msgID", 0, 32), ]  # Message ID msgID


class OPT(Packet):
    name = "OPT"
    fields_desc = [BitField("type", 1, 8),  # Type typ
                   BitField("optlen", ohl, 8),  # Length optLen
                   BitField("fraNum", 0, 15),  # Fragment Number segNum
                   BitField("L", 0, 1), ]  # Last last


class PAYLOAD(Packet):
    name = "PAYLOAD"
    fields_desc = [StrField("msg", "idle"), ]  # Notification Message


def generate(args):

    # Setting vars

    source = args.src_ip[0]
    destination = args.dest_ip[0]
    sourcePort = int(args.src_port[0])
    destinationPort = int(args.dest_port[0])
    nMessages = args.packet_amount
    mtu = args.mtu
    sleepTime = args.sleep_time
    messageType = args.type
    discardProbability = args.packet_loss_proba
    verbose = args.verbose

    display = "none"
    if (verbose == 1):
        display = "header"
    elif (verbose == 2):
        display = "all"

    if (display != "none"):
        print("source : ", source)
        print("destination : ", destination)
        print("sourcePort : ", sourcePort)
        print("destinationPort : ", destinationPort)
        print("nMessages : ", nMessages)
        print("mtu : ", mtu)
        print("sleepTime : ", sleepTime)
        print("messageType : ", messageType)
        print("discardProbability : ", discardProbability)
        print("verbose : ", verbose)

    # MESSAGE GENERATION
    if messageType == "json":
        message = json.dumps(open("message.json", 'r').read())
        message = json.loads(message)
    elif messageType == "ints":
        message = "0123456789"
        for n in range(10):
            message += message  # 2**10 times the integers string
    elif messageType == "rand":
        message = "0123456789"
        for m in range(rd.randint(6, 12)):
            message += message  # 2**randint(1,9) times the integers string
    else:
        # can't happen anymore
        pass

    maxl = mtu - udpnhl  # maximum UDP length minus header bytes
    for i in range(nMessages):

        # CHANGE MESSAGE IF GENERATION MUST BE RANDOM
        if messageType == "rand":
            message = "0123456789"
            for k in range(rd.randint(6, 12)):
                message += message

        if i != 0:
            time.sleep(sleepTime)
        sender = mgids[rd.randint(0, 3)]

        # CASE WITH SEGMENTATION
        if len(message) > maxl:
            maxl = mtu - udpnhl - ohl
            packet = IP(src=source, dst=destination)/UDP()/UDPN()/OPT()/PAYLOAD()
            packet[PAYLOAD].msg = message
            msg = packet[PAYLOAD].msg
            nSegments = len(msg) // maxl
            if len(msg) % maxl != 0:
                # if the whole division has a remainder, there will be one more segment that will not be full (this is the general case of course)
                nSegments += 1
            for j in range(nSegments):
                segment = packet
                segment.sport = sourcePort
                segment.dport = destinationPort
                segment[UDPN].msgGenID = sender
                segment[UDPN].msgID = index[sender]
                segment[UDPN].hLen = udpnhl + ohl
                segment[OPT].fraNum = j
                # if the message string from maxl * j to its end is bigger than max packet size, it isn't the last one
                if (len(msg[maxl * j:]) > maxl):
                    # then evaluate a full message size in the string
                    segment[PAYLOAD].msg = msg[maxl * j:maxl * (j + 1)]
                    segment[UDPN].mLen = segment[UDPN].hLen + len(segment[PAYLOAD].msg)
                else:  # now it is the last one
                    # then evalutate whatever remains in the string, since it is equal to or lower than maxl * i
                    segment[PAYLOAD].msg = msg[maxl * j:]
                    segment[UDPN].mLen = segment[UDPN].hLen + len(segment[PAYLOAD].msg)
                    segment[OPT].L = 1  # change last value
                    # increment index after sending the last segment of message
                    index[sender] += 1

                if display == "header" or display == "all":
                    print("segment ", j, " ver = ", segment[UDPN].ver)
                    print("segment ", j, " spa = ", segment[UDPN].spa)
                    print("segment ", j, " eTyp = ", segment[UDPN].eTyp)
                    print("segment ", j, " hLen = ", segment[UDPN].hLen)
                    print("segment ", j, " mLen = ", segment[UDPN].mLen)
                    print("segment ", j, " msgGenID = ",
                          segment[UDPN].msgGenID)
                    print("segment ", j, " msgID ", segment[UDPN].msgID)
                    print("segment ", j, " type = ", segment[OPT].type)
                    print("segment ", j, " fraNum = ", segment[OPT].fraNum)
                    print("segment ", j, " optlen = ", segment[OPT].optlen)
                    print("segment ", j, " L = ", segment[OPT].L)
                    if display == "all":
                        print("segment ", j, " msg = ",
                              segment[PAYLOAD].msg.decode())
                elif display != "none":
                    pass

                if (discardProbability == 0):
                    send(segment)
                    wrpcap('filtered.pcap', segment, append=True)
                elif rd.randint(1, int(1 / discardProbability)) != 1:
                    send(segment)
                    wrpcap('filtered.pcap', segment, append=True)
                else:
                    print("\n\n\nSEGMENT DROPPED\n\n\n")
        # CASE WITHOUT SEGMENTATION
        else:
            packet = IP(src=source, dst=destination)/UDP()/UDPN()/PAYLOAD()
            packet.sport = sourcePort
            packet.dport = destinationPort
            packet[PAYLOAD].msg = message
            packet[UDPN].mLen = packet[UDPN].hLen + len(packet[PAYLOAD].msg)
            packet[UDPN].msgGenID = sender
            packet[UDPN].msgID = index[sender]
            index[sender] += 1
            if display == "header" or display == "all":
                print("packet ver = ", packet[UDPN].ver)
                print("packet spa = ", packet[UDPN].spa)
                print("packet eTyp = ", packet[UDPN].eTyp)
                print("packet hLen = ", packet[UDPN].hLen)
                print("packet mLen = ", packet[UDPN].mLen)
                print("packet msgGenID = ", packet[UDPN].msgGenID)
                print("packet msgID = ", packet[UDPN].msgID)
                if display == "all":
                    print("packet msg = ", packet[PAYLOAD].msg.decode())
            elif display != "none":
                pass

            if discardProbability == 0:
                send(packet)
                wrpcap('filtered.pcap', packet, append=True)
            elif rd.randint(1, int(1 / discardProbability)) != 1:
                send(packet)
                wrpcap('filtered.pcap', packet, append=True)
            else:
                print("\n\n\nPACKET DROPPED\n\n\n")
        print("Notification message ", str(i), " sent")
    return


if __name__ == "__main__":

    # argparse part and all it's components

    parser = argparse.ArgumentParser(
        description='Process scapy call arguments.')
    parser.add_argument('src_ip', metavar='src-ip', nargs=1,
                        help='w.x.y.z source IPv4 address.')
    parser.add_argument('dest_ip', metavar='dest-ip', nargs=1,
                        help='w.x.y.z dest IPv4 address.')
    parser.add_argument('src_port', metavar='src-port', nargs=1, type=int,
                        help='1000 < port < 10 000')
    parser.add_argument('dest_port', metavar='dest-port',
                        nargs=1, type=int, help='1000 < port < 10 000')
    parser.add_argument('mtu', type=int, help='The packets MTU.')
    parser.add_argument('--packet-amount', '-n', type=int,
                        default=1, help='The number of packets to be sent')
    parser.add_argument('--sleep-time', '-s', type=float,
                        default=0.0, help='The sleep time between packets.')
    parser.add_argument('--type', '-t', default="ints",
                        choices=["ints", "json"], help='The type of data sent')
    parser.add_argument('--packet-loss-proba', '-l', type=float, default=0,
                        help='The probability of a packet loss during transmission')
    parser.add_argument('--verbose', '-v', type=int, default=0,
                        choices=[0, 1, 2], help='The verbosity level of the program. 0 : Show nothing. 1 : Show only messages headers. 2 : Show all messages')

    args = parser.parse_args()

    generate(args)
