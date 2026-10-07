# Глава 16 — Протоколы маршрутизации и технология SDN

Состояние артефактов: `RAG_GROUNDED`. Это **не** означает, что пользователь прочитал главу; reading state книги остаётся `planned`.

## Источник, границы и режим

- Книга: «Компьютерные сети. Принципы, технологии, протоколы», 7-е издание; Виктор Олифер, Наталья Олифер.
- `book_id: computer-networks-olifer-7e-ru-2026`.
- Канонический источник: `source/book.pdf`; SHA-256: `16f4b02985f65c602c6268620878cbacd692a61fd5898ca811b3d1a332e3f84d`.
- Source policy: **rag_only**; прямое чтение PDF, внешний web и модельная память не использовались как источник содержания главы.
- RAG boundary: `computer-networks-olifer-7e-ru-2026:p0472:c01` … `p0513:c01`.
- PDF pages: **472–513**, включительно; **42** адресуемых RAG chunks.
- Печатные страницы книги: **471–512**.
- На `p0472:c01` явно начинается «Глава 16. Протоколы маршрутизации и технология SDN».
- На `p0514:c01` явно начинается «Глава 17. IPv6 как развитие стека TCP/IP»; `p0514:c01` в scope главы 16 не входит.
- Chapter boundary: **VERIFIED**.
- BOOK-READINESS v1.3: `READY`; source/RAG generation, acceptance и checksum не менялись.
- Контракт: `BIBLIOTEKA-VSP-CHAPTER-ARTIFACT-COLLECTION v1.7`.

## Карта главы

| Раздел | PDF pages | RAG | Фокус |
| --- | ---: | --- | --- |
| Обзор методов маршрутизации | 472–477 | `p0472:c01`–`p0477:c01` | static/dynamic, distributed/centralized, DV/LS/PV, proactive/reactive, IGP/EGP |
| RIP | 477–485 | `p0477:c01`–`p0485:c01` | distance vector, hop metric, periodic advertisements, count-to-infinity, split horizon, triggered updates, hold-down |
| OSPF / IS-IS | 485–490 | `p0485:c01`–`p0490:c01` | HELLO, LSA/LSDB, Dijkstra, DR, areas/ABR/backbone, equal-cost paths |
| Heterogeneous routing / BGP | 490–498 | `p0490:c01`–`p0498:c01` | route redistribution, AS, IGP/EGP, eBGP/iBGP, UPDATE, AS path, policy, route reflector |
| Multicast | 498–504 | `p0498:c01`–`p0504:c01` | multicast model, IGMP, DVMRP/MOSPF/PIM, dense/sparse mode, shared/source trees, RPF |
| SDN / OpenFlow / P4 | 504–510 | `p0504:c01`–`p0510:c01` | control/forwarding separation, controller, match/action/counters, table pipeline, programmable packet processors |
| NFV / MANO | 510–513 | `p0510:c01`–`p0513:c01` | VNF, service chain, orchestration, NFV MANO, SDN/NFV relationship |

Boundary anchors: [p0472:c01](../../../rag/chunks/p0401-p0500/p0472-c01.md) → [p0513:c01](../../../rag/chunks/p0501-p0600/p0513-c01.md) → [p0514:c01](../../../rag/chunks/p0501-p0600/p0514-c01.md).

## Главный принцип

**Routing control builds forwarding state; forwarding then uses that state packet by packet.** Distributed protocols differ mainly in what knowledge they exchange and how they converge, while SDN moves more control logic into a programmable controller. NFV addresses a different axis: implementing network functions in software on general-purpose infrastructure.

## Что важно вынести

