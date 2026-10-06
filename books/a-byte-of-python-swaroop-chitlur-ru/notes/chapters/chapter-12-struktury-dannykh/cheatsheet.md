# Chapter 12 cheatsheet — «Структуры данных»

## Symptom / problem framing

Нужно хранить несколько связанных значений и понимать, какой контейнер нужен:
изменяемая последовательность, неизменяемая последовательность, mapping или множество.

## Baseline / context

Source map:

`list → mutable sequence`  
`tuple → immutable sequence`  
`dict → key/value mapping`  
`set → unordered membership-oriented collection`

Общие sequence operations для list/tuple/string:

- membership;
- indexing;
- negative indexing;
- slicing;
- slice step.

## Read-only checks

При ревью data structure usage проверить:

1. Нужна ли mutation после создания.
2. Требуется ли key/value lookup или positional indexing.
3. Используется ли zero-based index.
4. Правильно ли понимается end-exclusive slice.
5. Не перепутана ли ссылка на тот же объект с копией.
6. Для set не зависит ли логика от order.
7. Для string search проверяется ли `find(...) != -1`, если используется source pattern.
8. Mutation method действительно должен менять исходный object.

## Interpretation

- `list.append` добавляет элемент к исходному list.
- `list.sort` source подчёркивает как in-place mutation.
- Tuple nesting сохраняет вложенный tuple как отдельный object.
- Singleton tuple требует comma: `(2,)`.
- Dict lookup использует key вместо numeric position.
- `in` применяется и к sequences, и к source set/dict examples.
- Slice `[start:end]` включает start и исключает end.
- `[::-1]` source демонстрирует reverse slice.
- `mylist = shoplist` создаёт второе имя того же list object.
- `mylist = shoplist[:]` в source example создаёт отдельный list copy.
- `join` собирает sequence strings с delimiter.

## Next action

Следующая глава — «Решение задач»: накопленные language/data-structure concepts
используются для проектирования полноценной backup program.

## Modifying action

### List mutation

```python
shoplist.append('рис')
shoplist.sort()
del shoplist[0]
```

Effect: исходный `shoplist` меняется.

Verification: `print(shoplist)`.

Rollback: **[Needs confirmation]** — source не даёт generic inverse procedure.

### Dictionary mutation

```python
del ab['Spammer']
ab['Guido'] = 'guido@python.org'
```

Effect: удаляет и добавляет key/value pairs.

Verification: length/items/membership examples из source.

Rollback: **[Needs confirmation]**.

### Set mutation

```python
bric.add('Китай')
bri.remove('Россия')
```

Effect: изменяет соответствующие set objects.

Verification: membership / `issuperset` / intersection.

Rollback: **[Needs confirmation]**.

### File creation/edit

Source examples: `using_list.py`, `using_tuple.py`, `using_dict.py`, `seq.py`,
`reference.py`, `str_methods.py`.

Effect: filesystem change.

Rollback: **[Needs confirmation]**.

## Verification / acceptance checks

- `using_list.py`: append/sort/delete видны в output.
- `using_tuple.py`: source reports 5 total animals in nested tuple example.
- `using_dict.py`: Spammer removed, Guido added.
- `seq.py`: negative indices/slices match shown output.
- set REPL: India membership True, USA False, intersection contains Brazil/India.
- `reference.py`: alias changes together; slice-copy diverges after deletion.
- `str_methods.py`: startswith/in/find/join source outputs observed.

## Rollback

Runtime object mutations end with process. Filesystem rollback:
**[Needs confirmation]**.
