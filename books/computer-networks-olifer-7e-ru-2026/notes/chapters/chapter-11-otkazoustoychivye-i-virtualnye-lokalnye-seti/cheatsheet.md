# Cheatsheet — глава 11: отказоустойчивые и виртуальные локальные сети

## Symptom / problem framing

**Проблема:** L2 redundancy without control creates loops; a single spanning tree can waste capacity; flat switching propagates broadcast; manual VLAN/LAG state can become inconsistent. The chapter separates these failure domains into **loop control, link aggregation, segmentation and multi-tree balancing**. `p0326:c01`–`p0350:c01`.

## Baseline / context

| Mechanism | What it solves | Source trade-off |
| --- | --- | --- |
| STP | Remove active L2 loops | Redundant links are blocked |
| RSTP | Faster topology reconvergence | Still tree-based forwarding |
| LAG/LACP | Parallel active links between two systems | Scope is the local aggregate, not whole topology |
| VLAN | Separate L2/broadcast domains logically | Inter-VLAN traffic needs L3 |
| MSTP | Several trees for VLAN groups | Requires consistent tree/VLAN mapping |
| MAC access filter | Additional L2 policy | Limited visibility and broadcast handling |

## Read-only checks

1. Is the physical topology redundant? Which links form potential **L2 loops**?
2. Which switch is intended/actual root bridge? Root selection evidence: **[Needs confirmation]**.
3. Which ports are root/designated/alternate/backup/edge and in what forwarding state?
4. Are BPDU/control frames received where expected? Exact counters/timers: **[Needs confirmation]**.
5. Is a redundant link intentionally blocked by STP or unexpectedly down?
6. Are parallel links independent STP edges or members of one **LAG**?
7. If LAG: which physical members are active, and is LACP negotiating/monitoring them?
8. Which VLAN IDs are active on each switch?
9. Is the port model access, trunk or flexible tagged/untagged?
10. Are required VLANs allowed on the inter-switch link?
11. Is the same MAC learned in unexpected VLAN/port locations?
12. Which spanning-tree instance carries each VLAN under MSTP?
13. Is inter-VLAN connectivity expected? If yes, the required L3 gateway/routing state is **[Needs confirmation]**.

## Interpretation

- **Blocked STP port is not automatically a fault.** Blocking/discarding redundant paths is the mechanism that prevents loops. `p0326:c01`–`p0332:c01`.
- **A loop symptom can masquerade as “switch instability”.** Frame duplication, broadcast amplification and unstable MAC learning are consequences of uncontrolled redundant paths.
- **RSTP improves recovery, not topology utilization.** It shortens reconvergence but still selects a loop-free tree. `p0331:c01`–`p0332:c01`.
- **LAG is not a replacement for spanning-tree control across the whole LAN.** The source explicitly says aggregation only understands links between its two endpoint systems; the aggregate must still participate in STA as one link. `p0335:c01`–`p0338:c01`.
- **VLAN isolation is L2-complete in the source model.** A frame does not cross VLANs just because the destination MAC exists; L3 routing is required. `p0339:c01`–`p0341:c01`.
- **Tagged/untagged mismatch is a classification problem before it is a routing problem.** First verify how the ingress port assigns VLAN identity and how the trunk carries it. `p0343:c01`–`p0346:c01`.
- **MSTP balances topology by VLAN groups, not per packet.** Different VLANs can have different active trees/roots. `p0348:c01`–`p0349:c01`.

## Next action

For an L2 LAN incident use:

**map physical redundancy → verify STP/RSTP root and port roles → verify LAG membership/LACP → verify VLAN ingress classification → verify tagged trunk propagation → verify per-VLAN MAC learning → verify MSTP instance mapping → only then move to L3 inter-VLAN routing**.

Exact commands depend on vendor/platform and are not supplied by the chapter.

## Modifying action

The chapter conceptually describes state changes such as:

- STP bridge priority/root influence;
- edge/port roles;
- static/dynamic LAG membership;
- MAC access filters;
- VLAN creation and port membership;
- trunk allowed VLANs;
- MSTP tree/VLAN mapping.

Executable syntax, safe ordering, before-state capture and rollback are **[Needs confirmation]**.

## Verification / acceptance checks

Глава усвоена, если можно:

- explain why transparent bridging needs an active tree;
- describe root bridge / root port / designated port selection;
- distinguish STP from RSTP roles/convergence;
- compare STP redundancy with LAG redundancy;
- explain LAS/LAG/LACP at a conceptual level;
- define VLAN as a broadcast/L2 isolation domain;
- explain the 802.1Q tagging purpose;
- distinguish access vs trunk behavior;
- explain VTP/GVRP/MVRP roles without treating them as universal requirements;
- explain how MSTP maps VLAN groups to different trees;
- name the main scaling limits of an all-L2 network.

## Rollback

For chapter artifacts — **[Not applicable]**. For production L2 changes rollback should restore previous bridge priority/port state, LAG membership, VLAN membership/tagging and MSTP mapping; exact procedure: **[Needs confirmation]**.
