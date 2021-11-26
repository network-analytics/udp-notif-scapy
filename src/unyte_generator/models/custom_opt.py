from scapy.all import Packet, BitField
from .unyte_global import OPT_header_length


class CUSTOM_OPT(Packet):
    name = "CUSTOM_OPT"
    fields_desc = [BitField("type", 1, 8),
                   BitField("option_length", OPT_header_length, 8),
                   BitField("value", 0, 16), ]
