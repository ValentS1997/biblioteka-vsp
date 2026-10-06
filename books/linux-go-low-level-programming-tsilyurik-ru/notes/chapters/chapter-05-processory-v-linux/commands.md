# Commands — глава 5 «Процессоры в Linux»

Только команды, присутствующие в chapter RAG.

| Команда | Класс | Назначение | Risk / effect | Verification |
|---|---|---|---|---|
| `cat /proc/cpuinfo` | read-only | Подробная CPU-информация ядра | Нет изменения | stdout |
| `lscpu` | read-only | CPU topology summary | Нет изменения | stdout |
| `lscpu -e` | read-only | CPU/NODE/SOCKET/CORE mapping | Нет изменения | таблица topology |
| `inxi -Cxxx` | read-only | Краткая CPU диагностика | Нет изменения | stdout |
| `inxi -C` | read-only | CPU summary | Нет изменения | stdout |
| `sensors coretemp-isa-*` | read-only | Температуры CPU | Нет изменения | sensors output |
| `gcc how-many-p.c -Wall -o how-many-p` | state-changing | Собрать process-affinity example | Создаёт binary | `./how-many-p` |
| `gcc how-many-t.c -Wall -lpthread -o how-many-t` | state-changing | Собрать pthread-affinity example | Создаёт binary | `./how-many-t` |
| `./how-many-p` | workload | Показать CPU count по process affinity | Выполняет local binary | stdout |
| `./how-many-t` | workload | Показать CPU count по thread affinity | Выполняет local binary | stdout |
| `taskset --help` | read-only | Справка affinity tool | Нет изменения | help |
| `taskset -p PID` | read-only | Получить affinity PID | Нет изменения | mask |
| `taskset -p 03 PID` | state-changing | Изменить affinity PID | Ограничивает CPU set | `taskset -p PID` |
| `taskset -pc 0,3,7-11 PID` | state-changing | Задать affinity list | Ограничивает CPU set | `taskset -p PID` |
| `taskset -c 0-3 ./how-many-p` | state-changing/workload | Запустить process с CPU list | Ограничивает CPU при запуске | output = 4 в примере |
| `taskset -c 1,3,5,7,9 ./how-many-t` | state-changing/workload | Запустить task с CPU list | Ограничивает CPU при запуске | output = 5 в примере |
| `nice --help` | read-only | Справка по nice | Нет изменения | help |
| `chrt --help` | read-only | Справка по scheduler tool | Нет изменения | help |
| `chrt -p PID` | read-only | Получить policy/priority | Нет изменения | stdout |
| `chrt -r 50 bash` | high-risk state-changing | Запустить bash с SCHED_RR/priority 50 | RT scheduling; возможна starvation | `chrt -p PID` |
| `chrt -r -p 5 PID` | high-risk state-changing | Изменить RT priority | Возможна starvation | `chrt -p PID` |
| `chrt -f 20 bash` | high-risk state-changing | Запустить bash с SCHED_FIFO | Высокий риск starvation | `chrt -p PID` |
| `chrt -r -p -r 10 PID` | high-risk state-changing | Изменить policy/priority | RT scheduling | `chrt -p PID` |
| `chrt -r -p -o 0 PID` | state-changing | Перевести показанный process к SCHED_OTHER/0 | Меняет scheduler policy | `chrt -p PID` |
| `ps` | read-only | Получить PID в примерах | Нет изменения | stdout |

## Risk boundary

Наиболее опасная часть главы — `chrt`.

Источник прямо объясняет, что активная real-time задача может блокировать получение CPU time обычными процессами. Поэтому эти команды не должны использоваться как «просто тест» на production/remote host без отдельного recovery channel.

## Rollback-first note

Перед изменением affinity или scheduler policy:

```bash
taskset -p <PID>
chrt -p <PID>
```

Сохранить вывод как rollback point.

Точные rollback-команды для произвольного исходного состояния источник не задаёт — **[Needs confirmation]**.
