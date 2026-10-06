# Глава 14. Объектно-ориентированное программирование

Status: `RAG_GROUNDED`

Book: `a-byte-of-python-swaroop-chitlur-ru`

## Scope

Глава 14 — «Объектно-ориентированное программирование». Она переходит от
procedural style к организации данных и поведения внутри объектов: вводит классы,
экземпляры, `self`, методы, `__init__`, переменные класса/объекта, наследование,
полиморфизм и кратко касается метаклассов/абстрактных базовых классов.

Разделы, подтверждённые RAG:

- вводная часть: классы, объекты, поля, методы и атрибуты
- 14.1 `self`
- 14.2 Классы
- 14.3 Методы объектов
- 14.4 Метод `__init__`
- 14.5 Переменные класса и объекта
- 14.6 Наследование
- 14.7 Метаклассы
- 14.8 Резюме

## Provenance

- source format: PDF
- source SHA-256: `ac1abb7761fccb914988a583b4362c1760bafc3489c34f3f1fdb4ba45a0d7db5`
- RAG chunks: `p0109:c01` — `p0120:c01`
- PDF pages: 109–120
- printed pages visible in chapter: 101–112
- chapter start: PDF page 109, heading «Объектно-ориентированное программирование»
- chapter end: PDF page 120, section 14.8 «Резюме»
- next chapter boundary: PDF page 121 begins «Ввод-вывод»
- boundary verified: yes

## Main principle

Source OOP model:

- class creates a new type;
- object is an instance of a class;
- fields hold data;
- methods hold behavior;
- `self` identifies the current instance;
- inheritance reuses common behavior through a base class;
- subtype objects can be used in places expecting the parent type in the source
  explanation of polymorphism.

## Chapter map

| Section | Source-grounded concept |
|---|---|
| Intro | Procedural vs object-oriented organization; classes, objects, fields, methods, attributes. |
| 14.1 | `self` is the conventional first method parameter and is supplied by Python at method call. |
| 14.2 | Minimal class with `class Person:` + `pass`; instantiate with `Person()`. |
| 14.3 | Object methods: `p.sayHi()`; method definition still contains `self`. |
| 14.4 | `__init__` initializes object state; example stores `self.name`. |
| 14.5 | Class variables are shared in source model; object variables belong to individual instances; `staticmethod`, docstrings and `__del__` are shown. |
| 14.6 | Inheritance, base/derived classes, overriding `tell`, explicit base method calls, polymorphism, multiple inheritance mention. |
| 14.7 | Metaclasses and ABC: `ABCMeta`, `@abstractmethod`, abstract base class example. |
| 14.8 | OOP terminology and advantages/pitfalls summarized before moving to I/O. |

## Core examples

### Minimal class

```python
class Person:
    pass

p = Person()
print(p)
```

### Method

```python
class Person:
    def sayHi(self):
        print('Привет! Как дела?')

p = Person()
p.sayHi()
```

### Initialization

```python
class Person:
    def __init__(self, name):
        self.name = name

    def sayHi(self):
        print('Привет! Меня зовут', self.name)
```

### Class/object state

```python
class Robot:
    population = 0

    def __init__(self, name):
        self.name = name
        Robot.population += 1
```

### Inheritance

```python
class Teacher(SchoolMember):
    def __init__(self, name, age, salary):
        SchoolMember.__init__(self, name, age)
        self.salary = salary
```

### Abstract base class

```python
from abc import *

class SchoolMember(metaclass=ABCMeta):
    @abstractmethod
    def tell(self):
        ...
```

## Operational acceptance

После главы читатель должен уметь:

- объяснить class vs object/instance;
- использовать `self` в method definition;
- создать class и instance;
- использовать `__init__` для instance fields;
- различать class variable и object variable на source example;
- объяснить `staticmethod` и dotted attribute access;
- построить base/subclass relation и override method;
- объяснить source meaning polymorphism;
- распознать `ABCMeta` / `@abstractmethod` как abstract-base-class mechanism.

## Safety / integrity boundary

- Все examples — учебные runtime operations; системную конфигурацию они не меняют.
- `del droid1` / `del droid2` меняют runtime bindings и в source example
  используются для наблюдения `__del__`.
- Сохранение `.py` example files меняет filesystem state; rollback source не задан.
- Exact object representation/address in `simplestclass.py` is variable; source itself
  warns that memory address differs.
- Statements about `__del__` timing, privacy/public/virtual behavior and base-class
  constructor calls are preserved as historical source claims, not externally verified
  current-language rules.

## Conditional artifacts

Раздел 14.8 — явное chapter-end «Резюме», поэтому создан `summary.md`.

Review/control questions в границе главы отсутствуют, поэтому
`review-questions.md` и `review-answers.md` не создаются.
