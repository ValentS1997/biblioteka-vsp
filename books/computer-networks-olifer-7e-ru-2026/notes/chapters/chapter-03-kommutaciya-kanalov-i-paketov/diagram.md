# Diagram — глава 3: коммутация каналов и пакетов

```mermaid
flowchart TD
    A[Information flow] --> Q{How is network capacity allocated?}

    Q -->|Reserve before transfer| C[Circuit switching]
    C --> C1[Choose route]
    C1 --> C2[Check elementary channels on every link]
    C2 --> C3{Enough capacity?}
    C3 -->|No| C4[Connection rejected]
    C3 -->|Yes| C5[Build composite circuit]
    C5 --> C6[Exclusive fixed capacity during session]
    C6 --> C7[Release elementary channels]

    Q -->|Share dynamically| P[Packet switching]
    P --> P1[Split message into packets + headers]
    P1 --> P2[Store-and-forward buffers]
    P2 --> P3[Queues / possible overflow]
    P3 --> M{Forwarding model}

    M --> D[Datagram]
    D --> D1[Each packet independent]
    D1 --> D2[Best effort / paths may differ]

    M --> L[Logical connection]
    L --> L1[Endpoints negotiate connection parameters]
    L1 --> L2[State supports reliability/security]
    L2 --> L3[Route may still change per packet]

    M --> V[Virtual circuit]
    V --> V1[Fixed path established]
    V1 --> V2[Packets carry flow label]
    V2 --> V3[Still packet switching]

    C6 --> X[Predictable transfer, lower resource utilization for bursty traffic]
    D2 --> Y[Dynamic utilization, variable delay]
    L3 --> Y
    V3 --> Y
    P3 --> Y
```

## Delay decomposition

```text
Circuit: propagation + serialization (+ setup before transfer)

Packet path:
packetization
+ propagation
+ serialization/buffering
+ queueing
+ switching
repeated across hops, with pipeline overlap between packets
```

Queueing is the principal load-dependent component in the chapter's comparison.

Provenance: `p0081:c01`–`p0107:c01`.
