# Шпаргалка: глава 9 — Выбор владельца

## Symptom / problem framing

Несколько replicas способны выполнять работу, но конкретным resource/task одновременно должен управлять только один active owner.

~~~text
many candidates
→ one current owner
→ failover on owner loss
~~~

## Baseline / context

Simplest option:

~~~text
one service instance
→ ownership implicit
→ simple
→ lower availability during failure/update
~~~

Distributed option:

~~~text
replicas
→ coordination store
→ election / lock / lease
→ one active owner
~~~

## Read-only checks

1. Нужна ли distributed ownership вообще?
2. Допустим ли singleton downtime?
3. Какой resource требует exclusivity?
4. Где хранится authoritative owner state?
5. Поддерживается ли atomic compare-and-swap?
6. Есть ли TTL?
7. Как owner renews lease?
8. Что делает process при renewal failure?
9. Проверяет ли downstream current owner?
10. Проверяет ли downstream resource version/epoch?
11. Что произойдет при process pause/network delay?
12. Каков failover time versus TTL?

## Interpretation

### CAS

~~~text
expected == current
→ atomic update succeeds

expected != current
→ contender loses
~~~

### Lock without TTL

~~~text
owner crashes
→ lock remains forever
→ no progress
~~~

### TTL

~~~text
owner disappears
→ expiry
→ next owner can acquire
~~~

### Version-aware unlock

~~~text
stale owner unlock
+ version mismatch
→ reject
~~~

### Renewable ownership

~~~text
acquire
→ renew every TTL/2
→ continue
→ renewal failure → stop protected activity
~~~

### Receiver validation

~~~text
request
→ validate owner + version
→ accept/reject
~~~

## Next action

1. Decide whether singleton is sufficient.
2. Choose authoritative coordination store.
3. Use atomic acquisition.
4. Add finite TTL.
5. Track resource version.
6. Make release/version checks conditional.
7. Renew long-lived ownership before TTL expiry.
8. Stop protected work immediately after detected loss.
9. Require downstream owner/version validation.
10. Test process pause, delayed request and failover cases.

## Modifying action

Source-supported state-changing actions:
- initialize/install Helm/operator;
- create etcd cluster;
- write etcd keys;
- acquire/release lock;
- create/renew TTL lease.

Exact command inventory: `commands.md`.

Risks:
- modifies cluster/control state;
- wrong lock manipulation can violate exclusivity;
- source commands may target obsolete APIs/tooling.

## Verification / acceptance checks

### etcd cluster
- 3 replicas expected by source config;
- pods become visible;
- endpoints can be resolved;
- test key write succeeds.

### Mutex
- Alice acquisition succeeds;
- Bob acquisition from `unlocked` fails while Alice owns;
- Alice conditional release succeeds only against expected current owner.

### Lease
- key exists during successful renewals;
- absent key becomes acquirable after TTL expiry;
- stale process stops protected activity when renewal lost.

### Protected downstream
- stale owner request rejected;
- delayed request from previous ownership version rejected.

Exact modern commands/tests: `[Needs confirmation]`.

## Rollback

Chapter provides no complete rollback workflow.

- etcd operator/cluster rollback: `[Needs confirmation]`;
- lock state rollback: application-specific;
- lease recovery: reacquisition after expiry is source-supported conceptually;
- cluster resource deletion commands: `[Needs confirmation]`.

Do not infer deletion/uninstall commands.

## Failure sequence to remember

~~~text
A owns
→ A pauses
→ TTL expires
→ B owns
→ A resumes
→ local belief may be stale
→ downstream must verify authoritative owner/version
~~~
