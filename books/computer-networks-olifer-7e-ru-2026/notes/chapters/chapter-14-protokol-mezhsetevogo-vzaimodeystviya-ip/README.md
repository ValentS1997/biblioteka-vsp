# Глава 14 — Протокол межсетевого взаимодействия IP

Состояние артефактов: `RAG_GROUNDED`. Это **не** означает, что пользователь прочитал главу; reading state книги остаётся `planned`.

## Источник, границы и режим

- Книга: «Компьютерные сети. Принципы, технологии, протоколы», 7-е издание; Виктор Олифер, Наталья Олифер.
- `book_id: computer-networks-olifer-7e-ru-2026`.
- Канонический источник: `source/book.pdf`; SHA-256: `16f4b02985f65c602c6268620878cbacd692a61fd5898ca811b3d1a332e3f84d`.
- Source policy: **rag_only**; прямое чтение PDF, внешний web и модельная память не использовались как источник содержания главы.
- RAG boundary: `computer-networks-olifer-7e-ru-2026:p0399:c01` … `p0441:c01`.
- PDF pages: **399–441**, включительно; **46** адресуемых RAG chunks.
- Печатные страницы книги: **398–440**.
- На `p0399:c01` явно начинается «Глава 14. Протокол межсетевого взаимодействия IP».
- На `p0442:c01` явно начинается «Глава 15. Протоколы транспортного уровня TCP и UDP»; `p0442:c01` в scope главы 14 не входит.
- Chapter boundary: **VERIFIED**.
- BOOK-READINESS v1.3: `READY`; source/RAG generation, acceptance и checksum не менялись.
- Контракт: `BIBLIOTEKA-VSP-CHAPTER-ARTIFACT-COLLECTION v1.7`.

## Карта главы

| Раздел | PDF pages | RAG | Фокус |
| --- | ---: | --- | --- |
| IPv4 packet | 399–402 | `p0399:c01`–`p0402:c01` | header fields, TTL, protocol, checksum, fragmentation flags, ToS/DS |
| IP routing scheme | 402–416 | `p0402:c01`–`p0416:c01` | routing tables, next hop, output interface, default route, metrics, route sources |
| Routing with masks / CIDR | 417–425 | `p0417:c01`–`p0425:c01` | subnetting, VLSM, longest-prefix match, default /0, supernetting/aggregation |
| IP fragmentation | 425–429 | `p0425:c01`–`p0429:c01` | MTU, ID/offset/MF/DF, router fragmentation, destination reassembly |
| ICMP | 429–435 | `p0429:c01`–`p0435:c01` | error/control messages, destination unreachable, TTL expiry, traceroute/tracert, ping |
| Mobile IPv4 | 435–438 | `p0435:c01`–`p0438:c01` | home/foreign agents, care-of address, registration, tunnel |
| IP QoS | 438–441 | `p0438:c01`–`p0441:c01` | IntServ/RSVP vs DiffServ, DS byte/DSCP, EF/AF/LE, per-hop behavior |

Boundary anchors: [p0399:c01](../../../rag/chunks/p0301-p0400/p0399-c01.md) → [p0441:c01](../../../rag/chunks/p0401-p0500/p0441-c01.md) → [p0442:c01](../../../rag/chunks/p0401-p0500/p0442-c01.md).

## Главный принцип

**IPv4 forwards independent best-effort packets hop by hop using a routing-table decision, then relies on adjacent mechanisms for local delivery, diagnostics and adaptation.** Routing chooses the most specific matching prefix and next hop; MTU differences can force fragmentation; ICMP reports conditions but does not repair delivery; QoS markings influence per-hop treatment without changing IP's best-effort core model.

## Что важно вынести

