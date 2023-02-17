import logging
import random
import time

from scapy.all import send
from scapy.layers.inet import IP, UDP

from unyte_generator.models.opt import SEGMENTATION_OPT
from unyte_generator.models.payload import PAYLOAD
from unyte_generator.models.udpn import UDPN
from unyte_generator.models.unyte_global import (UDPN_HEADER_LEN,
                                                 UDPN_SEGMENTATION_OPT_LEN)
from unyte_generator.unyte_generator import UDP_notif_generator

class UDP_notif_generator_draft_08(UDP_notif_generator):

    def __init__(self, args):
        super().__init__(args=args)

    def __generate_udp_notif_packets(self, yang_push_msgs: list) -> list:
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

    def __forward_current_message(self, udp_notif_msgs: list, current_domain_id: int) -> int:
        current_message_lost_packets = 0
        # if self.random_order: # FIXME: random reorder
        #     random.shuffle(udp_notif_msgs)
        
        if current_domain_id not in self.msg_id:
            self.msg_id[current_domain_id] = 0

        msg_id = self.msg_id[current_domain_id]
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
        self.msg_id[current_domain_id] = msg_id

        return current_message_lost_packets

    def _stream_infinite_udp_notif(self):
        observation_domain_id = self.initial_domain
        while True:
            yang_push_payloads: list[str] = self.generate_mock_payload(nb_payloads=1)

            # Generate packet only once
            udp_notif_msgs: list[list] = self.__generate_udp_notif_packets(yang_push_payloads)

            for udp_notif_msg in udp_notif_msgs:
                self.__forward_current_message(udp_notif_msg, observation_domain_id)

                time.sleep(self.waiting_time)
                observation_domain_id += 1

                if observation_domain_id > (self.initial_domain + self.additional_domains):
                    observation_domain_id = self.initial_domain

    def _send_n_udp_notif(self, message_to_send: int):
        yang_push_payloads: list[str] = self.generate_mock_payload(nb_payloads=message_to_send)

        lost_packets = 0
        forwarded_packets = 0

        # Generate packet only once
        udp_notif_msgs: list[list] = self.__generate_udp_notif_packets(yang_push_payloads)
        observation_domain_id = self.initial_domain
        # if self.random_order:
        #     random.shuffle(udp_notif_msgs)

        for udp_notif_msg_group in udp_notif_msgs:
            current_message_lost_packets: int = self.__forward_current_message(udp_notif_msg_group, observation_domain_id)
            forwarded_packets += len(udp_notif_msg_group) - current_message_lost_packets
            lost_packets += current_message_lost_packets

            time.sleep(self.waiting_time)
            observation_domain_id += 1

            if observation_domain_id > (self.initial_domain + self.additional_domains):
                observation_domain_id = self.initial_domain
        logging.info('Sent ' + str(forwarded_packets) + ' messages')
        logging.info('Simulated %d lost packets from %d total packets', lost_packets, (forwarded_packets + lost_packets))

