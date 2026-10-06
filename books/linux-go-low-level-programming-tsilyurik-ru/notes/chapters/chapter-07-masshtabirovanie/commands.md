# Commands — глава 7 «Масштабирование»

Только команды, подтверждённые chapter RAG.

## Platform diagnostics

| Command | Class | Purpose |
|---|---|---|
| `inxi -MCxxx` | read-only | ARM machine/CPU inventory |
| `inxi -Cxxx` | read-only | CPU topology summary |
| `inxi -mCxxx` | read-only | memory + CPU summary |
| `sudo inxi -MCxxx` | elevated read-only | same diagnostic with elevated access |
| `free` | read-only | memory inventory |
| `lsb_release -a` | read-only | distribution info |
| `cat /etc/debian_version` | read-only | Debian version |
| `uname -a` | read-only | kernel/architecture |
| `go version` | read-only | active Go version |
| `lscpu | grep -i яд` | read-only | core/thread subset in localized output |

## Build

```bash
time go build mlpar.go
ls -l mlpar
```

Classification:

- `go build`: state-changing local build, creates/replaces executable;
- `time`: measurement wrapper;
- `ls -l`: read-only verification.

Rollback build artifact: **[Needs confirmation]**.

## First scaling workload

```bash
./mlpar
./mlpar 10
./mlpar -20
./mlpar -50
./mlpar -100
./mlpar -1000
./mlpar 2
./mlpar 4
./mlpar -10
./mlpar 5
./mlpar 8
./mlpar 7
./mlpar -40
```

Class: workload-generating.

Negative argument is application semantics shown by source: disable debug while using the absolute value as branch count.

## Second scaling workload

```bash
./mlpar2
./mlpar2 7
./mlpar2 -20
./mlpar2 -50
./mlpar2 -100
./mlpar2 -9
```

Class: workload-generating CPU experiment.

The source presents `mlpar2` as an improved methodology after identifying system-time calls inside the first worker loop.

## CPU-count diagnostics

```bash
nproc
cat /proc/cpuinfo | grep processor | wc -l
lscpu | grep 'CPU(s)'
```

Class: read-only.

## GOMAXPROCS experiments

```bash
./numproc
./numproc 5
export GOMAXPROCS=7; ./numproc
GOMAXPROCS=9; ./numproc
```

Classification:

- `./numproc*`: workload/diagnostic;
- `export GOMAXPROCS=7`: modifies current shell environment;
- inline `GOMAXPROCS=9`: modifies environment only for launched command.

Verification: `numproc` output.

Persistent shell rollback after `export`: **[Needs confirmation]** because source does not show it explicitly.

## Affinity diagnostics

```bash
taskset --help
ps
taskset -p 8148
```

Class: read-only.

PID `8148` is source-example-specific.

## Affinity-constrained workload

```bash
taskset -c 0-3 ./numproc
taskset -c 32,34,36,38 ./numproc

taskset -c 0-3 ./mlpar -40
taskset -c 0,2,4 ./mlpar -40
taskset -c 0,20 ./mlpar -40
```

Class: state-constraining + workload.

Effect: selected process is launched with restricted CPU affinity.

Risk:

- CPU list is hardware/topology-specific;
- values such as `0,20` are meaningful only for the topology demonstrated by the source;
- copying these CPU IDs to another host without `lscpu` validation is unsafe/meaningless.

Verification:

```bash
taskset -p <PID>
```

and application-reported runtime CPU/thread state.

## Safe execution order derived from chapter

```text
read topology
→ record Go version
→ record baseline CPU count
→ run baseline workload
→ restrict GOMAXPROCS or affinity
→ rerun same workload
→ compare results
```
