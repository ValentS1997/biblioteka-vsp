# Cheatsheet — глава 7 «Масштабирование»

## Goal

Проверить, как Go workload масштабируется при изменении:

- аппаратной платформы;
- доступного числа CPU;
- числа goroutines;
- `GOMAXPROCS`;
- process affinity.

Не смешивать эти факторы в одном выводе.

## 1. Baseline hardware

Источник использует несколько классов систем:

- ARM SBC: Raspberry Pi 2;
- ARM SBC: Orange Pi One;
- x86 desktops с разным числом cores/SMT;
- DELL PowerEdge R420 с большим числом logical CPUs.

Read-only baseline:

```bash
inxi -MCxxx
inxi -Cxxx
inxi -mCxxx
free
lsb_release -a
cat /etc/debian_version
uname -a
go version
lscpu
```

## 2. Scheduler model

Source model:

```text
GOMAXPROCS
    ↓
runtime worker / OS-thread capacity
    ↓
goroutine queues
    ↓
goroutines scheduled across available execution resources
```

Источник сам подчёркивает, что детали scheduler существенно меняются между версиями Go. Поэтому эта модель используется как chapter model, а не как timeless runtime specification.

## 3. First experiment — mlpar

Цель: создать N CPU-like goroutines и наблюдать:

- elapsed time;
- thread IDs;
- распределение ветвей.

Примеры:

```bash
./mlpar
./mlpar 10
./mlpar -20
./mlpar -50
./mlpar -100
./mlpar -1000
```

В программе отрицательный параметр используется как application-specific switch: абсолютное значение задаёт число ветвей, а debug output отключается.

### Limitation discovered by source

В worker loop использовался `time.Now()`.

Автор отмечает, что это может создавать kernel/system interaction и нарушать чистоту CPU-bound experiment.

Это приводит к **второй методике**, а не к игнорированию первой.

## 4. Second experiment — mlpar2

Изменение:

- калибровать длительность заранее;
- внутри основной worker activity выполнять вычислительный цикл;
- не обращаться к time service в основном вычислительном цикле;
- после completion собирать thread-ID histogram.

Наблюдаемое:

- при числе goroutines меньше доступных processors распределение близко к one-per-worker model;
- когда goroutines больше processors, несколько goroutines обслуживаются одними runtime/OS threads;
- на малых ARM системах рост N быстрее увеличивает суммарное elapsed time;
- на многопроцессорном сервере высокая concurrency распределяется по большему числу execution resources.

## 5. Verification signals

Для каждого запуска фиксировать:

```text
hardware/platform
Go version
available CPU count
goroutine count
GOMAXPROCS
affinity mask / CPU list
actual completion time
worker/thread distribution
```

Не сравнивать только elapsed time без этих параметров.

## 6. GOMAXPROCS

Read current value in code:

```go
runtime.GOMAXPROCS(-1)
```

Set in code:

```go
runtime.GOMAXPROCS(n)
```

Set via shell environment:

```bash
export GOMAXPROCS=7
./numproc
```

One-command override:

```bash
GOMAXPROCS=9 ./numproc
```

Difference:

- `export` persists in current shell until changed/unset;
- inline assignment applies to the launched command environment.

Rollback for exported value: source does not show an explicit restoration command — **[Needs confirmation]**.

## 7. CPU availability diagnostics

```bash
cat /proc/cpuinfo | grep processor | wc -l
nproc
lscpu | grep 'CPU(s)'
```

These are read-only.

## 8. taskset

Read:

```bash
taskset -p <PID>
```

Launch constrained workload:

```bash
taskset -c 0-3 ./numproc
taskset -c 32,34,36,38 ./numproc
taskset -c 0-3 ./mlpar -40
taskset -c 0,2,4 ./mlpar -40
taskset -c 0,20 ./mlpar -40
```

Effect: process runs only on selected CPU list in source experiment.

Verification:

- application-reported CPU count;
- `taskset -p PID` for running process;
- expected workload result/timing.

Rollback for a launched one-shot command: process exits and constraint disappears with it.

For changing an already-running PID, exact rollback requires saving original mask first.

## 9. Interpretation rule

Correct comparison:

```text
same workload
+ known CPU set
+ known GOMAXPROCS
+ repeated runs
+ same measurement method
= useful comparison
```

Incorrect comparison:

```text
more goroutines → therefore faster
```

## Acceptance criteria

A scaling experiment is interpretable only if:

- platform is identified;
- CPU count/topology is known;
- Go version is recorded;
- GOMAXPROCS is known;
- affinity restrictions are known;
- workload does not unintentionally introduce blocking points;
- result correctness is checked;
- timing is repeated rather than inferred from one sample.
