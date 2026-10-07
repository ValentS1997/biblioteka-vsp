# Глава 8 — Mermaid: prior → evidence → posterior

**Source:** EPUB spine 34–35, `OPS/ch1-32.xhtml` → `OPS/ch1-33.xhtml`; RAG `e0034:c01–c03`, `e0035:c01–c05`.

## 1. Байесовское обновление

```mermaid
flowchart LR
    A["Prior P(КУД)"] --> C["Bayes / conditional probability"]
    B["Evidence: ПТП или ~ПТП"] --> C
    D["Likelihoods: P(evidence | event/no-event)"] --> C
    C --> E["Posterior P(КУД | evidence)"]
    E --> F["Решение / следующий measurement"]
```

## 2. Учебная causal/dependency chain

```mermaid
flowchart LR
    A["ПТП: результат penetration test"] --> B["УЭУ: remote exploitable vulnerability"]
    B --> C["КУД: major data breach"]
    A -. "обновляет вероятность" .-> B
    B -. "изменяет вероятность" .-> C
```

Это decomposition учебного примера, не доказанная causal model конкретной организации.

## 3. Sanity-check posterior

```mermaid
flowchart TD
    A["Prior: P(КУД)=1,24%"] --> B{"Test result"}
    B -->|ПТП| C["Posterior = 23,8%"]
    B -->|~ПТП| D["Posterior = 1,01%"]
    C --> E["Positive evidence повышает risk estimate"]
    D --> F["Negative evidence немного снижает risk estimate"]
```

Источник: `e0035:c04–c05`.

## 4. Не путать условные вероятности

```mermaid
flowchart LR
    A["P(КУД | УЭУ)"] <-->|"Bayes + base rates"| B["P(УЭУ | КУД)"]
```

Они в общем случае **не равны**.

## Boundary

Рис. 8.1–8.2 не реконструируются как оригинальные изображения. Повреждённая числовая запись шага 3 сохраняется в `commands.md` и `source-findings.md`; diagram не исправляет источник.
