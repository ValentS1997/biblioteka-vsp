# Diagram — глава 12: Carrier Ethernet service and OAM

```mermaid
flowchart LR
    CE1[Customer Edge / site A] --> UNI1[UNI / Provider Edge]
    UNI1 --> PUSH[Map customer service<br/>C-VID → add S-VID]
    PUSH --> CORE[Provider Ethernet core]
    CORE --> POP[Remove S-VID]
    POP --> UNI2[UNI / Provider Edge]
    UNI2 --> CE2[Customer Edge / site B]

    MEP1[MEP] -. CCM .-> MIP1[MIP]
    MIP1 -. transit CCM .-> MIP2[MIP]
    MIP2 -. CCM .-> MEP2[MEP]

    MEP1 --> PERF[Y.1731 delay / variation / loss]
    MEP2 --> PERF

    CE1 --> ELMI[E-LMI<br/>service state / parameters]
    ELMI --> UNI1

    UNI1 --> LOOP[Physical remote loopback<br/>disruptive maintenance test]
```

## Carrier-grade gaps addressed by the chapter

```text
classic Ethernet
  → cheap/simple best-effort frame forwarding

carrier requirements
  → customer/provider address separation
  → controllable resilient paths
  → connectivity/fault OAM
  → delay/loss performance monitoring
  → service-state visibility

Provider Bridge
  → Q-in-Q / C-VID + S-VID
  → still customer-MAC scaling and STP limits

PBB / MPLS-based evolution in source
  → stronger separation / different provider transport model
```

Provenance: `p0351:c01`–`p0360:c01`.
