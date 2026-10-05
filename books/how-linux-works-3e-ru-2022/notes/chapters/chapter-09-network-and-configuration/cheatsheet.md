# Шпаргалка: сеть и ее конфигурация по главе 9

## Symptom / problem framing

Типовые симптомы:

- interface существует, но не имеет ожидаемого IP;
- IP назначен, но remote network недоступна;
- local subnet работает, internet — нет;
- hostname не разрешается, хотя IP reachable;
- service не принимает connection;
- DHCP не выдаёт/не применяет configuration;
- router не пересылает packets;
- NAT/firewall меняет или блокирует traffic;
- neighbor cache устарел;
- Wi-Fi interface видит сеть, но не подключается.

Начинать не с «починки сети вообще», а с определения слоя, на котором исчезает ожидаемое поведение.

## Baseline / context

Source-derived network stack:

```text
application/name-resolution context
        ↓
transport: TCP / UDP
        ↓
network: IPv4 / IPv6 + routing
        ↓
link/physical: Ethernet / Wi-Fi + MAC
        ↓
network interface / hardware
```

Operational localization:

```text
link/interface
  ↓
address + prefix
  ↓
routing table / default gateway
  ↓
neighbor resolution
  ↓
DNS/name resolution
  ↓
TCP/UDP endpoint
  ↓
application
```

IPv4 and IPv6 may operate simultaneously as dual stack.

## Read-only checks

### Interface and addresses

```bash
ip address show
ip -6 address show
```

Check:
- interface state;
- MAC address;
- IPv4/IPv6 addresses;
- prefix length;
- link-local IPv6 address.

### Routes

```bash
ip route show
ip -6 route show
route -n
```

Check:
- directly connected networks;
- more specific routes;
- default route;
- next-hop gateway.

### ICMP and DNS

```bash
ping <ip-or-host>
host <name-or-ip>
resolvectl status
```

Interpretation:
- successful ping confirms an ICMP path, not application health;
- failed ping does not prove a service is unavailable;
- `host` checks name/address resolution;
- `resolvectl status` exposes systemd-resolved state when applicable.

### Network manager state

```bash
nmcli
nm-online
```

`nmcli` without arguments gives a connection/interface summary.  
`nm-online` returns success when NetworkManager considers the network online.

### Transport endpoints

```bash
netstat -nt
netstat -ntl
```

Use `-n` to avoid DNS lookup while inspecting raw endpoint addresses/ports.

### Neighbor cache

```bash
ip -4 neigh
```

Check IP → MAC mappings and state such as `REACHABLE` or `STALE`.

### Router/firewall state

```bash
sysctl net.ipv4.ip_forward
iptables -L
```

These establish current forwarding and filter policy before any modification.

### Wi-Fi

```bash
iw dev <interface> scan
iw dev <interface> link
```

Scan requires the interface to be up, but IP configuration is not required merely to inspect physical-layer wireless networks.

## Interpretation

### Address + subnet

An IP address without its prefix/subnet is incomplete for routing decisions.

CIDR prefix length describes how many leading bits identify the network.

### Routing

The kernel chooses a matching route based on network/prefix specificity.

Default route:
- IPv4: `0.0.0.0/0`;
- IPv6: `::/0`.

A default gateway must be reachable through a directly connected network.

### IPv6

IPv6 uses 128-bit addresses.

Link-local addresses use the local link and are part of normal IPv6 operation. IPv4 and IPv6 stacks are independent enough to coexist.

### DNS/name resolution

Resolution may involve:
1. `/etc/nsswitch.conf`;
2. `/etc/hosts`;
3. DNS resolver configuration;
4. local caching/resolver services such as `systemd-resolved`.

Do not assume `/etc/resolv.conf` is a static standalone file; source notes it may be a generated symlink.

### TCP / UDP

TCP:
- connection-oriented;
- uses local/remote address + port;
- server listens on a port;
- client normally uses an ephemeral local port.

UDP:
- datagram-oriented;
- has ports but no TCP-style connections;
- does not provide TCP-style recovery for loss/reordering.

