# Глава 17 — IPv6 как развитие стека TCP/IP

Состояние артефактов: `RAG_GROUNDED`. Это **не** означает, что пользователь прочитал главу; reading state книги остаётся `planned`.

## Источник, границы и режим

- Книга: «Компьютерные сети. Принципы, технологии, протоколы», 7-е издание; Виктор Олифер, Наталья Олифер.
- `book_id: computer-networks-olifer-7e-ru-2026`.
- Канонический источник: `source/book.pdf`; SHA-256: `16f4b02985f65c602c6268620878cbacd692a61fd5898ca811b3d1a332e3f84d`.
- Source policy: **rag_only**; прямое чтение PDF, внешний web и модельная память не использовались как источник содержания главы.
- RAG boundary: `computer-networks-olifer-7e-ru-2026:p0514:c01` … `p0545:c01`.
- PDF pages: **514–545**, включительно; **33** адресуемых RAG chunks.
- Печатные страницы книги: **513–544**.
- На `p0514:c01` явно начинается «Глава 17. IPv6 как развитие стека TCP/IP».
- На `p0546:c01` явно начинается «Вопросы к части IV»; это общий review block части IV, а не продолжение главы 17.
- Chapter boundary: **VERIFIED**.
- BOOK-READINESS v1.3: `READY`; source/RAG generation, acceptance и checksum не менялись.
- Контракт: `BIBLIOTEKA-VSP-CHAPTER-ARTIFACT-COLLECTION v1.7`.

## Карта главы

| Раздел | PDF pages | RAG | Фокус |
| --- | ---: | --- | --- |
| Предпосылки и цели IPv6 | 514 | `p0514:c01` | address scale, autoconfiguration, router work reduction, QoS/security goals |
| IPv6 addressing | 515–523 | `p0515:c01`–`p0523:c01` | 128-bit notation, unicast/anycast/multicast, scope, link-local/ULA, solicited-node multicast |
| IPv6 packet format | 523–528 | `p0523:c01`–`p0528:c01` | fixed 40-byte base header, next-header chain, extension headers, hop limit, fragmentation model |
| ICMPv6 / Neighbor Discovery | 528–534 | `p0528:c01`–`p0534:c01` | RS/RA/NS/NA/Redirect, DAD, address resolution, local-hop validation |
| IPv6 adoption / heterogeneous-network integration | 534–540 | `p0534:c01`–`p0540:c01` | source adoption snapshot, dual stacks, translation, tunneling |
| IPv4/IPv6 coexistence | 540–545 | `p0540:c01`–`p0545:c01` | dual stack, Happy Eyeballs source description, GRE/6to4 examples, NAT64/DNS64 flow |

Boundary anchors: [p0514:c01](../../../rag/chunks/p0501-p0600/p0514-c01.md) → [p0545:c01](../../../rag/chunks/p0501-p0600/p0545-c01.md) → [p0546:c01](../../../rag/chunks/p0501-p0600/p0546-c01.md).

## Главный принцип

**IPv6 is not merely “IPv4 with longer addresses”.** The chapter presents it as a redesign around a much larger address space, scoped/multiple interface addresses, a simplified fixed base header with extension headers, endpoint-side fragmentation, ICMPv6/Neighbor Discovery and explicit coexistence mechanisms for a long IPv4→IPv6 transition.

## Что важно вынести

