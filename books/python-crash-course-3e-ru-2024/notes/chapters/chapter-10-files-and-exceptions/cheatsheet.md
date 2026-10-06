# Шпаргалка главы 10 — Файлы и исключения

## Problem framing

Типовые задачи:

- прочитать весь файл;
- обработать файл построчно;
- понять relative/absolute path;
- сохранить строку в файл;
- не перезаписать данные случайно;
- обработать ожидаемое исключение без crash;
- продолжить обработку остальных файлов;
- сохранить пользовательские данные между запусками.

## Read-only checks

~~~python
from pathlib import Path

path = Path('pi_digits.txt')
contents = path.read_text()
print(contents)
~~~

Построчно:

~~~python
for line in contents.splitlines():
    print(line)
~~~

Проверка existence:

~~~python
if path.exists():
    ...
~~~

## File path model

Relative:

~~~python
Path('text_files/file.txt')
~~~

Absolute source example:

~~~python
Path('/home/eric/data_files/text_files/file.txt')
~~~

Реальный абсолютный путь в окружении пользователя: `[Needs confirmation]`.

## Modifying action: write_text()

~~~python
path = Path('programming.txt')
path.write_text("I love programming.")
~~~

Effect:
- создаёт файл, если его нет;
- source предупреждает: если файл уже существует, его содержимое будет перезаписано.

Risk: data loss through overwrite.

Verification:
- проверить target path;
- после записи прочитать файл и сверить содержимое.

Rollback: source не задаёт автоматического rollback. Если старое содержимое важно, backup/previous copy требуется определить отдельно: `[Needs confirmation]`.

## Exception flow

~~~python
try:
    answer = int(first_number) / int(second_number)
except ZeroDivisionError:
    print("You can't divide by 0!")
else:
    print(answer)
~~~

Source rule:
- в `try` — только потенциально failing code;
- `except` — expected exception;
- `else` — код, зависимый от success.

## FileNotFoundError

~~~python
try:
    contents = path.read_text(encoding='utf-8')
except FileNotFoundError:
    print(f"Sorry, the file {path} does not exist.")
~~~

Silent skip:

~~~python
except FileNotFoundError:
    pass
~~~

Использовать `pass` source предлагает только когда отсутствие файла допустимо и user notification не нужно.

## ValueError

Exercise 10.6/10.7 pattern:

~~~python
try:
    first = int(input("First number: "))
    second = int(input("Second number: "))
except ValueError:
    print("Введите числа.")
else:
    print(first + second)
~~~

Точная формулировка user-facing message не задана source: можно адаптировать.

## JSON persistence

Write:

~~~python
contents = json.dumps(numbers)
path.write_text(contents)
~~~

Read:

~~~python
contents = path.read_text()
numbers = json.loads(contents)
~~~

## Acceptance checks

- read target существует либо `FileNotFoundError` обработан;
- encoding задан там, где source example его использует;
- write target подтверждён до overwrite;
- `try` не содержит лишний unrelated code;
- failure path проверен намеренно;
- success path через `else` проверен;
- при обработке нескольких файлов missing file не блокирует последующие;
- JSON data читаются после отдельного write run;
- first-run и repeat-run persistence flow проверены.

## Security / exposure boundary

Source предупреждает: traceback может показать пользователю имя файла и проблемный участок кода. Это повод обрабатывать ожидаемые exceptions, но полноценная security model главы: `[Needs confirmation]`.
