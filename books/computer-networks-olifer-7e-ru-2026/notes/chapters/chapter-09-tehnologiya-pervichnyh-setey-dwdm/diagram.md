# Diagram — глава 9: DWDM optical path

```mermaid
flowchart LR
    C[Client optical signal] --> T1[Transponder<br/>client λ → DWDM λ]
    T1 --> M[Optical multiplexer]
    M --> F[Composite colourless signal<br/>many spectral channels]

    F --> A[Optical amplifier]
    A --> OADM{OADM}
    OADM -->|Drop λx| LOCAL[Local transponder/client]
    OADM -->|Pass remaining λ| PATH[Optical line]
    LOCAL2[Local transponder/client] -->|Add λx after drop| OADM

    PATH --> R{ROADM / OXC}
    R --> WSS[WSS selects wavelengths<br/>from ingress directions/banks]
    WSS --> OUT1[Egress direction A]
    WSS --> OUT2[Egress direction B]
    WSS --> BANK[Local transponder bank]

    OUT1 --> D[Optical demultiplexer]
    D --> T2[Destination transponder]
    T2 --> DEST[Destination client]
```

## Resource model

```text
fiber
  → frequency plan
    → spectral slots
      → wavelength/spectral channels
        → add/drop or cross-connect state
          → optical power / dispersion constraints
```

## Equipment evolution

```text
fixed OADM
  → wavelength-specific physical add/drop

OXC
  → mesh cross-connect

ROADM + WSS
  → remote wavelength routing
  → optionally colorless / directionless architecture
```

Provenance: `p0268:c01`–`p0281:c01`.
