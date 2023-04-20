# Scapy generator for UDP-notif

This repository implements a mock generator for YANG-push notifications using UDP-notif transport as defined in [draft-ietf-netconf-udp-notif-09](https://datatracker.ietf.org/doc/draft-ietf-netconf-udp-notif/09/). This mock generator supports IPv4.


### Supported IETF RFCs/drafts

The mock YANG-push notifications uses the following IETF RFCs and drafts. The supported variant is Configured Subscriptions defined in [RFC8641](https://datatracker.ietf.org/doc/rfc8641/).

- [RFC5277](https://datatracker.ietf.org/doc/rfc5277): Netconf Event Notifications
- [RFC8639](https://datatracker.ietf.org/doc/rfc8639): Subscription to YANG Notifications
- [RFC8641](https://datatracker.ietf.org/doc/rfc8641/): Subscription to YANG Notifications for Datastore Updates (Configured Subscriptions only)
- [draft-ietf-netconf-udp-notif-09](https://datatracker.ietf.org/doc/draft-ietf-netconf-udp-notif/09/): UDP-based Transport for Configured Subscriptions
- [draft-ietf-netconf-distributed-notif-06](https://datatracker.ietf.org/doc/draft-ietf-netconf-distributed-notif/06/): Subscription to Distributed Notifications
- [draft-ahuang-netconf-notif-yang-01](https://datatracker.ietf.org/doc/draft-ahuang-netconf-notif-yang/01/): YANG model for NETCONF Event Notifications
- [draft-tgraf-netconf-notif-sequencing-00](https://datatracker.ietf.org/doc/draft-tgraf-netconf-notif-sequencing/00/): Support of Hostname and Sequencing in YANG Notifications
- [draft-tgraf-yang-push-observation-time-00](https://datatracker.ietf.org/doc/draft-tgraf-yang-push-observation-time/00/): Support of Network Observation Timestamping in YANG Notifications
- [draft-tgraf-netconf-yang-notifications-versioning-03](https://datatracker.ietf.org/doc/draft-tgraf-netconf-yang-notifications-versioning/03/): Support of Versioning in YANG Notifications Subscription


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

- `--initial-domain <domain>` or `-i <domain>` : (Integer) initial observation domain id, `<domain>` >= 0, Default: `0`

- `--additional-domains <obs_nb>` or `-a <obs_nb>` : (Integer) amount of additional observation domains, `<obs_nb>` >= 0, Default: `0`

- `--message-amount <msgs>` or `-n <msgs>` : (Integer) amount of notification messages to send, `<msgs>` >= 1, Default: `1`

- `--encoding <encoding>` or `-e <encoding>`: (String) encoding of the UDP-notif payload. Options: [`json`, `xml`]. Default: `json`.

- `--mtu <value>` or `-m <value>` : (Integer) maximum transmission unit, 16 < `<value>` < 65535, Default: `1500`

- `--waiting-time <time>` or `-w <time>` : (Float) waiting time (in seconds) between two messages, `<time>` > 0, Default: `0`

- `--probability-of-loss <loss>` or `-p <loss>` : (Float) segment loss probability, 0 <= `<loss>` < 1, Default: `0`

- `--logging-level <level>` or `-l <level>` : (String) logging level, `<level>` = none or `<level>` = warning or `<level>` = info or `<level>` = debug, Default: `info`

- `--capture <path>` or `-c <path>` : (String) Save a wireshark capture of the forwarded packets in the `<path>`. Default: `None` (disabled).

- `--legacy` or `-leg` : Generate legacy headers as defined in [draft-ietf-netconf-udp-pub-channel-05](https://datatracker.ietf.org/doc/draft-ietf-netconf-udp-pub-channel/), /!\ No segmentation is possible. Default: Disabled.

- `--update-yang` or `-upd`: Simulate a YANG module update to a backward compatible YANG module. Default: Disabled.

## Examples

One YANG-push message [RFC8641](https://datatracker.ietf.org/doc/rfc8641) using UDP-notif as transport.
```shell
$ sudo python3 src/main.py 192.0.2.65 192.0.2.66 10001 10010
```

Continuous stream of YANG-push messages [RFC8641](https://datatracker.ietf.org/doc/rfc8641) using UDP-notif as transport.
```shell
$ sudo python3 src/main.py 192.0.2.66 192.0.2.66 10001 10010 -n 0
```

### Simulating a YANG subscription update

This generator can also simulate a YANG module update in YANG-push.

```shell
$ sudo python3 src/main.py 192.0.2.65 192.0.2.66 10001 10010 -upd
```

#### Used YANG modules

The YANG modules used in [yang/interfaces](./yangs/interfaces/).

The mock generator emulates a subscription to the Xpath `/if:interfaces` of [ietf-interfaces@2018-02-20.yang](./yangs/interfaces/ietf-interfaces%402018-02-20.yang)

```yang
module: ietf-interfaces
  +--rw interfaces
     +--rw interface* [name]
        +--rw name                        string
        +--rw description?                string
        +--rw type                        identityref
        +--rw enabled?                    boolean
        +--rw link-up-down-trap-enable?   enumeration {if-mib}?
        +--ro admin-status                enumeration {if-mib}?
        +--ro oper-status                 enumeration
        +--ro last-change?                yang:date-and-time
        +--ro if-index                    int32 {if-mib}?
        +--ro phys-address?               yang:phys-address
        +--ro higher-layer-if*            interface-ref
        +--ro lower-layer-if*             interface-ref
        +--ro speed?                      yang:gauge64
        +--ro statistics
           +--ro discontinuity-time    yang:date-and-time
           +--ro in-octets?            yang:counter64
           +--ro in-unicast-pkts?      yang:counter64
           +--ro in-broadcast-pkts?    yang:counter64
           +--ro in-multicast-pkts?    yang:counter64
           +--ro in-discards?          yang:counter32
           +--ro in-errors?            yang:counter32
           +--ro in-unknown-protos?    yang:counter32
           +--ro out-octets?           yang:counter64
           +--ro out-unicast-pkts?     yang:counter64
           +--ro out-broadcast-pkts?   yang:counter64
           +--ro out-multicast-pkts?   yang:counter64
           +--ro out-discards?         yang:counter32
           +--ro out-errors?           yang:counter32
```

After the update of the subscription, the generator emulates pushing a new versioned of the same YANG module with a new leaf `mtu`. This new YANG module is defined in [ietf-interfaces@2023-04-30.yang](./yangs/interfaces/ietf-interfaces%402023-04-30.yang). Note that this new YANG module is defined for test purposes and is not part of any IETF standard RFC.

```yang
module: ietf-interfaces
  +--rw interfaces
     +--rw interface* [name]
        +--rw name                        string
        +--rw description?                string
        +--rw mtu                         uint32
        +--rw type                        identityref
        +--rw enabled?                    boolean
        +--rw link-up-down-trap-enable?   enumeration {if-mib}?
        +--ro admin-status                enumeration {if-mib}?
        +--ro oper-status                 enumeration
        +--ro last-change?                yang:date-and-time
        +--ro if-index                    int32 {if-mib}?
        +--ro phys-address?               yang:phys-address
        +--ro higher-layer-if*            interface-ref
        +--ro lower-layer-if*             interface-ref
        +--ro speed?                      yang:gauge64
        +--ro statistics
           +--ro discontinuity-time    yang:date-and-time
           +--ro in-octets?            yang:counter64
           +--ro in-unicast-pkts?      yang:counter64
           +--ro in-broadcast-pkts?    yang:counter64
           +--ro in-multicast-pkts?    yang:counter64
           +--ro in-discards?          yang:counter32
           +--ro in-errors?            yang:counter32
           +--ro in-unknown-protos?    yang:counter32
           +--ro out-octets?           yang:counter64
           +--ro out-unicast-pkts?     yang:counter64
           +--ro out-broadcast-pkts?   yang:counter64
           +--ro out-multicast-pkts?   yang:counter64
           +--ro out-discards?         yang:counter32
           +--ro out-errors?           yang:counter32
```

## NETCONF configuration XML examples

As defined in [RFC8641](https://datatracker.ietf.org/doc/rfc8641), configured subscriptions are configured via Netconf RPC `<edit-config>`.

Examples of configuration files can be found in [configurations](./src/resources/xml/subscription/).

## Docker container
See [Docker docs](docker)
