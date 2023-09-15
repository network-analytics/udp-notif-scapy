#!/usr/bin/python
from unyte_generator.unyte_argparser import Unyte_argparser
from unyte_generator.unyte_generator import UDP_notif_generator
from unyte_generator.unyte_generator_legacy_proto import UDP_notif_generator_legacy
from unyte_generator.unyte_generator_draft_11 import UDP_notif_generator_draft_11


if __name__ == "__main__":
    parser = Unyte_argparser()
    args = parser.parse_args()

    mock_generator: UDP_notif_generator = None

    # use old udp-notif headers: draft-ietf-netconf-udp-pub-channel-05
    if args.legacy:
        mock_generator = UDP_notif_generator_legacy(args=args)
    else: # draft-ietf-netconf-udp-notif-11
        mock_generator = UDP_notif_generator_draft_11(args=args)

    mock_generator.send_udp_notif()
