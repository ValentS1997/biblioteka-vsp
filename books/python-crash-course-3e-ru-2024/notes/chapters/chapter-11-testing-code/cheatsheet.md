# Шпаргалка главы 11 — Тестирование кода

## Baseline

Минимальный pytest test:

~~~python
from name_function import get_formatted_name

def test_first_last_name():
    formatted_name = get_formatted_name('janis', 'joplin')
    assert formatted_name == 'Janis Joplin'
~~~

Discovery rules source:
- filename начинается с `test_`;
- test function начинается с `test_`.

## Test lifecycle

1. Определить expected behavior.
2. Вызвать test subject.
3. Сохранить actual result.
4. Выполнить `assert`.
5. Запустить pytest.
6. При failure читать имя теста, failing line и exception.
7. Если expectation корректен — исправлять production code.
8. Перезапустить test suite.

## Regression rule

Source pattern:

- функция работала для first + last;
- добавление обязательного middle ломает прежний call shape;
- существующий test падает;
- production code меняется так, чтобы middle стал optional;
- старый test снова green;
- добавляется новый test для first + middle + last.

## Assertions

~~~python
assert a == b
assert a != b
assert a
assert not a
assert item in items
assert item not in items
~~~

## Class testing

~~~python
survey = AnonymousSurvey(question)
survey.store_response('English')
assert 'English' in survey.responses
~~~

Для нескольких значений:

~~~python
for response in responses:
    assert response in survey.responses
~~~

## Fixture

~~~python
import pytest

@pytest.fixture
def language_survey():
    question = "What language did you first learn to speak?"
    return AnonymousSurvey(question)

def test_store_single_response(language_survey):
    language_survey.store_response('English')
    assert 'English' in language_survey.responses
~~~

Fixture создаёт reusable resource и передаётся test function через parameter.

## Failure interpretation

Провал теста — не инструкция автоматически менять test.

Сначала проверить:
- expectation теста всё ещё корректен?
- изменение production code нарушило старое behavior?
- failure вызван test environment/dependency?
- нужен новый test для нового behavior?

## Coverage boundary

Source:
- full coverage может быть сложным;
- для крупных/важных проектов стремление к широкому coverage полезно;
- в ранних проектах достаточно критических аспектов поведения.

## Package-change boundary

~~~text
python -m pip install --upgrade pip
python -m pip install --user pytest
~~~

Это modifying actions для Python environment.

Перед запуском в реальном окружении:
- interpreter/environment: `[Needs confirmation]`;
- current pip/pytest state: `[Needs confirmation]`;
- rollback/version pin: `[Needs confirmation]`.

В artifacts команды сохраняются как source material, не как автоматически одобренное изменение текущей системы.
