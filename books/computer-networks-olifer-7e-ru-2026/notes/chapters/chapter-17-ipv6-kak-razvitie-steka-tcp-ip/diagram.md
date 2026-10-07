# Diagram — глава 17: IPv6 addressing, ND and coexistence

```mermaid
flowchart TD
    APP[Application / destination name] --> DNS[DNS A / AAAA]
    DNS --> SEL{IPv6 path selected?}

    SEL -->|IPv6| ADDR[Choose IPv6 source + destination by scope/prefix]
    ADDR --> ROUTER{On-link or routed?}

    ROUTER -->|Need router| RS[RS / RA: discover router + prefix + MTU]
    ROUTER -->|Need local L2 address| NS[Neighbor Solicitation]
    RS --> NH[IPv6 next hop]
    NS --> NA[Neighbor Advertisement]
    NA --> L2[Link-layer destination]

    ADDR --> DAD[DAD before tentative address becomes usable]
    DAD --> NS

    NH --> PMTU{Fits path MTU?}
    L2 --> PMTU
    PMTU -->|Yes| SEND[Send IPv6 packet]
    PMTU -->|Too large| PTB[ICMPv6 Packet Too Big → endpoint adapts]

    SEL -->|IPv4/IPv6 coexistence| COEX{Mechanism}
    COEX --> DS[Dual stack]
    COEX --> TUN[Tunnel: IPv6 passenger over IPv4 transit]
    COEX --> NAT[NAT64 + DNS64 translation]

    SEND --> BASE[40-byte IPv6 base header]
    BASE --> EXT[Optional extension-header chain]
    EXT --> L4[TCP / UDP / ICMPv6 / other]
```

## Neighbor Discovery dependency

```text
Router discovery:
  RS → RA → prefix / MTU / default-router information

Duplicate-address check:
  tentative address → NS to solicited-node multicast
  reply present → duplicate exists

Address resolution:
  target IPv6 known → derive solicited-node multicast
  NS → NA → learn target link-layer address
```

## Transition models

```text
dual stack:
  same node has independent IPv4 + IPv6 configurations

tunnel:
  IPv6 packet remains passenger payload across IPv4 transit

translation:
  IPv6-only and IPv4-only endpoints communicate through protocol/address translation
```

Provenance: `p0514:c01`–`p0545:c01`.
