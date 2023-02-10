from scapy.all import Packet, BitField
from .unyte_global import UDPN_LEGACY_HEADER_LEN


class UDPN_legacy(Packet):
    name = "UDPN"
    fields_desc = [
        BitField(name="version", default=0, size=4),
        BitField(name="flag", default=0, size=8),
        BitField(name="media_type", default=2, size=4),  # 2 = JSON for legacy
        BitField(name="message_length", default=UDPN_LEGACY_HEADER_LEN, size=16),
        BitField(name="observation_domain_id", default=0, size=32),
        BitField(name="message_id", default=0, size=32)
    ]
