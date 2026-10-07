# Source findings — глава 17

Canonical evidence: book `computer-networks-olifer-7e-ru-2026`, PDF pp. 514–545; source SHA-256 `16f4b02985f65c602c6268620878cbacd692a61fd5898ca811b3d1a332e3f84d`. Policy: `rag_only`.

## F-01 — [Source extraction issue] Repeated non-book footer/URL

Many chunks contain `Книги для программистов: https://t.me/free_books_for_it`, sometimes merged into prose, captions or tables.

**Decision:** exclude it from canonical artifacts.

## F-02 — [Source extraction issue] Mixed-script/OCR degradation

Frequent examples include malformed `IPv4`, `IPv6`, `ICMPv6`, `ND`, `NAT64`, `DNS64`, MAC literals and RFC identifiers.

**Decision:** normalize only unambiguous standard protocol names.

## F-03 — [Source extraction issue] IPv6 extension-header figure is severely flattened

`p0523:c01` and `p0523:c02` contain a diagram whose spatial structure is largely destroyed in text extraction.

**Decision:** do not reconstruct exact figure geometry. Diagram/SVG artifacts use only prose-supported relationships.

## F-04 — [Source snapshot] Global-unicast prefix/allocation description is edition-specific

`p0518:c01` describes a 45-bit global routing prefix + 16-bit subnet ID + 64-bit interface ID model and states that most contemporary global addresses use `2001::/16`.

**Decision:** preserve as the book's explanatory/allocation snapshot; do not generalize as a universal current IPv6 addressing rule.

## F-05 — [Source snapshot] Interface-ID generation emphasizes MAC/EUI-64 derivation

`p0519:c01`–`p0520:c01` spends substantial space deriving a 64-bit interface ID from an IEEE 802 MAC address and presents it as an autoconfiguration mechanism.

**Decision:** preserve as source content. Current host privacy/stable-address behavior is not inferred from outside knowledge.

## F-06 — [Source wording issue] Multicast group identifiers are confusing in one paragraph

`p0521:c01` describes permanent examples using `::1` / `::2`, then immediately gives `FF02::1` and `FF02::2` as scoped multicast addresses.

**Decision:** canonical notes use the explicit full multicast forms `FF02::1` / `FF02::2` when discussing operational addresses and avoid relying on the abbreviated wording.

## F-07 — [Source snapshot] Neighbor Discovery references an older RFC number

`p0528:c01` identifies Neighbor Discovery with RFC 2461, while ICMPv6 is tied to RFC 4443.

**Decision:** preserve the book's reference as a source-era citation; current standards status is not externally verified in this RAG-only artifact.

## F-08 — [Source snapshot] IPv6 adoption percentages are time-stamped measurements

`p0534:c01`–`p0535:c01` compare old Google IPv6-request percentages with a source snapshot around 2025/2026 and country percentages.

**Decision:** do not present these values as live deployment statistics.

## F-09 — [Source snapshot] Happy Eyeballs behavior is simplified

`p0542:c01` describes browser selection as sending requests via both IPv4 and IPv6 and choosing the faster response.

**Decision:** retain the high-level source idea only; do not treat this paragraph as a complete current algorithm/state-machine specification.

## F-10 — [Source snapshot] Transition technologies include legacy examples

`p0543:c01` names GRE and 6to4 while discussing IPv6-over-IPv4 tunneling.

**Decision:** treat these as source examples, not a recommendation or current deployment default.

## F-11 — [Source inconsistency / OCR-risk] NAT64 example contains inconsistent translator IPv4 literal

`p0544:c01` describes the NAT64 IPv4 interface as `203.0.113.1`, while later mapping text on `p0544:c01`/`p0545:c01` uses `2003.0.113.1`, which is not a valid IPv4 literal and is likely a source/OCR typo.

**Decision:** canonical artifacts describe the mapping generically and do not normalize the literal silently.

## F-12 — [Scope boundary] Part-IV questions are not chapter-17-specific

`p0546:c01` begins «Вопросы к части IV» and mixes material from chapters 13–17.

**Decision:** exclude from chapter-17 review artifacts.
