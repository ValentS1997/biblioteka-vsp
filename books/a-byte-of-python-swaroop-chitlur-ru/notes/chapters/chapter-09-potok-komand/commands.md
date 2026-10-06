# Commands and code — глава 9 «Поток команд»

## Execution commands

| Command | Classification | Source role | Verification | Rollback |
|---|---|---|---|---|
| `python if.py` | workload-generating / interactive | запускает branching example | output зависит от введённого number | [Not applicable] |
| `python while.py` | workload-generating / interactive | повторяет guesses до success | завершает loop при correct guess | [Not applicable] |
| `python for.py` | workload-generating | iteration over `range(1, 5)` | 1,2,3,4 + loop else | [Not applicable] |
| `python break.py` | workload-generating / interactive | читает strings до sentinel `выход` | после sentinel печатает завершение | [Not applicable] |
| `python continue.py` | workload-generating / interactive | фильтрует short strings | short input → `Слишком мало` | [Not applicable] |

Source uses executable name `python`; do not silently rewrite these commands to
`python3`.

## if / elif / else

```python
if guess == number:
    ...
elif guess < number:
    ...
else:
    ...
```

Minimal source form:

```python
if True:
    print('Да, это верно.')
```

## while / else

```python
while running:
    ...
else:
    print('Цикл while закончен.')
```

Important source rule: loop-`else` is skipped if `break` terminates the loop.

## for / range / else

```python
for i in range(1, 5):
    print(i)
else:
    print('Цикл for закончен')
```

Source examples also mention:

```python
range(1, 5, 2)
list(range())
```

## break

```python
while True:
    s = input('Введите что-нибудь : ')
    if s == 'выход':
        break
```

Operational note: `while True` is intentionally unbounded until the sentinel branch
executes `break`.

## continue

```python
if len(s) < 3:
    print('Слишком мало')
    continue
```

Effect: rest of current loop block is skipped; execution resumes with next iteration.

## State-changing filesystem actions

Saving the five `.py` examples changes filesystem state. The chapter does not provide
editor commands or rollback procedure.

Rollback: **[Needs confirmation]**.
