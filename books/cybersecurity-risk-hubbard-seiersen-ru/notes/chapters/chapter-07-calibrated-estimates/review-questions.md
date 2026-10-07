# Глава 7 — упражнение по калибровке

**Тип:** source exercise transferred from chapter RAG.  
**Source:** EPUB spine 32, `OPS/ch1-30.xhtml`, `cybersecurity-risk-hubbard-seiersen-ru:e0032:c01–c04`.  
**Ответы источника:** spine 33, `OPS/ch1-31.xhtml`, `e0033:c04`.

## Инструкция из источника

Упражнение содержит **два набора по 10 вопросов**:

1. **90%-ные доверительные интервалы:** для каждого вопроса указать нижнюю и верхнюю границу так, чтобы, по вашей оценке, вероятность попадания истинного ответа внутрь составляла 90%.
2. **Бинарные вопросы:** выбрать «верно/неверно» и отдельно указать степень уверенности от 50% до 100%.

После заполнения предлагается использовать тест равноценной ставки и только затем смотреть правильные ответы.

## A. 90%-ные интервалы

**[Source extraction issue]**: строки таблицы 7.2 с текстами самих вопросов не представлены в доступном RAG. Нумерация восстанавливается только из source answer key; формулировки **не реконструируются**.

1. [Question text unavailable in RAG — Needs confirmation]
2. [Question text unavailable in RAG — Needs confirmation]
3. [Question text unavailable in RAG — Needs confirmation]
4. [Question text unavailable in RAG — Needs confirmation]
5. [Question text unavailable in RAG — Needs confirmation]
6. [Question text unavailable in RAG — Needs confirmation]
7. [Question text unavailable in RAG — Needs confirmation]
8. [Question text unavailable in RAG — Needs confirmation]
9. [Question text unavailable in RAG — Needs confirmation]
10. [Question text unavailable in RAG — Needs confirmation]

## B. Верно / неверно + confidence

1. [Question text unavailable in RAG — Needs confirmation]
2. [Question text unavailable in RAG — Needs confirmation]
3. [Question text unavailable in RAG — Needs confirmation]
4. [Question text unavailable in RAG — Needs confirmation]
5. [Question text unavailable in RAG — Needs confirmation]
6. [Question text unavailable in RAG — Needs confirmation]
7. [Question text unavailable in RAG — Needs confirmation]
8. [Question text unavailable in RAG — Needs confirmation]
9. [Question text unavailable in RAG — Needs confirmation]
10. [Question text unavailable in RAG — Needs confirmation]

## Scoring guidance из главы

- Для раздела A ожидается около **9 из 10** попаданий при истинном 90%-ном покрытии.
- Для раздела B ожидаемое число правильных ответов — сумма заявленных вероятностей.
- Один короткий тест не является окончательной оценкой навыка; источник использует повторение с feedback.

См. `source-findings.md` для ограничения table extraction.
