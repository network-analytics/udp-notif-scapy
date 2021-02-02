#!/usr/bin/python
import os
import sys
import json
import time
import argparse
import random
from unyte_generator.models.unyte_global import UDPN_header_length, OPT_header_length
from unyte_generator.models.udpn import UDPN
from unyte_generator.models.opt import OPT
from unyte_generator.models.payload import PAYLOAD

from scapy.all import IP, UDP, send, wrpcap

def generate(args):
    
    start = time.time()
    npackets = 0

    # SOURCE AND DESTINATION DATA
    source_ip = args.source_ip[0]
    destination_ip = args.destination_ip[0]
    source_port = int(args.source_port[0])
    destination_port = int(args.destination_port[0])
    # DOMAIN START VALUE AND AMOUNT
    initial_domain = args.initial_domain
    additional_domains = args.additional_domains
    # MESSAGE TYPE AND AMOUNT
    message_type = args.message_type
    message_amount = args.message_amount
    # INFINITE MESSAGES
    if message_amount == 0:
        message_amount = float('inf')
    # FORWARDING RULES
    mtu = args.mtu
    sleep_time = args.sleep_time
    # RANDOMNESS
    loss_probability = args.loss_probability
    random_order = args.random_order
    # DISPLAY
    display = args.display
    
    observation_domains = []
    message_ids = {}
    for i in range(1 + additional_domains):
        observation_domains.append(initial_domain + i)
        message_ids[observation_domains[i]] = 0

    if (display != "control"):
        # SOURCE AND DESTINATION DATA
        print("source_ip : ", source_ip)
        print("destination_ip : ", destination_ip)
        print("source_port : ", source_port)
        print("destination_port : ", destination_port)
        # DOMAIN START VALUE AND AMOUNT
        print("initial_domain : ", initial_domain)
        print("additional_domains : ", additional_domains)
        # MESSAGE TYPE AND AMOUNT
        print("message_type : ", message_type)
        print("message_amount : ", message_amount)
        # FORWARDING RULES
        print("mtu : ", mtu)
        print("sleep_time : ", sleep_time)
        # RANDOMNESS
        print("loss_probability : ", loss_probability)
        print("random_order : ", random_order)
        # DISPLAY
        print("display : ", display)

    # MESSAGE GENERATION
    if message_type == "json":
        message = json.dumps(open("./message.json", 'r').read())
        message = json.loads(message)
    elif message_type == "ints":
        message = "0123456789"
        for i in range(6):
            message += message
    elif message_type == "rand":
        message = "0123456789"
        for i in range(random.randint(6, 12)):
            message += message

    maximum_length = mtu - UDPN_header_length
    
    message_increment = 0
    
    while message_increment < message_amount:
    
    #for message_increment in range(message_amount):
        message_increment += 1
        
        segment_list = []

        if message_increment != 0:
            if message_type == "rand":
                message = "0123456789"
                for i in range(random.randint(6, 12)):
                    message += message
            time.sleep(sleep_time)
        
        domain = observation_domains[message_increment%len(observation_domains)]

        # SEGMENTATION
        if len(message) > maximum_length:
            
            maximum_length = mtu - UDPN_header_length - OPT_header_length
            segment_amount = len(message) // maximum_length
            if len(message) % maximum_length != 0:
                segment_amount += 1
                
            for segment_increment in range(segment_amount):
                segment = IP(src=source_ip, dst=destination_ip)/UDP()/UDPN()/OPT()/PAYLOAD()
                segment.sport = source_port
                segment.dport = destination_port
                segment[UDPN].observation_domain_id = domain
                segment[UDPN].message_id = message_ids[domain]
                segment[UDPN].header_length = UDPN_header_length + OPT_header_length
                segment[OPT].segment_id = segment_increment
                if (len(message[maximum_length * segment_increment:]) > maximum_length):
                    segment[PAYLOAD].message = message[maximum_length * segment_increment:maximum_length * (segment_increment + 1)]
                    segment[UDPN].message_length = segment[UDPN].header_length + len(segment[PAYLOAD].message)
                else:
                    segment[PAYLOAD].message = message[maximum_length * segment_increment:]
                    segment[UDPN].message_length = segment[UDPN].header_length + len(segment[PAYLOAD].message)
                    segment[OPT].last = 1
                    message_ids[domain] += 1

                if display != "control":
                    # UPDN
                    print("segment ", segment_increment, " version = ", segment[UDPN].version)
                    print("segment ", segment_increment, " space = ", segment[UDPN].space)
                    print("segment ", segment_increment, " encoding_type = ", segment[UDPN].encoding_type)
                    print("segment ", segment_increment, " header_length = ", segment[UDPN].header_length)
                    print("segment ", segment_increment, " message_length = ", segment[UDPN].message_length)
                    print("segment ", segment_increment, " observation_domain_id = ", segment[UDPN].observation_domain_id)
                    print("segment ", segment_increment, " message_id ", segment[UDPN].message_id)
                    # OPT
                    print("segment ", segment_increment, " type = ", segment[OPT].type)
                    print("segment ", segment_increment, " option_length = ", segment[OPT].option_length)
                    print("segment ", segment_increment, " segment_id = ", segment[OPT].segment_id)
                    print("segment ", segment_increment, " last = ", segment[OPT].last)
                    # PAYLOAD
                    if display == "everything":
                        print("segment ", segment_increment, " message = ", segment[PAYLOAD].message.decode())
                    
                segment_list.append(segment)
                wrpcap('filtered.pcap', segment, append=True)
                    
        # NO SEGMENTATION
        else:
            packet = IP(src=source_ip, dst=destination_ip)/UDP()/UDPN()/PAYLOAD()
            packet.sport = source_port
            packet.dport = destination_port
            packet[PAYLOAD].message = message
            packet[UDPN].message_length = packet[UDPN].header_length + len(packet[PAYLOAD].message)
            packet[UDPN].observation_domain_id = domain
            packet[UDPN].message_id = message_ids[domain]
            message_ids[domain] += 1
            if display != "control":
                # UDPN
                print("packet version = ", packet[UDPN].version)
                print("packet space = ", packet[UDPN].space)
                print("packet encoding_type = ", packet[UDPN].encoding_type)
                print("packet header_length = ", packet[UDPN].header_length)
                print("packet message_length = ", packet[UDPN].message_length)
                print("packet observation_domain_id = ", packet[UDPN].observation_domain_id)
                print("packet message_id = ", packet[UDPN].message_id)
                # PAYLOAD
                if display == "everything":
                    print("packet message = ", packet[PAYLOAD].message.decode())

            if loss_probability == 0:
                send(packet, verbose=0)
                npackets += 1
                wrpcap('filtered.pcap', packet, append=True)
            elif random.randint(1, int(1 / loss_probability)) != 1:
                send(packet, verbose=0)
                npackets += 1
                wrpcap('filtered.pcap', packet, append=True)
            else:
                print("PACKET ", str(packet[UDPN].message_id)," LOST")
                
        if (random_order == 1):
            random.shuffle(segment_list)
        
        for i in range(len(segment_list)):
            if (loss_probability == 0):
                send(segment_list[i], verbose=0)
                npackets += 1
            elif random.randint(1, int(1000 * (1 / loss_probability))) >= 1000:
                send(segment_list[i], verbose=0)
                npackets += 1
            else:
                print("SEGMENT ", str(segment_list[i][OPT].segment_id), " FROM MESSAGE ", str(segment_list[i][UDPN].message_id)," LOST")
        # print("NOTIFICATION MESSAGE", str(message_increment), "SENT")
    end = time.time()
    duration = end - start
    print(str(duration), str(npackets))
    return


