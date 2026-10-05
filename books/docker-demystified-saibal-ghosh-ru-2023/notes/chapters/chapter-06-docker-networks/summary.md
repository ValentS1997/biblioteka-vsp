# Итог главы 6

## Заключение

Глава 6 рассматривает Docker networking от single-host bridge до multi-host overlay.

Default Docker installation создаёт Bridge, Host и None networks. Default bridge основан на Linux bridge `docker0`. Container получает отдельный network namespace, IP от Docker IPAM и `eth0`, связанный veth pair с host bridge.

Docker хранит network namespaces в `/var/run/docker/netns`. Source показывает symbolic-link workaround к `/var/run/netns`, чтобы стандартный `ip netns` мог видеть namespace.

Default bridge позволяет containers общаться по IP; в source example name resolution между containers не работает. User-defined bridge позволяет обращение по именам в показанном lab.

Host network заставляет container использовать host network stack; отдельного container IP/network stack нет. None network предоставляет isolated container без external interface.

Port publishing связывает host port с container port. Outbound connectivity объясняется через NAT/netfilter/MASQUERADE. `-P` выбирает host port автоматически; `-p` задаёт mapping явно; source показывает TCP/UDP-specific publication.

MACVLAN подключает container к physical network как отдельный endpoint со своим MAC/IP. Source разбирает bridge mode и trunk bridge 802.1Q. В default MACVLAN behavior host и container напрямую не общаются; source создаёт host-side MACVLAN interface для host→container connectivity.

Overlay строит virtual L2 network across L3 host network and requires Swarm context in source. `ingress` является default overlay; `docker_gwbridge` используется для external connectivity. Standalone containers require custom overlay with `--attachable`.

Overlay container имеет два interfaces: overlay-side и gateway-side. Overlay-side veth terminates in Docker overlay netns on `br0`. `vxlan0`/VTEP encapsulates Ethernet frames in UDP over physical L3. Source captures UDP 4789 traffic and inspects neighbor entries mapping overlay IP→MAC.

## Основные тезисы источника

- Default networks: Bridge, Host, None.
- Swarm adds ingress and docker_gwbridge.
- docker0 is Linux-bridge based.
- Docker netns path is `/var/run/docker/netns`.
- User-defined bridge supports name communication in source lab.
- Host shares host networking; None isolates.
- Port mapping uses host→container publication; bridge outbound traffic uses NAT.
- MACVLAN connects containers to physical network.
- MACVLAN modes: bridge and trunk bridge 802.1Q.
- Overlay spans hosts and uses VXLAN.
- docker_gwbridge gives overlay containers external connectivity.
- VXLAN carries L2 over L3 using UDP 4789.

## Ключевые термины

| Термин | Смысл главы |
|---|---|
| Bridge network | Single-host Docker network based on Linux bridge |
| docker0 | Default Docker bridge |
| Host network | Shared host network namespace |
| None network | No external interface |
| Network namespace | Isolated network stack |
| veth | Virtual Ethernet pair |
| Port mapping | Host port → container port |
| NAT/MASQUERADE | Translation for external communication |
| MACVLAN | Endpoint tied to physical parent |
| Trunk bridge 802.1Q | MACVLAN using VLAN subinterface |
| Overlay | Multi-host virtual L2 |
| ingress | Default Swarm overlay |
| docker_gwbridge | External gateway bridge for overlay containers |
| br0 | Virtual switch in overlay namespace |
| VXLAN | L2-over-L3 encapsulation |
| VNI | VXLAN network identifier |
| VTEP | VXLAN tunnel endpoint |

## Provenance

- Chapter RAG: `p0114:c01`–`p0151:c01`
- PDF pages: 114–151
- Printed pages: 119–156
- Source SHA-256: `7a52f7d947347a470790c7d384390f60bf49fe5426827f5829a75757b50faaa8`
