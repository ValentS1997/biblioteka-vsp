# Диаграмма — глава 7: goroutines, channels and synchronization

~~~mermaid
flowchart TD
    A["Application"] --> B["go function()"]
    B --> C["goroutines"]
    C --> C1["WaitGroup: completion"]
    C --> D["channels: communication"]
    D --> D1["unbuffered / buffered"]
    D --> D2["directional channels"]
    D --> D3["select / timeout / nil channel"]
    D --> D4["range until close"]

    C --> E["shared memory"]
    E --> E1["race condition"]
    E1 --> E2["go run -race"]
    E1 --> F["synchronization"]
    F --> F1["Mutex"]
    F --> F2["RWMutex"]
    F --> F3["sync/atomic"]

    C --> G["runtime scheduling"]
    G --> G1["GOMAXPROCS"]

    D --> H["patterns"]
    H --> H1["Generator"]
    H --> H2["Pipeline"]
    H --> H3["Queuing"]
    H --> H4["Fan-in"]
    H --> H5["Fan-out"]
    H --> H6["Worker Pool"]

    H --> I["Tic-tac-toe v.6"]
    I --> I1["parallel AI strategies"]
    I --> I2["parallel win checks"]
    I --> I3["async DB save/load"]
~~~

## Synchronization decision map

~~~text
Need to wait for goroutines?
→ WaitGroup

Need to transfer data/signal?
→ channel

Need one goroutine to mutate shared state?
→ Mutex

Many readers + exclusive writer?
→ RWMutex

Simple supported built-in atomic value?
→ sync/atomic

Need to detect unsynchronized shared access?
→ go run -race
~~~

## Channel pattern map

~~~text
one producer on demand → Generator
stages in sequence → Pipeline
N tasks to M concurrent handlers → Queuing
many streams to one → Fan-in
one stream to many → Fan-out
fixed worker group → Worker Pool
~~~

## Project v.6 flow

~~~text
candidate moves
→ parallel evaluators
→ channel
→ best move

large board
→ parallel row/column/diagonal checks
→ bool channel
→ win result

DB call
→ goroutine
→ background save OR result channel
→ UI keeps progressing
~~~

## Provenance

- goroutines / WaitGroup: `p0363:c01–p0367:c01`
- channels/select: `p0368:c01–p0378:c01`
- race/mutex/atomic: `p0379:c01–p0389:c01`
- GOMAXPROCS/patterns: `p0389:c01–p0400:c01`
- project v.6: `p0401:c01–p0414:c01`
