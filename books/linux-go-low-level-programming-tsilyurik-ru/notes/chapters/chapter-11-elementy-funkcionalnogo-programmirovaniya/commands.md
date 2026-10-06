# Commands — глава 11 «Элементы функционального программирования»

Только команды, подтверждённые RAG страниц 233–243.

| Command | Class | Purpose |
|---|---|---|
| `./clos1.py` | workload | Python closure example |
| `go run clos1.go` | compile-run | Go closure example |
| `./clos3.py` | workload | Python default-parameter closure-like example |
| `make` | state-changing build | Build comparative C/C++/Go closure examples |
| `./clos_c` | workload | C static-state implementation |
| `./clos_gcc` | workload | GCC nested-function implementation |
| `./clos_cc` | workload | C++ functor implementation |
| `./clos_cc11` | workload | C++11 lambda implementation |
| `./clos_go` | workload | Go gc closure implementation |
| `./clos_go.gcc` | workload | gccgo implementation |
| `./clos.py` | workload | Python comparison |
| `./curry1.py` | workload | Python currying example |
| `go build curry1.go` | state-changing build | Build Go currying example |
| `./curry1` | workload | Verify Go currying |
| `go fmt btree.go` | state-changing source edit | Format tree example |
| `go run btree.go` | compile-run | Run recursive tree traversal |
| `./fibos 15` … `./fibos 45` | CPU workload | Naive recursive Fibonacci |
| `./fibom 15` … `./fibom 70` | CPU workload | Memoized Fibonacci |
| `go fmt nomut.go` | state-changing source edit | Format pure-function example |
| `go run nomut.go` | compile-run | Run immutable-value style example |

## Makefile output shown by source

```bash
gcc -Wall -O0 clos_c.c -o clos_c
gcc -Wall -O0 clos_gcc.c -o clos_gcc
g++ -Wall -std=gnu++11 -O0 clos_cc.cc -o clos_cc
g++ -Wall -std=gnu++11 -O0 clos_cc11.cc -o clos_cc11
gccgo -Wall clos_go.go -g -O0 -o clos_go.gcc
go build -o clos_go -compiler gc clos_go.go
```

Effects: creates/replaces local binaries.

Rollback/cleanup command is not shown by source: **[Needs confirmation]**.

## Verification

All closure comparison variants should produce the same accumulated values:

```text
8 14 21 26 29 29 38
```

Tree:

```text
[1 2 3 4 5 6]
```

Pure-value example:

```text
6 10
```

Fibonacci comparison must verify both result and timing; timing alone is insufficient.

## Risk

No privileged/system-changing commands are present.

Potential practical risk: large naive Fibonacci input can consume substantial CPU/time because the source intentionally uses exponential recursive work.
