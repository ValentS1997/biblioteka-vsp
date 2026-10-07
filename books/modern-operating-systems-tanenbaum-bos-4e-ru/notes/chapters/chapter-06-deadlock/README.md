# Глава 6 — Взаимоблокировка

Status: `RAG_GROUNDED`

Book: `modern-operating-systems-tanenbaum-bos-4e-ru`  
Edition: 4  
Chapter: 6 — «Взаимоблокировка»

## Scope and provenance

- Source mode: `rag_only`
- Canonical source format: PDF
- Canonical source SHA-256: `57b4906fe976351be3cc7ba692bdcee069036667b5f1d042517aea04d37a3bbd`
- PDF source locator range: `488–526`
- Addressable RAG chunk range: `p0488:c01 … p0526:c01`
- Chunks in chapter range: `39`
- Printed-page range: `[Needs confirmation]`
- Boundary verification:
  - PDF page 488 begins with `Глава 6. Взаимоблокировка`;
  - PDF page 527 begins with `Глава 7. Виртуализация и облако`.
- Chapter boundary: `VERIFIED`

The explicit chapter-end summary begins on PDF page 519 and continues on page 520. Review questions/exercises occupy PDF pages 520–526 and are explicitly numbered 1–45.

## Main principle

A deadlock is not simply "a process is waiting." It is a dependency structure in which no participant can cause the event needed by another participant to make progress.

For resource deadlocks the operational model is:

`resource ownership + pending requests → wait-for dependency → cycle / unsatisfied set → no forward progress`.

The chapter separates four strategies: ignore, detect/recover, avoid unsafe states, or prevent one Coffman condition from becoming true.

## Chapter map

| Section | Topic | PDF pages |
|---|---|---:|
| 6.1 | Ресурсы | 489–492 |
| 6.1.1 | Выгружаемые и невыгружаемые ресурсы | 489–490 |
| 6.1.2 | Получение ресурса | 490–492 |
| 6.2 | Введение во взаимоблокировки | 492–496 |
| 6.2.1 | Условия возникновения ресурсных взаимоблокировок | 493 |
| 6.2.2 | Моделирование взаимоблокировок | 493–496 |
| 6.3 | Страусиный алгоритм | 496–497 |
| 6.4 | Обнаружение взаимоблокировок и восстановление | 497–504 |
| 6.4.1 | Обнаружение: один ресурс каждого типа | 497–499 |
| 6.4.2 | Обнаружение: несколько ресурсов каждого типа | 499–502 |
| 6.4.3 | Выход из взаимоблокировки | 502–504 |
| 6.5 | Уклонение от взаимоблокировок | 504–510 |
| 6.5.1 | Траектории ресурса | 504–506 |
| 6.5.2 | Безопасное и небезопасное состояние | 506–507 |
| 6.5.3 | Алгоритм банкира для одного ресурса | 507–508 |
| 6.5.4 | Алгоритм банкира для нескольких типов ресурсов | 508–510 |
| 6.6 | Предотвращение взаимоблокировки | 510–513 |
| 6.6.1 | Атака условия взаимного исключения | 510–511 |
| 6.6.2 | Атака условия удержания и ожидания | 511–512 |
| 6.6.3 | Атака условия невыгружаемости | 512 |
| 6.6.4 | Атака условия циклического ожидания | 512–513 |
| 6.7 | Другие вопросы | 513–518 |
| 6.7.1 | Двухфазное блокирование | 513–514 |
| 6.7.2 | Взаимные блокировки при обмене данными | 514–516 |
| 6.7.3 | Активная взаимоблокировка | 516–518 |
| 6.7.4 | Зависание | 518 |
| 6.8 | Исследования в области взаимоблокировок | 518–519 |
| 6.9 | Краткие выводы | 519–520 |
| — | Вопросы / упражнения | 520–526 |

## Key concepts

- **Preemptable resource:** can be taken away without destroying the computation; memory may be preemptable when swapping/paging exists.
- **Nonpreemptable resource:** cannot be safely removed from its owner mid-operation; these resources dominate classic deadlocks.
- **Resource lifecycle:** request → use → release.
- **Resource deadlock:** every process in a set waits for a resource held by another process in that set.
- **Coffman conditions:** mutual exclusion, hold-and-wait, no preemption, circular wait.
- **Resource-allocation graph:** process/resource nodes and directed request/assignment edges; with one instance per resource type, a cycle identifies deadlock.
- **Detection with multiple instances:** use existing-resource vector `E`, available vector `A`, allocation matrix `C` and request matrix `R`; repeatedly finish any process whose remaining request is `≤ A`.
- **Recovery:** preempt a resource when possible, roll back to a checkpoint, or terminate processes.
- **Safe state:** some completion order guarantees every process can finish even if each later demands its declared maximum.
- **Unsafe state:** no such guarantee exists; it is not itself a deadlock.
- **Banker's algorithm:** grant only requests that leave the system safe; requires advance knowledge of maximum demand.
- **Prevention:** structurally eliminate at least one Coffman condition.
- **Two-phase locking:** first acquire all required locks without irreversible work; only then perform updates and release.
- **Communication deadlock:** processes wait for messages/events from one another without a resource cycle.
- **Livelock:** processes continue executing/retrying but collectively make no useful progress.
- **Starvation:** a process waits indefinitely because the allocation policy repeatedly serves others.

## Operational interpretation

For an incident, distinguish:

`blocked thread` ≠ `deadlock` ≠ `livelock` ≠ `starvation`.

A useful evidence path is:

1. enumerate owners and waiters;
2. identify the exact nonpreemptable resource or awaited event;
3. build a wait-for/resource graph or equivalent matrix;
4. prove a cycle or an unsatisfiable process set;
5. only then choose recovery or prevention.

Important boundaries:

- a high lock-wait time is not proof of deadlock;
- an unsafe state is not yet a deadlock;
- timeouts can break some communication deadlocks, but retries can duplicate effects and do not generally solve resource deadlocks;
- killing a process is a recovery action, not a detection method;
- a fixed retry delay can synchronize contenders and create livelock;
- unfair allocation can starve a process even when other work continues normally.

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

- Figures and their matrix/graph artwork are referenced through text RAG and are not independently encoded as multimodal objects.
- Figure-dependent questions whose required numeric state is absent from the text layer remain `[Needs confirmation]`.
- Programming exercises retain `[Needs confirmation]` for actual execution/test results.
- No external source or model-memory content is used to fill missing book evidence.
- Source inconsistencies/extraction defects are registered explicitly rather than silently corrected.
