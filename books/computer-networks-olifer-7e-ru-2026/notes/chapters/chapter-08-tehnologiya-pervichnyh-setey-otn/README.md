# Глава 8 — Технология первичных сетей OTN

Состояние артефактов: `RAG_GROUNDED`. Это **не** означает, что пользователь прочитал главу; reading state книги остаётся `planned`.

## Источник, границы и режим

- Книга: «Компьютерные сети. Принципы, технологии, протоколы», 7-е издание; Виктор Олифер, Наталья Олифер.
- `book_id: computer-networks-olifer-7e-ru-2026`.
- Канонический источник: `source/book.pdf`; SHA-256: `16f4b02985f65c602c6268620878cbacd692a61fd5898ca811b3d1a332e3f84d`.
- Source policy: **rag_only**; прямое чтение PDF, внешний web и модельная память не использовались как источник содержания главы.
- RAG boundary: `computer-networks-olifer-7e-ru-2026:p0242:c01` … `p0267:c01`.
- PDF pages: **242–267**, включительно; **30** адресуемых RAG chunks.
- Печатные страницы книги: **241–266**.
- На `p0242:c01` явно начинается «Глава 8. Технология первичных сетей OTN».
- На `p0268:c01` явно начинается «Глава 9. Технология первичных сетей DWDM»; `p0268:c01` в scope главы 8 не входит.
- Chapter boundary: **VERIFIED**.
- BOOK-READINESS v1.3: `READY`; source/RAG generation, acceptance и checksum не менялись.
- Контракт: `BIBLIOTEKA-VSP-CHAPTER-ARTIFACT-COLLECTION v1.7`.

## Карта главы

| Раздел | PDF pages | RAG | Фокус |
| --- | ---: | --- | --- |
| Особенности первичных сетей | 242–250 | `p0242:c01`–`p0250:c01` | circuit-switched transport, static point-to-point channels, overlay role, TDM topology/equipment, load and multiplexer functions |
| PDH и SDH | 250–253 | `p0250:c01`–`p0253:c01` | bit stuffing, limitations of PDH, SDH hierarchy/pointers/topologies/failover |
| Причины создания OTN | 254–255 | `p0254:c01`–`p0255:c01` | SDH limitations for high-rate/computer traffic and DWDM integration |
| Иерархия и функциональные уровни OTN | 255–257 | `p0255:c01`–`p0257:c01` | OPU / ODU / OTU, speed hierarchy, O-E-O processing |
| Формат кадра OTN и FEC | 257–259 | `p0257:c01`–`p0259:c01` | fixed-size OTN frame, headers, FEC, variable frame transmission time |
| Отображение пользовательских данных | 259–260 | `p0259:c01`–`p0260:c01` | synchronous vs asynchronous clients, GFP-F/GFP-T, rate alignment |
| Мультиплексирование OTN | 261–265 | `p0261:c01`–`p0265:c01` | ODU→OPU, tributary slots, PSI, ODU0/2e/4/Cn/Flex, GMP |
| Организация сетей OTN | 265–267 | `p0265:c01`–`p0267:c01` | transponder → muxponder → OTN cross-connect / switching over DWDM |

Boundary anchors: [p0242:c01](../../../rag/chunks/p0201-p0300/p0242-c01.md) → [p0267:c01](../../../rag/chunks/p0201-p0300/p0267-c01.md) → [p0268:c01](../../../rag/chunks/p0201-p0300/p0268-c01.md).

## Главный принцип

**OTN — это статически provisioned transport network, которая превращает разнородные клиентские потоки в иерархию фиксированных транспортных блоков и передаёт их через оптическую инфраструктуру с встроенными функциями monitoring, multiplexing, switching и FEC.** Это не packet routing system: path/channel state задаётся заранее, а пользовательские данные должны быть отображены и выровнены под непрерывный транспортный поток.

## Что важно вынести

