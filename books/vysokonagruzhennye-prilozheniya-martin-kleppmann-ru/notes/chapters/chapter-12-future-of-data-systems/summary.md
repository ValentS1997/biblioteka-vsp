# Резюме главы 12

Источник: раздел 12.5 «Резюме», `p0627:c01`–`p0628:c01`, PDF 627–628.

Глава 12 — заключительная и явно более opinionated, чем предыдущие главы. Автор объединяет идеи книги и предлагает направление развития information systems.

## Integration through dataflows

Одного программного продукта недостаточно для всех workloads.

Complex applications combine multiple specialized systems:

- systems of record;
- search indexes;
- materialized views;
- caches;
- analytics;
- machine-learning/statistical models;
- user-facing projections.

Author proposes viewing the whole architecture as data transformations between datasets.

Some systems are authoritative sources; other systems derive their state by consuming transformations/change streams.

Asynchronous weak coupling localizes failures: a slow or failed consumer does not necessarily stop the system of record or unrelated consumers.

## Reprocessing and evolution

Derived state should be rebuildable.

If schema, index structure, cache representation or application requirements change, a new transformation can replay existing history and construct a new view.

Old and new projections can run in parallel, allowing gradual and reversible migration.

This extends the batch/stream model from chapters 10–11 into an architecture principle.

## Unbundling the database

The chapter compares databases and Unix/dataflow philosophy.

A database internally maintains indexes, materialized views and replication state. At organization scale, batch and stream pipelines can perform analogous work across independent systems.

The desired direction is a high-level/declarative way to connect specialized components, analogous to Unix pipelines but with durable distributed semantics.

The author calls this style "database inside-out"/unbundling rather than one monolithic database.

## Correctness and integrity

The chapter argues that transaction semantics are valuable but not sufficient to guarantee application correctness.

Correctness must be considered end-to-end.

Stable request/operation IDs can prevent logical duplicates across retries that lower-level TCP or processor-level deduplication cannot fully eliminate.

For uniqueness/constraints, potentially conflicting requests may be routed into a single partition and decided sequentially.

Cross-partition workflows can sometimes avoid global atomic commit by:

1. durably recording one request event;
2. deterministically deriving downstream commands;
3. propagating the same request ID;
4. deduplicating downstream effects.

## Timeliness vs integrity

The chapter separates two meanings often grouped under "consistency":

- **timeliness** — whether users see current state;
- **integrity** — whether the state is correct and uncorrupted.

Staleness is often temporary and heals by waiting/catching up.

Integrity violations—lost, duplicated, inconsistent or corrupted data—typically persist until detected and repaired.

Author's position is that integrity is more important than strict timeliness for many applications.

## Coordination and compensation

Strict uniqueness constraints require coordination when conflicting requests must be rejected immediately.

But some business constraints may be temporarily violated and corrected with compensating actions.

Examples in the source include inventory shortages, overbooking and overdraft-like scenarios.

The general principle is not to remove coordination entirely, but to use synchronous coordination only where the cost of temporary violation is unacceptable or irreversible.

This allows many workflows to remain asynchronous and geographically scalable while preserving integrity.

## Trust but verify

Storage engines, networks, disks and application software can all contain rare failures or bugs.

The chapter therefore argues for auditability and independent integrity verification instead of blind trust.

Event/dataflow architectures help because:

- source events are explicit;
- transformations can be deterministic;
- provenance can be traced;
- derived state can be recomputed and compared.

The source also points to cryptographic audit techniques such as Merkle trees as a promising direction.

## Ethics and human impact

Section 12.4 deliberately steps beyond technical architecture.

The author argues that software engineers must consider the effects of data systems on people.

Topics include:

- predictive analytics;
- encoded/amplified bias;
- discrimination;
- surveillance;
- privacy;
- data breaches;
- retention;
- user control over personal information.

Data about people should not be treated merely as optimization inputs.

The chapter advocates respect for human dignity, restraint in collection/retention and responsibility for the consequences of automated decisions.

These are the author's normative conclusions, not claims presented as technical consensus.

## Итог

The final architectural thesis can be summarized as:

`authoritative data → replayable transformations → derived state → end-to-end integrity + audit → minimal necessary coordination`

Reliable systems should be designed so that derived state can evolve and be rebuilt, failures stay localized, correctness is verified end-to-end, and the human consequences of data use are treated as part of the design problem.

This is the final numbered chapter of the book.
