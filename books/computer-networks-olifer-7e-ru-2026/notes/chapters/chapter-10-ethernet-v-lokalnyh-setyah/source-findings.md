# Source findings — глава 10

Canonical evidence: book `computer-networks-olifer-7e-ru-2026`, PDF pp. 287–325; source SHA-256 `16f4b02985f65c602c6268620878cbacd692a61fd5898ca811b3d1a332e3f84d`. Policy: `rag_only`.

## F-01 — [Source extraction issue] Повторяющийся посторонний footer/URL

Во множестве chunks присутствует строка `Книги для программистов: https://t.me/free_books_for_it`, иногда слитая с основным текстом или figure/table labels.

**Решение:** footer не считается содержанием книги и не переносится в canonical artifacts.

## F-02 — [Source extraction issue] OCR/glyph substitutions

Встречаются `1О` вместо `10`, `Gigablt`, смешанные кириллические/латинские glyphs в `Ethernet`, `MAC`, `PAM4`, `FEC`, `MDI`, `PMA`, `PMD`, standard identifiers and formulas.

**Решение:** standard terms are normalized only when unambiguous; damaged exact strings are not quoted as authoritative identifiers.

## F-03 — [Source extraction issue] Diagrams and switch/PHY structures lose spatial semantics

Figures 10.x contain collision timing, bridge topology, forwarding table layouts, switch fabrics and multi-lane PHY diagrams. Text RAG preserves prose/captions but not all geometry.

**Решение:** Mermaid/SVG are new source-grounded conceptual diagrams, not copies of original figures.

## F-04 — [Source snapshot] High-speed Ethernet values are edition-specific

The chapter includes standard names, reach values, lane counts, modulation rates, FEC formats and “next generation” statements up to 800G/1.6T.

**Решение:** preserve them as source statements. Current IEEE/OIF status, modern modules and deployed reaches require external verification.

## F-05 — [Source claim requiring caution] EUI-64 / IPv4 / IPv6 relationship

`p0292:c01` gives a simplified relationship between 48-bit/64-bit MAC formats and IPv4/IPv6 usage.

**Решение:** keep this only as a source claim in the chapter context; do not generalize it into a current universal operational rule without external verification.

## F-06 — [Historical boundary] CSMA/CD remains explanatory but not the model for modern switched Ethernet

The source deliberately retains shared-medium Ethernet because it explains minimum frame size, legacy behavior and historical design choices.

**Решение:** artifacts distinguish legacy/shared-medium mechanics from modern full-duplex switched Ethernet.

## F-07 — [Needs confirmation] Real Ethernet device state is absent

RAG contains no real switch/NIC config, FDB, STP state, port counters, negotiation state, queues, optics or FEC diagnostics.

**Решение:** production diagnosis/configuration remains **[Needs confirmation]** until real evidence is supplied.
