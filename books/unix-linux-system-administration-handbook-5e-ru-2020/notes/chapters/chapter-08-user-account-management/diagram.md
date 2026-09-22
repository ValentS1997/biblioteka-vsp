# Диаграмма: жизненный цикл учетной записи

~~~mermaid
flowchart TD
    A["Нужна новая identity"] --> B["Проверить authorization / local policy"]
    B --> C["Выделить unique login + UID/GID"]
    C --> D{"Local или centralized source?"}

    D -->|Local| E["passwd/shadow/group или master.passwd"]
    D -->|Centralized| F["LDAP / AD / identity system"]

    E --> G["Создать account и group membership"]
    F --> G

    G --> H["Назначить credential"]
    H --> I["Создать home + startup files"]
    I --> J["Set ownership / roles / privileges"]
    J --> K["Login as new user"]
    K --> L{"Verification passed?"}

    L -->|Нет| M["Исправить account/home/group/policy"]
    M --> K
    L -->|Да| N["Record in administrative source of truth"]

    N --> O{"Lifecycle event"}
    O -->|Temporary suspension| P["Lock account"]
    P --> Q["Проверить все access paths"]

    O -->|Offboarding| R["Preserve business data"]
    R --> S["Remove jobs/processes/mail/group refs"]
    S --> T["Remove account"]
    T --> U["find -xdev -nouser"]
    U --> V["Verify no orphaned ownership/access"]

    O -->|Organization scale| W["Centralize identity"]
    W --> X["LDAP / AD / SSO / IAM"]
    X --> Y["Audit + role mapping + rapid deprovisioning"]
~~~

## Смысл диаграммы

Глава рассматривает account management как lifecycle. Создание записи недостаточно: identity должна согласоваться с UID/GID, authentication, group membership, home ownership, roles и внешними системами. Offboarding требует отдельного контролируемого процесса с сохранением нужных данных и проверкой orphaned files.
