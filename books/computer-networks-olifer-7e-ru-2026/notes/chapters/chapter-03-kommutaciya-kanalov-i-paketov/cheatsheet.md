# Cheatsheet — глава 3: коммутация каналов и пакетов

## Symptom / problem framing

**Проблема:** одной маршрутизации недостаточно — сеть должна решить, как именно делить пропускную способность между конкурирующими информационными потоками. Глава сравнивает два фундаментальных режима: заранее зарезервировать ресурс end-to-end или динамически делить его между отдельными пакетами. `p0081:c01`–`p0107:c01`.

## Baseline / context

| Модель | Resource allocation | Передача | Основной trade-off | RAG |
| --- | --- | --- | --- | --- |
| Circuit switching | Резервируется до передачи | Непрерывно по составному каналу | Predictability ↔ idle reserved capacity | `p0081:c01`–`p0089:c01` |
| Packet switching | Dynamic sharing | Пакеты с headers | Utilization ↔ queueing/loss/jitter | `p0089:c01`–`p0104:c01` |
| Datagram | No per-flow history in network | Каждый packet independent | Fast setup / best effort | `p0093:c01`–`p0094:c01` |
| Logical connection | Endpoint connection state | Packets may take different paths | Reliability/security features ↔ setup/state overhead | `p0095:c01`–`p0096:c01` |
| Virtual circuit | Fixed path + flow label | Packets follow one path | Compact forwarding state ↔ setup/path dependency | `p0097:c01`–`p0098:c01` |

## Read-only checks

1. Какой traffic profile: steady или bursty? `p0088:c01`–`p0089:c01`.
2. Нужна ли гарантированная фиксированная capacity на весь session или допустимо dynamic sharing? `p0085:c01`, `p0099:c01`.
3. Где может возникнуть очередь: input buffer, output buffer или оба? `p0092:c01`–`p0093:c01`.
4. Может ли packet loss быть следствием buffer overflow? `p0093:c01`.
5. Forwarding model: datagram, logical connection или virtual circuit? `p0093:c01`–`p0098:c01`.
6. Передаётся ли полный destination address в каждом packet или compact flow label? `p0097:c01`–`p0098:c01`.
7. При анализе latency разделены ли propagation, serialization, packetization, queueing и switching? `p0100:c01`–`p0104:c01`.
8. Не делается ли вывод о real network из учебного количественного примера? Фактические user-network measurements: **[Needs confirmation]**.

## Interpretation

- **Reservation даёт предсказуемость, но не гарантирует эффективность использования.** Если source замолчал, зарезервированный circuit остаётся недоступен другим flows. `p0085:c01`–`p0089:c01`.
- **Packet switching использует statistical multiplexing.** Несовпадающие bursts разных источников сглаживают aggregate traffic и повышают utilization. `p0090:c01`–`p0091:c01`.
- **Store-and-forward создаёт unavoidable buffering stage.** Queueing появляется дополнительно при mismatch input/output rates или недостаточной switching performance. `p0092:c01`–`p0093:c01`.
- **Datagram best effort не означает “пакет обязательно потеряется”.** Это означает отсутствие гарантии доставки со стороны самого дейтаграммного метода. `p0094:c01`.
- **Logical connection не фиксирует маршрут автоматически.** Packets одного logical connection могут идти разными paths; state mainly находится на endpoints. `p0095:c01`–`p0096:c01`.
- **Virtual circuit фиксирует path и использует label.** Но это всё ещё packet switching, что источник подчёркивает отдельно. `p0097:c01`–`p0098:c01`.
- **Queueing dominates uncertainty.** Propagation и serialization можно вычислять из distance/rate; queueing depends on current load. `p0101:c01`–`p0104:c01`.
- **Ethernet example ties the abstractions together.** Shared medium vs switched topology changes access mechanics, but frames remain packetized data with MAC addressing, checksum and possible queues. `p0105:c01`–`p0107:c01`.

## Next action

При анализе реальной сети использовать последовательность:

**traffic profile → reservation/sharing model → forwarding model → buffer/queue location → bottleneck/capacity → latency decomposition → loss/retry owner → remeasure**.

Это RAG-grounded учебная модель главы, а не готовый vendor-specific runbook.

## Modifying action

**[Not applicable].** Глава описывает установление/разрыв circuits, logical connections и virtual circuits как механизмы технологий, но не даёт пользователю executable CLI/configuration actions.

Конкретная смена forwarding mode, QoS, buffers, link parameters или topology: **[Needs confirmation]**.

## Verification / acceptance checks

Базовое понимание главы подтверждается, если можно:

- объяснить, почему bursty traffic плохо сочетается с permanently reserved capacity;
- описать lifecycle circuit: route/resource check → reservation → transfer → release;
- объяснить причины input/output queues и buffer overflow;
- отличить datagram, logical connection и virtual circuit;
- доказать, почему virtual circuit остаётся packet switching;
- разложить end-to-end delay на propagation / serialization / packetization / queue / switch components;
- объяснить, какие свойства Ethernet в конце главы иллюстрируют packet switching.

## Rollback

Для chapter artifacts — **[Not applicable]**. Source-supported production rollback procedure отсутствует.
