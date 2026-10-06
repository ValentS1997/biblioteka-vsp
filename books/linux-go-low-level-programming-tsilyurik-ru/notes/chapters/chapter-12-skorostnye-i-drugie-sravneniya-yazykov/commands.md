# Commands — глава 12 «Скоростные и другие сравнения языков»

Только commands, подтверждённые RAG pages 244–257.

## Environment / tools

| Command | Class | Purpose |
|---|---|---|
| `sudo apt install clang` | privileged state-changing | Install Clang package |
| `gcc --version` | read-only | GCC version |
| `clang --version` | read-only | Clang version |
| `go version` | read-only | Go version |
| `ls -l \| grep rwx` | read-only | Inspect executable files/sizes |
| `file fibo_go` | read-only | Inspect gccgo binary format |
| `ldd fibo_go` | read-only | Inspect dynamic dependencies |
| `file fibo_gc` | read-only | Inspect gc binary format |
| `ldd fibo_gc` | read-only | Check dynamic linkage status |

## Measurement

```bash
time <command> <size>
time nice -9 <command> <size>
```

`time`: measurement wrapper.

`nice -9`: scheduling-priority change for launched process; not read-only.

## Build

The chapter repeatedly uses:

```bash
make
```

Shown build commands include GCC, G++, Clang, gccgo and `go build`.

Effect: creates/replaces local binaries.

Rollback/cleanup:

- bubble-sort Makefile explicitly shows `clean: rm -f $(TASK)`;
- generalized cleanup for all chapter examples: **[Needs confirmation]**.

## Fibonacci

```bash
time ./fibo_c 42
time ./fibo_cc 42
time ./fibo_cl 42
time ./fibo_go 42
time ./fibo_gc 42
```

Expected result for each:

```text
433494437
```

## Bubble sort

```bash
./sort_go
./sort_go -20

time ./sort_c 20000
time ./sort_cc 20000
time ./sort_cl 20000
time ./sort_go 20000
time ./sort_gc 20000
```

Expected swap count for `20000`:

```text
199990000
```

## Tower of Hanoi

```bash
./hanoy_c -3

time ./hanoy_c 30
time ./hanoy_cl 30
time ./hanoy_go 30
time ./hanoy_gol 30
```

Expected move count for `30`:

```text
1073741823
```

## Sieve

```bash
time ./erastof_c 50000000
time ./erastof_cl 50000000
time ./erastof_go 50000000
time ./erastof_gol 50000000
```

Expected count:

```text
3001134
```

## Risk / acceptance

Before trusting a timing:

- verify output/result;
- verify optimization level;
- verify host load/context;
- repeat the run;
- do not compare unlike source structures as if compiler/language were the only variable.
