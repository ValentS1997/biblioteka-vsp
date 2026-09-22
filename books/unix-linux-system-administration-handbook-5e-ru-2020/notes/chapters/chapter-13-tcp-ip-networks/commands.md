# Команды главы 13

Только команды и формы команд, подтверждённые RAG главы 13.

| Команда | Назначение | Что проверить | Тип |
|---|---|---|---|
| `ip link show` | Показать Linux network interfaces и link state | interface names, state, MTU, MAC | read-only |
| `ip address show` | Показать адреса интерфейсов Linux | IPv4/IPv6 addresses, prefixes, scope | read-only |
| `ip route show` | Показать Linux routing table | destination prefixes, next hops, interfaces | read-only |
| `ip address add 192.168.1.13/26 broadcast 192.168.1.63 dev enp0s5` | Добавить IPv4 address к Linux interface | address/prefix/broadcast/interface correct | state-changing |
| `ip route add 132.236.220.64/26 via 132.236.212.6 dev eth1` | Добавить static route в Linux | route appears and next hop is directly reachable | state-changing |
| `ip route add default via 132.236.227.1 dev eth0` | Добавить default route | default path points to intended gateway | state-changing |
| `ip route delete <route>` | Удалить route в Linux | intended route removed, reachability preserved | state-changing |
| `ip route flush ...` | Очистить matching routes в Linux | only intended routes removed | state-changing / high-risk |
| `netstat -rn` | Показать routing table без DNS lookup | numeric destinations, masks, gateways, interfaces | read-only |
| `netstat -r` | Показать routing table | routes and gateways | read-only |
| `ipcalc 24.8.175.69/28` | Рассчитать network/netmask/broadcast/host range | prefix arithmetic matches intended subnet | read-only |
| `ip neigh show` | Показать Linux ARP/ND cache | neighbor IP↔MAC/link-state mappings | read-only |
| `hostname` | Inspect/set host network name depending invocation | current intended host name | read-only or state-changing |
| `ifdown <interface>` | Отключить Linux interface using distro config | interface goes down as intended | state-changing / access-risk |
| `ifup <interface>` | Включить Linux interface using distro config | configured address/routes restored | state-changing |
| `ifup -a` | Поднять interfaces marked for automatic startup | expected set becomes active | state-changing |
| `service network restart` | Перезапустить network configuration в shown Linux workflow | all intended interfaces/routes return | state-changing / high-risk |
| `ethtool eth0` | Показать link characteristics | speed, duplex, autonegotiation, link detected | read-only |
| `ethtool -s eth0 speed 100 duplex full` | Изменить speed/duplex | both ends are configured consistently | state-changing / link-risk |
| `ethtool -r <interface>` | Restart autonegotiation | link renegotiates and remains healthy | state-changing / transient-link-risk |
| `ethtool -k <interface>` | Показать protocol offload features | current offload state | read-only |
| `cat /proc/sys/net/ipv4/icmp_echo_ignore_broadcasts` | Прочитать Linux networking sysctl via procfs | current runtime value | read-only |
| `sysctl net.ipv4.icmp_echo_ignore_broadcasts=1` | Изменить runtime network security parameter | value changed and intended traffic unaffected | state-changing |
| `sudo sh -c "echo 1 > icmp_echo_ignore_broadcasts"` | Direct procfs-style write example from chapter context | value changed; runtime-only | state-changing |
| `ifconfig -a` | FreeBSD: показать interfaces/current settings | interface inventory, addresses, state | read-only |
| `ifconfig em0 192.168.1.13/26 up` | FreeBSD: назначить IPv4 address/prefix | address applied and interface usable | state-changing / access-risk |
| `ifconfig em0 media 1000baseT mediaopt full-duplex` | FreeBSD: задать media settings | peer is configured consistently; link stable | state-changing / link-risk |
| `route add -net 192.168.45.128/25 zulu-gw.atrust.net` | FreeBSD: добавить static route | route appears with intended gateway | state-changing |
| `route add default gw 132.236.227.1 eth0` | Добавить default route in chapter example form | default path is correct | state-changing |
| `route del ...` | Удалить FreeBSD route | intended entry removed | state-changing |
| `route flush` | Очистить FreeBSD routing table | console/recovery available before use | state-changing / high-risk |
| `service netif restart` | FreeBSD: повторить network-interface startup configuration | interfaces restore expected state | state-changing / high-risk |
| `service routing restart` | FreeBSD: reload routing after `defaultrouter` change | intended routes restored | state-changing / high-risk |
| `sysctl -ad` | FreeBSD: list tunables with descriptions | relevant network parameters found | read-only |
| `sudo sysctl net.inet.icmp.drop_redirect=1` | FreeBSD: ignore ICMP redirects | runtime parameter changed | state-changing |
| `sudo /etc/rc.d/sysctl reload` | Reload persistent FreeBSD sysctl settings | configured values applied | state-changing |
| `ping <host>` | Проверить IP-level reachability | loss/RTT, but not application health | workload-generating |
| `ping -s 1500 cuinfo.cornell.edu` | Probe with large packets to expose MTU/media issues | fragmentation/loss behavior | workload-generating |
| `traceroute <host>` | Показать sequence of routed hops | path and hop behavior | workload-generating |
| `traceroute -n <host>` | Trace without DNS lookups | numeric path when name resolution is suspect | workload-generating |
| `sudo tcpdump host bull` | Capture packets involving host `bull` | actual packet flow and protocol fields | read-only / packet-capture |
| `sudo tcpdump src net 192.168.1.0/24 and dst port 80` | Capture traffic matching source network and destination port | filter selects intended traffic | read-only / packet-capture |
| `iperf -s` | Запустить iPerf server | listener is available for controlled test | workload-generating / service-start |
| `iperf -c 10.211.55.11` | Generate network throughput test toward server | measured throughput/loss context | workload-generating / potentially heavy |
| `iptables -L -v` | Показать firewall chains/counters | rule order, counters, matches | read-only |
| `iptables -F <chain>` | Flush rules from a chain | console/recovery and replacement rules ready | state-changing / high-risk |
| `iptables -P <chain> <target>` | Set default chain policy | intended default action in effect | state-changing / high-risk |
| `iptables -A <chain> -i <iface> -j <target>` | Append firewall rule | rule order and target semantics correct | state-changing |
| `iptables -F` | Flush default filter chains in chapter example | only when complete replacement ruleset is ready | state-changing / high-risk |
| `iptables -P INPUT DROP` | Default-deny INPUT in chapter example | explicit required permits exist first | state-changing / lockout-risk |
| `iptables -P FORWARD DROP` | Default-deny FORWARD in chapter example | forwarding allow rules exist as required | state-changing |
| `iptables -A FORWARD -m state --state ESTABLISHED,RELATED -j ACCEPT` | Allow return traffic for tracked sessions | expected established flows work | state-changing |
| `iptables -t nat -A POSTROUTING -o eth0 -j SNAT --to 128.138.101.4` | SNAT example | correct inside/outside interfaces/address mapping | state-changing / routing-impact |
| `sudo modprobe iptable_nat` | Load Linux NAT module shown in chapter | module loads successfully | state-changing |
| `sudo modprobe ip_conntrack` | Load connection tracking module shown in chapter | state tracking available | state-changing |
| `sudo modprobe ip_conntrack_ftp` | Load FTP conntrack helper shown in chapter | helper loaded if needed | state-changing |
| `sudo ipf -Fa -f /etc/ipf/ipf.conf` | Flush IPFilter rules and load rules file | syntax valid and intended access preserved | state-changing / high-risk |
| `terraform apply` | Apply cloud-network IaC example | planned VPC/subnet/routes/resources created as intended | state-changing / billable |
| `terraform destroy -force` | Destroy Terraform-managed cloud resources in chapter-era syntax | intended resources only; dependencies/data considered | state-changing / destructive / billable-impact |
| `tugboat info <droplet>` | Show DigitalOcean droplet info in chapter-era tool | interfaces/addresses as expected | read-only / network |
| `tugboat ssh <droplet>` | Open SSH session via chapter-era DigitalOcean tool | reaches intended droplet | read-only session / network |
| `ip address show eth0` | Inspect cloud VM interface addresses | provider-visible/private/public addressing model | read-only |

