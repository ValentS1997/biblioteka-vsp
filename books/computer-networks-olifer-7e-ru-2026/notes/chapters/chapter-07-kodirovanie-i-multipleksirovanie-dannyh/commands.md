# Commands and tools — глава 7 (RAG-only)

**Scope:** `computer-networks-olifer-7e-ru-2026:p0215:c01` … `p0241:c01`, PDF pp. 215–241.

## Executable commands

**Исполняемые shell/network/vendor CLI commands в границе главы не обнаружены.**

- read-only commands: **[Not applicable]**;
- workload-generating commands: **[Not applicable]**;
- state-changing commands: **[Not applicable]**.

Не добавлять из памяти PHY debug commands, spectrum/constellation utilities, modem AT commands, Ethernet diagnostics or optical mux CLI.

## Source-confirmed codes, mechanisms and technologies

| Объект | Класс | Роль | RAG |
| --- | --- | --- | --- |
| NRZ | line code | Simple two-level potential coding | `p0220:c01`–`p0221:c01` |
| AMI | bipolar line code | Alternating polarity for ones | `p0221:c01`–`p0222:c01` |
| NRZI | line code | Invert on one; transition-dependent timing | `p0222:c01` |
| Manchester | transition code | Mid-bit transition and self-synchronization | `p0222:c01`–`p0223:c01` |
| 4B/5B / 64B/66B | redundant block codes | Constrain patterns and improve coding properties | `p0223:c01`–`p0224:c01` |
| B8ZS / HDB3 | AMI substitutions | Replace long zero runs with recognizable violations | `p0224:c01`–`p0225:c01` |
| Scrambling | logical transform | Reversible bit mixing to avoid long runs | `p0226:c01` |
| ASK / FSK / PSK | analog modulation | Encode discrete data in carrier amplitude/frequency/phase | `p0226:c01`–`p0228:c01` |
| BPSK / QPSK / QAM | multistate modulation | More information per symbol using phase/amplitude states | `p0228:c01`–`p0230:c01` |
| I/Q representation | modulation model | In-phase/quadrature components for mod/demod | `p0229:c01`–`p0231:c01` |
| Parity / vertical-horizontal parity | error detection | Low-complexity redundancy | `p0231:c01`–`p0232:c01` |
| CRC / FCS | error detection | Frame error detection using polynomial-style remainder operation | `p0231:c01`–`p0232:c01` |
| FEC / Hamming / convolutional codes | error correction | Correct errors without retransmission under source-described models | `p0232:c01`–`p0233:c01` |
| ADC / DAC / codec / PCM | analog digitization | Sample/quantize/reconstruct analog information | `p0234:c01`–`p0236:c01` |
| FDM | multiplexing | Frequency bands per channel | `p0236:c01`–`p0238:c01` |
| WDM / CWDM / DWDM | optical multiplexing | Wavelength/frequency channels in fiber | `p0238:c01` |
| Synchronous TDM | multiplexing/switching | Fixed recurring time slots | `p0238:c01`–`p0241:c01` |
| Asynchronous TDM | source category | Source associates it with packet networks | `p0236:c01`–`p0238:c01` |

## Operational boundary

The chapter supports conceptual identification of coding/multiplexing mechanisms, not platform actions.

For a real link these remain **[Needs confirmation]**:

- negotiated/forced PHY and line code;
- modulation order and symbol rate;
- scrambling/FEC parameters;
- actual spectrum/clock recovery;
- BER/FCS counters;
- multiplexing channel map;
- time-slot/wavelength/frequency allocation;
- supported configuration/rollback procedure.

No command is invented.
