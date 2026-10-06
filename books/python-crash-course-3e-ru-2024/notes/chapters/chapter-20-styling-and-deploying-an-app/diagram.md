# Диаграмма главы 20

~~~mermaid
flowchart TD
    A["Рабочий локальный Learning Log"] --> B["Подключить django-bootstrap5"]
    B --> C["Общий Bootstrap layout в base.html"]
    C --> D["Оформить index/login/topics/topic"]
    D --> E["Проверить локальную функциональность и responsive navbar"]

    E --> F["Подготовить deployment dependencies"]
    F --> F1["requirements.txt"]
    F --> F2["requirements_remote.txt: gunicorn + psycopg2"]

    F --> G["Создать Platform.sh configuration"]
    G --> G1[".platform.app.yaml"]
    G --> G2[".platform/routes.yaml"]
    G --> G3[".platform/services.yaml"]
    G --> H["Platform-specific settings.py"]
    H --> H1["ALLOWED_HOSTS"]
    H --> H2["STATIC_ROOT"]
    H --> H3["SECRET_KEY"]
    H --> H4["Postgres DATABASES"]

    H --> I["Подготовить Git"]
    I --> I1[".gitignore"]
    I --> I2["git init / add / commit"]
    I2 --> J{"git status clean?"}
    J -- "нет" --> I2
    J -- "да" --> K["platform create"]
    K --> L["platform push"]
    L --> M["platform url"]
    M --> N{"Deployment работает?"}
    N -- "нет" --> O["Исправить code/config"]
    O --> P["commit"]
    P --> L
    N -- "да" --> Q["platform environment:ssh"]
    Q --> R["createsuperuser"]

    R --> S["Production hardening"]
    S --> S1["DEBUG = False только в Platform.sh environment"]
    S1 --> T["commit → status → platform push"]
    T --> U["Проверить /topics/999/: без debug details"]

    U --> V["Добавить custom 404/500 templates"]
    V --> W["git add → commit → platform push"]
    W --> X["Проверить error pages"]

    X --> Y["Текущая разработка"]
    Y --> Z["local change → add if needed → commit → push → verify"]
    Z --> Y

    X --> AA{"Учебный deployment больше не нужен?"}
    AA -- "нет" --> Y
    AA -- "да" --> AB["Удалить Platform.sh project"]
    AB --> AC["При необходимости удалить Git remote reference"]
~~~

## Контрольные точки

1. Styling не должен менять основную Django data/view functionality.
2. Deployment configuration фиксируется до первого push.
3. Source требует clean Git working tree перед отправкой.
4. После push deployment проверяется через platform url и browser.
5. Production hardening проверяется отдельным повторным deployment.
6. Exact rollback для failed deployment в главе не задан; source использует corrective commit + повторный push.
