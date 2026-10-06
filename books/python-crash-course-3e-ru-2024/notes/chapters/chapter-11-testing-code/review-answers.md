# Разбор упражнений главы 11

Это RAG-grounded решения/шаблоны, не официальный ключ издателя.

## 11.1. Город, страна

Source parameter order неоднозначен; ниже используется `city, country`, поскольку expected call values идут как `'santiago', 'chile'` и expected result — `Santiago, Chile`.

`city_functions.py`:

~~~python
def city_country(city, country):
    return f"{city.title()}, {country.title()}"
~~~

`test_cities.py`:

~~~python
from city_functions import city_country

def test_city_country():
    formatted = city_country('santiago', 'chile')
    assert formatted == 'Santiago, Chile'
~~~

Run:

~~~bash
pytest
~~~

или source fallback:

~~~bash
python -m pytest
~~~

## 11.2. Население

Сначала intentionally breaking version:

~~~python
def city_country(city, country, population):
    return (
        f"{city.title()}, {country.title()} "
        f"- population {population}"
    )
~~~

После этого прежний `test_city_country()` должен fail из-за missing required argument.

Source-required compatible version:

~~~python
def city_country(city, country, population=''):
    if population:
        return (
            f"{city.title()}, {country.title()} "
            f"- population {population}"
        )

    return f"{city.title()}, {country.title()}"
~~~

Tests:

~~~python
from city_functions import city_country

def test_city_country():
    formatted = city_country('santiago', 'chile')
    assert formatted == 'Santiago, Chile'

def test_city_country_population():
    formatted = city_country(
        'santiago',
        'chile',
        population=5000000,
    )
    assert formatted == 'Santiago, Chile - population 5000000'
~~~

## 11.3. Штат компании

RAG полностью поддерживает production class:

~~~python
class Employee:
    def __init__(self, first_name, last_name, annual_salary):
        self.first_name = first_name
        self.last_name = last_name
        self.annual_salary = annual_salary

    def give_raise(self, amount=5000):
        self.annual_salary += amount
~~~

Поведение можно полностью проверить средствами pytest, уже показанными в главе:

~~~python
def test_give_default_raise():
    employee = Employee('anna', 'ivanova', 50000)
    employee.give_raise()
    assert employee.annual_salary == 55000

def test_give_custom_raise():
    employee = Employee('anna', 'ivanova', 50000)
    employee.give_raise(10000)
    assert employee.annual_salary == 60000
~~~

Этот вариант исполним и подтверждает два требуемых behavior, но **не удовлетворяет отдельному source-требованию использовать `setUp()`**.

Точная RAG-grounded implementation `setUp()` невозможна: глава не определяет этот mechanism и не показывает framework/API, которому он принадлежит. Поэтому canonical answer:

- production `Employee`: подтверждён source;
- test names и expected behavior: подтверждены source;
- executable pytest verification без shared setup: подтверждается изученным material;
- конкретная реализация `setUp()`: `[Needs confirmation]`;
- заменять `setUp()` fixture-ом как будто это исходное задание — нельзя.

Если придерживаться только изученного pytest flow, reusable Employee resource можно было бы оформить fixture по аналогии с `language_survey`, но это **interpretation**, а не дословное выполнение требования 11.3.
