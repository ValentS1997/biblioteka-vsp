# Mermaid — глава 9 «Сеть и ее конфигурация»

Источник: **RAG `p0270:c01`–`p0319:c01`**, PDF/печатные страницы 270–319. Диаграммы синтезированы из текста главы; исходные рисунки 9.1–9.7 не реконструируются.

## 1. Четырёхуровневый сетевой стек

```mermaid
flowchart TD
  APP["Application layer: HTTP / TLS / DNS"] --> TRANS["Transport: TCP / UDP"]
  TRANS --> NET["Network: IPv4 / IPv6"]
  NET --> PHY["Physical/link: Ethernet / Wi-Fi"]
  PHY --> MEDIUM["Frames / physical medium"]
  MEDIUM --> PHY2["Remote physical/link"]
  PHY2 --> NET2["Remote network layer"]
  NET2 --> TRANS2["Remote transport"]
  TRANS2 --> APP2["Remote application"]
```

Глава сознательно использует четырёхуровневую модель, а не OSI-7 (§9.3).

## 2. Address + subnet + route

```mermaid
flowchart TD
  IF["Kernel interface"] --> ADDR["IP address / CIDR"]
  ADDR --> LOCAL{"Destination in connected subnet?"}
  LOCAL -->|Yes| DIRECT["Send directly through interface"]
  LOCAL -->|No| RT["Kernel routing table"]
  RT --> MATCH["Choose longest matching prefix"]
  MATCH --> GW{"Specific route?"}
  GW -->|Yes| NEXTHOP["Send to configured next hop"]
  GW -->|No| DEF["Use default route / gateway"]
```

Address assignment and route selection are distinct; the default route is the least-specific catch-all (§9.4–9.6).

## 3. IPv4 / IPv6 dual stack

```mermaid
flowchart LR
  HOST["One host/application"] --> V4["IPv4 address + route table"]
  HOST --> V6["IPv6 global + link-local + route table"]
  V6 --> RA["Router Advertisement / link-local gateway"]
  APP["Dual-stack application"] --> CHOOSE{"Choose address family"}
  CHOOSE --> V4
  CHOOSE --> V6
```

The source treats IPv4 and IPv6 as independent network-layer protocols that may coexist (§9.7.2).

## 4. Name-resolution chain

```mermaid
flowchart TD
  APP["Application lookup"] --> LIB["System resolver / shared library"]
  LIB --> NSS["/etc/nsswitch.conf"]
  NSS --> HOSTS["/etc/hosts"]
  NSS --> DNS["DNS path"]
  DNS --> CACHE["systemd-resolved / dnsmasq / other cache"]
  CACHE --> NS["Configured nameserver"]
  NS --> ANSWER["Address returned to application"]
```

With systemd-resolved, `/etc/resolv.conf` may point to an automatically generated file (§9.15).

## 5. TCP ports and listener role

```mermaid
flowchart LR
  CLIENT["Client process"] --> EPHEM["Local ephemeral port"]
  EPHEM --> TCP["TCP connection"]
  TCP --> WELL["Remote well-known/service port"]
  WELL --> SERVER["Listening server process"]
  LISTEN["netstat -ntl"] --> SERVER
  CONN["netstat -nt"] --> TCP
```

Port pairs identify one TCP connection; listener state is a separate observation (§9.17.1).

## 6. NetworkManager ownership model

```mermaid
flowchart TD
  K["Kernel / udev device events"] --> NM["NetworkManager daemon"]
  DBUS["User / desktop D-Bus requests"] --> NM
  CFG["Connections + config/plugins"] --> NM
  NM --> TOOLS["DHCP / lower-level tools"]
  NM --> KCFG["Kernel address / route / link state"]
  NETPLAN["Netplan YAML"] --> BACKEND{"Backend"}
  BACKEND --> NM
  BACKEND --> ND["systemd-networkd"]
```

Before persistent changes, identify which manager/backend actually owns the interface (§9.12–9.14).

## 7. Linux router / NAT path

```mermaid
flowchart LR
  LAN["Private LAN host"] --> RIN["Router LAN interface"]
  RIN --> FWD{"IPv4 forwarding enabled?"}
  FWD -->|No| STOP["Packet not routed"]
  FWD -->|Yes| NAT["Optional NAT / masquerade"]
  NAT --> WAN["Uplink / internet"]
  WAN --> NAT
  NAT --> RIN
  RIN --> LAN
```

Forwarding and NAT are separate mechanisms. Private IPv4 requires translation to communicate with the public internet in the chapter's example (§9.21–9.23).

## 8. Firewall chain model

```mermaid
flowchart TD
  IN["Packet enters host"] --> INCHAIN["INPUT chain"]
  INCHAIN --> LOCAL["Local process"]
  FWDIN["Packet to be routed"] --> FWD["FORWARD chain"]
  FWD --> OUTPHY["Outgoing interface"]
  PROC["Local process generates packet"] --> OUT["OUTPUT chain"]
  OUT --> OUTPHY
  RULES["Rules evaluated top → bottom; first match wins"] --> INCHAIN
  RULES --> FWD
  RULES --> OUT
```

Default chain policy applies only when no rule matches (§9.25.1–9.25.3).

## 9. Ethernet neighbor resolution

```mermaid
flowchart TD
  IP["Need to send IP packet"] --> N{"Neighbor MAC known?"}
  N -->|Yes| FRAME["Build Ethernet frame"]
  N -->|No, IPv4| ARP["ARP request on local subnet"]
  N -->|No, IPv6| NDP["NDP neighbor solicitation"]
  ARP --> CACHE["Update neighbor cache"]
  NDP --> CACHE
  CACHE --> FRAME
  FRAME --> NIC["Transmit via interface"]
```

For destinations outside the local subnet, the host resolves the router's MAC rather than the final remote host (§9.26).

## 10. Layered troubleshooting workflow

```mermaid
flowchart TD
  S["Symptom"] --> L1["Link/interface: UP? associated? MAC?"]
  L1 --> L2["IP/CIDR assigned?"]
  L2 --> L3["Route/default gateway correct?"]
  L3 --> L4["Direct IP reachability?"]
  L4 --> L5["NSS/DNS resolution?"]
  L5 --> L6["TCP/UDP listener/connection?"]
  L6 --> L7["Forwarding/NAT/firewall policy?"]
  L7 --> V["Verify same layer after one change"]
```

This is an operational synthesis of chapter concepts, not a distro-specific troubleshooting script.
