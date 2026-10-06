# Commands and code — глава 12 «Структуры данных»

## Execution commands

| Command | Classification | Source role | Verification | Rollback |
|---|---|---|---|---|
| `python3 using_list.py` | workload-generating | list mutation example | source list output | [Not applicable] |
| `help(list)` | read-only | inspect list methods | help text | [Not applicable] |
| `python3 using_tuple.py` | workload-generating | tuple/nesting example | source counts/output | [Not applicable] |
| `python3 using_dict.py` | workload-generating | dictionary mutation/iteration | source address-book output | [Not applicable] |
| `help(dict)` | read-only | inspect dict methods | help text | [Not applicable] |
| `python3 seq.py` | workload-generating | indexing/slicing | source slice output | [Not applicable] |
| set REPL snippets | workload-generating / runtime mutation | set operations | Boolean/set results | process-local |
| `python3 reference.py` | workload-generating | alias vs slice-copy example | two list pairs differ as shown | [Not applicable] |
| `help(str)` | read-only | inspect string methods | help text | [Not applicable] |
| `python3 str_methods.py` | workload-generating | string methods | source string output | [Not applicable] |

## List operations

```python
shoplist.append('рис')
shoplist.sort()
del shoplist[0]
```

Classification: state-changing runtime mutations.

Source explicitly says `sort()` acts on the list itself rather than returning a changed
version.

## Tuple operations

```python
zoo = ('питон', 'слон', 'пингвин')
new_zoo = 'обезьяна', 'верблюд', zoo
new_zoo[2][2]
singleton = (2,)
```

Classification: workload/read operations on immutable tuple values.

## Dictionary operations

```python
del ab['Spammer']

for name, address in ab.items():
    print('Контакт {0} с адресом {1}'.format(name, address))

ab['Guido'] = 'guido@python.org'

if 'Guido' in ab:
    print(ab['Guido'])
```

`del` and assignment are state-changing runtime mutations.

## Sequence indexing / slicing

```python
shoplist[0]
shoplist[-1]
shoplist[1:3]
shoplist[2:]
shoplist[1:-1]
shoplist[:]
shoplist[:-1]
shoplist[::2]
shoplist[::-1]
```

Source rule: start included, end excluded.

## Set REPL

```python
bri = set(['Бразилия', 'Россия', 'Индия'])
'Индия' in bri
'США' in bri
bric = bri.copy()
bric.add('Китай')
bric.issuperset(bri)
bri.remove('Россия')
bri & bric
```

`add` and `remove` mutate set objects.

## References

```python
mylist = shoplist
del shoplist[0]

mylist = shoplist[:]
del mylist[0]
```

The first assignment aliases the same object in source explanation; full slice is used
to produce an independent list copy in the example.

## String methods

```python
name.startswith('Swa')
'a' in name
name.find('war')
delimiter.join(mylist)
```

## Source integrity boundary

Do not promote historical dict/set/copy wording into current verified Python guarantees.
See `source-findings.md`.