if __name__ == "__main__":

    # ARGPARSE
    parser = argparse.ArgumentParser(description='Process scapy call arguments.')
    
    # SOURCE AND DESTINATION DATA
    parser.add_argument('source_ip', metavar='source-ip', nargs=1,
                        help='w.x.y.z source IPv4 address.')
    parser.add_argument('destination_ip', metavar='destination-ip', nargs=1,
                        help='w.x.y.z dest IPv4 address.')
    parser.add_argument('source_port', metavar='source-port', nargs=1, type=int,
                        help='1000 < source_port < 10 000')
    parser.add_argument('destination_port', metavar='destination-port', nargs=1, type=int,
                        help='1000 < destination_port < 10 000 and destination_port != source_port')
    # DOMAIN START VALUE AND AMOUNT
    parser.add_argument('--initial-domain', '-i', type=int,
                        default=0, help='Identifier of the initial observation domain')
    parser.add_argument('--additional-domains', '-a', type=int,
                        default=0, help='Amount of observation domains in addition to the first')
    # MESSAGE TYPE AND AMOUNT
    parser.add_argument('--message-type', '-t',
                        default="ints", choices=["ints", "json", "rand"], help='The type of data sent')
    parser.add_argument('--message-amount', '-n', type=int,
                        default=1, help='Amount of notification messages to send')
    # FORWARDING RULES
    parser.add_argument('--mtu', '-m', type=int,
                        default=1500, help='Maximum Transmission Unit')
    parser.add_argument('--sleep-time', '-s', type=float,
                        default=0, help='Sleep time between sending two notification messages')
    # RANDOMNESS
    parser.add_argument('--loss-probability', '-l', type=float,
                        default=0, help='Probability of a packet loss during transmission')
    parser.add_argument('--random-order', '-r', type=int,
                        default=0, help='Whether the segments must be sent in a random order or not')
    # DISPLAY
    parser.add_argument('--display', '-d',
                        default="control", choices=["control", "headers", "everything"], help='Information display, from only control messages to payloads')

    args = parser.parse_args()

    generate(args)
