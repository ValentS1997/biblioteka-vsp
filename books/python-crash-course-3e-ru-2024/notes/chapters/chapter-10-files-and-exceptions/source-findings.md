# Source findings — глава 10

## Finding 1 — count_words() docstring vs implementation

Classification: **[Source documentation/code mismatch]**

Provenance:

- chunks: `e0019:c09–c10`
- EPUB spine item: `19`
- locator: `OEBPS/Text/978544614112-16.xhtml`

Функция называется `count_words()`, а implementation использует:

~~~python
words = contents.split()
num_words = len(words)
~~~

Но docstring в source:

~~~python
"""Подсчитывает приблизительное количество строк в файле."""
~~~

То есть documentation говорит о строках, implementation и surrounding prose — о словах.

Adjudication: `[Needs confirmation]`.

Policy action: canonical source не исправлять; instructional summary описывает фактический shown computation как approximate word count.

## Finding 2 — exercise 10.7 cross-reference

Classification: **[Source exercise-reference mismatch]**

Provenance:

- chunk: `e0019:c11`

Exercise 10.7 говорит: «Поместите код из упражнения 10.5 в цикл while», но 10.5 — guest book. Собственная формулировка 10.7 говорит о продолжении ввода чисел после text/number error, то есть продолжает непосредственно предшествующий `ValueError` scenario 10.6.

Adjudication: intended reference `[Needs confirmation]`.

Policy action: в review artifact сохранить source reference mismatch и не переписывать canonical text.

## Finding 3 — exercise 10.9 cross-reference

Classification: **[Source exercise-reference mismatch]**

Provenance:

- chunk: `e0019:c11`

Exercise 10.9 говорит изменить `except` из упражнения 10.7, чтобы при отсутствии файла программа молча продолжала работу. FileNotFoundError scenario находится в 10.8; 10.7 посвящено numeric calculator.

Adjudication: intended reference `[Needs confirmation]`.

Policy action: сохранить mismatch явно.

## Finding 4 — json.dumps() prose vs shown code

Classification: **[Source prose/code mismatch]**

Provenance:

- chunk: `e0019:c12`

Source prose утверждает, что `json.dumps()` получает два arguments: сохраняемые данные и file object.

Однако shown code:

~~~python
contents = json.dumps(numbers)
path.write_text(contents)
~~~

То есть в самом source JSON string сначала создаётся отдельно, а file write выполняет `Path.write_text()`.

Adjudication: `[Needs confirmation]`.

Policy action: не исправлять source statement на основании model memory; в operational artifact повторять только shown data flow.

## Finding 5 — chunk-boundary clipping / overlap

Classification: **[Source extraction issue]**

Provenance:

- affected starts observed: `e0019:c02`–`e0019:c15`
- EPUB spine item: `19`
- locator: `OEBPS/Text/978544614112-16.xhtml`

Observed starts include partial continuations such as `его новые данные...`, `s и заканчивается...`, `pi_string содержит...`, `льзоваться...`, `и именно так...`, `трассировки...`, `to quit...`, `, the file...`, `файл siddhartha...`, `каких-то файлов...`, `очти всегда...`, `обы сохранить его...`, `!")...`.

Cross-check:

- adjacent preceding chunks preserve transition context;
- exercises 10.1–10.14 remain recoverable;
- chapter-end summary is intact;
- `e0020:c01` confirms chapter 11;
- no chapter-level semantic loss was detected.

Adjudication: extractor/chunker root cause `[Needs confirmation]`.

Policy action: retain legacy RAG unchanged until separately justified controlled rebuild.
