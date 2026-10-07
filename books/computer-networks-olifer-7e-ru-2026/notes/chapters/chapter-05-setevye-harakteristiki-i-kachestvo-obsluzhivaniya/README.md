# Глава 5 — Сетевые характеристики и качество обслуживания

Состояние артефактов: `RAG_GROUNDED`. Это **не** означает, что пользователь прочитал главу; reading state книги остаётся `planned`.

## Источник, границы и режим

- Книга: «Компьютерные сети. Принципы, технологии, протоколы», 7-е издание; Виктор Олифер, Наталья Олифер.
- `book_id: computer-networks-olifer-7e-ru-2026`.
- Канонический источник: `source/book.pdf`; SHA-256: `16f4b02985f65c602c6268620878cbacd692a61fd5898ca811b3d1a332e3f84d`.
- Source policy: **rag_only**; прямое чтение PDF, внешний web и модельная память не использовались как источник содержания главы.
- RAG boundary: `computer-networks-olifer-7e-ru-2026:p0131:c01` … `p0177:c01`.
- PDF pages: **131–177**, включительно; **48** адресуемых RAG chunks.
- Печатные страницы книги: **130–176**.
- На `p0131:c01` явно начинается «Глава 5. Сетевые характеристики и качество обслуживания».
- На `p0178:c01` начинаются «Вопросы к части 1» — это уже вне scope главы 5.
- На `p0182:c01` начинается часть II, а на `p0183:c01` — глава 6.
- Chapter boundary: **VERIFIED**.
- BOOK-READINESS v1.3: `READY`; source/RAG generation, acceptance и checksum не менялись.
- Контракт: `BIBLIOTEKA-VSP-CHAPTER-ARTIFACT-COLLECTION v1.7`.

## Карта главы

| Раздел | PDF pages | RAG | Фокус |
| --- | ---: | --- | --- |
| Типы характеристик и SLA | 131–133 | `p0131:c01`–`p0133:c01` | User/provider view, long/medium/short-term metrics, SLA |
| Производительность и надёжность | 134–149 | `p0134:c01`–`p0149:c01` | Ideal vs real network, statistics, measurements, delays, rates, loss, availability, provider characteristics |
| Приложения и QoS | 149–152 | `p0149:c01`–`p0152:c01` | Stream/burst traffic, sensitivity to delay/jitter/loss |
| Методы QoS | 152–153 | `p0152:c01`–`p0153:c01` | Congestion management vs avoidance; differentiation by traffic class |
| Управление очередями | 154–162 | `p0154:c01`–`p0162:c01` | Queueing theory, FIFO, priority, weighted queues, utilization and burstiness |
| Кондиционирование трафика | 163–166 | `p0163:c01`–`p0166:c01` | Profiling/policing vs shaping; traffic profiles |
| Обратная связь | 166–169 | `p0166:c01`–`p0169:c01` | Flow/congestion feedback, explicit/implicit signals |
| Резервирование ресурсов | 169–173 | `p0169:c01`–`p0173:c01` | Admission control, reserved bandwidth, delay guarantees by measurement |
| Инжиниринг трафика | 173–176 | `p0173:c01`–`p0176:c01` | Route choice with resource/load awareness |
| Недогруженный режим | 176–177 | `p0176:c01`–`p0177:c01` | Overprovisioning, utilization monitoring, RSVP sidebar/source supplement |

Boundary anchors: [p0131:c01](../../../rag/chunks/p0101-p0200/p0131-c01.md) → [p0177:c01](../../../rag/chunks/p0101-p0200/p0177-c01.md) → [p0178:c01](../../../rag/chunks/p0101-p0200/p0178-c01.md).

## Главный принцип

**QoS — это не одна метрика и не одна очередь, а управляемый компромисс между характеристиками трафика, загрузкой ресурсов и требованиями приложений.** Глава строит цепочку: сначала формализовать качество через измеримые показатели и SLA, затем измерить сеть, классифицировать трафик и только после этого применять механизмы очередей, кондиционирования, обратной связи, резервирования и traffic engineering.

## Что важно вынести

