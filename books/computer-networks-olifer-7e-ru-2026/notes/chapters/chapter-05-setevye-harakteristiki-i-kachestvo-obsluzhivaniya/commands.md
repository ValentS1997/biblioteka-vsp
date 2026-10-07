# Commands and tools — глава 5 (RAG-only)

**Scope:** `computer-networks-olifer-7e-ru-2026:p0131:c01` … `p0177:c01`, PDF pp. 131–177.

## Executable commands

**Исполняемые shell/network/vendor CLI commands в границе главы не обнаружены.**

Классификация:

- read-only commands: **[Not applicable]**;
- workload-generating commands: **[Not applicable]**;
- state-changing commands: **[Not applicable]**.

Важно: глава описывает **active measurements**, которые генерируют measurement packets, то есть operationally создают workload, но конкретной команды/утилиты/packet rate source не задаёт.

## Source-confirmed metrics and mechanisms

| Объект | Класс | Роль | RAG |
| --- | --- | --- | --- |
| SLA | service agreement | Quantitative QoS bounds + measurement interval/method | `p0133:c01` |
| Histogram / mean / deviation / CV / quantile | statistics | Describe random network metrics | `p0136:c01`–`p0139:c01` |
| Active measurement | measurement method | Inject dedicated measurement traffic | `p0139:c01`–`p0141:c01` |
| Passive measurement / port mirroring | measurement method | Observe real traffic | `p0141:c01`–`p0142:c01` |
| OWD / jitter / RTT | delay metrics | Delay and variation characterization | `p0142:c01`–`p0144:c01` |
| SIR / IIR / PIR / burst | rate metrics | Long/short-term traffic characterization | `p0144:c01`–`p0146:c01` |
| Loss ratio / availability / fault tolerance | reliability metrics | Delivery/service/system reliability | `p0146:c01`–`p0147:c01` |
| FIFO | queue scheduler | Single undifferentiated queue | `p0158:c01` |
| Strict priority | queue scheduler | Prefer high-priority classes | `p0159:c01`–`p0160:c01` |
| Weighted queues | queue scheduler | Minimum capacity share per class | `p0161:c01`–`p0162:c01` |
| Traffic profiling/policing | conditioning | Drop traffic exceeding profile | `p0163:c01`–`p0164:c01` |
| Traffic shaping | conditioning | Delay/buffer excess traffic | `p0164:c01`–`p0166:c01` |
| Token bucket | algorithm reference | Source names it for shaping/profiling | `p0166:c01` |
| Flow/congestion feedback | congestion avoidance | Signal source/upstream nodes to reduce rate | `p0166:c01`–`p0169:c01` |
| TCP | protocol example | Source example of implicit congestion information | `p0169:c01` |
| Admission control | reservation control | Check free resource along path | `p0170:c01` |
| Resource/bandwidth reservation | QoS mechanism | Reserve per-flow capacity/state | `p0169:c01`–`p0172:c01` |
| Traffic engineering | routing/resource method | Balance flows over network resources | `p0173:c01`–`p0176:c01` |
| RSVP | reservation protocol reference | Source sidebar describes path reservation signalling | `p0177:c01` |

## Source-described state changes without executable syntax

Source mechanisms that would change real network behavior:

- queue class/priority/weight configuration;
- buffer allocation;
- traffic classification/remarking;
- profiling/policing and shaping;
- admission-control/reservation state;
- traffic-engineered route placement;
- overprovisioning/capacity upgrade.

For all of them:

- exact command/syntax/platform: **[Needs confirmation]**;
- before-state capture: **[Needs confirmation]**;
- verification command: **[Needs confirmation]**;
- rollback command: **[Needs confirmation]**.

No vendor command is invented to fill these gaps.
