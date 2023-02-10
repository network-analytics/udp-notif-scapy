import logging
import os
import random
import time

from scapy.all import send, wrpcap
from scapy.layers.inet import IP, UDP

from unyte_generator.models.payload import PAYLOAD
from unyte_generator.models.udpn_legacy import UDPN_legacy
from unyte_generator.models.unyte_global import UDPN_LEGACY_HEADER_LEN, PCAP_FILENAME
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

    def generate_packet_list(self, yang_push_msgs: list):
        packet_list = []
        for yang_push_payload in yang_push_msgs:
            packet = IP(src=self.source_ip, dst=self.destination_ip)/UDP()/UDPN_legacy()/PAYLOAD()
            packet.sport = self.source_port
            packet.dport = self.destination_port
            packet[PAYLOAD].message = yang_push_payload
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
            self.save_pcap(PCAP_FILENAME, packet)

        return current_message_lost_packets

    def __stream_infinite_udp_notif(self):
        obs_domain_id = self.initial_domain
        while True:
            yang_push_msgs: list = self.generate_mock_payload(nb_payloads=1)

            # Generate packet only once
            packets_list: list = self.generate_packet_list(yang_push_msgs)
            for packet in packets_list:
                self.forward_current_message(packet, obs_domain_id)
                time.sleep(self.waiting_time)

                obs_domain_id += 1
                if obs_domain_id > (self.initial_domain + self.additional_domains):
                    obs_domain_id = self.initial_domain


    def __send_n_udp_notif(self, message_to_send: int):
        yang_push_msgs: list = self.generate_mock_payload(nb_payloads=message_to_send)

        lost_packets = 0
        forwarded_packets = 0

        # Generate packet only once
        packets_list: list = self.generate_packet_list(yang_push_msgs)
        obs_domain_id = self.initial_domain
        for packet in packets_list:
            current_message_lost_packets = self.forward_current_message(packet, obs_domain_id)
            forwarded_packets += len(packet) - current_message_lost_packets
            lost_packets += current_message_lost_packets
            time.sleep(self.waiting_time)

            obs_domain_id += 1
            if obs_domain_id > (self.initial_domain + self.additional_domains):
                obs_domain_id = self.initial_domain
        logging.warn('Sent ' + str(forwarded_packets) + ' packets')
        logging.info('Simulated %d lost packets from %d total packets', lost_packets, (forwarded_packets + lost_packets))

    def send_udp_notif(self):
        timer_start = time.time()
        self.logger.log_used_args(self)

        if self.message_amount == float('inf'):
            self.__stream_infinite_udp_notif()
        else:
            self.__send_n_udp_notif(message_to_send=self.message_amount)

        timer_end = time.time()
        execution_time = timer_end - timer_start
        logging.info('Execution time: %d seconds', execution_time)
