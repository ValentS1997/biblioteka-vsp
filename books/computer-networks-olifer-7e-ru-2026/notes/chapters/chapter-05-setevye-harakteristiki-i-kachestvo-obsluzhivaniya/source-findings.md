# Source findings — глава 5

Canonical evidence: book `computer-networks-olifer-7e-ru-2026`, PDF pp. 131–177; source SHA-256 `16f4b02985f65c602c6268620878cbacd692a61fd5898ca811b3d1a332e3f84d`. Policy: `rag_only`.

## F-01 — [Source extraction issue] Повторяющийся посторонний footer/URL

Во многих chunks главы присутствует строка `Книги для программистов: https://t.me/free_books_for_it`, иногда слитая с последним словом, formula label или caption.

Подтверждённые примеры среди просмотренных chunks: `p0132:c01`, `p0134:c01`, `p0135:c01`, `p0136:c01`, `p0139:c01`, `p0141:c01`, `p0142:c01`, `p0143:c01`, `p0144:c01`, `p0145:c01`, `p0146:c01`, `p0147:c01`, `p0148:c01`, `p0149:c01`, `p0150:c01`, `p0151:c01`, `p0152:c01`, `p0153:c01`, `p0154:c01`, `p0155:c01`, `p0156:c01`, `p0157:c01`, `p0158:c01`, `p0159:c01`, `p0160:c01`, `p0161:c01`, `p0162:c01`, `p0164:c01`, `p0165:c01`, `p0166:c01`, `p0167:c01`, `p0168:c01`, `p0169:c01`, `p0170:c01`, `p0171:c01`, `p0172:c01`, `p0173:c01`, `p0174:c01`, `p0176:c01`, `p0177:c01`.

**Решение:** footer не считается содержанием книги и не переносится в artifacts.

## F-02 — [Source extraction issue] Формулы/символы статистики деградированы

Text extraction местами повреждает математические symbols и indices: coefficient of variation, averages, queueing parameters `λ`, `μ`, `ρ`, delay variables и формулы на страницах со statistical/queueing analysis.

**Решение:** artifacts используют source-supported conceptual relations (`ρ = arrival/service rate`, рост queue delay near saturation, SIR/PIR/burst relationships), но не реконструируют повреждённые формулы посимвольно из памяти.

## F-03 — [Source extraction issue] Графики и topology/QoS diagrams не являются multimodal RAG objects

Figures 5.x содержат histograms, queue curves, classifiers, reservation diagrams and traffic-engineering topology. RAG сохраняет captions/labels частично, spatial information местами теряется.

**Решение:** Mermaid/SVG — новая source-grounded synthesis, не копия figures. Точное воспроизведение original graphs/figures: **[Needs confirmation]**.

## F-04 — [Needs confirmation] Numeric examples are not universal operational thresholds

В главе есть учебные значения: voice jitter example, loss percentages, priority/weighted queue shares, utilization thresholds, availability examples, underload example ~20–30%, sample SLA rates и др.

**Решение:** эти числа трактуются как examples/source illustrations. Они не используются как production defaults без конкретного SLA, traffic profile, equipment and measurements.

## F-05 — [Needs confirmation] Current technology claims remain source snapshots

Утверждения о распространённости методов QoS, RSVP, protocol behavior and current operational practice сохранены как statements книги.

**Решение:** current implementation/support/security status конкретного vendor/protocol не проверялся, поскольку chapter analysis выполняется в `rag_only` режиме.

## F-06 — [Boundary finding] Questions are part-level, not chapter-level

`p0178:c01` начинается заголовком «Вопросы к части 1» и включает материал по нескольким предыдущим главам.

**Решение:** questions pp. 178+ не включены в boundary главы 5 и не преобразованы в chapter-specific review artifacts.
