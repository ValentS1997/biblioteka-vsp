# Шпаргалка — глава 4: ошибки и panic

## Fast model

~~~text
error
→ returned value
→ caller checks err != nil
→ program can continue

panic
→ exceptional runtime stop path
→ defer still runs if registered
→ recover can intercept in deferred function
~~~

Scope: PDF 199–212.

## Symptom / action map

| Symptom / need | Source-grounded mechanism |
|---|---|
| invalid slice index | runtime panic + stack trace |
| nil pointer use | runtime panic |
| explicitly abort on invalid state | `panic(v)` |
| cleanup even during panic | `defer` before panic point |
| intercept panic | `recover()` in deferred function |
| operation can fail normally | return `(value, error)` |
| create simple error | `errors.New` / `fmt.Errorf` |
| identify known error | `errors.Is` |
| need structured error details | custom type + `Error() string` + `errors.As` |
| add context but keep cause | `%w` in `fmt.Errorf` |
| inspect wrapped cause | `errors.Unwrap` |

## Runtime panic

Chapter examples:

~~~text
slice[index outside length]
→ panic: index out of range

nil pointer method/field access
→ panic: invalid memory address / nil pointer dereference
~~~

Stack trace helps locate failure point.

## User panic

~~~go
panic("detailed reason")
~~~

Built-in signature shown in source: `panic(v any)`.

## `defer` + panic

Correct ordering from chapter:

~~~go
defer cleanup()
panic("failure")
~~~

Not useful:

~~~go
panic("failure")
defer cleanup() // never registered
~~~

## `recover`

~~~go
defer func() {
    if err := recover(); err != nil {
        // panic observed here
    }
}()
~~~

Chapter demonstrates repeated/nested recovery levels.

## Normal error handling

~~~go
value, err := strconv.Atoi(str)
if err != nil {
    // handle
}
~~~

## Create errors

~~~go
err1 := errors.New("first error")
err2 := fmt.Errorf("second error")
~~~

## Function returning `error`

~~~go
func div(a, b int) (int, error) {
    if b == 0 {
        return 0, fmt.Errorf("cannot divide by zero")
    }
    return a / b, nil
}
~~~

## Named package-level errors

~~~go
var ErrDivByZero = errors.New("divide by zero")
var ErrDivByOne  = errors.New("divide by one")
~~~

Chapter naming convention: `Err...`.

## Identify with `errors.Is`

~~~go
switch {
case errors.Is(err, ErrDivByZero):
    ...
case errors.Is(err, ErrDivByOne):
    ...
}
~~~

## Structured custom error

~~~go
type DivError struct {
    Numerator   int
    Denominator int
    Msg         string
}

func (d *DivError) Error() string {
    return d.Msg
}
~~~

## Extract with `errors.As`

~~~go
var divErr *DivError
if errors.As(err, &divErr) {
    fmt.Println(divErr.Numerator)
}
~~~

## Wrap error

~~~go
return fmt.Errorf("DataBase error: %w", err)
~~~

Purpose:

~~~text
low-level cause
+ higher-level context
→ wrapped error chain
~~~

## Unwrap

~~~go
cause := errors.Unwrap(err)
~~~

## Interpretation / acceptance

После главы читатель должен уметь объяснить:
- difference `error` vs `panic`;
- common panic causes from source;
- `panic`, `defer`, `recover` relationship;
- standard `(value, error)` pattern;
- `errors.New` vs `fmt.Errorf` use in chapter;
- package-level `Err...` values;
- `errors.Is`;
- custom error implementing `Error() string`;
- `errors.As`;
- wrapping through `%w`;
- `errors.Unwrap`.

## Rollback

Глава не описывает shell/system state changes и VCS rollback. Большинство examples изменяют только in-memory execution path/source code. Rollback procedure: `[Not applicable]` / `[Needs confirmation]` для source edits.
