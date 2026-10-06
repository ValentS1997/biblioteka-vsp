# Глава 5. Процессоры в Linux

Статус: **RAG_GROUNDED**

## Scope

Глава связывает аппаратную топологию CPU с Linux-механизмами управления выполнением. Основные темы:

1. диагностика CPU через `/proc/cpuinfo`, `lscpu`, `inxi`;
2. физические ядра, SMT/Hyper-Threading и неоднозначная нумерация CPU;
3. выбор CPU по affinity mask;
4. POSIX API для process/thread affinity;
5. `taskset` для запуска и переназначения affinity;
6. базовая модель Linux scheduler;
7. `SCHED_OTHER`, `SCHED_FIFO`, `SCHED_RR`;
8. nice priorities;
9. real-time priorities и `chrt`.

## Provenance

- Book ID: `linux-go-low-level-programming-tsilyurik-ru`
- Source path: `source/book.pdf`
- Source SHA-256: `df8db4893a8ddd656fcaaed7933b1bd639d32bd6cd18547a3b1d103bef7afdd2`
- Part-level preface: PDF page **132**, excluded from chapter boundary
- Chapter title: `Процессоры в Linux`
- RAG chunk range: `p0133:c01` … `p0146:c01`
- Included chunks: **14**
- PDF page range: **133–146**
- Chapter boundary verified: **yes**
- Boundary evidence:
  - page 133 starts with `Процессоры в Linux`;
  - page 146 contains the chapter sources;
  - page 147 starts `Параллелизм и многопроцессорность`.

## Main principle

Глава строится вокруг operational chain:

```text
observe topology
    ↓
identify CPU/core/socket relationships
    ↓
measure/select usable CPUs
    ↓
apply affinity
    ↓
understand scheduling policy
    ↓
change priority/policy only with explicit risk awareness
```

Ключевой инженерный вывод источника: CPU numbering нельзя надёжно угадывать по модели или производителю; topology нужно проверять на конкретной системе.

## Operational notes

- `/proc/cpuinfo`, `lscpu`, `lscpu -e`, `inxi -Cxxx`, `sensors` — diagnostic/read-only path.
- `taskset` может как читать, так и изменять affinity.
- `nice` меняет приоритет запускаемой задачи.
- `chrt` может менять scheduling policy и real-time priority.
- Источник подчёркивает, что real-time scheduling способен полностью вытеснить обычные процессы на CPU; это high-risk operational action.
- Команды с root и RT-политиками не должны применяться без отдельной проверки и rollback-плана.

## Conditional artifacts

- explicit chapter-end summary: **not present**
- review questions/exercises: **not present**
- source findings: **present**

## Artifacts

- [cheatsheet.md](./cheatsheet.md)
- [commands.md](./commands.md)
- [diagram.md](./diagram.md)
- [visual-cheatsheet.svg](./visual-cheatsheet.svg)
- [visual-cheatsheet-detailed.svg](./visual-cheatsheet-detailed.svg)
- [source-findings.md](./source-findings.md)
