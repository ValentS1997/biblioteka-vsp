# Глава 11 — operational cheatsheet

**Источник:** принятый RAG PDF 434–464; [provenance и границы](README.md). Версии ПО, команды и расположение файлов относятся к описанной учебной среде, не являются подтверждённой актуальной процедурой обновления.

## Symptom / problem framing

| Симптом / задача | Первая проверка | RAG |
|---|---|---|
| Во время обслуживания продолжаются уведомления | Есть ли активное maintenance window, совпадает ли host group, включено ли у action `Pause operations for suppressed problems`? | [p0435](../../../rag/chunks/p0401-p0500/p0435-c01.md)–[p0437](../../../rag/chunks/p0401-p0500/p0437-c01.md) |
| Backup «создан», но неполон | Скопированы `/etc/zabbix`, web/PHP, `/usr/lib/zabbix`, дамп DB? Достаточно ли свободного места и есть ли copy вне host? | [p0438](../../../rag/chunks/p0401-p0500/p0438-c01.md)–[p0441](../../../rag/chunks/p0401-p0500/p0441-c01.md) |
| Cron backup не появляется | Проверить пути назначения, включая отсутствующий `web-config`, переносы строк, права DB и stderr `>/dev/null` | [p0439](../../../rag/chunks/p0401-p0500/p0439-c01.md)–[p0440](../../../rag/chunks/p0401-p0500/p0440-c01.md) |
| Upgrade не начинается / frontend несовместим | Реальные версии `zabbix_server`, `php-fpm`, `mariadb` и версионные требования конкретного релиза | [p0442](../../../rag/chunks/p0401-p0500/p0442-c01.md)–[p0454](../../../rag/chunks/p0401-p0500/p0454-c01.md) |
| После upgrade сервис не Active | `systemctl status zabbix-server`, `tail -f /var/log/zabbix/zabbix_server.log`, frontend; **не продолжать миграцию без расследования** | [p0451](../../../rag/chunks/p0401-p0500/p0451-c01.md)–[p0454](../../../rag/chunks/p0401-p0500/p0454-c01.md) |
| Discovery worker близок к 100 % | `Utilization of discovery worker internal processes, in %`, число и стоимость LLD rules, CPU/RAM/DB connections | [p0455](../../../rag/chunks/p0401-p0500/p0455-c01.md)–[p0462](../../../rag/chunks/p0401-p0500/p0462-c01.md) |
| Housekeeper постоянно занят | `HousekeepingFrequency`, `MaxHousekeeperDelete`, сроки history/trends, DB/partitioning | [p0457](../../../rag/chunks/p0401-p0500/p0457-c01.md)–[p0463](../../../rag/chunks/p0401-p0500/p0463-c01.md) |
| MySQLTuner предлагает множество изменений | Изучить `Variables to adjust`, подтвердить workload/DB memory, не применять автоматически | [p0459](../../../rag/chunks/p0401-p0500/p0459-c01.md)–[p0463](../../../rag/chunks/p0401-p0500/p0463-c01.md) |

## Baseline / context

В книге Zabbix 7 поддерживается на работающем сервере; для учебного upgrade используется **lar-book-zbx6 с Zabbix 6** и Rocky Linux 8 или Ubuntu 22.04. PHP 8.2/8.3 и MariaDB 11.4 — **версии лабораторной цели издания**, а не проверенная рекомендация для текущего deployment ([p0434](../../../rag/chunks/p0401-p0500/p0434-c01.md), [p0442](../../../rag/chunks/p0401-p0500/p0442-c01.md), [p0450](../../../rag/chunks/p0401-p0500/p0450-c01.md)). Нужны подтверждённые бэкапы, достаточные ресурсы и окно возможного простоя.

## Read-only checks

- `Data collection → Maintenance` (просмотр): Active since/till, Periods, type, Host groups, Description. `Alerts → Actions`: checkbox suppression ([p0435](../../../rag/chunks/p0401-p0500/p0435-c01.md)–[p0437](../../../rag/chunks/p0401-p0500/p0437-c01.md)).
- `php-fpm --version`, `php --version`, `mysql --version`, `mariadb --version`, `zabbix_server --version`: **Read-only**, реальные версии перед любым изменением ([p0443](../../../rag/chunks/p0401-p0500/p0443-c01.md), [p0445](../../../rag/chunks/p0401-p0500/p0445-c01.md), [p0446](../../../rag/chunks/p0401-p0500/p0446-c01.md), [p0451](../../../rag/chunks/p0401-p0500/p0451-c01.md)).
- `dnf module list php`: **Read-only** в RHEL8, доступные streams; не заменяет проверку версий и совместимости из release notes ([p0443](../../../rag/chunks/p0401-p0500/p0443-c01.md)).
- `systemctl status zabbix-server`, `tail -f /var/log/zabbix/zabbix_server.log`: **Read-only**, последняя стадия upgrade и ошибка миграции ([p0451](../../../rag/chunks/p0401-p0500/p0451-c01.md)–[p0454](../../../rag/chunks/p0401-p0500/p0454-c01.md)).
- `Monitoring → Dashboard → Global view` / `Monitoring → Hosts → Latest data` и график discovery worker: read-only проверка загрузки ([p0455](../../../rag/chunks/p0401-p0500/p0455-c01.md)–[p0456](../../../rag/chunks/p0401-p0500/p0456-c01.md)).
- `Administration → Housekeeping`: прочитать сроки хранения; сравнить с retention item/шаблона ([p0462](../../../rag/chunks/p0401-p0500/p0462-c01.md)).
- Проверка существования/целостности backup за пределами этого рецепта: `[Needs confirmation]` (книга демонстрирует копирование/дампы, но не восстановление).

