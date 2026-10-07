# Diagram — глава 2: общие принципы построения сетей

```mermaid
flowchart TD
    A[Application needs remote resource] --> B[Client part of network service]
    B --> C[Logical protocol: message format + rules]
    C --> D[Network OS / transport means]
    D --> E[NIC + driver]
    E --> F[Physical channel: encoding + synchronization + error control]

    F --> G{More than two nodes?}
    G -- No --> H[Direct computer-computer exchange]
    G -- Yes --> T[Topology of nodes and links]

    T --> AD[Addressing]
    AD --> U[Interface address: unicast / multicast / broadcast / anycast]
    AD --> P[Process address: e.g. TCP/UDP port]

    U --> S[Switching problem]
    P --> S

    S --> FL[1. Define information flow / descriptor]
    FL --> R[2. Routing: choose path]
    R --> RT[Distribute / build forwarding table]
    RT --> FW[3. Forwarding: recognize flow + lookup + send to output interface]
    FW --> M[4. Multiplex / demultiplex]

    M --> SM{Shared medium?}
    SM -- No --> DX[Dedicated / duplex use]
    SM -- Yes --> ARB[Access arbitration / coordination]

    DX --> TH[Observed throughput]
    ARB --> TH
    CAP[Channel capacity] --> TH
    LOAD[Offered load] --> TH
```

## Ключевые разделения

- **Protocol vs interface:** logical rules vs physical boundary.
- **Capacity vs throughput:** maximum channel capability vs measured passed data rate.
- **Routing vs forwarding:** compute/learn path vs apply table to each unit of data.
- **Multiplexing vs shared medium:** shared medium is a special case where flows from different nodes contend for one physical medium.

Provenance: `p0046:c01`–`p0080:c01`.
