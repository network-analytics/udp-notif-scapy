
import argparse


class unyte_argparser():

    def __init__(self):

        # ARGPARSE
        self.parser = argparse.ArgumentParser(description='Process scapy call arguments.')

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
        self.parser.add_argument('--initial-domain', '-i', type=int,
                                 default=0, help='Identifier of the initial observation domain')
        self.parser.add_argument('--additional-domains', '-a', type=int,
                                 default=0, help='Amount of observation domains in addition to the first')
        # MESSAGE TYPE AND AMOUNT
        self.parser.add_argument('--message-type', '-t',
                                 default="ints", choices=["ints", "json", "rand"], help='The type of data sent')
        self.parser.add_argument('--message-amount', '-n', type=int,
                                 default=1, help='Amount of notification messages to send')
        # FORWARDING RULES
        self.parser.add_argument('--mtu', '-m', type=int,
                                 default=1500, help='Maximum Transmission Unit')
        self.parser.add_argument('--sleep-time', '-s', type=float,
                                 default=0, help='Sleep time between sending two notification messages')
        # RANDOMNESS
        self.parser.add_argument('--loss-probability', '-l', type=float,
                                 default=0, help='Probability of a packet loss during transmission')
        self.parser.add_argument('--random-order', '-r', type=int,
                                 default=0, help='Whether the segments must be sent in a random order or not')
        # DISPLAY
        self.parser.add_argument('--display', '-d',
                                 default="control", choices=["control", "headers", "everything"], help='Information display, from only control messages to payloads')

    def parse_args(self):
        return self.parser.parse_args()
