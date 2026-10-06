# Шпаргалка — глава 7: конкурентность в Go

## Fast model

~~~text
go func()
→ concurrent work
→ WaitGroup coordinates completion
→ channels move data/signals
→ mutex/atomic protect shared state
→ patterns structure concurrency
~~~

Scope: PDF 363–416.

## Goroutine

~~~go
go work()

go func() {
    ...
}()
~~~

Remember:
- main/application exit ends remaining goroutines;
- scheduling order is not deterministic;
- use synchronization, not sleep, to coordinate completion.

## WaitGroup

~~~go
var wg sync.WaitGroup
wg.Add(1)
go func() {
    defer wg.Done()
    ...
}()
wg.Wait()
~~~

Failure modes:
- extra `Add` → deadlock-like wait;
- extra `Done` → negative counter panic.

## Channels

~~~go
ch := make(chan int)
buf := make(chan int, 3)

ch <- 10
v := <-ch
v, ok := <-ch
close(ch)
~~~

Directional:

~~~go
<-chan T
chan<- T
~~~

Buffered state:

~~~go
len(ch)
cap(ch)
~~~

## select

~~~go
select {
case v := <-a:
    ...
case v := <-b:
    ...
case <-time.After(time.Second):
    return
}
~~~

Empty `select {}` blocks forever.

Nil channel assigned with `ch = nil` permanently blocks channel operations and disables its case in the source’s select pattern.

## Channel range

~~~go
for v := range ch {
    ...
}
~~~

Producer must eventually close the channel if consumer needs the range loop to terminate.

## Race detector

~~~bash
go run -race .\main.go
~~~

Race = unsynchronized shared-memory access where execution order changes the result.

## Mutex

~~~go
mu.Lock()
defer mu.Unlock()
~~~

Use for exclusive critical sections.

## RWMutex

~~~go
rw.RLock()
defer rw.RUnlock()

rw.Lock()
defer rw.Unlock()
~~~

Many readers, one writer.

## Atomic

~~~go
atomic.AddInt64(&value, 1)
atomic.LoadInt64(&value)
~~~

Use source-supported atomic operations for simple built-in shared values.

## GOMAXPROCS

Concept in chapter:

~~~text
logical CPUs / OS threads executing Go code
→ runtime concurrency ceiling
→ too low can reduce throughput
→ too high is not automatically better
~~~

## Patterns

| Pattern | Source purpose |
|---|---|
| Generator | lazy value production |
| Pipeline | staged channel-connected transformation |
| Queuing | N tasks across M goroutines |
| Fan-in | many input channels → one output |
| Fan-out | one input → many outputs |
| Worker Pool | fixed group of workers processes tasks |

## Project v.6

~~~text
AI candidate moves
→ goroutines
→ result channel
→ select best result

large-board win check
→ rows/cols + diagonals concurrently
→ result channel

DB save/load
→ goroutine
→ result channel / background completion
~~~

## Acceptance

After chapter you should be able to:
- distinguish process/thread/goroutine;
- distinguish concurrency/parallelism;
- start and wait for goroutines;
- use buffered/unbuffered and directional channels;
- explain `select`, nil channels and channel range;
- detect a data race;
- choose Mutex/RWMutex/atomic in source scenarios;
- explain GOMAXPROCS concept;
- identify six concurrency patterns;
- explain v.6 parallel AI/win-check/DB changes.

## Rollback / safety

Concurrency bugs are behavioral rather than configuration rollback problems. Verification in source is rerunning examples, using `-race`, and checking deterministic invariants such as final counter/balance. VCS rollback is not specified → `[Needs confirmation]`.
