# Source findings — глава 13

Canonical evidence: book `computer-networks-olifer-7e-ru-2026`, PDF pp. 365–398; source SHA-256 `16f4b02985f65c602c6268620878cbacd692a61fd5898ca811b3d1a332e3f84d`. Policy: `rag_only`.

## F-01 — [Source extraction issue] Repeated non-book footer/URL

Many chunks contain `Книги для программистов: https://t.me/free_books_for_it`, sometimes merged into prose/tables.

**Decision:** exclude it from canonical artifacts.

## F-02 — [Source extraction issue] Mixed Cyrillic/Latin glyphs

Protocol names are frequently OCR-degraded: examples include mixed-script forms of `TCP`, `IP`, `IPv4`, `DHCP`, `ARP`, `DNS`, `Ethernet`.

**Decision:** normalize only unambiguous protocol names; do not treat damaged literal strings as authoritative.

## F-03 — [Source extraction issue] Addressing/DNS/ARP diagrams lose spatial semantics

Figures show internetwork paths, address classes, CIDR pools, ARP exchange, DNS resolution and DHCP topology. Text extraction retains labels but partially loses geometry.

**Decision:** Mermaid/SVG artifacts are source-grounded syntheses, not exact figure reproductions.

## F-04 — [Historical context] Classful IPv4 is taught alongside masks/CIDR

The chapter spends significant space on A/B/C/D/E classes while later presenting masks and CIDR.

**Decision:** preserve classful material as historical/conceptual source content; do not present classful allocation as the default modern planning model.

## F-05 — [Source inconsistency] Private-class-C count appears internally inconsistent

`p0378:c01` states that the private range `192.168.0.0–192.168.255.0` contains **255** class-C networks. The enumerated /24 range spans 256 possible third-octet values.

**Decision:** do not silently correct the book inside chapter notes; record the discrepancy here and avoid relying on that count operationally.

## F-06 — [Source extraction issue] DNS mail-record type appears damaged

`p0390:c01` extracts the mail-server zone-record type as `MS`, which is suspicious in context.

**Decision:** artifacts do not normalize this field from model memory. Use only clearly extracted DNS record types such as A/AAAA/NS where needed.

## F-07 — [Source snapshot] DNS root-server deployment count is dated

`p0393:c01` explicitly cites an August 2013 root-server deployment count while explaining the 13 logical names/addresses model.

**Decision:** treat node-count/geographic deployment details as historical snapshot, not current DNS infrastructure state.

## F-08 — [Implementation-dependent claim] IP packets awaiting ARP resolution

`p0384:c01` says some IP/ARP implementations may drop an IP packet rather than queue it while ARP resolution is pending.

**Decision:** preserve this as implementation-dependent source behavior; do not generalize it to every OS/network stack.

## F-09 — [Source-model boundary] DHCP behavior is conceptual, not a platform lease-state specification

The source explains pools, lease duration, broadcast discovery, relay and renewal at a conceptual level.

**Decision:** real lease timers, option values, failover behavior and server/relay configuration remain **[Needs confirmation]**.
