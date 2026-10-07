# Глава 11 — Отказоустойчивые и виртуальные локальные сети

Состояние артефактов: `RAG_GROUNDED`. Это **не** означает, что пользователь прочитал главу; reading state книги остаётся `planned`.

## Источник, границы и режим

- Книга: «Компьютерные сети. Принципы, технологии, протоколы», 7-е издание; Виктор Олифер, Наталья Олифер.
- `book_id: computer-networks-olifer-7e-ru-2026`.
- Канонический источник: `source/book.pdf`; SHA-256: `16f4b02985f65c602c6268620878cbacd692a61fd5898ca811b3d1a332e3f84d`.
- Source policy: **rag_only**; прямое чтение PDF, внешний web и модельная память не использовались как источник содержания главы.
- RAG boundary: `computer-networks-olifer-7e-ru-2026:p0326:c01` … `p0350:c01`.
- PDF pages: **326–350**, включительно; **25** адресуемых RAG chunks.
- Печатные страницы книги: **325–349**.
- На `p0326:c01` явно начинается «Глава 11. Отказоустойчивые и виртуальные локальные сети».
- На `p0351:c01` явно начинается «Глава 12. Ethernet операторского класса»; `p0351:c01` в scope главы 11 не входит.
- Chapter boundary: **VERIFIED**.
- BOOK-READINESS v1.3: `READY`; source/RAG generation, acceptance и checksum не менялись.
- Контракт: `BIBLIOTEKA-VSP-CHAPTER-ARTIFACT-COLLECTION v1.7`.

## Карта главы

| Раздел | PDF pages | RAG | Фокус |
| --- | ---: | --- | --- |
| STP / STA | 326–330 | `p0326:c01`–`p0330:c01` | loop-free spanning tree, root bridge, root/designated ports, BPDU, port states |
| RSTP | 331–332 | `p0331:c01`–`p0332:c01` | faster reconvergence, edge/alternative/backup roles, reduced timers/states |
| Фильтрация трафика | 332–334 | `p0332:c01`–`p0334:c01` | MAC-based access lists and limitations of L2 filtering |
| Агрегирование каналов | 334–339 | `p0334:c01`–`p0339:c01` | trunk/LAG, logical port, LAS, LACP, reliability + capacity |
| VLAN | 339–346 | `p0339:c01`–`p0346:c01` | broadcast-domain isolation, IEEE 802.1Q tag, access/trunk and flexible port models |
| Автоматизация VLAN | 347–348 | `p0347:c01`–`p0348:c01` | VTP, GVRP/GARP, MVRP/MRP |
| Альтернативные маршруты VLAN | 348–349 | `p0348:c01`–`p0349:c01` | MSTP and per-VLAN tree assignment |
| Ограничения L2 switching | 349–350 | `p0349:c01`–`p0350:c01` | topology, broadcast, filtering, addressing and heterogeneity limits |

Boundary anchors: [p0326:c01](../../../rag/chunks/p0301-p0400/p0326-c01.md) → [p0350:c01](../../../rag/chunks/p0301-p0400/p0350-c01.md) → [p0351:c01](../../../rag/chunks/p0301-p0400/p0351-c01.md).

## Главный принцип

**Надёжная Ethernet LAN требует одновременно контролировать петли, использовать избыточность и ограничивать broadcast-domain scope.** STP/RSTP превращает произвольную физическую избыточность в loop-free active topology; Link Aggregation оставляет несколько физических линий активными как один logical link; VLAN создаёт логические L2-границы; MSTP позволяет совместить VLAN-разделение с несколькими активными деревьями.

## Что важно вынести

