from scapy.all import Packet, BitField
from .unyte_global import UDPN_legacy_header_length

class UDPN_legacy(Packet):
    name = "UDPN"
    fields_desc = [BitField("version", 0, 4),
                   BitField("flag", 0, 8),
                   BitField("encoding_type", 2, 4), # 2 = JSON for legacy
                   BitField("message_length", UDPN_legacy_header_length, 16),
                   BitField("observation_domain_id", 0, 32),
                   BitField("message_id", 0, 32)]
