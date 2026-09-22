# Команды главы 29

| Команда | Назначение | Что смотреть | Тип |
|---|---|---|---|
| `uptime` | Быстрая оценка общей нагрузки | `load average` | read-only |
| `top` | Интерактивный мониторинг CPU и процессов | CPU, load, `st`/steal time, процессы-лидеры | read-only |
| `ps auxww` | Поиск процессов, потребляющих ресурсы | CPU, память, подозрительные процессы | read-only |
| `vmstat 5 5` | CPU, память, paging/swap и I/O | `us`, `sy`, `id`, `wa`, `si`, `so`, `r`, `cs` | read-only |
| `mpstat -P ALL` | Нагрузка по отдельным CPU | дисбаланс между CPU, idle/iowait | read-only |
| `cat /proc/cpuinfo` | Инвентаризация CPU | модель, ядра, capabilities | read-only |
| `cat /proc/meminfo` | Информация о памяти | общий объём и использование RAM | read-only |
| `cat /proc/diskstats` | Низкоуровневая статистика дисков | активность блочных устройств | read-only |
| `dmidecode -t 4` | Данные о процессоре через DMI/SMBIOS | физическая конфигурация CPU | read-only, root обычно нужен |
| `ip a` | Сетевая конфигурация Linux | интерфейсы, IP/MAC | read-only |
| `ifconfig -a` | Сетевая конфигурация FreeBSD | интерфейсы, IP/MAC | read-only |
| `ss` | Состояние сетевых соединений в Linux | соединения и сокеты | read-only |
| `netstat` | Сетевая диагностика FreeBSD | соединения/сетевые показатели | read-only |
| `iostat` | Производительность дисковой подсистемы | transfers, read/write throughput | read-only |
| `fio <job>.fio` | Активное тестирование storage | IOPS, bandwidth, average/max latency | workload-generating |
| `lsof` | Связь процессов с открытыми файлами | кто работает с конкретными файлами/ФС | read-only |
| `fuser` | Процессы, использующие файловую систему | PID процессов | read-only |
| `sar` | Историческая статистика CPU | тренды во времени | read-only |
| `sar -d` | Историческая статистика дисков | активность дисков | read-only |
| `sar -n DEV` | Историческая статистика сети | интерфейсы | read-only |
| `sar -A` | Вся доступная статистика sar | комплексный обзор | read-only |
| `perf top` | Профилирование Linux в реальном времени | функции/ядро/процессы с CPU overhead | read-only, заметный overhead |
| `kill -STOP <PID>` | Временно остановить подозрительный процесс для проверки гипотезы | исчез ли симптом после остановки | state-changing |
| `renice` | Изменить CPU-приоритет процесса | влияние на конкуренцию за CPU | state-changing |
| `ionice -c 3 -p <PID>` | Понизить I/O-приоритет процесса | влияние процесса на дисковый I/O | state-changing |
| `ulimit -m <value>` | Ограничить физическую память последующих команд оболочки | потребление памяти | state-changing |
| `cat /sys/block/<disk>/queue/scheduler` | Посмотреть I/O scheduler Linux | активный scheduler в `[]` | read-only |
| `echo noop > /sys/block/<disk>/queue/scheduler` | Временно сменить I/O scheduler | сравнение latency/throughput до и после | state-changing |

## Рекомендуемая последовательность

`uptime` → `top` / `ps auxww` → `vmstat` → `mpstat` → `iostat` → `sar` → при необходимости `fio` / `perf`.

## Важное ограничение

Не менять scheduler, приоритеты процессов или параметры памяти только потому, что команда позволяет это сделать. Глава рекомендует сначала подтвердить bottleneck измерениями и иметь baseline для сравнения.
