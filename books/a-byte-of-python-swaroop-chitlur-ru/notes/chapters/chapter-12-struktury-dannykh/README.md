# Глава 12. Структуры данных

Status: `RAG_GROUNDED`

Book: `a-byte-of-python-swaroop-chitlur-ru`

## Scope

Глава 12 — «Структуры данных». Она вводит четыре встроенные структуры данных,
названные источником: список, кортеж, словарь и множество. Затем объединяет списки,
кортежи и строки понятием последовательности, разбирает ссылки/копирование и
показывает дополнительные методы строк.

Разделы, подтверждённые RAG:

- 12.1 Список
- 12.2 Краткое введение в объекты и классы
- 12.3 Кортеж
- 12.4 Словарь
- 12.5 Последовательности
- 12.6 Множество
- 12.7 Ссылки
- 12.8 Ещё о строках
- 12.9 Резюме

## Provenance

- source format: PDF
- source SHA-256: `ac1abb7761fccb914988a583b4362c1760bafc3489c34f3f1fdb4ba45a0d7db5`
- RAG chunks: `p0087:c01` — `p0098:c01`
- PDF pages: 87–98
- printed pages visible in chapter: 79–90
- chapter start: PDF page 87, heading «Структуры данных»
- chapter end: PDF page 98, section 12.9 «Резюме»
- next chapter boundary: PDF page 99 begins «Решение задач»
- boundary verified: yes

## Main principle

Структуры данных позволяют хранить связанные значения и выбирать способ организации
по требуемому поведению:

- `list` — ordered mutable sequence в source framing;
- `tuple` — immutable sequence;
- `dict` — key/value mapping;
- `set` — unordered collection where membership matters more than order;
- list/tuple/string share sequence operations such as indexing and slicing;
- assignment may bind two names to the same mutable object, while a full slice is shown
  as a way to copy a list-like sequence.

## Chapter map

| Section | Source-grounded concept |
|---|---|
| 12.1 | Lists: square brackets, mutable elements, `append`, `sort`, indexing, `del`. |
| 12.2 | Objects/classes: methods and fields accessed through dotted notation. |
| 12.3 | Tuples: immutable sequence, optional parentheses, nested tuple behavior, singleton comma. |
| 12.4 | Dictionaries: key/value pairs, indexing by key, `del`, `items()`, membership and adding entries. |
| 12.5 | Sequences: membership, indexing, negative indices, slicing and slicing step. |
| 12.6 | Sets: membership, copy/add/remove, superset and intersection examples. |
| 12.7 | References: assignment can create two names for the same object; full slice demonstrates a separate list copy. |
| 12.8 | String methods: `startswith`, `in`, `find`, `join`. |
| 12.9 | Built-in data structures are framed as foundational for larger programs. |

## Core examples

### List

```python
shoplist = ['яблоки', 'манго', 'морковь', 'бананы']
shoplist.append('рис')
shoplist.sort()
del shoplist[0]
```

### Tuple

```python
zoo = ('питон', 'слон', 'пингвин')
new_zoo = 'обезьяна', 'верблюд', zoo
singleton = (2,)
```

### Dictionary

```python
ab = {
    'Swaroop': 'swaroop@swaroopch.com',
    'Larry': 'larry@wall.org',
    'Matsumoto': 'matz@ruby-lang.org',
    'Spammer': 'spammer@hotmail.com'
}

del ab['Spammer']
ab['Guido'] = 'guido@python.org'
```

### Sequence slicing

```python
shoplist[1:3]
shoplist[:]
shoplist[:-1]
shoplist[::2]
shoplist[::-1]
```

### Set

```python
bri = set(['Бразилия', 'Россия', 'Индия'])
bric = bri.copy()
bric.add('Китай')
bri.remove('Россия')
bri & bric
```

### References / copy

```python
mylist = shoplist
mylist = shoplist[:]
```

## Operational acceptance

После главы читатель должен уметь:

- выбрать list/tuple/dict/set по source-described behavior;
- различать mutable list и immutable tuple/string;
- выполнять indexing и slicing, включая negative indices и step;
- добавлять/удалять list/dict/set elements на source examples;
- объяснить aliasing в `mylist = shoplist`;
- объяснить source copy example `mylist = shoplist[:]`;
- использовать `startswith`, membership, `find` и `join`.

## Safety / integrity boundary

- `append`, `sort`, `del`, dict assignment, set `add/remove` меняют runtime
  objects; это state-changing operations внутри процесса.
- Сохранение example files меняет filesystem state; source rollback не задан.
- `dict.items()` description, dictionary-key rule and dictionary ordering wording
  сохраняются как historical source claims; current semantics не проверяются.
- Set source explicitly says unordered, поэтому shown REPL representation не используется
  как guarantee of element order.
- Source recommendation про full slice как способ копирования «сложного объекта»
  сохраняется только в контексте приведённого sequence/list example.

## Conditional artifacts

Раздел 12.9 — явное chapter-end «Резюме», поэтому создан `summary.md`.

Review/control questions в границе главы отсутствуют, поэтому
`review-questions.md` и `review-answers.md` не создаются.
