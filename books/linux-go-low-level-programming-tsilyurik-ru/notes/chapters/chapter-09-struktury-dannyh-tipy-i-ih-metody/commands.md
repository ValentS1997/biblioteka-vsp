# Commands — глава 9 «Структуры данных, типы и их методы»

В chapter RAG показаны только запуски уже собранных examples.

| Command | Class | Purpose | Expected observation |
|---|---|---|---|
| `./array_c` | workload | C array parameter example | caller-visible element changes |
| `./array_go` | workload | Go array/slice comparison | array copy vs pointer/slice effects |
| `./garray_c` | workload | C struct-wrapped fixed array | value-copy and pointer mutation behavior |
| `./cpptr` | workload | pointer value-copy demonstration | local pointer changes, caller state remains usable |
| `./3slice` | workload | irregular 2D slice | triangular nested slice output |
| `./marg` | workload | multiple-return example | int + float + []string, then ignored values |

## State-changing commands

Конкретные build commands внутри границы главы не приведены.

```text
build command: [Needs confirmation]
cleanup command: [Needs confirmation]
```

## Verification discipline

Для `array_go` проверяется последовательность состояний: исходный array, copy/result, состояние после value call, состояние после pointer call, slice before/after `strans`.

Для `marg` source output:

```text
5 1.6666666666666667 [g h i]
2.333
```

## Risk

Команды локальные и согласно chapter evidence не изменяют системную конфигурацию.

Application-specific side effects вне показанного stdout: **[Needs confirmation]**.
