# Глава 13 — Стек протоколов TCP/IP. Адресация

Состояние артефактов: `RAG_GROUNDED`. Это **не** означает, что пользователь прочитал главу; reading state книги остаётся `planned`.

## Источник, границы и режим

- Книга: «Компьютерные сети. Принципы, технологии, протоколы», 7-е издание; Виктор Олифер, Наталья Олифер.
- `book_id: computer-networks-olifer-7e-ru-2026`.
- Канонический источник: `source/book.pdf`; SHA-256: `16f4b02985f65c602c6268620878cbacd692a61fd5898ca811b3d1a332e3f84d`.
- Source policy: **rag_only**; прямое чтение PDF, внешний web и модельная память не использовались как источник содержания главы.
- RAG boundary: `computer-networks-olifer-7e-ru-2026:p0365:c01` … `p0398:c01`.
- PDF pages: **365–398**, включительно; **35** адресуемых RAG chunks.
- Печатные страницы книги: **364–397**.
- На `p0365:c01` явно начинается «Глава 13. Стек протоколов TCP/IP. Адресация».
- На `p0399:c01` явно начинается «Глава 14. Протокол межсетевого взаимодействия IP»; `p0399:c01` в scope главы 13 не входит.
- Chapter boundary: **VERIFIED**.
- BOOK-READINESS v1.3: `READY`; source/RAG generation, acceptance и checksum не менялись.
- Контракт: `BIBLIOTEKA-VSP-CHAPTER-ARTIFACT-COLLECTION v1.7`.

## Карта главы

| Раздел | PDF pages | RAG | Фокус |
| --- | ---: | --- | --- |
| Стек TCP/IP | 365–368 | `p0365:c01`–`p0368:c01` | 4 layers, TCP/UDP/IP roles, network-interface abstraction, PDU terminology |
| Межсетевое взаимодействие | 369–370 | `p0369:c01`–`p0370:c01` | routers, heterogeneous subnetworks, hop-by-hop frame replacement |
| Типы адресов | 370–371 | `p0370:c01`–`p0371:c01` | local/hardware address, IP address, symbolic/domain name |
| IPv4 format and masks | 372–377 | `p0372:c01`–`p0377:c01` | 32-bit IPv4, historical classes, multicast/special addresses, masks/prefixes |
| Address assignment and CIDR | 377–380 | `p0377:c01`–`p0380:c01` | public/private allocation, NAT pointer, CIDR address pools |
| IP→local address mapping | 380–386 | `p0380:c01`–`p0386:c01` | ARP cache/request/reply, static/dynamic entries, RARP, Proxy-ARP |
| DNS | 386–394 | `p0386:c01`–`p0394:c01` | hierarchical names, resolver/server, zones, iterative/recursive lookup, reverse zone |
| DHCP | 394–398 | `p0394:c01`–`p0398:c01` | automatic interface configuration, lease, relay, offer/request/ack flow, dynamic-address trade-offs |

Boundary anchors: [p0365:c01](../../../rag/chunks/p0301-p0400/p0365-c01.md) → [p0398:c01](../../../rag/chunks/p0301-p0400/p0398-c01.md) → [p0399:c01](../../../rag/chunks/p0301-p0400/p0399-c01.md).

## Главный принцип

**TCP/IP separates end-to-end network identity from local-link delivery.** IP provides globally meaningful network-layer addressing and inter-network forwarding; each local link still uses its own link-layer addressing, so the stack needs mapping mechanisms such as ARP, scalable naming through DNS and scalable configuration through DHCP.

## Что важно вынести

