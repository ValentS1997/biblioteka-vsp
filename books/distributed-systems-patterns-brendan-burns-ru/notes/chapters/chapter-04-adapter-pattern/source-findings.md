# Source findings — глава 4

Этот файл фиксирует source/RAG extraction-sensitive fragments без silent correction.

## Finding 1 — Go string literal line wrapping

Classification: `[Source extraction issue]`

Provenance:
- `distributed-systems-patterns-brendan-burns-ru:p0074:c01`

В RAG Go declaration для параметра database визуально разорвана переносом строки внутри quoted description.

Finding:
- PDF text-layer wrapping делает точную compile-ready форму строки ненадежной;
- смысл параметра понятен, но literal source formatting не восстанавливается по model memory.

Action:
- в chapter artifacts сохраняется semantic description параметра;
- полный Go block не объявляется compile-ready;
- exact source formatting: `[Needs confirmation]`.

## Finding 2 — YAML indentation sensitivity

Classification: `[Source extraction issue]`

Provenance:
- Redis/Prometheus Pod: `p0068:c01`
- MySQL health Pod: `p0075:c01–p0076:c01`

YAML извлечен из PDF text layer, где whitespace/indentation может быть изменен переносами.

Action:
- snippets используются для архитектурной структуры;
- не считать их production-copy-safe manifest без отдельной проверки;
- exact whitespace-safe form: `[Needs confirmation]`.

## Finding 3 — example credentials normalized in artifacts

Classification: `[Needs confirmation]`

Provenance:
- example invocation: `distributed-systems-patterns-brendan-burns-ru:p0075:c01`

Source содержит example username/password-like values в комментарии к `db-check`.

Repository safety rule требует не переносить credentials/secrets/environment-specific identifiers как reusable commands.

Action:
- `commands.md` заменяет значения на `<db-user>` и `<db-password>`;
- это deliberate safety normalization, а не исправление смысла source;
- исходные example values не используются как реальные credentials.
