# Команды и интерфейсы — глава 9 «Сеть и ее конфигурация»

**Provenance:** `p0270:c01`–`p0319:c01`, PDF/печатные страницы 270–319. Только явно поддержанные chapter RAG команды/интерфейсы.

Классы: **RO** — read-only observation; **WG** — workload-generating / interactive; **SC** — state-changing.

## 1. Addresses, routes and basic diagnostics

| Команда | Класс | Назначение | PDF |
|---|---|---|---:|
| `ip address show` | RO | IPv4/IPv6 addresses grouped by interface | 275,284–285 |
| `ip -6 address show` | RO | IPv6 addresses only | 280 |
| `ip route show` | RO | IPv4 routing table | 278 |
| `ip -6 route show` | RO | IPv6 routing table | 280–281 |
| `route -n` | RO legacy | Traditional route view without DNS lookup | 278 |
| `ping 10.23.2.1` | WG/RO | ICMP echo path test | 282 |
| `ping -4` / `ping -6` | WG/RO | Force IPv4/IPv6 for ping | 282 |
| `host www.example.com` | RO/WG DNS query | Resolve hostname | 283 |
| `host IP_address` | RO/WG DNS query | Attempt reverse lookup | 283 |
| `host -4` / `host -6` | RO/WG | Select protocol used to contact DNS server | 283 |
| `ethtool interface` | RO or SC depending options | Inspect/change Ethernet hardware settings; chapter only names tool | 285 |

## 2. Manual interface/route configuration — state changing

Source syntax:

```sh
ip address add address/subnet dev interface
ip route add default via gw-address dev interface
ip route del default
ip route add 192.168.45.0/24 via 10.23.2.44
ip route del 192.168.45.0/24
```

These commands modify **live kernel network state**. The source explicitly says manual configuration is rarely necessary and better suited to an experimental system (§9.11).

**Verification:** `ip address show`, `ip route show`, then layer-appropriate reachability.

**Rollback:** exact previous address/routes must be captured before change; generic rollback is **[Needs confirmation]**.

## 3. Persistent network managers/config

Source-confirmed components/paths:

- Netplan YAML: `/etc/netplan`.
- NetworkManager: `/etc/NetworkManager/NetworkManager.conf`, `/etc/NetworkManager/system-connections`, dispatcher directory `/etc/NetworkManager/dispatcher.d`.
- systemd-networkd: `/etc/systemd/network`.
- Legacy/distribution examples: `/etc/network/interfaces`, `/etc/sysconfig/network-scripts/ifcfg-*`.
- NetworkManager settings shown: `plugins=ifupdown,keyfile`, `managed=false`, `NM_CONTROLLED=yes/no`, `unmanaged-devices=mac:...`.

Commands:

| Команда | Класс | Назначение |
|---|---|---|
| `nmcli` | RO by no-argument use | Current NetworkManager interfaces/connections summary |
| `nm-online` | RO status | Exit code 0 if NetworkManager considers network online |
| `ifup eth0` / `ifdown` | SC legacy | Distro-specific boot/network configuration; implementations differ |

The chapter does not give a concrete Netplan apply command, so none is invented.

## 4. DNS/name resolution

| Команда/path | Класс | Назначение |
|---|---|---|
| `/etc/hosts` | config | Local manual hostname mappings |
| `/etc/resolv.conf` | config/generated path | Traditional nameserver/search configuration; may be generated symlink |
| `nslookup -debug host` | RO/WG | Source suggests inspecting nameserver behavior/caching addresses |
| `resolvectl status` | RO | Current systemd-resolved settings per interface |
| `systemd-resolve` | RO legacy name | Older name for `resolvectl` in source |
| `/etc/systemd/resolved.conf` | SC config | systemd-resolved configuration |
| `/etc/nsswitch.conf` | SC config | Name-service lookup ordering |
| `hosts: files dns` | config syntax | Check local hosts before DNS |

