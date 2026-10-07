# Commands and tools — глава 4 (RAG-only)

**Scope:** `computer-networks-olifer-7e-ru-2026:p0108:c01` … `p0130:c01`, PDF pp. 108–130.

## Executable commands

**Исполняемые shell/network/vendor CLI commands в границе главы не обнаружены.**

Классификация v1.7:

- read-only commands: **[Not applicable]**;
- workload-generating commands: **[Not applicable]**;
- state-changing commands: **[Not applicable]**.

Не добавлять из памяти `show`, `ip`, `ss`, `tcpdump`, SNMP CLI, Telnet client syntax или RFC lookup commands: глава их не приводит.

## Source-confirmed protocols, standards and components

| Объект | Класс | Роль в главе | RAG |
| --- | --- | --- | --- |
| OSI model | reference model | Seven-layer decomposition of packet-network interaction | `p0112:c01`–`p0121:c01` |
| PDU | terminology | Generic unit exchanged by protocols of a layer | `p0115:c01` |
| Repeater / hub | network component | Source maps to physical-layer functionality | `p0119:c01` |
| LAN switch | network component | Source maps to physical + data-link layers | `p0119:c01` |
| Router | network component | Source maps to physical + data-link + network layers | `p0119:c01` |
| SNMP | management protocol | Source example of management-plane protocol | `p0119:c01`–`p0120:c01` |
| Telnet | management/application protocol example | Remote device configuration example in source | `p0119:c01`–`p0120:c01` |
| DNS | auxiliary application protocol | Name-to-IP mapping example | `p0119:c01`–`p0120:c01` |
| RIP / OSPF | routing protocols | Demonstrate difficulty of strict OSI layer placement | `p0121:c01` |
| RFC | Internet specification/document series | Open Internet standardization process | `p0124:c01` |
| ISOC / IAB / IRTF / IETF | standards ecosystem | Organizations/groups described in Internet standardization | `p0124:c01` |
| IEEE 802.3 / ISO 8802.3 | standards | Source example of Ethernet standard evolution | `p0123:c01`–`p0124:c01` |
| TCP / UDP / IP | protocol stack components | Core examples in TCP/IP mapping | `p0120:c01`–`p0126:c01` |
| QUIC | transport protocol example | Source example of a vendor-originated protocol becoming Internet standard | `p0123:c01` |
| CSMA/CA, Wi-Fi, Bluetooth, ZigBee, Thread, Wi-SUN FAN | lower-stack technologies/protocols | Examples of technologies operating below/around IP | `p0125:c01`–`p0126:c01` |

## Operational boundary

Названия protocols/tools above are **not executable instructions**. Exact versions, current standards status, command syntax, security posture and availability in any real environment: **[Needs confirmation]**.

No state-changing command is invented.
