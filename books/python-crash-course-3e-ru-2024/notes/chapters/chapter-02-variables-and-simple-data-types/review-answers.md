# Разбор упражнений главы 2

Это RAG-grounded решения/шаблоны, а не официальный ключ издателя.

## 2.1. Простое сообщение

Один минимальный вариант, использующий конструкции главы:

~~~python
message = "Hello Python world!"
print(message)
~~~

## 2.2. Простые сообщения

~~~python
message = "Hello Python world!"
print(message)

message = "Hello Python Crash Course world!"
print(message)
~~~

Ожидается два разных сообщения, потому что второе присваивание меняет текущее значение `message`.

## 2.3. Личное сообщение

Имя пользователя: `[Needs confirmation]`.

Шаблон:

~~~python
name = "[имя]"
message = f"Здравствуйте, {name}, не хотите ли вы изучить Python сегодня?"
print(message)
~~~

Сам текст-пример основан на упражнении; конкретное имя не выдумывается.

## 2.4. Регистр символов в именах

Имя пользователя: `[Needs confirmation]`.

~~~python
name = "[имя]"
print(name.lower())
print(name.upper())
print(name.title())
~~~

## 2.5. Знаменитая цитата

Выбранная пользователем цитата: `[Needs confirmation]`.

Source exercise уже даёт пример с Альбертом Эйнштейном; его можно использовать как учебный образец, но пользовательский выбор не подменяется.

Шаблон:

~~~python
print('[автор] однажды сказал: "[цитата]"')
~~~

## 2.6. Знаменитая цитата 2

~~~python
famous_person = "[автор]"
message = f'{famous_person} однажды сказал: "[цитата]"'
print(message)
~~~

Автор и цитата: `[Needs confirmation]`.

## 2.7. Удаление пробельных символов

Имя пользователя: `[Needs confirmation]`.

~~~python
name = "\t[имя]\n"

print(name)
print(name.lstrip())
print(name.rstrip())
print(name.strip())
~~~

Source acceptance: сравнить исходный вывод с тремя вариантами очистки.

## 2.8. Расширения файлов

~~~python
filename = "python_notes.txt"
print(filename.removesuffix(".txt"))
~~~

Ожидаемое значение по логике source example:

~~~text
python_notes
~~~

## 2.9. Число 8

~~~python
print(5 + 3)
print(10 - 2)
print(4 * 2)
print(16 / 2)
~~~

Первые три выражения выводят `8`. Для деления сама глава ранее устанавливает правило: `/` возвращает float даже при делении целых, поэтому последняя строка отображается как `8.0`.

Это не исправляется молча; см. [source-findings.md](source-findings.md).

## 2.10. Любимое число

Любимое число пользователя: `[Needs confirmation]`.

~~~python
favorite_number = [число]
message = f"Мое любимое число — {favorite_number}."
print(message)
~~~

## 2.11. Добавление комментариев

Конкретные две программы, имя и текущая дата пользователя: `[Needs confirmation]`.

Source-grounded шаблон:

~~~python
# [кратко: что делает программа]
print("Hello Python world!")
~~~

Если используется вариант с именем/датой из упражнения:

~~~python
# [имя], [дата]
# [одно предложение о назначении программы]
~~~

## 2.12. Дзен Python

Source command:

~~~python
>>> import this
~~~

В RAG главы явно представлены следующие идеи:

- красивое лучше уродливого;
- простое лучше сложного;
- сложное лучше запутанного;
- удобочитаемость имеет значение;
- желательно иметь один очевидный способ решения;
- сейчас лучше, чем никогда.

Упражнение просит просмотреть и другие принципы, но полный вывод `import this` в chapter RAG не содержится. Поэтому остальные пункты: `[Needs confirmation]` / `RAG_MISS`; они не восстанавливаются из model memory.
