# Cheatsheet — глава 5 «Процессоры в Linux»

## Symptom / problem framing

Нужно понять:

- сколько CPU видит Linux;
- какие logical CPU относятся к одному physical core;
- как распределены CPU по sockets/cores;
- каким CPU разрешено выполнять процесс;
- как политика планирования и priority влияют на выполнение.

## Baseline / read-only checks

### CPU topology

```bash
cat /proc/cpuinfo
lscpu
lscpu -e
inxi -Cxxx
inxi -C
```

Назначение:

- `/proc/cpuinfo` — низкоуровневая информация ядра;
- `lscpu` — агрегированная topology;
- `lscpu -e` — соответствие CPU/NODE/SOCKET/CORE;
- `inxi -Cxxx` — краткое человекочитаемое резюме.

### Thermal check

```bash
sensors coretemp-isa-*
```

Read-only. Источник использует этот вывод как дополнительный способ увидеть число физических температурных сенсоров/ядер в конкретном примере.

## Interpreting topology

Не предполагать, что logical CPU нумеруются одинаково на разных системах.

Проверять:

```bash
lscpu -e
```

Сопоставлять колонки:

- `CPU`
- `SOCKET`
- `CORE`
- `NODE`

В источнике показаны разные схемы нумерации на разных Intel CPU и сервере с двумя sockets.

## Affinity

### POSIX model

Источник использует `cpu_set_t` и макросы `CPU_SET`, `CPU_CLR`, `CPU_ISSET`, `CPU_ZERO`, `CPU_COUNT` и др.

Для процесса:

```c
sched_getaffinity(...)
sched_setaffinity(...)
```

Для pthread:

```c
pthread_getaffinity_np(...)
pthread_setaffinity_np(...)
```

### Verify affinity count

Собираются два примера:

```bash
gcc how-many-p.c -Wall -o how-many-p
gcc how-many-t.c -Wall -lpthread -o how-many-t

./how-many-p
./how-many-t
```

Ожидаемый смысл результата: число set bits в effective affinity mask.

## taskset

Read-only/help:

```bash
taskset --help
taskset -p <PID>
```

State-changing:

```bash
taskset -p 03 <PID>
taskset -pc 0,3,7-11 <PID>
taskset -c 0-3 ./how-many-p
taskset -c 1,3,5,7,9 ./how-many-t
```

Effect: ограничивает CPU affinity существующего процесса или запускаемой команды.

Verification:

```bash
taskset -p <PID>
```

или проверка самого приложения, как в `how-many-*`.

Rollback: **[Needs confirmation]**; исходная affinity mask должна быть заранее сохранена вручную, если требуется безопасный rollback.

## Scheduling policies

Источник выделяет:

- `SCHED_OTHER`
- `SCHED_FIFO`
- `SCHED_RR`

Для API рассматриваются:

```c
sched_setscheduler()
sched_getscheduler()
sched_setparam()
sched_getparam()
getpriority()
setpriority()
pthread_setschedparam()
pthread_getschedparam()
pthread_setschedprio()
```

## nice

Read-only:

```bash
nice --help
```

State-changing example class:

```bash
nice -n <N> <command>
```

Источник объясняет nice как «уступчивость»: большее числовое значение → меньший scheduling priority для обычной задачи.

## chrt

Read-only:

```bash
chrt --help
chrt -p <PID>
```

High-risk state-changing examples из источника:

```bash
chrt -r 50 bash
chrt -r -p 5 <PID>
chrt -f 20 bash
chrt -r -p -r 10 <PID>
chrt -r -p -o 0 <PID>
```

Risk:

Real-time task с высоким static priority может не давать обычным задачам CPU time до блокировки/завершения самой RT-задачи.

Перед изменением:

1. зафиксировать PID;
2. сохранить текущую policy/priority через `chrt -p <PID>`;
3. иметь отдельный root shell/console для rollback;
4. не применять эксперимент на production workload.

Verification:

```bash
chrt -p <PID>
```

Rollback pattern, показанный источником концептуально: вернуть `SCHED_OTHER` и priority `0` через `chrt`; точная команда должна соответствовать фактическому PID и исходному состоянию.

## Acceptance checks

CPU topology:

- `lscpu -e` позволяет однозначно построить CPU→CORE→SOCKET mapping.

Affinity:

- после `taskset` effective CPU count/маска соответствует заданной.

Scheduling:

- после `chrt` `chrt -p PID` показывает требуемую policy/priority.

## Next action

Следующая глава переходит от инфраструктуры CPU/scheduler к моделям параллелизма процессов, потоков и Go concurrency.