1. **“Сеть работает хорошо” нужно переводить в измеримые характеристики.** В source это прежде всего производительность, надёжность и безопасность транспортной услуги, а SLA фиксирует количественные требования и метод измерения. `p0131:c01`–`p0133:c01`.
2. **Пакетная сеть статистична.** Реальные задержки, потери, reorder и variation возникают из-за очередей, случайной нагрузки и различий маршрутов; поэтому one-off measurement недостаточно. `p0134:c01`–`p0139:c01`.
3. **Active и passive measurement решают разные задачи.** Active measurement вводит специальные test packets; passive measurement наблюдает реальный traffic и может потребовать mirroring/measurement infrastructure. `p0139:c01`–`p0142:c01`.
4. **Delay metrics нельзя смешивать.** One-way delay, jitter, reaction time и RTT измеряют разные свойства; RTT удобнее, но скрывает асимметрию направлений. `p0142:c01`–`p0144:c01`.
5. **Rate тоже многомерна.** SIR, IIR, PIR и burst size описывают разные временные масштабы трафика; SLA должен задавать не только limit, но и averaging interval. `p0144:c01`–`p0146:c01`.
6. **Reliability — это не только packet loss.** Source отдельно рассматривает loss ratio, availability и fault tolerance. `p0146:c01`–`p0147:c01`.
7. **Extensibility ≠ scalability.** Легко добавить компонент — не значит, что сеть сохранит performance при росте. `p0147:c01`–`p0149:c01`.
8. **Приложения требуют разного QoS.** Потоковый и bursty traffic, delay/jitter sensitivity и loss sensitivity должны определять policy, а не единый режим для всего traffic. `p0149:c01`–`p0152:c01`.
9. **Queueing резко ухудшается при высокой utilization.** Source связывает delay не только с average load, но и с burstiness/CV; для снижения задержек нужно уменьшать и utilization, и pulsation. `p0154:c01`–`p0157:c01`.
10. **FIFO, strict priority и weighted queues дают разные trade-offs.** FIFO не дифференцирует; priority минимизирует delay high-priority traffic, но может подавлять остальные classes; weighted queues гарантируют classes долю capacity при congestion. `p0158:c01`–`p0162:c01`.
11. **Policing/profiling и shaping не эквивалентны.** Profiling source описывает как dropping excess packets; shaping — как buffering/delaying them, сохраняя среднюю скорость при возможности. `p0163:c01`–`p0166:c01`.
12. **Feedback лечит overload через источник/узлы, reservation — до появления нагрузки.** Admission control проверяет ресурсы вдоль path; reservation эффективен только если фактический flow соответствует заявленным характеристикам. `p0166:c01`–`p0172:c01`.
13. **Traffic engineering добавляет load-aware route choice.** Цель — не просто shortest path, а более сбалансированное использование network resources. `p0173:c01`–`p0176:c01`.
14. **Overprovisioning — простой, но дорогой QoS strategy.** Source предлагает держать сеть далеко от saturation и мониторить utilization; конкретные thresholds в главе — учебные примеры, не универсальные нормы. `p0176:c01`–`p0177:c01`.

## Артефакты

- [cheatsheet.md](cheatsheet.md) — conceptual/operational cheatsheet v1.7.
- [commands.md](commands.md) — source-confirmed measurement/QoS mechanisms; executable CLI в главе отсутствует.
- [diagram.md](diagram.md) — Mermaid-карта «measure → classify → control → verify».
- [visual-cheatsheet.svg](visual-cheatsheet.svg) — компактная визуальная схема.
- [visual-cheatsheet-detailed.svg](visual-cheatsheet-detailed.svg) — подробная визуальная схема.
- [source-findings.md](source-findings.md) — extraction/provenance ограничения главы.

## Conditional artifacts

- Отдельного явного chapter-end summary на PDF pp. 131–177 **не обнаружено** → `summary.md` не создаётся.
- `p0178:c01` начинает **«Вопросы к части 1»**, относящиеся сразу к главам 1–5, а не к одной главе 5. Поэтому chapter-specific `review-questions.md` / `review-answers.md` не создаются.

## Ограничения источника

RAG содержит повторяющийся посторонний footer/URL, OCR/glyph substitutions, деградированные формулы/графики и textbook numeric examples. Они зарегистрированы в [source-findings.md](source-findings.md); значения из примеров не переносятся как универсальные production thresholds.
