# Diagram — глава 14: IPv4 forwarding path

```mermaid
flowchart TD
    P[IPv4 packet arrives] --> TTL[Decrement / validate TTL]
    TTL -->|Expired| ICMP1[Drop + ICMP time-exceeded]
    TTL -->|Alive| ROUTE[Routing-table lookup]

    ROUTE --> HOST{Host-specific /32 match?}
    HOST -->|Yes| CHOSEN[Selected route]
    HOST -->|No| PREFIX[Match destination against route masks/prefixes]
    PREFIX --> LPM[Choose most-specific / longest prefix]
    LPM --> DEFAULT{Any match?}
    DEFAULT -->|No + default exists| DEF[Use 0.0.0.0/0]
    DEFAULT -->|No route| ICMP2[Drop / possible ICMP unreachable]
    DEF --> CHOSEN
    LPM --> CHOSEN

    CHOSEN --> NH[Next hop + outgoing interface]
    NH --> MTU{Packet fits next-link MTU?}
    MTU -->|Yes| LINK[Resolve local next-hop address and transmit]
    MTU -->|No, DF clear| FRAG[Fragment → ID / offset / MF]
    MTU -->|No, DF set| ICMP3[Drop + diagnostic ICMP]
    FRAG --> LINK

    LINK --> DEST{Destination host?}
    DEST -->|No| P
    DEST -->|Yes| REASM[Reassemble fragments at destination]
    REASM --> UPPER[Deliver to upper-layer protocol]
```

## Diagnostics

```text
ping
  → ICMP echo request/reply
  → reachability + RTT/loss sample

traceroute / tracert
  → probes with increasing TTL
  → ICMP time-exceeded reveals intermediate routers

ICMP
  → reports conditions
  → does not retransmit lost IP data
```

## QoS model

```text
IntServ + RSVP
  → reserve resources per flow, end to end
  → poor source-described scalability

DiffServ
  → mark packet class in DS/DSCP
  → router applies PHB per hop
  → EF / AF / LE / best effort in source
```

Provenance: `p0399:c01`–`p0441:c01`.
