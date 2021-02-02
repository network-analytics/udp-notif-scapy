from scapy.all import Packet, StrField

class PAYLOAD(Packet):
    name = "PAYLOAD"
    fields_desc = [StrField("message", "idle")]
