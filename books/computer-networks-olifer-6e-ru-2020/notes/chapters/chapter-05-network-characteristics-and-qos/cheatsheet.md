# Cheatsheet — глава 5

Source mode: `rag_only`. Scope: PDF 134-180 / printed 133-179.

## Symptom / problem framing

“Network quality” is not one metric. The chapter asks how to:

- define service quality quantitatively;
- measure it without distorting the system;
- relate application requirements to network behavior;
- control queueing and overload;
- choose between differentiated QoS mechanisms, reservation, traffic engineering and extra capacity.

## Baseline / context

A real packet network differs from an ideal one through:

- variable packet delay;
- delay variation;
- packet reordering;
- loss/corruption;
- duplication;
- changed output-flow rate.

Therefore service quality must be described statistically rather than by one deterministic value.

## Read-only checks

| Check | Interpretation |
|---|---|
| Mean only or distribution/tail too? | Mean alone can hide rare but severe delay events |
| OWD or RTT? | OWD preserves direction but needs synchronized clocks; RTT is easier to measure but loses directionality |
| Delay or jitter? | Constant large delay and highly variable delay affect applications differently |
| Active or passive measurement? | Synthetic probes simplify controlled measurement but add traffic; passive measurement observes real traffic but is harder to instrument accurately |
| Capacity or flow rate? | Capacity is resource capability; flow rate depends on traffic over time |
| Utilization close to 1? | Queue waiting can grow rapidly even before offered load exceeds nominal capacity |
| FIFO, priority or weighted? | FIFO is simple; priority minimizes top-class delay; weighted queues preserve capacity shares |
| Policing or shaping? | Policing removes/downgrades excess; shaping delays excess |
| Reservation or TE? | Reservation allocates resources along a chosen path; TE also chooses paths to balance load |
| QoS mechanisms or overprovisioning? | Either differentiate/manage traffic or keep utilization low with excess capacity |

## Interpretation

### SLA turns expectations into measurable obligations

A useful SLA must specify:
- the metric;
- threshold/range;
- measurement interval;
- ideally, measurement method.

Without the time interval, even a rate requirement is ambiguous.

### Statistical metrics

The chapter uses:
- histogram/distribution;
- mean;
- median;
- standard deviation;
- coefficient of variation;
- quantiles/percentiles.

High-percentile metrics are useful because packet-service degradation often appears in distribution tails.

### Measurement method matters

**Active measurement**
- creates dedicated probe traffic;
- can carry timestamps;
- enables specialized synchronized measurement hosts;
- must avoid materially changing network load.

**Passive measurement**
- observes actual user traffic;
- avoids synthetic load;
- may suffer from synchronization, timestamp and endpoint-OS limitations;
- can be useful for metrics such as loss that do not always require synchronized clocks.

### Queueing intuition

Two variables strongly influence queue delay:
1. resource utilization;
2. burstiness.

Even when average offered load is below capacity, short bursts can create queues. As utilization approaches 1, delay growth becomes strongly nonlinear.

### Application classes

Applications differ by:
- stream vs bursty traffic;
- sensitivity to absolute delay;
- sensitivity to jitter;
- sensitivity to loss/corruption.

QoS therefore must differentiate traffic instead of treating every packet identically.

### Queue algorithms

- **FIFO:** simple, no differentiation.
- **Strict priority:** best delay for highest class; lower classes can be suppressed.
- **Weighted queues:** capacity shares are assigned to classes; unused share can be redistributed.
- **Combined algorithms:** use priority for delay-sensitive traffic and weighted treatment for other traffic.

### Conditioning

**Classification** assigns traffic to a class.

**Policing** forces compliance with a traffic profile, commonly by dropping excess packets.

**Shaping** buffers and postpones excess packets, smoothing peaks.

Both reduce peak rate; only policing necessarily reduces average rate by removing traffic.

### Feedback

A congested endpoint/intermediate node can cause upstream senders/devices to reduce offered load. Feedback can communicate:
- congestion indication;
- maximum allowed rate;
- maximum allowed volume/window;
- indirect signs such as loss.

Feedback delay matters because stale information can cause oscillation or delayed reaction.

### Reservation and admission control

Before admitting a flow with guarantees, the network checks available unreserved resources along the complete path. Accepted reservations are reflected in local QoS mechanisms such as classifiers and weighted/priority queues.

### Traffic engineering

Traditional shortest-path routing may overload one path while leaving another underused.

TE chooses routes using:
- topology;
- resource capacity;
- offered load;
- flow requirements.

Goal: keep resource utilization below a chosen threshold while satisfying QoS.

### Overprovisioning

The simplest QoS strategy is to keep the network sufficiently underloaded. It reduces the need for complex per-class mechanisms but requires spare capacity and continuous utilization monitoring.

## Next action

For any future QoS troubleshooting or design task, use this sequence:

1. identify the application requirement;
2. choose measurable metrics;
3. determine measurement method/window;
4. measure utilization, burstiness, delay distribution and loss;
5. identify where queues form;
6. choose the least complex mechanism that addresses the actual constraint.

## Modifying action

[Not applicable] — the chapter explains mechanisms conceptually and does not provide a source-confirmed device configuration procedure.

## Verification / acceptance checks

You should be able to explain:

1. SLA and measurement interval;
2. mean/median/standard deviation/CV/quantile;
3. active vs passive measurement;
4. OWD vs jitter vs response time vs RTT;
5. SIR/IIR/PIR and burstiness;
6. loss, availability and fault tolerance;
7. stream vs bursty applications and delay/loss sensitivity;
8. why queues exist below 100% average utilization;
9. FIFO vs priority vs weighted scheduling;
10. policing vs shaping;
11. feedback for congestion avoidance;
12. admission control and resource reservation;
13. traffic engineering;
14. overprovisioning.

## Rollback

[Not applicable] — no state-changing operation is performed.

## Source caveat

Exact mathematical typography in several formulas is extraction-damaged and is not silently reconstructed. See `source-findings.md`.
