# Разбор упражнений главы 5

Это RAG-grounded решения/шаблоны, не официальный ключ издателя.

## 5.1. Проверка условий

Один допустимый набор, построенный только из конструкций главы:

~~~python
car = 'subaru'
age = 19
requested_toppings = ['mushrooms', 'onions', 'pineapple']

print(car == 'subaru')                 # True
print(car == 'audi')                   # False
print(car != 'bmw')                    # True
print(car.lower() == 'SUBARU'.lower()) # True
print(age >= 18)                       # True
print(age < 18)                        # False
print(age == 21)                       # False
print(age != 21)                       # True
print('mushrooms' in requested_toppings)   # True
print('pepperoni' in requested_toppings)   # False
~~~

Источник требует также выводить описание и прогноз перед каждой проверкой.

## 5.2. Больше проверок условий

Минимальный checklist:

~~~python
name = 'Alice'
age_0 = 22
age_1 = 18
items = ['a', 'b']

print(name == 'Alice')
print(name != 'Bob')
print(name.lower() == 'alice')

print(age_0 == 22)
print(age_0 != 21)
print(age_1 < 21)
print(age_0 >= 21)

print(age_0 >= 21 and age_1 >= 21)
print(age_0 >= 21 or age_1 >= 21)

print('a' in items)
print('z' not in items)
~~~

Для полного acceptance упражнения пользователь должен дополнить набор так, чтобы у каждого требуемого вида были True и False cases.

## 5.3. Цвета пришельцев 1

True case:

~~~python
alien_color = 'green'

if alien_color == 'green':
    print("Вы заработали 5 очков.")
~~~

False case:

~~~python
alien_color = 'red'

if alien_color == 'green':
    print("Вы заработали 5 очков.")
~~~

Во второй версии вывода нет.

## 5.4. Цвета пришельцев 2

~~~python
alien_color = 'green'

if alien_color == 'green':
    print("Вы заработали 5 очков.")
else:
    print("Вы заработали 10 очков.")
~~~

Для проверки `else` заменить цвет на другое допустимое значение упражнения.

## 5.5. Цвета пришельцев 3

~~~python
alien_color = 'yellow'

if alien_color == 'green':
    print("Вы заработали 5 очков.")
elif alien_color == 'yellow':
    print("Вы заработали 10 очков.")
else:
    print("Вы заработали 15 очков.")
~~~

Source acceptance: отдельно проверить green, yellow и red.

## 5.6. Периоды жизни

~~~python
age = 20

if age < 2:
    stage = "младенец"
elif age < 4:
    stage = "малыш"
elif age < 13:
    stage = "ребенок"
elif age < 20:
    stage = "подросток"
elif age < 65:
    stage = "взрослый"
else:
    stage = "пожилой человек"

print(stage)
~~~

## 5.7. Любимый фрукт

Любимые фрукты пользователя: `[Needs confirmation]`.

~~~python
favorite_fruits = ['[фрукт1]', '[фрукт2]', '[фрукт3]']

if 'banana' in favorite_fruits:
    print("Вы очень любите бананы!")
~~~

Нужно пять независимых `if`; конкретные проверяемые фрукты: `[Needs confirmation]`.

## 5.8. Здравствуйте, админ!

~~~python
users = ['admin', 'user1', 'user2', 'user3', 'user4']

for user in users:
    if user == 'admin':
        print("Здравствуйте, admin, хотите просмотреть отчет о состоянии дел?")
    else:
        print(f"Привет, {user}, спасибо, что авторизовался в системе.")
~~~

Имена кроме `admin` — учебные placeholders.

## 5.9. Нет пользователей

~~~python
users = []

if users:
    for user in users:
        print(user)
else:
    print("Нам нужно добавить несколько пользователей!")
~~~

Пустой список — source-supported способ проверить требуемую ветвь.

## 5.10. Проверка имен пользователей

~~~python
current_users = ['Anna', 'Boris', 'John', 'Maria', 'Denis']
new_users = ['JOHN', 'Olga', 'Maria', 'Ivan', 'Pavel']

current_users_lower = [user.lower() for user in current_users]

for user in new_users:
    if user.lower() in current_users_lower:
        print(f"{user}: выберите другое имя.")
    else:
        print(f"{user}: имя доступно.")
~~~

List comprehension введён в предыдущей главе, а упражнение требует lower-case копию current users.

## 5.11. Порядковые числительные

~~~python
numbers = list(range(1, 10))

for number in numbers:
    if number == 1:
        print("1st")
    elif number == 2:
        print("2nd")
    elif number == 3:
        print("3rd")
    else:
        print(f"{number}th")
~~~

## 5.12. Форматирование операторов if

Конкретные файлы пользователя: `[Needs confirmation]`.

Source checklist: вокруг `==`, `>=`, `<=`, `<`, `>` используются пробелы.

## 5.13. Ваши идеи

Конкретные задачи пользователя: `[Needs confirmation]`.

Рабочая форма:

1. Идея 1 — `[Needs confirmation]`.
2. Идея 2 — `[Needs confirmation]`.
3. Идея 3 — `[Needs confirmation]`.

Источник предлагает направления: игры, анализ данных, веб-приложения, но не выбирает проект за читателя.
