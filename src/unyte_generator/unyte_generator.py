import time
import logging
import os
import random
from unyte_generator.utils.unyte_message_gen import mock_message_generator
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
        self.message_size = args.message_size
        self.message_amount = args.message_amount
        if self.message_amount == 0:
            self.message_amount = float('inf')
        self.mtu = args.mtu
        self.waiting_time = args.waiting_time
        self.probability_of_loss = args.probability_of_loss
        self.random_order = args.random_order
        self.logging_level = args.logging_level
        self.capture = args.capture

        self.mock_generator = mock_message_generator()

        self.pid = os.getpid()
        self.set_logger_level(self.logging_level)
        logging.info("Unyte scapy generator launched")

    def set_logger_level(self, logging_level):
        if logging_level == 'debug':
            logging.basicConfig(format='[%(levelname)s] (' + str(self.pid) + '): %(message)s', level=logging.DEBUG)
        elif logging_level == 'info':
            logging.basicConfig(format='[%(levelname)s] (' + str(self.pid) + '): %(message)s', level=logging.INFO)
        elif logging_level == 'warning':
            logging.basicConfig(format='[%(levelname)s] (' + str(self.pid) + '): %(message)s', level=logging.WARNING)
        elif logging_level == 'none':
            logging.disable(level=logging.DEBUG)

    def log_used_args(self):
        attrs = vars(self)
        logging.info('Used args: ' + ', '.join("%s: %s" % item for item in attrs.items()))

    def log_header_udpn(self, packet):
        logging.info("packet version = " + str(packet[UDPN].version))
        logging.info("packet space = " + str(packet[UDPN].space))
        logging.info("packet encoding type = " + str(packet[UDPN].encoding_type))
        logging.info("packet header length = " + str(packet[UDPN].header_length))
        logging.info("packet message length = " + str(packet[UDPN].message_length))
        logging.info("packet observation domain id = " + str(packet[UDPN].observation_domain_id))
        logging.info("packet message id = " + str(packet[UDPN].message_id))

    def log_header_opt(self, packet):
        logging.info("packet type = " + str(packet[OPT].type))
        logging.info("packet option length = " + str(packet[OPT].option_length))
        logging.info("packet segment id = " + str(packet[OPT].segment_id))
        logging.info("packet last = " + str(packet[OPT].last))

    def log_packet(self, packet):
        logging.info("---------------- packet ----------------")
        self.log_header_udpn(packet)
        logging.debug("packet message = " + str(packet[PAYLOAD].message.decode()))
        logging.info("-------------- end packet --------------")

    def log_segment(self, packet, packet_increment):
        logging.info("---------- packet (segment " + str(packet_increment) + ") ----------")
        self.log_header_udpn(packet)
        self.log_header_opt(packet)
        logging.debug("packet message = " + str(packet[PAYLOAD].message.decode()))
        logging.info("-------- end packet (segment " + str(packet_increment) + ") --------")

    def save_pcap(self, filename, packet):
        if self.capture == 1:
            wrpcap(filename, packet, append=True)

    def generate_mock_message(self):
        return self.mock_generator.generate_message(self.message_size)

    def generate_packet_list(self, packet_amount, maximum_length, current_message, current_domain_id, current_message_id):
        packet_list = []
        for packet_increment in range(packet_amount):
            if packet_amount == 1:
                packet = IP(src=self.source_ip, dst=self.destination_ip)/UDP()/UDPN()/PAYLOAD()
            else:
                packet = IP(src=self.source_ip, dst=self.destination_ip)/UDP()/UDPN()/OPT()/PAYLOAD()
            packet.sport = self.source_port
            packet.dport = self.destination_port
            packet[UDPN].observation_domain_id = current_domain_id
            packet[UDPN].message_id = current_message_id
            if packet_amount == 1:
                packet[PAYLOAD].message = current_message
                packet[UDPN].message_length = packet[UDPN].header_length + len(packet[PAYLOAD].message)
            else:
                packet[UDPN].header_length = UDPN_header_length + OPT_header_length
                packet[OPT].segment_id = packet_increment
                if (len(current_message[maximum_length * packet_increment:]) > maximum_length):
                    packet[PAYLOAD].message = current_message[maximum_length * packet_increment:maximum_length * (packet_increment + 1)]
                    packet[UDPN].message_length = packet[UDPN].header_length + len(packet[PAYLOAD].message)
                else:
                    packet[PAYLOAD].message = current_message[maximum_length * packet_increment:]
                    packet[UDPN].message_length = packet[UDPN].header_length + len(packet[PAYLOAD].message)
                    packet[OPT].last = 1
            if packet_amount == 1:
                self.log_packet(packet)
            else:
                self.log_segment(packet, packet_increment)
            self.save_pcap('filtered.pcap', packet)
            packet_list.append(packet)
        return packet_list

    def forward_current_message(self, packet_list):
        current_message_lost_packets = 0
        if (self.random_order == 1):
            random.shuffle(packet_list)
        for i in range(len(packet_list)):
            if (self.probability_of_loss == 0):
                send(packet_list[i], verbose=0)
            elif random.randint(1, int(1000 * (1 / self.probability_of_loss))) >= 1000:
                send(packet_list[i], verbose=0)
            else:
                current_message_lost_packets += 1
                if len(packet_list) == 1:
                    logging.info("simulating packet number 0 from message_id " + str(packet_list[i][UDPN].message_id) + " lost")
                else:
                    logging.info("simulating packet number " + str(packet_list[i][OPT].segment_id) +
                                 " from message_id " + str(packet_list[i][UDPN].message_id) + " lost")
        return current_message_lost_packets

    def send_udp_notif(self):
        timer_start = time.time()
        observation_domains = []
        message_ids = {}
        for i in range(1 + self.additional_domains):
            observation_domains.append(self.initial_domain + i)
            message_ids[observation_domains[i]] = 0

        self.log_used_args()
        current_message = self.generate_mock_message()
        maximum_length = self.mtu - UDPN_header_length

        lost_packets = 0
        forwarded_packets = 0

        for message_increment in range(self.message_amount):
            current_domain_id = observation_domains[message_increment % len(observation_domains)]
            current_message_id = message_ids[current_domain_id]
            message_ids[current_domain_id] += 1

            if len(current_message) > maximum_length:
                maximum_length = self.mtu - UDPN_header_length - OPT_header_length
                packet_amount = len(current_message) // maximum_length
                if len(current_message) % maximum_length != 0:
                    packet_amount += 1
                packet_list = self.generate_packet_list(packet_amount, maximum_length, current_message, current_domain_id, current_message_id)
            else:
                packet_amount = 1
                packet_list = self.generate_packet_list(packet_amount, maximum_length, current_message, current_domain_id, current_message_id)

            current_message_lost_packets = self.forward_current_message(packet_list)
            forwarded_packets += len(packet_list) - current_message_lost_packets
            lost_packets += current_message_lost_packets
            time.sleep(self.waiting_time)

        timer_end = time.time()
        generation_total_duration = timer_end - timer_start
        logging.info('Sent ' + str(forwarded_packets) + ' in ' + str(generation_total_duration))
        logging.info('Simulated %d lost packets from %d total packets', lost_packets, (forwarded_packets + lost_packets))
        return forwarded_packets
