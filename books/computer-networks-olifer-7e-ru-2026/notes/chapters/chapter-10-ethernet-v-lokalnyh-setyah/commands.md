# Commands and tools — глава 10 (RAG-only)

**Scope:** `computer-networks-olifer-7e-ru-2026:p0287:c01` … `p0325:c01`, PDF pp. 287–325.

## Executable commands

**Исполняемые shell/network/vendor CLI commands в границе главы не обнаружены.**

- read-only commands: **[Not applicable]**;
- workload-generating commands: **[Not applicable]**;
- state-changing commands: **[Not applicable]**.

Не добавлять из памяти `ip link`, `ethtool`, `bridge fdb`, switch `show mac address-table`, span/mirror commands or PHY/FEC diagnostics.

## Source-confirmed mechanisms, standards and components

| Объект | Класс | Роль | RAG |
| --- | --- | --- | --- |
| IEEE 802.3 | Ethernet standard family | MAC/PHY Ethernet definitions | `p0290:c01` onward |
| IEEE 802.2 / LLC | link-layer service | Upper interface/service modes in source history | `p0290:c01`–`p0291:c01` |
| Ethernet II / DIX frame | frame format | DA/SA/EtherType/data/FCS | `p0292:c01`–`p0293:c01` |
| CRC-32 / FCS | error detection | Detect damaged Ethernet frame | `p0293:c01` |
| CSMA/CD | medium access | Shared half-duplex access/collision handling | `p0293:c01`–`p0296:c01` |
| Hub / repeater | L1 component | Repeat bits; preserve shared collision domain | `p0297:c01`–`p0298:c01` |
| IEEE 802.1D transparent bridge | switching algorithm | Learn source MAC; forward/filter/flood | `p0299:c01`–`p0306:c01` |
| MAC forwarding table | switch state | Dynamic/static MAC→port state | `p0301:c01`–`p0304:c01` |
| STA/STP reference | loop-control pointer | Chapter 10 names it; detailed in chapter 11 | `p0306:c01` |
| ASIC / FPGA / NPU | switch processing | Hardware/software processing implementations | `p0310:c01`–`p0311:c01` |
| Switch matrix / shared bus / shared memory | switch fabric models | Internal frame transfer architectures | `p0311:c01` |
| ONIE / Bare Metal / White Box | open switch model | Decouple hardware and network OS | `p0312:c01` |
| RS / PCS / PMA / PMD / MDI | Ethernet PHY blocks | Modular high-speed physical architecture | `p0313:c01`–`p0314:c01` |
| Autonegotiation / FLP | link setup mechanism | Agree speed/duplex among supported modes | `p0314:c01` |
| 4B/5B / MLT-3 | Fast Ethernet coding | 100Base-FX/TX source examples | `p0315:c01`–`p0316:c01` |
| 8B/10B / 4D-PAM5 | Gigabit Ethernet coding | Fiber/copper Gigabit source examples | `p0317:c01`–`p0319:c01` |
| 64B/66B | high-speed coding | 10G/40G/100G source use | `p0319:c01`–`p0321:c01` |
| PAM4 + Reed-Solomon FEC | high-speed PHY | 200/400G and later scaling | `p0321:c01`–`p0324:c01` |
| CWDM / coherent Ethernet-DWDM | optical PHY examples | Parallel wavelengths / long-reach source examples | `p0323:c01`–`p0325:c01` |

## Operational boundary

For a real Ethernet incident these remain **[Needs confirmation]**:

- switch/NIC model and software/firmware;
- port admin/oper state;
- negotiated speed/duplex;
- FDB/MAC table;
- broadcast/unknown-unicast counters;
- loop/STP state;
- queue/drop counters;
- transceiver/media type;
- lane/FEC/BER/optical diagnostics;
- exact standard revision.

No command is invented.
