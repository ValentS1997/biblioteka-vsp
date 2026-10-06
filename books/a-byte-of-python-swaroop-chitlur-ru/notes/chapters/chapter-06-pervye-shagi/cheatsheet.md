# Chapter 6 cheatsheet — «Первые шаги»

## Symptom / problem framing

Python установлен, но нужно получить первый рабочий цикл:
**ввести код → запустить → увидеть результат → сохранить → повторно запустить → получить справку**.

## Baseline / context

Два режима source workflow:

1. interactive interpreter;
2. program file.

Для файлового режима нужен редактор и известный каталог сохранения.

## Read-only checks

### Запуск интерпретатора

```text
python3
```

Expected source signal: приглашение `>>>`.

### Встроенная справка

```python
help(print)
help()
help('return')
```

Для выхода из help source указывает клавишу `q`.

### PATH inspection

```text
echo $PATH
```

Это чтение текущего значения переменной окружения.

## Interpretation

- Interactive prompt удобен для немедленного выполнения одиночных выражений.
- Файл нужен для программы, которую требуется сохранять и запускать повторно.
- Source подчёркивает чувствительность Python к регистру: `print` и `Print` различны.
- Source также предупреждает проверить отсутствие нежелательных пробелов/табуляции
  перед первым символом строки.
- Syntax highlighting и automatic indentation названы важными свойствами редактора.
- Shebang + executable bit позволяют Unix-like системе выбирать interpreter через
  `/usr/bin/env python3`.
- Каталог из `PATH` позволяет запускать script без полного пути.

## Next action

После успешного `helloworld.py` и знакомства с `help()` глава 6 завершает bootstrap.
Следующая глава — «Основы»: константы, переменные и другие базовые элементы языка.

## Modifying action

### Создать рабочий каталог

Source example:

```text
mkdir /tmp/py
```

Effect: создаёт каталог `/tmp/py`.

Verification: каталог используется как target для последующих `cd`/file operations.

Rollback: **[Needs confirmation]** — source не приводит команду удаления.

### Сделать script исполнимым

```text
chmod a+x helloworld.py
```

Effect: добавляет executable attribute всем users по source explanation.

Verification:

```text
./helloworld.py
```

Rollback: **[Needs confirmation]** — source не приводит inverse mode command.

### Скопировать script в PATH directory

```text
cp helloworld.py /home/swaroop/bin/helloworld
```

Effect: создаёт копию script в source-specific каталоге из `PATH`.

Verification:

```text
helloworld
```

Rollback: **[Needs confirmation]**.

### Изменить PATH текущего shell context

```text
PATH=$PATH:/home/swaroop/mydir
```

Effect: добавляет source-specific каталог к значению `PATH` в текущем shell context.

Verification:

```text
echo $PATH
```

Rollback: **[Needs confirmation]** — source не приводит процедуру восстановления
предыдущего значения.

## Verification / acceptance checks

Минимальный acceptance:

1. `python3` открывает prompt;
2. `print(...)` выдаёт ожидаемый текст;
3. `python3 helloworld.py` выводит `Привет, Мир!`;
4. после executable setup `./helloworld.py` выводит тот же текст;
5. `help(print)` открывает справку.

## Rollback

Для filesystem/permission/PATH changes source-specific rollback-команды отсутствуют:
**[Needs confirmation]**.
