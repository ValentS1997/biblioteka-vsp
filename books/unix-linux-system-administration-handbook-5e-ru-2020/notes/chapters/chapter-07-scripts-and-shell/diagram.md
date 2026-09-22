# Диаграмма: от интерактивной команды к воспроизводимой автоматизации

~~~mermaid
flowchart TD
    A["Повторяемая административная задача"] --> B["Выполнить вручную и понять semantics"]
    B --> C["Собрать read-only / observable pipeline"]
    C --> D["Фильтровать и проверить candidates"]
    D --> E["Сгенерировать будущие modifying commands в STDOUT"]
    E --> F{"Output корректен?"}

    F -->|Нет| C
    F -->|Да| G{"Сложность задачи"}

    G -->|Simple command composition| H["sh script"]
    G -->|Structured data / richer logic| I["Python / Ruby"]

    H --> H1["args + validation + STDERR + exit codes"]
    H1 --> H2["bash -n / trace with -x when needed"]

    I --> I1["modules / functions / structured objects"]
    I1 --> I2["requirements.txt / Gemfile"]

    H2 --> J["Dependency/environment control"]
    I2 --> J

    J --> J1["virtualenv / Bundler / RVM"]
    J1 --> K["Git working tree"]
    K --> K1["git status / git diff"]
    K1 --> K2["git add → index"]
    K2 --> K3["git commit → repository history"]

    K3 --> L["Reproducible administrative procedure"]
    L --> M["Review / reuse / collaborate"]

    N["Regex/text processing"] --> C
    N --> N1["cut / sort / uniq / wc / tee / grep / tail"]
    N1 --> C
~~~

## Смысл диаграммы

Глава связывает shell, scripting languages, dependency environments и Git в единую инженерную цепочку. Автоматизация начинается не с большого script, а с понятной command-line операции; затем появляются validation, reproducibility и version history.
