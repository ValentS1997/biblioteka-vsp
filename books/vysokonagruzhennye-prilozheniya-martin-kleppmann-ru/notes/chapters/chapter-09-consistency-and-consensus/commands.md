# Source-confirmed operations, APIs and tools — глава 9

Глава концептуальная. Универсальных shell/admin commands она не дает. Ниже только source-confirmed operations, APIs и coordination mechanisms.

## Linearizable register operations

Источник: `p0380:c01`–`p0382:c01`, PDF 380–382.

~~~text
read(x) -> v
write(x, v) -> result
cas(x, old, new) -> result
~~~

Тип:

- `read` — read-only;
- `write` — state-changing;
- `cas` — state-changing atomic compare-and-set.

Смысл: linearizability требует, чтобы operations выглядели как atomic actions над одной logical copy и уважали real-time order.

Verification:

- read после завершенного write не возвращает более старое значение;
- successful CAS соответствует одному atomic decision point.

Rollback: зависит от application state и semantics — `[Needs confirmation]`.

## ZooKeeper sync()

Источник: `p0408:c01`, PDF 408.

~~~text
sync()
~~~

Тип: coordination/read-barrier operation.

Source point: один из способов добиться linearizable-like fresh read — получить linearizable position последней записи, дождаться delivery всех entries до этой position, затем выполнять read. Глава связывает эту идею с `sync()` в ZooKeeper.

Verification: local replica применяет все entries до required log position перед subsequent read.

Rollback: `[Not applicable]`.

## Two-phase commit — phase model

Источник: `p0413:c01`–`p0415:c01`, PDF 413–415.

Conceptual sequence:

~~~text
phase 1: coordinator -> PREPARE to all participants
participant -> YES / NO

if all YES:
  phase 2: coordinator -> COMMIT
else:
  phase 2: coordinator -> ABORT
~~~

Тип: state-changing distributed transaction protocol.

Source-confirmed commitments:

- transaction has globally unique ID;
- participant that votes YES must durably promise it can commit later;
- coordinator records final commit/abort decision durably;
- after final decision, participants must follow it.

Risks:

- coordinator failure can leave participants in-doubt;
- prepared transactions may retain locks;
- losing coordinator log can require manual intervention;
- heuristic unilateral decisions may violate atomicity.

Verification:

- all participants resolve to same final outcome;
- coordinator restart recovers final decisions;
- prepared/in-doubt transactions are observable.

Rollback: arbitrary rollback after prepare is unsafe; recovery procedure is product-specific — `[Needs confirmation]`.

## XA / JTA / JDBC / JMS

Источник: `p0413:c01` и далее в 9.4.

Source-confirmed interfaces/standards:

- X/Open XA;
- Java Transaction API (JTA);
- JDBC;
- JMS;
- WS-AtomicTransaction.

Тип: transaction coordination APIs/standards.

Source point: XA exposes 2PC across heterogeneous participants; it is not itself a network protocol.

Concrete API calls or vendor CLI commands are not provided in chapter RAG.

## Consensus protocol names

Источник: `p0424:c01`–`p0428:c01`.

Source-confirmed protocols/algorithms:

- Viewstamped Replication;
- Paxos / Multi-Paxos;
- Raft;
- Zab.

Type: fault-tolerant consensus / total-order-broadcast protocols.

Source-common structure:

- leader-like role;
- monotonically increasing epoch/term/ballot/view number;
- quorum/majority voting;
- newer epoch supersedes older leader;
- safety preserved even when liveness stops because majority is unavailable.

Concrete implementation commands: absent from chapter RAG.

## ZooKeeper / etcd coordination service

Источник: `p0428:c01`–`p0431:c01`.

Source-confirmed capabilities:

- linearizable atomic operations;
- total ordering with monotonically increasing transaction/version identifiers;
- sessions and failure detection;
- ephemeral nodes / lease-like ownership;
- change notifications;
- leader election / membership / partition assignment support.

Тип: coordination service.

Operational boundary: small, slowly changing coordination metadata; not bulk/high-throughput application state.

## Что не добавлено

- `zkCli.sh`;
- etcdctl commands;
- Raft/Paxos tuning parameters;
- XA recovery commands;
- vendor-specific prepared-transaction queries;
- DB isolation or replication configuration.

Они не подтверждены chapter RAG.
