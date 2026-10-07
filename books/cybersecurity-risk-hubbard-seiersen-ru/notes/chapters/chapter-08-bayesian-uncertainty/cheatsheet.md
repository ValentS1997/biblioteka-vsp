# Глава 8 — байесовское обновление: cheatsheet

**Источник:** `cybersecurity-risk-hubbard-seiersen-ru`; EPUB spine 34–35, `OPS/ch1-32.xhtml` → `OPS/ch1-33.xhtml`; RAG `e0034:c01–c03`, `e0035:c01–c05`.

## Symptom / problem framing

Есть исходная оценка риска, затем появляется новая информация — например положительный или отрицательный тест на проникновение. Нужен способ **последовательно обновить вероятность**, не заменяя её интуитивной реакцией на один факт.

Авторы используют Bayes/conditional probability как механизм перехода:
`prior + evidence → posterior`.

## Baseline / context

Учебный сценарий содержит три бинарных состояния:

- **КУД** — крупная утечка данных в текущем году;
- **УЭУ** — наличие пока неизвестной удалённо эксплуатируемой уязвимости;
- **ПТП** — положительный тест на проникновение, указывающий на такую уязвимость.

Термины должны быть понятны, наблюдаемы и полезны для решения (`e0034:c03`).

### Базовые правила

- `P(A) + P(~A) = 1`
- если A и B независимы: `P(A,B) = P(A)P(B)`
- `P(A|B) = P(A,B)/P(B)`
- chain rule: `P(A,B,C)=P(A|B,C)P(B|C)P(C)`
- total probability: `P(A)=P(A|B)P(B)+P(A|~B)P(~B)`
- Bayes: `P(A|B)=P(A)P(B|A)/P(B)`

Источник: `e0035:c01–c02`.

## Read-only checks

1. События определены так, чтобы их можно было наблюдать?
2. Указан временной горизонт?
3. Какие вероятности — prior, какие — conditional inputs, какие — derived?
4. Не перепутаны ли `P(A|B)` и `P(B|A)`?
5. Есть ли доказательство независимости, прежде чем перемножать вероятности?
6. Какова вероятность наблюдения при наличии события и при его отсутствии?
7. Изменяет ли evidence итоговую вероятность в ожидаемую сторону?
8. Согласуются ли complement probabilities с правилом `P(A)+P(~A)=1`?
9. Числовые входы калиброваны или являются неподтверждёнными assumptions?
10. Есть ли достаточные данные, чтобы empirical evidence перевешивало prior?

Реальные probabilities, penetration-test sensitivity/specificity и risk thresholds организации: **[Needs confirmation]**.

## Interpretation

### P(A|B) не равно P(B|A)

Глава отдельно подчёркивает эту ошибку. Вероятность утечки при наличии уязвимости не равна вероятности наличия уязвимости при утечке. Formula Bayes связывает эти величины через base rates (`e0035:c02–c04`).

### Informative prior

Авторы используют калиброванные оценки CISO как **informative prior**: эксперт не знает исход наверняка, но имеет релевантный опыт. Non-informative prior обсуждается как максимально неопределённая starting point для бинарного состояния (в источнике — 50%), однако авторы отмечают, что такой prior может игнорировать полезное предварительное знание (`e0035:c02–c03`).

### Penetration test как evidence

В учебном примере:
- prior `P(КУД)=1,24%`;
- при positive test: `P(КУД|ПТП)=23,8%`;
- при negative test: `P(КУД|~ПТП)=1,01%`.

Таким образом test result **обновляет**, но не превращает вероятность в 0% или 100% (`e0035:c04–c05`).

## Next action

1. Определить target event и evidence event.
2. Зафиксировать prior до получения нового evidence.
3. Оценить/измерить conditional probabilities evidence при event и no-event.
4. Проверить base rates и complements.
5. Рассчитать posterior.
6. Проверить результат sanity-check'ом: evidence должен сдвигать вероятность согласно likelihood.
7. Сохранять prior, evidence, posterior и provenance входных значений.
8. При появлении новых наблюдений повторять update, а не переписывать историю исходных оценок.

Это аналитический flow главы, не готовая corporate risk policy.

## Modifying action

- Изменение spreadsheet/risk model — аналитически `state-changing`.
- Новый penetration test — потенциально `workload-generating` и в реальной среде может быть intrusive/security-sensitive.
- Глава **не даёт** команды запуска penetration testing, scope rules или authorization procedure.
- Production action, approval, test scope, credentials, data handling, rollback — **[Needs confirmation]**.

## Verification / acceptance checks

- Проверить арифметику всех derived values.
- Проверить, что probabilities остаются в диапазоне [0,1].
- Проверить prior/posterior против независимого расчёта или валидированного инструмента.
- Не принимать posterior как «измеренный факт», если его inputs — экспертные оценки.
- Проверять model calibration на последующих наблюдаемых исходах.

## Rollback

Для модели: сохранить предыдущую версию prior/inputs и расчёта, чтобы можно было восстановить pre-update state и воспроизвести изменение.

Для penetration test / infrastructure actions готового rollback в главе нет: **[Needs confirmation]**.
