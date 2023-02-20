import logging
import random
import time

from scapy.all import send
from scapy.layers.inet import IP, UDP

from unyte_generator.models.payload import PAYLOAD
from unyte_generator.models.udpn_legacy import UDPN_legacy
from unyte_generator.models.unyte_global import UDPN_LEGACY_HEADER_LEN
from unyte_generator.unyte_generator import UDP_notif_generator


class UDP_notif_generator_legacy(UDP_notif_generator):

    def __init__(self, args):
        super().__init__(args=args)

    def __generate_packet_list(self, yang_push_msgs: list):
        packet_list: list = []
        for yang_push_payload in yang_push_msgs:
            if (len(yang_push_payload) + UDPN_LEGACY_HEADER_LEN) > self.mtu:
                logging.warning("MTU not used, no segmentation supported in legacy protocol")
            packet = IP(src=self.source_ip, dst=self.destination_ip)/UDP()/UDPN_legacy()/PAYLOAD()
            packet.sport = self.source_port
            packet.dport = self.destination_port
            packet[PAYLOAD].message = yang_push_payload
            packet[UDPN_legacy].message_length = UDPN_LEGACY_HEADER_LEN + len(packet[PAYLOAD].message)
            packet_list.append(packet)
        return packet_list

    def __forward_current_message(self, packet_list, current_domain_id):
        current_message_lost_packets = 0
        # if self.random_order == 1:
        #     random.shuffle(packet_list)

        if current_domain_id not in self.msg_id:
            self.msg_id[current_domain_id] = 0

        msg_id = self.msg_id[current_domain_id]
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
            self.save_pcap(packet)
        self.msg_id[current_domain_id] = msg_id

        return current_message_lost_packets

    def _stream_infinite_udp_notif(self):
        obs_domain_id = self.initial_domain

        # Send subscription-started notification first
        subs_started: str = self.mock_payload_reader.get_json_subscription_started_notif()
        udp_notif_msgs: list[list] = self.__generate_packet_list([subs_started])
        for udp_notif_msg in udp_notif_msgs:
            self.__forward_current_message(udp_notif_msg, obs_domain_id)

        while True:
            yang_push_msgs: list = self.mock_payload_reader.get_json_push_update_notif(nb_payloads=1)

            # Generate packet only once
            packets_list: list = self.__generate_packet_list(yang_push_msgs)
            for packet in packets_list:
                self.__forward_current_message(packet, obs_domain_id)
                time.sleep(self.waiting_time)

                obs_domain_id += 1
                if obs_domain_id > (self.initial_domain + self.additional_domains):
                    obs_domain_id = self.initial_domain


    def _send_n_udp_notif(self, message_to_send: int):
        payloads: list[str] = self._get_n_json_payloads(push_update_msgs=message_to_send)

        lost_packets = 0
        forwarded_packets = 0

        # Generate packet only once
        packets_list: list = self.__generate_packet_list(payloads)
        obs_domain_id = self.initial_domain
        for packet_group in packets_list:
            current_message_lost_packets = self.__forward_current_message(packet_group, obs_domain_id)
            forwarded_packets += 1 - current_message_lost_packets
            lost_packets += current_message_lost_packets
            time.sleep(self.waiting_time)

            obs_domain_id += 1
            if obs_domain_id > (self.initial_domain + self.additional_domains):
                obs_domain_id = self.initial_domain
        logging.warn('Sent ' + str(forwarded_packets) + ' packets')
        logging.info('Simulated %d lost packets from %d total packets', lost_packets, (forwarded_packets + lost_packets))
