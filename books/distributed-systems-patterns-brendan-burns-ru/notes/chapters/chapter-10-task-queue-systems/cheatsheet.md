# Шпаргалка: глава 10 — Системы на основе очередей задач

## Symptom / problem framing

Есть набор независимых batch tasks, которые нужно:
- обнаружить;
- запустить;
- надежно довести до completion;
- масштабировать по backlog/load.

~~~text
source
→ queue manager
→ workers
~~~

## Baseline / context

Source container:
- предоставляет work items.

Queue manager:
- хранит generic orchestration logic;
- сравнивает source items with existing Jobs;
- запускает missing work.

Worker:
- выполняет один item;
- one-shot lifecycle.

## Read-only checks

1. Tasks действительно independent?
2. Где authoritative source items?
3. Стабилен ли versioned source API?
4. Как определяется already-running/completed work?
5. Worker idempotent?
6. Как передается work item?
7. Ограничена ли concurrency?
8. Каков average inter-arrival interval?
9. Каково average processing time?
10. Каков effective processing time при текущей parallelism?
11. Растет ли queue depth?
12. Можно ли worker logic decomposed into reusable Multi-Worker parts?

## Interpretation

### Stable queue

~~~text
processing_time / parallelism
<
inter-arrival interval
~~~

### Overloaded queue

~~~text
effective processing time
>=
arrival interval
→ backlog grows
→ wait time grows
~~~

### Concurrency trade-off

~~~text
more workers
→ faster drain
→ more cluster resources

fewer workers
→ lower resource use
→ higher queue delay
~~~

### Multi-Worker

~~~text
one worker interface
→ several reusable internal worker containers
~~~

## Next action

1. Define source API.
2. Define worker input contract.
3. Identify durable execution state.
4. Compute pending items.
5. Bound worker concurrency.
6. Measure arrival interval.
7. Measure processing duration.
8. Compare service rate to arrival rate.
9. Scale concurrency with reserve.
10. Decompose repeated worker logic into reusable containers.

## Modifying action

Source explicit runtime command:
- `ffmpeg` thumbnail command.

Source Python manager creates Kubernetes Jobs programmatically, but chapter does not provide a standalone `kubectl` deployment sequence.

Exact details: `commands.md`.

## Verification / acceptance checks

Verify:
- source returns expected item list/details;
- manager does not recreate Jobs for already-known items;
- new item produces one worker Job;
- successful worker completion is observable through Job state;
- backlog does not grow indefinitely under target load;
- worker concurrency stays within intended resource envelope.

Exact SLO thresholds: `[Needs confirmation]`.

## Rollback

Chapter provides no complete rollback procedure.

- queue-manager rollback: `[Needs confirmation]`;
- Job cleanup: `[Needs confirmation]`;
- worker artifact cleanup: `[Needs confirmation]`;
- scaling rollback: reduce concurrency only after verifying backlog/service margin.

Do not invent delete/rollback commands.
