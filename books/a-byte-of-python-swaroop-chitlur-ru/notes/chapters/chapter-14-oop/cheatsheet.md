# Chapter 14 cheatsheet — «Объектно-ориентированное программирование»

## Symptom / problem framing

Нужно организовать данные и поведение как связанные сущности и переиспользовать
общую функциональность между типами.

## Baseline / context

Source hierarchy:

`class → instance/object → fields + methods → inheritance → polymorphism`

Core access form:

`object.attribute`

## Read-only checks

При ревью OOP example проверить:

1. Class объявлен через `class Name:`.
2. Instance methods имеют первым parameter `self`.
3. Instance state хранится через `self.name`-style fields.
4. Class state accessed through class name in source example.
5. Override method в subclass действительно заменяет inherited lookup path.
6. Base initialization/method calls записаны так, как показано source.
7. Abstract method marked `@abstractmethod`, если используется ABC example.
8. Не полагаться на конкретный object memory address из printed representation.

## Interpretation

- `Person()` creates instance in source example.
- `p.sayHi()` conceptually maps to class method call with instance supplied as `self`.
- `__init__` receives constructor arguments passed after class name.
- `self.name` and local `name` are distinct names in source explanation.
- `Robot.population` is shared class-level state in the example.
- `self.name` is per-instance state.
- `staticmethod` is used when method does not need class identity in source example.
- Subclasses `Teacher` / `Student` reuse `SchoolMember` and override `tell`.
- Source describes this substitutability as polymorphism.
- `ABCMeta` + `@abstractmethod` are used to prevent direct instantiation of the
  abstract base class in the example.

## Next action

Следующая глава — «Ввод-вывод»: user input/output, files and serialization.

## Modifying action

### Runtime class variable

```python
Robot.population += 1
Robot.population -= 1
```

Effect: mutates class-level runtime state.

Verification: `Robot.howMany()`.

Rollback: process-local; generic source rollback not applicable.

### Runtime binding deletion

```python
del droid1
del droid2
```

Effect: removes runtime names; source uses this to demonstrate `__del__`.

Verification: source output shows population decreasing.

Rollback: object recreation would be required; source does not provide a generic rollback.

### File creation/edit

Source files include `simplestclass.py`, `method.py`, `class_init.py`,
`objvar.py`, `inherit.py`, `inherit_abc.py`.

Effect: filesystem changes.

Rollback: **[Needs confirmation]**.

## Verification / acceptance checks

- `simplestclass.py` prints a `Person` object representation.
- `method.py` prints greeting.
- `class_init.py` prints the instance name.
- `objvar.py` reaches population 2 and then 0 in shown run.
- `inherit.py` prints Teacher and Student-specific `tell` output.
- ABC example preserves subclass behavior while marking base `tell` abstract.

## Rollback

Runtime state ends with process. Filesystem rollback:
**[Needs confirmation]**.
