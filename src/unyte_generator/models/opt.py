from scapy.all import Packet, BitField
from .unyte_global import OPT_header_length


class OPT(Packet):
    name = "OPT"
    fields_desc = [BitField("type", 1, 8),
                   BitField("option_length", OPT_header_length, 8),
                   BitField("segment_id", 0, 15),
                   BitField("last", 0, 1), ]
