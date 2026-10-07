# Шпаргалка: глава 6 — Шардированные сервисы

## Symptom / problem framing

Один node больше не вмещает:
- весь data set;
- требуемый working set cache;
- либо один shard становится hot.

Базовый выбор:

~~~text
replication → copies of same responsibility
sharding → split responsibility/data
~~~

Глава 6 про второй случай и про комбинацию sharding + replication.

## Baseline / context

Core topology:

~~~text
request
→ sharding function
→ shard A / shard B / shard C
~~~

Replicated shard:

~~~text
request
→ shard A
→ replica A1 / replica A2
~~~

Router may be:
- local Ambassador;
- shared replicated routing service.

## Read-only checks

1. Действительно ли data set/workload не помещается на один node?
2. Что является sharding key?
3. Совпадает ли key с semantics ответа/данных?
4. Детерминирован ли routing?
5. Достаточно ли равномерно распределяется load?
6. Что произойдет при failure одного shard?
7. Перегрузится ли backend при cache miss/failure?
8. Нужна ли replication внутри каждого shard?
9. Что произойдет при изменении shard count?
10. Есть ли hot shards?
11. Нужен local Ambassador или shared router?
12. Какая extra latency появляется у shared router?

## Interpretation

### Replicated cache

~~~text
same hot data repeated in many replicas
→ high redundancy
→ low unique-data coverage
~~~

### Sharded cache

~~~text
different data subsets
→ larger aggregate working set
→ one failed shard affects mapped traffic
~~~

### Sharded + replicated

~~~text
partition data
+ replicate each partition
→ data scale + shard availability
~~~

### Wrong key

Too broad:
- different responses collapse into same shard/cache group.

Too specific:
- equivalent requests split across shards;
- locality and cache efficiency fall.

### Changing shard count

~~~text
ordinary modulo mapping
→ N changes
→ large remap
→ misses / reshuffle

consistent hashing
→ minimize remap
~~~

### Hot shard

~~~text
uniform key distribution
!=
uniform real workload
~~~

Popular keys can overload one shard; replicated shard can scale independently.

## Next action

1. Define partitioning objective: data capacity, cache coverage, locality.
2. Choose semantic key.
3. Verify determinism and load distribution.
4. Model shard failure.
5. Test system with degraded/absent cache where applicable.
6. Decide if each shard needs replication.
7. Select local Ambassador or shared router.
8. Use consistent hashing if shard count changes are expected.
9. Measure shard-level traffic and detect hot shards.
10. Scale hot shards independently.

## Modifying action

Source-supported cluster modifications:
- create memcached StatefulSet;
- create headless Service;
- create twemproxy ConfigMap;
- create Ambassador Pod;
- alternatively create shared twemproxy Deployment and Service.

Exact commands and source mismatches are recorded in `commands.md` and `source-findings.md`.

Risk:
- changes runtime/cluster state;
- bad routing can send keys to wrong shard;
- bad resharding can cause miss storms;
- source manifests are not asserted current/production-safe.

## Verification / acceptance checks

### Sharded memcache
- three memcache instances are expected;
- DNS names follow `memcache-0.memcache`, etc.;
- twemproxy references all shards;
- application reaches proxy through intended local/shared endpoint.

### Capacity
- backend remains stable under expected cache degradation;
- source recommends load testing both with and without cache.

Exact load-test command: `[Needs confirmation]`.

### Consistent hashing
- shard-count change should remap a limited subset, not effectively the whole keyspace.

Exact production measurement procedure: `[Needs confirmation]`.

### Hot sharding
- per-shard traffic is observable;
- overloaded shard gains capacity independently.

Exact autoscaler configuration: `[Needs confirmation]`.

## Rollback

No complete rollback workflow is supplied in chapter 6.

- StatefulSet/Service: `[Needs confirmation]`;
- Ambassador Pod: `[Needs confirmation]`;
- shared router: `[Needs confirmation]`;
- resharding rollback: `[Needs confirmation]`.

Do not infer delete/rollback commands from model knowledge.

## Decision frame

~~~text
Need more request capacity only?
  → replication

Need more data/working-set capacity?
  → sharding

Shard failure unacceptable?
  → replicate each shard

Uneven real load?
  → scale hot shard independently
~~~
