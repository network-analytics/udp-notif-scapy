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
                                                 UDPN_SEGMENTATION_OPT_LEN, PCAP_FILENAME)
from unyte_generator.utils.unyte_logger import unyte_logger
from unyte_generator.utils.unyte_message_gen import Mock_payload_reader


class UDP_notif_generator:

    def __init__(self, args):
        self.source_ip = args.source_ip[0]
        self.destination_ip = args.destination_ip[0]
        self.source_port = int(args.source_port[0])
        self.destination_port = int(args.destination_port[0])
        self.initial_domain = args.initial_domain
        self.additional_domains = args.additional_domains
        self.message_amount = args.message_amount
        if self.message_amount == 0:
            self.message_amount = float('inf')
        self.mtu = args.mtu
        self.waiting_time = args.waiting_time
        self.probability_of_loss = args.probability_of_loss
        self.random_order: bool = args.random_order == 1
        self.logging_level = args.logging_level
        self.capture_file_path: str = args.capture

        self.mock_payload_reader = Mock_payload_reader()

        self.pid = os.getpid()
        self.logger = unyte_logger(self.logging_level, self.pid)
        logging.info("Unyte scapy generator started")

    def save_pcap(self, packet):
        if self.capture_file_path is not None:
            wrpcap(self.capture_file_path, packet, append=True)

    def generate_mock_payload(self, nb_payloads: int) -> list:
        return self.mock_payload_reader.get_json_push_update_notif(nb_payloads=nb_payloads)

    def generate_udp_notif_packets(self, yang_push_msgs: list) -> list:
        payload_per_msg_len = self.mtu - UDPN_HEADER_LEN

        udp_notif_packets: list = [] # list[list[msg]]
        for payload in yang_push_msgs:
            # check if segmentation is needed
            if (len(payload) + UDPN_HEADER_LEN) > self.mtu:
                payload_per_msg_len = self.mtu - UDPN_HEADER_LEN - UDPN_SEGMENTATION_OPT_LEN
                udp_notif_segmented_pckts = len(payload) // payload_per_msg_len
                if len(payload) % payload_per_msg_len != 0:
                    udp_notif_segmented_pckts += 1
            else:
                udp_notif_segmented_pckts = 1

            aggregated_msgs: list = []
            for packet_increment in range(udp_notif_segmented_pckts):
                if udp_notif_segmented_pckts == 1:
                    packet = IP(src=self.source_ip, dst=self.destination_ip)/UDP()/UDPN()/PAYLOAD()
                else:
                    packet = IP(src=self.source_ip, dst=self.destination_ip)/UDP()/UDPN()/SEGMENTATION_OPT()/PAYLOAD()

                packet.sport = self.source_port
                packet.dport = self.destination_port
                if udp_notif_segmented_pckts == 1:
                    packet[UDPN].header_length = UDPN_HEADER_LEN
                    packet[UDPN].message_length = packet[UDPN].header_length + len(packet[PAYLOAD].message)
                    packet[PAYLOAD].message = payload
                else:
                    packet[UDPN].header_length = UDPN_HEADER_LEN + UDPN_SEGMENTATION_OPT_LEN
                    packet[SEGMENTATION_OPT].segment_id = packet_increment
                    if (len(payload[payload_per_msg_len * packet_increment:]) > payload_per_msg_len):
                        packet[PAYLOAD].message = payload[payload_per_msg_len * packet_increment:payload_per_msg_len * (packet_increment + 1)]
                        packet[UDPN].message_length = packet[UDPN].header_length + len(packet[PAYLOAD].message)
                    else:
                        packet[PAYLOAD].message = payload[payload_per_msg_len * packet_increment:]
                        packet[UDPN].message_length = packet[UDPN].header_length + len(packet[PAYLOAD].message)
                        packet[SEGMENTATION_OPT].last = 1
                aggregated_msgs.append(packet)
            udp_notif_packets.append(aggregated_msgs)
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
                self.logger.log_packet(packet, False)
            else:
                self.logger.log_segment(packet, packet[SEGMENTATION_OPT].segment_id)
            self.save_pcap(packet)
            msg_id += 1
        return current_message_lost_packets

    def __send_infinite_stream_udp_notif(self):
        observation_domain_id = self.initial_domain
        while True:
            yang_push_payloads: list[str] = self.generate_mock_payload(nb_payloads=1)

            # Generate packet only once
            udp_notif_msgs: list[list] = self.generate_udp_notif_packets(yang_push_payloads)

            for udp_notif_msg in udp_notif_msgs:
                self.forward_current_message(udp_notif_msg, observation_domain_id)

                time.sleep(self.waiting_time)
                observation_domain_id += 1

                if observation_domain_id > (self.initial_domain + self.additional_domains):
                    observation_domain_id = self.initial_domain

    def __send_n_udp_notif(self, message_to_send: int):
        yang_push_payloads: list[str] = self.generate_mock_payload(nb_payloads=message_to_send)

        lost_packets = 0
        forwarded_packets = 0

        # Generate packet only once
        udp_notif_msgs: list[list] = self.generate_udp_notif_packets(yang_push_payloads)
        observation_domain_id = self.initial_domain

        for udp_notif_msg in udp_notif_msgs:
            current_message_lost_packets: int = self.forward_current_message(udp_notif_msg, observation_domain_id)
            forwarded_packets += len(udp_notif_msgs) - current_message_lost_packets
            lost_packets += current_message_lost_packets

            time.sleep(self.waiting_time)
            observation_domain_id += 1

            if observation_domain_id > (self.initial_domain + self.additional_domains):
                observation_domain_id = self.initial_domain
        logging.warn('Sent ' + str(forwarded_packets) + ' messages')
        logging.info('Simulated %d lost packets from %d total packets', lost_packets, (forwarded_packets + lost_packets))


    def send_udp_notif(self):
        timer_start = time.time()

        self.logger.log_used_args(self)
        print(self.message_amount)
        if self.message_amount == float('inf'):
            self.__send_infinite_stream_udp_notif()
        else:
            self.__send_n_udp_notif(message_to_send=self.message_amount)

        timer_end = time.time()
        execution_time = timer_end - timer_start
        logging.info('Execution time: %d seconds', execution_time)
