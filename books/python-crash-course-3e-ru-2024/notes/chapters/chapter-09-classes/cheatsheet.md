# Шпаргалка главы 9 — Классы

## Symptom / problem framing

Типовые вопросы:

- где хранить состояние объекта;
- почему method не видит attribute;
- как изменить attribute контролируемо;
- когда использовать inheritance;
- когда вынести часть объекта в отдельный class;
- как организовать классы по modules;
- почему `import *` нежелателен.

## Baseline

~~~python
class Dog:
    def __init__(self, name, age):
        self.name = name
        self.age = age

    def sit(self):
        print(f"{self.name} is now sitting.")

my_dog = Dog('Willie', 6)
~~~

- `Dog` — class.
- `my_dog` — instance.
- `name`, `age` — attributes.
- `sit()` — method.
- `self` — ссылка на конкретный instance.

## Read-only checks

~~~python
print(my_dog.name)
print(my_dog.age)
my_dog.sit()
~~~

Dot notation применяется и к attributes, и к methods.

## Mutation patterns

### Direct

~~~python
my_new_car.odometer_reading = 23
~~~

### Through method

~~~python
my_new_car.update_odometer(23)
~~~

### Increment

~~~python
my_used_car.increment_odometer(100)
~~~

Source advantage method-based mutation: можно добавить validation.

## Inheritance

~~~python
class ElectricCar(Car):
    def __init__(self, make, model, year):
        super().__init__(make, model, year)
~~~

Child получает parent attributes/methods и может добавлять/override собственные.

## Composition

~~~python
class ElectricCar(Car):
    def __init__(self, make, model, year):
        super().__init__(make, model, year)
        self.battery = Battery()
~~~

Вызов:

~~~python
my_leaf.battery.describe_battery()
~~~

## Next action

1. Определить responsibility класса.
2. Сформулировать attributes.
3. Сформулировать methods.
4. Решить, какие mutations должны проходить через методы.
5. Для specialization — проверить inheritance.
6. Для отдельной составной части — проверить composition.
7. При росте файла — вынести классы в modules.
8. Проверить создание минимум одного instance и ключевые методы.

## Verification / acceptance checks

- `__init__()` получает нужные параметры;
- `self.attribute` доступен последующим methods;
- два instances имеют независимое состояние;
- mutation method изменяет только ожидаемый attribute;
- validation отклоняет недопустимое изменение;
- child instance использует parent methods;
- overridden method действительно заменяет parent behavior;
- composed object доступен через attribute;
- imported class создаётся из отдельного module.

## Rollback

- read-only attribute/method calls: `[Not applicable]`.
- direct/method mutation: отдельный универсальный rollback в source не задан — `[Needs confirmation]`.
- для odometer source показывает preventive validation вместо rollback.
- module/file restructuring: rollback procedure `[Needs confirmation]`.

## Security boundary

Source прямо предупреждает: проверка внутри `update_odometer()` не является полной защитой, потому что пользователь с доступом к program code может присвоить attribute напрямую.
