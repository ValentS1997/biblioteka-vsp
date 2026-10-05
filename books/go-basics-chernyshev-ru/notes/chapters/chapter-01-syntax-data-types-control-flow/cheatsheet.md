# Шпаргалка — глава 1: синтаксис, типы данных и управляющие конструкции Go

## Baseline / context

Глава — фундаментальная. Она вводит минимальный рабочий набор языка и сразу применяет его в консольном проекте.

~~~text
Go toolchain
→ module + main.go
→ variables/types
→ collections
→ operators/control flow
→ conversions/I/O
→ stdlib helpers
→ tic-tac-toe v.0
~~~

Provenance: PDF 16–100, `p0016:c01–p0100:c01`.

## Symptom / problem framing

Типовые проблемы, которые глава учит распознавать:

| Симптом | Что проверить |
|---|---|
| приложение не запускается | есть ли `package main` и `func main()`; корректны ли types/braces |
| переменная не компилируется после повторного объявления | не использован ли `:=` вместо `=` |
| Unicode-строка индексируется странно | byte index vs rune |
| изменение одного slice меняет другой | общий backing storage |
| numeric expression не компилируется | типы операндов различаются |
| после narrowing получено неожиданное число | отсечение битов / overflow |
| цикл не заканчивается | condition / `break` / `continue` / `goto` |
| сложная цепочка `if/else` | возможно, подходит `switch/case` |

## Read-only checks

### Toolchain

~~~bash
go version
~~~

Проверяет успешность установки Go.

### Type / value inspection inside code

Глава использует:
- `reflect.TypeOf(value)`;
- `fmt.Printf("%T", value)`;
- `fmt.Printf("%v", value)`.

Это code-level inspection, а не shell checks.

## Interpretation

### Variable declaration

~~~go
var value int
var value2 = 10
value3 := 20
value3 = 30
~~~

- `var` — обычное объявление;
- type может быть указан явно или выведен;
- `:=` — short declaration;
- `=` — последующее присваивание.

### Naming

- meaningful names;
- `mixedCaps` для internal identifiers;
- `MixedCaps` для идентификаторов, используемых из других packages;
- не совпадать с keywords;
- initialism: `productAPI`, не `productApi`.

### Types: short map

| Category | Chapter examples |
|---|---|
| integers | `int`, `int8`…`int64`, `uint`, `uint8`… |
| float | `float32`, `float64` |
| complex | `complex64`, `complex128` |
| character aliases | `byte` = `uint8`; `rune` = `int32` |
| text | `string` |
| logic | `bool` |
| aggregate | arrays, structs |
| reference | slices, maps, channels, pointers, functions, methods |
| interface | interface |

### Array vs slice

| Property | Array | Slice |
|---|---|---|
| length | fixed | variable |
| assignment | copies array | shares underlying data |
| structure | elements | ptr + len + cap |
| independent copy | normal assignment | allocate + `copy` |

### UTF-8

~~~text
string = bytes
byte index != Unicode character index
range string → byte offset + rune
[]rune(string) → work by Unicode code points
~~~

### Map

~~~go
m := map[string]int{"a": 1}
m["b"] = 2
v := m["a"]
delete(m, "a")
v, ok := m["b"]
~~~

### Pointer

~~~go
value := 4
p := &value
fmt.Println(*p)
*p = 20
~~~

`nil` — zero value pointer.

### Constants

~~~go
const max = 30

const (
    None = iota
    January
    February
)
~~~

### Operators

Chapter categories:
- arithmetic;
- comparison;
- logical;
- bitwise;
- assignment;
- unary;
- address/dereference operators.

Precedence from high to low:
1. `* / % << >> & &^`
2. `+ - | ^`
3. `== != < <= > >=`
4. `&&`
5. `||`

Parentheses override precedence.

### if

~~~go
if condition {
    ...
} else {
    ...
}
~~~

`else` is optional.

