# Source findings — глава 11

## Finding 1 — assertIn() vs pytest assert syntax

Classification: **[Source terminology/code mismatch]**

Provenance:

- chunk: `e0020:c08`
- EPUB spine item: `20`
- locator: `OEBPS/Text/978544614112-17.xhtml`

Source prose говорит, что `assertIn()` проверяет наличие ответа в списке.

Shown pytest code:

~~~python
assert 'English' in language_survey.responses
~~~

В этой главе отдельный `assertIn()` API не определяется.

Adjudication: `[Needs confirmation]`.

Policy action: operational artifacts используют shown pytest syntax и сохраняют prose mismatch отдельно.

## Finding 2 — TestAnonymousSurvey vs top-level test functions

Classification: **[Source structure mismatch]**

Provenance:

- chunks: `e0020:c08–c09`

Prose сообщает, что второй test method добавляется в `TestAnonymousSurvey`.

Однако shown code определяет:

~~~python
def test_store_single_response():
    ...

def test_store_three_responses():
    ...
~~~

То есть test class `TestAnonymousSurvey` в показанном pytest example отсутствует.

Adjudication: `[Needs confirmation]`.

Policy action: canonical RAG не исправлять.

## Finding 3 — exercise 11.3 setUp() vs chapter pytest fixtures

Classification: **[Source exercise/process mismatch]**

Provenance:

- chunk: `e0020:c10`

Exercise 11.3 требует использовать `setUp()` и говорит о test methods.

Непосредственно перед exercise глава обучает:
- pytest;
- top-level test functions;
- reusable setup через `@pytest.fixture`.

Mechanism `setUp()` в source material главы не определён и example его не показывает.

Adjudication: intended testing framework/process `[Needs confirmation]`.

Policy action: не подменять `setUp()` fixture-ом молча. В review answer разделить source-supported behavior и unsupported setup mechanism.

## Finding 4 — exercise 11.1 parameter-order wording

Classification: **[Source wording/example mismatch]**

Provenance:

- chunk: `e0020:c06`

Prose сначала говорит, что функция получает «название страны и название города».

Но expected output — `Santiago, Chile`, а test example предлагает values `'santiago'` и `'chile'`, что естественно соответствует order `city, country`.

Exact intended parameter order: `[Needs confirmation]`.

Policy action: в answer явно указать выбранную interpretation.

## Finding 5 — chunk-boundary clipping / overlap

Classification: **[Source extraction issue]**

Provenance:

- affected starts observed: `e0020:c02`–`e0020:c11`
- EPUB spine item: `20`
- locator: `OEBPS/Text/978544614112-17.xhtml`

Observed starts include continuation fragments such as `ду для обновления...`, `пешно работает...`, `у, в которой...`, `() missing...`, `ботает для имен...`, `т правильно...`, `опроса...`, `y...`, `nguage_survey...`, `еагировать...`.

Cross-check:

- adjacent preceding chunks preserve transition context;
- exercises 11.1–11.3 are recoverable;
- summary is intact;
- `e0021:c01` confirms transition to Part II;
- no chapter-level semantic loss was detected.

Adjudication: extractor/chunker root cause `[Needs confirmation]`.

Policy action: retain legacy RAG unchanged until separately justified controlled rebuild.
