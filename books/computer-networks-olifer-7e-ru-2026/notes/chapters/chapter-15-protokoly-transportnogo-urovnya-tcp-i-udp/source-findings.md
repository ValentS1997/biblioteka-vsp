# Source findings — глава 15

Canonical evidence: book `computer-networks-olifer-7e-ru-2026`, PDF pp. 442–471; source SHA-256 `16f4b02985f65c602c6268620878cbacd692a61fd5898ca811b3d1a332e3f84d`. Policy: `rag_only`.

## F-01 — [Source extraction issue] Repeated non-book footer/URL

Many chunks contain `Книги для программистов: https://t.me/free_books_for_it`, sometimes merged into prose/figures.

**Decision:** exclude it from canonical artifacts.

## F-02 — [Source extraction issue] Mixed Cyrillic/Latin glyphs and OCR damage

Frequent forms include malformed `TCP`, `UDP`, `ACK`, `SYN`, `RTT`, `ESTABLISHED`, RFC identifiers and product/algorithm names.

**Decision:** normalize only unambiguous protocol terms; do not treat damaged literals as authoritative spellings.

## F-03 — [Source extraction issue] Window/timing diagrams lose spatial semantics

Figures 15.10–15.22 are timing/window diagrams whose meaning depends on relative position, arrows and axes.

**Decision:** Mermaid/SVG artifacts synthesize the prose concepts and are not exact reproductions.

## F-04 — [Source-model boundary] Port-number ranges are presented as a simplified two-range model

`p0443:c01` describes `0–1023` as assigned/well-known and `1024–65535` as dynamic.

**Decision:** preserve this as the chapter's model. Do not treat it as a complete current IANA/OS ephemeral-port allocation rule without external verification.

## F-05 — [Source-model boundary] Socket identity is conceptual

`p0444:c01` defines a socket as `(IP address, port number)`, and later identifies a TCP connection by two sockets.

**Decision:** retain this conceptual model; platform API binding/listening semantics are not inferred.

## F-06 — [Source simplification] TCP connection setup/close is explicitly schematic

`p0450:c01` says the shown open/close procedure omits loss, delays, resource failures and additional negotiated parameters.

**Decision:** do not convert the figure into a complete TCP state-machine reference.

## F-07 — [Source snapshot] Receiver-window/URG zero-window behavior is implementation-era specific

`p0465:c01` describes urgent data as something a closed/zero-window port must accept even by displacing buffered data.

**Decision:** preserve only as a source statement; do not use it as a universal modern implementation rule.

## F-08 — [Source simplification] Retransmission timeout calculation is conceptual

`p0465:c01`–`p0466:c01` describes adaptive RTT averaging and says a coefficient greater than 2 is used in the estimate.

**Decision:** treat this as explanatory source material, not an operational formula for a current TCP stack.

## F-09 — [Historical/source snapshot] Slow Start begins at one segment in the chapter example

`p0468:c01` presents a classical algorithm with initial congestion window equal to one segment.

**Decision:** retain as source/classical example. Current defaults and implementation algorithms require platform/current-standard verification.

## F-10 — [Source snapshot / OCR ambiguity] Final TCP-extension table is not externally validated

`p0470:c01`–`p0471:c01` names SACK, CUBIC, BBR, HyStart++, ECN-related mechanisms, Westwood+ and MPTCP, with RFC/default/deployment claims. Some identifiers are visibly OCR-degraded.

**Decision:** record them as edition claims only; do not use them as authoritative current OS/default/RFC mapping without external verification.

## F-11 — [Source wording nuance] ACK-number caption is simplified before cumulative semantics are clarified

The header figure describes ACK using the maximum byte number plus one; later text makes clear that basic TCP acknowledgement advances over a **continuous** byte sequence and repeats the first missing-byte boundary across gaps.

**Decision:** canonical artifacts use the later contiguous/cumulative explanation.
