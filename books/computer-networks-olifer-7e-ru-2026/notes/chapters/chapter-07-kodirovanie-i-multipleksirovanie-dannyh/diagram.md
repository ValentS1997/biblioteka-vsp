# Diagram — глава 7: coding → error control → multiplexing

```mermaid
flowchart TD
    I[Information] --> T{Information type}
    T -->|Discrete| D[Discrete data]
    T -->|Analog| A[Analog source]

    D --> S{Signal type}
    S -->|Discrete| LC[Line coding]
    LC --> NRZ[NRZ / AMI / NRZI / Manchester]
    LC --> RED[4B/5B · 64B/66B · B8ZS/HDB3 · scrambling]

    S -->|Analog| MOD[Carrier modulation]
    MOD --> M1[ASK / FSK / PSK]
    MOD --> QAM[QAM / I-Q representation]

    A --> AA[Analog modulation: AM / FM]
    A --> AD[Sampling + quantization]
    AD --> PCM[ADC / PCM / binary samples]
    PCM --> LC

    NRZ --> E[Error-control layer]
    RED --> E
    M1 --> E
    QAM --> E
    E --> DET[Parity / CRC-FCS: detect]
    E --> FEC[FEC: correct]

    DET --> MX[Multiplex flows]
    FEC --> MX
    MX --> FDM[FDM: frequency bands]
    MX --> WDM[WDM: optical wavelengths]
    MX --> TDM[TDM: time division]

    TDM --> ATDM[Asynchronous TDM → packet sharing in source model]
    TDM --> STDM[Synchronous TDM → fixed recurring slots]
    STDM --> SW[Switch by reordering slot/byte positions]
```

## Design constraints

```text
coding choice
  → spectrum width / position
  → self-synchronization
  → noise tolerance
  → redundancy / error behavior
  → symbol rate and bit rate

multiplexing choice
  → frequency / wavelength / time resource allocation
  → compatible switching semantics
```

Provenance: `p0215:c01`–`p0241:c01`.
