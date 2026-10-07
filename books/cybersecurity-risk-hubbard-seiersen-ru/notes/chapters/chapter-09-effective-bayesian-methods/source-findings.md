# Глава 9 — source findings

**Book:** `cybersecurity-risk-hubbard-seiersen-ru`. **Boundary:** EPUB spine 36–39. **Mode:** `rag_only`.

## F-01 — [Source wording/code mismatch] Несогласованная запись логарифма отношения шансов

- Locator: spine 38, `OPS/ch1-36.xhtml`, chunk `e0038:c02`.
- Вариант определения:
  ```text
  log(P(x)/(1 – P(x)
  ```
  — отсутствует закрывающая скобка.
- Затем источник пишет:
  ```text
  ЛОШ(P(Событие)) = ln(P(Событие)) / (1 – P(Событие))
  = ln(0,02 / 0,98)
  = –3,89182
  ```
  Первая символьная запись визуально ставит деление вне `ln()`, а следующая числовая запись — внутри.
- Для `P=0,04` источник даёт:
  ```text
  ln(0,04 / 0,96) = 3,17805
  ```
  при том что непосредственно выше утверждает: log-odds отрицателен при `P<0,5`. В следующем шаге delta используется значение `–3,18`.
- Решение: сохранить все варианты; не выбирать «правильную» форму/знак из model memory. Для практического использования требуется сверка с original layout/spreadsheet: **[Needs confirmation]**.

## F-02 — [Source wording/code mismatch] Описание состояния X расходится с Excel criterion

- Locator: spine 39, `OPS/ch1-37.xhtml`, chunk `e0039:c02`.
- Проза перед формулой говорит о вычислении `P(Y|X)` через число строк, где `Y=Да` и `X=Нет`, делённое на все строки, где `X=Нет`.
- Затем приводится формула:
  ```text
  = СЧЁТЕСЛИМН(столбец A; «=1»; столбец B; «=1»)
    / СЧЁТЕСЛИ(столбец B; «=1»)
  ```
- В доступном фрагменте нет однозначного mapping `1 ↔ Да/Нет` для X, который устранял бы расхождение.
- Решение: не менять `=1` на другой criterion и не переписывать prose; schema/value mapping будущего dataset — **[Needs confirmation]**.

## F-03 — [Source extraction issue] Figures/tables не доступны как полноценные мультимодальные объекты

В chapter RAG упомянуты, среди прочего:
- beta-distribution figures, включая рис. 9.2–9.4 (`e0037:c03–c06`);
- рис. 9.5 lens/regression comparison (`e0038:c06`);
- рис. 9.6 external empirical analysis (`e0039:c04`);
- табл. 9.1 node probabilities (`e0038:c01`);
- табл. 9.2 control-decision consequences (`e0039:c01`);
- табл. 9.3 binary event/condition data (`e0039:c02`).

Подписи и prose доступны, но полные axes, cells, points и original layout не реконструируются.

## F-04 — [External artifact not retrieved] Chapter spreadsheets

Источник многократно ссылается на downloadable Excel workbooks с сайта книги для beta distribution, ЛОШ, lens/value-of-information и empirical examples. Контракт `rag_only`: эти файлы не загружались, не исполнялись и не используются как silent correction layer.

## F-05 — [Source-context caution] External datasets/examples are historical source claims

AllClear ID, Verizon DBIR, HHS breach portal, password analysis и другие примеры описываются книгой в историческом контексте. В этой ветке они **не обновлялись по web** и не трактуются как current 2026 measurements.

**Итог:** canonical EPUB, checksum и RAG не изменялись.
