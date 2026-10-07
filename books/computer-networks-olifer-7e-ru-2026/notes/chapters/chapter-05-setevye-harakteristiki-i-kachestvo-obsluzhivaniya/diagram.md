# Diagram — глава 5: QoS workflow

```mermaid
flowchart TD
    S[User symptom / SLA requirement] --> M[Define metric]
    M --> M1[Delay: OWD / jitter / RTT / response time]
    M --> M2[Rate: SIR / IIR / PIR / burst]
    M --> M3[Reliability: loss / availability]
    M1 --> X[Measure]
    M2 --> X
    M3 --> X

    X --> A{Measurement method}
    A -->|Active| AP[Inject measurement packets]
    A -->|Passive| PP[Observe real traffic / mirror]

    AP --> C[Classify traffic + application sensitivity]
    PP --> C
    C --> L[Assess utilization + burstiness + bottleneck]

    L --> Q{Congestion exists?}
    Q -->|Yes| QM[Congestion management: queues]
    QM --> FIFO[FIFO]
    QM --> PRI[Priority]
    QM --> W[Weighted queues]

    Q -->|Prevent / control| AV[Congestion avoidance]
    AV --> POL[Profiling / policing: drop excess]
    AV --> SH[Shaping: buffer/delay excess]
    AV --> FB[Feedback: reduce source/upstream rate]
    AV --> RES[Admission control + reservation]
    AV --> TE[Traffic engineering]
    AV --> OP[Overprovisioning]

    FIFO --> V[Re-measure]
    PRI --> V
    W --> V
    POL --> V
    SH --> V
    FB --> V
    RES --> V
    TE --> V
    OP --> V
    V --> SLA{Within SLA / target?}
    SLA -->|No| M
    SLA -->|Yes| OK[Accept current QoS state]
```

## Key relationships

- Queueing delay depends strongly on **utilization** and **burstiness**.
- Priority reduces latency for favored traffic but can starve lower classes.
- Weighted queues protect minimum bandwidth shares under congestion.
- Policing drops; shaping delays.
- Reservation coordinates resources along the path.
- Traffic engineering changes route/resource placement.
- Overprovisioning avoids congestion by maintaining excess capacity.

Provenance: `p0131:c01`–`p0177:c01`.
