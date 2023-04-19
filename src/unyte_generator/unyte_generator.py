import logging
import os
import time

from datetime import datetime, timedelta
from scapy.all import wrpcap

from unyte_generator.utils.unyte_logger import Unyte_logger
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
        # self.random_order: bool = args.random_order == 1
        self.logging_level = args.logging_level
        self.capture_file_path: str = args.capture
        self.encoding: str = args.encoding
        self.update_yang_module: bool = args.update_yang
        if self.update_yang_module and self.message_amount == float('inf'):
            raise Exception("YANG updates are only supported for a finite value of messages. Please set a message_amount different from 0.")

        self.mock_payload_reader: Mock_payload_reader = Mock_payload_reader()

        self.pid = os.getpid()
        self.logger = Unyte_logger(self.logging_level, self.pid)
        self.msg_id: dict = {}
        logging.info("Unyte scapy generator started")

    def save_pcap(self, packet):
        if self.capture_file_path is not None:
            wrpcap(self.capture_file_path, packet, append=True)

    def _get_n_json_payloads(self, push_update_msgs: int) -> list:
        time_reference: datetime = datetime.now()
        seq_nb = 0
        if self.update_yang_module:
            time_reference = time_reference - timedelta(minutes=(2*push_update_msgs))
        else:
            time_reference = time_reference - timedelta(minutes=(push_update_msgs))

        obs_domain_ids = [obs_id for obs_id in range(self.initial_domain, self.initial_domain + self.additional_domains + 1, 1)]
        payloads: list[str] = []
        payloads += [self.mock_payload_reader.get_json_subscription_started_notif(msg_timestamp=time_reference, sequence_number=seq_nb, observation_domain_ids=obs_domain_ids)]
        seq_nb += 1
        for i in range(push_update_msgs):
            time_reference = time_reference + timedelta(minutes=1)
            payloads += [self.mock_payload_reader.get_json_push_update_1_notif(msg_timestamp=time_reference, sequence_number=seq_nb+i)]
        seq_nb += push_update_msgs

        if self.update_yang_module:
            time_reference = time_reference + timedelta(minutes=1)
            payloads += [self.mock_payload_reader.get_json_subscription_modified_notif(msg_timestamp=time_reference, sequence_number=seq_nb, observation_domain_ids=obs_domain_ids)]
            seq_nb += 1
            for i in range(push_update_msgs):
                time_reference = time_reference + timedelta(minutes=1)
                payloads += [self.mock_payload_reader.get_json_push_update_2_notif(msg_timestamp=time_reference, sequence_number=seq_nb+i)]
            seq_nb += push_update_msgs

        time_reference = time_reference + timedelta(minutes=1)
        payloads += [self.mock_payload_reader.get_json_subscription_terminated_notif(msg_timestamp=time_reference, sequence_number=seq_nb)]
        return payloads

    def _get_n_xml_payloads(self, push_update_msgs: int) -> list:
        time_reference: datetime = datetime.now()
        seq_nb = 0
        if self.update_yang_module:
            time_reference = time_reference - timedelta(minutes=(2*push_update_msgs))
        else:
            time_reference = time_reference - timedelta(minutes=(push_update_msgs))

        obs_domain_ids = [obs_id for obs_id in range(self.initial_domain, self.initial_domain + self.additional_domains + 1, 1)]
        payloads: list[str] = []
        payloads += [self.mock_payload_reader.get_xml_subscription_started_notif(msg_timestamp=time_reference, sequence_number=seq_nb, observation_domain_ids=obs_domain_ids)]

        seq_nb += 1
        for i in range(push_update_msgs):
            time_reference = time_reference + timedelta(minutes=1)
            payloads += [self.mock_payload_reader.get_xml_push_update_1_notif(msg_timestamp=time_reference, sequence_number=i+1)]
        seq_nb += push_update_msgs

        if self.update_yang_module:
            time_reference = time_reference + timedelta(minutes=1)
            payloads += [self.mock_payload_reader.get_xml_subscription_modified_notif(msg_timestamp=time_reference, sequence_number=seq_nb, observation_domain_ids=obs_domain_ids)]
            seq_nb += 1

            for i in range(push_update_msgs):
                time_reference = time_reference + timedelta(minutes=1)
                payloads += [self.mock_payload_reader.get_xml_push_update_2_notif(msg_timestamp=time_reference, sequence_number=seq_nb+i)]
            seq_nb += push_update_msgs
        time_reference = time_reference + timedelta(minutes=1)
        payloads += [self.mock_payload_reader.get_xml_subscription_terminated_notif(msg_timestamp=time_reference, sequence_number=seq_nb)]
        return payloads

    def _stream_infinite_udp_notif(self, encoding: str):
        raise ValueError("Abstract method: must be implemented")

    def _send_n_udp_notif(self, message_to_send: int, encoding: str):
        raise ValueError("Abstract method: must be implemented")

    def send_udp_notif(self):
        timer_start = time.time()
        self.logger.log_used_args(self)

        if self.message_amount == float('inf'):
            self._stream_infinite_udp_notif(encoding=self.encoding)
        else:
            self._send_n_udp_notif(message_to_send=self.message_amount, encoding=self.encoding)

        timer_end = time.time()
        execution_time = timer_end - timer_start
        logging.info('Execution time: %d seconds', execution_time)