1. **Routing and forwarding are different tasks.** Routing finds/maintains paths; forwarding applies already selected next-hop decisions to packets. `p0472:c01`–`p0474:c01`.
2. **The chapter classifies routing along several independent axes:** static vs dynamic, distributed vs centralized, proactive vs reactive, unicast vs multicast, single vs multiple paths, IGP vs EGP. `p0472:c01`–`p0477:c01`.
3. **Convergence is the interval in which routers move from inconsistent state after a topology change to mutually consistent routing state.** Different protocols converge at different rates. `p0474:c01`–`p0476:c01`.
4. **Distance-vector protocols exchange reachability plus distance, not a full topology graph.** RIP is the source's main DV example and commonly uses hop count. `p0475:c01`–`p0478:c01`.
5. **RIP learns recursively from neighbors.** Each router advertises known networks and distances; the receiver increments the metric and keeps better information. `p0478:c01`–`p0481:c01`.
6. **RIP failure adaptation can be slow and loop-prone.** The source explains route lifetime, metric 16 as unreachable and the count-to-infinity problem. `p0481:c01`–`p0484:c01`.
7. **RIP loop-mitigation mechanisms in the chapter are split horizon, triggered updates and hold-down/freeze behavior.** These reduce stale-route propagation but do not turn DV into a topology-aware protocol. `p0484:c01`–`p0485:c01`.
8. **OSPF separates topology synchronization from route calculation.** Routers maintain an LSDB from LSA information, then run Dijkstra locally to obtain next hops. `p0485:c01`–`p0487:c01`.
9. **OSPF uses HELLO for neighbor/link-state awareness and floods topology changes through LSA.** Stable topology reduces update traffic relative to periodic full-vector exchange. `p0485:c01`–`p0486:c01`.
10. **Transit networks introduce a designated-router abstraction in the source model.** LSA Type 1/2 information represents routers and shared transit networks. `p0487:c01`–`p0488:c01`.
11. **OSPF areas scale the LSDB/SPF problem.** Routers inside an area share detailed topology; ABRs exchange summarized inter-area information, and area 0 is the backbone in the source description. `p0488:c01`–`p0490:c01`.
12. **Multiple routing protocols can coexist.** Route provenance/priority matters, and redistribution allows one routing process to inject selected information learned by another. `p0490:c01`–`p0491:c01`.
13. **Autonomous systems add a higher routing hierarchy.** IGP handles routing inside an AS; BGP is the EGP used between ASes in the chapter. `p0491:c01`–`p0493:c01`.
14. **BGP is policy-based and path-vector.** Peering is explicitly configured; BGP sessions use TCP/179 in the source, and UPDATE announcements carry reachability/path information. `p0493:c01`–`p0495:c01`.
15. **AS path gives BGP loop visibility across autonomous systems.** If a router sees its own AS in the advertised path, the route is rejected. `p0495:c01`–`p0496:c01`.
16. **eBGP and iBGP solve different scopes.** iBGP propagates external reachability within one AS; the basic full-mesh rule scales poorly, so the chapter introduces route reflectors. `p0496:c01`–`p0498:c01`.
17. **Multicast avoids sending identical unicast copies across common path segments.** Replication occurs at branching routers only where needed. `p0498:c01`–`p0499:c01`.
18. **IGMP manages local host membership, not the entire multicast tree.** Separate multicast-routing protocols such as DVMRP, MOSPF and PIM build/maintain forwarding trees across routers. `p0500:c01`–`p0502:c01`.
19. **Dense and sparse multicast modes make opposite receiver-density assumptions.** Sparse mode uses an explicit rendezvous-point concept in the source. `p0502:c01`–`p0503:c01`.
20. **RPF validates a multicast packet against the reverse unicast path to its source before further replication.** This is the chapter's central anti-loop principle for multicast forwarding. `p0503:c01`–`p0504:c01`.
21. **SDN separates forwarding from control through a standardized controller-device abstraction.** The controller receives network state and programs device behavior. `p0504:c01`–`p0507:c01`.
22. **OpenFlow is presented as match → action → counters.** A rule can match multiple header/input-port fields, modify/forward/drop according to actions and expose counters to the controller. `p0507:c01`–`p0508:c01`.
23. **OpenFlow pipelines multiple tables because one universal rule table does not scale cleanly.** The source also notes the architectural-unification problem that motivates programmable packet processors. `p0508:c01`.
24. **P4 moves packet-processing architecture into programmable hardware.** The source separates architecture configuration, rule loading by the controller and runtime packet processing, with P4Runtime-like controller interaction. `p0509:c01`–`p0510:c01`.
25. **NFV is not the same thing as SDN.** NFV implements routers/firewalls/switches and other network functions as software on general-purpose servers; chaining VNFs creates a virtual network service. `p0510:c01`–`p0512:c01`.
26. **NFV MANO orchestrates lifecycle and infrastructure/function management.** The source divides responsibility among infrastructure management, VNF management and an NFV orchestrator. `p0512:c01`–`p0513:c01`.
27. **SDN and NFV can be independent or complementary.** One controls programmable forwarding behavior; the other virtualizes the functions providing network services. `p0513:c01`.

## Артефакты

- [cheatsheet.md](cheatsheet.md) — conceptual/operational cheatsheet v1.7.
- [commands.md](commands.md) — source-confirmed protocols and pseudorule formats; executable vendor CLI is not invented.
- [diagram.md](diagram.md) — Mermaid map from route-control families to BGP/multicast and SDN/NFV.
- [visual-cheatsheet.svg](visual-cheatsheet.svg) — compact visual summary.
- [visual-cheatsheet-detailed.svg](visual-cheatsheet-detailed.svg) — detailed visual summary.
- [source-findings.md](source-findings.md) — extraction/provenance, inconsistencies and source-snapshot caveats.

## Conditional artifacts

- Отдельного явного chapter-end summary на PDF pp. 472–513 **не обнаружено** → `summary.md` не создаётся.
- Review/control questions or exercises inside the verified boundary **не обнаружены** → `review-questions.md` / `review-answers.md` не создаются.

## Ограничения источника

RAG contains repeated footer contamination, OCR/mixed-script protocol names, degraded topology diagrams and a number of historical/default/scaling claims. These are retained as source-era context rather than silently replaced with current protocol/vendor behavior.