## Interpretation

- Maintenance: **`With data collection`** оставляет опрос данных и подавляет delivery при checkbox action. Фраза «для остановки сбора выбрать With data collection» в конце p437 **противоречит** ранее введённому `No data collection`, см. [source-findings.md](source-findings.md); сам `nodata` по книге не срабатывает в обоих режимах.
- Backup: frontend зависит от PHP/web server, server имеет отдельную конфигурацию, DB — отдельный dump. Наличие одного копируемого каталога не равно полной резервной копии ([p0441](../../../rag/chunks/p0401-p0500/p0441-c01.md)).
- Upgrade: Zabbix 6→7 в описанном рецепте выполняется после приведения PHP/DB к требуемым уровням; текущая package availability **не проверялась** ([p0445](../../../rag/chunks/p0401-p0500/p0445-c01.md), [p0450](../../../rag/chunks/p0401-p0500/p0450-c01.md)–[p0454](../../../rag/chunks/p0401-p0500/p0454-c01.md)).
- Processes: `StartDiscoverers=2` снижает очередь нескольких LLD rules на малой инсталляции, но требует CPU/RAM и возможно большего connection pool ([p0456](../../../rag/chunks/p0401-p0500/p0456-c01.md)–[p0462](../../../rag/chunks/p0401-p0500/p0462-c01.md)).
- History: `HousekeepingFrequency=2` и `MaxHousekeeperDelete=20000` — **пример**, а не универсальный optimum. DB partitioning/TimescaleDB в главе 12 ([p0458](../../../rag/chunks/p0401-p0500/p0458-c01.md)–[p0463](../../../rag/chunks/p0401-p0500/p0463-c01.md)).
- Async pollers: Agent, HTTP Agent, SNMP `walk[OID]`/`get[OID]`, `MaxConcurrentChecksPerPoller` до 1000 на один poller в книге ([p0464](../../../rag/chunks/p0401-p0500/p0464-c01.md)).

## Next action

1. Перед любой записью собрать baseline, оценить доступность rollback/restore и согласовать outage.
2. Создать ограниченное maintenance с нужной группой; проверить именно **Action suppression**, а не предположить его по названию окна.
3. Сделать корректный набор backup конфигураций/базы и независимую копию, подтвердить восстановимость.
4. Установить фактические требования целевых PHP/MariaDB/Zabbix **до** остановки служб; проводить upgrade строго по согласованной версии ОС.
5. После каждого этапа проверять статус, журнал и UI, затем производительность на том же workload.
6. Для busy housekeeper рассмотреть retention и partitioning, а не только увеличить интервалы.

## Modifying action

- `Create maintenance period` и настройка actions: **State-changing**, может скрыть нужные alerts; scope/time/checkbox критичны.
- `mkdir/cp/tar`, `mysqldump/pg_dump`: **State-changing** на стороне backup files, **Workload-generating** на DB; риск места/доступа к секретам и неконсистентности.
- `crontab -e`, `find ... -delete`: **State-changing**, последнее **Destructive**; не включать до теста путей и retention.
- `dnf module reset/enable`, `apt install`, `rpm`, MariaDB repos/upgrade, `systemctl stop/restart`: **State-changing / high-risk downtime**, исторические репозитории нельзя запускать вслепую.
- `StartDiscoverers=2`, `HousekeepingFrequency=2`, `MaxHousekeeperDelete=20000` и my.cnf настройки: **State-changing**, требуют контролируемого restart и измерения.

## Verification / acceptance checks

- Window ограничено нужными hosts/датами; датированный пример 2023 года не переносится без изменения.
- Action pause flags соответствуют политике; реальные важные alarms продолжают обрабатываться вне окна.
- Backup набор существует, доступ защищён, вынесен с хоста, restore test успешен (в главе **не показан**, должен быть спроектирован отдельно).
- Все версии совместимы, `zabbix-server` active, журналы без upgrade errors, frontend и last data доступны.
- Утилизация discovery и очередь уменьшились **без насыщения CPU/RAM/DB connections**.
- Housekeeping и retention удерживают рост DB; не исчерпаны время очистки и место, в длинном горизонте анализировать partitioning.

## Rollback

**Не дан** проверенный end-to-end rollback для PHP streams, MariaDB major migration, Zabbix schema upgrade, данных, удалённых housekeeper/retention cron, и `curl | bash` repository changes. Поэтому `[Needs confirmation]`. Использовать только отдельный утверждённый recovery plan, а не считать `systemctl restart` восстановлением. Дефекты команд и источника: [source-findings.md](source-findings.md).
