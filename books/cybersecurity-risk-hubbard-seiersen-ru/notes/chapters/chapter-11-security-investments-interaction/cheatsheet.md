# Глава 11 — взаимодействие security investments: cheatsheet

**Источник:** `cybersecurity-risk-hubbard-seiersen-ru`; EPUB spine 43–44, `OPS/ch1-41.xhtml` → `OPS/ch1-42.xhtml`; RAG `e0043:c01–c02`, `e0044:c01–c06`.

## Symptom / problem framing

Организация может иметь множество security controls и KPI по отдельности, но не понимать:

- какие controls реально уменьшают один и тот же risk;
- какие из них дублируют или компенсируют друг друга;
- где остаётся residual exposure;
- какой vendor/control обнаруживает угрозы быстрее;
- сколько времени процессы remediation проводят на каждой стадии.

Глава предлагает dimensional modeling как логический слой для таких вопросов.

## Baseline / context

### Facts + dimensions

В центре mart находится fact table с событиями/состояниями. Dimensions описывают контекст: date, asset, vulnerability, mitigation, malware и т. д.

Security fact может быть «factless»: основная мера — сам факт существования строки/события, который агрегируется как count (`e0044:c02–c03`).

### Conformed dimensions

Если vulnerability, malware и mitigation marts используют одинаковые date/asset dimensions, их можно связывать и cross-drill. Это позволяет анализировать interactions между controls без попытки собрать одну монолитную модель (`e0044:c01–c02`).

### KISS

Источник прямо предостерегает от «размерной модели управления Вселенной». Начинать следует с реальных stakeholder questions и добавлять attributes по необходимости (`e0044:c03`).

## Read-only checks

1. Какой security decision/KPI должен поддержать mart?
2. Какова grain fact table — одно событие, asset-state-at-time, process instance?
3. Какие dimensions являются conformed?
4. Asset определяется одинаково во всех sources?
5. Date/time semantics одинаковы: event time, discovery time, remediation time?
6. Есть ли stable IDs и provenance для source events?
7. Не теряется ли atomicity при предварительной агрегации?
8. Какие controls могут jointly affect один risk?
9. Можно ли измерить residual exposure duration?
10. Для survival metric определены start/end/censoring rules?
11. Для workflow snapshot определены стадии и timestamps?
12. Не создаются ли dimensions «на всякий случай» без decision value?

Фактическая schema, data sources, retention, SLAs и owners: **[Needs confirmation]**.

## Interpretation

### Data mart — логическая модель, не обязательно physical star schema

Авторы подчёркивают слово «логический»: современные запросы могут виртуализировать facts/dimensions, поэтому рисунки не требуют буквального создания физических таблиц (`e0044:c01`).

### Security fact

Факт безопасности — событие или состояние. В отличие от sales, monetary measure может отсутствовать; сама строка/наличие события становится measure через count (`e0044:c02–c03`).

### Survival analysis

Для hidden threat authors используют survival function: time против доли угроз, которые ещё существуют. Это превращает vague «мы долго не видим угрозу» в measurable dwell/exposure distribution (`e0044:c04`).

### Cross-control effectiveness

Если marts связаны через asset/date, можно задавать вопросы:
- где application allowlisting была последней линией защиты;
- какой mitigation vendor быстрее блокировал threats;
- какие controls перестали приносить ожидаемую пользу;
- какие gaps повторяются на одних классах assets.

Это source examples, не доказанные ответы для конкретной среды.

### Accumulating snapshot

Для multi-stage process модель хранит несколько milestone dates и durations. Это подходит для remediation, SDL и CI/CD workflows; purpose — measure cycle time and bottlenecks (`e0044:c05–c06`).

## Next action

1. Выбрать один cross-control risk question.
2. Определить atomic fact grain.
3. Определить minimal conformed dimensions: обычно date/time + asset, затем risk-specific dimensions.
4. Проверить source identifiers/time semantics.
5. Создать read-only logical model / view на sample data.
6. Проверить drill-down до исходного события.
7. Добавить survival or process-duration metric, если вопрос связан со временем.
8. Сравнить controls по одному measurable outcome.
9. Добавлять attributes только при подтверждённой аналитической потребности.

## Modifying action

- Создание data mart/view/ETL pipeline — `state-changing`.
- Backfill и крупные historical joins — `workload-generating`.
- Изменение log retention/collection — `state-changing` и может иметь storage/privacy impact.
- Глава не содержит готовых DDL/SQL/ETL-команд.
- Schema owner, RBAC, data classification, retention, capacity и rollback: **[Needs confirmation]**.

## Verification / acceptance checks

- fact grain документирован и не двусмыслен;
- dimensions имеют stable keys/semantics;
- cross-source joins не создают duplicate facts;
- totals drill back to source events;
- time-based metrics воспроизводимы;
- survival start/end definitions стабильны;
- KPI связан с risk outcome, а не только с activity volume.

## Rollback

До physical implementation сохранить:
- исходные source queries;
- schema/view definitions;
- baseline counts;
- data lineage;
- previous KPI definitions.

Конкретный DB/ETL rollback runbook в главе отсутствует: **[Needs confirmation]**.
