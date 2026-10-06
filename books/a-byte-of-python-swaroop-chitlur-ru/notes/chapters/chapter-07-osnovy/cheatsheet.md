# Chapter 7 cheatsheet — «Основы»

## Symptom / problem framing

Нужно перейти от запуска первой программы к пониманию базовой структуры Python-кода:
какие значения существуют, как их именовать/хранить и как Python определяет границы
выражений и блоков.

## Baseline / context

Базовая цепочка главы:

`literal → value/type → variable/identifier → expression line → block by indentation`

Отдельная ветка для текста:

`string → quoting → immutability → format()`.

## Read-only checks

При ревью Python source проверить:

1. Комментарий объясняет предположение/решение/проблему, а не просто повторяет код.
2. Identifier начинается с разрешённого символа.
3. Case-sensitive names не перепутаны.
4. Строки заключены в корректные quotes.
5. Для нескольких logical statements на одной physical line не используется случайный semicolon.
6. Continuation выполнен явно `\` или неявно внутри brackets.
7. Statements одного блока имеют одинаковый indentation style.
8. Пробелы и tabs не смешиваются без необходимости.

## Interpretation

- Literal constant представляет значение непосредственно.
- Variable позволяет связать имя со значением и затем изменить эту связь.
- Python 3 strings source-framing — Unicode by default.
- Single и double quotes в source описаны как эквивалентные.
- Triple quotes позволяют multiline strings.
- Strings immutable: созданное строковое значение не изменяется in-place.
- Adjacent string literals могут автоматически объединяться.
- `format()` отделяет message template от подставляемых данных.
- Python не требует предварительного объявления variable type в source example.
- Indentation — синтаксический механизм группировки blocks, а не косметическое оформление.

## Next action

Глава 8 «Операторы и выражения» использует эти основы для разбора operators, operands
и evaluation expressions.

## Modifying action

### Assignment в программе

```python
i = 5
i = i + 1
```

Effect: имя `i` связывается сначала со значением 5, затем со значением 6 в runtime.

Verification:

```python
print(i)
```

Source output после второго assignment: `6`.

Rollback: [Not applicable] для учебного runtime example после завершения процесса.

### Создание/изменение source file

Глава просит сохранить examples как `str_format.py` и `var.py`.

Effect: создаётся/изменяется файл программы.

Verification: запустить соответствующий source command и сравнить output.

Rollback: **[Needs confirmation]** — source не задаёт file rollback procedure.

## Verification / acceptance checks

- `var.py` выдаёт source sequence `5`, затем `6`, затем две строки текста.
- `str_format.py` подставляет `Swaroop` и `26` в placeholders.
- intentionally bad indent выдаёт `IndentationError: unexpected indent`.
- valid identifiers проходят rules из 7.6; invalid examples нарушают их.

## Rollback

Для runtime assignments rollback не нужен после завершения process.

Для созданных/редактируемых `.py` files source-specific rollback:
**[Needs confirmation]**.
