# Разбор упражнений главы 4

Это RAG-grounded решения/шаблоны, не официальный ключ издателя.

## 4.1. Пицца

Любимые виды пиццы пользователя: `[Needs confirmation]`.

~~~python
pizzas = ['[пицца1]', '[пицца2]', '[пицца3]']

for pizza in pizzas:
    print(f"Я люблю пиццу {pizza}.")

print("Я очень люблю пиццу!")
~~~

## 4.2. Животные

Конкретные животные и общее свойство: `[Needs confirmation]`.

~~~python
animals = ['[животное1]', '[животное2]', '[животное3]']

for animal in animals:
    print(animal)
    print(f"{animal} обладает общей характеристикой.")

print("[общее свойство]")
~~~

## 4.3. Считаем до 20

~~~python
for value in range(1, 21):
    print(value)
~~~

Верхняя граница `21` выбрана по source rule: `stop` не включается.

## 4.4. Миллион

~~~python
numbers = list(range(1, 1_000_001))

for number in numbers:
    print(number)
~~~

Это большой объём stdout. Source stop action: `Ctrl+C` или закрытие окна вывода.

## 4.5. Суммирование миллиона чисел

~~~python
numbers = list(range(1, 1_000_001))

print(min(numbers))
print(max(numbers))
print(sum(numbers))
~~~

Ожидаемые границы по конструкции списка: 1 и 1 000 000. Точное время выполнения: `[Needs confirmation]`.

## 4.6. Нечётные числа

~~~python
odd_numbers = list(range(1, 21, 2))

for number in odd_numbers:
    print(number)
~~~

## 4.7. Тройки

~~~python
multiples_of_three = list(range(3, 31, 3))

for number in multiples_of_three:
    print(number)
~~~

## 4.8. Кубы

~~~python
cubes = []

for value in range(1, 11):
    cubes.append(value**3)

for cube in cubes:
    print(cube)
~~~

## 4.9. Генератор кубов

~~~python
cubes = [value**3 for value in range(1, 11)]
print(cubes)
~~~

## 4.10. Срезы

Конкретный исходный список: `[Needs confirmation]`.

Для списка с достаточным количеством элементов source-supported формы:

~~~python
print(items[:3])
print(items[-3:])
~~~

Точный slice для «трёх элементов из середины» зависит от длины и выбранного списка: `[Needs confirmation]`. Источник не задаёт универсальные индексы.

## 4.11. Моя пицца, твоя пицца

Пиццы пользователя: `[Needs confirmation]`.

~~~python
pizzas = ['[пицца1]', '[пицца2]', '[пицца3]']
friend_pizzas = pizzas[:]

pizzas.append('[новая моя пицца]')
friend_pizzas.append('[новая пицца друга]')

print("Мои любимые пиццы:")
for pizza in pizzas:
    print(pizza)

print("Любимые пиццы моего друга:")
for pizza in friend_pizzas:
    print(pizza)
~~~

Разные добавленные значения проверяют, что `[:]` создал отдельный список.

## 4.12. Больше циклов

Source requirement — заменить прямой вывод каждого списка в выбранной версии `foods.py` на два `for`:

~~~python
for food in my_foods:
    print(food)

for food in friend_foods:
    print(food)
~~~

Конкретная версия исходного `foods.py`: `[Needs confirmation]`.

## 4.13. Шведский стол

Пять блюд пользователя: `[Needs confirmation]`.

~~~python
menu = ('[блюдо1]', '[блюдо2]', '[блюдо3]', '[блюдо4]', '[блюдо5]')

for item in menu:
    print(item)
~~~

Source-supported negative test:

~~~python
menu[0] = '[другое блюдо]'
~~~

Должен возникнуть `TypeError`, поскольку tuple item assignment не поддерживается.

Изменение меню делается переопределением всего tuple:

~~~python
menu = ('[новое1]', '[блюдо2]', '[блюдо3]', '[блюдо4]', '[новое2]')

for item in menu:
    print(item)
~~~

## 4.14. PEP 8

Требуется внешний ресурс. В режиме `rag_only` содержимое сайта не запрашивалось.

Статус: `[Needs confirmation]`.

Source-confirmed URL: `https://python.org/dev/peps/pep-0008/`.

## 4.15. Анализ кода

Какие именно три программы выбраны пользователем: `[Needs confirmation]`.

RAG-grounded checklist:
- четыре пробела на уровень indentation;
- строки менее 80 символов;
- без лишних пустых строк;
- редактор при Tab вставляет четыре пробела;
- визуальный ориентир у 80-го символа.

Конкретные изменения зависят от выбранных файлов.
