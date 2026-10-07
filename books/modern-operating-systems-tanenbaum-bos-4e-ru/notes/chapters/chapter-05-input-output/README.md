# Глава 5 — Ввод и вывод информации

Status: `RAG_GROUNDED`

Book: `modern-operating-systems-tanenbaum-bos-4e-ru`  
Edition: 4  
Chapter: 5 — «Ввод и вывод информации»

## Scope and provenance

- Source mode: `rag_only`
- Canonical source format: PDF
- Canonical source SHA-256: `57b4906fe976351be3cc7ba692bdcee069036667b5f1d042517aea04d37a3bbd`
- PDF source locator range: `380–487`
- Addressable RAG chunk range: `p0380:c01 … p0487:c01`
- Chunks in chapter range: `108`
- Printed-page range: `[Needs confirmation]`
- Boundary verification:
  - PDF page 380 begins with `Глава 5. Ввод и вывод информации`;
  - PDF page 488 begins with `Глава 6. Взаимоблокировка`.
- Chapter boundary: `VERIFIED`

The explicit chapter-end summary begins on PDF page 479 and continues onto page 480. Review questions/exercises occupy PDF pages 480–487 and are explicitly numbered 1–56.

## Main principle

The chapter presents I/O as a layered translation problem:

`application request → device-independent interface → device driver → controller/DMA → physical device → interrupt/completion → application`.

The operating system hides device-specific mechanics while preserving four concerns: correctness, isolation, performance and recoverability.

## Chapter map

| Section | Topic | PDF pages |
|---|---|---:|
| 5.1 | Основы аппаратного обеспечения ввода-вывода | 380–395 |
| 5.1.1 | Устройства ввода-вывода | 381–382 |
| 5.1.2 | Контроллеры устройств | 382–383 |
| 5.1.3 | Ввод-вывод, отображаемый на пространство памяти | 383–387 |
| 5.1.4 | Прямой доступ к памяти (DMA) | 387–391 |
| 5.1.5 | Еще раз о прерываниях | 391–395 |
| 5.2 | Принципы создания ПО ввода-вывода | 395–400 |
| 5.2.1 | Задачи ПО ввода-вывода | 395–397 |
| 5.2.2 | Программный ввод-вывод | 397–398 |
| 5.2.3 | Ввод-вывод, управляемый прерываниями | 398–399 |
| 5.2.4 | Ввод-вывод с использованием DMA | 399–400 |
| 5.3 | Уровни программного обеспечения ввода-вывода | 400–414 |
| 5.3.1 | Обработчики прерываний | 400–402 |
| 5.3.2 | Драйверы устройств | 402–406 |
| 5.3.3 | Независимое от устройств ПО ввода-вывода | 406–412 |
| 5.3.4 | Пользовательское ПО ввода-вывода | 412–414 |
| 5.4 | Диски | 414–435 |
| 5.4.1 | Аппаратная часть дисков, RAID | 414–421 |
| 5.4.2 | Форматирование диска | 421–425 |
| 5.4.3 | Планирование перемещения головок | 425–429 |
| 5.4.4 | Обработка ошибок | 429–432 |
| 5.4.5 | Стабильное хранилище данных | 432–435 |
| 5.5 | Часы | 435–442 |
| 5.5.1 | Аппаратная составляющая часов | 436–437 |
| 5.5.2 | Программное обеспечение часов | 437–440 |
| 5.5.3 | Программируемые таймеры | 440–442 |
| 5.6 | Пользовательский интерфейс: клавиатура, мышь, монитор | 442–466 |
| 5.6.1 | Программное обеспечение ввода | 442–448 |
| 5.6.2 | Программное обеспечение вывода | 448–466 |
| 5.7 | Тонкие клиенты | 466–467 |
| 5.8 | Управление энергопотреблением | 467–477 |
| 5.8.1 | Роль оборудования | 468–470 |
| 5.8.2 | Роль операционной системы | 470–476 |
| 5.8.2 | Роль прикладных программ | 476–477 |
| 5.9 | Исследования в области ввода-вывода | 477–479 |
| 5.10 | Краткие выводы | 479–480 |
| — | Вопросы / упражнения | 480–487 |

The duplicate `5.8.2` numbering is preserved from the source and registered in `source-findings.md`.

## Key concepts

- **Block vs character device:** block devices expose independently addressable fixed-size blocks; character devices expose streams without block addressing.
- **Device controller:** translates low-level device signals into registers, buffers, status and error information usable by the OS.
- **Port-mapped vs memory-mapped I/O:** control registers may live in a separate I/O-port space or be mapped into memory addresses; MMIO requires careful cache treatment.
- **DMA:** transfers a block between a controller and memory with minimal CPU involvement and normally one interrupt per completed buffer.
- **Precise interrupt:** presents a well-defined restartable CPU state; imprecise interrupts push recovery complexity into the OS.
- **Device independence:** upper layers use uniform naming, protection, logical block sizes and error semantics instead of device-specific command sequences.
- **I/O layers:** interrupt handlers → device drivers → device-independent I/O software → user-space libraries/spooling.
- **Buffering:** kernel buffers, double buffering and ring buffers decouple producer/consumer timing but excessive copying costs throughput.
- **Spooling:** queues work for exclusive devices such as printers so user processes do not monopolize them.
- **RAID:** striping, mirroring and parity trade capacity, read/write performance and fault tolerance.
- **Disk scheduling:** FCFS is fair by arrival; SSF reduces seek but may starve distant requests; elevator balances seek efficiency and bounded service.
- **Stable storage:** paired disks plus verified writes/reads and deterministic recovery aim to make a write appear either completed or not performed.
- **Clock driver:** maintains time, process quanta, CPU accounting, alarms, watchdogs and profiling.
- **Canonical/noncanonical terminal input:** the driver may edit a line before delivery or expose a less processed character stream.
- **X/GUI event model:** graphical systems route keyboard/mouse/window events to applications; X separates client, server and window manager.
- **Power management:** OS and applications trade wake-up latency, performance and quality against energy use.

## Operational interpretation

When I/O misbehaves, first classify the failing layer:

`application/API` ≠ `buffering/spooling` ≠ `device-independent layer` ≠ `driver` ≠ `interrupt/DMA` ≠ `controller/bus` ≠ `physical media`.

Examples:

- high CPU during slow I/O may indicate polling/busy waiting rather than device throughput;
- data loss under load can be a buffer/bus timing problem rather than an application logic problem;
- disk latency can come from seek scheduling even when transfer bandwidth is high;
- an I/O error should be handled at the lowest layer able to recover it and propagated only when lower layers cannot;
- stable-storage recovery and RAID address different failure models and must not be treated as interchangeable.

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

- Figures/tables are referenced through text RAG and are not independently encoded as multimodal objects.
- Exact answers that depend on an unavailable graphical layout or on an unstated device parameter remain `[Needs confirmation]`.
- Programming exercises that require compilation/execution retain `[Needs confirmation]` for empirical results.
- Hardware/product/version examples are preserved as chapter content and are not modernized with external information.
- Source inconsistencies are registered explicitly rather than silently corrected.
