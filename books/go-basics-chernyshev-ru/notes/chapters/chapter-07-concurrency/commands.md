# Команды и инструменты — глава 7

Source policy: `rag_only`.

## Race detector

~~~bash
go run -race .\main.go
~~~

Type: workload-generating diagnostic command.

Purpose:
- detect shared-memory data races;
- print conflicting read/write stacks;
- return non-zero status when races are found in source example.

Source dependency note:

~~~text
go: -race requires cgo; enable cgo by setting CGO_ENABLED=1
~~~

The chapter’s Windows setup additionally requires GCC/MinGW for cgo-backed race detection.

## Goroutine primitives

### Start

~~~go
go functionCall()
go func() { ... }()
~~~

### WaitGroup

~~~go
wg.Add(1)
defer wg.Done()
wg.Wait()
~~~

## Channel primitives

~~~go
ch := make(chan T)
ch := make(chan T, capacity)
ch <- value
value := <-ch
value, ok := <-ch
close(ch)
len(ch)
cap(ch)
~~~

Directional channel types:

~~~go
<-chan T
chan<- T
~~~

## `select`

~~~go
select {
case value := <-ch1:
    ...
case ch2 <- value:
    ...
case <-time.After(time.Second):
    ...
default:
    ...
}
~~~

Source warns that `default` can be less safe when arrival intervals vary.

## Mutexes

~~~go
var mu sync.Mutex
mu.Lock()
mu.Unlock()
~~~

RWMutex:

~~~go
var rw sync.RWMutex
rw.RLock()
rw.RUnlock()
rw.Lock()
rw.Unlock()
~~~

## Atomic operations

~~~go
atomic.AddInt64(&value, 1)
atomic.LoadInt64(&value)
~~~

Package: `sync/atomic`.

## GOMAXPROCS

The chapter changes the runtime GOMAXPROCS setting in code and compares execution time. The exact function token is noisy in the extracted RAG, so this artifact does not silently normalize its spelling.

Verified semantic meaning:
- controls number of OS threads allowed to execute Go code simultaneously;
- default corresponds to logical CPU count in source framing.

## Project v.6 operational primitives

### Candidate-move evaluation

~~~go
resultChan := make(chan moveResult, len(emptyCells))
var wg sync.WaitGroup

for _, cell := range emptyCells {
    wg.Add(1)
    go func(...) {
        defer wg.Done()
        ...
        resultChan <- result
    }(...)
}
wg.Wait()
close(resultChan)
~~~

### Parallel win-check result aggregation

~~~go
resultChan := make(chan bool, 3)
wg.Add(3)
...
go func() {
    wg.Wait()
    close(resultChan)
}()

for result := range resultChan {
    if result {
        return true
    }
}
~~~

### Background persistence

~~~go
go func(snapshot *model.GameSnapshot) {
    err := repository.SaveSnapshot(...)
    ...
}(snapshot)
~~~

## Verification matrix

| Mechanism | Verification | Failure signal |
|---|---|---|
| WaitGroup | all work finishes before return | deadlock / negative counter panic |
| channel range | loop exits after close | deadlock if producer never closes |
| race protection | `go run -race` clean | DATA RACE report |
| Mutex/RWMutex | invariant final value holds | inconsistent shared state |
| atomic | counter reaches expected value | unexpected count |
| project parallelism | same functional result with concurrent path | wrong move/win/save/load behavior |
