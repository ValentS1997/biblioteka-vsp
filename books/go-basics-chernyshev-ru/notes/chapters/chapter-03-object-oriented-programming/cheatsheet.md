# Шпаргалка — глава 3: объектно-ориентированное программирование в Go

## Baseline

~~~text
state → struct
behavior → methods
boundary → package/export rules
reuse → composition
polymorphism → interfaces
type reuse → generics
~~~

Scope: PDF 153–198.

## Symptom / problem framing

| Problem | Source-grounded direction |
|---|---|
| нужно объединить related state | `struct` |
| method должен менять instance | pointer receiver |
| нельзя позволять caller напрямую ломать state | unexported fields + validated methods |
| нужен standard creation path | `New...` constructor function |
| нужно переиспользовать state/behavior | anonymous embedding / composition |
| несколько types имеют общий behavior | interface |
| concrete value спрятан в `interface{}` | type assertion / type switch |
| код повторяется только из-за type | generics |
| map key type parameter | `comparable` |

## Struct quick reference

~~~go
type Point struct {
    X int
    Y int
}

p := Point{X: 10, Y: 20}
pp := &p
pp.X = 42
~~~

Equality requires:
- same struct type;
- comparable fields.

## Value vs pointer receiver

~~~go
func (r RUB) Set(v RUB) {
    r = v // copy only
}

func (r *RUB) Set(v RUB) {
    *r = v // mutates caller instance
}
~~~

## Constructor function

~~~go
func NewShape(...) *Shape {
    return &Shape{...}
}
~~~

Source convention: `New` / `New<Type>`.

## Encapsulation / hiding

~~~text
package
├─ exported API: Uppercase
└─ internal details: lowercase
~~~

Goal in source: protect invariants, not merely hide fields.

## Composition

~~~go
type Rectangle struct {
    shape
    width  uint
    length uint
}
~~~

Embedded methods are promoted. Same-named outer method wins lookup before embedded method.

## Interface

~~~go
type IShape interface {
    GetArea() float64
    GetPerimeter() uint
}
~~~

No explicit `implements` declaration in chapter examples.

Useful positions:
- argument;
- return;
- variable;
- slice element;
- struct field.

## Interface slice

~~~text
Rectangle ┐
Triangle  ├─→ []IShape → one loop → common methods
...       ┘
~~~

## Interface field

~~~go
type Car struct {
    motor motor.IMotor
}
~~~

Concrete motor may be replaced as long as it conforms to interface.

## Type assertion

Risky:

~~~go
v := i.(SomeType)
~~~

Checked form:

~~~go
v, ok := i.(SomeType)
if ok {
    ...
}
~~~

## Type switch

~~~go
switch i.(type) {
case shape:
case car:
default:
}
~~~

## Generic function

~~~go
func Sum[T int | float64 | string](a, b T) T {
    return a + b
}
~~~

Named underlying types:

~~~go
func Sum[T ~int | float64 | string](a, b T) T
~~~

## Constraint interface

~~~go
type NumberLike interface {
    ~int | float64 | uint16 | uint32
}
~~~

## Generic collections

~~~go
func GetMapKeys[K comparable, V any](m map[K]V) []K
~~~

- `comparable` — required in chapter for map key parameter;
- `any` — any type.

## Project v.2 mapping

| Struct | Responsibility |
|---|---|
| `Board` | grid, moves, win/draw, output |
| `Player` | current symbol, switch player |
| `Game` | input, coordination, state machine, loop |

~~~text
main
→ NewBoard
→ NewPlayer
→ NewGame
→ Game.Play
   ├─ Board
   └─ Player
~~~

## Verification / acceptance checks

После главы читатель должен уметь:
- создать struct и pointer;
- объяснить exported/unexported field;
- выбрать value vs pointer receiver;
- написать constructor function;
- различить encapsulation/hiding по source framing;
- использовать composition;
- объявить и применить interface;
- безопасно выполнить type assertion;
- объяснить interface as field;
- написать generic function с constraint;
- объяснить `~`, `any`, `comparable`;
- разложить tic-tac-toe v.2 на Board/Player/Game.

## Rollback

Глава в основном посвящена code design и не задаёт VCS rollback workflow. Для изменений source code rollback остаётся `[Needs confirmation]` в рамках RAG-only policy.
