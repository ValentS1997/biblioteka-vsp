# Summary — глава 13 «Многопроцессорные параллельные вычисления»

Источник завершает главу двумя явными выводами:

1. Механическое распараллеливание, даже корректно реализованное, не гарантирует улучшения времени выполнения и может сделать задачу медленнее.
2. В critical sections должно быть достаточно полезной работы, чтобы synchronization overhead не доминировал над целевыми вычислениями.

Контекст этих выводов в главе:

- goroutines дешёвы относительно процессов/threads в показанном activation test;
- shared mutable state без синхронизации приводит к races;
- race detector помогает локализовать conflicting accesses, но вносит большой overhead;
- atomics, mutexes и channels восстанавливают correctness ценой synchronization cost;
- CPU-parallel workload может хорошо масштабироваться, если ветви достаточно независимы;
- слишком мелкая гранулярность работы и частая синхронизация способны полностью уничтожить expected speedup.

Canonical operational rule:

```text
correctness first
→ measure sequential baseline
→ parallelize coarse useful work
→ minimize shared critical sections
→ measure again
```
