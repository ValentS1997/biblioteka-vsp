# Commands and tools — глава 8 (RAG-only)

**Scope:** `computer-networks-olifer-7e-ru-2026:p0242:c01` … `p0267:c01`, PDF pp. 242–267.

## Executable commands

**Исполняемые shell/network/vendor CLI commands в границе главы не обнаружены.**

- read-only commands: **[Not applicable]**;
- workload-generating commands: **[Not applicable]**;
- state-changing commands: **[Not applicable]**.

Не добавлять из памяти optical transport CLI, OTN cross-connect commands, transponder/muxponder provisioning syntax, FEC/BER commands or DWDM channel commands.

## Source-confirmed blocks, protocols and equipment

| Объект | Класс | Роль | RAG |
| --- | --- | --- | --- |
| TM | transport equipment | Terminal multiplexer for point-to-point line termination | `p0244:c01` |
| ADM | transport equipment | Add/drop tributary channels on a line/ring | `p0244:c01`–`p0245:c01` |
| DXC / cross-connect | transport equipment | Switch subchannels among multiple aggregate/user interfaces | `p0245:c01` |
| Regenerator | physical equipment | Restore optical/electrical signal shape/timing | `p0245:c01` |
| PDH bit stuffing | rate-alignment mechanism | Compensate slightly mismatched plesiochronous streams | `p0250:c01`–`p0251:c01` |
| SDH virtual container/pointer | mapping mechanism | Locate/move client payload without full hierarchy demux | `p0251:c01`–`p0253:c01` |
| OPU | OTN functional block | Client mapping and rate alignment | `p0256:c01`–`p0260:c01` |
| ODU | OTN functional block | End-to-end monitoring, multiplexing and transport state | `p0256:c01`–`p0263:c01` |
| OTU | OTN functional block | Adjacent-node transport, FEC, photonic handoff | `p0256:c01`–`p0258:c01` |
| RS(255,239) | FEC code | Source-described OTU Reed–Solomon FEC | `p0258:c01` |
| GFP-F / GFP-T | client mapping/framing | Generic framing for frame-based or transparent synchronous client traffic | `p0259:c01`–`p0260:c01` |
| Tributary Slot (TS) | multiplexing resource | Byte-interleaved slot carrying lower-order ODU data | `p0261:c01`–`p0263:c01` |
| PSI | payload structure metadata | Describe slot assignment/type/tributary-port relation | `p0262:c01`–`p0263:c01` |
| ODU0 / ODU2e / ODU4 / ODUCn / ODUFlex | OTN containers | Adapt hierarchy to Ethernet/arbitrary-rate clients | `p0263:c01`–`p0265:c01` |
| GMP | mapping procedure | Flexible mapping of arbitrary-rate ODUFlex clients | `p0265:c01` |
| PM-QPSK / PM-16QAM / PM-32QAM | optical coding examples | Source examples for higher-rate optical transport | `p0264:c01`–`p0265:c01` |
| Transponder / muxponder | OTN/DWDM equipment | Point-to-point digital wrapper / aggregated client transport | `p0265:c01`–`p0267:c01` |
| OTN cross-connect / switching | transport switching | Transit switching of tributary/aggregate OTN data | `p0267:c01` |

## Operational boundary

For a real OTN system these remain **[Needs confirmation]**:

- vendor/platform/software release;
- client signal type/rate;
- OPU/ODU/OTU container mapping;
- tributary-slot/PSI assignment;
- cross-connect path;
- OTU/FEC error counters and alarms;
- optical wavelength/ROADM path;
- supported protection/restoration mode;
- exact standard revision and supported hierarchy;
- provisioning and rollback syntax.

No command is invented.