1. **TCP/IP uses a four-layer model in the source:** application, transport, internet/network and network-interface layers. Mapping to OSI is approximate rather than one-to-one. `p0365:c01`–`p0367:c01`.
2. **TCP and UDP offer different transport services.** TCP is connection-oriented and reliability-oriented; UDP is datagram/best-effort at transport level. IP itself is connectionless best-effort. `p0366:c01`–`p0367:c01`.
3. **The network-interface layer is deliberately under-specified by TCP/IP.** IP only requires the lower technology to move data between directly connected IP nodes; Ethernet, PPP and other technologies can serve that role. `p0367:c01`–`p0368:c01`.
4. **Encapsulation changes hop by hop.** The IP packet remains the network-layer unit while each router removes the incoming local frame and creates a new frame suitable for the next subnetwork. `p0369:c01`–`p0370:c01`.
5. **Three address classes coexist conceptually:** local/hardware address, network/IP address and symbolic/domain name. They solve different scopes and require mappings between them. `p0370:c01`–`p0371:c01`.
6. **IPv4 is 32-bit and the source presents both historical classful addressing and mask/prefix addressing.** Classful A/B/C/D/E material is preserved as historical/source context; masks make network/host boundaries flexible. `p0372:c01`–`p0377:c01`.
7. **Special addresses encode special semantics.** The source discusses unspecified-style zero forms, limited/directed broadcast forms and the 127/8 loopback range. `p0375:c01`–`p0376:c01`.
8. **Public and private allocation solve different uniqueness scopes.** The source lists private IPv4 blocks and points forward to NAT for connecting private-address networks to external networks. `p0377:c01`–`p0378:c01`.
9. **CIDR allocates contiguous prefix-based address pools.** A prefix length defines the network portion and the remaining bits define the address pool; this improves address-space utilization and later supports route aggregation. `p0379:c01`–`p0380:c01`.
10. **ARP maps an IPv4 next-hop address to a local address on a broadcast-capable link.** Cache miss → broadcast ARP request → matching interface replies → mapping enters ARP cache. `p0381:c01`–`p0384:c01`.
11. **ARP cache has dynamic and static entries.** Source states static entries can be created manually with the `arp` utility; concrete syntax is not supplied. `p0384:c01`.
12. **RARP and Proxy-ARP are separate source-described mechanisms.** RARP solves reverse local→IP mapping in older scenarios; Proxy-ARP lets a router answer ARP on behalf of a node beyond the local broadcast segment. `p0385:c01`–`p0386:c01`.
13. **DNS replaces flat, broadcast-style name resolution with hierarchical delegated naming.** Domain hierarchy divides administrative responsibility while DNS servers maintain a distributed mapping database. `p0386:c01`–`p0390:c01`.
14. **Resolver and DNS server are separate roles.** Applications call the OS resolver; the resolver contacts configured DNS servers. Source states DNS commonly uses UDP/53 and TCP/53 in cases requiring reliable transfer. `p0389:c01`–`p0391:c01`.
15. **Authoritative and cached answers differ.** A server is authoritative for records in its zone and may give non-authoritative answers from cache. Primary/secondary servers replicate zone data. `p0390:c01`–`p0391:c01`.
16. **DNS resolution can be iterative, recursive or mixed.** Recursive servers cache final results; root/TLD servers are described as returning referrals rather than performing recursion for lower clients. `p0391:c01`–`p0392:c01`.
17. **Reverse DNS reuses the DNS hierarchy by reversing IPv4 octets under `in-addr.arpa`.** Forward and reverse data are independently maintained and may become inconsistent. `p0393:c01`–`p0394:c01`.
18. **DHCP centralizes interface configuration.** It can supply address, mask, default router, DNS server and related parameters while preventing duplicate dynamic assignment within its managed pool. `p0394:c01`–`p0395:c01`.
19. **DHCP uses leases and can use a relay.** A relay lets one server serve clients in other subnets even though the initial client discovery is broadcast on the local subnet. `p0396:c01`–`p0397:c01`.
20. **Dynamic addressing has operational trade-offs.** The source explicitly notes problems for stable DNS naming, remote monitoring and address-based security policy; stable infrastructure endpoints may therefore need non-dynamic assignment. `p0398:c01`.

## Артефакты

- [cheatsheet.md](cheatsheet.md) — conceptual/operational cheatsheet v1.7.
- [commands.md](commands.md) — source-named utilities/protocol operations and safety boundary; no CLI syntax is invented.
- [diagram.md](diagram.md) — Mermaid map from application data to IP/link addressing plus ARP/DNS/DHCP support services.
- [visual-cheatsheet.svg](visual-cheatsheet.svg) — compact visual summary.
- [visual-cheatsheet-detailed.svg](visual-cheatsheet-detailed.svg) — detailed visual summary.
- [source-findings.md](source-findings.md) — extraction/provenance and historical/source-snapshot caveats.

## Conditional artifacts

- Отдельного явного chapter-end summary на PDF pp. 365–398 **не обнаружено** → `summary.md` не создаётся.
- Review/control questions или exercises внутри verified boundary **не обнаружены** → `review-questions.md` / `review-answers.md` не создаются.

## Ограничения источника

RAG contains repeated footer contamination, mixed Cyrillic/Latin glyphs in protocol names, degraded diagrams and some suspicious historical/numeric statements. Classful addressing, root-server counts and old address-resolution mechanisms are preserved as source context rather than silently modernized.
