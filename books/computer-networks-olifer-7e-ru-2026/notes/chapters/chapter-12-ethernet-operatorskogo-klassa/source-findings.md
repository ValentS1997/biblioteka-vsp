# Source findings — глава 12

Canonical evidence: book `computer-networks-olifer-7e-ru-2026`, PDF pp. 351–360; source SHA-256 `16f4b02985f65c602c6268620878cbacd692a61fd5898ca811b3d1a332e3f84d`. Policy: `rag_only`.

## F-01 — [Source extraction issue] Repeated non-book footer/URL

Many chunks contain `Книги для программистов: https://t.me/free_books_for_it`, sometimes merged into prose.

**Decision:** exclude it from canonical artifacts.

## F-02 — [Source extraction issue] Standard identifiers are OCR-degraded

The RAG contains strings such as `802.tag`, `802.Заh`, `802.tad`, `802.tah`, mixed Cyrillic/Latin `Y.1731`, and distorted Ethernet terms.

**Decision:** use standard acronyms/names only where context is unambiguous; do not treat the damaged literal strings as authoritative identifiers.

## F-03 — [Source extraction issue] OAM and encapsulation figures lose spatial semantics

Figures 12.1–12.4 show MEP/MIP paths, nested maintenance domains and C-VID/S-VID encapsulation. Text extraction preserves labels but not full topology geometry.

**Decision:** Mermaid/SVG are new source-grounded conceptual diagrams, not exact reproductions.

## F-04 — [Operational safety finding] Remote loopback is explicitly disruptive

`p0357:c01` states that physical-link loopback testing interrupts normal connection operation and should be performed during maintenance time.

**Decision:** classify it as a disruptive maintenance action, not a harmless read-only diagnostic.

## F-05 — [Source snapshot] OAM timing/standards and failover comparisons are edition-specific

The source compares STP/RSTP recovery with transport technologies and names specific IEEE/ITU-T/MEF standards.

**Decision:** preserve these as chapter context. Current standard revisions, timers and implementation behavior require external/platform verification.

## F-06 — [Source snapshot] Provider Bridge scaling limits are presented in the edition's model

The chapter states that PB retains customer-MAC learning, has a 12-bit S-VID service-space limit and relies on RSTP/MSTP for traffic engineering.

**Decision:** use as source-grounded conceptual limits; do not extrapolate to every modern provider Ethernet architecture.

## F-07 — [Source snapshot] PBB vs MPLS/EVPN deployment statement

`p0360:c01` says PBB was too complex and that large provider networks instead use MPLS-based EVPN and L2 MPLS VPN.

**Decision:** retain as an authored/source-era statement, not a current market-universal claim.

## F-08 — [Boundary finding] Part-III questions are not chapter-specific

`p0361:c01` begins «Вопросы к части III» and includes material spanning chapters 10–12.

**Decision:** exclude them from chapter-12 review artifacts.
