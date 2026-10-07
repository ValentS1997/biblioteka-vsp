# Cheatsheet — глава 9 «Сеть и ее конфигурация»

**Источник:** `how-linux-works-brian-ward-3e-ru-2022:p0270:c01`–`p0319:c01`, PDF/печатные страницы 270–319. Только `rag_only`.

## Symptom / problem framing

Глава помогает локализовать сетевую проблему по уровню:

1. физический/link: интерфейс, MAC, Ethernet/Wi-Fi;
2. network: IP, subnet/CIDR, route, gateway;
3. name resolution: NSS, hosts, resolver, DNS;
4. transport: TCP/UDP ports and listeners;
5. policy/router: forwarding, NAT, firewall.

Перед изменением состояния сначала определить, **какой компонент владеет конфигурацией**: live kernel state, NetworkManager, Netplan, systemd-networkd или distro-specific files.

## Baseline / context

| Область | Модель главы | PDF |
|---|---|---:|
| Stack | application → transport → network → physical | 272–273 |
| IPv4 | Address + subnet/CIDR; route table selects next hop | 273–279 |
| IPv6 | Global + link-local addresses; `::/0` default route | 279–281 |
| Ethernet | MAC-addressed frames carry IP packets | 283–285 |
| Interface | Kernel network interface connects physical/network layers | 284–286 |
| Manager | NetworkManager/systemd-networkd/Netplan may own persistent config | 287–292 |
| Resolver | NSS + hosts + resolver/DNS + optional caching | 292–296 |
| Transport | TCP/UDP ports, client/server/listener state | 296–301 |
| Autoconfig | DHCP for IPv4; RA/stateless methods for IPv6 | 302–304 |
| Router | Forwarding + routes + optional NAT/firewall | 304–314 |
| Neighbor | ARP for IPv4; NDP for IPv6 | 315–316 |
| Wi-Fi | SSID/auth/encryption on physical layer | 317–319 |

## Read-only checks

```sh
ip address show
ip route show
ip -6 address show
ip -6 route show
ping host
host name
ethtool interface
nmcli
nm-online
resolvectl status
nslookup -debug host
netstat -nt
netstat -ntl
ip -4 neigh
sysctl net.ipv4.ip_forward
iw dev interface scan
iw dev interface link
```

Additional read-only/config inspection:
- `/etc/hosts`, `/etc/resolv.conf`, `/etc/nsswitch.conf`;
- `/etc/NetworkManager`, `/etc/NetworkManager/system-connections`;
- `/etc/netplan`, `/etc/systemd/network`;
- `/etc/services`;
- firewall listing: `iptables -L`.

Caveats:
- `ping` failure does **not** prove host/application failure because ICMP echo may be blocked.
- `host -4/-6` selects transport used for DNS lookup, not necessarily address family of returned records.
- `nm-online` is a binary connectivity state check, not a complete path diagnosis.
- `netstat` is the source tool here; chapter notes `-n` avoids DNS lookups.
- `iw scan` can generate a large scan and requires an enabled wireless interface.

## Interpretation

| Observation | Interpretation from chapter | Still unchecked |
|---|---|---|
| Interface has `inet A/B` | IPv4 address + CIDR prefix assigned | Correct gateway/DNS still unknown |
| `default via X` | X is default gateway for unmatched destinations | Whether X is reachable |
| Route with longer prefix exists | Kernel prefers longest matching destination prefix | Policy/rule routing not covered here |
| IPv6 `scope link` | Link-local address | Global reachability still separate |
| `ping` replies | ICMP echo path works round-trip | TCP/UDP/application still unchecked |
| `host name` returns address | DNS lookup succeeded | Application protocol still unchecked |
| `nmcli` shows active connection | NetworkManager has current connection state | Effective persistent owner/file [Needs confirmation] |
| `resolvectl status` shows DNS server | systemd-resolved has resolver configuration | Whether upstream server answers |
| `netstat -ntl` shows LISTEN | Local process listens on TCP port | Firewall/path/remote reachability |
| Neighbor entry is STALE | Cached MAC mapping is old and may need refresh | Not automatically a fault |
| `ip_forward=1` | IPv4 forwarding enabled | NAT/firewall correctness still separate |
| Firewall policy DROP | Unmatched packet is discarded | Rule order/allow paths must be reviewed |

