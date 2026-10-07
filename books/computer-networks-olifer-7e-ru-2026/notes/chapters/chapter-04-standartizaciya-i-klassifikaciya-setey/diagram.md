# Diagram — глава 4: стандартизация и классификация сетей

```mermaid
flowchart TD
    A[Complex network interaction] --> D[Decomposition into modules]
    D --> L[Group modules into layers]
    L --> I[Service interfaces between adjacent layers]
    L --> P[Peer protocols between same-level entities]
    I --> S[Protocol stack]
    P --> S

    S --> O[OSI reference model]
    O --> O7[Application]
    O --> O6[Presentation]
    O --> O5[Session]
    O --> O4[Transport]
    O --> O3[Network]
    O --> O2[Data Link]
    O --> O1[Physical]

    O --> E[Encapsulation down / decapsulation up]
    O --> N[Node responsibility]
    N --> N1[End node: full stack]
    N --> N2[Repeater: physical]
    N --> N3[LAN switch: physical + data link]
    N --> N4[Router: physical + data link + network]

    O --> H[Horizontal view]
    H --> U[User plane]
    H --> C[Control plane]
    H --> M[Management plane]

    S --> ST[Standardization]
    ST --> OPEN[Open specifications]
    OPEN --> INT[Interoperability / replaceability / interconnection]
    ST --> RFC[Internet: RFC / IETF ecosystem]
    ST --> TCP[Standard protocol stacks → TCP/IP dominance]
    TCP --> IP[IP as narrow waist]

    ST --> CL[Classification]
    CL --> GEO[LAN / MAN / WAN]
    CL --> MED[Wired / wireless]
    CL --> SW[Packet / circuit switching]
    CL --> TOP[Topology]
    CL --> USER[Carrier / corporate / personal]
    CL --> ROLE[Access / aggregation / backbone]
    CL --> OV[Primary / overlay]
```

## Логика главы

Многоуровневая архитектура отвечает на вопрос **«как разделить сложность»**; стандартизация — **«как сделать независимые реализации совместимыми»**; классификация — **«по каким независимым признакам описывать реальные сети»**.

Provenance: `p0108:c01`–`p0130:c01`.