1. **Transparent bridging требует loop-free active topology.** Альтернативные физические пути полезны для отказоустойчивости, но без loop-control приводят к циркуляции кадров. STP автоматически выбирает активное покрывающее дерево. `p0326:c01`–`p0330:c01`.
2. **STP строит дерево в три шага:** выбирает root bridge, root port каждого non-root switch и designated bridge/port для каждого segment. Остальные порты блокируются для user traffic. `p0328:c01`–`p0330:c01`.
3. **BPDU — control-plane frames STP.** Source описывает periodic HELLO/configuration BPDU и topology-change notifications; user frames and BPDU follow different forwarding rules while ports converge. `p0328:c01`–`p0330:c01`.
4. **Classic STP reconverges slowly.** Source показывает default-timer path to tens of seconds; RSTP removes listening, recognizes point-to-point/edge links and introduces alternate/backup roles to converge faster. `p0331:c01`–`p0332:c01`.
5. **L2 access filters are limited.** Source example permits/denies frames by source/destination MAC and applies the list to a port/direction; broadcast traffic and higher-layer semantics are not naturally handled by simple switch MAC filters. `p0332:c01`–`p0334:c01`.
6. **STP and Link Aggregation use redundancy differently.** STP places redundant links into hot standby; aggregation keeps all member links active, so it can improve both reliability and throughput. `p0334:c01`–`p0336:c01`.
7. **A LAG must appear as one logical link to upper protocols.** Source introduces Link Aggregation Sublayer (LAS), a logical aggregator port/MAC and the LAG group below it; STP should see the aggregate as one link. `p0336:c01`–`p0338:c01`.
8. **LACP forms and monitors dynamic aggregation groups.** If a member port/link fails, group membership can change and traffic continues over remaining members. `p0338:c01`–`p0339:c01`.
9. **VLAN = L2 isolation boundary including broadcast.** Frames do not cross from one VLAN to another based only on L2 switching; inter-VLAN communication requires network-layer functions. `p0339:c01`–`p0341:c01`.
10. **802.1Q carries VLAN identity between switches.** Source describes a 4-byte VLAN tag with outer EtherType `0x8100`, TCI priority/CFI/VID fields and a 12-bit VID. `p0343:c01`–`p0344:c01`.
11. **Access and trunk links have different frame expectations.** Access ports face end hosts and normally hide tags; trunks carry traffic of multiple VLANs between switches and preserve tags. `p0344:c01`–`p0346:c01`.
12. **MAC learning becomes VLAN-scoped.** Source states switches learn MAC addresses separately for each VLAN and filter forwarding by both destination state and VLAN membership. `p0346:c01`.
13. **VLAN control can be automated, but protocols differ.** VTP is Cisco-specific; GVRP is IEEE/GARP-based; MVRP replaced GVRP in the source narrative to reduce service traffic and convergence delay. `p0347:c01`–`p0348:c01`.
14. **MSTP allows several spanning trees for groups of VLANs.** Different VLANs can use different roots/trees to reduce the resource waste of one global spanning tree while retaining fast RSTP-based failure handling. `p0348:c01`–`p0349:c01`.
15. **Pure L2 scaling has structural limits.** The chapter ends by identifying constraints around topology, broadcast isolation, complex filtering, flat MAC addressing and heterogeneous protocol translation, motivating network-layer routing. `p0349:c01`–`p0350:c01`.

## Артефакты

- [cheatsheet.md](cheatsheet.md) — conceptual/operational cheatsheet v1.7.
- [commands.md](commands.md) — source-confirmed STP/LAG/VLAN mechanisms plus the chapter's generic ACL example; no vendor CLI is invented.
- [diagram.md](diagram.md) — Mermaid map of redundancy → loop control / aggregation → VLAN / MSTP.
- [visual-cheatsheet.svg](visual-cheatsheet.svg) — compact visual summary.
- [visual-cheatsheet-detailed.svg](visual-cheatsheet-detailed.svg) — detailed visual summary.
- [source-findings.md](source-findings.md) — extraction/provenance and source-snapshot caveats.

## Conditional artifacts

- Отдельного явного chapter-end summary на PDF pp. 326–350 **не обнаружено** → `summary.md` не создаётся.
- Review/control questions или exercises внутри verified boundary **не обнаружены** → `review-questions.md` и `review-answers.md` не создаются.

## Ограничения источника

RAG содержит footer contamination, OCR/glyph substitutions and degraded topology/tag diagrams. Timers, standard revisions, VLAN field terminology and vendor automation protocols are preserved as source snapshots; current platform behavior is not externally verified under `rag_only`.
