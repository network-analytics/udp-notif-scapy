import logging
import os
import random
import time

from scapy.all import send, wrpcap
from scapy.layers.inet import IP, UDP

from unyte_generator.models.payload import PAYLOAD
from unyte_generator.models.udpn_legacy import UDPN_legacy
from unyte_generator.models.unyte_global import UDPN_LEGACY_HEADER_LEN
from unyte_generator.utils.unyte_logger import unyte_logger
from unyte_generator.utils.unyte_message_gen import Mock_payload_reader


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

        self.mock_payload_reader = Mock_payload_reader()

        self.pid = os.getpid()
        self.logger = unyte_logger(self.logging_level, self.pid)
        logging.info("Unyte scapy generator launched")

    def save_pcap(self, filename, packet):
        if self.capture == 1:
            wrpcap(filename, packet, append=True)

    def generate_mock_payload(self, nb_payloads: int) -> list:
        return self.mock_payload_reader.get_json_push_update_notif(nb_payloads=nb_payloads)

    def generate_packet_list(self, current_message):
        packet_list = []
        packet = IP(src=self.source_ip, dst=self.destination_ip)/UDP()/UDPN_legacy()/PAYLOAD()
        packet.sport = self.source_port
        packet.dport = self.destination_port
        packet[PAYLOAD].message = current_message
        packet[UDPN_legacy].message_length = UDPN_LEGACY_HEADER_LEN + len(packet[PAYLOAD].message)
        packet_list.append(packet)
        return packet_list

    def forward_current_message(self, packet_list, current_domain_id):
        current_message_lost_packets = 0
        if (self.random_order == 1):
            random.shuffle(packet_list)

        msg_id = 0
        for packet in packet_list:
            packet[UDPN_legacy].observation_domain_id = current_domain_id
            packet[UDPN_legacy].message_id = msg_id
            if (self.probability_of_loss == 0):
                send(packet, verbose=0)
            elif random.randint(1, int(1000 * (1 / self.probability_of_loss))) >= 1000:
                send(packet, verbose=0)
            else:
                current_message_lost_packets += 1
                logging.info("simulating packet number 0 from message_id " + str(packet[UDPN_legacy].message_id) + " lost")
            self.logger.log_packet(packet, True)
            msg_id += 1
            self.save_pcap('filtered.pcap', packet)

        return current_message_lost_packets

    def send_udp_notif(self):
        timer_start = time.time()

        self.logger.log_used_args(self)
        current_message = self.generate_mock_payload(nb_payloads=self.message_amount)

        lost_packets = 0
        forwarded_packets = 0

        # Generate packet only once
        packets_list = self.generate_packet_list(current_message)
        obs_domain_id = self.initial_domain
        for _ in range(self.message_amount):
            current_message_lost_packets = self.forward_current_message(packets_list, obs_domain_id)
            forwarded_packets += len(packets_list) - current_message_lost_packets
            lost_packets += current_message_lost_packets
            time.sleep(self.waiting_time)

            obs_domain_id += 1
            if obs_domain_id > (self.initial_domain + self.additional_domains):
                obs_domain_id = self.initial_domain

        timer_end = time.time()
        generation_total_duration = timer_end - timer_start
        logging.warn('Sent ' + str(forwarded_packets) + ' in ' + str(generation_total_duration))
        logging.info('Simulated %d lost packets from %d total packets', lost_packets, (forwarded_packets + lost_packets))
        return forwarded_packets
