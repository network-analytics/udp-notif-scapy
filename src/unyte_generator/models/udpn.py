from scapy.all import Packet, BitField
from .unyte_global import UDPN_header_length, OPT_header_length


class UDPN(Packet):
    name = "UDPN"
    fields_desc = [BitField("version", 0, 3),
                   BitField("space", 0, 1),
                   BitField("encoding_type", 1, 4),
                   BitField("header_length", UDPN_header_length, 8),
                   BitField("message_length", UDPN_header_length, 16),
                   BitField("observation_domain_id", 0, 32),
                   BitField("message_id", 0, 32)]
