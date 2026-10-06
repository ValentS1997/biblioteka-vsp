# Commands and code — глава 15 «Ввод-вывод»

## Execution / inspection commands

| Command / operation | Classification | Source role | Verification | Rollback |
|---|---|---|---|---|
| `help(str)` | read-only | inspect string methods such as `rjust` | help text | [Not applicable] |
| `python3 user_input.py` | workload-generating / interactive | palindrome input example | source yes/no output | [Not applicable] |
| `help(open)` | read-only | inspect file modes | help text | [Not applicable] |
| `python3 using_file.py` | state-changing / workload | writes and then reads `poem.txt` | poem output | [Needs confirmation] |
| `open('poem.txt', 'w')` | state-changing filesystem | text write | file contains poem | [Needs confirmation] |
| `f.readline()` | read-only file operation | line-by-line read | empty string ends loop | [Not applicable] |
| `python3 pickling.py` | state-changing / workload | writes and reloads `shoplist.data` | restored list output | [Needs confirmation] |
| `pickle.dump(shoplist, f)` | state-changing filesystem | binary serialization | later load succeeds | [Needs confirmation] |
| `pickle.load(f)` | read operation in source flow | restores object | list printed | [Not applicable] |
| `del shoplist` | state-changing runtime namespace | removes source name before reload | name removed in process | recreate/reassign |

## User input

```python
something = input('Введите текст: ')
```

Reverse:

```python
text[::-1]
```

Source homework asks to improve palindrome detection to ignore:

- punctuation;
- spaces;
- letter case.

The hint mentions a list of punctuation available “здесь”, but no URL is present in the
RAG chunk. Do not invent the missing reference.

## File write/read

```python
f = open('poem.txt', 'w')
f.write(poem)
f.close()

f = open('poem.txt')
while True:
    line = f.readline()
    if len(line) == 0:
        break
    print(line, end='')

f.close()
```

Source mode descriptions:

- `r` — reading;
- `w` — writing;
- `a` — appending;
- `t` — text;
- `b` — binary.

## Pickle

```python
f = open(shoplistfile, 'wb')
pickle.dump(shoplist, f)
f.close()

del shoplist

f = open(shoplistfile, 'rb')
storedlist = pickle.load(f)
print(storedlist)
```

Expected source output:

```text
['яблоки', 'манго', 'морковь']
```

## State-changing boundary

Do not run the file-writing examples against real files without confirming the target
paths and overwrite intent.

Source does not provide filesystem rollback commands.

Rollback: **[Needs confirmation]**.
