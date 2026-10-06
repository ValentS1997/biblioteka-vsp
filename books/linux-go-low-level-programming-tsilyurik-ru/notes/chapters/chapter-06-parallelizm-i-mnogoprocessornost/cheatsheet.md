# Cheatsheet — глава 6 «Параллелизм и многопроцессорность»

## Problem framing

Нужно выбрать модель параллельного выполнения и не смешивать три разных уровня:

1. process isolation;
2. kernel threads;
3. user-space goroutines.

При этом конкурентная структура программы и фактическое выполнение на нескольких CPU — не одно и то же.

## 1. Processes / fork

Источник описывает `fork()` как разветвление текущего процесса:

- child получает `0`;
- parent получает PID child;
- отрицательное значение означает failure.

Ключевое свойство: после ветвления процессы логически имеют отдельные address spaces. Copy-on-write оптимизирует начальное копирование, но не превращает переменные parent/child в общий shared state.

Практическое следствие: IPC нужен отдельно.

## 2. POSIX threads

pthread model:

```text
process owns memory/resources
threads provide parallel execution
threads share process address space
```

Источник показывает:

```c
pthread_create(...)
pthread_join(...)
pthread_self()
pthread_exit(...)
```

Сборка примера:

```bash
g++ -O3 threads.cc -lpthread -o threads
```

Verification:

```bash
./threads 3
```

Наблюдение: порядок сообщений между запусками меняется.

## 3. C++ threads

`std::thread` рассматривается как более удобная надстройка над kernel-thread model.

Источник показывает:

- function target;
- arguments в constructor;
- functor;
- `join()` для ожидания.

Главный смысл не в синтаксисе C++, а в сохранении той же shared-memory concurrency model.

## 4. Goroutines

Базовый запуск:

```go
go function(args...)
```

Источник подчёркивает:

- нет специального thread-function prototype;
- goroutines внутри программы используют одно address space;
- runtime планирует множество goroutines на набор OS threads;
- вызывающий код не ждёт goroutine автоматически.

Поэтому завершение `main()` без ожидания может завершить процесс раньше фоновых goroutines.

## 5. Channels

Создание:

```go
c1 := make(chan string)
c2 := make(chan string, 100)
```

Передача:

```go
c <- value
value = <-c
```

Directional function parameters:

```go
func retrans(in <-chan string, out chan<- string)
```

Закрытие и проверка:

```go
close(c)
v, ok := <-c
for v := range c {
    // ...
}
```

## 6. select

```go
select {
case x := <-c:
    // receive
case out <- value:
    // send
default:
    // no channel operation ready
}
```

Без `default` select может блокироваться до готовности branch. С `default` источник показывает non-blocking attempt.

## 7. Closure capture

Источник демонстрирует три варианта:

- closure directly captures loop variable;
- loop value передаётся argument в closure;
- создаётся новая переменная `v := v`.

Конкретный результат первого варианта является version-scoped source claim; см. `source-findings.md`.

## 8. sync

### Mutex

```go
m.Lock()
m.Unlock()
```

Источник: если mutex уже захвачен, вызывающая goroutine блокируется.

### Cond

Pattern:

```go
c.L.Lock()
for !condition() {
    c.Wait()
}
// use condition
c.L.Unlock()
```

### RWMutex

Разделяет reader и writer locking:

- `RLock/RUnlock`;
- `Lock/Unlock`.

### Once

```go
once.Do(initFunc)
```

Один экземпляр `Once` выполняет функцию только один раз.

### WaitGroup

```go
wg.Add(1)
go func() {
    defer wg.Done()
    // work
}()
wg.Wait()
```

Используется как completion barrier.

### atomic

Источник перечисляет семейства:

- Add;
- CompareAndSwap;
- Load;
- Store;
- Swap.

## 9. Concurrency vs parallelism

Источник разделяет:

- concurrency — структура/взаимодействие goroutines;
- parallelism — реальное использование CPU hardware.

Диагностика в примерах:

```go
runtime.NumCPU()
runtime.GOMAXPROCS(-1)
```

Изменение:

```go
runtime.GOMAXPROCS(n)
```

Historical behavior `GOMAXPROCS` зависит от версии и явно отмечен источником как изменявшийся.

## 10. Performance lesson

`smp1`: atomic increment.

`smp2`: send through channel to dedicated counter goroutine.

В конкретном тесте high-level channel synchronization оказывается значительно дороже trivial increment.

Главный вывод главы:

> увеличивать число параллельных ветвей без оценки synchronization/cache overhead нельзя.

## Verification / acceptance

Для любого parallel experiment:

1. одинаковый workload;
2. фиксированное число operations;
3. подтверждённое число CPU/runtime execution threads;
4. проверенный итоговый result count;
5. повторные запуски;
6. интерпретировать порядок величин, а не один timing sample.

## Rollback

Примеры главы преимущественно создают локальные build artifacts и workload.

Rollback build artifacts: **[Needs confirmation]**.

Изменение `runtime.GOMAXPROCS(n)` действует для текущего процесса; source-defined persistent rollback не требуется.
