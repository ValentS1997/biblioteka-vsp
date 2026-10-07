# Source findings — глава 16

Canonical evidence: book `computer-networks-olifer-7e-ru-2026`, PDF pp. 472–513; source SHA-256 `16f4b02985f65c602c6268620878cbacd692a61fd5898ca811b3d1a332e3f84d`. Policy: `rag_only`.

## F-01 — [Source extraction issue] Repeated non-book footer/URL

Many chunks contain `Книги для программистов: https://t.me/free_books_for_it`, sometimes merged into prose, tables and captions.

**Decision:** exclude it from canonical artifacts.

## F-02 — [Source extraction issue] OCR and mixed-script protocol names

Examples include distorted/mixed-script `RIP`, `OSPF`, `BGP`, `iBGP/eBGP`, `IGMP`, `OpenFlow`, `P4`, `NFV` and RFC/identifier text.

**Decision:** normalize only unambiguous standard names; uncertain literals are not treated as authoritative.

## F-03 — [Source extraction issue] Routing/SDN figures lose topology and pipeline geometry

RIP/OSPF/BGP examples, multicast trees, OpenFlow pipelines and NFV service diagrams rely heavily on spatial layout.

**Decision:** Mermaid/SVG artifacts are source-grounded syntheses, not copies of the original figures.

## F-04 — [Source snapshot] RIP timers and metric-16 behavior are treated as chapter-era protocol values

The chapter gives periodic advertisements of 30 s, route invalidation around 180 s and 16 as unreachable, then develops a count-to-infinity example.

**Decision:** preserve as source protocol context; current device timers/features require platform verification.

## F-05 — [Source snapshot / historical behavior] OSPF metric/TOS discussion is source-era material

`p0488:c01` describes separate OSPF route tables for delay/throughput/reliability TOS-related metrics and gives fixed example costs for old link speeds.

**Decision:** preserve as chapter content only; do not turn it into a current universal OSPF implementation rule.

## F-06 — [Source snapshot] BGP scalability and deployment claims are not externally verified

The chapter includes numerical statements about prefix/AS scaling, full-mesh iBGP and provider route-reflector practice.

**Decision:** use the architectural ideas; treat specific scale/deployment statements as edition snapshots.

## F-07 — [Internal inconsistency] OpenFlow TCP destination-port example disagrees with its prose

`p0507:c01` prints a match condition with `TCP DstPort = 5009`, while the following prose says the same condition selects TCP port `5901`.

**Decision:** do not choose one silently. Canonical artifacts describe the field generically and record the mismatch here.

## F-08 — [Source extraction issue] OpenFlow action example contains a damaged MAC literal

`p0508:c01` renders the destination-MAC rewrite value with an OCR-damaged final byte/character.

**Decision:** do not reuse that literal operationally.

## F-09 — [Source snapshot / naming] P4 runtime naming is typographically inconsistent

`p0510:c01` renders the controller protocol as `p4.runtime`.

**Decision:** artifacts describe it generically as the P4 runtime/controller interface; exact current standard/product naming requires external verification if needed.

## F-10 — [Source snapshot] NFV advantages/disadvantages are architectural claims, not measured guarantees

The chapter contrasts general-purpose servers with specialized network hardware in cost, performance and reliability.

**Decision:** preserve as source reasoning; actual performance/reliability depends on implementation and workload.

## F-11 — [Operational boundary] No live control-plane/device state exists in RAG

There is no real RIB/FIB, routing neighbor state, LSDB, BGP policy, multicast tree, SDN rule dump, P4 pipeline or NFV MANO inventory.

**Decision:** production troubleshooting/configuration remains **[Needs confirmation]** until real evidence is supplied.
