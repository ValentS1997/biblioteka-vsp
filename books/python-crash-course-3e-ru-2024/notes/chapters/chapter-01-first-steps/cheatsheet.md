# Шпаргалка главы 1 — Первые шаги

## Symptom / problem framing

Цель главы — получить минимальную рабочую среду Python и подтвердить её запуском `hello_world.py`.

Негативный сигнал: интерпретатор не запускается, версия ниже требуемой книгой, VS Code не запускает файл, либо программа не выводит `Hello Python world!`.

## Baseline / context

- Книга рассчитывает примеры на Python 3.9 или новее.
- На момент написания книги новой версией была Python 3.11.
- Windows: глава использует команду `python`.
- macOS/Linux: глава использует `python3`.
- Основной редактор главы: VS Code с Python extension от Microsoft.
- Проверочный файл: `python_work/hello_world.py`.

## Read-only checks

Проверки не изменяют постоянную конфигурацию, но запускают процессы интерпретатора:

### Windows

~~~text
C:\> python
~~~

Ожидаемый признак: баннер Python и приглашение `>>>`.

### macOS / Linux

~~~text
$ python3
~~~

Ожидаемый признак: баннер Python и приглашение `>>>`.

### Проверка интерактивного выполнения

~~~python
>>> print("Hello Python interpreter!")
Hello Python interpreter!
~~~

### Проверка наличия файла перед запуском

Windows:

~~~text
C:\Desktop\python_work> dir
hello_world.py
~~~

macOS/Linux:

~~~text
~/Desktop/python_work$ ls
hello_world.py
~~~

## Interpretation

- Есть `>>>` и версия Python 3.9+ → по критерию книги интерпретатор пригоден для примеров главы.
- Команда не распознана / Windows открывает Microsoft Store → Python не установлен по сценарию главы; источник рекомендует официальный дистрибутив с python.org.
- VS Code запускает `hello_world.py` и получает ожидаемый текст → минимальная цепочка среды работает.
- Ошибка при запуске → сначала анализировать traceback и точность синтаксиса.
- Ошибка может быть вызвана регистром `print`, отсутствующей кавычкой или непарной скобкой.

## Next action

1. Определить свою ОС.
2. Запустить `python` (Windows) или `python3` (macOS/Linux).
3. Если версия соответствует требованию книги, перейти к VS Code.
4. Установить Python extension.
5. Создать `python_work/hello_world.py`.
6. Запустить файл.
7. Сверить результат с `Hello Python world!`.

## Modifying action

Следующие действия изменяют систему или пользовательские файлы:

- установка Python;
- Windows: включение Add Python to PATH при установке;
- macOS: запуск `Install Certificates.command` после установки Python;
- установка VS Code;
- установка Python extension в VS Code;
- создание каталога `python_work`;
- создание/изменение `hello_world.py`.

Перед изменением: убедиться, что действие относится к вашей ОС и действительно требуется.

## Verification / acceptance checks

Минимальный acceptance chain главы:

1. Интерпретатор запускается.
2. Приглашение `>>>` доступно.
3. `print("Hello Python interpreter!")` выводит ожидаемый текст.
4. VS Code с Python extension открывает `hello_world.py`.
5. Файл содержит:

~~~python
print("Hello Python world!")
~~~

6. Запуск выдаёт:

~~~text
Hello Python world!
~~~

7. При запуске из терминала файл виден через `dir` или `ls`, затем выполняется `python hello_world.py` или `python3 hello_world.py`.

## Rollback

- Для неудачного `hello_world.py` источник прямо предлагает удалить файл и создать его заново.
- Для установки Python, изменения PATH, установки VS Code и extension процедура rollback в главе не описана: `[Needs confirmation]`.
- Для `cd` изменение относится только к текущему терминальному сеансу; конкретная команда возврата в главе не задана: `[Needs confirmation]`.

## Troubleshooting sequence

`сбой → traceback → проверить символы/регистр/кавычки/скобки → перечитать шаг → при необходимости пересоздать файл → повторить запуск`.

Если этого недостаточно, книга рекомендует приложения и помощь сообщества. Эти внешние источники в текущем RAG-only анализе не использовались.
