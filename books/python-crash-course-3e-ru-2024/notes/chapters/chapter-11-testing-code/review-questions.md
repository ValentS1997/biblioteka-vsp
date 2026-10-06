# Упражнения главы 11

Source provenance:

- EPUB spine item: `20`
- locator: `OEBPS/Text/978544614112-17.xhtml`
- exercise chunks: `e0020:c06`, `e0020:c10`

## 11.1. Город, страна

Создайте функцию, возвращающую строку вида `"Santiago, Chile"`, и сохраните её в `city_functions.py`.

Создайте `test_cities.py` и test function `test_city_country()`, проверяющую пример с `'santiago'` и `'chile'`.

Запустите pytest и подтвердите, что test проходит.

Примечание: source prose перечисляет параметры как «страна, город», тогда как пример значений/название test ориентируют на `city, country`; это зарегистрировано как source mismatch.

## 11.2. Население

Измените функцию так, чтобы population стал третьим обязательным параметром и строка имела вид:

`Santiago, Chile - population 5000000`

Снова запустите прежний test и подтвердите failure.

Затем:
- сделайте population optional;
- подтвердите, что старый test снова проходит;
- добавьте `test_city_country_population()`;
- проверьте вызов с `'santiago'`, `'chile'`, `population=5000000`.

## 11.3. Штат компании

Создайте `Employee`:
- `__init__()` сохраняет first name, last name, annual salary;
- `give_raise()` по умолчанию увеличивает salary на 5000;
- method принимает custom raise.

Создайте tests:
- `test_give_default_raise()`;
- `test_give_custom_raise()`.

Source отдельно требует использовать `setUp()`, чтобы не создавать Employee заново в каждом test method. При этом глава обучает pytest fixtures и не объясняет `setUp()`; mismatch зарегистрирован в `source-findings.md`.

Нумерация и требования сохранены по RAG.
