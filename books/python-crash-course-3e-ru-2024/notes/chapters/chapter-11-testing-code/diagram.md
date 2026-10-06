# Диаграмма — тестирование кода

## Test loop

~~~mermaid
flowchart TD
    A["Expected behavior"] --> B["Write test_* function"]
    B --> C["Call production code"]
    C --> D["assert actual == expected"]
    D --> E["Run pytest"]
    E --> F{"Pass?"}
    F -- "Да" --> G["Behavior covered by this test"]
    F -- "Нет" --> H["Read failing test / line / exception"]
    H --> I{"Expectation still valid?"}
    I -- "Да" --> J["Fix production code"]
    J --> E
    I -- "Нет" --> K["Re-evaluate test requirement"]
~~~

## Regression example

~~~mermaid
flowchart LR
    A["first + last works"] --> B["existing test"]
    C["add required middle"] --> D["existing test fails"]
    D --> E["make middle optional"]
    E --> F["old test passes"]
    F --> G["add 3-part-name test"]
~~~

## Fixture flow

~~~mermaid
flowchart LR
    A["@pytest.fixture"] --> B["fixture function"]
    B --> C["resource"]
    C --> D["test(resource)"]
    C --> E["another_test(resource)"]
~~~