## Read-only baseline

Перед любым сетевым изменением chapter logic поддерживает такой baseline:

~~~bash
ip link show
ip address show
ip route show
ip neigh show
netstat -rn
~~~

На FreeBSD:

~~~bash
ifconfig -a
netstat -rn
sysctl -ad
~~~

Для link-layer suspicion:

~~~bash
ethtool <interface>
~~~

Для subnet arithmetic:

~~~bash
ipcalc <address>/<prefix>
~~~

## Routing safety

Перед `ip route add/delete/flush`, `route del/flush`, `ifdown`, `service network restart`, `service netif restart` или удаленным `ifconfig`:

- зафиксировать current route table;
- знать management path и default route;
- иметь console/out-of-band recovery;
- менять один route/interface за раз;
- после изменения проверить reachability both directions.

`flush` в chapter присутствует как legitimate operation, но это high-risk action. Universal rollback отсутствует: `[Needs confirmation]`.

## Linux persistent configuration

Chapter показывает разные distro schemes:

Ubuntu-style:
- `/etc/hostname`;
- `/etc/network/interfaces`;
- `ifup` / `ifdown`.

Red Hat/CentOS-style:
- `/etc/sysconfig/network`;
- `/etc/sysconfig/network-scripts/ifcfg-<interface>`;
- route files under network-scripts.

Runtime `ip`, `ethtool` и `sysctl` changes не следует автоматически считать persistent.

## FreeBSD persistent configuration

Chapter uses:

- `/etc/rc.conf`;
- `hostname=`;
- `ifconfig_<iface>=`;
- `defaultrouter=`;
- `ifconfig_<iface>="DHCP"`;
- `/etc/dhclient.conf`;
- `/etc/sysctl.conf`.

## Diagnostics ladder

~~~text
link/interface
  ↓
address/prefix
  ↓
neighbor resolution
  ↓
routing table
  ↓
ping
  ↓
traceroute
  ↓
tcpdump/Wireshark
  ↓
application-specific check
~~~

Important: successful `ping` proves only IP-level response, not service health.

## Firewall safety

Firewall rules are ordered and stateful behavior changes semantics.

Before a modifying ruleset:

1. inspect current rules/counters;
2. preserve current ruleset outside the new script;
3. ensure management traffic has an explicit allow path;
4. avoid remote default-deny cutover without rollback;
5. apply rules atomically where possible;
6. test from an independent session;
7. verify counters/logs.

Exact restore command for the previous iptables/IPFilter state is environment-specific and not supplied by the chapter: `[Needs confirmation]`.

## Cloud/IaC safety

Chapter-era Terraform/AWS/DigitalOcean examples include historical commands and credential environment variables. Do not commit access keys or copy chapter credentials. Cloud-network changes may create billable resources and connectivity impact. External/current verification is intentionally excluded by `rag_only`.
