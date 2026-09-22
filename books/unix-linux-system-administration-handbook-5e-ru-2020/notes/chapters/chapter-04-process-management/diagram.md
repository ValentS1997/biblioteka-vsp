# Диаграмма: управление процессом от наблюдения до действия

```mermaid
flowchart TD
    A["Симптом: неизвестный / зависший / ресурсоёмкий process"] --> B["Идентифицировать: PID, PPID, UID, command"]
    B --> C["Snapshot: ps aux / ps lax"]
    C --> D["Continuous view: top + uptime"]

    D --> E{"Что наблюдаем?"}
    E -->|CPU / priority| F["CPU usage + NI"]
    E -->|Memory| G["VIRT / RES / DATA"]
    E -->|Disk full| H["df -h → du -h"]
    E -->|Неясное поведение| I["/proc/<PID>"]

    H --> H1{"df и du расходятся?"}
    H1 -->|Да| H2["fuser / lsof → open deleted file"]
    H1 -->|Нет| J["large file/directory identified"]

    I --> K{"Обычных данных достаточно?"}
    K -->|Нет| L["strace / truss"]
    K -->|Да| M["Сформировать гипотезу"]
    L --> M
    F --> M
    G --> M
    H2 --> M
    J --> M

    M --> N{"Нужно вмешательство?"}
    N -->|Нет| O["Документировать / наблюдать"]
    N -->|Priority| P["nice / renice"]
    N -->|Graceful stop| Q["TERM"]
    Q --> R{"Process завершился?"}
    R -->|Нет| S["KILL только после graceful attempt"]
    R -->|Да| T["Проверить recovery"]
    S --> T
    P --> T

    T --> U["Проверить resource usage и root cause"]

    V["Recurring task"] --> W{"Scheduler"}
    W -->|cron| X["crontab + explicit PATH/env + logs"]
    W -->|systemd| Y[".timer + .service / systemd-run"]
    X --> Z["Проверить execution + avoid synchronized load"]
    Y --> Z
```

## Смысл диаграммы

Глава строит управление процессами вокруг наблюдаемости. Process не следует останавливать только потому, что он выглядит подозрительно: сначала сохранить evidence, определить resource pattern и при необходимости трассировать syscalls. Signals и priority changes — controlled actions после diagnosis. Отдельная ветвь показывает recurring processes: scheduler должен быть таким же проверяемым объектом, как обычный process.
