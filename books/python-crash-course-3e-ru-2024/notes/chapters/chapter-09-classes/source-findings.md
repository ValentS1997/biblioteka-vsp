# Source findings — глава 9

## Finding 1 — self.make vs self.manufacturer

Classification: **[Source code mismatch]**

Provenance:

- chunk: `e0018:c11`
- EPUB spine item: `18`
- locator: `OEBPS/Text/978544614112-15.xhtml`

Source `Car.__init__()` сохраняет:

~~~python
self.make = make
~~~

Но `get_descriptive_name()` использует:

~~~python
long_name = f"{self.year} {self.manufacturer} {self.model}"
~~~

Атрибут `self.manufacturer` в показанном class code не создаётся.

Adjudication: `[Needs confirmation]`.

Policy action: не исправлять canonical source молча; в instructional code использовать только внутренне согласованные examples либо явно ссылаться на finding.

## Finding 2 — повреждённая docstring в inheritance example

Classification: **[Source code/extraction mismatch]**

Provenance:

- chunk: `e0018:c07`
- EPUB spine item: `18`
- locator: `OEBPS/Text/978544614112-15.xhtml`

В RAG показано:

~~~python
"""Инициализирует атрибуты описания автомобиля.""
~~~

Закрывающая последовательность содержит две кавычки вместо трёх.

Adjudication: является ли это дефектом source markup или extraction — `[Needs confirmation]`.

Policy action: canonical RAG не исправлять.

## Finding 3 — get_range(): code vs shown output

Classification: **[Source code/output mismatch]**

Provenance:

- chunks: `e0018:c09`, `e0018:c12`
- EPUB spine item: `18`
- locator: `OEBPS/Text/978544614112-15.xhtml`

Source code:

~~~python
print(f"This car can go about {range} miles on a full charge.")
~~~

Shown output:

~~~text
This car can go approximately 150 miles on a full charge.
~~~

Wording differs: `about` vs `approximately`.

Adjudication: `[Needs confirmation]`.

Policy action: не использовать shown output как буквальную проверку строки, если выполняется именно показанный code.

## Finding 4 — chunk-boundary clipping / overlap

Classification: **[Source extraction issue]**

Provenance:

- affected starts observed: `e0018:c02`–`e0018:c15`
- EPUB spine item: `18`
- locator: `OEBPS/Text/978544614112-15.xhtml`

Observed starts include partial continuations such as `ачала мы определили...`, `писан в предыдущем...`, `жнения 9.1...`, `4)`, `казания одометра...`, `фических для электромобилей...`, `са нередко...`, `запас равен...`, `е классов...`, `лектродвигателем...`, `але файла...`.

Cross-check:

- preceding chunks preserve transition context;
- exercises 9.1–9.16 remain recoverable;
- chapter-end summary is intact;
- `e0019:c01` confirms chapter 10;
- no chapter-level semantic loss was detected.

Adjudication: extractor/chunker root cause `[Needs confirmation]`.

Policy action: keep legacy RAG unchanged until a separately justified controlled rebuild.
