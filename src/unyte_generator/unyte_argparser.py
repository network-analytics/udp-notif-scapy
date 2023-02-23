
import argparse

class Unyte_argparser():

    def __init__(self):

        # ARGPARSE
        self.parser = argparse.ArgumentParser(description='Mock generator for YANG-push using UDP-Notif as transport.')

        # SOURCE AND DESTINATION DATA
        self.parser.add_argument('source_ip', metavar='source-ip', nargs=1,
                                 help='w.x.y.z source IPv4 address.')
        self.parser.add_argument('destination_ip', metavar='destination-ip', nargs=1,
                                 help='w.x.y.z dest IPv4 address.')
        self.parser.add_argument('source_port', metavar='source-port', nargs=1, type=int,
                                 help='1000 < source_port < 10 000')
        self.parser.add_argument('destination_port', metavar='destination-port', nargs=1, type=int,
                                 help='1000 < destination_port < 10 000 and destination_port != source_port')
        # DOMAIN START VALUE AND AMOUNT
        self.parser.add_argument('--initial-domain', '-i', type=int, default=0,
                                 help='Identifier of the initial observation domain')
        self.parser.add_argument('--additional-domains', '-a', type=int, default=0,
                                 help='Amount of observation domains in addition to the first')
        self.parser.add_argument('--message-amount', '-n', type=int, default=1,
                                 help="Amount of 'push-update' notification to send")
        # FORWARDING RULES
        self.parser.add_argument('--mtu', '-m', type=int, default=1500,
                                 help='Maximum Transmission Unit')
        self.parser.add_argument('--waiting-time', '-w', type=float, default=0,
                                 help='Sleep time between sending two notification messages in seconds')
        # LOSS
        self.parser.add_argument('--probability-of-loss', '-p', type=float, default=0,
                                 help='Probability of a packet loss during transmission')
        # self.parser.add_argument('--random-order', '-r', action='store_true',
        #                          help='Simulating random order of the messages')
        # UTILITY
        self.parser.add_argument('--logging-level', '-l', default="info", choices=["none", "warning", "info", "debug"],
                                 help='Logging mode, warning by default, set to none for no logs, info for headers, debug for payloads')
        self.parser.add_argument('--encoding', '-e', default="json", choices=["json", "xml"],
                                 help='Encoding of the UDP-notif payload')
        self.parser.add_argument('--capture', '-c', type=str,
                                 help='Capture the mocked generated packets to a pcap file.')
        self.parser.add_argument('--legacy', '-leg', action='store_true',
                                 help='Generate legacy headers as defined in draft-ietf-netconf-udp-pub-channel-05.')
        self.parser.add_argument('--update-yang', '-upd', action='store_true',
                                help='Simulate a YANG module update to a backward compatible YANG module.')

    def parse_args(self):
        return self.parser.parse_args()
