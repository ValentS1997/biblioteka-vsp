# Ответы на вопросы для самопроверки — глава 7

Это RAG-grounded ответы по материалу главы. Они не являются официальным издательским ключом.

## 1. Process, thread, goroutine

По source framing:
- **process** — running program instance с instructions, data и OS resources;
- **thread** — более лёгкая execution entity внутри process, имеющая собственный flow/control и stack;
- **goroutine** — ещё более лёгкая Go execution entity, которой управляет Go scheduler, а не напрямую OS.

Goroutines выполняются внутри threads, которые существуют внутри process.

Provenance: `p0363:c01`.

## 2. Concurrency vs parallelism

**Concurrency** — организация задач так, что они могут выполняться поочерёдно/interleaved или частично одновременно.

**Parallelism** — фактическое одновременное выполнение нескольких computations.

Source example: один человек переключается между утренними задачами — concurrency; кофемашина/второй человек выполняет часть работы одновременно — parallelism.

Provenance: `p0363:c01–p0364:c01`.

## 3. Как Go реализует concurrent execution?

Через goroutines, которые планируются Go runtime scheduler. Дополнительные mechanisms chapter вводит для coordination/communication: `sync.WaitGroup`, channels, mutexes и atomics.

Provenance: `p0363:c01–p0368:c01`, `p0379:c01–p0389:c01`.

## 4. Как запустить goroutine?

Поставить keyword `go` перед function call или immediately invoked anonymous function:

~~~go
go work()
go func() {
    ...
}()
~~~

Provenance: `p0364:c01–p0365:c01`.

## 5. Нюансы goroutines

Source highlights:
- application exit terminates remaining goroutines;
- execution order is not guaranteed without synchronization;
- `time.Sleep` is not a proper completion mechanism for real programs;
- function invoked with `go` is not used as an expression returning a value;
- goroutine completion should be coordinated with mechanisms such as `WaitGroup` or channels.

Provenance: `p0364:c01–p0367:c01`.

## 6. Channels

Channels are the chapter’s mechanism for communication/data exchange between goroutines.

Create:

~~~go
ch := make(chan int)
buf := make(chan int, 3)
~~~

Send/receive:

~~~go
ch <- value
value := <-ch
value, ok := <-ch
~~~

Close:

~~~go
close(ch)
~~~

Each channel carries one element type. Source examples use channels between producer/consumer goroutines and close them when range-based reading must terminate.

Provenance: `p0368:c01–p0378:c01`.

## 7. Direction of channel transfer

Receive-only:

~~~go
<-chan T
~~~

Send-only:

~~~go
chan<- T
~~~

Source uses directional channels to make producer/consumer responsibilities explicit, especially in pipeline-style code.

Provenance: `p0370:c01–p0371:c01`.

## 8. `select`

`select` is a channel-specific control structure similar to `switch` in source framing.

It allows one goroutine to wait on multiple channel operations.

Behavior shown:
- if none are ready, it blocks;
- if multiple are ready, runtime chooses one;
- `time.After` can provide timeout;
- `default` can provide non-blocking fallback;
- empty `select {}` blocks forever.

Provenance: `p0373:c01–p0376:c01`.

## 9. Nil channel

Source defines a nil channel as a channel variable assigned `nil`.

Operations on it block permanently, so its case effectively stops participating in `select`.

Provenance: `p0377:c01`.

## 10. Race condition and detection

Race condition occurs when goroutines share memory and unsynchronized writes/reads make the result depend on execution order.

Detection command from chapter:

~~~bash
go run -race .\main.go
~~~

The detector prints conflicting access stacks and reports `DATA RACE`.

Provenance: `p0379:c01–p0380:c01`.

## 11. Mutexes

Mutex protects a critical section so only one goroutine can write/access it at a time.

Example:

~~~go
mutex.Lock()
defer mutex.Unlock()
value = value + 1
~~~

`sync.RWMutex` additionally allows many readers through `RLock/RUnlock` while writes remain exclusive.

Provenance: `p0380:c01–p0384:c01`.

## 12. Atomic vs ordinary operations

Source defines an atomic operation as one that completes as a single indivisible step and cannot be interrupted halfway.

Ordinary read-modify-write operations may race across goroutines.

Chapter example replaces `value = value + 1` with:

~~~go
atomic.AddInt64(&value, 1)
~~~

and reads with `atomic.LoadInt64`.

Provenance: `p0387:c01–p0389:c01`.

## 13. Generator

Used for lazy production of a sequence on demand.

Producer sends values through a channel; consumer receives them as needed.

Provenance: `p0390:c01–p0391:c01`.

## 14. Pipeline

Used when processing can be divided into sequential stages connected by channels.

Each stage receives values, transforms/filters them and passes them to the next stage. Source highlights independent modification/reordering of stages.

Provenance: `p0391:c01–p0393:c01`.

## 15. Queuing

Used to distribute N tasks among M goroutines and process several elements concurrently.

Source commonly uses a buffered channel, where channel capacity limits the amount of concurrently handled work.

Provenance: `p0393:c01–p0394:c01`.

## 16. Fan-in

Merges several input channels into one output channel.

Source compares it to a multiplexer and notes that ordering is not guaranteed.

Provenance: `p0395:c01–p0396:c01`.

## 17. Fan-out

Splits one input channel into multiple output channels so work/data can be distributed in parallel directions.

Provenance: `p0397:c01–p0398:c01`.

## 18. Worker Pool

Used when work should be distributed across a fixed set of worker goroutines that process tasks concurrently and send results to a common output channel.

Source says the ideal worker count is related to the number of logical CPU cores.

Provenance: `p0399:c01–p0400:c01`.
