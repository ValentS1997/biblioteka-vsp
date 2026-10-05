# Translation / editorial findings — Chapter 6

Статус: findings для будущего **RU v2 repair**.  
Source truth: canonical English RAG `p0086:c01`–`p0093:c01`.  
Текущий перевод: `translation/ru/chapters/chapter-06-a-dynamic-approach-to-incident-response.md`.

## Итог проверки

- Semantic fidelity: high.
- DAIR structure preserved correctly.
- Figures 22–28 represented.
- Main problem: very dense mixed-language narrative.
- Chapter 6 should become a book-level terminology anchor for v2.

## Findings

| Current wording | Finding | Candidate v2 wording |
|---|---|---|
| `модель incident response` | mixed-language | `модель реагирования на инциденты` |
| `incident response teams` | mixed-language | `команды реагирования на инциденты` |
| `prepare — подготовка` | acceptable first-use form | keep once; later use Russian or fixed canonical term |
| `detect — обнаружение` | acceptable first-use form | keep once |
| `threat hunting` | mixed-language | `поиск угроз (threat hunting)` first use |
| `Event of Interest` | established acronym | `событие, представляющее интерес (EOI)` |
| `incident` | repeated English in Russian prose | `инцидент` |
| `triage — триаж` | terminology choice | `триаж / приоритизация` define once |
| `Response Actions Loop` | canonical DAIR term | preserve English + Russian canonical form |
| `containment` | mixed-language | `сдерживание` |
| `eradication` | mixed-language | `искоренение` |
| `recovery` | mixed-language | `восстановление` |
| `metrics` | mixed-language | `метрики` acceptable but consistent |
| `best practices` | mixed-language | `рекомендуемые практики` |
| `framework` | mixed-language | choose canonical policy |
| `incident response analysts` | mixed-language | `аналитики по реагированию на инциденты` |
| `stakeholders` | mixed-language | `заинтересованные стороны` |
| `management` | mixed-language | `руководство` |
| `executive leadership` | mixed-language | `высшее руководство` |
| `threat detection` | mixed-language | `обнаружение угроз` |
| `forensic analysis` | mixed-language | `форензик-анализ` / `криминалистический анализ` policy needed |
| `business priorities` | mixed-language | `бизнес-приоритеты` |
| `operational realities` | mixed-language | `операционные реалии` |
| `guidance from decision makers` | mixed-language | `рекомендации лиц, принимающих решения` |
| `investigative decisions` | mixed-language | `решения по расследованию` |
| `production database servers` | mixed-language | `production-серверы баз данных` or full Russian |
| `customer-facing applications` | mixed-language | `клиентские приложения` |
| `live response techniques` | mixed-language | `методы live response` define once |
| `maintenance window` | mixed-language | `окно обслуживания` |
| `network segmentation` | mixed-language | `сегментация сети` |
| `disruptive forensic analysis` | mixed-language | `форензик-анализ с заметным операционным воздействием` |
| `security goals` | mixed-language | `цели безопасности` |
| `organizational priorities` | mixed-language | `приоритеты организации` |
| `initial vector` | mixed-language | `начальный вектор атаки` |
| `phishing email` | mixed-language | `фишинговое письмо` |
| `phishing lure` | mixed-language | `фишинговая приманка` |
| `scheduled task` | mixed-language | `запланированная задача` |
| `malicious code` | mixed-language | `вредоносный код` |
| `response functions` | mixed-language | `функции реагирования` |

## Canonical v2 terminology recommendation

Chapter 6 should define the book-wide standard:

- Prepare — Подготовка
- Detect — Обнаружение
- Verify — Проверка
- Triage — Триаж / Приоритизация
- Scope — Определение масштаба
- Contain — Сдерживание
- Eradicate — Искоренение
- Recover — Восстановление
- Debrief — Разбор
- Response Actions Loop — Цикл действий реагирования
- Decision Makers — Лица, принимающие решения

После первого bilingual introduction narrative prose следует вести преимущественно на русском.

## Visual debt

Figures 22–28 are extremely important.

Priority:
- Figure 22 — highest: full DAIR model
- Figure 24 — high: waypoints/actions concept
- Figure 25 — high: decision-maker overlay
- Figure 26 — high: Verify/Triage
- Figure 27 — high: Scope
- Figure 28 — highest: Response Actions Loop

Chapter 6 без figures теряет значительную часть educational value.

## Priority

`CRITICAL`

Это центральная методологическая глава книги.  
Её terminology и figures должны стать эталоном для всего RU v2.
