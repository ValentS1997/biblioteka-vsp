# Команды и конструкции главы 11

Только source-confirmed элементы из `e0020:c01–c11`.

## Обновление pip

~~~bash
python -m pip install --upgrade pip
~~~

Классификация: **state-changing package-management action**.

Effect: source описывает upgrade установленного pip.

Risk:
- меняет Python package environment;
- source output versions относятся к моменту написания книги;
- применимость к текущему interpreter/environment: `[Needs confirmation]`.

Verification source: успешный installation output.

Rollback: `[Needs confirmation]`.

## Установка pytest

~~~bash
python -m pip install --user pytest
~~~

Классификация: **state-changing package-management action**.

Source alternative при проблемах:

~~~bash
python -m pip install pytest
~~~

Risk: второй вариант меняет scope установки; конкретный target environment должен быть подтверждён.

## Запуск tests

~~~bash
pytest
~~~

Классификация: workload-generating / test execution.

Source fallback:

~~~bash
python -m pytest
~~~

если command `pytest` не найден.

## Один test file

~~~bash
pytest test_survey.py
~~~

Классификация: targeted test execution.

## Test file/function naming

~~~text
test_name_function.py
test_first_last_name()
~~~

Pytest discovery source rules:
- files: prefix `test_`;
- functions: prefix `test_`.

## Assert forms

~~~python
assert a == b
assert a != b
assert a
assert not a
assert item in items
assert item not in items
~~~

## Fixture

~~~python
@pytest.fixture
def language_survey():
    ...
~~~

и injection:

~~~python
def test_store_single_response(language_survey):
    ...
~~~

## Acceptance checks

- pytest discovers intended test file;
- expected number of tests collected;
- success summary matches expected test count;
- failure output identifies failing test and exception;
- after production-code fix, regression test returns green;
- newly supported behavior gets its own test.

## Source version boundary

Shown outputs mention Python 3.x.x / pytest 7.x.x and historical pip versions. Они являются source examples, а не verified current versions.
