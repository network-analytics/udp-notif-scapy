import time
import json
import random
import logging
import os
from unyte_generator.models.unyte_global import UDPN_header_length, OPT_header_length
from unyte_generator.models.udpn import UDPN
from unyte_generator.models.opt import OPT
from unyte_generator.models.payload import PAYLOAD
from scapy.layers.inet import IP, UDP
from scapy.all import send, wrpcap


class udp_notif_generator:

    def __init__(self, args):
        self.source_ip = args.source_ip[0]
        self.destination_ip = args.destination_ip[0]
        self.source_port = int(args.source_port[0])
        self.destination_port = int(args.destination_port[0])
        self.initial_domain = args.initial_domain
        self.additional_domains = args.additional_domains
        self.message_type = args.message_type
        self.message_amount = args.message_amount
        if self.message_amount == 0:
            self.message_amount = float('inf')
        self.mtu = args.mtu
        self.sleep_time = args.sleep_time
        self.loss_probability = args.loss_probability
        self.random_order = args.random_order
        self.display = args.display
        self.pid = os.getpid()

        self.set_logger_level(self.display)
        logging.info("Unyte scapy generator launched")

    def set_logger_level(self, display):
        if display == 'everything':
            logging.basicConfig(format='[%(levelname)s] (' + str(self.pid) + '): %(message)s', level=logging.DEBUG)
        elif display == 'headers':
            logging.basicConfig(format='[%(levelname)s] (' + str(self.pid) + '): %(message)s', level=logging.INFO)
        else:
            # logging.basicConfig(format='[%(levelname)s] (' + str(self.pid) + '): %(message)s', level=logging.INFO)
            logging.disable()

    def log_used_args(self):
        attrs = vars(self)
        logging.info('Used args: ' + ', '.join("%s: %s" % item for item in attrs.items()))

    def log_packet(self, packet):
        logging.info("-------------- packet --------------")
        logging.info("packet version = " + str(packet[UDPN].version))
        logging.info("packet space = " + str(packet[UDPN].space))
        logging.info("packet encoding_type = " + str(packet[UDPN].encoding_type))
        logging.info("packet header_length = " + str(packet[UDPN].header_length))
        logging.info("packet message_length = " + str(packet[UDPN].message_length))
        logging.info("packet observation_domain_id = " + str(packet[UDPN].observation_domain_id))
        logging.info("packet message_id = " + str(packet[UDPN].message_id))
        logging.debug("packet message = " + str(packet[PAYLOAD].message.decode()))
        logging.info("------------ end packet ------------")

    def log_segment(self, segment_increment, segment):
        logging.info("-------------- segment --------------")
        logging.info("segment " + str(segment_increment) + " version = " + str(segment[UDPN].version))
        logging.info("segment " + str(segment_increment) + " space = " + str(segment[UDPN].space))
        logging.info("segment " + str(segment_increment) + " encoding_type = " + str(segment[UDPN].encoding_type))
        logging.info("segment " + str(segment_increment) + " header_length = " + str(segment[UDPN].header_length))
        logging.info("segment " + str(segment_increment) + " message_length = " + str(segment[UDPN].message_length))
        logging.info("segment " + str(segment_increment) + " observation_domain_id = " + str(segment[UDPN].observation_domain_id))
        logging.info("segment " + str(segment_increment) + " message_id " + str(segment[UDPN].message_id))
        logging.info("segment " + str(segment_increment) + " type = " + str(segment[OPT].type))
        logging.info("segment " + str(segment_increment) + " option_length = " + str(segment[OPT].option_length))
        logging.info("segment " + str(segment_increment) + " segment_id = " + str(segment[OPT].segment_id))
        logging.info("segment " + str(segment_increment) + " last = " + str(segment[OPT].last))
        logging.debug("segment " + str(segment_increment) + " message = " + str(segment[PAYLOAD].message.decode()))
        logging.info("------------ end segment ------------")

    def send_udp_notif(self):

        start = time.time()
        npackets = 0
        observation_domains = []
        message_ids = {}
        for i in range(1 + self.additional_domains):
            observation_domains.append(self.initial_domain + i)
            message_ids[observation_domains[i]] = 0

        if (self.display != "control"):
            self.log_used_args()

        # MESSAGE GENERATION
        if self.message_type == "json":
            message = json.dumps(open("./message.json", 'r').read())
            message = json.loads(message)
        elif self.message_type == "ints":
            message = "0123456789"
            for i in range(6):
                message += message
        elif self.message_type == "rand":
            message = "0123456789"
            for i in range(random.randint(6, 12)):
                message += message

        maximum_length = self.mtu - UDPN_header_length

        message_increment = 0

        while message_increment < self.message_amount:

            # for message_increment in range(message_amount):
            message_increment += 1

            segment_list = []

            if message_increment != 0:
                if self.message_type == "rand":
                    message = "0123456789"
                    for i in range(random.randint(6, 12)):
                        message += message
                time.sleep(self.sleep_time)

            domain = observation_domains[message_increment % len(
                observation_domains)]

            # SEGMENTATION
            if len(message) > maximum_length:

                maximum_length = self.mtu - UDPN_header_length - OPT_header_length
                segment_amount = len(message) // maximum_length
                if len(message) % maximum_length != 0:
                    segment_amount += 1

                for segment_increment in range(segment_amount):
                    segment = IP(src=self.source_ip, dst=self.destination_ip)/UDP()/UDPN()/OPT()/PAYLOAD()
                    segment.sport = self.source_port
                    segment.dport = self.destination_port
                    segment[UDPN].observation_domain_id = domain
                    segment[UDPN].message_id = message_ids[domain]
                    segment[UDPN].header_length = UDPN_header_length + \
                        OPT_header_length
                    segment[OPT].segment_id = segment_increment
                    if (len(message[maximum_length * segment_increment:]) > maximum_length):
                        segment[PAYLOAD].message = message[maximum_length *
                                                           segment_increment:maximum_length * (segment_increment + 1)]
                        segment[UDPN].message_length = segment[UDPN].header_length + \
                            len(segment[PAYLOAD].message)
                    else:
                        segment[PAYLOAD].message = message[maximum_length * segment_increment:]
                        segment[UDPN].message_length = segment[UDPN].header_length + \
                            len(segment[PAYLOAD].message)
                        segment[OPT].last = 1
                        message_ids[domain] += 1

                    self.log_segment(segment_increment, segment)

                    segment_list.append(segment)
                    wrpcap('filtered.pcap', segment, append=True)

            # NO SEGMENTATION
            else:
                packet = IP(src=self.source_ip,
                            dst=self.destination_ip)/UDP()/UDPN()/PAYLOAD()
                packet.sport = self.source_port
                packet.dport = self.destination_port
                packet[PAYLOAD].message = message
                packet[UDPN].message_length = packet[UDPN].header_length + \
                    len(packet[PAYLOAD].message)
                packet[UDPN].observation_domain_id = domain
                packet[UDPN].message_id = message_ids[domain]
                message_ids[domain] += 1

                self.log_packet(packet)

                if self.loss_probability == 0:
                    send(packet, verbose=0)
                    npackets += 1
                    wrpcap('filtered.pcap', packet, append=True)
                elif random.randint(1, int(1 / self.loss_probability)) != 1:
                    send(packet, verbose=0)
                    npackets += 1
                    wrpcap('filtered.pcap', packet, append=True)
                else:
                    print("PACKET ", str(packet[UDPN].message_id), " LOST")

            if (self.random_order == 1):
                random.shuffle(segment_list)

            for i in range(len(segment_list)):
                if (self.loss_probability == 0):
                    send(segment_list[i], verbose=0)
                    npackets += 1
                elif random.randint(1, int(1000 * (1 / self.loss_probability))) >= 1000:
                    send(segment_list[i], verbose=0)
                    npackets += 1
                else:
                    print("SEGMENT ", str(segment_list[i][OPT].segment_id), " FROM MESSAGE ", str(
                        segment_list[i][UDPN].message_id), " LOST")
            # print("NOTIFICATION MESSAGE", str(message_increment), "SENT")
        end = time.time()
        duration = end - start
        print(str(duration), str(npackets))
        return
