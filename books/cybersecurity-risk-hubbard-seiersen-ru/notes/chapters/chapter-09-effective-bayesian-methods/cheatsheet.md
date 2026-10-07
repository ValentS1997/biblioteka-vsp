# Глава 9 — эффективные методы Bayes: cheatsheet

**Источник:** `cybersecurity-risk-hubbard-seiersen-ru`; EPUB spine 36–39, `OPS/ch1-34.xhtml` → `OPS/ch1-37.xhtml`; RAG `e0036:c01`, `e0037:c01–c07`, `e0038:c01–c08`, `e0039:c01–c05`.

## Symptom / problem framing

Типичные возражения: «данных слишком мало», «слишком много условий», «нельзя оценить всё», «неясно, стоит ли тратить время на дополнительное исследование».

Глава отвечает четырьмя инструментами:
- beta distribution для малой выборки;
- ЛОШ и lens model для нескольких условий;
- value of information для выбора, **что измерять дальше**;
- empirical conditional probabilities для замены части экспертных inputs наблюдаемыми данными.

## Baseline / context

### Beta distribution

Для бинарной выборки:
- hit увеличивает `α`;
- miss увеличивает `β`;
- prior `Beta(1,1)` авторы используют как равномерный non-informative starting point;
- posterior остаётся распределением, а не single-point frequency.

### Несколько условий

Полная node probability table быстро становится непрактичной. Пример источника: 7 факторов, где три имеют по 2 значения и четыре — по 3, дают **648 комбинаций** (`e0038:c01`).

Два подхода:
- **ЛОШ** — эксперт оценивает отдельное влияние каждого условия;
- **lens model** — регрессия выводит устойчивое правило из множества экспертных оценок сценариев.

### Value of Information

Дополнительное измерение ценно только в контексте **решения**. Если новая информация не способна изменить действие или стоимость ошибки мала, глубже измерять может быть экономически невыгодно.

## Read-only checks

1. Как определены hit/miss и population/exposure unit?
2. Выборка независима от того, произошло событие или нет?
3. Какой prior используется и почему?
4. Не интерпретируется ли observed frequency как точная истинная frequency?
5. Для нескольких условий: действительно ли факторы достаточно независимы?
6. Проверены ли крайние комбинации условий на абсурдно высокие/низкие probabilities?
7. Согласуются ли baseline probability и conditional probabilities?
8. Если используется lens model, есть ли достаточное число сценариев и duplicate pairs?
9. Какие решения реально изменятся после дополнительной информации?
10. EVPI выше стоимости планируемого measurement?
11. Empirical `P(Y|X)` считает именно тот state X, который указан в definition?
12. Исторические данные сопоставимы по периоду, population и event definition?

Конкретные datasets, priors, decision thresholds и control costs: **[Needs confirmation]**.

## Interpretation

### Малое количество данных всё равно уменьшает неопределённость

Авторы используют beta distribution, чтобы не выдавать `hits / n` за известную истинную частоту. Даже при малой выборке posterior distribution исключает часть возможных значений и может обновляться каждым новым hit/miss (`e0037:c01–c06`).

### Frequency uncertainty влияет на tail risk

Если сама частота события неизвестна и моделируется распределением, вероятность нескольких событий может быть выше, чем при модели с одной фиксированной средней частотой. В примере это увеличивает правый хвост aggregate-loss distribution при сохранении среднего (`e0037:c05–c06`).

### ЛОШ

Метод переводит probabilities в log-odds, добавляет относительные effects условий к baseline и преобразует назад в probability. Главная оговорка: correlated conditions могут привести к double counting и экстремальным estimates (`e0038:c02–c04,c07`).

В исходной записи ЛОШ есть internal mismatch знака/скобок — практический синтаксис **не нормализован**, см. `source-findings.md`.

### Lens model

Lens model не пытается описать внутреннее мышление эксперта. Она статистически моделирует **наблюдаемые экспертные оценки**, усредняя их и удаляя inconsistency. Авторы рекомендуют regression-aware пользователям; для незнакомых с regression — сначала ЛОШ (`e0038:c04–c07`).

### EOL / EVPI

EOL связывает вероятность ошибки с её economic consequence. EVPI отвечает: «какова максимальная ожидаемая ценность полного устранения этой неопределённости?» Поэтому measurement priority должна зависеть не от любопытства, а от потенциального изменения решения (`e0039:c01–c02`).

### Empirical conditional probabilities

Источник показывает `COUNTIFS/COUNTIF` для вычисления conditional frequency из binary historical table. В соседней прозе и формуле есть mismatch относительно состояния `X=Нет` vs Excel criterion `B=1`; не исправлять молча (`e0039:c02`).

## Next action

1. Определить decision/event/population/exposure unit.
2. Зафиксировать prior и его provenance.
3. Для binary data обновлять `α/β` hits/misses.
4. Для нескольких условий сначала убрать неинформативные/correlated factors.
5. Выбрать ЛОШ для быстрого structured expert model или lens model при наличии regression skill и достаточных сценариев.
6. Проверить model outputs на крайних combinations.
7. Оценить EOL/EVPI и выбрать, какую uncertainty уменьшать дальше.
8. По мере появления historical data заменять часть expert conditionals empirical estimates.
9. Сохранять version/provenance каждого update.

## Modifying action

- Пересчёт spreadsheet / Monte Carlo / regression — `workload-generating`.
- Изменение risk methodology/model — аналитически/организационно `state-changing`.
- Сбор telemetry/исторических security data может затрагивать privacy и governance.
- Infrastructure commands отсутствуют: **[Not applicable]**.
- Owners, approvals, data retention, toolchain, rollout/rollback: **[Needs confirmation]**.

## Verification / acceptance checks

- probabilities ∈ [0,1];
- `α>0`, `β>0`;
- hits+misses соответствуют population/exposure definition;
- posterior обновляется воспроизводимо;
- correlated conditions не double-counted;
- lens/regression проверяется вне training scenarios;
- EVPI не трактуется как гарантированная экономия;
- conditional probability соответствует корректному denominator/state.

Локальные acceptance thresholds: **[Needs confirmation]**.

## Rollback

Для модели: version-control prior, inputs, formulas, data snapshot и previous outputs; при обнаруженной ошибке восстановить последнюю валидированную версию.

Для организационных/process изменений rollback procedure отсутствует в главе: **[Needs confirmation]**.
