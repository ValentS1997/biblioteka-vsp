# Commands and code — глава 16 «Исключения»

## Execution / interaction commands

| Command / operation | Classification | Source role | Verification | Rollback |
|---|---|---|---|---|
| REPL `Print('Привет, Мир!')` | negative test | demonstrates traceback | source shows `NameError` | [Not applicable] |
| REPL `input(...)` + Ctrl-D | negative/interactive test | demonstrates EOF | source shows `EOFError` | [Not applicable] |
| `python3 try_except.py` | workload-generating / interactive | exception handlers + else | three source branches | [Not applicable] |
| `python3 raising.py` | workload-generating / interactive | custom exception + raise | short/normal input branches | [Not applicable] |
| `python3 finally.py` | workload-generating / file read | cleanup under Ctrl-C | cleanup message | [Not applicable] |
| `python3 using_with.py` | workload-generating / file read | context-manager file handling | same poem output | [Not applicable] |
| `raise ShortInputException(...)` | runtime control-flow change | explicit exception | matching handler | [Not applicable] |
| `f.close()` | runtime resource action | closes file handle | cleanup path completes | [Not applicable] |

## Error / exception examples

Source REPL:

```python
Print('Привет, Мир!')
```

Displayed traceback ends with:

```text
NameError: name 'Print' is not defined
```

The surrounding prose calls this a syntax error; this mismatch is preserved in
`source-findings.md`.

EOF example:

```python
s = input('Введите что-нибудь --> ')
```

with Ctrl-D produces source `EOFError`.

## try / except / else

```python
try:
    text = input('Введите что-нибудь --> ')
except EOFError:
    ...
except KeyboardInterrupt:
    ...
else:
    ...
```

## Custom exception / raise

```python
class ShortInputException(Exception):
    ...

raise ShortInputException(len(text), 3)
```

Source binds exception object:

```python
except ShortInputException as ex:
```

## try / finally

```python
try:
    f = open('poem.txt')
    ...
finally:
    f.close()
```

Dependency: `poem.txt` must exist for the intended source path.
Standalone existence: **[Needs confirmation]**.

## with

```python
with open("poem.txt") as f:
    for line in f:
        print(line, end='')
```

Source describes context-manager calls through `__enter__` and `__exit__`.

## Timing

```python
time.sleep(2)
```

Classification: workload delay; deliberately makes `finally.py` slow enough for
interactive Ctrl-C demonstration.

## Filesystem actions

Saving the four example scripts changes filesystem state. No source rollback commands
are supplied.

Rollback: **[Needs confirmation]**.
