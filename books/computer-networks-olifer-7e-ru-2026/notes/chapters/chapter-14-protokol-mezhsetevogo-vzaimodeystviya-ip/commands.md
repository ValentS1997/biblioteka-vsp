# Commands and tools — глава 14 (RAG-only)

**Scope:** `computer-networks-olifer-7e-ru-2026:p0399:c01` … `p0441:c01`, PDF pp. 399–441.

## Executable/source-named utilities

### `route`

`p0412:c01` states that an administrator can create static routing-table entries with a system utility such as `route` on Unix/Windows.

- Exact syntax: **not supplied by the chapter**.
- Effect: state-changing.
- Platform/version semantics: **[Needs confirmation]**.

Do not synthesize route-add/delete commands from model memory.

### `traceroute` / `tracert`

`p0432:c01`–`p0433:c01` names Unix `traceroute` and Windows `tracert` and explains the TTL/ICMP method.

- The source shows output, but not a canonical invocation syntax to preserve as platform-neutral.
- Diagnostic intent: read-only from configuration perspective, but it generates probe traffic.

### `ping`

`p0434:c01`–`p0435:c01` describes ICMP echo request/reply and shows an example invocation line beginning with `ping` followed by a hostname. The hostname text is OCR-ambiguous in RAG.

- Utility behavior: sends active ICMP probes and reports replies/loss/RTT.
- Exact target from the example is not normalized because of OCR ambiguity.
- Workload: active diagnostic traffic, normally low volume in the source example.

## Source-confirmed protocols/mechanisms

| Object | Role | RAG |
| --- | --- | --- |
| IPv4 | Connectionless best-effort internetwork packet delivery | `p0399:c01`–`p0402:c01` |
| Routing table | Destination/prefix → next hop/output interface | `p0402:c01`–`p0425:c01` |
| Longest-prefix match | Most-specific matching route wins | `p0420:c01`–`p0421:c01` |
| Default route | Least-specific `0.0.0.0/0` fallback | `p0420:c01`–`p0421:c01` |
| RIP / OSPF | Dynamic-route sources/examples | `p0411:c01`–`p0412:c01`, `p0424:c01` |
| CIDR | Prefix aggregation / routing-table reduction | `p0424:c01`–`p0425:c01` |
| MTU | Maximum packet payload constraint of next-link technology | `p0425:c01`–`p0428:c01` |
| DF / MF / fragment offset / identification | IPv4 fragmentation/reassembly metadata | `p0426:c01`–`p0429:c01` |
| ICMP | Error/reporting and query-response support | `p0429:c01`–`p0435:c01` |
| Mobile IPv4 | Home/foreign agent + care-of/tunnel mobility model | `p0435:c01`–`p0438:c01` |
| IntServ / RSVP | Per-flow resource-reservation QoS model | `p0438:c01`–`p0439:c01` |
| DiffServ / DSCP / PHB | Aggregated class-based per-hop QoS | `p0439:c01`–`p0441:c01` |

## Operational boundary

For a real incident these remain **[Needs confirmation]**:

- OS/router platform and release;
- actual routing table and route provenance;
- current next-hop/interface state;
- ARP/link state;
- interface/path MTU;
- DF behavior of the tested flow;
- ICMP filtering/rate limiting;
- actual DSCP markings and queue/policer configuration;
- dynamic-routing protocol state.

No platform syntax is invented.
