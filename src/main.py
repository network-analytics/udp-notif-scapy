#!/usr/bin/python
from unyte_generator.unyte_argparser import unyte_argparser
from unyte_generator.unyte_generator import udp_notif_generator
from unyte_generator.unyte_generator_legacy_proto import udp_notif_generator_legacy


if __name__ == "__main__":
    parser = unyte_argparser()
    args = parser.parse_args()

    # use old udp-notif headers
    if args.legacy == 1:
        generator_legacy = udp_notif_generator_legacy(args)
        generator_legacy.send_udp_notif()
    else: # draft-ietf-netconf-udp-notif-04
        generator = udp_notif_generator(args)
        generator.send_udp_notif()
