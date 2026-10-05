# Команды и инструменты — глава 4

Source policy: `rag_only`.

## Shell commands

В RAG главы 4 отдельные shell/Go CLI commands не подтверждены. Поэтому здесь не добавляются `go run`, `go test`, Git или другие commands из внешнего знания.

## Built-in / standard-library mechanisms

| Mechanism | Type | Purpose in chapter |
|---|---|---|
| `panic(v)` | control-flow / failure | explicitly generate panic |
| `defer` | control-flow | schedule cleanup/handler before function exits |
| `recover()` | panic handling | intercept panic from deferred function |
| `errors.New(msg)` | error creation | simple error value |
| `fmt.Errorf(...)` | error creation/wrapping | formatted error; with `%w` wraps cause |
| `errors.Is(err, target)` | inspection | identify known/sentinel-like error |
| `errors.As(err, &target)` | inspection | extract compatible custom error type |
| `errors.Unwrap(err)` | inspection | retrieve one wrapped lower-level error |

## `panic`

~~~go
panic(fmt.Sprintf("%s too old!!!", p.name))
~~~

Effect:
- changes control flow into panic path;
- without recovery may terminate application.

Verification:
- runtime output contains panic information / stack trace.

## `defer`

~~~go
defer func() {
    fmt.Println("cleanup")
}()
~~~

Effect:
- deferred call runs when function exits, including panic path shown by source, if registered before panic.

## `recover`

~~~go
defer func() {
    if err := recover(); err != nil {
        ...
    }
}()
~~~

Effect:
- source example intercepts panic and allows normal completion.

Risk:
- handler may itself re-panic; source demonstrates higher-level recovery.

## `errors.New`

~~~go
var ErrDivByZero = errors.New("divide by zero")
~~~

Use:
- simple package-level known error.

## `fmt.Errorf`

Simple:

~~~go
fmt.Errorf("second error")
~~~

Wrapped:

~~~go
fmt.Errorf("DataBase error: %w", err)
~~~

The `%w` form is explicitly used for nested error chains.

## `errors.Is`

~~~go
errors.Is(err, ErrDivByZero)
~~~

Use:
- choose behavior for known error variants.

## `errors.As`

~~~go
var myDivError *DivError
errors.As(err, &myDivError)
~~~

Use:
- obtain structured custom error and read its fields.

## `errors.Unwrap`

~~~go
errors.Unwrap(err)
~~~

Use:
- access wrapped lower-level error in source example.

## Safety / operational boundary

No filesystem/network/system modification workflow is part of this chapter. The operational risk is application control flow: panic may terminate the process, while recovery changes whether execution continues.
