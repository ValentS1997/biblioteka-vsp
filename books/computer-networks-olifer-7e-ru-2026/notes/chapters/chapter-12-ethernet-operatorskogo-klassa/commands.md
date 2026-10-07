# Commands and tools — глава 12 (RAG-only)

**Scope:** `computer-networks-olifer-7e-ru-2026:p0351:c01` … `p0360:c01`, PDF pp. 351–360.

## Executable commands

**Vendor-neutral executable CLI commands are not present.**

Do not add from model memory:

- CFM/MEP/MIP configuration syntax;
- Y.1731 test commands;
- Ethernet OAM loopback commands;
- E-LMI queries;
- Q-in-Q / S-VLAN commands;
- provider-bridge or PBB provisioning syntax.

## Source-confirmed OAM and service mechanisms

| Object | Class | Role | RAG |
| --- | --- | --- | --- |
| CE / UNI | service boundary | Customer equipment ↔ provider Ethernet interface | `p0351:c01` |
| CFM | Ethernet OAM | Monitor service connectivity/faults | `p0354:c01`–`p0357:c01` |
| MEP | maintenance endpoint | Generate/receive maintenance messages | `p0354:c01`–`p0357:c01` |
| MIP | maintenance intermediate point | Observe transit CFM traffic / fault localization | `p0354:c01`–`p0356:c01` |
| CCM | continuity message | Periodic active continuity check | `p0354:c01`–`p0356:c01` |
| Maintenance level/domain | OAM hierarchy | Separate operator/provider/customer monitoring scopes | `p0356:c01`–`p0357:c01` |
| Y.1731 | performance OAM | One-way delay, delay variation, frame-loss measurement | `p0357:c01` |
| Remote loopback | physical-link test | Return received frames for physical connection analysis | `p0357:c01` |
| E-LMI | service management interface | Query service status/VLAN mapping/bandwidth info | `p0358:c01` |
| Provider Bridge | service encapsulation | Separate customer/provider VLAN namespaces | `p0358:c01`–`p0360:c01` |
| C-VID / S-VID | VLAN identifiers | Customer and provider service VLAN IDs | `p0358:c01`–`p0359:c01` |
| Q-in-Q | encapsulation | Push S-VID outside existing customer VLAN tag | `p0358:c01`–`p0359:c01` |
| PBB | provider backbone encapsulation | Stronger address-space separation in source | `p0360:c01` |

## Safety classification

### Read-only / passive in operational intent

- inspect existing service/MEP/MIP/VLAN mapping;
- inspect received CCM/statistics;
- read E-LMI service information.

Actual commands: **[Needs confirmation]**.

### Active but normally non-disruptive measurement

- CFM CCM generation;
- Y.1731 delay/loss measurement.

These generate protocol traffic; exact load/timing is platform-specific.

### Disruptive test

**Remote physical Ethernet loopback** is explicitly described by the source as disrupting normal connection operation.

Required before use:

1. maintenance window;
2. known affected service/interface;
3. explicit rollback/exit method;
4. post-test service verification.

Executable syntax: **[Needs confirmation]**.

## Source-described state changes without executable syntax

The chapter conceptually permits:

- configuring maintenance domains/levels;
- creating MEP/MIP points;
- enabling service measurements;
- configuring C-VID→S-VID service mapping;
- provider edge push/pop of S-tag;
- provider-bridge/PBB service construction.

No vendor command is invented.
