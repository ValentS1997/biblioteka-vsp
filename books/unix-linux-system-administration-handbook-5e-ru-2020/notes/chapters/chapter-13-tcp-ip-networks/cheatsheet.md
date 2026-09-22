# Шпаргалка: сети TCP/IP

Цель: диагностировать и изменять сеть послойно — от link/interface до application path — без смешивания адресации, маршрутизации и policy.

## 1. TCP/IP как стек

Глава показывает пятиуровневую operational model:

~~~text
Applications
  SSH / SMTP / HTTP / DNS / traceroute
        ↓
Transport
  TCP / UDP
        ↓
Network
  IP / ICMP
        ↓
Link
  ARP/ND + device drivers
        ↓
Physical
  copper / fiber / radio
~~~

Реальный TCP/IP stack chapter трактует как несколько взаимодействующих уровней, где верхний layer использует нижний.

## 2. Ключевые протоколы

- IP — packet delivery между network interfaces;
- ICMP — control/error/debug messages;
- ARP — IPv4 IP→MAC resolution;
- Neighbor Discovery — IPv6 neighbor/link-layer resolution;
- UDP — datagram delivery без reliable session semantics;
- TCP — reliable duplex stream with flow/error control.

## 3. Encapsulation

~~~text
application data
  ↓
TCP/UDP header
  ↓
IP header
  ↓
Ethernet/link header
  ↓
frame on medium
~~~

На receiving side headers снимаются в обратном порядке.

## 4. MTU

Link layer задает maximum transfer unit.

Для Ethernet chapter использует стандартный payload MTU 1500 bytes.

IPv4 может fragment packet на route.

IPv6 intermediate routers не fragment packets; sender должен адаптировать размер.

Tunnel headers могут увеличить packet size и вызвать fragmentation.

Диагностический вопрос:

~~~text
исходный packet
+ tunnel/encapsulation overhead
> path MTU ?
~~~

## 5. Addressing layers

Не смешивать:

~~~text
MAC address
  → local/link delivery

IP address
  → network interface in IP topology

hostname
  → human-readable mapping to address

TCP/UDP port
  → service/channel on IP endpoint
~~~

IP-address относится к interface, а не абстрактно ко всей machine.

## 6. Ports

TCP и UDP имеют отдельные port spaces.

Chapter показывает well-known services через `/etc/services`.

Примеры из source:

- SMTP 25;
- DNS 53;
- HTTP 80;
- Kerberos 88.

Firewall rule должен учитывать protocol + port, не только port number.

## 7. Address types

Chapter distinguishes:

- unicast;
- multicast;
- broadcast;
- anycast.

IPv6 заменяет traditional broadcast mechanisms multicast-oriented behavior.

## 8. IPv4 subnetting

Prefix/netmask делит address на:

~~~text
network bits | host bits
~~~

Example:

~~~text
/26
→ 26 network bits
→ 6 host bits
→ 64 total addresses
~~~

Для ordinary subnet chapter subtracts network+broadcast addresses from usable host count.

## 9. CIDR

CIDR notation:

~~~text
address/prefix-length
~~~

Example:

~~~text
128.138.243.64/26
~~~

Routing benefit: aggregation/supernetting.

All hosts in one subnet must use a consistent subnet interpretation.

## 10. Проверка subnet arithmetic

~~~bash
ipcalc 24.8.175.69/28
~~~

Use to verify:

- network;
- netmask;
- broadcast;
- host range;
- prefix assumptions.

Do not calculate production ranges only “на глаз”.

## 11. IPv6 operational model

Chapter describes IPv6 as separate address family with 16-byte addresses.

Operationally:

- configure IPv4 and IPv6 separately;
- do not assume one family mirrors the other automatically;
- Neighbor Discovery replaces ARP role;
- SLAAC can automate address configuration;
- DHCPv6 remains relevant for higher-level configuration;
- path-MTU handling differs from IPv4.

## 12. Routing

Kernel routing table maps:

~~~text
destination prefix
  → next hop / interface
~~~

Selection rule:

~~~text
longest / most specific matching prefix wins
~~~

If no specific route matches:

~~~text
default route
~~~

If there is no usable route:

~~~text
ICMP unreachable
~~~

## 13. Routing baseline

Linux:

~~~bash
ip route show
netstat -rn
~~~

FreeBSD:

~~~bash
netstat -rn
~~~

Numeric output is useful during troubleshooting because DNS failure does not hide routing state.

## 14. Static route examples

Linux:

~~~bash
ip route add 132.236.220.64/26   via 132.236.212.6 dev eth1
~~~

Default:

~~~bash
ip route add default   via 132.236.227.1 dev eth0
~~~

Before modifying:

- verify next hop is directly reachable;
- preserve current table;
- know management path;
- have rollback/console.

## 15. ARP / Neighbor Discovery

Same subnet:

~~~text
destination IP
  ↓
ARP/ND
  ↓
destination MAC
~~~

Remote subnet:

~~~text
destination IP
  ↓
routing table chooses next-hop router
  ↓
ARP/ND resolves next-hop MAC
~~~

