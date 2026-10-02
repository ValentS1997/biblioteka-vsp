# Диаграмма: рабочий цикл по главе 2

~~~mermaid
flowchart TD
    A["Задача в shell"] --> B["Определить текущий контекст"]
    B --> C["Read-only inspection"]
    C --> D{"Есть ошибка?"}
    D -->|Да| E["Сначала разобрать первую ошибку"]
    E --> C
    D -->|Нет| F{"Нужно изменение?"}
    F -->|Нет| G["Готово"]
    F -->|Да| H["Проверить target / path / PID / permissions"]
    H --> I["Минимальное изменение"]
    I --> J["Повторный read-only check"]
    J --> K{"Результат ожидаемый?"}
    K -->|Да| G
    K -->|Нет| L["Rollback если source-supported / иначе [Needs confirmation]"]
~~~

## Потоки shell

~~~mermaid
flowchart LR
    IN["stdin"] --> P1["process"]
    P1 --> OUT["stdout"]
    P1 --> ERR["stderr"]
    OUT --> P2["pipe → next process"]
    OUT --> FILE["redirect → file"]
    ERR --> EFILE["redirect → error file"]
~~~

## Процессы

~~~mermaid
flowchart LR
    A["ps → определить PID"] --> B["обычный signal"]
    B --> C["повторный ps"]
    C --> D{"Нужна временная остановка?"}
    D -->|Да| E["STOP → CONT"]
    D -->|Нет| F["завершить проверку"]
~~~

## Архив

~~~mermaid
flowchart LR
    A["archive"] --> B["Сначала listing/test mode"]
    B --> C{"Структура путей разумна?"}
    C -->|Да| D["Extract"]
    C -->|Неясно| E["Временный каталог перед extraction"]
~~~

## Иерархия каталогов

~~~mermaid
flowchart TB
    ROOT["/"] --> BIN["/bin"]
    ROOT --> DEV["/dev"]
    ROOT --> ETC["/etc"]
    ROOT --> HOME["/home"]
    ROOT --> LIB["/lib"]
    ROOT --> PROC["/proc"]
    ROOT --> RUN["/run"]
    ROOT --> SYS["/sys"]
    ROOT --> SBIN["/sbin"]
    ROOT --> TMP["/tmp"]
    ROOT --> USR["/usr"]
    ROOT --> VAR["/var"]
    ROOT --> BOOT["/boot"]
    ROOT --> MEDIA["/media"]
    ROOT --> OPT["/opt"]
~~~
