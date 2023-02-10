import time
import logging
import os
import random
from unyte_generator.utils.unyte_message_gen import mock_message_generator
from unyte_generator.utils.unyte_logger import unyte_logger
from unyte_generator.models.unyte_global import UDPN_LEGACY_HEADER_LEN
from unyte_generator.models.udpn_legacy import UDPN_legacy
from unyte_generator.models.payload import PAYLOAD
from scapy.layers.inet import IP, UDP
from scapy.all import send, wrpcap


class UDP_notif_generator_legacy:

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
        self.legacy = args.legacy == 1

        self.mock_generator = mock_message_generator()

        self.pid = os.getpid()
        self.logger = unyte_logger(self.logging_level, self.pid)
        logging.info("Unyte scapy generator launched")

    def save_pcap(self, filename, packet):
        if self.capture == 1:
            wrpcap(filename, packet, append=True)

    def generate_mock_message(self):
        return self.mock_generator.generate_message(self.message_size)

    def generate_packet_list(self, current_message):
        packet_list = []
        packet = IP(src=self.source_ip, dst=self.destination_ip)/UDP()/UDPN_legacy()/PAYLOAD()
        packet.sport = self.source_port
        packet.dport = self.destination_port
        packet[PAYLOAD].message = current_message
        packet[UDPN_legacy].message_length = UDPN_LEGACY_HEADER_LEN + len(packet[PAYLOAD].message)
        packet_list.append(packet)
        return packet_list

    def forward_current_message(self, packet_list, current_domain_id, current_message_id):
        current_message_lost_packets = 0
        if (self.random_order == 1):
            random.shuffle(packet_list)
        
        for packet in packet_list:
            packet[UDPN_legacy].observation_domain_id = current_domain_id
            packet[UDPN_legacy].message_id = current_message_id
            if (self.probability_of_loss == 0):
                send(packet, verbose=0)
            elif random.randint(1, int(1000 * (1 / self.probability_of_loss))) >= 1000:
                send(packet, verbose=0)
            else:
                current_message_lost_packets += 1
                logging.info("simulating packet number 0 from message_id " + str(packet[UDPN_legacy].message_id) + " lost")
            self.logger.log_packet(packet, self.legacy)

            self.save_pcap('filtered.pcap', packet)
        return current_message_lost_packets

    def send_udp_notif(self):
        timer_start = time.time()
        observation_domains = []
        message_ids = {}
        for i in range(1 + self.additional_domains):
            observation_domains.append(self.initial_domain + i)
            message_ids[observation_domains[i]] = 0

        self.logger.log_used_args(self)
        current_message = self.generate_mock_message()
        maximum_length = self.mtu - UDPN_LEGACY_HEADER_LEN

        lost_packets = 0
        forwarded_packets = 0
        message_increment = 0

        packet_amount = 1

        # Generate packet only once
        packets_list = self.generate_packet_list(current_message)

        while message_increment < self.message_amount:
            current_domain_id = observation_domains[message_increment % len(observation_domains)]
            current_message_id = message_ids[current_domain_id]
            message_ids[current_domain_id] += 1

            current_message_lost_packets = self.forward_current_message(packets_list, current_domain_id, current_message_id)

            forwarded_packets += len(packets_list) - current_message_lost_packets
            lost_packets += current_message_lost_packets
            time.sleep(self.waiting_time)
            message_increment += 1

        timer_end = time.time()
        generation_total_duration = timer_end - timer_start
        logging.warn('Sent ' + str(forwarded_packets) + ' in ' + str(generation_total_duration))
        logging.info('Simulated %d lost packets from %d total packets', lost_packets, (forwarded_packets + lost_packets))
        return forwarded_packets