### switch

~~~go
switch value {
case a:
    ...
case b, c:
    ...
default:
    ...
}
~~~

`default` is optional. `fallthrough` executes the following case body when explicitly used.

### for

Go uses one loop keyword:

~~~go
for init; condition; post { ... }
for condition { ... }
for { ... }
for i, v := range collection { ... }
~~~

- `break` — leave loop;
- `continue` — next iteration.

### goto

~~~go
goto label
label:
    ...
~~~

Source warning: avoid it because it obscures sequential logic and can create unintended infinite loops.

### Numeric conversions

~~~go
var a int = 5
var b float32 = 5.32

float32(a)
int(b)
~~~

Narrowing may lose data.

### String ↔ int

~~~go
s := strconv.Itoa(33)
n, err := strconv.Atoi(s)
~~~

### Formatted output

Integers:
`%b %c %d %o %O %x %X %U`

Floats:
`%b %e %E %f %F %x %X`

Strings / bytes:
`%s %q %x %X`

Generic:
`%v %+v %T`

Pointer:
`%p`

Bool:
`%t`

## Standard-library helpers introduced

### strings

Examples shown:
- `TrimSpace`, `Trim`, `TrimLeft`, `TrimRight`;
- `TrimPrefix`, `TrimSuffix`;
- `ToUpper`, `ToLower`, `ToTitle`;
- `Split`, `SplitAfter`, `SplitN`;
- `Fields`, `FieldsFunc`;
- `strings.Builder`.

### slices

Examples shown:
- `All`, `Backward`, `Chunk`;
- `Insert`, `Clone`, `Concat`;
- `Delete`, `DeleteFunc`, `Repeat`, `Replace`, `Reverse`;
- `Sort`, `SortFunc`, `IsSorted`;
- `BinarySearch`, `Index`, `Contains`, `Compare`, `Equal`;
- `Compact`, `Max`, `Min`.

### maps

Examples shown:
- `Clone`;
- `Copy`;
- `DeleteFunc`;
- `Equal`;
- `Keys`;
- `Values`.

## Next action

После усвоения главы:
1. собрать минимальный module;
2. повторить основные types/collections/control flow;
3. пройти вопросы для самопроверки;
4. реализовать или разобрать tic-tac-toe v.0;
5. выполнить два задания на доработку.

## Modifying action

### Инициализация модуля

~~~bash
go mod init hello-go
~~~

Effect:
- создаётся `go.mod`.

Risk:
- меняет содержимое project directory.

Verification:
- `go.mod` существует и содержит module declaration.

Rollback:
- [Needs confirmation] — глава не задаёт rollback procedure.

### Запуск кода

~~~bash
go run main.go
~~~

Type:
- workload-generating.

Effect:
- компилирует/запускает приложение для текущего source.

Verification:
- в Hello World example ожидается `Hello World!`.

Rollback:
- [Not applicable] для сохранённого состояния проекта; способ остановки процесса в главе отдельно не описан.

## Verification / acceptance checks

После главы читатель должен уметь объяснить:

- почему `string` и `rune` нельзя считать одним и тем же;
- чем array отличается от slice;
- почему присваивание slice не создаёт независимую копию;
- как map хранит key/value pairs и как проверить наличие ключа;
- как получить и разыменовать pointer;
- что делает `iota`;
- как строятся `if`, `switch`, `for`;
- зачем нужны `break`, `continue`, `range`;
- почему conversions явные и где возникает overflow/data loss;
- какие formatting verbs использовать с integer/float/string;
- как материал главы собирается в tic-tac-toe v.0.

## Rollback

Для language-learning examples rollback обычно означает вернуть исходный код вручную.

Для `go mod init` точная процедура rollback в главе не приводится: `[Needs confirmation]`.

Для project modifications глава предлагает итеративное развитие, но не описывает VCS/commit rollback workflow: `[Needs confirmation]`.
