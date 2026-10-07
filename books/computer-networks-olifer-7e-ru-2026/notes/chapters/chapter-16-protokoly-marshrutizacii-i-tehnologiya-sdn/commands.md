# Commands and tools — глава 16 (RAG-only)

**Scope:** `computer-networks-olifer-7e-ru-2026:p0472:c01` … `p0513:c01`, PDF pp. 472–513.

## Executable commands

**Vendor-neutral executable CLI commands in the chapter were not found.**

Do not inject from model memory:

- `show ip route` / `ip route`;
- RIP/OSPF/BGP configuration syntax;
- multicast/PIM/IGMP diagnostics;
- OpenFlow controller commands;
- P4 compiler/runtime commands;
- NFV/MANO/OSM CLI.

## Source-confirmed protocols and control objects

| Object | Role | RAG |
| --- | --- | --- |
| RIP / RIPv1 / RIPv2 | Distance-vector IGP examples | `p0477:c01`–`p0485:c01` |
| Split horizon / triggered update / hold-down | RIP stale-route mitigations | `p0484:c01`–`p0485:c01` |
| OSPF | Link-state IGP | `p0485:c01`–`p0490:c01` |
| HELLO / LSA / LSDB / Dijkstra | OSPF neighbor/topology/SPF chain | `p0485:c01`–`p0489:c01` |
| DR / ABR / area 0 | OSPF transit/area scaling roles | `p0487:c01`–`p0490:c01` |
| IS-IS | Link-state routing example | `p0476:c01`, `p0490:c01` |
| Route redistribution | Exchange route knowledge between routing processes | `p0490:c01`–`p0495:c01` |
| BGP / eBGP / iBGP | Path-vector policy routing between/within AS | `p0492:c01`–`p0498:c01` |
| TCP/179 | BGP session transport in source description | `p0494:c01` |
| UPDATE / AS path / next hop | BGP reachability/path information | `p0494:c01`–`p0497:c01` |
| Route Reflector | iBGP session-scaling mechanism | `p0497:c01` |
| IGMP | Host-to-router multicast membership | `p0500:c01`–`p0502:c01` |
| DVMRP / MOSPF / PIM | Multicast-routing examples | `p0500:c01` |
| Dense / Sparse mode / rendezvous point | Multicast-tree models | `p0502:c01`–`p0503:c01` |
| RPF | Reverse-path check before multicast replication | `p0503:c01`–`p0504:c01` |
| SDN controller | Centralized programmable control element | `p0504:c01`–`p0507:c01` |
| OpenFlow | Controller↔forwarding-device rule protocol/model | `p0507:c01`–`p0508:c01` |
| P4 / P4 runtime text | Programmable packet-processing pipeline | `p0509:c01`–`p0510:c01` |
| NFV / VNF / NFV MANO | Software network functions and orchestration | `p0510:c01`–`p0513:c01` |

## Source pseudostructures — not executable CLI

### BGP route representation

The chapter gives the conceptual form:

```text
BGP Route = AS_Path ; NextHop ; Network/Prefix
```

This is a data model/explanatory notation, not configuration syntax.

### OpenFlow rule structure

The source presents rules as three logical components:

```text
match conditions
actions
counters
```

A source example matches ingress port + VLAN + source/destination IP + TCP destination port, then illustrates actions such as output-port selection, VLAN rewrite and destination-MAC rewrite.

**Important:** the source's condition example contains an internal destination-port mismatch between the printed condition and surrounding prose; see `source-findings.md`.

## Operational boundary

Real routing/SDN/NFV state remains **[Needs confirmation]**:

- routing-table/RIB/FIB contents and route preference;
- neighbor/adjacency/session state;
- OSPF LSDB/areas;
- BGP policy, prefixes, AS path and RR topology;
- IGMP/PIM tree and RPF state;
- controller reachability and installed OpenFlow/P4 rules;
- P4 pipeline version;
- VNF instance/chain/MANO health.

No vendor syntax is invented.
