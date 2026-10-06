# Commands and code — глава 7 «Основы»

## Execution commands

| Command | Classification | Source role | Verification | Rollback |
|---|---|---|---|---|
| `python str_format.py` | workload-generating | запускает example 7.4.6 | сравнить с source output | [Not applicable] |
| `python3 program.py` | workload-generating / template | standard procedure source gives for future examples | program-specific output | [Not applicable] |
| `python var.py` | workload-generating | запускает example 7.8.1 | output `5`, `6`, multiline string | [Not applicable] |

Source uses both `python` and `python3`; do not silently normalize these command
variants. See `source-findings.md`.

## Python snippets — strings and format

```python
age = 26
name = 'Swaroop'

print('Возраст {0} -- {1} лет.'.format(name, age))
print('Почему {0} забавляется с этим Python?'.format(name))
```

Source also shows implicit positional placeholders:

```python
print('Возраст {} -- {} лет.'.format(name, age))
```

More detailed source examples:

```python
'{0:.3}'.format(1/3)
'{0:_^11}'.format('hello')
'{name} написал {book}'.format(name='Swaroop', book='A Byte of Python')
```

## Python snippets — variables

```python
i = 5
print(i)
i = i + 1
print(i)
```

Classification: workload-generating runtime code.

Expected source values: `5`, then `6`.

## Logical / physical lines

Source-equivalent forms include:

```python
i = 5
print(i)
```

```python
i = 5; print(i)
```

Source recommendation: prefer one logical line per physical line and normally avoid
semicolon.

Explicit continuation:

```python
s = 'Это строка. \
Это строка продолжается.'
print(s)
```

## Indentation failure example

The source intentionally demonstrates an extra leading space before `print`.

Expected error:

```text
IndentationError: unexpected indent
```

Classification: negative test / verification example.

## Other source-confirmed code references

ASCII encoding example:

```python
str.encode("ascii")
```

Source curiosity:

```python
from __future__ import braces
```

The chapter says to enter it «чтобы узнать больше», but does not provide the resulting
output in the RAG boundary. Do not invent the output.

## State-changing filesystem actions

Saving `str_format.py`, `var.py` or other examples changes filesystem state, but no
specific editor command or rollback procedure is provided.

Rollback: **[Needs confirmation]**.
