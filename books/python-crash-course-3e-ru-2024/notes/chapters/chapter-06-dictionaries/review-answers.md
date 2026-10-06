# Разбор упражнений главы 6

Это RAG-grounded решения/шаблоны, не официальный ключ издателя. Персональные и внешние данные не выдумываются.

## 6.1. Персона

Конкретный человек и его данные: `[Needs confirmation]`.

~~~python
person = {
    'first_name': '[имя]',
    'last_name': '[фамилия]',
    'age': '[возраст]',
    'city': '[город]',
}

print(person['first_name'])
print(person['last_name'])
print(person['age'])
print(person['city'])
~~~

## 6.2. Любимые числа

Реальные имена/числа: `[Needs confirmation]`.

~~~python
favorite_numbers = {
    '[имя1]': '[число1]',
    '[имя2]': '[число2]',
    '[имя3]': '[число3]',
    '[имя4]': '[число4]',
    '[имя5]': '[число5]',
}

for name, number in favorite_numbers.items():
    print(f"{name}: {number}")
~~~

## 6.3. Глоссарий

Термины можно брать только из уже изученных глав. Один source-grounded набор категорий для заполнения:

~~~python
glossary = {
    'variable': '[определение]',
    'list': '[определение]',
    'tuple': '[определение]',
    'if': '[определение]',
    'dictionary': '[определение]',
}
~~~

Точные пользовательские формулировки определений: `[Needs confirmation]`.

## 6.4. Глоссарий 2

~~~python
for term, definition in glossary.items():
    print(f"\n{term}: {definition}")
~~~

Добавить ещё пять терминов: `[Needs confirmation]`.

## 6.5. Реки

Конкретные три реки/страны, кроме source example Nile/Egypt: `[Needs confirmation]`.

Механика:

~~~python
rivers = {
    'nile': 'egypt',
    '[river2]': '[country2]',
    '[river3]': '[country3]',
}

for river, country in rivers.items():
    print(f"{river.title()} протекает через {country.title()}.")

for river in rivers.keys():
    print(river.title())

for country in rivers.values():
    print(country.title())
~~~

## 6.6. Опрос

~~~python
favorite_languages = {
    'jen': 'python',
    'sarah': 'c',
    'edward': 'rust',
    'phil': 'python',
}

people = ['jen', 'erin', 'phil', 'maria']

for person in people:
    if person in favorite_languages.keys():
        print(f"{person.title()}, спасибо за участие.")
    else:
        print(f"{person.title()}, примите участие в опросе.")
~~~

Имена вне source dictionary — учебные placeholders.

## 6.7. Люди

Конкретные люди: `[Needs confirmation]`.

~~~python
person_1 = {'first_name': '[имя1]', 'last_name': '[фамилия1]', 'age': '[возраст1]', 'city': '[город1]'}
person_2 = {'first_name': '[имя2]', 'last_name': '[фамилия2]', 'age': '[возраст2]', 'city': '[город2]'}
person_3 = {'first_name': '[имя3]', 'last_name': '[фамилия3]', 'age': '[возраст3]', 'city': '[город3]'}

people = [person_1, person_2, person_3]

for person in people:
    print(person)
~~~

## 6.8. Домашние животные

Реальные животные/владельцы: `[Needs confirmation]`.

~~~python
pet_1 = {'kind': '[вид]', 'owner': '[владелец]'}
pet_2 = {'kind': '[вид]', 'owner': '[владелец]'}

pets = [pet_1, pet_2]

for pet in pets:
    print(pet)
~~~

## 6.9. Любимые места

Имена и реальные любимые места: `[Needs confirmation]`.

~~~python
favorite_places = {
    '[имя1]': ['[место1]', '[место2]'],
    '[имя2]': ['[место1]'],
    '[имя3]': ['[место1]', '[место2]', '[место3]'],
}

for name, places in favorite_places.items():
    print(name)
    for place in places:
        print(place)
~~~

## 6.10. Любимые числа

Реальные значения: `[Needs confirmation]`.

~~~python
favorite_numbers = {
    '[имя1]': ['[число1]', '[число2]'],
    '[имя2]': ['[число1]'],
}

for name, numbers in favorite_numbers.items():
    print(name)
    for number in numbers:
        print(number)
~~~

## 6.11. Города

Конкретные города, численность и факты требуют выбора/данных пользователя: `[Needs confirmation]`.

Структура:

~~~python
cities = {
    '[город1]': {
        'country': '[страна]',
        'population': '[население]',
        'fact': '[факт]',
    },
    '[город2]': {
        'country': '[страна]',
        'population': '[население]',
        'fact': '[факт]',
    },
    '[город3]': {
        'country': '[страна]',
        'population': '[население]',
        'fact': '[факт]',
    },
}

for city, info in cities.items():
    print(city)
    print(info)
~~~

Внешние сведения о городах в режиме `rag_only` не подбираются.

## 6.12. Расширение

Выбранный пример и желаемое расширение: `[Needs confirmation]`.

Source-supported варианты изменения:
- добавить пары key/value;
- изменить контекст;
- улучшить форматирование вывода.
