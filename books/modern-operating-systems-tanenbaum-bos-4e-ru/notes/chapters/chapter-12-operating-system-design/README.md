# Глава 12 — Разработка операционных систем

Status: `RAG_GROUNDED`

Book: `modern-operating-systems-tanenbaum-bos-4e-ru`  
Edition: 4  
Chapter: 12 — «Разработка операционных систем»

## Scope and provenance

- Source mode: `rag_only`
- Canonical source format: PDF
- Canonical source SHA-256: `57b4906fe976351be3cc7ba692bdcee069036667b5f1d042517aea04d37a3bbd`
- PDF source locator range: `1058–1109`
- Addressable RAG chunk range: `p1058:c01 … p1109:c01`
- Chunks in chapter range: `52`
- Printed-page range: `[Needs confirmation]`
- Boundary verification:
  - PDF page 1058 begins with `Глава 12. Разработка операционных систем`;
  - PDF page 1110 begins with `Глава 13. Библиография`.
- Chapter boundary: `VERIFIED`

The explicit chapter-end summary begins on PDF page 1106. Review questions occupy PDF pages 1106–1109 and are explicitly numbered 1–28.

## Main principle

The chapter treats operating-system construction primarily as an engineering discipline rather than an exact science.

The recurring design rule is:

`clear goals → simple/complete/efficient interface → structured implementation → measured optimization → disciplined project management`.

The chapter repeatedly favors explicit boundaries, orthogonality, minimal mechanism, controlled complexity and measurement over feature accumulation or premature optimization.

## Chapter map

| Section | Topic | PDF pages |
|---|---|---:|
| 12.1 | Природа проблемы проектирования | 1058–1062 |
| 12.1.1 | Цели | 1058–1060 |
| 12.1.2 | Почему так сложно спроектировать операционную систему? | 1060–1062 |
| 12.2 | Разработка интерфейса | 1062–1071 |
| 12.2.1 | Руководящие принципы | 1062–1064 |
| 12.2.2 | Парадигмы | 1064–1068 |
| 12.2.3 | Интерфейс системных вызовов | 1068–1071 |
| 12.3 | Реализация | 1071–1089 |
| 12.3.1 | Структура системы | 1071–1075 |
| 12.3.2 | Механизм и политика | 1075–1076 |
| 12.3.3 | Ортогональность | 1076–1077 |
| 12.3.4 | Именование | 1077–1079 |
| 12.3.5 | Время связывания | 1079–1080 |
| 12.3.6 | Статические и динамические структуры | 1080–1081 |
| 12.3.7 | Реализация сверху вниз и снизу вверх | 1081–1082 |
| 12.3.8 | Синхронный и асинхронный обмен данными | 1082–1083 |
| 12.3.9 | Полезные методы | 1083–1089 |
| 12.4 | Производительность | 1089–1097 |
| 12.4.1 | Почему операционные системы такие медленные? | 1089–1090 |
| 12.4.2 | Что следует оптимизировать? | 1090–1091 |
| 12.4.3 | Скорость против памяти | 1091–1094 |
| 12.4.4 | Кэширование | 1094–1095 |
| 12.4.5 | Подсказки | 1095 |
| 12.4.6 | Использование локальности | 1095–1096 |
| 12.4.7 | Оптимизируйте общий случай | 1096–1097 |
| 12.5 | Управление проектом | 1097–1102 |
| 12.5.1 | Мифический человеко-месяц | 1097–1098 |
| 12.5.2 | Структура команды | 1098–1100 |
| 12.5.3 | Роль опыта | 1100–1101 |
| 12.5.4 | Панацеи нет | 1101–1102 |
| 12.6 | Тенденции в проектировании ОС | 1102–1106 |
| 12.6.1 | Виртуализация и облако | 1102 |
| 12.6.2 | Многоядерные микропроцессоры | 1103 |
| 12.6.3 | Большое адресное пространство | 1103–1104 |
| 12.6.4 | Беспрепятственный доступ к данным | 1104–1105 |
| 12.6.5 | Компьютеры с автономным питанием | 1105 |
| 12.6.6 | Встроенные системы | 1105–1106 |
| 12.7 | Краткие выводы | 1106 |
| — | Вопросы / упражнения | 1106–1109 |

