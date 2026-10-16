# Глава 11 — Mermaid-диаграммы обслуживания и производительности

Основание: **RAG PDF 434–464, ACCEPTED**. Схемы отображают смысл текстовых инструкций, не параметры рисунков; значения только в графических формах = `RAG_MISS`.

## 1. Maintenance: подавление vs сбор данных ([p0435](../../../rag/chunks/p0401-p0500/p0435-c01.md)–[p0437](../../../rag/chunks/p0401-p0500/p0437-c01.md))

```mermaid
flowchart TD
  M["Data collection → Maintenance"]
  M --> TIMER["Active since/till + recurring Periods"]
  TIMER --> HOSTS["Выбранные host groups"]
  HOSTS --> MODE{"Maintenance type?"}
  MODE -- "With data collection" --> CONT["Сбор продолжается"]
  MODE -- "No data collection" --> STOP["Сбор прекращается: проверять по источнику"]
  CONT --> ACTION{"Action Pause operations for suppressed problems?"}
  ACTION -- "Включён" --> SILENCE["Подавление уведомлений во время окна"]
  ACTION -- "Не включён" --> ALERT["Риск оповещений во время окна"]
  STOP --> CHECK["nodata не срабатывает по тексту"]
```

В p437 **дважды назван `With data collection`** с противоположным назначением — второе упоминание помечено в [source-findings.md](source-findings.md).

## 2. Границы резервного копирования ([p0438](../../../rag/chunks/p0401-p0500/p0438-c01.md)–[p0441](../../../rag/chunks/p0401-p0500/p0441-c01.md))

```mermaid
flowchart TB
  SERVER["Zabbix stack"] --> CFG["Server /etc/zabbix"]
  SERVER --> WEB["NGINX / Apache config"]
  SERVER --> PHP["Frontend/PHP files + libraries"]
  SERVER --> DB["MySQL/MariaDB или PostgreSQL"]
  CFG --> BACKUP["Защищённая резервная копия"]
  WEB --> BACKUP
  PHP --> BACKUP
  DB --> DUMP["mysqldump / pg_dump"]
  DUMP --> BACKUP
  BACKUP --> OFF["Внешний диск/машина"]
  OFF --> RESTORE["Проверка восстановления: требуется отдельно"]
```

Cron строки источника имеют сломанные пути, секреты DB и возможное destructive удаление старых backup-файлов; ни один такой фрагмент не используется как production automation.

## 3. Последовательность upgrade ([p0442](../../../rag/chunks/p0401-p0500/p0442-c01.md)–[p0454](../../../rag/chunks/p0401-p0500/p0454-c01.md))

```mermaid
flowchart TD
  BASE["Check versions + release notes + backups"] --> PHP["PHP 8.2/8.3: учебная целевая версия"]
  PHP --> MARIA["MariaDB 11.4: учебная целевая версия"]
  MARIA --> ZBX["Zabbix server/front-end/agent 6→7"]
  ZBX --> STATUS["systemctl status + server log"]
  STATUS --> OK{"Ошибки / доступность?"}
  OK -- "Есть ошибки" --> HALT["Остановить продолжение; recovery plan"]
  OK -- "Норма" --> VERIFY["UI, Latest data и alerts"]
```

Схема **не является гарантированным путём обновления современной среды**: актуальные версии, миграции DB и rollback из текста не подтверждаются.

## 4. Анализ performance bottlenecks ([p0455](../../../rag/chunks/p0401-p0500/p0455-c01.md)–[p0464](../../../rag/chunks/p0401-p0500/p0464-c01.md))

```mermaid
flowchart TD
  OBS["Global view / Latest data"] --> HIGH{"Discovery utilization ≈100%?"}
  HIGH -- "Да" --> RULE["Проверить стоимость и количество LLD rules"]
  RULE --> CAP["Оценить CPU / RAM / DB connections"]
  CAP --> SCALE["StartDiscoverers=2 в учебной среде"]
  SCALE --> CHECK["Повторно оценить graph / queue"]
  HIGH -- "Нет" --> HK["Housekeeper / рост истории"]
  CHECK --> HK
  HK --> RET["History/trends retention"]
  RET --> HOUSE["HousekeepingFrequency=2, MaxHousekeeperDelete=20000: пример"]
  HOUSE --> LARGE{"Большая БД?"}
  LARGE -- "Да" --> PART["Partitioning MySQL / TimescaleDB — глава 12"]
  LARGE -- "Нет" --> TUNE["MySQLTuner — гипотезы, не готовые настройки"]
```

**Асинхронные pollers** в тексте: agent, HTTP-agent и SNMP `walk/get`, до 1000 проверок на poller в зависимости от `MaxConcurrentChecksPerPoller` — [p0464](../../../rag/chunks/p0401-p0500/p0464-c01.md). Масштабирование только числом процессов без устранения конфигурационных проблем неэффективно.

**Source policy:** без внешних данных и PDF-скриншотов; [source-findings.md](source-findings.md).
