# Шпаргалка главы 12 — dataflow, correctness, integrity, responsibility

## Symptom / problem framing

Проблема главы: сложная information system состоит из нескольких databases, indexes, caches, analytics/ML systems и user-facing views. Главные риски — divergence between copies, brittle synchronization, hidden coordination, irrecoverable corruption и harmful use of data.

Негативные сигналы:

- несколько systems independently accept writes to the same logical fact;
- migration требует irreversible big-bang cutover;
- derived index/cache/model нельзя rebuild from source;
- one slow/downstream service blocks unrelated writes;
- distributed transaction spreads local outage across systems;
- retry duplicates a payment/operation;
- uniqueness/inventory constraints coordinate everything globally;
- stale data and corrupted data treated as one class of "consistency";
- no audit/reconciliation mechanism exists because DB is assumed infallible;
- data lineage from input/request to output is unknown;
- personal data retained indefinitely without clear purpose;
- automated decisions materially affect people but have no review/appeal/accountability path.

## Baseline / context

### Data integration

Source proposes explicit flow:

`system of record → change/event log → transformation → derived system`

Derived state includes:

- search indexes;
- materialized views;
- caches;
- analytics;
- ML/statistical models;
- recommendations;
- live UI state.

### Batch + stream

- batch supports full historical reprocessing;
- stream supports low-latency incremental maintenance;
- unified systems should replay historical events through the same logic used for live events.

### Unbundled database / dataflow

Instead of one monolithic DB providing every feature:

- storage systems specialize;
- processing systems transform;
- log/event interfaces connect components;
- high-level/declarative layer should describe dependencies.

### Correctness

Chapter distinguishes:

- timeliness — how current observed data is;
- integrity — whether data/state is correct and uncorrupted.

Staleness can often heal with time/retry; integrity violations usually require explicit detection/repair.

## Read-only checks

1. Enumerate systems holding copies/derived forms of the same logical data.
2. Mark exactly one authoritative source for each fact where architecture permits.
3. Draw dataflow edges and transformation ownership.
4. Identify synchronous RPC/write dependencies on write path.
5. Find ad hoc dual writes.
6. Check whether every derived dataset can be rebuilt.
7. Check whether migrations support old/new versions in parallel.
8. For each retryable operation, trace request/operation ID end-to-end.
9. Identify invariants requiring uniqueness/coordination.
10. Classify each invariant:
    - must never be violated;
    - may be temporarily violated and compensated.
11. Separate timeliness SLO from integrity invariant.
12. Verify deduplication and deterministic derivation.
13. Check audit/reconciliation mechanisms.
14. Trace data provenance for important outputs/decisions.
15. For personal data, record purpose, retention, deletion path and access/control assumptions.
16. For automated decisions affecting people, record review/appeal/explainability boundary — exact mechanism `[Needs confirmation]`.

## Interpretation

- Derived system stale but eventually catches up → timeliness issue.
- Derived state permanently misses/duplicates records → integrity issue.
- Multiple systems independently accept writes → divergence risk.
- Local downstream outage blocks source write → excessive synchronous coupling.
- Request ID not preserved across layers → end-to-end deduplication incomplete.
- Unique constraint has one conflict key → candidate for partitioned serial decision.
- Constraint violation can be repaired by accepted compensation → synchronous global coordination may be stronger than needed.
- Projection cannot be rebuilt → derived state has become accidental source of truth.
- No independent reconciliation → corruption may remain undetected.
- Personal-data retention has no end condition → architecture conflicts with chapter's stated privacy principle.

## Next action

1. Draw authoritative dataflow and derived-state graph.
2. Mark integrity invariants and timeliness targets separately.
3. Locate unnecessary synchronous coordination/dual writes.
4. Choose one narrow improvement:
   - ordered change log;
   - replayable projection;
   - end-to-end request ID;
   - reconciliation/audit;
   - reversible migration;
   - narrower coordination scope.
5. Test failure/replay scenario.
6. Verify integrity first, then latency/availability.
7. Keep only if acceptance criteria pass.

## Modifying action

Source-confirmed classes of change:

- introduce change/event log between source and derived systems;
- replace dual write with ordered transformation;
- run old/new projection in parallel during migration;
- replay historical events through new transformation;
- add end-to-end request/operation ID;
- serialize conflicting constraint requests within one partition;
- split cross-partition workflow into durable request + deterministic derived instructions;
- use compensating process for constraints that may be temporarily violated;
- add audit/reconciliation/integrity checks;
- reduce or remove unnecessary data retention.

Concrete vendor CLI, legal/compliance procedure and production migration syntax: `[Needs confirmation]`.

## Verification / acceptance checks

### Dataflow/integration

- authoritative source remains unambiguous;
- derived systems can be rebuilt from retained source/history;
- downstream failure does not corrupt or block unrelated source operations beyond intended contract;
- migration can return to previous known-good projection.

### Integrity

- duplicate retries do not duplicate logical operation;
- debit/credit or equivalent multi-step effects preserve end-to-end invariant;
- derived data matches source after catch-up/rebuild;
- audit detects injected/modeled discrepancy.

### Coordination

- strict uniqueness is enforced where it is truly required;
- temporary constraint violation follows documented compensation path where allowed;
- synchronous coordination scope is minimal and explicit.

### Responsibility

- retention/deletion path is defined for personal data;
- provenance exists for material automated decisions;
- user-impacting use of data is reviewed as part of system design.

## Rollback

- Projection/migration: switch consumers back to previous known-good derived version while source/history remains intact; concrete switch mechanism `[Needs confirmation]`.
- Dataflow change: restore previous consumer/transformation only after verifying no events were lost; concrete procedure `[Needs confirmation]`.
- Coordination relaxation: revert to stricter path if compensation/integrity tests fail.
- Retention/deletion changes may be irreversible; rollback may be impossible once data is deleted.
- Read-only audit checks: `[Not applicable]`.

## Operational loop

`authoritative facts → replayable transformations → derived state → invariant/audit checks → reversible evolution → minimal coordination`.
