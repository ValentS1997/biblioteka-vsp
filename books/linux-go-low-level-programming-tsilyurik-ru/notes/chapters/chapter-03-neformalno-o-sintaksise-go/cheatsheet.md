# Cheatsheet — глава 3 «Неформально о синтаксисе Go»

## Symptom / problem framing

Нужно быстро получить рабочую модель базового Go-синтаксиса без попытки охватить весь язык. Источник строит объяснение через отличия от C/C++ и через небольшие исполнимые примеры.

## Baseline / context

Глава предполагает хотя бы поверхностное знакомство с C и фокусируется на конструкциях, которые понадобятся дальше.

Базовые правила по источнику:

- перенос строки участвует в синтаксисе через автоматическую постановку `;`;
- предпочтителен единый формат через `gofmt`/`go fmt`;
- управляющие конструкции сведены к `if`, `for`, `switch`;
- типы не смешиваются неявно;
- неиспользуемые переменные/import считаются ошибкой компиляции;
- `_` используется как пустой идентификатор.

## Read-only checks

### Formatting/tool help

```bash
which gofmt
gofmt --help
go help fmt
```

### Inspecting examples/output

В главе результаты примеров проверяются обычным запуском готовых программ:

```bash
./circle
./object3
./panic
./string2
./bigint
```

Это workload-generating executions, но не системные изменения.

## Interpretation

### Syntax and formatting

Если перенос строки поставлен в позиции, где Go автоматически завершает выражение, структура кода может измениться. В качестве практического инструмента источник рекомендует formatter, а не ручное управление стилем.

### Types

Источник подчёркивает:

- явные преобразования;
- различие именованных типов;
- `byte` и `rune` как специальные имена/синонимы в своих контекстах;
- zero values для объявленных переменных;
- short declaration `:=`.

### Data structures

Ключевые механизмы:

- arrays — значения;
- slices — дескрипторные структуры поверх базового массива;
- `new(T)` возвращает указатель на обнулённое значение;
- `make` применяется для slice/map/channel и подготавливает внутренние структуры;
- map поддерживает чтение, запись, `delete` и двухзначную проверку присутствия.

### Control flow

- `for` покрывает обычный цикл, while-подобную форму и бесконечный цикл;
- `switch` по умолчанию не проваливается в следующий case;
- `fallthrough` используется явно;
- `++`/`--` рассматриваются как statements, а не выражения.

### Functions

Глава показывает:

- функции как значения;
- множественные возвращаемые значения;
- именованные результаты;
- variadic parameters;
- анонимные функции и closures;
- `defer`;
- функции высших порядков.

### Methods and interfaces

Метод — функция с receiver. Receiver может быть value или pointer.

Интерфейс задаётся набором методов. Реализация не декларируется отдельно: тип удовлетворяет интерфейсу, если имеет нужные методы.

### Errors

Обычная ошибка передаётся как значение `error`. Для экстремального пути рассматриваются `panic`, `defer`, `recover`.

## Next action

После этой главы уже можно читать последующие разделы, где конструкции используются без постоянного объяснения базового синтаксиса.

Практический порядок закрепления:

1. formatter и простые объявления;
2. arrays/slices/maps;
3. `for`/`switch`;
4. функции и multiple return;
5. методы/interfaces;
6. error flow;
7. package/import/testing.

## Modifying action

### Formatting

`go fmt`/режим записи `gofmt -w` изменяет исходный код.

Effect: форматирование файла/пакета.

Risk: рабочий файл переписывается.

Verification: inspect/diff результата.

Rollback: **[Needs confirmation]** — источник не задаёт VCS/backup rollback.

### Building examples

Примеры:

```bash
go build panic.go
go build -o string3 string3.go
go build -o string2 string2.go
go build -o bigint bigint.go
```

Effect: создают/заменяют build artifacts.

Verification: запуск полученного бинарника; для `bigint` также используется `ls -l bigint`.

Rollback: **[Needs confirmation]**.

## Verification / acceptance checks

Для синтаксической/форматной части:

```bash
which gofmt
gofmt --help
go help fmt
```

Для executable examples:

- сборка проходит;
- программа запускается;
- вывод совпадает с ожидаемым поведением примера.

Для testing subsection source-defined acceptance:

- файл имеет суффикс `_test.go`;
- импортирован `testing`;
- test function имеет форму `TestFoo(t *testing.T)`;
- `go test` находит, собирает и запускает тесты.

## Rollback

Source-supported общего rollback workflow нет.

- formatter rewrite: **[Needs confirmation]**
- build artifacts: **[Needs confirmation]**
- `go test`: [Not applicable] для исходного кода, если тест сам не имеет внешних side effects; такие side effects в главе не рассматриваются.
