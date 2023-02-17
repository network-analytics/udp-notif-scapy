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

    def _stream_infinite_udp_notif(self):
        raise ValueError("Abstract method: must be implemented")

    def _send_n_udp_notif(self, message_to_send: int):
        raise ValueError("Abstract method: must be implemented")

    def send_udp_notif(self):
        timer_start = time.time()
        self.logger.log_used_args(self)

        if self.message_amount == float('inf'):
            self._stream_infinite_udp_notif()
        else:
            self._send_n_udp_notif(message_to_send=self.message_amount)

        timer_end = time.time()
        execution_time = timer_end - timer_start
        logging.info('Execution time: %d seconds', execution_time)
