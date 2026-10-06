# Commands and code — глава 14 «Объектно-ориентированное программирование»

## Execution / inspection commands

| Command / snippet | Classification | Source role | Verification | Rollback |
|---|---|---|---|---|
| `help(int)` | read-only | inspect class `int` | help text | [Not applicable] |
| `python3 simplestclass.py` | workload-generating | minimal class/instance | object representation | [Not applicable] |
| `python3 method.py` | workload-generating | object method | greeting | [Not applicable] |
| `python3 class_init.py` | workload-generating | `__init__` and field | named greeting | [Not applicable] |
| `python3 objvar.py` | workload-generating / runtime mutation | class/object variables, `del`, `__del__` | population output | [Not applicable] |
| `python3 inherit.py` | workload-generating | inheritance/polymorphism | Teacher/Student output | [Not applicable] |
| `del droid1`, `del droid2` | state-changing runtime namespace | remove names in source example | source destructor output | recreate instances |
| `Robot.__doc__` | read-only | class docstring access | docstring value | [Not applicable] |
| `Robot.sayHi.__doc__` | read-only | method docstring access | docstring value | [Not applicable] |

The source names the abstract-base-class file `inherit_abc.py`, but the output block
that follows it shows `$ python3 inherit.py`. Do not synthesize or normalize a canonical
execution command for that file; see `source-findings.md`.

## self model

Source conceptual transformation:

```text
myobject.method(arg1, arg2)
→ MyClass.method(myobject, arg1, arg2)
```

## Minimal class

```python
class Person:
    pass

p = Person()
print(p)
```

Exact memory address in printed representation is not stable; source explicitly says it
will differ by run/system.

## Object method

```python
class Person:
    def sayHi(self):
        print('Привет! Как дела?')
```

## __init__

```python
class Person:
    def __init__(self, name):
        self.name = name
```

## Class / object variables

```python
class Robot:
    population = 0

    def __init__(self, name):
        self.name = name
        Robot.population += 1
```

Source static-method form:

```python
def howMany():
    print('У нас {0:d} роботов.'.format(Robot.population))

howMany = staticmethod(howMany)
```

Decorator form:

```python
@staticmethod
def howMany():
    ...
```

## Inheritance

```python
class Teacher(SchoolMember):
    def __init__(self, name, age, salary):
        SchoolMember.__init__(self, name, age)
        self.salary = salary

    def tell(self):
        SchoolMember.tell(self)
        ...
```

Source mentions multiple inheritance when more than one base class is listed.

## Abstract base class

```python
from abc import *

class SchoolMember(metaclass=ABCMeta):
    @abstractmethod
    def tell(self):
        ...
```

The direct-instantiation line is commented in source:

```python
#m = SchoolMember('abc', 10)
```

with a commented expected `TypeError`. Exact exception text is not promoted to a
current-runtime guarantee.

## Filesystem actions

Saving example scripts changes filesystem state. No editor/create/delete commands are
provided in the chapter.

Rollback: **[Needs confirmation]**.
