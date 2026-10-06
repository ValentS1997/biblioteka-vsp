# Cheatsheet — «Заключение»

## Source thesis

Книга позиционируется как руководство не столько по Go, сколько по использованию многопроцессорного hardware.

## What the book converges to

```text
single-core frequency scaling
        ↓
multicore / multiprocessor systems
        ↓
need for software parallelism
        ↓
goroutines / channels / synchronization
        ↓
measure real scaling
```

## Engineering interpretation grounded in the book

- concurrency is not equal to speedup;
- shared mutable state creates correctness risks;
- synchronization restores correctness but has cost;
- fine-grained parallelism can be slower than sequential execution;
- CPU topology and runtime scheduling matter;
- benchmark results require controlled conditions;
- parallelism is useful when independent useful work dominates coordination overhead.

## Final acceptance rule

Перед тем как считать многопроцессорную реализацию успешной:

1. результат корректен;
2. races отсутствуют;
3. baseline известен;
4. worker/task granularity оправдана;
5. synchronization overhead измерен;
6. speedup подтверждён на целевом hardware.

## Boundary

Page 281 `Об авторе` не входит в этот artifact.
