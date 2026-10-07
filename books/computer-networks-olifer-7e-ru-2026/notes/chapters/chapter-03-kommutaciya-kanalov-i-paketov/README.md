# Глава 3 — Коммутация каналов и пакетов

Состояние артефактов: `RAG_GROUNDED`. Это **не** означает, что пользователь прочитал главу; reading state книги остаётся `planned`.

## Источник, границы и режим

- Книга: «Компьютерные сети. Принципы, технологии, протоколы», 7-е издание; Виктор Олифер, Наталья Олифер.
- `book_id: computer-networks-olifer-7e-ru-2026`.
- Канонический источник: `source/book.pdf`; SHA-256: `16f4b02985f65c602c6268620878cbacd692a61fd5898ca811b3d1a332e3f84d`.
- Source policy: **rag_only**; прямое чтение PDF, внешний web и модельная память не использовались как источник содержания главы.
- RAG boundary: `computer-networks-olifer-7e-ru-2026:p0081:c01` … `p0107:c01`.
- PDF pages: **81–107**, включительно; **28** адресуемых RAG chunks.
- Печатные страницы книги: **80–106**.
- На `p0081:c01` явно начинается «Глава 3. Коммутация каналов и пакетов».
- На `p0108:c01` явно начинается «Глава 4. Стандартизация и классификация сетей»; `p0108:c01` в scope главы 3 не входит.
- Chapter boundary: **VERIFIED**.
- BOOK-READINESS v1.3: `READY`; source/RAG generation, acceptance и checksum не менялись.
- Контракт: `BIBLIOTEKA-VSP-CHAPTER-ARTIFACT-COLLECTION v1.7`.

## Карта главы

| Раздел | PDF pages | RAG | Фокус |
| --- | ---: | --- | --- |
| Коммутация каналов | 81–88 | `p0081:c01`–`p0088:c01` | Элементарный и составной канал, резервирование, установление соединения, детерминированная передача |
| Коммутация пакетов | 89–98 | `p0089:c01`–`p0098:c01` | Пакеты, headers, store-and-forward, buffering/queues, три способа продвижения |
| Дейтаграммная передача | 93–94 | `p0093:c01`–`p0094:c01` | Независимая обработка пакетов, best effort, возможные разные маршруты |
| Логическое соединение | 95–96 | `p0095:c01`–`p0096:c01` | Согласование параметров, state на конечных узлах, reliability/security features |
| Виртуальный канал | 97–98 | `p0097:c01`–`p0098:c01` | Фиксированный путь, метка потока, shorter forwarding state |
| Сравнение каналов и пакетов | 99–105 | `p0099:c01`–`p0105:c01` | Resource efficiency, delay structure, quantitative example |
| Ethernet как packet-switching technology | 105–107 | `p0105:c01`–`p0107:c01` | Shared vs switched Ethernet, datagram forwarding, MAC, checksum, queues |

Boundary anchors: [p0081:c01](../../../rag/chunks/p0001-p0100/p0081-c01.md) → [p0107:c01](../../../rag/chunks/p0101-p0200/p0107-c01.md) → [p0108:c01](../../../rag/chunks/p0101-p0200/p0108-c01.md).

## Главный принцип

**Коммутация каналов и коммутация пакетов по-разному распределяют сетевой ресурс во времени.** Channel switching сначала резервирует фиксированную полосу на всём пути и затем даёт предсказуемый поток; packet switching делит ресурсы динамически между пакетами, повышая эффективность для пульсирующего трафика ценой очередей, переменных задержек и возможных потерь.

## Что важно вынести

1. **Channel switching начинается с reservation.** На всём маршруте выделяется одинаковое число элементарных каналов; из них формируется составной канал с фиксированной пропускной способностью. `p0082:c01`–`p0086:c01`.
2. **Соединение может быть отклонено до передачи данных.** Если на любом участке нет свободного elementary channel, сеть отказывает в установлении соединения. `p0085:c01`–`p0087:c01`.
3. **Channel switching детерминирован после setup.** Ресурс закреплён эксклюзивно, поэтому данные передаются без очередей, характерных для packet switching, но ресурс простаивает во время пауз bursty traffic. `p0087:c01`–`p0089:c01`.
4. **Packet switching дробит сообщение на пакеты.** Каждый пакет несёт служебную информацию, а сеть не резервирует заранее end-to-end capacity. `p0089:c01`–`p0091:c01`.
5. **Buffers — обязательная часть packet switch.** Store-and-forward, согласование скоростей и конкуренция за output interface создают queues; переполнение buffer может привести к потере пакетов. `p0092:c01`–`p0093:c01`.
6. **Три packet-forwarding модели различаются amount of state.** Datagram: каждый пакет независим; logical connection: endpoints хранят состояние обмена; virtual circuit: ещё и путь фиксирован, а packet carries a label вместо полного destination address. `p0093:c01`–`p0098:c01`.
7. **Virtual circuit ≠ circuit switching.** Несмотря на setup, по virtual circuit идут отдельные packets, а не непрерывный поток с зарезервированной постоянной скоростью. `p0098:c01`.
8. **Packet switching эффективнее использует ресурс для bursty traffic, но latency stochastic.** Channel switching жертвует utilization ради предсказуемости; packet switching — наоборот. `p0099:c01`–`p0104:c01`.
9. **Delay надо раскладывать по компонентам.** Источник отделяет propagation, serialization, packetization, buffering/queueing и switching time; именно queueing делает packet delay заранее неопределённой. `p0100:c01`–`p0104:c01`.
10. **Ethernet — конкретизация packet-switching principles.** Глава рассматривает shared-medium и switched variants, datagram forwarding, MAC addressing, checksum и queues. `p0105:c01`–`p0107:c01`.

## Артефакты

- [cheatsheet.md](cheatsheet.md) — conceptual/operational cheatsheet v1.7.
- [commands.md](commands.md) — source-confirmed mechanisms/technologies; исполняемых CLI-команд в главе нет.
- [diagram.md](diagram.md) — Mermaid-сравнение channel switching и packet switching.
- [visual-cheatsheet.svg](visual-cheatsheet.svg) — компактная визуальная схема.
- [visual-cheatsheet-detailed.svg](visual-cheatsheet-detailed.svg) — подробная визуальная схема.
- [source-findings.md](source-findings.md) — extraction/provenance ограничения главы.

## Conditional artifacts

- Отдельное явное chapter-end summary на PDF pp. 81–107 **не обнаружено** → `summary.md` не создаётся.
- Review/control questions или exercises внутри границы главы **не обнаружены** → `review-questions.md` и `review-answers.md` не создаются.

## Ограничения источника

RAG содержит повторяющийся посторонний footer/URL, OCR/glyph substitutions и частично деградировавшие формулы/схемы. Они перечислены в [source-findings.md](source-findings.md) и не используются для молчаливой реконструкции точных формул или рисунков.