Linux:

~~~bash
ip neigh show
~~~

Wrong neighbor entries can indicate duplicate IP or spoofing/cache poisoning.

## 16. DHCP

DHCP leases configuration from central server.

Chapter examples include:

- IP address;
- subnet mask;
- default gateway;
- DNS servers;
- Syslog server;
- NTP and other service addresses.

Lease must be renewed.

Relay allows broadcast-originated DHCP workflow to reach centralized servers across subnet boundaries.

## 17. DHCP + DNS

Dynamic addressing requires an explicit naming strategy.

Chapter presents two patterns:

~~~text
dynamic address → generic dynamic hostname
~~~

or

~~~text
DHCP server updates DNS dynamically
~~~

The second is more complex but preserves stable names.

## 18. Security-sensitive IP behavior

Chapter highlights:

- IP forwarding;
- ICMP redirects;
- source routing;
- directed broadcast;
- IP spoofing;
- built-in firewalls;
- VPN.

General rule:

~~~text
ordinary host should not act like a router unless intentionally configured
~~~

## 19. ICMP redirects

Redirect is routing advice from a router.

Chapter treats it as untrusted control input because it is not authenticated.

For security-sensitive hosts/routers, consider disabling acceptance according to platform policy.

## 20. Source routing / spoofing

IPv4 source routing can bypass normal next-hop decision and creates security problems.

Spoofed source addresses should be filtered at boundaries.

Chapter describes reverse-path validation/uRPF as a defense, with caveats for multihomed/asymmetric-routing systems.

## 21. VPN

VPN:

~~~text
untrusted Internet
  ↓ encrypted tunnel
private network semantics
~~~

Chapter discusses IPsec and TLS-based VPN approaches.

Important: understand whether solution provides a real routed IP interface or only application/proxy behavior.

## 22. Basic host network configuration

Chapter workflow:

~~~text
1. unique address + host name
2. configure interfaces at boot
3. default route / additional routes
4. DNS configuration
5. reboot/boot verification after persistent change
~~~

If DHCP supplies all required settings, much of this is automated.

## 23. Interface discovery

Linux:

~~~bash
ip link show
ip address show
~~~

FreeBSD:

~~~bash
ifconfig -a
~~~

Baseline should record:

- interface name;
- MAC;
- link state;
- MTU;
- IPv4/IPv6 addresses;
- prefix lengths.

## 24. Linux: iproute2 model

~~~text
ip link
  → interface/link state

ip address
  → protocol addresses

ip route
  → routing table
~~~

This separation is central to modern Linux workflow in the chapter.

## 25. Linux address change

Example:

~~~bash
ip address add 192.168.1.13/26   broadcast 192.168.1.63   dev enp0s5
~~~

This is runtime state.

Persistence depends on distro configuration.

## 26. Linux persistence

Ubuntu-style chapter model:

~~~text
/etc/hostname
/etc/network/interfaces
ifup / ifdown
~~~

Red Hat/CentOS-style:

~~~text
/etc/sysconfig/network
/etc/sysconfig/network-scripts/ifcfg-*
route files
~~~

Do not assume runtime `ip` changes survive reboot.

## 27. Ethernet link settings

Read:

~~~bash
ethtool eth0
~~~

Change example:

~~~bash
ethtool -s eth0 speed 100 duplex full
~~~

Critical rule:

~~~text
manual speed/duplex must agree on both ends
~~~

One-sided manual configuration can produce loss/performance problems.

## 28. Linux network sysctl

Network tunables live under:

~~~text
/proc/sys/net/ipv4
/proc/sys/net/ipv6
~~~

Read example:

~~~bash
cat /proc/sys/net/ipv4/icmp_echo_ignore_broadcasts
~~~

Change example:

~~~bash
sysctl net.ipv4.icmp_echo_ignore_broadcasts=1
~~~

Persistent settings go to:

~~~text
/etc/sysctl.conf
~~~

## 29. Remote-change hazard

Chapter explicitly warns that network administrators are often logged into the same network they are modifying.

Therefore before:

- `ifdown`;
- route replacement;
- interface address change;
- firewall default-deny;
- service restart;

have a console/out-of-band recovery point.

## 30. FreeBSD configuration

Runtime:

~~~bash
ifconfig -a
ifconfig em0 192.168.1.13/26 up
~~~

Media:

~~~bash
ifconfig em0 media 1000baseT mediaopt full-duplex
~~~

Persistent:

~~~text
/etc/rc.conf
hostname=
ifconfig_em0=
defaultrouter=
~~~

DHCP:

~~~text
ifconfig_em0="DHCP"
~~~

## 31. FreeBSD reload

Chapter workflow:

~~~bash
service netif restart
service routing restart
~~~

These are high-risk over remote management.

## 32. Troubleshooting ladder

~~~text
interface/link
   ↓
address/prefix
   ↓
neighbor ARP/ND
   ↓
routing table
   ↓
ping
   ↓
traceroute
   ↓
packet capture
   ↓
application-specific test
~~~

Do not jump directly to application troubleshooting if lower layers are not verified.

