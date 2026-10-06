# Source findings — глава 7 «Масштабирование»

## Finding 1 — scheduler description is explicitly version-sensitive

Classification: **[Source version note]**

Provenance:

- PDF/RAG pages 174–175
- chunks `p0174:c01`, `p0175:c01`

Observed:

Источник сам говорит, что scheduler mechanism сложен, существенно менялся между версиями Go и что автор не считает детали полностью стабильными/понятными.

Impact:

Утверждения о:

- точном числе OS threads;
- one-thread-per-processor model;
- local/global goroutine queues;
- migration behavior;
- preemption points

нельзя переносить из главы как timeless specification Go runtime.

Action:

- артефакты используют это как **source model**;
- современная runtime verification не выполнялась;
- внешний adjudication: **[Needs confirmation]**.

## Finding 2 — "without recompilation" scaling wording is ambiguous

Classification: **[Source wording ambiguity]**

Provenance:

- PDF/RAG page 174

Observed:

Источник пишет, что Go code «даже без перекомпиляции» масштабируется от ARM SBC до многопроцессорных серверов.

В последующих страницах, однако, демонстрируются разные платформы, установленные native Go environments и native compilation of examples.

Impact:

Из chapter RAG неясно, относится ли «без перекомпиляции» к:

- одному executable binary;
- неизменённому source code;
- отсутствию ручной platform-specific adaptation.

Action:

- artifacts do **not** interpret this as binary portability claim;
- intended meaning: **[Needs confirmation]**.

## Finding 3 — first experiment contains a measurement contaminant acknowledged by source

Classification: **[Source experiment limitation]**

Provenance:

- pages 180–186
- `mlpar` → transition to `mlpar2`

Observed:

Первая worker function repeatedly uses `time.Now()` to determine one-second activity. Автор позднее отмечает, что time acquisition may involve Linux system interaction/context effects and therefore alters the experiment.

Action:

- preserve `mlpar` as first attempt;
- do not promote its timings as clean CPU-scaling measurements;
- use `mlpar2` as the source's controlled second attempt.

## Finding 4 — taskset/runtime CPU-count result is environment-specific evidence

Classification: **[Source environment-specific result]**

Provenance:

- pages 193–195

Observed:

Under source environment:

```bash
taskset -c 0-3 ./numproc
```

reports 4 processors / 4 execution threads, and other CPU lists similarly alter the application's reported available count.

Impact:

This is evidence from the demonstrated Linux/Go environment. Artifacts do not generalize exact runtime/API semantics to every Go/kernel version.

Action:

- preserve as experiment result;
- verify on target host before operational use.

## Finding 5 — CPU-list examples depend on topology discussed in previous chapter

Classification: **[Operational dependency]**

Provenance:

- pages 194–195

Observed:

Examples use lists such as:

```text
0-3
32,34,36,38
0,2,4
0,20
```

The intended distinction includes physical cores, NUMA/socket placement and a hyper-thread sibling pair.

Impact:

The same numeric CPU IDs can mean something completely different on another host.

Action:

- never reuse these IDs blindly;
- prerequisite: target-specific `lscpu -e` / topology verification.

## Finding 6 — benchmark timings are not isolated from host scheduler noise

Classification: **[Source experiment limitation]**

Provenance:

- page 192 and surrounding experiment discussion

Observed:

Источник explicitly notes that Linux remains a preemptive multitasking OS and Go worker threads compete with unrelated system/user workloads.

Impact:

Single timing samples cannot establish deterministic scaling efficiency.

Action:

- require repeated measurements;
- record platform/load state where possible;
- treat chapter numbers as observed examples, not performance guarantees.
