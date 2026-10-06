# Конструкции и операции главы 9

Только source-confirmed элементы из `e0018:c01–c15`.

## Class definition

~~~python
class Dog:
    """Простая модель собаки."""

    def __init__(self, name, age):
        self.name = name
        self.age = age
~~~

Source naming:
- class names: CamelCase;
- instance/module names: lowercase_with_underscores.

## Instance creation

~~~python
my_dog = Dog('Willie', 6)
~~~

Классификация: state-producing.

Effect: Python вызывает `__init__()` и создаёт отдельный instance.

## Attribute access

~~~python
my_dog.name
my_dog.age
~~~

Классификация: read-only access.

## Method call

~~~python
my_dog.sit()
~~~

Классификация: workload-generating/state-changing в зависимости от тела метода.

## Default instance attribute

~~~python
self.odometer_reading = 0
~~~

Attribute создаётся в `__init__()` без отдельного argument.

## Direct mutation

~~~python
my_new_car.odometer_reading = 23
~~~

Классификация: state-changing.

## Controlled mutation

~~~python
def update_odometer(self, mileage):
    if mileage >= self.odometer_reading:
        self.odometer_reading = mileage
    else:
        print("You can't roll back an odometer!")
~~~

Source purpose: отклонить уменьшение показаний.

## Increment mutation

~~~python
def increment_odometer(self, miles):
    self.odometer_reading += miles
~~~

Source note: метод можно дополнительно расширить проверкой отрицательного increment.

## Inheritance

~~~python
class ElectricCar(Car):
    def __init__(self, make, model, year):
        super().__init__(make, model, year)
~~~

`super()` вызывает parent method.

## Override

~~~python
class ElectricCar(Car):
    def fill_gas_tank(self):
        print("This car doesn't have a gas tank!")
~~~

При вызове child method Python использует child definition вместо parent method.

## Composition

~~~python
class Battery:
    ...

class ElectricCar(Car):
    def __init__(self, make, model, year):
        super().__init__(make, model, year)
        self.battery = Battery()
~~~

Доступ:

~~~python
my_leaf.battery.describe_battery()
~~~

## Import classes

~~~python
from car import Car
~~~

~~~python
from car import Car, ElectricCar
~~~

~~~python
import car
my_leaf = car.ElectricCar(...)
~~~

Module-to-module dependency:

~~~python
from car import Car
~~~

Alias:

~~~python
from electric_car import ElectricCar as EC
import electric_car as ec
~~~

## Import all classes

~~~python
from module_name import *
~~~

Source explicitly does not recommend this because:
- imports no longer show which classes are used;
- name collisions can create difficult errors.

## Standard library random

~~~python
from random import randint
randint(1, 6)
~~~

Source: returns integer within provided inclusive range.

~~~python
from random import choice
choice(players)
~~~

Source: returns random element from list/tuple.

Security note: source says `random` should not be used for security-related applications.

## Formatting classes

Source rules:
- class names: CamelCase;
- instance/module names: lowercase + underscores;
- class/module docstrings;
- one blank line between methods;
- two blank lines between classes in a module;
- standard-library imports first, then blank line, then user-written module imports.
