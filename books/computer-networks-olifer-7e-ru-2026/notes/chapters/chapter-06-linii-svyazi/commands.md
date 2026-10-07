# Commands and tools — глава 6 (RAG-only)

**Scope:** `computer-networks-olifer-7e-ru-2026:p0183:c01` … `p0214:c01`, PDF pp. 183–214.

## Executable commands

**Исполняемые shell/network/vendor CLI commands в границе главы не обнаружены.**

- read-only commands: **[Not applicable]**;
- workload-generating commands: **[Not applicable]**;
- state-changing commands: **[Not applicable]**.

Источник описывает измерительные величины и физические компоненты, но не даёт конкретных CLI/tester procedures. Не добавлять из памяти `ethtool`, optical DOM commands, cable-test commands, TDR/OTDR workflows или vendor CLI.

## Source-confirmed metrics, interfaces and media

| Объект | Класс | Роль | RAG |
| --- | --- | --- | --- |
| DTE / DCE | equipment roles | Data endpoint vs line-terminating physical equipment | `p0186:c01` |
| RS-232 / RS-530 / V.35 / HSSI | DTE-DCE interface examples | Physical interfaces named by source | `p0186:c01` |
| FDM / TDM | multiplexing concepts | Analog/digital primary-line examples | `p0187:c01` |
| FFT / IFFT | signal-analysis algorithms | Spectrum decomposition/reconstruction | `p0190:c01` |
| Attenuation | power metric | Loss across line | `p0194:c01`–`p0196:c01` |
| dB / dBm | units | Ratio vs absolute referenced power | `p0194:c01`–`p0197:c01` |
| Link budget | engineering calculation | Balance gains/losses vs receiver sensitivity | `p0197:c01` |
| Bandwidth | frequency characteristic | Frequency interval passed with acceptable attenuation | `p0198:c01` |
| SNR | noise metric | Signal power / noise power | `p0201:c01` |
| NEXT / FEXT | copper crosstalk metrics | Near/far-end pair interference | `p0201:c01`–`p0202:c01` |
| BER | reliability metric | Probability/rate of bit errors | `p0202:c01` |
| Capacity | data-rate metric | Maximum data rate for medium + physical coding | `p0202:c01`–`p0207:c01` |
| Shannon / Nyquist relations | theoretical limits | Relate capacity to bandwidth/SNR/states | `p0206:c01`–`p0207:c01` |
| UTP / STP | copper media | Twisted-pair variants | `p0207:c01`–`p0209:c01` |
| Coaxial / twinaxial | copper media | Coaxial variants/examples | `p0209:c01` |
| SMF / MMF | optical media | Single-/multi-mode fiber | `p0209:c01`–`p0212:c01` |
| CD / PMD | optical impairments | Chromatic / polarization-mode dispersion | `p0212:c01` |
| Structured Cabling System | infrastructure system | Standardized building/campus cabling | `p0213:c01`–`p0214:c01` |

## Operational boundary

Chapter source supports **what to measure/compare**, not **how to invoke a tool** on a particular platform.

For real troubleshooting the following remain **[Needs confirmation]**:

- switch/router/NIC model and PHY;
- transceiver type;
- cable/fiber class and length;
- TX/RX power;
- receiver thresholds;
- FEC/BER counters;
- NEXT/FEXT test results;
- negotiated physical protocol/data rate;
- cable tester/OTDR/TDR availability;
- acceptable margin and standard revision.

No operational command is invented.
