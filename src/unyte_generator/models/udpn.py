from scapy.all import Packet, BitField
from .unyte_global import UDPN_HEADER_LEN


class UDPN(Packet):
    name = "UDPN"
    fields_desc = [
        BitField(name="version", default=1, size=3),
        BitField(name="space", default=0, size=1),
        BitField(name="media_type", default=1, size=4), # 1 = application/yang-data+json
        BitField(name="header_length", default=UDPN_HEADER_LEN, size=8),
        BitField(name="message_length", default=UDPN_HEADER_LEN, size=16),
        BitField(name="observation_domain_id", default=0, size=32),
        BitField(name="message_id", default=0, size=32)
    ]
