# Глава 10. На пути к зрелости метрик безопасности

**Книга:** Дуглас У. Хаббард, Ричард Сирсен — «Как оценить риски в кибербезопасности: лучшие инструменты и практики».  
**Book ID:** `cybersecurity-risk-hubbard-seiersen-ru` · **Глава:** 10 · **Контракт:** BIBLIOTEKA-VSP-CHAPTER-ARTIFACT-COLLECTION v1.7.  
**Статус:** `RAG_GROUNDED`; анализ основан только на адресуемом каноническом RAG.

## Главная идея

Глава переводит предыдущие количественные методы в **операционную модель зрелости метрик безопасности**. Авторы предлагают начинать не с «больших данных», а с решения и риска: сначала использовать анализ скудных данных (АСД), затем измерять работу уже сделанных инвестиций, объединять данные между функциями безопасности и в перспективе переходить к предписывающей аналитике.

Основная логика:

1. **АСД / Sparse Data Analysis** — принимать решения при ограниченных эмпирических данных.
2. **Функциональные метрики** — после инвестиций измерять охват, конфигурацию и смягчение риска внутри отдельных функций.
3. **Витрины данных безопасности** — соединять источники и оценивать взаимодействие людей, процессов и технологий между функциями.
4. **Предписывающая аналитика** — объединять predictive/data-science outputs с decision analysis для выбора следующего действия.

Глава заканчивается практическим примером АСД на R/пакете `LearnBayes`.

## Verified RAG boundary

| Поле | Значение |
|---|---|
| Source mode | `rag_only` |
| Начало | EPUB spine **41**, `OPS/ch1-39.xhtml`: «Глава 10. На пути к зрелости метрик безопасности» |
| Продолжение/завершение | Spine **42**, `OPS/ch1-40.xhtml`: предписывающая аналитика и пример АСД на R |
| Следующая глава | Spine **43**, `OPS/ch1-41.xhtml`: «Глава 11. Насколько эффективно взаимодействуют мои вложения в безопасность?» |
| Addressable chunks | `e0041:c01–c04` (4), `e0042:c01–c05` (5): всего **9** |
| Boundary check | `e0043:c01` — начало главы 11 |
| Source SHA-256 | `43b5ec48fec54cf506d05b62975c8772978fc4fbbe2a97c97643d8c6ad054481` |
| Печатные страницы | `[Needs confirmation]`; EPUB spine не равен печатной странице |

## Карта главы

| Блок | Содержание | RAG |
|---|---|---|
| Модель зрелости | Метрики должны быть непрерывными и измеримыми; начинать следует с decision/risk question | `e0041:c01` |
| Анализ скудных данных | Quantitative risk analysis возможен до появления зрелой data/telemetry program | `e0041:c01–c02` |
| Функциональные метрики | Измерять охват/конфигурацию и скорость смягчения риска по отдельным security functions | `e0041:c02–c03` |
| Витрины данных | Объединять данные нескольких security domains для cross-functional questions | `e0041:c03–c04` |
| Residual exposure | Измерять время существования скрытого/остаточного риска и скорость его обнаружения/устранения | `e0041:c04` |
| Descriptive / predictive / prescriptive | Авторы разделяют три класса аналитики и связывают prescriptive с decision analysis | `e0042:c01–c02` |
| Grey-zone prioritization | Идея использовать evidence/model outputs для приоритизации расследований до подтверждённого breach | `e0042:c01–c02` |
| R example | Bayesian update доли cloud applications с базовыми controls при малой выборке | `e0042:c02–c05` |

## Функциональные метрики

Источник выделяет две макрообласти:

### 1. Coverage & configuration

Проверяется не наличие продукта само по себе, а фактическая работоспособность и охват:
- активировано ли решение;
- корректна ли конфигурация;
- действительно ли собираются логи;
- поступают ли они в нужные средства анализа;
- настроены ли alerts;
- измеряются ли false positives/false negatives;
- измеряется ли связанный operational workflow.

Пример авторов: firewall, установленный с правилом `any:any`, формально существует, но не даёт ожидаемого ограничения доступа (`e0041:c03`).

### 2. Mitigation metrics

Измеряется скорость появления и ликвидации риска. В книге приводится пример policy-like метрики для internet-facing remotely exploitable vulnerabilities: устранение в течение рабочего дня, а monitoring/mitigation — в течение часа. Это **пример источника**, не локальный SLA пользователя (`e0041:c03`).

## Витрины данных и residual risk

Security data mart в главе — не конкретный продукт, а subject-specific store/analytical layer, позволяющий связывать источники разных функций и отвечать на вопросы о cross-program effectiveness.

Особый акцент: **сколько времени residual exposure существует до обнаружения и приоритизации**. Авторы считают эту длительность важной измеримой величиной и переносят дальнейший survival-analysis KPI в главу 11 (`e0041:c04`).

## Предписывающая аналитика

Авторы различают:

- **descriptive** — sums/averages/trends;
- **predictive** — использование прошлых данных для оценок будущих результатов;
- **prescriptive** — объединение decision models и data-science models для выбора действия.

В предлагаемой архитектуре output data-science model становится input decision model. Это авторская целевая концепция, а не готовая архитектура SIEM/SOAR (`e0042:c01–c02`).

## R-пример АСД

Сценарий: due diligence компании с сотнями cloud applications и ограниченным временем/доступом. Исходные субъективные beliefs:
- 50% уверенности, что true control coverage < 40%;
- 90% уверенности, что true control coverage < 60%.

Через `LearnBayes::beta.select` источник получает prior parameters около `4.31, 6.30`, затем обновляет их аудитами:
- 3 successes / 7 failures;
- затем 5 successes / 30 failures.

После второго набора источник приводит 90%-ный interval примерно:
`0.1148617 … 0.3082632`, то есть около **12–30%** coverage.

Далее моделируются outcomes для следующих 200 audits; source result set содержит примерно 17–56 successes с заявленным покрытием около 91% (`e0042:c03–c05`).

## Conditional artifacts

- Явного chapter-end summary/resume нет → `summary.md` не создаётся.
- Review/control questions/exercises отсутствуют → review-файлы не создаются.
- [source-findings.md](source-findings.md) создаётся из-за code/extraction mismatches в R-примере и отсутствующих исходных фигур 10.1–10.3.

## Артефакты

- [cheatsheet.md](cheatsheet.md)
- [commands.md](commands.md)
- [diagram.md](diagram.md)
- [visual-cheatsheet.svg](visual-cheatsheet.svg)
- [visual-cheatsheet-detailed.svg](visual-cheatsheet-detailed.svg)
- [source-findings.md](source-findings.md)

**Reading progress:** остаётся `planned`; canonical EPUB/RAG не изменяются.
