# Глава 8. Операторы и выражения

Status: `RAG_GROUNDED`

Book: `a-byte-of-python-swaroop-chitlur-ru`

## Scope

Глава 8 — «Операторы и выражения». Она вводит операторы и операнды, перечисляет
арифметические, битовые, сравнительные и логические операторы, показывает краткие
формы присваивания, объясняет приоритет и ассоциативность, а затем применяет выражения
в программе `expression.py`.

Разделы, подтверждённые RAG:

- 8.1 Операторы
  - 8.1.1 Краткая запись мат. операций и присваивания
- 8.2 Порядок вычисления
- 8.3 Изменение порядка вычисления
- 8.4 Ассоциативность
- 8.5 Выражения
- 8.6 Резюме

## Provenance

- source format: PDF
- source SHA-256: `ac1abb7761fccb914988a583b4362c1760bafc3489c34f3f1fdb4ba45a0d7db5`
- RAG chunks: `p0053:c01` — `p0058:c01`
- PDF pages: 53–58
- printed pages visible in chapter: 45–50
- chapter start: PDF page 53, heading «Операторы и выражения»
- chapter end: PDF page 58, section 8.6 «Резюме»
- next chapter boundary: PDF page 59 begins «Поток команд»
- boundary verified: yes

## Main principle

Выражение состоит из операторов и операндов. Результат вычисления зависит не только
от самих операторов, но и от их приоритета, ассоциативности и явной группировки
скобками. Источник рекомендует использовать скобки там, где они делают порядок
вычисления очевиднее и код легче читать.

## Chapter map

| Section | Source-grounded concept |
|---|---|
| 8.1 | Arithmetic, power, division, floor division, modulo, shifts, bitwise, comparisons, logical operators. |
| 8.1.1 | Augmented assignment: `a = a * 3` → `a *= 3`. |
| 8.2 | Operator precedence from lower to higher binding strength. |
| 8.3 | Parentheses improve readability and can alter evaluation order. |
| 8.4 | Equal-precedence operators are generally described as left-to-right; assignment is given as a right-to-left example. |
| 8.5 | Rectangle area/perimeter example using variables and expressions. |
| 8.6 | Operators, operands and expressions are framed as core program building blocks. |

## Operator groups in source

- arithmetic: `+`, `-`, `*`, `**`, `/`, `//`, `%`;
- bitwise: `<<`, `>>`, `&`, `|`, `^`, `~`;
- comparisons: `<`, `>`, `<=`, `>=`, `==`, `!=`;
- logical: `not`, `and`, `or`.

Source also introduces chained comparisons and short-circuit evaluation for `and` /
`or`.

## Core examples

Interactive expressions:

```python
2 + 3
3 * 5
```

Augmented assignment:

```python
a = 2
a *= 3
```

Parentheses:

```python
2 + (3 * 4)
(2 + 3) * 4
```

`expression.py`:

```python
length = 5
breadth = 2

area = length * breadth
print('Площадь равна', area)
print('Периметр равен', 2 * (length + breadth))
```

Source output:

```text
Площадь равна 10
Периметр равен 14
```

## Operational acceptance

После главы читатель должен уметь:

- разделить выражение на operators и operands;
- объяснить разницу `/`, `//`, `%`;
- распознавать comparison/logical operators;
- объяснить short-circuit behavior в source framing;
- переписать source pattern `variable = variable op expression` в augmented assignment;
- использовать precedence table и parentheses;
- предсказать результат `expression.py`.

## Limitations

- Глава содержит исторические/учебные claims о поведении операторов; они не проверяются
  внешними источниками в режиме `rag_only`.
- В таблице сравнений есть source statement о сравнении non-number operands, которое
  сохранено как source claim без внешней коррекции.
- В 8.4 запись `a = (b = c)` дана как объяснение right-to-left associativity; она
  сохранена как source wording/code issue, а не переписана.
- В translator footnote для `False` присутствует повреждённое слово; см.
  `source-findings.md`.

## Conditional artifacts

Раздел 8.6 — явное chapter-end «Резюме», поэтому создан `summary.md`.

Review/control questions в границе главы отсутствуют, поэтому
`review-questions.md` и `review-answers.md` не создаются.
