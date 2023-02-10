import logging
import os
import random
import time

from scapy.all import send, wrpcap
from scapy.layers.inet import IP, UDP

from unyte_generator.models.opt import SEGMENTATION_OPT
from unyte_generator.models.payload import PAYLOAD
from unyte_generator.models.udpn import UDPN
from unyte_generator.models.unyte_global import (UDPN_HEADER_LEN,
                                                 UDPN_SEGMENTATION_OPT_LEN)
from unyte_generator.utils.unyte_logger import unyte_logger
from unyte_generator.utils.unyte_message_gen import mock_message_generator


class UDP_notif_generator:

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
        self.random_order: bool = args.random_order == 1
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

    def generate_udp_notif_packets(self, msg_payload):
        payload_per_msg_len = self.mtu - UDPN_HEADER_LEN
        packet_amount = 1

        if (len(msg_payload) + UDPN_HEADER_LEN) > self.mtu:
            payload_per_msg_len = self.mtu - UDPN_HEADER_LEN - UDPN_SEGMENTATION_OPT_LEN
            packet_amount = len(msg_payload) // payload_per_msg_len
            if len(msg_payload) % payload_per_msg_len != 0:
                packet_amount += 1

        udp_notif_packets = []
        for packet_increment in range(packet_amount):
            if packet_amount == 1:
                packet = IP(src=self.source_ip, dst=self.destination_ip)/UDP()/UDPN()/PAYLOAD()
            else:
                packet = IP(src=self.source_ip, dst=self.destination_ip)/UDP()/UDPN()/SEGMENTATION_OPT()/PAYLOAD()
            packet.sport = self.source_port
            packet.dport = self.destination_port

            if packet_amount == 1:
                packet[UDPN].header_length = UDPN_HEADER_LEN
                packet[UDPN].message_length = packet[UDPN].header_length + len(packet[PAYLOAD].message)
                packet[PAYLOAD].message = msg_payload
            else:
                packet[UDPN].header_length = UDPN_HEADER_LEN + UDPN_SEGMENTATION_OPT_LEN
                packet[SEGMENTATION_OPT].segment_id = packet_increment
                if (len(msg_payload[payload_per_msg_len * packet_increment:]) > payload_per_msg_len):
                    packet[PAYLOAD].message = msg_payload[payload_per_msg_len * packet_increment:payload_per_msg_len * (packet_increment + 1)]
                    packet[UDPN].message_length = packet[UDPN].header_length + len(packet[PAYLOAD].message)
                else:
                    packet[PAYLOAD].message = msg_payload[payload_per_msg_len * packet_increment:]
                    packet[UDPN].message_length = packet[UDPN].header_length + len(packet[PAYLOAD].message)
                    packet[SEGMENTATION_OPT].last = 1
            udp_notif_packets.append(packet)
        return udp_notif_packets

    def forward_current_message(self, udp_notif_msgs: list, current_domain_id: int) -> int:
        current_message_lost_packets = 0
        if self.random_order:
            random.shuffle(udp_notif_msgs)

        msg_id = 0
        for packet in udp_notif_msgs:
            packet[UDPN].observation_domain_id = current_domain_id
            packet[UDPN].message_id = msg_id
            if (self.probability_of_loss == 0):
                send(packet, verbose=0)
            elif random.randint(1, int(1000 * (1 / self.probability_of_loss))) >= 1000:
                send(packet, verbose=0)
            else:
                current_message_lost_packets += 1
                if len(udp_notif_msgs) == 1:
                    logging.info("simulating packet number 0 from message_id " + str(packet[UDPN].message_id) + " lost")
                else:
                    logging.info("simulating packet number " + str(packet[SEGMENTATION_OPT].segment_id) +
                                 " from message_id " + str(packet[UDPN].message_id) + " lost")
            if len(udp_notif_msgs) == 1:
                self.logger.log_packet(packet, self.legacy)
            else:
                self.logger.log_segment(packet, packet[SEGMENTATION_OPT].segment_id)
            self.save_pcap('captured_udp_notif.pcap', packet)
            msg_id += 1
        return current_message_lost_packets

    def send_udp_notif(self):
        timer_start = time.time()

        self.logger.log_used_args(self)
        msg_payload = self.generate_mock_message()

        lost_packets = 0
        forwarded_packets = 0

        # Generate packet only once
        udp_notif_msgs = self.generate_udp_notif_packets(msg_payload)
        observation_domain_id = self.initial_domain

        for _ in range(self.message_amount):

            current_message_lost_packets: int = self.forward_current_message(udp_notif_msgs, observation_domain_id)
            forwarded_packets += len(udp_notif_msgs) - current_message_lost_packets
            lost_packets += current_message_lost_packets

            time.sleep(self.waiting_time)
            observation_domain_id += 1

            if observation_domain_id > (self.initial_domain + self.additional_domains):
                observation_domain_id = self.initial_domain

        timer_end = time.time()
        generation_total_duration = timer_end - timer_start
        logging.warn('Sent ' + str(forwarded_packets) + ' in ' + str(generation_total_duration))
        logging.info('Simulated %d lost packets from %d total packets', lost_packets, (forwarded_packets + lost_packets))
        return forwarded_packets
