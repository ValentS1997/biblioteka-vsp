# Source findings — глава 7

## Finding 1 — порядок вывода mountain_poll.py

Classification: **[Source code/output mismatch]**

Provenance:

- chunk: `e0016:c08`
- EPUB spine item: `16`
- locator: `OEBPS/Text/978544614112-13.xhtml`

Source interaction сначала вводит:

1. Eric → Denali
2. Lynn → Devil's Thumb

Код сохраняет ответы:

~~~python
responses[name] = response
~~~

и затем перебирает:

~~~python
for name, response in responses.items():
    print(f"{name} would like to climb {response}.")
~~~

Однако показанный source output перечисляет:

~~~text
Lynn would like to climb Devil's Thumb.
Eric would like to climb Denali.
~~~

Ранее в книге, в главе 6, source прямо утверждает, что словари сохраняют порядок добавления пар «ключ — значение». Поэтому показанный порядок вывода не согласуется с описанной source model.

Adjudication: `[Needs confirmation]`.

Policy action: не переставлять source output молча; в chapter artifacts не использовать этот вывод как доказательство порядка словаря.

## Finding 2 — chunk-boundary clipping / overlap

Classification: **[Source extraction issue]**

Provenance:

- affected starts observed: `e0016:c02`–`e0016:c09`
- EPUB spine item: `16`
- locator: `OEBPS/Text/978544614112-13.xhtml`

Observed continuation starts include `me, we can personalize...`, `апример...`, `м выполнении...`, `т называться...`, `ng.py`, `ограмма получала...`, `ном экземпляре...`, `ом, что...`.

Cross-check:

- preceding chunks preserve transition context;
- exercises 7.1–7.10 are recoverable;
- chapter-end summary is intact;
- `e0017:c01` confirms the next chapter;
- no chapter-level semantic loss was detected.

Adjudication: extractor/chunker root cause `[Needs confirmation]`.

Policy action: keep legacy RAG unchanged until a separately justified controlled rebuild.
