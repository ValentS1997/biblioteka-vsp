# Cheatsheet — глава 16: routing, SDN and NFV

## Symptom / problem framing

**Проблема:** routing incident must first be split into control-plane state, forwarding state and policy. For multicast add membership/tree/RPF; for SDN add controller/rule distribution; for NFV add VNF/service-chain lifecycle. `p0472:c01`–`p0513:c01`.

## Baseline / context

| Mechanism | Source model |
| --- | --- |
| RIP | Distance vector; hop-oriented metric; periodic neighbor advertisements |
| OSPF | Link state; HELLO + LSA + LSDB + Dijkstra |
| BGP | Policy + path vector between/within autonomous systems |
| IGMP | Local host membership signaling to multicast router |
| Multicast routing | Build distribution trees; RPF checks reverse path |
| SDN | Separate control logic from forwarding devices |
| OpenFlow | Match/action/counter rules programmed by controller |
| P4 | Programmable packet-processing architecture |
| NFV | Network functions as software VNFs on general-purpose infrastructure |

## Read-only checks

1. What routing protocol supplied the route: connected/static/RIP/OSPF/BGP/other?
2. Is the route absent, stale, less preferred or overridden by another source?
3. Is the failure local to one router or a convergence inconsistency across routers?
4. For RIP: neighbor advertisements, metric and route age/invalid state?
5. For OSPF: neighbor/HELLO state, LSDB consistency, LSA propagation, area/ABR scope?
6. For BGP: configured peer, session state, accepted/advertised prefix and AS path?
7. Is route redistribution involved between protocols?
8. For multicast: group membership, expected tree, dense/sparse model and RPF result?
9. For SDN: controller reachability, installed match/action rule and relevant counters?
10. For P4: expected pipeline/architecture plus runtime rules?
11. For NFV: VNF instances, service-chain order and orchestrator lifecycle state?
12. Real protocol/database/controller/VNF state: **[Needs confirmation]**.

## Interpretation

- **Forwarding-table failure is not automatically a routing-protocol failure.** First establish which control-plane source should have produced the route.
- **Convergence is a temporary consistency problem.** During convergence different routers can legitimately hold different transient views.
- **RIP knows distances, not full topology.** That explains count-to-infinity and why split horizon/triggered updates/hold-down are mitigations rather than a new routing model.
- **OSPF knows an area topology through LSDB.** Route calculation is local from synchronized topology state.
- **BGP path choice is policy-driven in the source model.** A longer AS path can still be selected if policy says so.
- **iBGP full mesh is a control-plane propagation rule, not a data-plane topology requirement.** Route reflectors reduce session scaling pressure.
- **IGMP membership does not prove multicast forwarding end to end.** Multicast routers still need a correct distribution tree and successful RPF.
- **RPF checks the path back toward source, not the receiver.**
- **SDN controller success does not prove a device installed the intended rule.** Validate programmed rule/counters on the forwarding element.
- **NFV service failure may be orchestration/placement/chain state even when the underlay network is healthy.**

## Next action

For unicast routing:

**identify route source → verify neighbor/session state → verify advertised/learned prefix → compare protocol database to installed route → check redistribution/policy → verify forwarding next hop → allow for convergence before modifying state**.

For multicast:

**membership → multicast tree → RPF → outgoing interfaces**.

For SDN/NFV:

**controller/orchestrator → intended state → device/VNF programmed state → counters/health → forwarding result**.

## Modifying action

The chapter describes configuration concepts but no executable vendor CLI.

Potential state-changing actions include:

- static/dynamic routing configuration and redistribution;
- BGP neighbor/policy changes;
- OSPF area/metric design;
- multicast membership/rendezvous/tree configuration;
- OpenFlow/P4 rule programming;
- VNF instantiation and service-chain orchestration.

Before production changes: capture control-plane and forwarding before-state, define rollback and acceptance checks. Exact commands: **[Needs confirmation]**.

## Verification / acceptance checks

Глава усвоена, если можно:

- distinguish routing from forwarding and convergence from steady state;
- classify DV/LS/PV and centralized/distributed/proactive/reactive routing;
- explain RIP count-to-infinity and its mitigations;
- explain OSPF HELLO → LSA/LSDB → Dijkstra and area/ABR scaling;
- distinguish IGP/EGP, eBGP/iBGP and route redistribution;
- explain AS-path loop detection and route-reflector purpose;
- distinguish IGMP membership from multicast routing and explain RPF;
- explain SDN control/forwarding separation;
- explain OpenFlow match/action/counter model and P4 programmability;
- explain NFV VNF/service chain/MANO and its relationship to SDN.

## Rollback

For chapter artifacts — **[Not applicable]**. For production routing/SDN/NFV changes rollback must restore prior route-policy/protocol state, installed forwarding rules or VNF/service-chain lifecycle state. Exact procedure: **[Needs confirmation]**.