Do not edit `/etc/resolv.conf` until ownership is known.

## 5. TCP/UDP and listeners

| Команда/path | Класс | Назначение |
|---|---|---|
| `netstat -nt` | RO | Current TCP connections, no name resolution |
| `netstat -ntl` | RO | Listening TCP ports |
| `netstat ... -6` | RO | IPv6-only view |
| `/etc/services` | RO/config reference | Well-known service names ↔ port/protocol |

The source interprets local/foreign address+port pairs to infer client/server role. Listener `0.0.0.0:port` means all IPv4 interfaces; a loopback address limits the listener to local host.

## 6. DHCP and IPv6 autoconfiguration

| Command/action | Класс | Effect |
|---|---|---|
| `dhclient enp0s31f6` | SC/WG | Request DHCP configuration on source example interface |
| systemd-networkd DHCP | SC config | Built-in client configured through networkd files; no standalone manual client command |
| RA/SLAAC | automatic runtime | IPv6 link-local + router-advertisement based configuration |

Source says before manually testing `dhclient`, remove any existing gateway route; this is a disruptive prerequisite and is **not** generalized into a production runbook.

## 7. Routing / forwarding / NAT

| Command | Класс | Effect | Boundary |
|---|---|---|---|
| `sysctl net.ipv4.ip_forward` | RO | Read IPv4 forwarding state | [Not applicable] |
| `sysctl -w net.ipv4.ip_forward=1` | SC | Enable IPv4 packet forwarding | Changes host/router behavior |
| `/etc/sysctl.conf`, `/etc/sysctl.d` | SC config | Persist sysctl setting | Distro ownership [Needs confirmation] |

The chapter gives a NAT/masquerade example built from forwarding plus firewall rules. It explicitly says readers will usually not need to enter such commands manually.

## 8. Firewall / packet filter

Read-only:

```sh
iptables -L
```

Source state-changing examples include:
- set default chain policy;
- append source-address drop/accept rules;
- filter TCP by destination port;
- delete a rule by chain position;
- insert a rule at the top/selected position;
- allow ICMP, loopback/local traffic, established non-SYN TCP traffic, DNS replies and SSH in a default-deny example;
- NAT POSTROUTING masquerade and FORWARD rules.

**Critical source warning:** setting a default DROP policy before installing the allow rules can instantly cut off a remote-only session. These examples are therefore catalogued conceptually, not promoted as a copy-paste production firewall.

The source also names nftables/`nft`, `iptables-translate`, bpfilter and Shorewall, but provides no detailed command workflow for them.

## 9. Neighbor discovery

| Команда | Класс | Назначение |
|---|---|---|
| `ip -4 neigh` | RO | IPv4 ARP/neighbor cache |
| `ip neigh del host dev interface` | SC | Delete one neighbor-cache entry |
| `ip-neighbour(8)` | documentation | Manual neighbor-cache details |

The chapter explains ARP for IPv4 and NDP for IPv6. Exact NDP command syntax beyond the shared `ip neigh` family is not added.

## 10. Wi-Fi

| Команда/config | Класс | Назначение |
|---|---|---|
| `iw dev wlp1s0 scan` | WG/RO | Scan visible wireless networks |
| `iw dev wlp1s0 link` | RO | Current Wi-Fi association |
| `iw wlp1s0 connect network_name` | SC | Connect to unprotected network example |
| `ifconfig wlp1s0 up` | SC legacy | Source says interface may need to be enabled before scan |
| `/etc/wpa_supplicant.conf` | SC config | Default wpa_supplicant configuration path |

The source says WEP is insecure and should not be used; it presents WPA2/WPA3 as supported by `wpa_supplicant`.

## Command discipline

- Source addresses, PIDs, ports, interface names, gateways and SSIDs are examples, not live-host facts.
- Read-only diagnosis should precede live/persistent configuration changes.
- Remote network/firewall changes require a verified recovery path.
- No external syntax is added where chapter RAG only names a tool.
