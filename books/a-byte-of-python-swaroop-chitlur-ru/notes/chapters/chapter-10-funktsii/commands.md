# Commands and code — глава 10 «Функции»

## Execution commands

| Command | Classification | Source role | Verification | Rollback |
|---|---|---|---|---|
| `python function1.py` | workload-generating | basic define/call example | greeting twice | [Not applicable] |
| `python func_param.py` | workload-generating | parameters/arguments | 4 then 7 as maxima | [Not applicable] |
| `python func_local.py` | workload-generating | local scope | outer x remains 50 | [Not applicable] |
| `python func_global.py` | workload-generating | global assignment | final x = 2 | [Not applicable] |
| `python func_nonlocal.py` | workload-generating | enclosing-scope assignment | enclosing x = 5 | [Not applicable] |
| `python func_default.py` | workload-generating / source-integrity caveat | default arguments | source shows two output lines | [Not applicable] |
| `python func_key.py` | workload-generating | keyword arguments | three source output lines | [Not applicable] |
| `python total.py` | workload-generating | variable argument count | `166` | [Not applicable] |
| `python keyword_only.py` | workload-generating / negative test | required keyword-only argument | 66 then source `TypeError` | [Not applicable] |
| `python func_return.py` | workload-generating | return value | `3` | [Not applicable] |
| `python func_doc.py` | workload-generating | docstring / `__doc__` | maximum + docstring | [Not applicable] |

Source uses executable name `python`; do not silently normalize to `python3`.

## Function definition / call

```python
def sayHello():
    print('Привет, Мир!')

sayHello()
sayHello()
```

## Parameters vs arguments

```python
def printMax(a, b):
    ...

printMax(3, 4)

x = 5
y = 7
printMax(x, y)
```

## Scope

Local:

```python
x = 50

def func(x):
    x = 2
```

Global:

```python
global x
x = 2
```

Nonlocal:

```python
def func_outer():
    x = 2

    def func_inner():
        nonlocal x
        x = 5
```

## Default arguments — source-integrity caveat

RAG source variant:

```python
def say(message, times = 1):
    print(message * times)

    say('Привет')
    say('Мир', 5)
```

The displayed calls are indented in the RAG/source variant, while the shown output is
presented as a normal two-call example. Do not silently dedent the canonical source
variant. See `source-findings.md`.

Source also states:

```python
def func(a, b=5)
```

is allowed, while:

```python
def func(a=5, b)
```

is not.

## Keyword arguments

```python
def func(a, b=5, c=10):
    ...

func(3, 7)
func(25, c=24)
func(c=50, a=100)
```

## Variable number of arguments

```python
def total(initial=5, *numbers, **keywords):
    ...
```

Source output for:

```python
total(10, 1, 2, 3, vegetables=50, fruits=100)
```

is `166`.

## Keyword-only parameters

```python
def total(initial=5, *numbers, extra_number):
    ...
```

Source also shows the unnamed-star form:

```python
def total(initial=5, *, extra_number):
    ...
```

The second call in `keyword_only.py` intentionally omits `extra_number` and produces
a source `TypeError`.

## return / pass

```python
def maximum(x, y):
    if x > y:
        return x
    elif x == y:
        return 'Числа равны.'
    else:
        return y
```

Empty body example:

```python
def someFunction():
    pass
```

Source teaching statement: a bare `return` is equivalent to `return None`, and a
function without explicit `return` has an implicit `return None` at the end.

## Docstrings / help

```python
print(printMax.__doc__)
help(printMax)
```

Source notes that `q` exits help.

The command/tool name `pydoc` is mentioned as analogous to `help()`, but the chapter
does not provide a concrete CLI invocation. Do not synthesize one.
