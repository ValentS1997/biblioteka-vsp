# Резюме главы 9

Источник: раздел 9.5 «Резюме», `p0432:c01`–`p0434:c01`, PDF 432–434.

Глава связывает consistency models, ordering и consensus.

## Linearizability

Linearizability делает replicated data похожими на одну copy, над которой operations выполняются атомарно.

Модель удобна для reasoning, но требует coordination и ухудшает latency, особенно при больших network delays.

При network fault linearizable system не может одновременно продолжать принимать conflicting operations в disconnected parts и сохранять одну актуальную logical copy.

Глава отдельно различает:

- serializability — transaction isolation/order;
- linearizability — real-time guarantee для register-like operations.

Эти guarantees независимы; вместе они образуют strict serializability.

## Causality

Causality задает более слабый порядок:

- причинно связанные события должны наблюдаться в правильной последовательности;
- concurrent events могут оставаться неупорядоченными.

Это позволяет избежать части coordination costs linearizability.

Lamport timestamps дают compact total order, совместимый с causality. Но они не определяют, являются ли events concurrent, и сами по себе не дают способ узнать, что total order уже окончательно построен.

## Total-order broadcast

Total-order broadcast требует:

- reliable delivery;
- одинаковой delivery sequence на всех nodes.

Эта abstraction связывает ordering с consensus. Она может использоваться для replication log/state machine, locks, uniqueness constraints и serial ordering.

Linearizable compare-and-set/register, total-order broadcast и consensus можно свести друг к другу.

## Distributed transactions and 2PC

Distributed atomic commit требует одного решения: все participants commit или все abort.

2PC решает эту задачу через coordinator:

1. prepare;
2. durable final commit/abort decision.

После YES на prepare participant связан обещанием выполнить coordinator decision.

Главный operational drawback — blocking: если coordinator unavailable после prepare, participant может остаться in-doubt и удерживать locks.

XA стандартизует 2PC across heterogeneous systems, но coordinator state становится критической persistent dependency, а failure одного participant может блокировать всю transaction.

## Fault-tolerant consensus

Consensus должен обеспечить:

- agreement;
- integrity;
- validity;
- termination.

Первые три — safety; termination — liveness.

При отсутствии majority consensus system может остановить progress, но safety не должна нарушиться.

Paxos, Raft, Zab и Viewstamped Replication используют leader-like roles, epochs/terms/views/ballots и quorum voting.

Consensus/total-order protocols фактически принимают последовательность решений.

## Coordination services

ZooKeeper/etcd выносят consensus в специализированный service.

Source выделяет полезные свойства:

- linearizable atomic operations;
- total ordering;
- sessions/failure detection;
- ephemeral ownership;
- change notifications.

Типичные задачи:

- leader election;
- membership;
- partition assignment;
- distributed locks/leases;
- coordination metadata.

Такой service предназначен для небольшого и сравнительно медленно меняющегося coordination state, а не для основного high-throughput application dataset.

## Итог

Большой класс задач сводится к consensus:

- linearizable CAS;
- atomic distributed commit;
- total-order broadcast;
- locks/leases;
- membership;
- uniqueness constraints.

Но global consensus нужен не всегда. Если application допускает branching histories и последующее merge, более слабая causal/eventual model может дать лучшую availability и performance.

Глава 9 завершает часть II. На `p0445:c01` начинается часть III «Производные данные», а глава 10 начинается на `p0449:c01`.
