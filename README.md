# Scapy generator for UDP-notif

This repository implements a mock generator for UDP-notif messages as defined in [draft-ietf-netconf-udp-notif-08](https://datatracker.ietf.org/doc/html/draft-ietf-netconf-udp-notif-08). This mock generator supports IPv4.

## Dependencies (Tested in Python 3.6.8)
Required libraries are specified in `src/requirements.txt`
```shell
$ pip install -r src/requirements.txt
```

## Usage

4 required arguments: 
```shell
$ sudo python3 src/main.py <src_ipv4> <dst_ipv4> <port_src> <port_dst>
```

- `<src_ipv4>`: valid source IPv4 address
- `<dst_ipv4>`: valid destination IPv4 address
- `<port_src>`: source port to be used
- `<port_dst>`: destination port to be used

### Optional arguments

- `--initial-domain x` or `-i x` : (Integer) initial observation domain id, x >= 0, Default: `0`

- `--additional-domains x` or `-a x` : (Integer) amount of additional observation domains, x >= 0, Default: `0`

- `--message-amount x` or `-n x` : (Integer) amount of messages to send, x >= 1, Default: `1`

- `--encoding <encoding>` or `-e <encoding>`: (String) encoding of the UDP-notif payload. Options: [`json`, `xml`]. Default: `json`.

- `--mtu x` or `-m x` : (Integer) maximum transmission unit, 16 < x < 65535, Default: `1500`

- `--waiting-time f` or `-w f` : (Float) waiting time (in seconds) between two messages, x > 0, Default: `0`

- `--probability-of-loss f` or `-p f` : (Float) segment loss probability, 0 <= x < 1, Default: `0`

- `--logging-level s` or `-l s` : (String) logging level, s = none or s = warning or s = info or s = debug, Default: `info`

- `--capture <path>` or `-c <path>` : (String) Save a wireshark capture of the forwarded packets in the `<path>`. Default: `None` (disabled).

- `--legacy` or `-leg` : Generate legacy headers as defined in [draft-ietf-netconf-udp-pub-channel-05](https://datatracker.ietf.org/doc/draft-ietf-netconf-udp-pub-channel/), /!\ No segmentation is possible. Default: Disabled.

- `--update-yang` or `-upd`: Simulate a YANG module update to a backward compatible YANG module. Default: Disabled.

## Examples

One YANG-push message [RFC8641](https://www.rfc-editor.org/rfc/rfc8641) using UDP-notif as transport.
```shell
$ sudo python3 src/main.py 192.0.2.65 192.0.2.66 10001 10010
```

Continuous stream of YANG-push messages [RFC8641](https://www.rfc-editor.org/rfc/rfc8641) using UDP-notif as transport.
```shell
$ sudo python3 src/main.py 192.0.2.66 192.0.2.66 10001 10010 -n 0
```

### Simulating a YANG subscription update

This generator can also simulate a YANG module update in YANG-push.

```shell
$ TBD
```

## NETCONF configuration XML examples

As defined in [RFC8641](https://www.rfc-editor.org/rfc/rfc8641), configured subscriptions are configured via Netconf RPC `<edit-config>`.

Examples of configuration files can be found in [configurations](./src/resources/xml/subscription/).

## Docker container
See [Docker docs](docker)

## Launch multiple simulations
- `./launch_multiple.sh <number_messages>` : launches multiple instances of the generator simuling multiple source ips and ports