1. **IPv6 uses 128-bit addresses and hexadecimal colon notation.** Zero compression with `::` is allowed once in an address. `p0515:c01`.
2. **IPv6 drops IPv4 classful A/B/C/D/E addressing and relies on prefix/CIDR-style structure.** `p0515:c01`.
3. **One interface commonly has multiple IPv6 addresses.** The source distinguishes unicast, multicast and anycast, plus special unspecified and loopback addresses. `p0516:c01`–`p0523:c01`.
4. **Address scope is operationally significant.** Link-local addresses are intended for one link; globally scoped addresses are used beyond it. `p0516:c01`, `p0520:c01`.
5. **The source presents a common global-unicast layout with routing prefix + subnet ID + 64-bit interface ID.** This is preserved as its explanatory model, not generalized beyond the source. `p0518:c01`–`p0519:c01`.
6. **Link-local addresses use the `FE80::` family in the chapter and are automatically present on IPv6 interfaces.** They are not routed off-link. `p0520:c01`.
7. **Unique-local addresses are described under `FC00::/7`.** Their scope is internal rather than global. `p0520:c01`.
8. **IPv6 multicast replaces many broadcast-style functions.** The chapter highlights all-nodes/all-routers multicast and solicited-node multicast. `p0520:c01`–`p0522:c01`.
9. **Solicited-node multicast narrows link-layer discovery traffic.** It is derived from the target unicast address and maps to an Ethernet multicast address. `p0521:c01`–`p0522:c01`.
10. **The IPv6 base header has a fixed 40-byte length.** It contains version, traffic class, flow label, payload length, next header, hop limit and 128-bit source/destination addresses. `p0523:c01`–`p0525:c01`.
11. **Optional information is carried in extension headers.** The source lists hop-by-hop, destination options, routing, fragment, authentication and encapsulating-security-payload headers. `p0523:c01`–`p0526:c01`.
12. **`Next Header` chains the base header, extension headers and upper-layer protocol together.** `p0523:c01`–`p0525:c01`.
13. **IPv6 routers do not fragment transit packets in the chapter model.** End hosts are expected to adapt packet size; routers return an ICMPv6 “packet too big” condition when needed. `p0527:c01`.
14. **ICMPv6 is more structurally important than ICMPv4 in this chapter.** Besides errors/diagnostics it carries Neighbor Discovery messages. `p0528:c01`–`p0529:c01`.
15. **Neighbor Discovery replaces ARP-like address resolution and also covers router discovery, redirects, duplicate-address detection and configuration information.** `p0528:c01`–`p0530:c01`.
16. **The five ND message types described are Router Solicitation, Router Advertisement, Neighbor Solicitation, Neighbor Advertisement and Redirect.** `p0529:c01`–`p0530:c01`.
17. **ND messages are constrained to the local link by the source's hop-limit check.** The chapter says they are sent with hop limit 255 and rejected when received with a smaller value. `p0530:c01`.
18. **Duplicate Address Detection uses Neighbor Solicitation before the tentative address is used.** A response proves a duplicate exists. `p0531:c01`–`p0532:c01`.
19. **IPv6 address resolution uses NS/NA plus solicited-node multicast instead of ARP broadcast.** `p0533:c01`–`p0534:c01`.
20. **The chapter treats migration as long-running coexistence rather than a flag-day cutover.** It compares dual stack, protocol translation and tunneling. `p0534:c01`–`p0541:c01`.
21. **Dual stack gives a node independent IPv4 and IPv6 configuration.** Application/name-resolution logic chooses which stack to use. `p0541:c01`–`p0542:c01`.
22. **The source describes browser preference selection using a Happy-Eyeballs-style race between IPv4 and IPv6 reachability.** This is recorded as source framing, not as a complete current algorithm specification. `p0542:c01`.
23. **Tunneling carries one protocol inside another across an incompatible transit network.** The source names GRE as a manual example and 6to4 as an automatic IPv6-over-IPv4 example. `p0539:c01`, `p0542:c01`–`p0543:c01`.
24. **Translation is required when an IPv6-only node must communicate with an IPv4-only node in the source model.** `p0543:c01`–`p0545:c01`.
25. **NAT64/DNS64 is explained as a stateful address/port translation path.** DNS64 synthesizes an IPv6 representation of an IPv4 destination; NAT64 then translates IPv6/IPv4 headers and transport-address mappings. `p0543:c01`–`p0545:c01`.

## Артефакты

- [cheatsheet.md](cheatsheet.md) — conceptual/operational cheatsheet v1.7.
- [commands.md](commands.md) — source-confirmed IPv6/ND/coexistence mechanisms; executable OS/router CLI is absent.
- [diagram.md](diagram.md) — Mermaid map of address selection, ND, packet handling and transition mechanisms.
- [visual-cheatsheet.svg](visual-cheatsheet.svg) — compact visual summary.
- [visual-cheatsheet-detailed.svg](visual-cheatsheet-detailed.svg) — detailed visual summary.
- [source-findings.md](source-findings.md) — extraction/provenance, dated statements and source-specific simplifications.

## Conditional artifacts

- Отдельного явного chapter-end summary на PDF pp. 514–545 **не обнаружено** → `summary.md` не создаётся.
- `p0546:c01` starts **«Вопросы к части IV»**, covering the whole Part IV rather than chapter 17 alone → chapter-specific `review-questions.md` / `review-answers.md` не создаются.

## Ограничения источника

RAG contains repeated footer contamination, OCR/mixed-script IPv4/IPv6 spellings, a severely degraded extension-header figure and several dated/edition-specific statements about address allocation, EUI-64-derived identifiers, deployment percentages, transition mechanisms and standards references. They are retained as source context rather than silently modernized.
