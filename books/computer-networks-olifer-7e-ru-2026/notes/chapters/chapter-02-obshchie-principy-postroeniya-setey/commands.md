# Commands and tools — глава 2 (RAG-only)

**Scope:** `computer-networks-olifer-7e-ru-2026:p0046:c01` … `p0080:c01`, PDF pp. 46–80.

## Executable commands

**Исполняемые shell/network/vendor CLI команды в границе главы не обнаружены.**

Классификация v1.7:

- read-only commands: **[Not applicable]**;
- workload-generating commands: **[Not applicable]**;
- state-changing commands: **[Not applicable]**.

Не добавлять из памяти `ip addr`, `ip route`, `arp`, `ping`, `traceroute`, `ethtool`, switch/router CLI или packet capture commands: источник их не приводит.

## Source-confirmed protocols, mechanisms and components

| Объект | Класс | Роль в главе | RAG |
| --- | --- | --- | --- |
| NIC / network adapter + driver | hardware + software | Physical transfer between computers | `p0047:c01`–`p0050:c01` |
| Client / server | software roles | Reusable access to remote resource | `p0051:c01`–`p0052:c01` |
| HTTP | application protocol | Example protocol of web service | `p0052:c01`–`p0053:c01` |
| Network OS transport modules | software mechanism | Message formation, packet/frame split, naming/address tasks | `p0053:c01`–`p0055:c01` |
| ARP | address-resolution protocol | Distributed mapping from hierarchical numeric address to hardware address | `p0067:c01` |
| TCP/UDP port numbers | process addressing | Address a process within a computer | `p0067:c01` |
| Switching/routing/forwarding tables | forwarding state | Map flow descriptor to outgoing interface/next node | `p0070:c01`–`p0074:c01` |
| Multiplexer/demultiplexer | switching specialization | Combine/split flows | `p0075:c01`–`p0076:c01` |
| Arbiter | shared-medium control | Centralized access decision to common medium | `p0077:c01`–`p0078:c01` |

## Source-described state change without executable syntax

`p0072:c01` states that an administrator can manually fix a route or add an entry to a switching table.

- **Class:** conceptually state-changing.
- **Exact command/syntax/platform:** **[Needs confirmation]**.
- **Effect:** changes the path/forwarding decision for matching traffic.
- **Risk:** source does not give a concrete operational risk/rollback procedure for a real platform.
- **Verification:** **[Needs confirmation]**.
- **Rollback:** **[Needs confirmation]**.

No command is invented to fill this gap.