1. **IPv4 is connectionless and best effort.** Each packet is processed independently; IP itself does not retransmit a packet lost because of an error. `p0399:c01`–`p0401:c01`.
2. **Header fields drive router behavior.** Version/header length, total length, identification, flags, fragment offset, TTL, upper-layer protocol, header checksum and source/destination addresses all carry operational meaning. `p0399:c01`–`p0402:c01`.
3. **TTL is an anti-loop lifetime bound.** Routers decrement it; when it reaches zero the packet is discarded. In practice the source interprets TTL as a hop-count-like upper bound. `p0401:c01`.
4. **A router is addressed through interfaces, not as one single forwarding address.** Each interface belongs to a directly connected network and has its own IP/local address. `p0402:c01`.
5. **A routing-table row conceptually answers three questions:** destination prefix/network, next-hop router and outgoing interface. Metrics and status/source fields may add route-selection or provenance information. `p0404:c01`–`p0412:c01`.
6. **Hosts route too.** A host may have a small routing table or simply a connected route plus default gateway; default-route use is especially common at hosts. `p0406:c01`.
7. **Routes can come from three source classes in the chapter:** connected/stack initialization, administrator-created static routes and dynamic routing protocols such as RIP/OSPF. `p0412:c01`.
8. **The source explicitly names a `route` utility for manual static entries.** It does not give a canonical command syntax for a current OS. `p0412:c01`.
9. **With masks, route lookup becomes prefix matching.** A host-specific /32 is checked as most specific; for network routes the destination is ANDed with each mask and matching entries are candidates. `p0420:c01`–`p0421:c01`.
10. **If several entries match, the most specific route wins.** The chapter states that the row with the greatest number of matching high-order bits is selected — the operational idea of longest-prefix match. `p0421:c01`.
11. **Default route is the least-specific route.** `0.0.0.0/0` matches any destination but is used only when no more-specific entry matches. `p0421:c01`.
12. **VLSM uses different mask lengths in one addressing plan.** Routing protocols must carry prefix/mask information for such routes; the source contrasts RIPv2/OSPF with old RIP in this regard. `p0421:c01`–`p0424:c01`.
13. **CIDR supports route aggregation.** Contiguous networks sharing a prefix can be summarized into one routing-table entry, reducing table size and update load. `p0424:c01`–`p0425:c01`.
14. **Fragmentation exists because next-link MTU can be smaller than the packet.** A router may split one IPv4 packet into multiple fragments; routers do not reassemble them in transit. `p0425:c01`–`p0428:c01`.
15. **Reassembly happens at the destination.** Source/destination addresses plus identification associate fragments; offset and MF place/terminate them. Missing fragments cause the reassembly set to be discarded after timeout. `p0428:c01`–`p0429:c01`.
16. **DF changes failure behavior.** If fragmentation is forbidden and a packet cannot pass the next MTU, it is discarded and diagnostic information is returned. `p0427:c01`.
17. **ICMP reports problems; it does not fix them.** It is carried inside IP and can report conditions such as destination unreachable or TTL expiry. `p0429:c01`–`p0431:c01`.
18. **Traceroute/tracert exploits TTL expiry.** It sends probes with increasing TTL values and learns intermediate routers from ICMP time-exceeded responses. `p0432:c01`–`p0433:c01`.
19. **Ping uses ICMP echo request/reply.** Successful replies indicate working IP transport for that test path at that moment, and RTT/loss are reported by the utility. `p0434:c01`–`p0435:c01`.
20. **Mobile IPv4 preserves communication through a home-address abstraction.** Home/foreign agents, a care-of address and a tunnel forward traffic to the current location. `p0435:c01`–`p0438:c01`.
21. **The source itself says Mobile IPv4 is rarely used in practice.** Complexity, NAT interaction, home-agent bottleneck and security exposure are listed as reasons; this remains an edition/source claim. `p0438:c01`.
22. **IntServ and DiffServ solve QoS differently.** IntServ/RSVP reserves per-flow resources end-to-end; DiffServ aggregates packets into classes and defines per-hop behavior. `p0438:c01`–`p0439:c01`.
23. **DiffServ uses the DS byte / DSCP marking to classify traffic.** The source describes EF, AF, LE and ordinary best-effort treatment. `p0439:c01`–`p0441:c01`.
24. **DiffServ is easier to scale but does not inherently provide quantitative end-to-end guarantees across the Internet.** The source says it is typically applied within one administrative domain. `p0441:c01`.

## Артефакты

- [cheatsheet.md](cheatsheet.md) — conceptual/operational cheatsheet v1.7.
- [commands.md](commands.md) — source-named `route`, `traceroute`/`tracert`, `ping` utilities and safety/interpretation boundary.
- [diagram.md](diagram.md) — Mermaid map of route lookup → next hop → MTU/fragmentation → ICMP/QoS.
- [visual-cheatsheet.svg](visual-cheatsheet.svg) — compact visual summary.
- [visual-cheatsheet-detailed.svg](visual-cheatsheet-detailed.svg) — detailed visual summary.
- [source-findings.md](source-findings.md) — extraction/provenance, contradictions and historical/source-snapshot caveats.

## Conditional artifacts

- Отдельного явного chapter-end summary на PDF pp. 399–441 **не обнаружено** → `summary.md` не создаётся.
- Review/control questions or exercises inside the verified boundary **не обнаружены** → `review-questions.md` / `review-answers.md` не создаются.

## Ограничения источника

RAG contains repeated footer contamination, OCR/glyph substitutions, degraded routing/fragmentation/QoS figures and several historical or internally inconsistent statements. These are recorded in `source-findings.md`; artifacts do not silently correct them from model memory.
