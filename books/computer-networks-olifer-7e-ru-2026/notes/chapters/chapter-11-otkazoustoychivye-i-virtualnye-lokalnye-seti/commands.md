# Commands and tools — глава 11 (RAG-only)

**Scope:** `computer-networks-olifer-7e-ru-2026:p0326:c01` … `p0350:c01`, PDF pp. 326–350.

## Executable commands

Vendor-neutral executable CLI commands are **not present**.

The chapter contains a **generic access-list example**, not a platform-specific command set:

```text
10 permit MAC-C1 MAC-S1
20 permit MAC-C3 MAC-S1
30 deny any any
```

Source says this list is evaluated top-to-bottom and applied to a port/direction; the example applies it to outbound traffic toward server S1. Exact syntax for any real switch is **[Needs confirmation]**.

## Source-confirmed protocols, standards and mechanisms

| Object | Class | Role | RAG |
| --- | --- | --- | --- |
| STA / STP | L2 loop-control algorithm/protocol | Build active spanning tree | `p0326:c01`–`p0331:c01` |
| BPDU | STP control frame | Carry bridge/port/root/path information | `p0328:c01`–`p0330:c01` |
| RSTP / IEEE 802.1w source history | faster STP variant | Faster failure detection/convergence | `p0331:c01`–`p0332:c01` |
| MAC access list | L2 policy | Permit/deny based on frame fields | `p0332:c01`–`p0334:c01` |
| Link Aggregation / LAG | link mechanism | Multiple physical links as one logical channel | `p0334:c01`–`p0338:c01` |
| LAS | Ethernet sublayer | Aggregate/distribute frames below client protocol | `p0336:c01`–`p0338:c01` |
| LACP | aggregation control protocol | Form and monitor dynamic LAG membership | `p0338:c01`–`p0339:c01` |
| VLAN | L2 segmentation | Isolate unicast/group/broadcast traffic between groups | `p0339:c01`–`p0343:c01` |
| IEEE 802.1Q tag | VLAN frame marking | Carry VID/priority information across switches | `p0343:c01`–`p0344:c01` |
| EtherType 0x8100 | tag indicator in source | Identify tagged Ethernet frame | `p0344:c01` |
| Access link/port | VLAN edge | Untagged end-host-facing membership | `p0344:c01`–`p0346:c01` |
| Trunk | VLAN inter-switch link | Carry multiple VLANs with tags | `p0344:c01`–`p0346:c01` |
| VTP | Cisco-specific VLAN protocol | Propagate active VLAN information | `p0347:c01` |
| GARP / GVRP / GMRP | IEEE registration family in source | Register VLAN/multicast attributes | `p0347:c01`–`p0348:c01` |
| MRP / MVRP / MMRP | replacement registration family in source | Reduce service traffic/convergence delay | `p0348:c01` |
| MSTP | multi-tree loop-control | Map VLAN groups to separate spanning trees | `p0348:c01`–`p0349:c01` |

## Source-described state changes without executable syntax

The chapter says an administrator can change/configure:

- STP bridge priority and edge-link status;
- user filters/access lists and their port/direction attachment;
- static LAG membership or dynamic LACP behavior;
- VLAN creation and VID;
- access/trunk/flexible-port membership;
- selective VLAN carriage on a trunk;
- VTP/GVRP/MVRP-related VLAN distribution;
- MSTP priorities and VLAN-to-tree assignment.

For real devices:

- current config: **[Needs confirmation]**;
- command syntax: **[Needs confirmation]**;
- change order: **[Needs confirmation]**;
- verification: **[Needs confirmation]**;
- rollback: **[Needs confirmation]**.

No vendor syntax is invented.
