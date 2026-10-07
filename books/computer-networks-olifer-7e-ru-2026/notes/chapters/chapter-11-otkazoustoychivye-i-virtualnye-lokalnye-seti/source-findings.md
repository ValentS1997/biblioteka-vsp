# Source findings — глава 11

Canonical evidence: book `computer-networks-olifer-7e-ru-2026`, PDF pp. 326–350; source SHA-256 `16f4b02985f65c602c6268620878cbacd692a61fd5898ca811b3d1a332e3f84d`. Policy: `rag_only`.

## F-01 — [Source extraction issue] Repeated non-book footer/URL

Many chunks contain `Книги для программистов: https://t.me/free_books_for_it`, sometimes merged into prose, captions or identifiers.

**Decision:** exclude it from canonical artifacts.

## F-02 — [Source extraction issue] OCR/glyph substitutions

Examples include `HELW` for HELLO-like text, mixed Cyrillic/Latin characters in MAC/VLAN/LACP identifiers, `802.tQ`, `Vir1ual`, and distorted symbols/numbers.

**Decision:** normalize only unambiguous standard terms; do not reconstruct uncertain literal strings from model memory.

## F-03 — [Source extraction issue] Topology/tag diagrams lose spatial semantics

The chapter relies on STP topology figures, LAG/LAS blocks, VLAN layouts and the 802.1Q tag diagram. Text RAG preserves labels/prose but not all geometry.

**Decision:** Mermaid/SVG are source-grounded syntheses, not exact copies.

## F-04 — [Source snapshot] STP/RSTP timers and standard revisions are edition-specific

The source gives classic default HELLO/max-age/listening-style timers and references 802.1D-2004 / 802.1w history.

**Decision:** preserve these only as chapter context. Real switch defaults/current IEEE behavior require platform/current-standard verification.

## F-05 — [Source snapshot / terminology] 802.1Q tag field naming is historical

The source describes TCI as priority + `CFI` + 12-bit VID and uses `0x8100`.

**Decision:** preserve the source terminology in chapter notes; do not silently modernize field naming or infer vendor behavior.

## F-06 — [Source claim requiring verification] Tagged-frame payload statement

`p0344:c01` states that adding the VLAN tag reduces maximum data-field length by 4 bytes.

**Decision:** record this as a source claim only; do not use it as a current universal Ethernet operational rule without external standards verification.

## F-07 — [Source-model caveat] VLAN1/native/default behavior is presented generically

The chapter describes VLAN1 as the default/natural VLAN and untagged classification in its configuration model.

**Decision:** treat this as the chapter's model. Actual native/default VLAN semantics are vendor/platform-specific: **[Needs confirmation]**.

## F-08 — [Needs confirmation] No real LAN configuration/state exists in RAG

There is no actual switch inventory, STP root/port roles, LACP state, VLAN database, trunk allow-list, MSTP mapping or counters.

**Decision:** production diagnosis/configuration remains **[Needs confirmation]** until device/topology evidence is supplied.
