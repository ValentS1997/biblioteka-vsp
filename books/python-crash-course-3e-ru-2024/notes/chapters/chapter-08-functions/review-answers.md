# Разбор упражнений главы 8

Это RAG-grounded решения/шаблоны, не официальный ключ издателя.

## 8.1. Сообщение

~~~python
def display_message():
    print("В этой главе рассматриваются функции.")

display_message()
~~~

## 8.2. Любимая книга

Любимая книга пользователя: `[Needs confirmation]`.

~~~python
def favorite_book(title):
    print(f'Одна из моих любимых книг — "{title}".')

favorite_book('[название]')
~~~

## 8.3. Футболка

~~~python
def make_shirt(size, text):
    print(f"Размер: {size}; текст: {text}")

make_shirt('L', 'Python')
make_shirt(size='M', text='Python')
~~~

## 8.4. Большие футболки

~~~python
def make_shirt(size='L', text='Я люблю Python'):
    print(f"Размер: {size}; текст: {text}")

make_shirt()
make_shirt(size='M', text='Другой текст')
~~~

## 8.5. Города

Страна по умолчанию и выбранные города: `[Needs confirmation]`.

~~~python
def describe_city(city, country='[страна по умолчанию]'):
    print(f"{city} находится в {country}.")

describe_city('[город1]')
describe_city('[город2]')
describe_city('[город3]', '[другая страна]')
~~~

## 8.6. Названия городов

~~~python
def city_country(city, country):
    return f"{city.title()}, {country.title()}"

print(city_country('santiago', 'chile'))
~~~

Ещё две пары: `[Needs confirmation]`.

## 8.7. Альбом

Конкретные исполнители/альбомы: `[Needs confirmation]`.

~~~python
def make_album(artist, title, tracks=None):
    album = {'artist': artist, 'title': title}
    if tracks:
        album['tracks'] = tracks
    return album
~~~

Source exercise прямо просит default `None`; это отличается от отдельного finding в source example `build_person()`.

## 8.8. Пользовательские альбомы

~~~python
while True:
    artist = input("Исполнитель (или 'q'): ")
    if artist == 'q':
        break

    title = input("Альбом (или 'q'): ")
    if title == 'q':
        break

    print(make_album(artist, title))
~~~

## 8.9. Сообщения

Сообщения пользователя: `[Needs confirmation]`.

~~~python
def show_messages(messages):
    for message in messages:
        print(message)

messages = ['[сообщение1]', '[сообщение2]', '[сообщение3]']
show_messages(messages)
~~~

## 8.10. Отправка сообщений

~~~python
def send_messages(messages, sent_messages):
    while messages:
        message = messages.pop()
        print(message)
        sent_messages.append(message)

messages = ['[сообщение1]', '[сообщение2]', '[сообщение3]']
sent_messages = []

send_messages(messages, sent_messages)
print(messages)
print(sent_messages)
~~~

## 8.11. Архивированные сообщения

~~~python
messages = ['[сообщение1]', '[сообщение2]', '[сообщение3]']
sent_messages = []

send_messages(messages[:], sent_messages)

print(messages)
print(sent_messages)
~~~

Acceptance: `messages` сохраняет исходные элементы.

## 8.12. Бутерброды

Компоненты пользовательских заказов: `[Needs confirmation]`.

~~~python
def make_sandwich(*items):
    print(items)

make_sandwich('[компонент1]')
make_sandwich('[компонент1]', '[компонент2]')
make_sandwich('[компонент1]', '[компонент2]', '[компонент3]')
~~~

## 8.13. Профиль

Персональные данные пользователя: `[Needs confirmation]`.

~~~python
def build_profile(first, last, **user_info):
    user_info['first_name'] = first
    user_info['last_name'] = last
    return user_info

profile = build_profile(
    '[имя]',
    '[фамилия]',
    field1='[value1]',
    field2='[value2]',
    field3='[value3]',
)

print(profile)
~~~

## 8.14. Автомобили

Конкретный автомобиль: `[Needs confirmation]`.

~~~python
def make_car(manufacturer, model, **car_info):
    car_info['manufacturer'] = manufacturer
    car_info['model'] = model
    return car_info

car = make_car(
    'subaru',
    'outback',
    color='blue',
    tow_package=True,
)

print(car)
~~~

Вызов взят из формулировки упражнения.

## 8.15. Печать моделей

`printing_functions.py`:

~~~python
def print_models(unprinted_designs, completed_models):
    while unprinted_designs:
        current_design = unprinted_designs.pop()
        print(f"Printing model: {current_design}")
        completed_models.append(current_design)


def show_completed_models(completed_models):
    for completed_model in completed_models:
        print(completed_model)
~~~

Основной файл:

~~~python
import printing_functions

unprinted_designs = ['phone case', 'robot pendant', 'dodecahedron']
completed_models = []

printing_functions.print_models(unprinted_designs, completed_models)
printing_functions.show_completed_models(completed_models)
~~~

## 8.16. Импортирование

Конкретная пользовательская функция: `[Needs confirmation]`.

Source-required forms:

~~~python
import module_name
module_name.function_name()
~~~

~~~python
from module_name import function_name
function_name()
~~~

~~~python
from module_name import function_name as alias
alias()
~~~

~~~python
import module_name as alias
alias.function_name()
~~~

~~~python
from module_name import *
function_name()
~~~

Последняя форма присутствует в упражнении, хотя основной текст главы предупреждает о риске conflicts.

## 8.17. Форматирование функций

Выбранные три программы: `[Needs confirmation]`.

Checklist по source:
- lowercase function/module names с underscores;
- docstring сразу после `def`;
- defaults/keyword arguments без пробелов вокруг `=`;
- строки кода в пределах source recommendation;
- две пустые строки между функциями;
- imports в начале файла после возможных file comments.