## 33. ping

~~~bash
ping <host>
~~~

Large-packet example:

~~~bash
ping -s 1500 cuinfo.cornell.edu
~~~

Use for:

- basic reachability;
- RTT/loss clues;
- MTU/media suspicion.

Limit:

~~~text
successful ping ≠ healthy application service
~~~

## 34. traceroute

~~~bash
traceroute <host>
traceroute -n <host>
~~~

Purpose:

~~~text
show sequence of routing hops
~~~

DNS-less `-n` helps when name resolution itself may be broken.

## 35. Packet capture

Examples:

~~~bash
sudo tcpdump host bull
~~~

~~~bash
sudo tcpdump   src net 192.168.1.0/24   and dst port 80
~~~

Capture answers:

- did packet leave?
- did reply arrive?
- which address/port/protocol?
- what was actually on the wire?

Wireshark provides GUI/dissectors around the same packet-analysis domain.

## 36. Monitoring vs troubleshooting

Point-in-time:

~~~text
ping / traceroute / tcpdump
~~~

Continuous/history:

~~~text
SmokePing / Cacti
~~~

Throughput test:

~~~bash
iperf -s
iperf -c 10.211.55.11
~~~

iPerf generates traffic and can affect a network under test.

## 37. Firewall model

iptables:

~~~text
table
  ↓
chain
  ↓
ordered rules
  ↓
target
~~~

Filter chains:

- INPUT;
- OUTPUT;
- FORWARD.

Common targets discussed:

- ACCEPT;
- DROP;
- REJECT;
- LOG.

Rule order changes outcome.

## 38. Default-deny example

Chapter starts a sample ruleset with:

~~~bash
iptables -F
iptables -P INPUT DROP
iptables -P FORWARD DROP
~~~

This is high-risk.

Before use:

- preserve existing rules;
- allow management path;
- use independent recovery session;
- verify after each stage.

## 39. Stateful firewalling

Example:

~~~bash
iptables -A FORWARD   -m state   --state ESTABLISHED,RELATED   -j ACCEPT
~~~

State tracking can simplify return-path permissions but adds complexity/resource use.

## 40. NAT

Chapter separates filtering from NAT.

Example form:

~~~bash
iptables -t nat -A POSTROUTING   -o eth0   -j SNAT   --to 128.138.101.4
~~~

NAT is not a substitute for a firewall ruleset.

## 41. IPFilter

IPFilter stores policy in rules files rather than long command sequences.

Rules are evaluated in order; chapter notes last matching rule wins unless `quick` stops evaluation.

Load example:

~~~bash
sudo ipf -Fa -f /etc/ipf/ipf.conf
~~~

This flushes existing rules first: high-risk.

## 42. AWS VPC

Chapter VPC primitives:

- private CIDR range;
- subnets;
- route tables;
- Internet gateway;
- NAT gateway;
- security groups;
- NACL;
- VPC peering/VPN.

Public/private nature is determined by route/gateway design, not only by address.

## 43. Security groups vs NACL

Security groups:

- instance/interface-oriented;
- stateful;
- default-deny inbound model in chapter;
- least privilege emphasized.

NACL:

- subnet boundary;
- stateless;
- separate policy layer.

## 44. Terraform for network state

Chapter recommendation logic:

~~~text
repeatable/project infrastructure
→ Terraform
~~~

Quick inspection/one-off action:

~~~text
CLI
~~~

Terraform configuration is intended for version control.

## 45. GCP network model

Chapter describes GCP private networks as global.

Subnets are regional.

External address may be implemented through provider translation rather than appearing directly as the same address on guest interface.

Firewall policy remains a separate control plane.

## 46. DigitalOcean model in chapter

Chapter-era DigitalOcean network example exposes:

- public IPv4;
- private IPv4;
- IPv6.

Private regional network described there is not equivalent to isolated AWS/GCP VPC semantics; chapter therefore stresses firewall/encryption requirements.

## 47. End-to-end network workflow

~~~text
Need connectivity
   ↓
inspect interface/link
   ↓
verify IP/prefix
   ↓
verify neighbor resolution
   ↓
verify route/default route
   ↓
verify firewall/policy
   ↓
ping/traceroute
   ↓
packet capture
   ↓
application-specific test
~~~

For changes:

~~~text
baseline
  ↓
one controlled change
  ↓
verify lower layer
  ↓
verify end-to-end
  ↓
persist only after success
  ↓
reboot/reload verification
~~~

## Acceptance criteria

- interface/link state is known;
- address and prefix are intentional;
- IPv4/IPv6 are checked independently where both are used;
- neighbor mapping is sane;
- default/specific routes are understood;
- DHCP/DNS relationship is known;
- runtime and persistent state are not confused;
- remote-changing actions have recovery path;
- firewall rules preserve management access;
- ping is not used as proof of application health;
- packet capture can confirm actual flow;
- monitoring is separated from generated-load testing;
- cloud network is represented as code when repeatability is required;
- rollback for route/firewall destructive actions is documented or marked `[Needs confirmation]`.
