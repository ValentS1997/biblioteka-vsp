# Source findings — глава 6

## Finding 1 — некавыченное значение speed

Classification: **[Source code mismatch]**

Provenance:

- chunk: `e0015:c03`
- EPUB spine item: `15`
- locator: `OEBPS/Text/978544614112-12.xhtml`

Source context ранее определяет:

~~~python
alien_0 = {'x_position': 0, 'y_position': 25, 'speed': 'medium'}
~~~

и сравнивает `speed` со строками `'slow'` и `'medium'`.

Затем источник показывает строку:

~~~python
alien_0['speed'] = fast
~~~

без кавычек вокруг `fast`.

Adjudication: `[Needs confirmation]`.

Policy action: не исправлять строку молча; в chapter explanation не использовать её как нормализованный executable example.

## Finding 2 — Edward: dictionary vs output

Classification: **[Source code mismatch]**

Provenance:

- chunk: `e0015:c10`
- EPUB spine item: `15`
- locator: `OEBPS/Text/978544614112-12.xhtml`

Source dictionary:

~~~python
'edward': ['rust', 'go']
~~~

Показанный далее source output:

~~~text
Edward's favorite languages are:
    Ruby
    Go
~~~

Variants disagree on the first language.

Adjudication: `[Needs confirmation]`.

Policy action: сохранить обе версии; не выбирать правильную на основе model memory или внешних источников.

## Finding 3 — chunk-boundary clipping / overlap

Classification: **[Source extraction issue]**

Provenance:

- affected starts observed: `e0015:c02`–`e0015:c12`
- spine item: `15`
- locator: `OEBPS/Text/978544614112-12.xhtml`

Examples include partial/continuation starts such as `nt(f"...`, `s green.`, `кольких строк...`, `чение None...`, `ля таких...`, `ние:`, `языка...`, `'points':...`, `ые словари...`, `ages are:`, `мени владельца...`.

Cross-check:

- preceding chunks preserve the relevant transition context;
- exercises 6.1–6.12 remain recoverable;
- chapter-end summary is intact;
- `e0016:c01` independently confirms the next chapter;
- no chapter-level semantic loss was detected.

Adjudication: extractor/chunker root cause `[Needs confirmation]`.

Policy action: retain legacy RAG until a separately justified controlled rebuild.
