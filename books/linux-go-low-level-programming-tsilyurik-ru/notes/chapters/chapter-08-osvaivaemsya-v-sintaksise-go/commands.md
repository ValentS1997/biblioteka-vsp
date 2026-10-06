# Commands — глава 8 «Осваиваемся в синтаксисе Go»

Только shell-команды, подтверждённые chapter RAG.

## CLI example

```bash
./echo повторяет то что я пишу
./echo -n 12345
./echo -z 12345
./echo 12345 -n
./echo -h
./echo --help
```

Class: workload / CLI behavior check.

## Sqrt comparison

```bash
ls -l | grep x
./sqrt_c 10
./sqrt_cl 10
./sqrt_go 10
./sqrt_gc 10
```

`ls`: read-only.

Executions: workload.

Build rules are shown in the source Makefile and invoke GCC, Clang, gccgo and `go build`; these create local binaries.

## π and arbitrary precision

```bash
./pi.py 80
go run pi.go 80
./newton
```

Class:

- `./pi.py`, `./newton`: workload;
- `go run`: compile-and-run workflow.

## Streaming statistics

```bash
make
time ./sko 100000000
time ./skoc 100000000
```

`make`: state-changing build.

Timed runs: CPU workload.

Source caveat: timings are not a clean language benchmark because random generators differ.

## Polygon

```bash
go build -o triangle triangle.go
./triangle
```

Build: state-changing local artifact.

Run: interactive workload.

## Sequential TCP echo server

```bash
go build -o echo_serv echo_serv.go
ls -l echo_serv*
./echo_serv
```

Network effect: process listens on source-selected TCP port `51500`.

Verification clients:

```bash
nc 127.0.0.1 51500
socat tcp4:127.0.0.1:51500 STDOUT
telnet 127.0.0.1 51500
```

Risk:

- port may already be occupied;
- bind/listen behavior depends on source code;
- process remains active until stopped.

Rollback: terminate server process; exact process-management command is not specified by source.

## Go TCP client

```bash
go build -o echo_cli echo_cli.go
ls -l echo_cli*
./echo_cli
./echo_cli 51501
```

Build: state-changing.

Run: network workload.

## Concurrent TCP server

```bash
go build -o echo_servm echo_servm.go
ls -l echo_servm*
```

Network test set:

```bash
./echo_cli 51501
nc 127.0.0.1 51501
socat tcp4:127.0.0.1:51501 STDOUT
telnet 127.0.0.1 51501
```

Source demonstrates simultaneous clients on the same server port.

## HTTP server

```bash
./http
```

Network workload: local HTTP listener on `localhost:4000` in shown source code.

Verification: browser request to `http://localhost:4000/`.

## map iteration

```bash
./map4rand
```

Run repeatedly to observe iteration order.

## Rollback / cleanup

The chapter does not provide a canonical build cleanup workflow for all examples.

- build artifact removal: **[Needs confirmation]**
- persistent network services: terminate the started process
- no system package/config changes are part of this chapter
