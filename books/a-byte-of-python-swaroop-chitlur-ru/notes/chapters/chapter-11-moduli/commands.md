# Commands and code — глава 11 «Модули»

## Execution / REPL commands

| Command / snippet | Classification | Source role | Verification | Rollback |
|---|---|---|---|---|
| `python3 using_sys.py we are arguments` | workload-generating | demonstrates `sys.argv` | argv entries printed | [Not applicable] |
| `import os; print(os.getcwd())` | read-only / workload | shows current working directory | path printed | [Not applicable] |
| `from sys import argv` | workload-generating import | binds `argv` directly | name accessible | [Not applicable] |
| `from sys import *` | workload-generating import | wildcard import | many names bound | [Not applicable] |
| `python3 using_name.py` | workload-generating | direct `__name__` mode | direct-run message | [Not applicable] |
| interactive `import using_name` | workload-generating import | imported `__name__` mode | import-message | [Not applicable] |
| `python mymodule_demo.py` | workload-generating | own module via dotted access | greeting + version 0.1 | [Not applicable] |
| `import this` | read-only/workload | displays Zen of Python in source instruction | text output | [Not applicable] |
| `dir(sys)` | read-only | lists module identifiers | list returned | [Not applicable] |
| `dir()` | read-only | lists current-module names | list returned | [Not applicable] |
| `del a` | state-changing (runtime namespace) | removes name `a` | `dir()` no longer contains `a` | recreate/reassign manually |
| `dir(str)` | read-only | lists class attributes | list returned | [Not applicable] |

## Basic import

```python
import sys

for i in sys.argv:
    print(i)

print(sys.path)
```

Source explanation: first import initializes module body; Python-written modules are
searched using `sys.path`.

## from ... import ...

```python
from sys import argv
```

Wildcard variant:

```python
from sys import *
```

Source recommendation: generally prefer plain `import` to reduce name conflicts and
improve readability.

## __name__

```python
if __name__ == '__main__':
    print('Эта программа запущена сама по себе.')
else:
    print('Меня импортировали в другой модуль.')
```

Direct run:

```text
python3 using_name.py
```

Imported run:

```text
python3
>>> import using_name
```

## Own module

`mymodule.py`:

```python
def sayhi():
    print('Привет! Это говорит мой модуль.')

__version__ = '0.1'
```

`mymodule_demo.py`:

```python
import mymodule

mymodule.sayhi()
print('Версия', mymodule.__version__)
```

Source command:

```text
python mymodule_demo.py
```

Alternative:

```python
from mymodule import sayhi, __version__
```

and source also shows:

```python
from mymodule import *
```

## dir / del

```python
import sys
dir(sys)
dir()
a = 5
dir()
del a
dir()
dir(str)
```

Source also prints `dir('print')` as an example; exact source wording describes it as
attributes of function `print`. See `source-findings.md`.

## Package structure

Source tree:

```text
<some sys.path directory>/
└── world/
    ├── __init__.py
    ├── asia/
    │   ├── __init__.py
    │   └── india/
    │       ├── __init__.py
    │       └── foo.py
    └── africa/
        ├── __init__.py
        └── madagascar/
            ├── __init__.py
            └── bar.py
```

No shell commands for creating this tree are provided. Do not synthesize `mkdir`,
`touch` or removal commands from model memory.

## Automatic filesystem side effect

Section 11.1 says imports may create byte-compiled `.pyc` files when the directory is
writable. This is source-grounded historical behavior; exact current cache layout is
**[Needs confirmation]**.
