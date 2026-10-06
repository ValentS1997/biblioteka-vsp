# Chapter 15 cheatsheet — «Ввод-вывод»

## Symptom / problem framing

Нужно взаимодействовать с пользователем и сохранять/восстанавливать данные через files.

## Baseline / context

Source I/O stack:

`input()/print() → text file I/O → pickle binary persistence`

## Read-only checks

Перед file operation проверить:

1. Какой file path будет открыт.
2. Какой mode используется: `r`, `w`, `a`, optional `t` / `b`.
3. Не приведёт ли `w` / `wb` к state change существующего target.
4. Закрывается ли file через `close()` в source flow.
5. Для `readline()` корректно ли обрабатывается empty string как EOF по source example.
6. Для palindrome check понимается ли `[::-1]`.
7. Для pickle совпадают ли write/read binary modes.

## Interpretation

- `input(prompt)` показывает prompt и возвращает введённый text.
- `[::-1]` используется для reverse string.
- `open(..., 'w')` source использует для text write.
- `open(path)` source трактует как default text read mode.
- `readline()` source example возвращает line including newline; empty string marks EOF.
- `print(..., end='')` подавляет дополнительный newline при печати уже прочитанной line.
- `wb` / `rb` используются для pickle data.
- `pickle.dump` сохраняет object в file; `pickle.load` восстанавливает object.

## Next action

Следующая глава — «Исключения»: обработка ошибок I/O и других exceptional conditions.

## Modifying action

### Write text file

```python
f = open('poem.txt', 'w')
f.write(poem)
f.close()
```

Effect: filesystem write; file может быть создан или перезаписан.

Verification: source script затем читает `poem.txt` и печатает poem.

Rollback: **[Needs confirmation]**.

### Write pickle file

```python
f = open('shoplist.data', 'wb')
pickle.dump(shoplist, f)
f.close()
```

Effect: filesystem binary write.

Verification:

```python
f = open(shoplistfile, 'rb')
storedlist = pickle.load(f)
print(storedlist)
```

Expected source output:

```text
['яблоки', 'манго', 'морковь']
```

Rollback: **[Needs confirmation]**.

## Verification / acceptance checks

- `user_input.py`: `мадам` and `топот` → palindrome; `сэр` → not palindrome.
- `using_file.py`: written poem is read back line-by-line and printed.
- `pickling.py`: restored list matches source list.
- No assumption is made that source homework already handles punctuation/case/spaces.

## Rollback

Runtime namespace effects end with process.

Filesystem rollback for `poem.txt` and `shoplist.data`: **[Needs confirmation]**.
