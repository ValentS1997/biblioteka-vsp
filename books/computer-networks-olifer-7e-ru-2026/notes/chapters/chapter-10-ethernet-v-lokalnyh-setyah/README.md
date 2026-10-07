# Глава 10 — Ethernet в локальных сетях

Состояние артефактов: `RAG_GROUNDED`. Это **не** означает, что пользователь прочитал главу; reading state книги остаётся `planned`.

## Источник, границы и режим

- Книга: «Компьютерные сети. Принципы, технологии, протоколы», 7-е издание; Виктор Олифер, Наталья Олифер.
- `book_id: computer-networks-olifer-7e-ru-2026`.
- Канонический источник: `source/book.pdf`; SHA-256: `16f4b02985f65c602c6268620878cbacd692a61fd5898ca811b3d1a332e3f84d`.
- Source policy: **rag_only**; прямое чтение PDF, внешний web и модельная память не использовались как источник содержания главы.
- RAG boundary: `computer-networks-olifer-7e-ru-2026:p0287:c01` … `p0325:c01`.
- PDF pages: **287–325**, включительно; **39** адресуемых RAG chunks.
- Печатные страницы книги: **286–324**.
- На `p0287:c01` явно начинается «Глава 10. Ethernet в локальных сетях».
- На `p0326:c01` явно начинается «Глава 11. Отказоустойчивые и виртуальные локальные сети»; `p0326:c01` в scope главы 10 не входит.
- Chapter boundary: **VERIFIED**.
- BOOK-READINESS v1.3: `READY`; source/RAG generation, acceptance и checksum не менялись.
- Контракт: `BIBLIOTEKA-VSP-CHAPTER-ARTIFACT-COLLECTION v1.7`.

## Карта главы

| Раздел | PDF pages | RAG | Фокус |
| --- | ---: | --- | --- |
| Первый этап — разделяемая среда | 287–298 | `p0287:c01`–`p0298:c01` | shared medium, IEEE 802 MAC/LLC, MAC addresses, Ethernet II frame, CSMA/CD, collision domain, 10M physical variants |
| Коммутируемый Ethernet | 299–312 | `p0299:c01`–`p0312:c01` | transparent bridge, self-learning forwarding table, flooding/filtering, loop problem, switches, duplex, nonblocking architecture |
| Скоростные версии Ethernet | 312–325 | `p0312:c01`–`p0325:c01` | modular PHY, autonegotiation, Fast/Gigabit/10G/40G/100G/200G/400G/800G, parallel lanes, PAM4/FEC, Ethernet over DWDM |

Boundary anchors: [p0287:c01](../../../rag/chunks/p0201-p0300/p0287-c01.md) → [p0325:c01](../../../rag/chunks/p0301-p0400/p0325-c01.md) → [p0326:c01](../../../rag/chunks/p0301-p0400/p0326-c01.md).

## Главный принцип

**Ethernet сохранил простой MAC/frame model, а масштабирование достигалось сменой среды доступа и постоянным усложнением физического уровня.** Исторически shared-medium Ethernet зависел от CSMA/CD и collision timing; современный Ethernet — это full-duplex switched network, где forwarding выполняется по MAC-table, а рост скорости достигается кодированием, параллельными lanes, FEC и более быстрыми PHY.

## Что важно вынести

