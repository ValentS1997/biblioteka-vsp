# Diagram — глава 13: TCP/IP addressing and support services

```mermaid
flowchart TD
    APP[Application / symbolic name] --> DNS[DNS resolver / server]
    DNS --> IPADDR[IPv4 address]

    APP --> TCPUDP[TCP or UDP]
    TCPUDP --> IP[IP packet]
    IPADDR --> IP

    IP --> DEC{Destination on local link?}
    DEC -->|Yes| NH[Next hop = destination]
    DEC -->|No| GW[Next hop = router]

    NH --> ARP[ARP: next-hop IPv4 → local/MAC address]
    GW --> ARP
    ARP --> FRAME[Local-link frame]
    FRAME --> LINK[Ethernet / Wi-Fi / PPP / other link]
    LINK --> ROUTER[Next router or destination]

    DHCP[DHCP] --> CFG[IP + mask + default router + DNS parameters]
    CFG --> IPADDR
    CFG --> DEC
    CFG --> DNS

    CIDR[Prefix / CIDR] --> DEC
```

## Addressing chain

```text
symbolic name
  → DNS
  → IPv4 address/prefix
  → routing/on-link decision
  → ARP/local mapping for next hop
  → link-layer frame
```

## DHCP role

```text
client local broadcast
  → server or relay
  → offers
  → client selects/request
  → selected server acknowledges
  → lease/configuration becomes active
```

Provenance: `p0365:c01`–`p0398:c01`.
