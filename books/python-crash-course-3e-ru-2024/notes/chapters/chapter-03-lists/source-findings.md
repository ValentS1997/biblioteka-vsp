# Source findings — глава 3

Этот файл фиксирует дефекты RAG-представления, обнаруженные при RAG-only cross-check. Канонический EPUB и RAG не исправляются в рамках chapter workflow.

## Finding 1 — обрезанные начала chunks на границе разбиения

Classification: **[Source extraction issue]**

Provenance:

- book: `python-crash-course-3e-ru-2024`
- EPUB spine item: `12`
- locator: `OEBPS/Text/978544614112-9.xhtml`
- affected chunks observed: `e0012:c03`, `e0012:c05`, `e0012:c06`, `e0012:c08`

Observed fragments:

- `e0012:c03` начинается с фрагмента `олько способов...`;
- `e0012:c05` начинается с хвоста предыдущего вывода `da', 'yamaha'...`;
- `e0012:c06` начинается с фрагмента `дположим...`;
- `e0012:c08` начинается с хвоста выражения `les[-1])`.

Cross-check:

- предыдущие соседние chunks содержат контекст/полные конструкции, необходимые для восстановления смысла главы;
- chapter boundary не затронута;
- упражнения и резюме доступны полностью;
- семантическая потеря материала главы при последовательном чтении диапазона `c01–c08` не выявлена.

Adjudication: проблема выглядит как chunk-boundary clipping/overlap artifact текущего legacy RAG. Точная причина на уровне extractor/chunker: `[Needs confirmation]`.

Policy action:

- не перестраивать legacy RAG только ради chapter artifact;
- не исправлять chunk text молча;
- при будущем controlled RAG rebuild проверить, исчезает ли clipping и сохраняется ли полный source-unit coverage.
