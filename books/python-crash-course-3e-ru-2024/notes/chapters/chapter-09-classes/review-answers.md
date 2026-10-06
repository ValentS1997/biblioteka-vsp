# Разбор упражнений главы 9

Это RAG-grounded решения/шаблоны, не официальный ключ издателя. Персональные/внешние данные не выдумываются.

## 9.1. Ресторан

~~~python
class Restaurant:
    def __init__(self, restaurant_name, cuisine_type):
        self.restaurant_name = restaurant_name
        self.cuisine_type = cuisine_type

    def describe_restaurant(self):
        print(self.restaurant_name)
        print(self.cuisine_type)

    def open_restaurant(self):
        print("Ресторан открыт.")

restaurant = Restaurant('[название]', '[кухня]')
print(restaurant.restaurant_name)
print(restaurant.cuisine_type)
restaurant.describe_restaurant()
restaurant.open_restaurant()
~~~

Название/кухня: `[Needs confirmation]`.

## 9.2. Три ресторана

Конкретные рестораны: `[Needs confirmation]`.

~~~python
restaurants = [
    Restaurant('[r1]', '[c1]'),
    Restaurant('[r2]', '[c2]'),
    Restaurant('[r3]', '[c3]'),
]

for restaurant in restaurants:
    restaurant.describe_restaurant()
~~~

## 9.3. Пользователи

Дополнительные profile attributes и реальные пользователи: `[Needs confirmation]`.

~~~python
class User:
    def __init__(self, first_name, last_name):
        self.first_name = first_name
        self.last_name = last_name

    def describe_user(self):
        print(self.first_name, self.last_name)

    def greet_user(self):
        print(f"Hello, {self.first_name}!")
~~~

## 9.4. Посетители

~~~python
class Restaurant:
    def __init__(self, restaurant_name, cuisine_type):
        self.restaurant_name = restaurant_name
        self.cuisine_type = cuisine_type
        self.number_served = 0

    def set_number_served(self, number):
        self.number_served = number

    def increment_number_served(self, number):
        self.number_served += number
~~~

Acceptance: проверить initial 0, direct change, setter-like method и increment.

## 9.5. Попытки входа

~~~python
class User:
    def __init__(self, first_name, last_name):
        self.first_name = first_name
        self.last_name = last_name
        self.login_attempts = 0

    def increment_login_attempts(self):
        self.login_attempts += 1

    def reset_login_attempts(self):
        self.login_attempts = 0
~~~

## 9.6. Киоск с мороженым

Flavours: `[Needs confirmation]`.

~~~python
class IceCreamStand(Restaurant):
    def __init__(self, restaurant_name, cuisine_type, flavors):
        super().__init__(restaurant_name, cuisine_type)
        self.flavors = flavors

    def show_flavors(self):
        for flavor in self.flavors:
            print(flavor)
~~~

## 9.7. Администратор

Конкретный список privileges можно взять из формулировки упражнения или заменить своими source-compatible строками.

~~~python
class Admin(User):
    def __init__(self, first_name, last_name):
        super().__init__(first_name, last_name)
        self.privileges = [
            'разрешено добавлять сообщения',
            'разрешено удалять пользователей',
            'разрешено банить пользователей',
        ]

    def show_privileges(self):
        for privilege in self.privileges:
            print(privilege)
~~~

## 9.8. Привилегии

~~~python
class Privileges:
    def __init__(self):
        self.privileges = [
            'разрешено добавлять сообщения',
            'разрешено удалять пользователей',
            'разрешено банить пользователей',
        ]

    def show_privileges(self):
        for privilege in self.privileges:
            print(privilege)


class Admin(User):
    def __init__(self, first_name, last_name):
        super().__init__(first_name, last_name)
        self.privileges = Privileges()
~~~

Вызов:

~~~python
admin.privileges.show_privileges()
~~~

## 9.9. Обновление аккумулятора

Source default battery size: 40; upgrade target: 65.

~~~python
class Battery:
    def __init__(self, battery_size=40):
        self.battery_size = battery_size

    def upgrade_battery(self):
        if self.battery_size != 65:
            self.battery_size = 65
~~~

Acceptance: вызвать source `get_range()` до и после upgrade и проверить увеличение range.

## 9.10. Импортирование класса Restaurant

`restaurant.py` содержит class `Restaurant`.

Основной file:

~~~python
from restaurant import Restaurant

restaurant = Restaurant('[название]', '[кухня]')
restaurant.describe_restaurant()
~~~

Значения: `[Needs confirmation]`.

## 9.11. Импортирование класса Admin

Module layout source-required:

~~~python
from users import Admin

admin = Admin('[имя]', '[фамилия]')
admin.privileges.show_privileges()
~~~

Точные module names в упражнении не заданы: `[Needs confirmation]`.

## 9.12. Множественные модули

Один source-consistent layout:
- `user.py` → `User`;
- `admin.py` → `Privileges`, `Admin`, плюс import `User`;
- main file → import `Admin`.

Точные filenames: `[Needs confirmation]`.

## 9.13. Игра в кости

~~~python
from random import randint

class Die:
    def __init__(self, sides=6):
        self.sides = sides

    def roll_die(self):
        print(randint(1, self.sides))
~~~

Создать instances для 6, 10, 20 и вызвать `roll_die()` по 10 раз.

## 9.14. Лотерея

Конкретные 10 numbers/5 letters: `[Needs confirmation]`.

Source-supported primitive:

~~~python
from random import choice

pool = ['[15 элементов]']
winning = []

while len(winning) < 4:
    winning.append(choice(pool))

print(winning)
~~~

Source не уточняет в упражнении, должны ли выбранные элементы быть уникальными: `[Needs confirmation]`.

## 9.15. Анализ лотереи

Конкретная модель ticket/combination зависит от 9.14: `[Needs confirmation]`.

Source requirement:
- создать `my_ticket`;
- генерировать combinations в цикле;
- остановиться при совпадении;
- вывести iteration count.

Важно: такая программа потенциально может выполнять много итераций; точное количество заранее неизвестно.

## 9.16. Модуль недели

Требует внешнего сайта `http://pymotw.com/` либо внешней документации.

В режиме `rag_only`: `[Needs confirmation]`.

Source альтернативно предлагает изучить документацию module `random`, но внешняя документация также не загружалась.
