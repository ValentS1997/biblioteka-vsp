# Source findings — глава 6

Canonical evidence: book `computer-networks-olifer-7e-ru-2026`, PDF pp. 183–214; source SHA-256 `16f4b02985f65c602c6268620878cbacd692a61fd5898ca811b3d1a332e3f84d`. Policy: `rag_only`.

## F-01 — [Source extraction issue] Повторяющийся посторонний footer/URL

Во множестве chunks присутствует строка `Книги для программистов: https://t.me/free_books_for_it`, иногда слитая с основной строкой или caption.

**Решение:** footer не считается содержанием книги и не переносится в artifacts.

## F-02 — [Source extraction issue] Математические символы и единицы местами деградированы

Fourier formulas, frequency/wavelength notation, logarithms, SNR and optical-dispersion units содержат OCR/glyph substitutions. На `p0197:c01` примеры единиц мощности извлечены подозрительно (например, буквы единиц выглядят как voltage units в контексте power).

**Решение:** artifacts сохраняют только однозначно поддерживаемые relations/units; подозрительные literal examples не нормализуются молча.

## F-03 — [Source inconsistency / convention] Знак attenuation используется неоднородно

- `p0194:c01` определяет attenuation как `10 lg(Pout/Pin)`, что для passive loss даёт отрицательное значение; `p0195:c01` отдельно подчёркивает отрицательный знак.
- В link-budget example `p0197:c01` используется запись, где `A` фактически ведёт себя как положительная magnitude loss в соотношении `A = x - y`.

**Решение:** chapter artifacts не фиксируют одну из этих conventions как универсальную. В практических расчётах нужно явно указать: signed gain/loss или positive loss magnitude.

## F-04 — [Source extraction issue] Figures/spectra are not multimodal RAG objects

Глава опирается на временные/частотные графики, spectra, attenuation curves, cable cross-sections and SCS hierarchy. RAG сохраняет captions/labels, но пространственная структура частично теряется.

**Решение:** Mermaid/SVG — новая source-grounded synthesis, не копия original figures.

## F-05 — [Needs confirmation] Cable/fiber numeric values are source snapshots

Категории витой пары, distances/frequencies, attenuation windows, fiber reach/rates and standard identifiers даны как технические примеры/состояние источника.

**Решение:** не использовать их как current deployment limits без проверки конкретной версии стандарта, transceiver/cable datasheet and environment.

## F-06 — [Needs confirmation] Theoretical limits are not deployment guarantees

Shannon/Nyquist relations задают theoretical boundaries under model assumptions. Они не определяют автоматически negotiated PHY rate, required BER, coding overhead, FEC or implementation margin.

**Решение:** production acceptance требует конкретного physical standard and measurements.
