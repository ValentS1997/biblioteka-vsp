# Cheatsheet — глава 7: кодирование и мультиплексирование данных

## Symptom / problem framing

**Проблема:** физическая линия может иметь достаточную nominal bandwidth, но выбранный код/модуляция может иметь слишком широкий spectrum, плохую self-synchronization или insufficient noise margin. Даже после успешного coding нужно определить, как несколько user flows разделят общий medium. `p0215:c01`–`p0241:c01`.

## Baseline / context

| Stage | Source question | RAG |
| --- | --- | --- |
| Information type | Discrete or analog? | `p0215:c01`–`p0216:c01` |
| Signal type | Discrete or analog carrier? | `p0215:c01`–`p0217:c01` |
| Spectrum | Does coded signal fit line bandwidth? | `p0217:c01`–`p0219:c01` |
| Synchronization | Can receiver recover symbol timing? | `p0219:c01`–`p0223:c01` |
| Error control | Detection only or correction? | `p0231:c01`–`p0233:c01` |
| Analog digitization | Sampling + quantization + binary representation | `p0234:c01`–`p0236:c01` |
| Resource sharing | Frequency/wavelength/time division | `p0236:c01`–`p0241:c01` |

## Read-only checks

1. Что исходно: **discrete information** или **analog information**?
2. Какой signaling family: discrete line code или analog modulation?
3. Каков symbol/clock rate и сколько bits несёт одно distinguishable state? `p0216:c01`–`p0219:c01`.
4. Есть ли long runs, DC component или недостаток transitions для clock recovery? `p0220:c01`–`p0226:c01`.
5. Применяется ли redundant block code, scrambling или bipolar substitution? `p0223:c01`–`p0226:c01`.
6. Для analog modulation: ASK/FSK/PSK/QAM; сколько реально разрешённых constellation states? `p0226:c01`–`p0230:c01`.
7. Error control: parity, CRC/FCS, FEC? Кто обнаруживает, кто исправляет, кто retransmits? `p0231:c01`–`p0233:c01`.
8. Для sampled analog source: выполняется ли source sampling condition relative to highest relevant frequency/band? `p0234:c01`–`p0235:c01`.
9. Multiplexing mode: FDM/WDM/synchronous TDM/asynchronous TDM? `p0236:c01`–`p0241:c01`.
10. В synchronous TDM не смешивается ли time-slot identity with per-packet addressing? `p0239:c01`–`p0241:c01`.

Фактический PHY, line code, modulation order, FEC, symbol rate, spectrum and mux configuration пользовательской сети: **[Needs confirmation]**.

## Interpretation

- **Narrower spectrum can buy data rate on the same line.** Но код может требовать больше states, clock transitions or redundancy. `p0217:c01`–`p0226:c01`.
- **Self-synchronization is part of correctness, not an optional feature.** Receiver must know when to sample a new symbol. `p0219:c01`–`p0223:c01`.
- **4B/5B trades 25% symbol overhead for controlled patterns.** Source then notes higher-rate Ethernet examples using 64B/66B with lower relative redundancy. `p0223:c01`–`p0224:c01`.
- **B8ZS/HDB3 are not generic compression.** They deliberately replace forbidden zero runs with recognizable violations to preserve timing/DC properties. `p0224:c01`–`p0225:c01`.
- **QAM increases bits/symbol but constellation points need distinguishability under noise.** Source explicitly leaves some amplitude/phase combinations unused to improve robustness in its example. `p0228:c01`–`p0229:c01`.
- **CRC detects; FEC corrects.** Their redundancy goals and receiver behavior differ. `p0231:c01`–`p0233:c01`.
- **Sampling rate and line coding are different stages.** PCM first converts analog amplitude samples to binary words; those bits then still need physical encoding for transmission. `p0234:c01`–`p0236:c01`.
- **FDM/WDM allocate spectrum continuously per channel; synchronous TDM allocates recurring time slots.** `p0236:c01`–`p0241:c01`.
- **Synchronous TDM can waste idle slots.** Slot position must remain stable because it serves as channel identity in the source model. `p0239:c01`–`p0241:c01`.

## Next action

Для physical-layer analysis использовать порядок:

**information type → line/modulation code → symbol rate/states → spectrum fit → clock recovery → error-control code → multiplexing mode → switching/addressing semantics → verify received signal/error behavior**.

Это source-grounded sequence; concrete PHY commands, eye diagrams, constellation tools and vendor counters require separate confirmation.

## Modifying action

**[Not applicable].** Глава не содержит executable configuration procedure. Изменение modulation order, line code, FEC, symbol rate or multiplexing requires platform/standard-specific rollback and acceptance plan: **[Needs confirmation]**.

## Verification / acceptance checks

Глава усвоена, если можно:

- классифицировать преобразование как Д-Д / Д-А / А-А / А-Д;
- объяснить, почему spectrum и synchronization влияют на выбор кода;
- сравнить NRZ / AMI / NRZI / Manchester;
- объяснить назначение 4B/5B, 64B/66B, B8ZS/HDB3 and scrambling;
- различить ASK / FSK / PSK / QAM;
- объяснить I/Q representation conceptually;
- различить parity / CRC / FEC и роль Hamming distance;
- объяснить sampling/PCM pipeline;
- различить FDM / WDM / synchronous vs asynchronous TDM;
- объяснить, почему time-slot position в synchronous TDM фактически является channel identity.

## Rollback

Для chapter artifacts — **[Not applicable]**. Для production PHY/multiplexing changes rollback procedure source не задаёт.
