# Шпаргалка: глава 12 — Координированная пакетная обработка

## Symptom / problem framing

Parallel batch branches must either:
- synchronize before next stage;
- or combine partial outputs into aggregate result.

## Baseline / context

~~~text
parallel outputs
→ Join or Reduce
→ coordinated downstream result
~~~

## Read-only checks

1. Does next stage require all upstream results?
2. Is simple Merger insufficient?
3. Can aggregation start before all inputs finish?
4. Is reduce operation associative/composable enough for repeated merging?
5. What happens if one shard never completes?
6. Is next action destructive?
7. Are originals/checkpoints retained until barrier completes?
8. Can partial aggregates be recomputed?

## Interpretation

### Join

~~~text
wait for every required branch
→ release only complete set
~~~

Use when completeness is mandatory.

Cost: barrier latency.

### Reduce

~~~text
partial + partial
→ smaller aggregate
→ repeat
~~~

Use when partial results can be incrementally combined.

### Image pipeline

~~~text
shard
→ Multi-Worker blur
→ Join
→ Copier
├→ delete originals
└→ recognition
   → Reduce
~~~

## Next action

1. Mark every fan-in point.
2. Decide Merger vs Join vs Reduce semantics.
3. Put destructive actions behind explicit completeness barrier.
4. Define reducible intermediate representation.
5. Test missing/slow shard behavior.
6. Verify aggregate correctness on known dataset.
7. Preserve restart source until coordinated stage is complete.

## Modifying action

`[Not applicable]`.

Chapter 12 contains architecture/examples but no explicit shell/Kubernetes state-changing command sequence.

## Verification / acceptance checks

Verify:
- Join does not release early;
- one incomplete shard prevents destructive cleanup;
- Reduce preserves correct totals;
- repeated reduction converges to one final aggregate;
- intermediate results have enough information for weighted histogram merge;
- final vehicle/color totals equal the aggregate of per-image outputs.

Exact distributed test commands: `[Needs confirmation]`.

## Rollback

No source-supported rollback procedure is supplied.

- barrier recovery: `[Needs confirmation]`;
- failed reduction recovery: `[Needs confirmation]`;
- deleted-source recovery depends on having respected Join before deletion.

## Decision rule

~~~text
Need every result first?
→ Join

Can combine incrementally?
→ Reduce

Only need streams interleaved?
→ Merger
~~~
