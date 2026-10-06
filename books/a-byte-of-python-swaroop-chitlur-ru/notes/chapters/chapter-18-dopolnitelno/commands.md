# Commands and code — глава 18 «Дополнительно»

## Execution / REPL examples

| Command / snippet | Classification | Source role | Verification | Rollback |
|---|---|---|---|---|
| tuple-unpacking REPL | runtime/read-write bindings | multiple return values | values unpacked | process-local |
| `python3 lambda.py` | workload-generating / list mutation | lambda sort key | source sorted output | [Not applicable] |
| `python3 list_comprehension.py` | workload-generating | new-list construction | `[6, 8]` | [Not applicable] |
| `exec('print("Здравствуй, Мир!")')` | code execution | execute source text | greeting printed | payload-dependent |
| `eval('2*3')` | expression execution | evaluate source expression | `6` | payload-dependent |
| `assert len(mylist) >= 1` | runtime invariant check | raise on false | source `AssertionError` | [Not applicable] |
| `repr(i)` | read-only representation | object representation | source string form | [Not applicable] |
| `eval(repr(i))` | expression execution | source round-trip example | shown list restored | payload-dependent |

## Tuple unpacking / swap

```python
errnum, errstr = get_error_details()
a, *b = [1, 2, 3, 4]

a = 5
b = 8
a, b = b, a
```

## Special methods listed by source

```text
__init__(self, ...)
__del__(self)
__str__(self)
__lt__(self, other)
__getitem__(self, key)
__len__(self)
```

The RAG table has extraction corruption in several `self` occurrences; see
`source-findings.md`.

## Single-line block

```python
flag = True
if flag: print('Да')
```

Source explicitly recommends avoiding this style except limited checking situations.

## Lambda

```python
points.sort(key=lambda i: i['y'])
```

## List comprehension

```python
listtwo = [2*i for i in listone if i > 2]
```

Source notes that `listone` is not changed.

## Variable arguments

```python
def powersum(power, *args):
    ...
```

Source explanation also covers `**` for additional key/value parameters.

## exec / eval — execution boundary

```python
exec('print("Здравствуй, Мир!")')
eval('2*3')
```

Only fixed chapter strings are canonical examples.

Do not pass unverified external/user/runtime strings into these examples as part of this
chapter workflow.

## assert

```python
mylist = ['item']
assert len(mylist) >= 1
mylist.pop()
assert len(mylist) >= 1
```

Final assert produces source `AssertionError`.

## repr

```python
i = []
i.append('item')
repr(i)
eval(repr(i))
eval(repr(i)) == i
```

The broad source statement about `eval(repr(object)) == object` is not promoted beyond
the demonstrated list example.

## Escape / raw strings

```python
'What\'s your name?'
"What's your name?"
"Это первая строка\nЭто вторая строка"
"\t"
r"Перевод строки обозначается \n"
```

Source also recommends raw strings for regular expressions.
