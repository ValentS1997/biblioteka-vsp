# Диаграмма: уровни управления доступом

```mermaid
flowchart TD
    A["Запрос доступа или административная задача"] --> B{"Достаточно стандартной UNIX-модели?"}

    B -->|Да| C["DAC: UID/GID + owner/group + permissions"]
    C --> C1["Файлы / процессы / устройства"]
    C1 --> C2["Root: UID 0 — широкие полномочия"]
    C2 --> C3["setuid/setgid — привилегия только для конкретной программы"]

    B -->|Нет| D{"Нужна конкретная делегированная admin-операция?"}
    D -->|Да| E["sudo"]
    E --> E1["user + host + target user + command"]
    E1 --> E2["audit / logging"]
    E2 --> E3["visudo + exact paths + simple policy"]

    D -->|Нет| F{"Какой тип ограничения нужен?"}
    F --> F1["Authentication abstraction"]
    F1 --> G1["PAM"]
    F1 --> G2["Kerberos"]

    F --> F2["Fine-grained filesystem access"]
    F2 --> G3["ACL"]

    F --> F3["Разделить полномочия root"]
    F3 --> G4["Linux capabilities"]

    F --> F4["Изоляция видимости объектов"]
    F4 --> G5["Namespaces"]

    F --> F5["Централизованная mandatory policy"]
    F5 --> H["LSM / MAC / RBAC"]
    H --> H1["SELinux"]
    H --> H2["AppArmor"]

    E3 --> V["Проверить policy, audit trail и failure mode"]
    G1 --> V
    G2 --> V
    G3 --> V
    G4 --> V
    G5 --> V
    H1 --> V
    H2 --> V

    V --> R{"Boundary понятна и минимальна?"}
    R -->|Да| K["Применить и документировать"]
    R -->|Нет| X["Упростить policy / сузить привилегии / [Needs confirmation]"]
    X --> B
```

## Смысл диаграммы

Глава показывает не одну систему доступа, а последовательность уровней. Традиционная UNIX-модель остаётся базой, `sudo` решает задачу делегирования административных действий, а PAM/Kerberos/ACL/capabilities/namespaces закрывают отдельные ограничения классической модели. Когда требуется централизованная mandatory policy, подключаются LSM/MAC/RBAC-механизмы вроде SELinux и AppArmor.
