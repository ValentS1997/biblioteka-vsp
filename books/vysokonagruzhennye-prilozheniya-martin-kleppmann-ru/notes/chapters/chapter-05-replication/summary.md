# Резюме главы 5

Источник: раздел 5.5 «Резюме», `p0230:c01`–`p0232:c01`, PDF 230–232.

Репликация хранит копии одних данных на нескольких машинах и используется ради нескольких целей:

- высокой доступности;
- возможности продолжать работу при временном отсутствии сети;
- снижения задержки через географически близкие replicas;
- масштабирования read workload.

Несмотря на кажущуюся простоту идеи, репликация требует работы с отказами, сетевыми задержками и concurrent access.

## Три основные модели

### Single-leader

Все writes поступают leader. Leader передает changes followers; reads могут обслуживаться разными replicas.

Преимущество — более простая ordering model и отсутствие обычной необходимости merge concurrent writes.

Недостаток — dependence on leader и возможная staleness followers при asynchronous replication.

### Multi-leader

Несколько leaders принимают writes и обмениваются change streams.

Это полезно, например, для нескольких ЦОДов или offline-first clients, но concurrent writes требуют conflict detection/resolution.

### Leaderless

Client пишет в несколько replicas и читает несколько replicas параллельно.

Quorum parameters `n`, `w`, `r` позволяют менять trade-off между availability, latency и вероятность stale reads.

Read repair, anti-entropy и hinted handoff помогают replicas снова сходиться.

## Replication lag

Asynchronous replication создаёт eventual consistency и user-visible anomalies.

Глава выделяет три полезные гарантии:

- read-after-write: пользователь видит собственные writes;
- monotonic reads: после более нового состояния пользователь не видит более старое;
- consistent prefix reads: causal order не наблюдается в обратной последовательности.

## Failover

Follower recovery сравнительно прямолинейно использует replication log.

Leader failover сложнее: нужно обнаружить отказ, выбрать новый leader, перенастроить clients/followers и корректно обработать возвращение старого leader.

При asynchronous replication возможно потерять writes, которые старый leader подтвердил, но не успел передать новому.

## Concurrent writes

Multi-leader и leaderless models допускают concurrent updates.

LWW обеспечивает convergence, но может незаметно потерять writes.

Более осторожный подход сохраняет siblings/concurrent values и использует causal/version information, после чего values объединяются приложением или специализированной data structure.

Version vectors позволяют отличать overwrite от concurrency.

## Итог

У replication нет универсально лучшей модели. Single-leader проще, а multi-leader/leaderless повышают устойчивость к некоторым network/node failures ценой более слабых guarantees и сложного conflict handling.

Следующая глава, согласно `p0239:c01`, переходит от копирования одних данных к их секционированию между узлами.