1. **Shared medium фундаментально плохо масштабируется.** Capacity делится между всеми узлами, а при росте utilization резко увеличивается ожидание доступа. `p0287:c01`–`p0289:c01`.
2. **IEEE 802 разделяет функции LAN на physical, MAC и LLC.** MAC отвечает за доступ/доставку кадра по MAC address, LLC — за интерфейс с upper layer и исторически задуманные service modes. `p0290:c01`–`p0291:c01`.
3. **MAC addresses бывают individual/group/broadcast и globally/local administered.** Source описывает OUI-based assignment и promiscuous receive mode. `p0291:c01`–`p0292:c01`.
4. **Ethernet II frame остаётся базовой frame structure.** Destination/Source MAC, EtherType, payload 46–1500 bytes и FCS/CRC-32; minimum payload исторически связан с CSMA/CD collision detection. `p0292:c01`–`p0296:c01`.
5. **CSMA/CD работает только для shared half-duplex medium.** Station senses carrier, transmits, detects collision, sends jam sequence and retries after random backoff; after repeated failures frame can be dropped. `p0293:c01`–`p0296:c01`.
6. **Minimum frame and network diameter are coupled.** Sender must still be transmitting when worst-case collision propagates back; increasing bit rate therefore shrinks feasible shared-medium diameter unless MAC behavior changes. `p0295:c01`–`p0297:c01`.
7. **Hub gives physical star but one logical collision domain.** Repeater forwards bits to other ports and preserves shared-medium semantics. `p0297:c01`–`p0298:c01`.
8. **Bridge/switch performs logical segmentation.** It buffers frames and makes forwarding decisions instead of repeating bits. `p0299:c01`–`p0300:c01`.
9. **Transparent bridge self-learns from source MAC.** Known destination on another port → forward; known destination on same port → filter; unknown/broadcast/group → flood. Dynamic entries age out. `p0301:c01`–`p0304:c01`.
10. **Layer-2 loops are destructive without loop-control.** Broadcast/unknown frames duplicate/circulate and MAC learning oscillates; chapter 10 points forward to STP in chapter 11. `p0305:c01`–`p0306:c01`.
11. **Switch performance comes from parallel forwarding.** Microsegmentation plus per-port processing enables multiple simultaneous transfers; output contention still creates queues. `p0306:c01`–`p0308:c01`.
12. **Full duplex removes collision semantics.** In a point-to-point switch link both directions transmit simultaneously; 10G and faster Ethernet are source-described as full-duplex-only. `p0308:c01`–`p0309:c01`.
13. **Nonblocking is an architectural capacity property.** Port processors alone are insufficient; switch fabric, memory, bus and processing path must sustain aggregate load. `p0309:c01`–`p0311:c01`.
14. **High-speed Ethernet keeps MAC compatibility but modularizes PHY.** RS/PCS/PMA/PMD and xMII isolate MAC from media-specific coding/signaling. `p0312:c01`–`p0314:c01`.
15. **Autonegotiation chooses a mutually supported mode.** Source prioritizes higher bit rate, then full duplex where half duplex exists. `p0314:c01`.
16. **Fast and Gigabit Ethernet show continuity plus PHY innovation.** 4B/5B, MLT-3, 8B/10B, 4D-PAM5, multiple copper pairs and DSP are used to fit higher rates into available media. `p0315:c01`–`p0319:c01`.
17. **10G and 40/100G move fully to switched full duplex and parallel lanes.** 64B/66B and lane striping reduce per-lane requirements. `p0319:c01`–`p0321:c01`.
18. **200/400G introduce PAM4 + FEC as a practical scaling pair.** PAM4 doubles bits per symbol relative to NRZ, while Reed–Solomon FEC compensates the increased error sensitivity. `p0321:c01`–`p0323:c01`.
19. **Later 400G/800G reduce lane count by raising per-lane symbol rate.** Source also describes coherent Ethernet/DWDM interfaces as a different cost/reach trade-off. `p0324:c01`–`p0325:c01`.

## Артефакты

- [cheatsheet.md](cheatsheet.md) — conceptual/operational cheatsheet v1.7.
- [commands.md](commands.md) — source-confirmed Ethernet mechanisms/components; executable CLI в главе отсутствует.
- [diagram.md](diagram.md) — Mermaid-карта shared Ethernet → learning switch → high-speed PHY.
- [visual-cheatsheet.svg](visual-cheatsheet.svg) — компактная визуальная схема.
- [visual-cheatsheet-detailed.svg](visual-cheatsheet-detailed.svg) — подробная визуальная схема.
- [source-findings.md](source-findings.md) — extraction/provenance и source-snapshot findings.

## Conditional artifacts

- Отдельного явного chapter-end summary на PDF pp. 287–325 **не обнаружено** → `summary.md` не создаётся.
- Review/control questions или exercises внутри verified boundary **не обнаружены** → `review-questions.md` и `review-answers.md` не создаются.

## Ограничения источника

RAG содержит footer contamination, OCR/glyph substitutions и частично деградированные схемы/tables. High-speed standard rates, reach and “current/future” statements remain source snapshots of the edition and are not externally updated under `rag_only`.
