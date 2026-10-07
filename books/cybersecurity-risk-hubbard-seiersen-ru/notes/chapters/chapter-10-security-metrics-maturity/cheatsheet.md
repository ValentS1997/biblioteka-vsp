# Глава 10 — зрелость метрик безопасности: cheatsheet

**Источник:** `cybersecurity-risk-hubbard-seiersen-ru`; EPUB spine 41–42, `OPS/ch1-39.xhtml` → `OPS/ch1-40.xhtml`; RAG `e0041:c01–c04`, `e0042:c01–c05`.

## Symptom / problem framing

Проблема главы — организация может много инвестировать в security tooling и собирать большие объёмы telemetry, но всё равно не знать:

- какое решение следует принять;
- какие вложения действительно уменьшают риск;
- насколько хорошо security functions покрывают среду;
- насколько быстро residual exposure обнаруживается и устраняется;
- когда additional analytics действительно улучшает prioritization.

Авторы предлагают maturity path, начинающийся с decision/risk analysis, а не с покупки big-data stack.

## Baseline / context

### Уровень 1: АСД

Sparse Data Analysis применяет методы предыдущих глав в условиях, когда operational data ещё мало. Это стартовая аналитика для решения, **во что инвестировать**, а не признак «незрелой математики» (`e0041:c01–c02`).

### Уровень 2: Functional metrics

После инвестиций нужны непрерывные метрики конкретных функций:

| Макрообласть | Примеры вопросов |
|---|---|
| Coverage/configuration | deployed? enabled? correctly configured? logging works? alerts connected? |
| Mitigation | как быстро возникает, обнаруживается и устраняется риск? |

Источник: `e0041:c02–c03`.

### Уровень 3: Security data marts

Данные нескольких security functions объединяются для cross-domain questions. Цель — измерять system-level effectiveness людей, процессов и технологий, а не только отдельного продукта (`e0041:c03–c04`).

### Уровень 4: Prescriptive analytics

Data-science signals + decision analysis → рекомендация следующего действия. Это целевая концепция авторов, а не готовый vendor implementation (`e0042:c01–c02`).

## Read-only checks

1. Какое решение поддерживает каждая метрика?
2. Есть ли baseline risk before investment?
3. Измеряется ли **фактический coverage**, а не факт покупки лицензии?
4. Проверяется ли configuration effectiveness?
5. Есть ли evidence, что logging/alerts реально работают end-to-end?
6. Есть ли false-positive / false-negative measurements?
7. Как измеряется time-to-detect / time-to-mitigate residual exposure?
8. Можно ли связать несколько security functions вокруг одного risk outcome?
9. Отделены descriptive metrics от predictive/prescriptive outputs?
10. Есть ли decision rule, превращающий analytics output в action priority?
11. Для R/АСД: зафиксированы ли prior assumptions, sample definition и success/failure criteria?
12. Можно ли воспроизвести posterior update независимо?

Фактическая maturity stage, tooling, KPI/SLA и datasets организации: **[Needs confirmation]**.

## Interpretation

### Начинать с решения, а не с data platform

Авторы прямо возражают против идеи, что сначала нужна зрелая big-data capability. Sparse-data methods должны помочь определить, **какие инвестиции и данные вообще имеют ценность** (`e0041:c01–c02`).

### Coverage ≠ effectiveness

Наличие firewall/AV/SIEM не является метрикой эффективности. Нужна проверка конфигурации, telemetry flow и operational response. Пример `any:any` показывает разрыв между deployment и фактическим control effect (`e0041:c03`).

### Residual exposure как измеряемая величина

Авторы делают акцент на dwell/exposure time между реальным появлением уязвимости/вредоносной активности и моментом, когда defender/vendor её распознаёт и приоритизирует (`e0041:c04`).

### Predictive ≠ prescriptive

Prediction сам по себе не определяет, **что делать дальше**. Prescriptive layer должен учитывать cost, risk и competing actions. Поэтому authors' architecture сохраняет decision analysis даже при росте data-science maturity (`e0042:c01–c02`).

### R example

R-код демонстрирует обновление prior по небольшой audit sample, а не production-ready audit framework. В extracted code есть inconsistencies, зарегистрированные в `source-findings.md`.

## Next action

1. Выбрать одно значимое security decision.
2. Зафиксировать current risk model и available sparse evidence.
3. Определить 2–5 functional metrics, связанных с coverage/configuration/mitigation.
4. Проверить end-to-end telemetry and action path.
5. Начать измерять residual exposure duration.
6. При накоплении данных объединять security domains вокруг common risk questions.
7. Использовать predictive outputs как inputs decision model, а не как автоматический priority score.
8. Версионировать priors, samples, model code и outcomes.

## Modifying action

- Включение новых logs, ETL/data marts, alerts или response automation — `state-changing`.
- Audit/simulation/model fitting — `workload-generating`.
- Автоматическая prescriptive action может иметь высокий operational impact.
- Глава не задаёт конкретные production commands, RBAC, retention или rollout.
- Owners, approvals, privacy, performance impact, test environment и rollback: **[Needs confirmation]**.

## Verification / acceptance checks

Для метрики:
- связана с decision/risk outcome;
- data path подтверждён;
- definition/version стабильны;
- metric может быть повторно вычислена;
- изменение метрики интерпретируется относительно baseline.

Для модели:
- prior и sample documented;
- posterior reproducible;
- code passes independent execution check;
- outputs validated before operational use.

## Rollback

До state-changing implementation сохранить:
- предыдущую конфигурацию logging/alerts;
- schema/data pipeline version;
- KPI definitions;
- model prior/code/output baseline.

Конкретный rollback runbook глава не предоставляет: **[Needs confirmation]**.
