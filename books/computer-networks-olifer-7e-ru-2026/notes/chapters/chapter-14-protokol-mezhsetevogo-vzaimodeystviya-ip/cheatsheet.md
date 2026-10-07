# Cheatsheet — глава 14: протокол IP

## Symptom / problem framing

**Проблема:** IPv4 incident should be decomposed into route selection, next-hop reachability, MTU/fragmentation, ICMP feedback and optional QoS policy. A “packet does not arrive” symptom does not identify which mechanism failed. `p0399:c01`–`p0441:c01`.

## Baseline / context

| Mechanism | Source role |
| --- | --- |
| IPv4 header | Carries forwarding, lifetime, fragmentation and protocol metadata |
| Routing table | Destination/prefix → next hop + outgoing interface |
| Longest-prefix match | Choose most specific matching route |
| Default route | Least-specific fallback `0.0.0.0/0` |
| MTU / fragmentation | Adapt packet to smaller next-link frame capacity |
| ICMP | Report/diagnose delivery conditions |
| ping | ICMP echo-based reachability/RTT probe |
| traceroute/tracert | TTL-expiry based hop/path probe |
| DiffServ | Per-hop class-based QoS treatment |

## Read-only checks

1. Capture destination IPv4 address and expected source/interface.
2. Inspect the routing table entry that should match the destination.
3. Verify whether a more-specific route overrides the expected aggregate/default route.
4. Confirm next-hop IP and outgoing interface.
5. Verify next-hop local delivery separately (ARP/link state from chapter 13).
6. Confirm whether the destination is directly connected, static, dynamic or default-routed.
7. Check packet TTL/hop-limit-like lifetime symptom: is failure caused by a loop or excessive path length?
8. Check interface/path MTU and whether DF is set.
9. If packet is dropped, note any ICMP type/code returned.
10. Compare `ping` reachability with `traceroute/tracert` path evidence.
11. If QoS is suspected, inspect DS/DSCP marking and class treatment.
12. Real route table, MTU, ICMP filtering and QoS policy: **[Needs confirmation]**.

## Interpretation

- **Default route matching is expected, not evidence of correctness.** `0.0.0.0/0` matches everything; a more-specific prefix should win when present. `p0421:c01`.
- **Several matches are normal.** Longest-prefix match resolves them by choosing the most specific route.
- **A routing-table entry does not prove next-hop reachability.** The next hop still needs working link/local-address resolution.
- **Ping success is not a proof that every application works.** It demonstrates successful ICMP echo exchange on that tested path/time.
- **Ping failure is not automatically proof that the destination is down.** The chapter does not provide a universal interpretation rule for filtered ICMP; real policy is **[Needs confirmation]**.
- **Traceroute RTT is source→hop→source round-trip time, not delay between adjacent hops.** `p0433:c01`–`p0434:c01`.
- **Fragmentation is path/MTU adaptation, not reliability.** Losing one fragment causes the destination to discard the incomplete reassembly set after timeout.
- **ICMP reports; it does not retransmit.** Reliability remains outside IP/ICMP.
- **DiffServ marking is only a classification signal.** Actual queueing/policing behavior depends on router policy.

## Next action

For an IPv4 path incident:

**route lookup → longest-prefix/default decision → next-hop/interface → ARP/link reachability → TTL/loop evidence → MTU/DF/fragmentation → ICMP type/code → ping/traceroute correlation → DSCP/QoS only if relevant**.

## Modifying action

Source-described state-changing actions include:

- add/remove static routes;
- change default route;
- change interface addressing/masks;
- adjust MTU or DF-related application behavior;
- change DS/DSCP classification/QoS policy.

Exact command syntax and rollback are **[Needs confirmation]**.

## Verification / acceptance checks

Глава усвоена, если можно:

- identify key IPv4 header fields and explain TTL/protocol/checksum roles;
- explain destination prefix, next hop and outgoing interface;
- explain connected/static/dynamic/default route sources;
- perform longest-prefix-match reasoning manually;
- explain VLSM and CIDR aggregation;
- explain MTU, DF/MF, fragment offset and destination reassembly;
- distinguish IP failure from ICMP reporting;
- explain how traceroute and ping use ICMP;
- describe Mobile IPv4 home/foreign agent + tunnel model;
- contrast IntServ/RSVP with DiffServ/DSCP/PHB.

## Rollback

For chapter artifacts — **[Not applicable]**. For production routing/QoS changes rollback must restore prior routes, MTU, interface state and classification/policy. Exact procedure: **[Needs confirmation]**.
