# Глава 5. Сетевые характеристики и качество обслуживания

**Book ID:** `computer-networks-olifer-6e-ru-2020`  
**Artifact contract:** `BIBLIOTEKA-VSP-CHAPTER-ARTIFACT-COLLECTION v1.7`  
**Status:** `RAG_GROUNDED`

## Scope and provenance

| Property | Verified value |
|---|---|
| Source mode | `rag_only` |
| PDF pages | **134-180** |
| Printed pages | **133-179** |
| Next section | PDF **181** — «Вопросы к части I», outside chapter scope |
| Addressable RAG | `p0134:c01` through `p0180:c01` |
| Blank source units in chapter | **none** |
| Source SHA-256 | `e35305daf978f3d14239683d657caa18c92ab6e979626fda22d2f1fa9cc2a5d9` |

## Main principle

The chapter turns vague statements such as “the network is fast/reliable” into measurable service characteristics, then connects those measurements to concrete QoS mechanisms.

The causal chain is:

```text
service expectations
  -> measurable metrics and SLA
  -> statistical observation
  -> application requirements
  -> congestion behavior
  -> queue management / conditioning / feedback
  -> resource reservation / traffic engineering
  -> or deliberate overprovisioning
```

The core idea is that packet-network quality is statistical. Average values alone are insufficient: delay variation, tails of distributions, traffic burstiness and resource utilization materially affect user-visible service.

## Chapter map

| Block | Main idea | RAG |
|---|---|---|
| Types of characteristics | User/provider views; long-, medium- and short-term metrics; SLA | `p0134:c01`-`p0136:c01` |
| Ideal vs real network | Delay variation, reordering, loss, corruption, duplication and throughput degradation | `p0137:c01`-`p0139:c01` |
| Statistical evaluation | Histograms, mean, median, standard deviation, coefficient of variation, quantiles | `p0139:c01`-`p0142:c01` |
| Active/passive measurement | Synthetic probes vs observation of real traffic; synchronization and measurement bias | `p0142:c01`-`p0144:c01` |
| Delay metrics | OWD, jitter, response time, RTT | `p0145:c01`-`p0146:c01` |
| Rate metrics | Sustained, instantaneous and peak rates; burst size and burst coefficient | `p0147:c01`-`p0148:c01` |
| Reliability | Loss ratio, availability, fault tolerance | `p0149:c01`-`p0150:c01` |
| Provider properties | Extensibility, scalability, manageability, interoperability | `p0150:c01`-`p0152:c01` |
| Application requirements | Stream/bursty traffic; sensitivity to delay, jitter and loss | `p0152:c01`-`p0154:c01` |
| QoS methods | Congestion management vs congestion avoidance | `p0155:c01`-`p0156:c01` |
| Queue behavior | Utilization, burstiness, FIFO, priority, weighted and combined scheduling | `p0157:c01`-`p0165:c01` |
| Traffic conditioning | Classification, policing, shaping | `p0166:c01`-`p0169:c01` |
| Congestion feedback | End-to-end and hop-oriented feedback; rate/volume/loss signals | `p0169:c01`-`p0171:c01` |
| Resource reservation | Admission control, bandwidth reservation and delay considerations | `p0172:c01`-`p0175:c01` |
| Traffic engineering | Route selection based on topology, capacity, offered load and QoS goals | `p0176:c01`-`p0179:c01` |
| Overprovisioning | Keep utilization low and monitor capacity rather than applying complex QoS mechanisms | `p0179:c01`-`p0180:c01` |

## Key distinctions

### Average does not describe the whole service

Two paths with the same average delay can provide very different service if their delay variation or high-percentile delay differs.

### Capacity, flow rate and utilization are different quantities

- **Capacity** is a property of the communication resource.
- **Flow rate** describes traffic over an observation interval.
- **Utilization** compares offered load with available service capacity.

As utilization approaches the resource limit, queue waiting can grow sharply and nonlinearly.

### Delay vs jitter vs RTT

- **One-way delay (OWD)** describes one direction.
- **Jitter** describes variation between packet delays.
- **RTT** avoids clock synchronization between endpoints but hides directional asymmetry.
- **Response time** also includes endpoint/server processing and therefore is not a pure network-transport metric.

### Congestion management vs avoidance

- **Management** acts after congestion exists; queue scheduling is the central example.
- **Avoidance** tries to prevent overload; conditioning, feedback, reservation and traffic engineering are examples.

### Policing vs shaping

- **Policing** enforces a traffic profile by dropping or otherwise downgrading excess traffic; average rate can decrease.
- **Shaping** delays excess traffic in a buffer, reducing peaks while preserving the average rate when no packets are discarded.

### Priority vs weighted scheduling

- Strict priority can minimize delay for the highest class but can starve lower classes.
- Weighted scheduling guarantees each class a share of capacity under overload, but by itself does not guarantee low delay.
- Combined schemes trade these properties.

### Reservation vs overprovisioning

Reservation explicitly allocates resources to flows/classes and requires admission logic. Overprovisioning instead keeps the network sufficiently underloaded that queues are rare, at the cost of excess capacity.

## Artifacts

- [cheatsheet.md](cheatsheet.md)
- [commands.md](commands.md)
- [diagram.md](diagram.md)
- [visual-cheatsheet.svg](visual-cheatsheet.svg)
- [visual-cheatsheet-detailed.svg](visual-cheatsheet-detailed.svg)
- [source-findings.md](source-findings.md)

## Conditional artifacts

- `summary.md`: not created — no explicit chapter-end summary/resume appears inside the chapter boundary.
- `review-questions.md` / `review-answers.md`: not created — PDF 181 begins **Questions to Part I**, which is outside the chapter boundary and covers multiple chapters.

## Limitations

1. Mathematical notation in several statistical/queueing formulas is partially damaged by text extraction; exact typography is not reconstructed.
2. Original figures 5.x are not independent multimodal RAG objects.
3. Historical protocol/examples such as RSVP are preserved as source content; no web freshness correction is applied.
4. No executable CLI/configuration procedure is present.