## Next action

1. Verify interface state and addresses.
2. Verify route selection and default gateway.
3. Test direct IP reachability before DNS.
4. Test DNS/NSS chain separately.
5. Confirm listener/port state for transport issues.
6. Identify which network manager owns persistence before editing files.
7. For router/firewall work, confirm console/recovery access before any restrictive rule/policy change.
8. Unknown owner, target interface, remote-access rollback or expected route → **[Needs confirmation]**.

## Modifying action

| Source-supported action | Effect | Risk |
|---|---|---|
| Add address to interface | Changes live IP configuration | Can create conflict or break remote session |
| Add/delete routes | Changes live path selection | Wrong default route can cut connectivity |
| `dhclient interface` | Obtains IPv4 config lease | Can replace current live network state |
| Edit Netplan/NM/networkd config | Changes persistent configuration ownership/state | Manager conflicts / next-boot outage |
| Enable IPv4 forwarding | Turns host into packet forwarder | Broadens routing behavior/security boundary |
| NAT/masquerade rules | Rewrites/forwards traffic | Can expose or break downstream network |
| Firewall policy/rules | Accept/drop traffic | **High risk:** remote lockout possible |
| Delete neighbor-cache entry | Forces neighbor re-resolution | Brief interruption; wrong interface/host possible |
| `iw ... connect` | Associates Wi-Fi interface | Changes link state; insecure/open network risk |
| wpa_supplicant config | Changes wireless authentication/security | Wrong credentials/policy can disconnect host |

## Verification / acceptance checks

| Change | Verification from chapter | Acceptance |
|---|---|---|
| Address | `ip address show` | Intended address/prefix on correct interface |
| Route | `ip route show` / `ip -6 route show` | Intended destination/gateway selected |
| DHCP | address/route/DNS readback | Lease produced expected network state |
| NetworkManager | `nmcli`, `nm-online` | Intended connection active, network reported online |
| DNS | `host`, resolver status | Intended name resolves through expected resolver path |
| Listener | `netstat -ntl` | Expected local address/port is LISTEN |
| Forwarding | `sysctl net.ipv4.ip_forward` | Expected kernel forwarding state |
| Firewall | `iptables -L` plus known-good remote/local connectivity | Required traffic still works; undesired traffic blocked |
| Neighbor | `ip -4 neigh` | Correct mapping/state reappears |
| Wi-Fi | `iw dev interface link` | Associated to intended AP/network |

## Rollback

- Live address/route changes: capture original `ip address show` and route tables before modification; exact inverse depends on what changed → **[Needs confirmation]**.
- NetworkManager/Netplan/networkd: preserve original files and identify the active manager before change; generic restore command is not provided in chapter.
- DHCP: previous static/dynamic state must be known before test; source does not define a generic restore sequence.
- Forwarding/NAT/firewall: save current state/rules and maintain alternate access. If remote access is the only path, restrictive firewall changes should **not** be applied without recovery access.
- Neighbor-cache deletion normally repopulates automatically when traffic resumes; manual restoration is not required by source.
- Wi-Fi: previous association/security config must be captured; rollback is manager/config dependent **[Needs confirmation]**.

## Guardrails

- Do not diagnose from DNS before proving basic IP path when the symptom allows direct-IP testing.
- Do not edit `/etc/resolv.conf` blindly when systemd-resolved or another manager generates it.
- Do not mix manual `ip` changes with persistent-manager changes without understanding ownership.
- Firewall chain order matters: first match wins.
- Default-deny is a security strategy, but sequencing the rules incorrectly can isolate the machine.