1. **Первичная сеть предоставляет transport channel, а не packet forwarding.** Каналы статические, point-to-point и служат основой для overlay computer/telephone networks. `p0242:c01`–`p0243:c01`.
2. **Topology equipment differs from packet networks.** Source выделяет terminal multiplexer, ADM, DXC/cross-connect and regenerators; tributary ports feed aggregate/line ports. `p0244:c01`–`p0246:c01`.
3. **Load must be known before provisioning.** Multiplexer tables define which tributary stream maps to which aggregate time slots/ports; lack of capacity can make a requested circuit impossible rather than merely slower. `p0246:c01`–`p0247:c01`.
4. **TDM frame semantics differ from packet frames.** OTN/SDH frames slice a continuous synchronous stream; they are not independently routed packets. `p0248:c01`–`p0250:c01`.
5. **PDH bit stuffing solved slight rate mismatch but harmed add/drop flexibility.** SDH introduced pointers/virtual containers and easier extraction, while keeping a 125 μs cycle and hierarchical rates. `p0250:c01`–`p0253:c01`.
6. **OTN was introduced to handle larger units, computer traffic and tighter DWDM integration.** Source also highlights standardized FEC as an important improvement over SDH. `p0254:c01`–`p0255:c01`.
7. **OTN has three key electrical functional blocks plus a photonic layer:** OPU maps client data; ODU provides end-to-end transport/monitoring and multiplexing; OTU handles adjacent-node transport and FEC before the photonic/DWDM layer. `p0256:c01`–`p0257:c01`.
8. **OTN frame architecture differs from SDH.** OTN keeps a fixed frame size while transmission time decreases as hierarchy rate rises; SDH keeps a fixed 125 μs period while frame size grows with rate. `p0257:c01`–`p0258:c01`.
9. **FEC is part of OTU transport.** Source describes Reed–Solomon RS(255,239) and gives quantitative gain/error-rate examples; these are preserved as source claims, not universal deployment guarantees. `p0258:c01`.
10. **Client transparency is primarily an OPU concern.** Synchronous streams and bursty computer frames use different mapping/alignment procedures. GFP provides a generic envelope for computer/network traffic; GFP-F and GFP-T serve different traffic forms. `p0259:c01`–`p0260:c01`.
11. **Multiplexing uses tributary slots and payload-structure metadata.** ODU blocks are byte-interleaved into higher-level OPU fields; PSI describes slot assignment and supports demultiplexing/switching. `p0261:c01`–`p0263:c01`.
12. **The hierarchy evolved with client rates.** Source describes ODU0, ODU2e, ODU4, ODUCn, ODUFlex and GMP as responses to Ethernet and arbitrary-rate client traffic. `p0263:c01`–`p0265:c01`.
13. **Network architecture evolved from “digital wrapper” to switching fabric.** Early OTN/DWDM used transponders, then muxponders, and later OTN cross-connects capable of transit switching between tributary and aggregate ports. `p0265:c01`–`p0267:c01`.

## Артефакты

- [cheatsheet.md](cheatsheet.md) — conceptual/operational cheatsheet v1.7.
- [commands.md](commands.md) — source-confirmed OTN blocks/equipment/mechanisms; executable CLI в главе отсутствует.
- [diagram.md](diagram.md) — Mermaid-карта client → OPU → ODU → OTU → DWDM.
- [visual-cheatsheet.svg](visual-cheatsheet.svg) — компактная визуальная схема.
- [visual-cheatsheet-detailed.svg](visual-cheatsheet-detailed.svg) — подробная визуальная схема.
- [source-findings.md](source-findings.md) — extraction/provenance и source-snapshot findings.

## Conditional artifacts

- Отдельного явного chapter-end summary на PDF pp. 242–267 **не обнаружено** → `summary.md` не создаётся.
- Review/control questions или exercises внутри verified boundary **не обнаружены** → `review-questions.md` и `review-answers.md` не создаются.

## Ограничения источника

RAG содержит footer contamination, OCR/glyph substitutions и потерю spatial semantics у frame/multiplexing diagrams. Rates, standard identifiers, FEC gains, restoration times and technology-status claims трактуются как source snapshot и не проверяются внешне в `rag_only` режиме.
