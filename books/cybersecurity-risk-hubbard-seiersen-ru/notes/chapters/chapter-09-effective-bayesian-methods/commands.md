# Глава 9 — source-confirmed formulas and analytical tools

**Provenance:** `cybersecurity-risk-hubbard-seiersen-ru`; EPUB spine 36–39; RAG `e0036:c01`, `e0037:c01–c07`, `e0038:c01–c08`, `e0039:c01–c05`.

## CLI / infrastructure commands

**[Not applicable].** Глава не содержит shell/API/SQL-команд, exploitation steps или production configuration changes.

## Beta distribution — Excel

Источник `e0037:c02`:

```text
=БЕТАРАСП(x;альфа; бета)
```

Функция описана как cumulative probability, что истинная proportion меньше `x`.

Обратная функция:

```text
=БЕТА.ОБР(вероятность; альфа; бета)
```

### Posterior update from hits/misses

Источник `e0037:c03`:

```text
= БЕТАРАСП(x; априорное α + попадания; априорное β + промахи)
```

При prior `α=1, β=1` каждый hit добавляется к α, каждый miss — к β.

### Approximate PDF bar from CDF differences

Источник:

```text
= БЕТАРАСП(x + i/2; априорное α + попадания; априорное β + промахи)
- БЕТАРАСП(x – i/2; априорное α + попадания; априорное β + промахи)
```

`i` — arbitrary increment; источник говорит, что меньший increment даёт более точное изображение распределения.

## Binomial distribution

Источник `e0037:c03`:

```text
=БИНОМРАСП(число_успехов; число_испытаний; вероятность успеха;0)
```

В `e0037:c06` приводится:

```text
1-БИНОМРАСП(3;120;0,0167;1)
```

как пример вероятности получить более трёх hits при фиксированной frequency 1,67%.

## Beta mean

Источник `e0037:c05`:

```text
mean = α / (α + β)
```

В учебном posterior `α=3, β=119` источник приводит mean **2,46%**.

## Log-odds / ЛОШ

RAG `e0038:c02` содержит несколько конфликтующих вариантов:

```text
log(P(x)/(1 – P(x)
```

и далее:

```text
ЛОШ(P(Событие)) = ln(P(Событие)) / (1 – P(Событие))
= ln(0,02 / 0,98)
= –3,89182
```

а для conditional probability:

```text
ln(0,04 / 0,96) = 3,17805
```

При этом той же строкой источник утверждает, что ЛОШ отрицателен при `P<0,5`, а следующий шаг использует `–3,18` при расчёте delta. Это **[Source wording/code mismatch]**; варианты не нормализуются.

### Delta log-odds

```text
delta L(condition) = L(P(event | condition)) - L(P(event))
```

Source example итоговой комбинации:

```text
Adjusted L = –3,89 + 0,71 + 0,19 – 0,45 + 1,02 = –2,42
```

Обратное преобразование в источнике:

```text
Adjusted probability = 1 / (1 + 1 / exp(–2,42)) = 0,08167
```

Использовать source spreadsheet syntax только после отдельной проверки; глава сама рекомендует обходить `P=0` и `P=1`, где log-odds calculation выдаёт ошибку.

## Conditional probability from historical binary data

Источник `e0039:c02`:

```text
= СЧЁТЕСЛИМН(столбец A; «=1»; столбец B; «=1»)
  / СЧЁТЕСЛИ(столбец B; «=1»)
```

Непосредственно перед формулой prose описывает numerator/denominator через строки с `X=Нет`, тогда как Excel criterion использует `B=1`. Значение `1` для X в этом фрагменте не разрешает конфликт однозначно. **Не менять criterion без сверки**, см. `source-findings.md`.

## Value of Information

Источник даёт концептуальные расчёты:

```text
EOL = probability of error × cost of error
EVPI = maximum expected reduction in EOL under perfect information
```

Для простого control decision источник поясняет:
- если control не внедряется, error cost может зависеть от `P(event) × event cost`;
- если control внедряется, error cost связывается с вероятностью, что event не произойдёт, и control cost.

Это упрощённая decision model; точная spreadsheet formula и полный table layout не извлечены как самостоятельный объект.

## Operational safety

Все формулы — analytical/spreadsheet operations. External chapter spreadsheets не загружались. Dataset schema, Excel locale/version, regression tooling, validation data и rollback: **[Needs confirmation]**.
