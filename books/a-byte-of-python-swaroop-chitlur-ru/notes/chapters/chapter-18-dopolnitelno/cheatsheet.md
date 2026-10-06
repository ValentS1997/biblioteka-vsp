# Chapter 18 cheatsheet — «Дополнительно»

## Symptom / problem framing

Нужно знать компактные Python idioms и расширенные mechanics, которые часто встречаются
в реальном коде поверх базовых constructs.

## Baseline / context

Source feature map:

`unpacking → special methods → lambda/comprehensions → *args/**kwargs → exec/eval → assert/repr → strings`

## Read-only checks

Перед использованием проверить:

1. Сколько values возвращает/unpacks выражение.
2. Какие special methods реально вызываются выбранной operation.
3. Не ухудшает ли single-line block читаемость.
4. `lambda` действительно короткая и локальная.
5. List comprehension не меняет исходный list в source pattern.
6. `*args` и `**kwargs` используются в ожидаемом binding position.
7. String для `exec` / `eval` полностью контролируется и проверена.
8. `assert` не подменяет normal error handling в source recommendation.
9. Representation из `repr` не принимается автоматически за serializable round-trip guarantee.
10. Escape/raw-string form соответствует ожидаемому literal content.

## Interpretation

- `a, b = expr` распаковывает two-value result in source example.
- `a, *b = ...` собирает остаток в `b`.
- `a, b = b, a` меняет значения местами.
- `__getitem__` source связывает с indexing syntax.
- `__len__` source связывает с `len()`.
- `lambda i: i['y']` служит sort key.
- List comprehension одновременно задаёт transformation и optional filter.
- `*args` → tuple in source explanation.
- `**kwargs` → dictionary-like key/value collection in source explanation.
- `exec` выполняет code text; `eval` вычисляет expression text.
- `assert` false-path → source `AssertionError`.
- `repr` can be customized by `__repr__`.
- Raw strings reduce backslash escaping in source regex recommendation.

## Next action

Следующая глава — «Что дальше».

## Modifying action

### In-place list sort

```python
points.sort(key=lambda i: i['y'])
```

Effect: changes `points` ordering in place.

Verification: source output starts with the item whose `y` is 1.

Rollback: re-create original list/order manually; no generic source rollback.

### List mutation in assert example

```python
mylist.pop()
```

Effect: removes list element.

Verification: source shows `mylist == []`.

Rollback: reinsert/recreate element manually.

### Runtime code execution

```python
exec(code_string)
eval(expression_string)
```

Effect: runtime execution/evaluation; potentially arbitrary state change depending on input.

Verification: use only fixed, source-known strings in chapter examples.

Rollback: **[Needs confirmation]** for arbitrary executed payloads.

## Verification / acceptance checks

- `errnum, errstr` gets `2` and source error description.
- `a, *b = [1,2,3,4]` gives `a == 1`, `b == [2,3,4]`.
- lambda sorting yields `y=1` item before `y=3`.
- list comprehension yields `[6, 8]`.
- `powersum(2,3,4)` → `25`; `powersum(2,10)` → `100`.
- `eval('2*3')` → `6`.
- false assert source path raises `AssertionError`.
- `eval(repr(i)) == i` is true for the shown list example.

## Rollback

Runtime example mutations end with process.

Filesystem rollback for saved example files: **[Needs confirmation]**.
