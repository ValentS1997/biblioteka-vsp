# Diagram — глава 10: Ethernet evolution

```mermaid
flowchart TD
    S[Shared-medium Ethernet] --> CS[CSMA/CD]
    CS --> COL[Carrier sense → transmit → collision detect → backoff]
    S --> HUB[Hub/repeater]
    HUB --> ONE[One logical collision domain]

    S --> SW[Bridge / switch]
    SW --> LEARN[Learn source MAC → ingress port]
    LEARN --> DEC{Destination}
    DEC -->|Known, other port| FWD[Forward]
    DEC -->|Known, same port| FIL[Filter]
    DEC -->|Unknown / broadcast / group| FLOOD[Flood]

    SW --> LOOP[Redundant L2 path]
    LOOP --> BAD[Loop → duplicated/circulating frames + MAC instability]
    BAD --> STP[Loop control deferred to chapter 11 / STP]

    SW --> FD[Microsegmentation + full duplex]
    FD --> PAR[Parallel forwarding]
    PAR --> Q[Output contention → queues]

    FD --> PHY[High-speed PHY evolution]
    PHY --> FAST[Fast Ethernet: 4B/5B · MLT-3]
    PHY --> GE[Gigabit: 8B/10B · 4D-PAM5]
    PHY --> H10[10G/40G/100G: 64B/66B + lanes]
    PHY --> H400[200/400/800G: PAM4 + FEC + faster lanes]
```

## Stable vs changing parts

```text
Mostly stable:
  Ethernet frame + MAC forwarding model

Changed over generations:
  medium access: shared half-duplex → switched full-duplex
  PHY: coding, lane count, optics/copper, FEC, symbol rate
  switch implementation: software bridge → ASIC/FPGA/NPU fabrics
```

Provenance: `p0287:c01`–`p0325:c01`.
