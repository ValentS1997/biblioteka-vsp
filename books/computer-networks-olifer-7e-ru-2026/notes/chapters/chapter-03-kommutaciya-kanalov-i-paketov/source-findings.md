# Source findings — глава 3

Canonical evidence: book `computer-networks-olifer-7e-ru-2026`, PDF pp. 81–107; source SHA-256 `16f4b02985f65c602c6268620878cbacd692a61fd5898ca811b3d1a332e3f84d`. Policy: `rag_only`.

## F-01 — [Source extraction issue] Повторяющийся посторонний footer/URL

Во многих chunks главы в конец извлечённого текста попадает строка `Книги для программистов: https://t.me/free_books_for_it`, иногда слитая с основной строкой.

Примеры: `p0083:c01`, `p0084:c01`, `p0085:c01`, `p0086:c01`, `p0087:c01`, `p0088:c01`, `p0089:c01`, `p0090:c01`, `p0091:c01`, `p0092:c01`, `p0093:c01`, `p0094:c01`, `p0095:c01`, `p0096:c01`, `p0097:c01`, `p0098:c01`, `p0099:c01`, `p0100:c01`, `p0101:c01`, `p0102:c01`, `p0103:c01`, `p0104:c01`, `p0105:c01`, `p0106:c01`, `p0107:c01`.

**Решение:** footer не считается содержанием главы и не переносится в canonical artifacts.

## F-02 — [Source extraction issue] OCR/glyph substitutions

Примеры подтверждённых искажений:

- `p0088:c01`: заголовок извлечён как «Глава З» вместо типографически ожидаемой цифры;
- `p0090:c01` и соседние chunks: смешанные glyphs в словах/терминах;
- `p0094:c01`: некоторые подписи и таблица содержат substitution/line-layout noise;
- `p0098:c01`: `датаграммный` и названия технологий извлечены с glyph substitutions;
- `p0106:c01`–`p0107:c01`: `Ethernet` местами содержит смешанные кириллические/латинские символы.

**Решение:** однозначно распознаваемые термины нормализуются в artifacts; повреждённые строки не цитируются как точный source text.

## F-03 — [Source extraction issue] Формулы и индексы частично деградированы

В разделе структуры задержек `p0101:c01`–`p0105:c01` математические индексы, обозначения (t_i), (T), (N_1), (S_1) и некоторые формулы местами извлекаются неоднозначно или с переставленными glyphs.

**Решение:** artifacts сохраняют source-supported decomposition delay components и явно читаемые формулы уровня `tprg=L/S`, `ttrns=V/C`, но не реконструируют повреждённые индексы из памяти. Для точной посимвольной формулы: **[Needs confirmation]** при текущем `rag_only` режиме.

## F-04 — [Source extraction issue] Рисунки и таблицы не являются multimodal RAG objects

Глава использует рис. 3.1–3.16 и таблицы 3.1–3.3. RAG сохраняет captions и часть labels, но не самостоятельные изображения.

**Решение:** Mermaid/SVG в chapter artifacts — новые source-grounded схемы, а не копии оригинальных рисунков. Точная визуальная реконструкция original figures: **[Needs confirmation]**.

## F-05 — [Needs confirmation] Учебный quantitative example не является measurement реальной сети

`p0104:c01`–`p0105:c01` приводит конкретный расчёт задержек для заданных distance/message/rate/packet assumptions и получает 825 ms против 1856 ms в выбранном сценарии.

**Решение:** результат сохраняется как частный source example, а не как универсальный вывод «circuit switching всегда быстрее». Реальные latency/load/buffer/link parameters пользователя: **[Needs confirmation]**.
