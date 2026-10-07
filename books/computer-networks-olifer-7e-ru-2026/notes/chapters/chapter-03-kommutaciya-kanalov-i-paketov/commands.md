# Commands and tools — глава 3 (RAG-only)

**Scope:** `computer-networks-olifer-7e-ru-2026:p0081:c01` … `p0107:c01`, PDF pp. 81–107.

## Executable commands

**Исполняемые shell/network/vendor CLI команды в границе главы не обнаружены.**

Классификация v1.7:

- read-only commands: **[Not applicable]**;
- workload-generating commands: **[Not applicable]**;
- state-changing commands: **[Not applicable]**.

Не добавлять из памяти `ping`, `traceroute`, `ip route`, switch/router CLI, QoS commands или packet-capture commands: источник их не приводит.

## Source-confirmed technologies and mechanisms

| Объект | Класс | Роль в главе | RAG |
| --- | --- | --- | --- |
| Circuit switching | switching model | End-to-end reservation of elementary channels | `p0081:c01`–`p0088:c01` |
| TDM / frequency division | multiplexing concepts | Ways to define/share elementary channel capacity | `p0082:c01`–`p0083:c01` |
| Packet switching | switching model | Dynamic sharing using packets | `p0089:c01`–`p0104:c01` |
| Store-and-forward | packet-switch mechanism | Buffer full packet before processing/forwarding | `p0092:c01` |
| Datagram forwarding | packet-forwarding method | Independent packet processing, best effort | `p0093:c01`–`p0094:c01` |
| Logical connection | connection-state method | Endpoint agreement on exchange parameters | `p0095:c01`–`p0096:c01` |
| Virtual circuit | packet-forwarding method | Fixed path with per-flow label | `p0097:c01`–`p0098:c01` |
| IP | datagram protocol example | Internet inter-network packet forwarding example | `p0098:c01` |
| TCP | logical-connection example | Reliable endpoint delivery without fixed route | `p0098:c01` |
| MPLS | virtual-circuit example | Label-based virtual channels inside Internet | `p0098:c01` |
| ATM | packet technology example | Fixed-size cells | `p0090:c01` |
| Ethernet | packet technology example | Datagram frames, MAC addressing, checksum, queues | `p0105:c01`–`p0107:c01` |

## Source-described state transitions without executable syntax

Глава описывает следующие state transitions:

- establishment / teardown of a circuit;
- establishment / teardown of a logical connection;
- setup / teardown of a virtual circuit;
- creation of local switching-table entries during setup.

Для всех:

- exact command/syntax/platform: **[Needs confirmation]**;
- operational risk on a real system: **[Needs confirmation]**;
- verification command: **[Needs confirmation]**;
- rollback command: **[Needs confirmation]**.

No command is invented to fill these gaps.
