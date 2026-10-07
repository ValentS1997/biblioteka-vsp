# Source findings — глава 4

Canonical evidence: book `computer-networks-olifer-7e-ru-2026`, PDF pp. 108–130; source SHA-256 `16f4b02985f65c602c6268620878cbacd692a61fd5898ca811b3d1a332e3f84d`. Policy: `rag_only`.

## F-01 — [Source extraction issue] Повторяющийся посторонний footer/URL

Во многих chunks в конец текста попадает строка `Книги для программистов: https://t.me/free_books_for_it`, иногда слитая с последним словом или подписью рисунка.

Примеры: `p0109:c01`, `p0110:c01`, `p0112:c01`, `p0113:c01`, `p0114:c01`, `p0115:c01`, `p0116:c01`, `p0117:c01`, `p0118:c02`, `p0119:c01`, `p0120:c01`, `p0121:c01`, `p0122:c01`, `p0123:c01`, `p0124:c01`, `p0125:c02`, `p0126:c01`, `p0127:c01`, `p0128:c01`, `p0129:c01`, `p0130:c01`.

**Решение:** footer не считается содержанием книги и не переносится в canonical artifacts.

## F-02 — [Source extraction issue] OCR/glyph substitutions

В RAG встречаются смешанные кириллические/латинские glyphs и искажённые слова/акронимы, в частности вокруг `TCP/IP`, `Ethernet`, `IP`, `OSI`, `RFC`, `Wi-Fi` и русских терминов.

**Решение:** только однозначно восстанавливаемые термины нормализуются типографически. Повреждённый текст не используется как точная цитата.

## F-03 — [Source extraction issue] Layer/stack diagrams извлечены как разрозненный текст

Рисунки 4.1–4.11 содержат иерархии, arrows, layer boxes и correspondence mappings. Text-layer RAG сохраняет captions и многие labels, но spatial relations частично теряются.

**Решение:** Mermaid/SVG — новая source-grounded synthesis по явному prose и labels, а не точная реконструкция original diagrams. Точное визуальное сопоставление с рисунками: **[Needs confirmation]**.

## F-04 — [Needs confirmation] Current-status claims сохранены как snapshot книги

Глава использует формулировки о текущем распространении technologies/standards и приводит организационные/количественные claims, например размер сообщества ISOC, распространённость protocol stacks и современное положение отдельных technologies.

**Решение:** в chapter artifacts это трактуется как source snapshot издания. Актуальный статус организаций, standards, protocol versions и adoption на текущую дату не проверяется из-за `rag_only` policy.

## F-05 — [Needs confirmation] Classification examples не являются inventory реальной инфраструктуры

LAN/WAN/MAN, carrier/corporate/personal, access/aggregation/backbone, primary/overlay и другие classes являются taxonomy source. Никакая конкретная пользовательская сеть в RAG главы не классифицирована.

**Решение:** применение taxonomy к реальной инфраструктуре требует topology/scope/ownership/role data: **[Needs confirmation]**.
