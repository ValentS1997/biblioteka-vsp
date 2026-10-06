# Разбор упражнений главы 7

Это RAG-grounded решения/шаблоны, не официальный ключ издателя.

## 7.1. Каршеринг

Желаемая машина пользователя: `[Needs confirmation]`.

~~~python
car = input("Какую машину вы хотели бы взять напрокат? ")
print(f"Посмотрим, смогу ли я найти вам {car}.")
~~~

## 7.2. Заказ стола

~~~python
people = input("На сколько мест забронировать стол? ")
people = int(people)

if people > 8:
    print("Вам придется немного подождать.")
else:
    print("Ваш стол готов.")
~~~

## 7.3. Числа, кратные 10

~~~python
number = input("Введите число: ")
number = int(number)

if number % 10 == 0:
    print("Число кратно 10.")
else:
    print("Число не кратно 10.")
~~~

## 7.4. Начинки для пиццы

Конкретные toppings вводит пользователь во время работы программы.

~~~python
prompt = "Введите начинку для пиццы (или 'quit'): "
topping = ""

while topping != 'quit':
    topping = input(prompt)
    if topping != 'quit':
        print(f"Добавляем {topping}.")
~~~

## 7.5. Билеты в кино

Чтобы цикл имел source-supported способ выхода, можно использовать quit value:

~~~python
prompt = "Введите возраст (или 'quit'): "

while True:
    age = input(prompt)

    if age == 'quit':
        break

    age = int(age)

    if age < 3:
        print("Билет бесплатный.")
    elif age <= 12:
        print("Билет стоит 10 долларов.")
    else:
        print("Билет стоит 15 долларов.")
~~~

Это сохраняет границы, заданные упражнением: младше 3, 3–12, старше 12.

## 7.6. Три выхода

Source wording требует представить три механизма. Практически безопаснее оформить три отдельные версии одной задачи, а не пытаться одновременно сделать три exit mechanisms активными в одном цикле.

### Условие while

~~~python
topping = ""

while topping != 'quit':
    topping = input("Topping: ")
~~~

### Flag

~~~python
active = True

while active:
    topping = input("Topping: ")
    if topping == 'quit':
        active = False
~~~

### break

~~~python
while True:
    topping = input("Topping: ")
    if topping == 'quit':
        break
~~~

Точная интерпретация единственного/нескольких вариантов в формулировке упражнения: `[Needs confirmation]`.

## 7.7. Бесконечный цикл

Минимальная source-consistent форма:

~~~python
while True:
    print("loop")
~~~

Риск: бесконечный stdout.

Source stop action: `Ctrl+C` или закрыть окно вывода.

## 7.8. Бутерброды

Виды бутербродов: `[Needs confirmation]`.

~~~python
sandwich_orders = ['[заказ1]', '[заказ2]', '[заказ3]']
finished_sandwiches = []

while sandwich_orders:
    current = sandwich_orders.pop()
    print(f"Я приготовил бутерброд {current}.")
    finished_sandwiches.append(current)

for sandwich in finished_sandwiches:
    print(sandwich)
~~~

## 7.9. Без пастромы

~~~python
sandwich_orders = ['pastrami', '[заказ1]', 'pastrami', '[заказ2]', 'pastrami']
finished_sandwiches = []

print("Пастромы больше нет.")

while 'pastrami' in sandwich_orders:
    sandwich_orders.remove('pastrami')

while sandwich_orders:
    current = sandwich_orders.pop()
    finished_sandwiches.append(current)

print(finished_sandwiches)
~~~

Acceptance: `'pastrami'` отсутствует в `finished_sandwiches`.

## 7.10. Отпуск мечты

Ответы пользователей: `[Needs confirmation]`.

~~~python
responses = {}
polling_active = True

while polling_active:
    name = input("Ваше имя: ")
    place = input("Если бы вы могли посетить одно место в мире, куда бы вы отправились? ")

    responses[name] = place

    repeat = input("Добавить еще ответ? (yes/no) ")
    if repeat == 'no':
        polling_active = False

for name, place in responses.items():
    print(f"{name}: {place}")
~~~

Source note: chapter example `mountain_poll.py` содержит отдельный output-order finding; этот шаблон не задаёт конкретный порядок пользовательских ответов заранее.
