import logging 
from unyte_generator.models.udpn import UDPN
from unyte_generator.models.udpn_legacy import UDPN_legacy
from unyte_generator.models.opt import SEGMENTATION_OPT
from unyte_generator.models.payload import PAYLOAD

class Unyte_logger:

    def __init__(self, logging_level, pid):
        self.set_logger_level(logging_level, pid)

    def set_logger_level(self, logging_level, pid):
        if logging_level == 'debug':
            logging.basicConfig(format='[%(levelname)s] (' + str(pid) + '): %(message)s', level=logging.DEBUG)
        elif logging_level == 'info':
            logging.basicConfig(format='[%(levelname)s] (' + str(pid) + '): %(message)s', level=logging.INFO)
        elif logging_level == 'warning':
            logging.basicConfig(format='[%(levelname)s] (' + str(pid) + '): %(message)s', level=logging.WARNING)
        elif logging_level == 'none':
            logging.disable(level=logging.DEBUG)

    def log_used_args(self, args):
        attrs = vars(args)
        logging.info('Used args: ' + ', '.join("%s: %s" % item for item in attrs.items()))

    def log_header_udpn_legacy(self, packet):
        logging.info("packet version = " + str(packet[UDPN_legacy].version))
        logging.info("packet encoding type = " + str(packet[UDPN_legacy].media_type))
        logging.info("packet message length = " + str(packet[UDPN_legacy].message_length))
        logging.info("packet observation domain id = " + str(packet[UDPN_legacy].observation_domain_id))
        logging.info("packet message id = " + str(packet[UDPN_legacy].message_id))

    def log_header_udpn(self, packet):
        logging.info("packet version = " + str(packet[UDPN].version))
        logging.info("packet space = " + str(packet[UDPN].space))
        logging.info("packet encoding type = " + str(packet[UDPN].media_type))
        logging.info("packet header length = " + str(packet[UDPN].header_length))
        logging.info("packet message length = " + str(packet[UDPN].message_length))
        logging.info("packet observation domain id = " + str(packet[UDPN].observation_domain_id))
        logging.info("packet message id = " + str(packet[UDPN].message_id))

    def log_header_opt(self, packet):
        logging.info("packet type = " + str(packet[SEGMENTATION_OPT].type))
        logging.info("packet option length = " + str(packet[SEGMENTATION_OPT].option_length))
        logging.info("packet segment id = " + str(packet[SEGMENTATION_OPT].segment_id))
        logging.info("packet last = " + str(packet[SEGMENTATION_OPT].last))

    def log_packet(self, packet, legacy: bool):
        logging.info("---------------- packet ----------------")
        if legacy:
            self.log_header_udpn_legacy(packet)
        else:
            self.log_header_udpn(packet)
        logging.debug("packet message = " + str(packet[PAYLOAD].message.decode()))
        logging.info("-------------- end packet --------------")

    def log_segment(self, packet, packet_increment):
        logging.info("---------- packet (segment " + str(packet_increment) + ") ----------")
        self.log_header_udpn(packet)
        self.log_header_opt(packet)
        logging.debug("packet message = " + str(packet[PAYLOAD].message.decode()))
        logging.info("-------- end packet (segment " + str(packet_increment) + ") --------")
