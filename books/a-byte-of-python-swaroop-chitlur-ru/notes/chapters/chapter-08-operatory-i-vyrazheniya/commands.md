# Commands and code — глава 8 «Операторы и выражения»

## Execution commands

| Command | Classification | Source role | Verification | Rollback |
|---|---|---|---|---|
| interactive `2 + 3` | workload-generating | проверка expression в REPL | source result `5` | [Not applicable] |
| interactive `3 * 5` | workload-generating | проверка expression в REPL | source result `15` | [Not applicable] |
| `python expression.py` | workload-generating | запускает section 8.5 example | area/perimeter output | [Not applicable] |

## Operator examples from source

```python
3 + 5
50 - 24
2 * 3
3 ** 4
4 / 3
4 // 3
8 % 3
2 << 2
11 >> 1
5 & 3
5 | 3
5 ^ 3
~5
```

## Comparison / logical examples

```python
3 < 5 < 7
x <= y
x >= 3
x == y
x != y
not x
x and y
x or y
```

Source describes short-circuit evaluation for `and` and `or`.

## Augmented assignment

Source transformation:

```python
a = 2
a = a * 3
```

to:

```python
a = 2
a *= 3
```

## Evaluation order

```python
2 + 3 * 4
2 + (3 * 4)
(2 + 3) * 4
```

Source recommendation: use parentheses where they clarify intended order.

## expression.py

```python
length = 5
breadth = 2

area = length * breadth
print('Площадь равна', area)
print('Периметр равен', 2 * (length + breadth))
```

Expected source output:

```text
Площадь равна 10
Периметр равен 14
```

## Source integrity boundary

Do not silently rewrite source claims or examples where semantics look questionable.
Specifically, see `source-findings.md` for the comparison-table claim and the
associativity notation `a = (b = c)`.
