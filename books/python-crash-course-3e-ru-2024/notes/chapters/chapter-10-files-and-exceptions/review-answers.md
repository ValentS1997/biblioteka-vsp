# Разбор упражнений главы 10

Это RAG-grounded решения/шаблоны, не официальный ключ издателя.

## 10.1. Изучение Python

Содержимое пользовательского файла: `[Needs confirmation]`.

~~~python
from pathlib import Path

path = Path('learning_python.txt')
contents = path.read_text()

print(contents)

for line in contents.splitlines():
    print(line)
~~~

## 10.2. Изучение C

~~~python
from pathlib import Path

path = Path('learning_python.txt')
contents = path.read_text()

for line in contents.splitlines():
    print(line.replace('Python', 'C'))
~~~

## 10.3. Более простой код

Source-required transformation:

~~~python
for line in contents.splitlines():
    print(line)
~~~

Конкретные программы пользователя: `[Needs confirmation]`.

## 10.4. Гость

Имя пользователя: `[Needs confirmation]`.

~~~python
from pathlib import Path

name = input("Ваше имя: ")
path = Path('guest.txt')
path.write_text(name)
~~~

Risk: если `guest.txt` уже существует, source `write_text()` перезапишет его.

## 10.5. Гостевая книга

Source требует цикл и накопление нескольких строк перед записью.

~~~python
from pathlib import Path

contents = ""

while True:
    name = input("Имя (или 'q'): ")
    if name == 'q':
        break

    print(f"Здравствуйте, {name}!")
    contents += f"{name}\n"

path = Path('guest_book.txt')
path.write_text(contents)
~~~

Конкретный quit value source exercise не задаёт: `'q'` здесь выбран по pattern предыдущих глав.

## 10.6. Сложение

~~~python
try:
    first = int(input("Первое число: "))
    second = int(input("Второе число: "))
except ValueError:
    print("Введите числовые значения.")
else:
    print(first + second)
~~~

Source требует проверить success и invalid-text case.

## 10.7. Калькулятор

Source cross-reference ошибочен; по собственному описанию упражнения это loop вокруг сценария 10.6.

~~~python
while True:
    first = input("Первое число (или 'q'): ")
    if first == 'q':
        break

    second = input("Второе число (или 'q'): ")
    if second == 'q':
        break

    try:
        result = int(first) + int(second)
    except ValueError:
        print("Введите числовые значения.")
    else:
        print(result)
~~~

Quit value не задан формулировкой упражнения; `'q'` взят из source patterns главы.

## 10.8. Кошки и собаки

Имена животных: `[Needs confirmation]`.

~~~python
from pathlib import Path

paths = [Path('cats.txt'), Path('dogs.txt')]

for path in paths:
    try:
        contents = path.read_text()
    except FileNotFoundError:
        print(f"Файл {path} не найден.")
    else:
        print(contents)
~~~

Acceptance: переместить один файл и подтвердить `except`.

## 10.9. Ошибки без уведомления

Source scenario соответствует 10.8, хотя cross-reference указывает 10.7.

~~~python
for path in paths:
    try:
        contents = path.read_text()
    except FileNotFoundError:
        pass
    else:
        print(contents)
~~~

## 10.10. Распространенные слова

Тексты Project Gutenberg: `[Needs confirmation]` — external source не использовался.

Source counting primitives:

~~~python
count_1 = contents.lower().count('the')
count_2 = contents.lower().count('the ')
print(count_1)
print(count_2)
~~~

## 10.11. Любимое число

Любимое число пользователя: `[Needs confirmation]`.

Writer:

~~~python
from pathlib import Path
import json

number = input("Любимое число: ")
path = Path('favorite_number.json')
path.write_text(json.dumps(number))
~~~

Reader:

~~~python
from pathlib import Path
import json

path = Path('favorite_number.json')
number = json.loads(path.read_text())
print(f"Я знаю ваше любимое число! Это {number}")
~~~

## 10.12. Сохраненное любимое число

~~~python
from pathlib import Path
import json

path = Path('favorite_number.json')

if path.exists():
    number = json.loads(path.read_text())
    print(f"Я знаю ваше любимое число! Это {number}")
else:
    number = input("Любимое число: ")
    path.write_text(json.dumps(number))
~~~

Acceptance: первый и второй запуск дают разные branches.

## 10.13. Словарь пользователя

Дополнительные поля: `[Needs confirmation]`.

~~~python
from pathlib import Path
import json

user = {
    'name': input("Имя: "),
    'field_1': input("Поле 1: "),
    'field_2': input("Поле 2: "),
}

path = Path('user.json')
path.write_text(json.dumps(user))

stored_user = json.loads(path.read_text())
print(stored_user)
~~~

## 10.14. Проверка пользователя

~~~python
from pathlib import Path
import json

def get_stored_username(path):
    if path.exists():
        return json.loads(path.read_text())
    return None

def get_new_username(path):
    username = input("What is your name? ")
    path.write_text(json.dumps(username))
    return username

def greet_user():
    path = Path('username.json')
    username = get_stored_username(path)

    if username:
        correct = input(f"Are you {username}? (yes/no) ")
        if correct == 'yes':
            print(f"Welcome back, {username}!")
        else:
            username = get_new_username(path)
            print(f"We'll remember you when you come back, {username}!")
    else:
        username = get_new_username(path)
        print(f"We'll remember you when you come back, {username}!")

greet_user()
~~~

Exact yes/no wording source не задаёт; обязательная семантика — подтвердить identity перед reuse stored name.
