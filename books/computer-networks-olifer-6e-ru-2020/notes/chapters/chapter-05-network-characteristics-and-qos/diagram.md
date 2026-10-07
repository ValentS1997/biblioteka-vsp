# Chapter 5 diagram

```mermaid
flowchart TD
    A[Service expectations] --> B[SLA and measurable metrics]
    B --> C[Measurement and statistics]

    C --> C1[Delay / jitter / RTT]
    C --> C2[Rate / burstiness]
    C --> C3[Loss / availability]

    C1 --> D[Application requirements]
    C2 --> D
    C3 --> D

    D --> E{Network under load}

    E --> F[Queue management]
    F --> F1[FIFO]
    F --> F2[Priority]
    F --> F3[Weighted / combined]

    E --> G[Congestion avoidance]
    G --> G1[Classification]
    G1 --> G2[Policing]
    G1 --> G3[Shaping]
    G --> G4[Feedback]

    G --> H[Resource reservation]
    H --> H1[Admission control]
    H1 --> H2[Allocate bandwidth / queue resources]

    H --> I[Traffic engineering]
    I --> I1[Topology + capacity + offered load]
    I1 --> I2[Choose balanced routes]

    E --> J[Alternative: overprovision]
    J --> J1[Keep utilization low]
    J1 --> J2[Monitor and upgrade capacity]
```

## Interpretation

QoS starts with measurable requirements, not with queue configuration. The chapter connects observed service quality to traffic characteristics and resource utilization, then introduces increasingly explicit control mechanisms: queue scheduling, conditioning, feedback, reservation and traffic engineering. Overprovisioning is presented as a simpler but capacity-expensive alternative.
