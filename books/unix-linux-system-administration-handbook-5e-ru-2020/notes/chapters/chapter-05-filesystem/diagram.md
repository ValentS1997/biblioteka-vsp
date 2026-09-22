# Диаграмма: слои файловой системы и безопасное изменение

~~~mermaid
flowchart TD
    A["Задача с filesystem object"] --> B{"Какой слой меняется?"}

    B --> P["Path / namespace"]
    B --> M["Mount / filesystem attachment"]
    B --> T["Object type / links"]
    B --> R["Traditional mode / owner / group"]
    B --> F["Filesystem flags"]
    B --> C["ACL"]

    P --> P1["absolute / relative / current directory"]

    M --> M1["mount → inspect"]
    M1 --> M2{"umount busy?"}
    M2 -->|Да| M3["fuser / lsof"]
    M3 --> M4["устранить holders"]
    M4 --> V
    M2 -->|Нет| V

    T --> T1{"Hard или symbolic link?"}
    T1 -->|Hard| T2["same inode; same filesystem"]
    T1 -->|Symlink| T3["separate object; literal target"]

    R --> R1["ls -l / ls -ld"]
    R1 --> R2["chmod / chown / chgrp / umask"]
    R2 --> R3["проверить file vs directory semantics"]

    F --> F1["lsattr"]
    F1 --> F2["chattr only if justified"]

    C --> C1{"POSIX или NFSv4?"}
    C1 -->|POSIX| C2["getfacl → mask/effective rights → setfacl"]
    C1 -->|NFSv4| C3["getfacl -q/-qv → ordered ACE"]
    C3 --> C4["backup ACL → edit → replace"]

    P1 --> V["Verification"]
    T2 --> V
    T3 --> V
    R3 --> V
    F2 --> V
    C2 --> V
    C4 --> V

    V --> Q{"State соответствует intent?"}
    Q -->|Да| K["Документировать / оставить"]
    Q -->|Нет| X["Rollback из known-good state или [Needs confirmation]"]
~~~

## Смысл диаграммы

Главная практическая идея главы — сначала определить уровень abstraction. Ошибка в path, mount, link semantics, traditional permissions, filesystem flags и ACL выглядит как «проблема с файлом», но диагностируется и исправляется совершенно по-разному.