### DHCP

DHCP automates address/configuration assignment.

Source warns that a subnet should not have multiple competing DHCP servers.

### Router / NAT

IP forwarding is separate from merely having multiple interfaces.

Private IPv4 networks need additional translation for common internet-sharing scenarios; source uses NAT/masquerading through `iptables`.

### Firewall

`iptables` chains are evaluated top-to-bottom. First matching rule wins.

A restrictive default policy is useful only when required traffic is explicitly permitted.

### ARP / NDP

ARP: IPv4 neighbor IP → MAC mapping on local subnet.  
NDP: IPv6 neighbor discovery on local link.

For remote destinations, the local host resolves the MAC of the next-hop router, not the final remote host.

### Wi-Fi

`iw` handles low-level wireless state.

Source explicitly advises against WEP and old insecure WPA; WPA2/WPA3 are handled through `wpa_supplicant`/higher-level managers.

## Next action

Use the first failed layer:

1. Interface absent/down → inspect physical/interface layer.
2. Interface up, no address → inspect address manager/DHCP/manual config.
3. Address present, local subnet fails → inspect prefix and neighbor state.
4. Local subnet works, remote fails → inspect routes/default gateway.
5. IP works, name fails → inspect `nsswitch`, hosts/resolver/DNS.
6. Host reachable, service fails → inspect TCP/UDP listener/port.
7. Router path fails → inspect forwarding, NAT and firewall.
8. Wi-Fi scan works but no association → inspect wireless authentication/configuration.

## Modifying action

Source-confirmed modifying actions include:

```bash
ip address add <address>/<prefix> dev <interface>
ip route add default via <gateway> dev <interface>
ip route del default
ip route add <subnet>/<prefix> via <router>
ip route del <subnet>/<prefix>
dhclient <interface>
sysctl -w net.ipv4.ip_forward=1
ip neigh del <host> dev <interface>
iw <interface> connect <network_name>
ifconfig <interface> up
```

Firewall/NAT examples also use `iptables -P`, `-A`, `-I`, `-D` and NAT/MASQUERADE rules.

Before any modifying action:
- preserve current address/route/firewall baseline;
- ensure current administrative access has a recovery path;
- avoid applying restrictive firewall changes sequentially over a remote-only session.

## Verification / acceptance checks

| Change | Verification |
|---|---|
| interface address | `ip address show` |
| IPv6 address | `ip -6 address show` |
| route/default gateway | `ip route show` or `ip -6 route show` |
| DHCP | address + route state after client run |
| IP forwarding | `sysctl net.ipv4.ip_forward` |
| firewall rule/policy | `iptables -L` + intended connectivity |
| neighbor-cache delete | `ip -4 neigh` |
| Wi-Fi association | `iw dev <interface> link` |
| DNS/resolver change | `host <name>` and resolver state |
| NetworkManager state | `nmcli` / `nm-online` |

Acceptance means not only that configuration exists, but that the expected layer now works without breaking required lower/parallel paths.

## Rollback

- `ip route add default ...` → source provides `ip route del default`.
- `ip route add <subnet> ...` → source provides `ip route del <subnet>`.
- `ip address add ...` → inverse command is not supplied in the verified chapter source: `[Needs confirmation]`.
- `dhclient <interface>` → `[Needs confirmation]`.
- `sysctl -w net.ipv4.ip_forward=1` → `[Needs confirmation]` unless previous value was captured and a source-supported restoration procedure is available.
- Firewall/NAT policy/rules → restore only from a captured known-good ruleset; generic rollback procedure: `[Needs confirmation]`.
- `ip neigh del ...` → explicit inverse is not supplied; cache may repopulate through normal neighbor discovery, but rollback procedure remains `[Needs confirmation]`.
- Wi-Fi connect/interface-up changes → `[Needs confirmation]`.
- Persistent NetworkManager/resolver/sysctl configuration → `[Needs confirmation]` without a verified host-specific backup/recovery path.
