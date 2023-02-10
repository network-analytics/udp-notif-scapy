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

- `--initial-domain x` or `-i x` : (INT) initial observation domain id, x >= 0, Default: `0`

- `--additional-domains x` or `-a x` : (INT) amount of additional observation domains, x >= 0, Default: `0`

- `--message-size s` or `-s s` : (STR) size of payload data, s = small or s = big, Default: `small`

- `--message-amount x` or `-n x` : (INT) amount of messages to send, x >= 1, Default: `1`

- `--mtu x` or `-m x` : (INT) maximum transmission unit, 16 < x < 65535, Default: `1500`

- `--waiting-time f` or `-w f` : (FLOAT) waiting time (in seconds) between two messages, x > 0, Default: `0`

- `--probability-of-loss f` or `-p f` : (FLOAT) segment loss probability, 0 <= x < 1, Default: `0`

- `--random-order x` or `-r x` : (INT) forward segments in random order, x = 0 or x = 1, Default: `0`

- `--logging-level s` or `-l s` : (STR) logging level, s = none or s = warning or s = info or s = debug, Default: `warning`

- `--capture x` or `-c x` : (INT) Set to 1 if you need a wireshark capture of the forwarded packets, x = 1 or x = 0, Default: `0`

- `--legacy x` or `-e x` : (INT) Set to 1 if you generate legacy headers: [draft-ietf-netconf-udp-pub-channel-05](https://datatracker.ietf.org/doc/draft-ietf-netconf-udp-pub-channel/), /!\ No segmentation is possible. x = 1 or x = 0, Default: `0`

## Examples

1 segment of size 12 + 716 (header + payload) with a json payload, from observation domain 0, with no loss probability, logging control messages only
```shell
$ sudo python3 src/main.py 192.0.2.66 192.0.2.66 3456 3457
```

Continuous stream of messages like the previous one
```shell
$ sudo python3 src/main.py 192.0.2.66 192.0.2.66 3456 3457 -n 0
```

2 messages of 5 shuffled segments of size 1500 with a json payload, from observation domains 10 and 11, with 0.1 loss probability and 0.1 second wait time between messages, logging control messages and segment headers
```shell
$ sudo python3 src/main.py 192.0.2.66 192.0.2.66 3456 3457 -n 2 -r 1 -s big -i 10 -a 1 -p 0.1 -w 0.1 -l info
```

## Docker container
See [Docker docs](docker)

## Launch multiple simulations
- `./launch_multiple.sh <number_messages>` : launches multiple instances of the generator simuling multiple source ips and ports
