# Diagram — глава 8: OTN transport pipeline

```mermaid
flowchart TD
    C[Client signal: Ethernet / SDH / other] --> MAP{Client mapping}
    MAP -->|Synchronous| SYNC[Rate alignment / synchronous mapping]
    MAP -->|Frame/bursty| GFP[GFP-F / GFP-T envelope]

    SYNC --> OPU[OPU: client payload + mapping/alignment overhead]
    GFP --> OPU

    OPU --> ODU[ODU: end-to-end monitoring + multiplexing]
    ODU --> TS[Tributary slots + PSI]
    TS --> HODU[Higher-order ODU]

    HODU --> OTU[OTU: section transport + FEC]
    ODU --> OTU
    OTU --> PH[Photonic layer / DWDM spectral channel]

    PH --> N1[Adjacent OTN node]
    N1 --> X{Equipment function}
    X --> TM[TM: terminate]
    X --> ADM[ADM: add/drop]
    X --> DXC[DXC / OTN switch: cross-connect]
    X --> REG[Regenerate]

    DXC --> PH2[Next DWDM section]
    ADM --> PH2
    REG --> PH2
    PH2 --> DEST[Destination OTN node]
    DEST --> DEMAP[Demultiplex / decapsulate]
    DEMAP --> CLIENT[Original client signal]
```

## Architecture evolution

```text
PDH
  → bit stuffing / difficult lower-order extraction

SDH
  → pointers + virtual containers + fixed 125 μs cycle

OTN
  → larger transport units
  → explicit OPU/ODU/OTU layering
  → FEC
  → GFP/client transparency
  → tributary slots / flexible hierarchy
  → transponder → muxponder → OTN switching
```

Provenance: `p0242:c01`–`p0267:c01`.
