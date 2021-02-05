#!/usr/bin/python
from unyte_generator.unyte_argparser import unyte_argparser
from unyte_generator.unyte_generator import udp_notif_generator


if __name__ == "__main__":
    parser = unyte_argparser()
    args = parser.parse_args()

    generator = udp_notif_generator(args)

    generator.send_udp_notif()
    
