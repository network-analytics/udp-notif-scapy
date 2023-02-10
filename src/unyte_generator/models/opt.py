from scapy.all import Packet, BitField
from .unyte_global import UDPN_SEGMENTATION_OPT_LEN


class SEGMENTATION_OPT(Packet):
    name = "SEGMENTATION_OPT"
    fields_desc = [
        BitField(name="type", default=1, size=8),
        BitField(name="option_length", default=UDPN_SEGMENTATION_OPT_LEN, size=8),
        BitField(name="segment_id", default=0, size=15),
        BitField(name="last", default=0, size=1)
    ]
