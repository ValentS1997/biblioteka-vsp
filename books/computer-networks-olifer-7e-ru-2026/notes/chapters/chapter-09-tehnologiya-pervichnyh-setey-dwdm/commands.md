# Commands and tools — глава 9 (RAG-only)

**Scope:** `computer-networks-olifer-7e-ru-2026:p0268:c01` … `p0281:c01`, PDF pp. 268–281.

## Executable commands

**Исполняемые shell/network/vendor CLI commands в границе главы не обнаружены.**

- read-only commands: **[Not applicable]**;
- workload-generating commands: **[Not applicable]**;
- state-changing commands: **[Not applicable]**.

Не добавлять из памяти coherent-optics CLI, transponder/ROADM/WSS provisioning syntax, optical power/OSNR commands or vendor alarms.

## Source-confirmed components, standards and mechanisms

| Объект | Класс | Роль | RAG |
| --- | --- | --- | --- |
| DWDM | optical multiplexing | Multiple spectral channels in one fiber | `p0268:c01`–`p0272:c01` |
| CWDM | optical multiplexing comparison | Coarser spectral spacing | `p0271:c01` |
| ITU-T G.694.1 | frequency-plan reference | Fixed/flexible DWDM grid in source | `p0271:c01`–`p0272:c01` |
| Dispersion / interference / diffraction / reflection | optical effects | Basis for mux/demux/switching and impairment mechanisms | `p0269:c01`–`p0270:c01` |
| T-MUX | optical transport equipment | Terminal DWDM multiplexer | `p0272:c01`–`p0273:c01` |
| Transponder | client/wavelength adapter | O-E-O wavelength conversion | `p0273:c01` |
| Thin-film filter | optical filter | Fixed wavelength selection in small-channel mux/OADM | `p0273:c01`–`p0276:c01` |
| Diffraction phase/waveguide structure | optical mux/demux | Scalable wavelength separation/combination | `p0274:c01`–`p0275:c01` |
| OADM | optical add/drop | Add/drop configured wavelength | `p0275:c01`–`p0276:c01` |
| EDFA | optical amplifier | Erbium-doped optical amplification | `p0276:c01` |
| Raman amplifier | optical amplifier | Distributed/broader-band amplification example | `p0276:c01` |
| G.652 / G.655 fiber | fiber references | Source context for dispersion behavior | `p0277:c01` |
| OXC | optical cross-connect | Mesh spectral-channel switching | `p0277:c01`–`p0278:c01` |
| ROADM | reconfigurable OXC | Remote optical add/drop/cross-connect | `p0278:c01`–`p0281:c01` |
| WSS | wavelength-selective switch | Select wavelengths from inputs and send to output | `p0279:c01`–`p0280:c01` |
| Power Splitter | optical distribution | Feed input composite signals to WSS blocks | `p0280:c01` |
| MEMS mirrors | switching implementation example | Direct selected wavelengths to output waveguides | `p0281:c01` |

## Operational boundary

For a real DWDM path these remain **[Needs confirmation]**:

- vendor/platform/software;
- frequency grid and slot width;
- exact wavelength/channel assignment;
- transponder client and line modes;
- TX/RX optical power, OSNR and receiver thresholds;
- amplifier type/gain/noise state;
- dispersion budget/compensation method;
- ROADM degree/bank/port structure;
- colorless/directionless capability;
- WSS cross-connect table;
- alarms/BER/FEC state;
- rollback syntax.

No operational command is invented.
