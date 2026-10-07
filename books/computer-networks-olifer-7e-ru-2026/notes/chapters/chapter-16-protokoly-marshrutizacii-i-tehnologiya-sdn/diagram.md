# Diagram — глава 16: routing control → programmable networking

```mermaid
flowchart TD
    R[Routing problem] --> CLS{Control model}

    CLS --> DV[Distance Vector]
    DV --> RIP[RIP]
    RIP --> RIPR[neighbor vectors → metric → route]
    RIPR --> RIPFAIL[count-to-infinity]
    RIPFAIL --> MIT[split horizon · triggered update · hold-down]

    CLS --> LS[Link State]
    LS --> OSPF[OSPF / IS-IS]
    OSPF --> HELLO[HELLO]
    HELLO --> LSDB[LSA flood → LSDB]
    LSDB --> SPF[Dijkstra / SPF]
    SPF --> AREA[areas · ABR · backbone]

    CLS --> PV[Path Vector / policy]
    PV --> BGP[BGP]
    BGP --> EB[eBGP between AS]
    BGP --> IB[iBGP inside AS]
    IB --> RR[route reflector]
    EB --> ASP[AS path + policy]

    R --> MC[Multicast]
    MC --> IGMP[IGMP membership]
    MC --> TREE[dense/sparse distribution tree]
    TREE --> RPF[RPF reverse-path check]

    R --> SDN[SDN]
    SDN --> CTRL[controller / control plane]
    CTRL --> OF[OpenFlow: match → action → counters]
    CTRL --> P4[P4 programmable pipeline]

    R --> NFV[NFV]
    NFV --> VNF[VNF chain]
    VNF --> MANO[NFV MANO orchestration]
```

## Operational dependency

```text
unicast:
  neighbor/session → protocol database → selected route → forwarding next hop

multicast:
  membership → tree state → RPF → replication interfaces

SDN:
  controller intent → rule installed on device → counter/state → forwarding

NFV:
  orchestrator intent → VNF lifecycle → service-chain connectivity → packet flow
```

Provenance: `p0472:c01`–`p0513:c01`.
