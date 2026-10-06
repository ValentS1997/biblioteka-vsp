# Упражнения главы 17

Source provenance:

- EPUB spine item: `27`
- locator: `OEBPS/Text/978544614112-24.xhtml`
- exercise chunk: `e0027:c10`

## 17.1. Другие языки

Измените query в `python_repos.py`, чтобы визуализировать популярные repositories на других языках.

Source examples:
- JavaScript;
- Ruby;
- C;
- Java;
- Perl;
- Haskell;
- Go.

Live results/counts/stars: `[Needs confirmation]`.

## 17.2. Активные обсуждения

На основе `hn_submissions.py` создайте bar chart:
- высота = comments count;
- label = article title;
- label служит ссылкой на discussion page;
- `KeyError` для posts без comments должен обрабатываться через `try-except`.

## 17.3. Тестирование python_repos.py

Создайте `test_python_repos.py` с pytest.

Обязательная source check:
- `status_code == 200`.

Source также предлагает придумать дополнительные проверки, например:
- число returned items соответствует expected;
- total repositories выше выбранного threshold.

Dynamic expected values/threshold source не фиксирует.

## 17.4. Дальнейшие исследования

Изучите Plotly/GitHub API/Hacker News API docs:
- измените formatting;
- загрузите другие data;
- создайте собственные visualizations;
- при желании исследуйте public APIs repository.

В режиме `rag_only` external docs/other APIs не открывались.

Нумерация и требования сохранены по RAG.
