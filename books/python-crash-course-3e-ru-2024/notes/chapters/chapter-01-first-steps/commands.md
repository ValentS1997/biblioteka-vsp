# Команды и инструменты главы 1

Включены только элементы, явно подтверждённые RAG главы 1. Современные альтернативы и привычные команды из model memory не добавлялись.

## Терминальный сеанс Python

| Элемент | ОС | Тип | Effect / риск | Verification | Rollback |
|---|---|---|---|---|---|
| `python` | Windows | workload-generating | Запускает интерактивный интерпретатор Python | Появляется баннер версии и `>>>` | Завершить сеанс через `exit()` или Ctrl+Z, Enter |
| `python3` | macOS/Linux | workload-generating | Запускает интерактивный интерпретатор Python 3 | Появляется баннер версии и `>>>` | `exit()` или Ctrl+D |
| `print("Hello Python interpreter!")` | все | workload-generating | Выполняет выражение в интерактивном интерпретаторе | Вывод `Hello Python interpreter!` | `[Not applicable]` |
| `exit()` | все | state-changing (session-local) | Завершает текущий интерактивный сеанс Python | Возврат к shell/command prompt | `[Not applicable]` |

## Запуск hello_world.py из терминала

### Windows

~~~text
C:\> cd Desktop\python_work
C:\Desktop\python_work> dir
hello_world.py
C:\Desktop\python_work> python hello_world.py
Hello Python world!
~~~

| Команда | Тип | Что делает в главе | Verification | Rollback |
|---|---|---|---|---|
| `cd Desktop\python_work` | state-changing (session-local) | Переходит в каталог проекта | Следующее приглашение показывает `python_work` | `[Needs confirmation]` |
| `dir` | read-only | Проверяет наличие `hello_world.py` | Имя файла присутствует в выводе | `[Not applicable]` |
| `python hello_world.py` | workload-generating | Запускает проверочную программу | `Hello Python world!` | `[Not applicable]` для программы главы |

### macOS / Linux

~~~text
~$ cd Desktop/python_work/
~/Desktop/python_work$ ls
hello_world.py
~/Desktop/python_work$ python3 hello_world.py
Hello Python world!
~~~

| Команда | Тип | Что делает в главе | Verification | Rollback |
|---|---|---|---|---|
| `cd Desktop/python_work/` | state-changing (session-local) | Переходит в каталог проекта | Следующее приглашение показывает `python_work` | `[Needs confirmation]` |
| `ls` | read-only | Проверяет наличие `hello_world.py` | Имя файла присутствует в выводе | `[Not applicable]` |
| `python3 hello_world.py` | workload-generating | Запускает проверочную программу | `Hello Python world!` | `[Not applicable]` для программы главы |

## Код hello_world.py

~~~python
print("Hello Python world!")
~~~

Тип: workload-generating при выполнении.

Эффект в контексте главы: выводит одну строку текста. Это минимальный end-to-end тест редактора и интерпретатора.

## Инструменты и state-changing действия

| Инструмент / действие | ОС | Тип | Source-confirmed effect | Verification | Rollback |
|---|---|---|---|---|---|
| Официальный installer с `python.org` | Windows/macOS | state-changing | Устанавливает Python | Повторно запустить `python` / `python3` | `[Needs confirmation]` |
| Add Python to PATH | Windows | state-changing | Упрощает обнаружение Python системой | `python` запускает интерпретатор | `[Needs confirmation]` |
| `Install Certificates.command` | macOS | state-changing | После установки Python помогает устанавливать дополнительные библиотеки | Отдельный verification в главе не задан | `[Needs confirmation]` |
| Ubuntu Software Center → Visual Studio Code | Ubuntu | state-changing | Устанавливает VS Code | Запустить VS Code | `[Needs confirmation]` |
| VS Code Python extension (Microsoft) | все | state-changing | Добавляет поддержку разработки, редактирования и запуска Python | Открыть/запустить `.py` файл в VS Code | `[Needs confirmation]` |
| Создание `python_work` и `hello_world.py` | все | state-changing (user files) | Создаёт учебный каталог и программу | `dir` / `ls` и запуск файла | Источник предлагает удалить и создать `hello_world.py` заново при проблемах |

## VS Code actions

- File → New File.
- Сохранить файл как `hello_world.py` в `python_work`.
- Run → Run Without Debugging.
- Windows/Linux shortcut в источнике: `Ctrl+F5`.
- macOS shortcut извлечён RAG как `⌘+B`; значение сохранено без исправления из внешнего знания.

## Source-confirmed URLs

- `https://python.org/`
- `https://code.visualstudio.com`
- `https://ehmatthes.github.io/pcc_3e`

URL перечислены потому, что присутствуют в главе. Они не открывались и не использовались как внешние источники.
