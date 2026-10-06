# Диаграмма — классы

## Class → instance

~~~mermaid
flowchart LR
    A["class Dog"] --> B["__init__(self, name, age)"]
    B --> C["instance my_dog"]
    C --> D["attributes: name, age"]
    C --> E["methods: sit(), roll_over()"]
~~~

## Mutation

~~~mermaid
flowchart TD
    A["attribute"] --> B{"Как менять?"}
    B -- "напрямую" --> C["instance.attribute = value"]
    B -- "с правилами" --> D["update_method(value)"]
    B -- "приращение" --> E["increment_method(delta)"]
    D --> F["validation"]
    F --> G{"Допустимо?"}
    G -- "Да" --> H["изменить state"]
    G -- "Нет" --> I["отклонить / message"]
~~~

## Reuse model

~~~mermaid
flowchart TD
    A["Новая модель"] --> B{"Это специализация существующего класса?"}
    B -- "Да" --> C["Inheritance"]
    C --> D["super().__init__()"]
    C --> E["new methods / override"]
    B -- "Нет: отдельная часть объекта" --> F["Composition"]
    F --> G["instance as attribute"]
~~~

## Modules

~~~mermaid
flowchart LR
    A["car.py"] --> B["from car import Car"]
    A --> C["import car"]
    D["electric_car.py"] --> E["from car import Car"]
    E --> F["class ElectricCar(Car)"]
~~~
