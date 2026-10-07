# Cheatsheet — глава 5: сетевые характеристики и качество обслуживания

## Symptom / problem framing

**Проблема:** “slow network”, “packet loss”, “jitter”, “overload” и “bad QoS” — слишком общие диагнозы. Глава требует сначала определить **что измеряется, на каком интервале и для какого traffic class**, а затем выбирать mechanism воздействия. `p0131:c01`–`p0177:c01`.

## Baseline / context

| Область | Source model | RAG |
| --- | --- | --- |
| SLA | Metric + quantitative bound + measurement interval/method | `p0133:c01` |
| Delay | OWD, jitter, reaction time, RTT | `p0142:c01`–`p0144:c01` |
| Rate | SIR, IIR, PIR, burst size | `p0144:c01`–`p0146:c01` |
| Reliability | Loss ratio, availability, fault tolerance | `p0146:c01`–`p0147:c01` |
| Traffic shape | Stream/CBR vs burst/VBR | `p0149:c01`–`p0150:c01` |
| App sensitivity | Delay/jitter and loss sensitivity | `p0150:c01`–`p0152:c01` |
| Congestion management | Queue scheduling after congestion exists | `p0152:c01`–`p0162:c01` |
| Congestion avoidance | Conditioning, feedback, reservation, traffic engineering | `p0152:c01`–`p0176:c01` |
| Capacity strategy | Overprovisioning / underloaded mode | `p0176:c01`–`p0177:c01` |

## Read-only checks

1. Какой **user-visible symptom**: response time, one-way delay, RTT, jitter, throughput, loss или availability?
2. На каком **time scale** измеряется metric: packet-level, seconds/hours, months/years? `p0132:c01`–`p0133:c01`.
3. Measurement **active or passive**? Active probes сами создают traffic; passive measurements требуют корректной observation point и иногда mirroring. `p0139:c01`–`p0142:c01`.
4. Не смешивается ли **network response time** с pure transport RTT? `p0143:c01`.
5. Для rate указаны ли **averaging interval**, SIR/PIR и burst behavior? `p0144:c01`–`p0146:c01`.
6. Какой **utilization coefficient** у ресурса и насколько bursty входной поток? `p0155:c01`–`p0157:c01`.
7. Какой scheduler: FIFO, priority, weighted? Какие classes реально делят ресурс? `p0158:c01`–`p0162:c01`.
8. Conditioning выполняет **drop**, **delay** или **remark/reclassify**? `p0163:c01`–`p0166:c01`.
9. Feedback explicit или implicit? Кто генерирует сигнал и кто снижает rate? `p0166:c01`–`p0169:c01`.
10. Reservation прошёл admission control по каждому node/path resource? `p0169:c01`–`p0172:c01`.
11. Есть ли unused alternate paths while shortest path is overloaded? `p0173:c01`–`p0176:c01`.

Фактические interface rates, queue sizes, drops, traffic classes, SLA bounds, topology и measurements пользовательской сети: **[Needs confirmation]**.

## Interpretation

- **Average is not enough.** Средний delay/rate может скрыть tail behavior; source вводит distribution, standard deviation/CV, median/quantiles. `p0136:c01`–`p0139:c01`.
- **RTT is easier but less diagnostic than OWD.** RTT не требует clock sync, но теряет directional asymmetry. `p0143:c01`–`p0144:c01`.
- **High utilization is nonlinear risk.** Queue waiting rises sharply as service utilization approaches saturation, especially for bursty input. `p0155:c01`–`p0157:c01`.
- **Priority is latency-oriented, not fairness-oriented.** High-priority traffic can starve lower classes if its load grows too large. `p0159:c01`–`p0160:c01`.
- **Weighted queues trade latency for bandwidth guarantees.** Each class gets a minimum share under congestion; cycle/granularity affects both proportional accuracy and delay. `p0161:c01`–`p0162:c01`.
- **Policing/profiling protects the network by dropping excess traffic.** Shaping protects conformity by buffering/delaying excess packets. `p0163:c01`–`p0166:c01`.
- **Feedback-loop delay matters.** Stale congestion information can cause oscillations or slow reaction. `p0166:c01`–`p0168:c01`.
- **Reservation without correct traffic envelope can make results worse.** If actual rate exceeds reserved/profiled assumptions, packets can be dropped even when some physical capacity exists. `p0170:c01`–`p0172:c01`.
- **Traffic engineering addresses topology-wide imbalance.** It complements per-node QoS by moving flows away from overloaded resources. `p0173:c01`–`p0176:c01`.
- **Overprovisioning is a valid engineering choice.** It reduces QoS mechanism complexity at the cost of excess capacity and continuous monitoring. `p0176:c01`–`p0177:c01`.

## Next action

Для operational troubleshooting применять порядок:

**symptom → metric definition → measurement method → time window → traffic class → load/burstiness → queue/drop point → conditioning/feedback/reservation → path balance → remeasure against SLA**.

Это source-grounded diagnostic sequence; конкретные команды и thresholds зависят от платформы и должны подтверждаться отдельно.

## Modifying action

**Executable modifying action: [Not applicable].** Глава описывает configuration mechanisms conceptually — priority/weighted queues, profiling, shaping, admission control, resource reservation, route changes — но не приводит CLI syntax или vendor procedure.

## Verification / acceptance checks

Глава усвоена, если можно:

- объяснить разницу OWD / jitter / response time / RTT;
- объяснить SIR / IIR / PIR / burst;
- выбрать active vs passive measurement и назвать limitation;
- объяснить, почему high utilization и burstiness образуют длинные queues;
- сравнить FIFO / priority / weighted queues;
- различить policing/profiling и shaping;
- объяснить feedback-loop risk;
- описать admission control и reservation;
- объяснить, чем traffic engineering отличается от обычного shortest-path routing;
- объяснить overprovisioning как альтернативную QoS strategy.

## Rollback

Для chapter artifacts — **[Not applicable]**. Для production QoS/routing changes rollback procedure в source не задан: **[Needs confirmation]**.
