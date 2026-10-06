# Commands — глава 13 «Многопроцессорные параллельные вычисления»

Только commands, подтверждённые RAG pages 258–279.

## Activation benchmarks

```bash
make

./gotim1
./gotim2
./forktim
./thretim

./gotim1 10
./gotim2 10
./forktim 10
./thretim 10

./gotim1 10000
./gotim2 10000
./thretim 10000
./forktim 10000
```

Large source runs:

```bash
./gotim1 1000000
./gotim2 1000000
./gotim1 10000000
./gotim2 10000000
```

Class: CPU/resource workload.

Risk: very high branch/process/thread counts can exhaust memory/process/thread limits or destabilize a host.

## Resource-limit inspection

Read-only:

```bash
ulimit -u
ulimit -i
ulimit -s
cat /proc/sys/kernel/threads-max
```

Source also shows privileged modifications:

```bash
ulimit -u 500000
echo 1100000 > /proc/sys/kernel/threads-max
ulimit -s 256
ulimit -i 120000
```

Classification: **high-risk state-changing resource tuning**.

Before any such change:

- capture original value;
- confirm shell/process/system scope;
- have a recovery shell;
- do not apply on production/shared systems merely to run a benchmark.

Rollback values: target-host-specific, therefore **[Needs confirmation]**.

## Race example

```bash
./race 1
./race 2
./race 4
./race 10
./race 20
./race 40
```

Build:

```bash
go build race.go
go build -race race.go
ls -l race
```

Race-detector build is diagnostic instrumentation and has very different performance characteristics.

## Protected counter variants

Atomic:

```bash
./racea 1
./racea 2
./racea 4
./racea 10
./racea 20
./racea 40
```

Mutex:

```bash
./racem 1
./racem 2
./racem 4
./racem 10
./racem 20
./racem 40
```

Channel/semaphore-labeled source variant:

```bash
./races 1
./races 2
./races 4
./races 10
./races 20
./races 40
```

Important: the printed `races.go` listing does not visibly protect `counter++`; see `source-findings.md`.

## Local toy hash-scaling example

The source uses local, known toy strings/hashes to demonstrate CPU scaling:

```bash
printf xyz98 | md5sum | ./bruteforce
printf xyz98 | md5sum | ./bruteforce -m
printf xyzyw | md5sum | ./bruteforce -b 2
printf xyzyw | md5sum | ./bruteforce -b 5
printf xyzyw | md5sum | ./bruteforce -b 10
printf xyzyw | md5sum | ./bruteforce -b 20
printf xyzyw | md5sum | ./bruteforce -b 200
```

Classification: local CPU workload from the book.

Scope boundary: keep this as the toy demonstration shown by source; do not adapt it to real accounts, services, or credentials.

## Channels / timers

```bash
./multy
./timer
./timera
./tickers
```

Class: interactive/asynchronous local workload.

## Basel-series comparison

Sequential:

```bash
./bazel0 1e-17
./bazel0 1e-7
./bazel0 1e-13
./bazel0 1e-15
```

Parallel attempt:

```bash
./bazel 1 1e-5
./bazel 1 1e-7
./bazel 1 1e-13
./bazel 1 1e-15
./bazel 2 1e-13
./bazel 10 1e-13
./bazel 20 1e-13
./bazel 40 1e-13
```

Acceptance: compare result accuracy, term count and elapsed time against `bazel0`; do not assume more workers should be faster.
