# Глава 4 — Стандартизация и классификация сетей

Состояние артефактов: `RAG_GROUNDED`. Это **не** означает, что пользователь прочитал главу; reading state книги остаётся `planned`.

## Источник, границы и режим

- Книга: «Компьютерные сети. Принципы, технологии, протоколы», 7-е издание; Виктор Олифер, Наталья Олифер.
- `book_id: computer-networks-olifer-7e-ru-2026`.
- Канонический источник: `source/book.pdf`; SHA-256: `16f4b02985f65c602c6268620878cbacd692a61fd5898ca811b3d1a332e3f84d`.
- Source policy: **rag_only**; прямое чтение PDF, внешний web и модельная память не использовались как источник содержания главы.
- RAG boundary: `computer-networks-olifer-7e-ru-2026:p0108:c01` … `p0130:c01`.
- PDF pages: **108–130**, включительно; **25** адресуемых RAG chunks.
- Печатные страницы книги: **107–129**.
- На `p0108:c01` явно начинается «Глава 4. Стандартизация и классификация сетей».
- На `p0131:c01` явно начинается «Глава 5. Сетевые характеристики и качество обслуживания»; `p0131:c01` в scope главы 4 не входит.
- Chapter boundary: **VERIFIED**.
- BOOK-READINESS v1.3: `READY`; source/RAG generation, acceptance и checksum не менялись.
- Контракт: `BIBLIOTEKA-VSP-CHAPTER-ARTIFACT-COLLECTION v1.7`.

## Карта главы

| Раздел | PDF pages | RAG | Фокус |
| --- | ---: | --- | --- |
| Декомпозиция сетевого взаимодействия | 108–111 | `p0108:c01`–`p0111:c01` | Модули, уровни, интерфейсы услуг, protocol vs interface, protocol stack |
| Модель OSI | 112–121 | `p0112:c01`–`p0121:c01` | Семь уровней, encapsulation, распределение функций между end/transit nodes, user/control/management planes |
| Стандартизация сетей | 122–126 | `p0122:c01`–`p0126:c01` | Open systems/specifications, sources of standards, RFC/IETF, TCP/IP stack |
| Классификация компьютерных сетей | 126–130 | `p0126:c01`–`p0130:c01` | LAN/WAN/MAN, wired/wireless, switching, topology, users, access/aggregation/backbone, primary/overlay networks |

Boundary anchors: [p0108:c01](../../../rag/chunks/p0101-p0200/p0108-c01.md) → [p0130:c01](../../../rag/chunks/p0101-p0200/p0130-c01.md) → [p0131:c01](../../../rag/chunks/p0101-p0200/p0131-c01.md).

## Главный принцип

**Стандартизация делает многоуровневую декомпозицию практически совместимой между разными реализациями.** Сначала сложная задача сетевого взаимодействия разбивается на уровни с формально определёнными интерфейсами и peer protocols; затем стандарты фиксируют общие правила, позволяя независимым реализациям взаимодействовать. Классификация, в свою очередь, показывает, что одна и та же реальная сеть одновременно принадлежит нескольким классам по разным признакам.

## Что важно вынести

1. **Interface и protocol описывают разные направления взаимодействия.** Interface связывает соседние уровни в одном узле; protocol задаёт правила взаимодействия peer entities одного уровня на разных узлах. `p0109:c01`–`p0111:c01`.
2. **Protocol stack — иерархически организованный набор протоколов, достаточный для взаимодействия узлов.** Модель описывает «что», protocol — «как», implementation — конкретную реализацию. `p0111:c01`–`p0116:c01`.
3. **OSI — reference model, а не утверждение, что любой реальный stack обязан буквально иметь семь отдельных protocol modules.** Источник отдельно отмечает трудности идеальной layer decomposition. `p0112:c01`–`p0121:c01`.
4. **OSI layers имеют разные scopes.** Physical передаёт signals/bits; data link работает между соседними узлами с frames; network — между произвольными конечными узлами; transport даёт нужный уровень transport service; session/presentation/application обслуживают higher-level interaction. `p0113:c01`–`p0115:c01`.
5. **Encapsulation — следствие layered hierarchy.** Сообщение идёт вниз по stack, обрастая service information; на receiving node headers обрабатываются и снимаются при движении вверх. `p0116:c01`–`p0118:c01`.
6. **Полный stack нужен конечным узлам, а transit devices используют только необходимые lower layers.** Repeater/hub — physical; LAN switch — physical + data link; router — physical + data link + network. `p0118:c01`–`p0119:c01`.
7. **Vertical OSI layering недостаточно для service protocols.** Глава добавляет horizontal view: user plane, control plane и management plane. `p0119:c01`–`p0121:c01`.
8. **Open system строится на опубликованных общедоступных specifications, принятых на основе согласия.** Это даёт interoperability, заменяемость компонентов и возможность соединять сети. `p0122:c01`–`p0123:c01`.
9. **Standards имеют разные источники и статус.** В главе различаются vendor, committee/association, national и international standards; интернет-стандартизация описана через RFC и IETF ecosystem. `p0123:c01`–`p0124:c01`.
10. **TCP/IP представлен как practically dominant family with IP as narrow waist.** Верхние и нижние protocol choices могут меняться, но IP связывает разнородные stacks. `p0124:c01`–`p0126:c01`.
11. **Classification is multi-axis.** Сеть одновременно классифицируется по territory, medium, switching method, topology, user type, functional role и relation primary/overlay. `p0126:c01`–`p0130:c01`.

## Артефакты

- [cheatsheet.md](cheatsheet.md) — conceptual/operational cheatsheet v1.7.
- [commands.md](commands.md) — source-confirmed protocols/standards/components; исполняемых CLI-команд в главе нет.
- [diagram.md](diagram.md) — Mermaid-карта layering → standardization → classification.
- [visual-cheatsheet.svg](visual-cheatsheet.svg) — компактная визуальная схема.
- [visual-cheatsheet-detailed.svg](visual-cheatsheet-detailed.svg) — подробная визуальная схема.
- [source-findings.md](source-findings.md) — extraction/provenance ограничения главы.

## Conditional artifacts

- Отдельное явное chapter-end summary на PDF pp. 108–130 **не обнаружено** → `summary.md` не создаётся.
- Review/control questions или exercises внутри границы главы **не обнаружены** → `review-questions.md` и `review-answers.md` не создаются.

## Ограничения источника

RAG содержит повторяющийся посторонний footer/URL, OCR/glyph substitutions и неполное текстовое представление многоуровневых diagrams. Исторические/организационные утверждения о стандартизации сохранены как утверждения книги и не проверялись внешне из-за `rag_only` policy.
