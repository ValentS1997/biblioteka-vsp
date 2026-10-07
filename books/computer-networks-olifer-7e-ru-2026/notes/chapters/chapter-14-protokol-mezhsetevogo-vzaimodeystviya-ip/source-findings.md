# Source findings — глава 14

Canonical evidence: book `computer-networks-olifer-7e-ru-2026`, PDF pp. 399–441; source SHA-256 `16f4b02985f65c602c6268620878cbacd692a61fd5898ca811b3d1a332e3f84d`. Policy: `rag_only`.

## F-01 — [Source extraction issue] Repeated non-book footer/URL

Many chunks contain `Книги для программистов: https://t.me/free_books_for_it`, often merged into prose, tables or figures.

**Decision:** exclude it from canonical artifacts.

## F-02 — [Source extraction issue] Mixed-script/OCR degradation

Examples include malformed `IP`, `ICMP`, `TTL`, `Mobile IP`, `DiffServ`, `IntServ`, `PHB`, route-table headings and hexadecimal literals.

**Decision:** normalize standard terms only when context is unambiguous.

## F-03 — [Source extraction issue] Routing/fragmentation/QoS figures lose spatial semantics

Figures 14.x carry route topologies, table layouts, subnetting diagrams, fragment placement, ICMP formats and DS-byte bit fields. RAG prose preserves the concepts but not all geometry.

**Decision:** Mermaid/SVG are source-grounded syntheses, not reproductions.

## F-04 — [Internal contradiction] DF flag description conflicts inside the source

`p0427:c01` correctly describes `DF=1` as **do not fragment**. But `p0428:c01` later says the example sets `DF=1` and glosses it as allowing fragmentation, immediately before the router fragments the packet.

**Decision:** do not silently reconcile the example. Canonical notes use the explicit semantic definition from `p0427:c01` and record the contradictory example here.

## F-05 — [Source snapshot] IPv4 fragmentation behavior is edition/protocol-context specific

The chapter presents router-based IPv4 fragmentation and destination reassembly in detail, including example reassembly timers and MTU values.

**Decision:** preserve as IPv4/source behavior. Real path-MTU behavior, OS defaults and modern deployment practice require platform/current verification.

## F-06 — [Source snapshot] ICMP type/code and traceroute behavior are explanatory examples

The chapter names ICMP types/codes and describes traceroute using TTL expiry. Actual utilities can differ in probe protocol/options by platform.

**Decision:** preserve the protocol principle; do not infer exact current utility flags.

## F-07 — [Source snapshot] Mobile IPv4 deployment assessment

The source says Mobile IPv4 is rarely used in practice and lists implementation/NAT/performance/security reasons.

**Decision:** retain as authored source-era assessment, not a current universal deployment claim.

## F-08 — [Source snapshot] DiffServ bit/class discussion is source-era terminology

The chapter explains DS byte/DSCP and EF/AF/LE behavior, including numeric code examples and an `IN` profile indicator description.

**Decision:** preserve the chapter's conceptual QoS framing; exact current standards terminology/codepoints/policies require external verification if needed operationally.

## F-09 — [Operational boundary] No real routing or QoS state exists in RAG

No actual router config, FIB/RIB dump, MTU state, ICMP policy, dynamic-routing adjacency or queue/policer configuration is present.

**Decision:** production diagnosis/configuration remains **[Needs confirmation]** until real evidence is supplied.
