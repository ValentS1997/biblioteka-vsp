# Diagram — глава 6: от физической среды к capacity

```mermaid
flowchart TD
    A[Data endpoint / DTE] --> D[DCE / PHY termination]
    D --> M{Physical medium}
    M --> CU[Copper: twisted pair / coax]
    M --> FI[Fiber: MMF / SMF]

    D --> SIG[Information signal]
    SIG --> SP[Frequency spectrum / harmonics]
    SP --> BW[Line bandwidth in Hz]

    CU --> IMP[Impairments]
    FI --> IMP
    IMP --> ATT[Attenuation]
    IMP --> NOISE[Noise / crosstalk / SNR]
    IMP --> DISP[Fiber dispersion / nonlinear effects]

    ATT --> LB[Link budget vs receiver sensitivity]
    NOISE --> BER[Bit error behavior]
    DISP --> DIST[Reach / pulse distortion]

    BW --> COD[Physical coding / modulation]
    COD --> BAUD[Symbol rate / baud]
    COD --> STATES[Distinguishable signal states]
    STATES --> RATE[Bit rate / capacity]
    BAUD --> RATE
    BW --> LIM[Shannon / Nyquist limits]
    NOISE --> LIM
    LIM --> RATE

    RATE --> OK{Reliable recognition at receiver?}
    LB --> OK
    BER --> OK
    DIST --> OK

    OK -->|Yes| LINK[Usable physical link]
    OK -->|No| FIX[Change medium / length / power / coding / termination]

    LINK --> SCS[Structured cabling: horizontal / vertical / campus]
```

## Key distinctions

- `bandwidth` in this chapter: Hz range passed by the line.
- `capacity`: bit/s achievable for the line **with a chosen physical coding/protocol**.
- `baud`: symbol/state changes per second; it is not automatically equal to bit/s.
- Copper emphasizes resistance/capacitance/inductance, noise and crosstalk.
- Fiber largely avoids electromagnetic interference but has attenuation/dispersion/nonlinear limits.

Provenance: `p0183:c01`–`p0214:c01`.
