# Translation / editorial findings — Chapter 5

Статус: findings для будущего **RU v2 repair**.  
Source truth: canonical English RAG `p0076:c01`–`p0084:c01`.  
Текущий перевод: `translation/ru/chapters/chapter-05-incident-response-models-and-their-limitations.md`.

## Итог проверки

- Semantic coverage: good.
- Figures 16–21 represented.
- References [1]–[2] preserved.
- Applied Risk / NIST quotes intentionally fail-closed.
- Основной v2 debt: mixed-language density и consistency.

## Findings

| Current wording | Finding | Candidate v2 wording |
|---|---|---|
| `Модели incident response` | mixed-language | `Модели реагирования на инциденты` |
| `системный framework` | hybrid | `системная модель / каркас` или glossary-consistent `framework` |
| `identification` | phase name vs prose mixed | в prose: `идентификация`; в model listing оставить original stage |
| `incident response team` | mixed-language | `команда реагирования на инциденты` |
| `containment` | repeated mixed-language | `сдерживание` в prose |
| `evidence` | mixed-language | `доказательства / артефакты` по context |
| `eradication` | mixed-language | `искоренение / устранение присутствия атакующего` |
| `recovery` | mixed-language | `восстановление` |
| `lessons learned analysis` | mixed-language | `анализ извлечённых уроков` |
| `metrics` | mixed-language | `метрики` допустимо, но единообразно |
| `incident information` | hybrid | `информация об инцидентах` |
| `cybersecurity program` | mixed-language | `программа кибербезопасности` |
| `incident handling` | mixed-language | `обработка инцидентов` |
| `risk management` | mixed-language | `управление рисками` |
| `controls` | mixed-language | `меры контроля` |
| `framework-oriented` | hybrid | `ориентированный на framework` → лучше переписать полностью |
| `workflows` | mixed-language | `рабочие процессы` |
| `cybersecurity posture` | mixed-language | `состояние защищённости` |
| `step-by-step guidance` | mixed-language | `пошаговое руководство` |
| `consulting services` | mixed-language | `консалтинговые услуги` |
| `communication / documentation` | mixed-language | `коммуникация / документирование` |
| `circular models` | mixed-language | `циклические модели` |
| `scoping` | core term | выбрать единый policy: `определение масштаба (scoping)` first use |
| `resource prioritization` | mixed-language | `приоритизация ресурсов` |
| `verification инцидента` | hybrid | `проверка/подтверждение инцидента` |
| `root cause analysis` | core recurring term | `анализ корневой причины (RCA)` first use |
| `operational needs` | mixed-language | `операционные потребности` |
| `business imperatives` | mixed-language | `приоритеты бизнеса` |
| `application server` | mixed-language | `сервер приложений` |
| `performance issue` | mixed-language | `проблема производительности` |
| `password complexity policy` | mixed-language | `политика сложности паролей` |
| `password auditing` | mixed-language | `аудит паролей` |
| `cracking tools` | mixed-language | `инструменты подбора/взлома паролей` |
| `remote access controls` | mixed-language | `меры контроля удалённого доступа` |
| `foundational concepts` | mixed-language | `базовые принципы` |

## Editorial strategy

Для v2 стоит разделить два режима:

1. **Model names / stage labels**
   - PICERL;
   - Preparation;
   - Detection and Analysis;
   - Govern/Identify/etc.

   Здесь original English допустим и полезен.

2. **Narrative prose**
   - переводить термины на русский;
   - English оставлять только при первом вводе профессионального термина.

Сейчас эти два режима смешаны, из-за чего текст выглядит дёрганым.

## Visual debt

Figures 16–21:

- Figure 16 — PICERL Linear
- Figure 17 — PICERL Stepped
- Figure 18 — NIST Incident Response Life Cycle
- Figure 19 — NIST Rev.3 + CSF
- Figure 20 — Seven-Step Model
- Figure 21 — Virginia Tech circular model

Visual priority: HIGH.

Эта глава строится вокруг сравнения моделей, поэтому отсутствие figures заметно ухудшает восприятие.

## Priority

`HIGH`

Причина: Chapter 5 — conceptual bridge между historical models и DAIR. Красивый v2 должен особенно хорошо показать этот transition и визуально, и терминологически.
