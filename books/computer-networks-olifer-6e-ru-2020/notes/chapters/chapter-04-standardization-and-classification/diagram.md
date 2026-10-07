# Chapter 4 diagram

```mermaid
flowchart TD
    A[Complex network interaction] --> B[Decompose into modules]
    B --> C[Organize modules into layers]

    C --> D[Adjacent-layer interface]
    C --> E[Peer-layer protocol]
    E --> F[Protocol stack]

    F --> G[OSI reference model]
    G --> G1[7 Application]
    G1 --> G2[6 Presentation]
    G2 --> G3[5 Session]
    G3 --> G4[4 Transport]
    G4 --> G5[3 Network]
    G5 --> G6[2 Data Link]
    G6 --> G7[1 Physical]

    G --> H[Standardization and open systems]
    H --> I[Open specifications]
    I --> J[Interoperability and replaceability]

    H --> K[Internet standards / RFC process]
    H --> L[Concrete protocol stacks]

    L --> M[Real stacks only approximately map to OSI]
    M --> N[Horizontal planes]
    N --> N1[User plane]
    N --> N2[Control plane]
    N --> N3[Management plane]

    M --> O[Services]
    O --> O1[Transport services]
    O --> O2[Information services]

    O --> P[Network classification]
    P --> P1[LAN / MAN / WAN]
    P --> P2[Wired / Wireless]
    P --> P3[Packet / Circuit]
    P --> P4[Topology]
    P --> P5[Carrier / Corporate / Personal]
    P --> P6[Access / Aggregation / Backbone]
    P --> P7[Primary / Overlay]
```

## Interpretation

The chapter moves from decomposition of a single network interaction problem to two complementary models:

- **vertical structure** — layers, interfaces and protocols;
- **horizontal structure** — user, control and management planes.

Standardization makes implementations from different vendors interoperable, while classification provides multiple independent ways to describe a network.
