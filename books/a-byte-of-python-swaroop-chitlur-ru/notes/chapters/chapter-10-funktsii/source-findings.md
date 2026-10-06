# Source findings — глава 10 «Функции»

Mode: `rag_only`

## Finding 1 — func_default.py indentation/output mismatch

Classification: **[Source wording/code mismatch]**

Provenance: `a-byte-of-python-swaroop-chitlur-ru:p0072:c01`, PDF page 72,
section 10.5.

RAG/source variant:

```python
def say(message, times = 1):
    print(message * times)

    say('Привет')
    say('Мир', 5)
```

Displayed output:

```text
Привет
МирМирМирМирМир
```

Issue: the two calls are extracted/displayed with indentation inside the function body,
which conflicts with the ordinary interpretation of the shown output.

Action: preserve the source variant. Do not silently dedent or repair it in canonical
artifacts.

## Finding 2 — default-value immutability claim

Classification: **[Source technical claim / Needs confirmation]**

Provenance: `p0071:c01`, section 10.5.

Source statement:

`значение по умолчанию должно быть константой. Или точнее говоря, оно должно быть неизменным`

Issue: this is a strong rule statement whose current Python semantics are not established
inside the RAG-only workflow.

Action: retain as source teaching statement only; do not upgrade it to externally verified
current guidance.

## Finding 3 — func_global.py output typo

Classification: **[Source wording/code mismatch]**

Provenance: `p0070:c01`, section 10.3.

Code string:

`print('Значение x составляет', x)`

Displayed output:

`Знчение x составляет 2`

Issue: output is missing the letter `а` in `Значение`.

Action: preserve both variants.

## Finding 4 — keyword-only TypeError wording

Classification: **[Needs confirmation]**

Provenance: `p0074:c01`, section 10.8.

Source output:

`TypeError: total() needs keyword-only argument extra_number`

Issue: exact exception wording is version/runtime specific; current wording is not
verified in this workflow.

Action: preserve as historical source output.

## Finding 5 — shebang/interpreter variant

Classification: **[Source wording/code mismatch]**

Provenance: `p0075:c01`, section 10.9.

Source shebang:

`#!/usr/bin/python`

Execution examples throughout this chapter also use `python <file>.py`.

Issue: the book elsewhere is framed around Python 3, but this chapter's executable
variants use `python` / `/usr/bin/python`.

Action: preserve the source variants; do not normalize them to `python3`.