## Key concepts

- **Goal definition:** design choices are meaningless without explicit system goals and target constraints.
- **Interface simplicity:** smaller interfaces are easier to understand, implement and verify.
- **Completeness:** an interface must still support the required work; minimality is not omission of essential capability.
- **Efficient implementation:** abstractions should not make implementation needlessly expensive.
- **Paradigm consistency:** user, execution and data models should form a coherent mental model.
- **Minimal mechanism:** expose a small set of primitive mechanisms and build richer behavior above them where practical.
- **Layering:** hide machine-specific detail low in the system and make upper layers progressively more machine-independent.
- **End-to-end argument / exokernel:** avoid duplicating work at lower layers when correctness must ultimately be checked at endpoints.
- **Microkernel client–server design:** move services and potentially drivers to isolated user processes, trading some performance for modularity and fault isolation.
- **Mechanism vs policy:** implement general mechanisms separately from changeable policy decisions.
- **Orthogonality:** unrelated properties should be controlled by unrelated mechanisms/parameters.
- **Naming / indirection:** stable symbolic names and indirection improve flexibility and reconfiguration.
- **Binding time:** decisions can be bound at compile, boot, load or run time; later binding increases flexibility but often adds cost.
- **Static vs dynamic structures:** fixed tables are simple and predictable; dynamic structures are flexible but more complex.
- **Synchronous vs asynchronous communication:** threads/blocking calls simplify sequential reasoning; event-driven designs reduce blocking but require explicit state tracking.
- **Hardware hiding:** convert awkward low-level events such as interrupts into cleaner abstractions where possible.
- **Conditional compilation:** keep one source base while isolating architecture-specific choices behind explicit configuration constants.
- **Reuse / reentrancy:** reusable primitives reduce code and testing scope; kernel routines must often tolerate concurrent or interrupted execution.
- **Error checks first:** validate failure conditions before acquiring resources to reduce cleanup complexity and leaks.
- **Premature optimization:** measure first; optimize the actual bottleneck rather than every code path.
- **Caching vs hints:** cache hits must be correct; hints may be stale and therefore require validation.
- **Locality:** exploit temporal/spatial locality in memory, storage and scheduling.
- **Common-case optimization:** fast path for frequent operations; rare path needs correctness more than peak speed.
- **Brooks' law / project scale:** communication, integration, planning and testing dominate large software projects; people and calendar time are not interchangeable.

## Operational interpretation

For engineering review, ask in this order:

`goal` → `interface` → `mechanism/policy split` → `dependency structure` → `failure isolation` → `measurement` → `optimization` → `project coordination`.

Do not confuse:

- minimal interface with incomplete interface;
- abstraction with hidden cost;
- mechanism with policy;
- a cache with a hint;
- reusable code with automatically reentrant code;
- more concurrency with simpler design;
- local optimization with system-level improvement;
- added developers with proportional schedule reduction;
- source-era predictions with current industry state.

## Historical scope

The chapter is explicitly more personal and speculative than earlier chapters. Predictions about hypervisors, many-core systems, battery-powered computers and embedded systems are preserved as the book's design perspective, not silently rewritten from current external knowledge.

## Artifacts

- [cheatsheet.md](cheatsheet.md)
- [commands.md](commands.md)
- [diagram.md](diagram.md)
- [visual-cheatsheet.svg](visual-cheatsheet.svg)
- [visual-cheatsheet-detailed.svg](visual-cheatsheet-detailed.svg)
- [summary.md](summary.md)
- [review-questions.md](review-questions.md)
- [review-answers.md](review-answers.md)
- [source-findings.md](source-findings.md)

## Limitations

- Figures/listings are grounded through the extracted text layer rather than independent multimodal extraction.
- Exercises that require implementation, timing measurements or current market prices remain partially `[Needs confirmation]`.
- The chapter contains design opinions and predictions; artifacts preserve that framing rather than converting opinion into universal fact.
- No external modernization is applied under `rag_only`.
