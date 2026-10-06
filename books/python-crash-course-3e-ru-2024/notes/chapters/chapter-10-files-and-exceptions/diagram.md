# Диаграмма — файлы и исключения

## Read flow

~~~mermaid
flowchart LR
    A["Path(file)"] --> B["read_text()"]
    B --> C["string"]
    C --> D["rstrip()/strip()"]
    C --> E["splitlines()"]
    E --> F["for line in lines"]
~~~

## Safe exception flow

~~~mermaid
flowchart TD
    A["Potentially failing operation"] --> B["try"]
    B --> C{"Success?"}
    C -- "Да" --> D["else"]
    D --> E["dependent code"]
    C -- "Нет" --> F{"Matching except?"}
    F -- "Да" --> G["message / pass / recovery"]
    F -- "Нет" --> H["unhandled exception / traceback"]
~~~

## Write boundary

~~~mermaid
flowchart TD
    A["Path(target)"] --> B{"Target confirmed?"}
    B -- "Нет" --> C["Do not write"]
    B -- "Да" --> D["write_text(contents)"]
    D --> E["Target created or overwritten"]
    E --> F["read-back verification"]
~~~

## Persistence

~~~mermaid
flowchart TD
    A["Path(username.json)"] --> B{"exists()?"}
    B -- "Да" --> C["read_text()"]
    C --> D["json.loads()"]
    D --> E["use stored data"]
    B -- "Нет" --> F["input()"]
    F --> G["json.dumps()"]
    G --> H["write_text()"]
    H --> E
~~~
