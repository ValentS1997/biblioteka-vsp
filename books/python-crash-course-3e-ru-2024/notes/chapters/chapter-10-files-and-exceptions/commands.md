# Операции главы 10

Только source-confirmed элементы из `e0019:c01–c15`.

## Path

~~~python
from pathlib import Path
path = Path('pi_digits.txt')
~~~

Тип: object creation / path reference.

## read_text()

~~~python
contents = path.read_text()
~~~

Тип: read-only file I/O.

Effect: source описывает возврат содержимого файла одной строкой.

Potential failure shown in chapter: `FileNotFoundError`.

## read_text(encoding='utf-8')

~~~python
contents = path.read_text(encoding='utf-8')
~~~

Source use: чтение файла, encoding которого может отличаться от system default.

## rstrip() / strip() / splitlines()

~~~python
contents = path.read_text().rstrip()
lines = contents.splitlines()
~~~

Тип: read-only string transformation.

## write_text()

~~~python
path.write_text(contents)
~~~

Тип: persistent state-changing.

Effect:
- creates target if absent;
- overwrites current contents if target exists.

Risk: destructive overwrite.

Verification:

~~~python
print(path.read_text())
~~~

Rollback: `[Needs confirmation]`.

## try / except / else

~~~python
try:
    answer = int(first_number) / int(second_number)
except ZeroDivisionError:
    print("You can't divide by 0!")
else:
    print(answer)
~~~

Тип: control flow / error handling.

Source rule: `try` должен содержать только code capable of raising the exception being handled.

## pass

~~~python
except FileNotFoundError:
    pass
~~~

Тип: explicit no-op.

Effect: exception handled silently and execution continues.

Risk: user may not know expected input/resource was skipped.

## Text analysis

~~~python
words = contents.split()
num_words = len(words)
~~~

Source describes result as approximate word count.

## JSON serialize

~~~python
import json
contents = json.dumps(numbers)
path.write_text(contents)
~~~

Тип: transformation + persistent write.

Note: source prose and shown call signature conflict; see `source-findings.md`.

## JSON deserialize

~~~python
contents = path.read_text()
numbers = json.loads(contents)
~~~

Тип: read-only file I/O + transformation.

## exists()

~~~python
if path.exists():
    ...
~~~

Source: returns `True` if file/folder exists, otherwise `False`.

## Refactoring pattern

Source final separation:

- `get_stored_username(path)` → load or `None`;
- `get_new_username(path)` → input + persist + return;
- `greet_user()` → orchestration.

## Operational classification

| Operation | State |
|---|---|
| `Path(...)` | no persistent change |
| `read_text()` | read-only |
| string methods | read-only |
| `exists()` | read-only |
| `write_text()` | persistent write / overwrite |
| `json.dumps()` | in-memory transformation |
| `json.loads()` | in-memory transformation |
| `pass` | no-op after handled exception |
