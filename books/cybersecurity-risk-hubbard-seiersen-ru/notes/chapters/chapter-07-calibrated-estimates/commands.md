# Глава 7 — методы, расчёты и operational boundary

**Provenance:** `cybersecurity-risk-hubbard-seiersen-ru`; EPUB spine 31–33; RAG `e0031:c01–c03`, `e0032:c01–c09`, `e0033:c01–c04`.

## Исполняемые команды

**[Not applicable].** Глава не содержит CLI, API, кода, Excel-формул, shell/SQL или конфигураций инфраструктуры.

## Подтверждённые вычисления

### 1. Ожидаемое покрытие 90%-ного интервала

Для 10 задач с заявленным 90%-ным покрытием:

```text
ожидаемое число попаданий ≈ 10 × 0,9 = 9
```

Источник: `e0032:c02–c03`. Это математическое ожидание, а не требование получить ровно 9 каждый раз.

### 2. Ожидаемое число правильных бинарных ответов

Пример источника:

```text
1 + 0,5 + 0,9 + 0,6 + 0,7 + 0,8 + 0,8 + 1 + 0,9 + 0,7 = 7,9
```

Источник: `e0032:c03`. Суммируются индивидуальные субъективные вероятности правильности ответов.

### 3. Проверка границ 90%-ного интервала

90%-ный центральный интервал интерпретируется авторами как:
- 5% вероятность значения ниже нижней границы;
- 5% вероятность значения выше верхней границы.

Поэтому каждую границу предлагают проверять отдельно как утверждение с 95%-ной уверенностью (`e0032:c04`).

## Source-confirmed методы

| Метод | Класс | Назначение |
|---|---|---|
| Calibration questionnaire | `workload-generating` | Сравнить заявленную и фактическую уверенность |
| Equivalent-bet test | `read-only` self-check / упражнение `workload-generating` | Проверить субъективный смысл процента |
| Repeat + feedback | `workload-generating` | Обучать корректировке over/underconfidence |
| Arguments against estimate | `read-only` аналитика | Ослабить confirmation/anchoring effects |
| Separate bound tests | `read-only` аналитика | Проверить верхнюю/нижнюю границу независимо |
| Absurdity test / reverse anchor | `read-only` аналитика | Начать широко и исключать явно невозможные значения |
| Calibration curve over forecasts | `read-only` analysis of recorded outcomes | Проверить соответствие confidence ↔ observed frequency |

## Числа источника — не operational thresholds

- Для 10 interval questions авторы указывают: шанс калиброванного участника получить ≤5 попаданий — **1/612**; в их агрегированных данных так плохо выступили **56%** респондентов (`e0032:c03`).
- В binary tests средняя ожидаемая точность была **74%**, фактическая **62%** (`e0032:c04`).
- В собственных training data Хаббарда после пятого упражнения: **80%** ideal calibration, **10%** significant improvement, **10%** no improvement (`e0033:c01`).

Эти цифры нельзя использовать как автоматический HR/performance gate без отдельной валидированной программы.

## Safety / privacy boundary

Практическая калибровка сотрудников может создавать персональные performance data. Глава не определяет:
- retention/access policy;
- HR/legal basis;
- anonymization;
- passing threshold;
- consequences of failure.

Все перечисленное: **[Needs confirmation]**.

Infrastructure state-changing actions: **[Not applicable]**.
