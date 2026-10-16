# Глава 12. Продвинутая настройка СУБД

**Книга:** «Zabbix 7: мониторинг ИТ-инфраструктуры»; inventory `0020`; `book_id=zabbix-7-monitoring-it-infrastructure-ru`.

## Границы и provenance

- **RAG-only**, источник — принятый Git RAG, `rag/acceptance.yaml: ACCEPTED`. Прямой PDF, внешние GitHub/документация/пакеты и память модели не используются для восполнения пробелов.
- **PDF 465–489 включительно**, первый chunk [p0465](../../../rag/chunks/p0401-p0500/p0465-c01.md), заключительная страница [p0489](../../../rag/chunks/p0401-p0500/p0489-c01.md); [глава 13 начинается p0490](../../../rag/chunks/p0401-p0500/p0490-c01.md). Chunk range `zabbix-7-monitoring-it-infrastructure-ru:p0465:c01`–`zabbix-7-monitoring-it-infrastructure-ru:p0489:c01`.
- Исходный SHA-256: `07204d885d4bf4c6c2de7c71ae42a4e3ed4cea794169cbe07985552e63875a27`. Corpus generation `6a5221f8e8a0f88b400905d7334879edff6f5451d9ab7f6e56bb203809018986`.
- Конкретные поля скриншотов 12.1–12.19 не доступны как структурированные данные: `RAG_MISS`.

## Карта трёх разделов

| Раздел | PDF | Цель и особенность |
|---|---:|---|
| [Партиционирование MySQL / MariaDB](../../../rag/chunks/p0401-p0500/p0466-c01.md) | 466–474 | `history*` по дням и `trends*` по месяцам; Perl script управляет созданием и удалением партиций |
| [Использование TimescaleDB](../../../rag/chunks/p0401-p0500/p0474-c01.md) | 474–479 | PostgreSQL/TimescaleDB extension, `timescaledb.sql`, гипертаблицы и чанки; retention через Zabbix UI |
| [Защита базы данных Zabbix](../../../rag/chunks/p0401-p0500/p0479-c01.md) | 479–489 | Отдельные серверы MariaDB/Zabbix, частный CA, ключи и сертификаты, `DBTLSConnect=verify_full` |

## 1. MySQL/MariaDB: временные партиции вместо построчной очистки

Стандартный Zabbix housekeeper удаляет устаревшие значения по строкам, что может создавать нагрузку в больших базах. В рецепте MySQL исторические таблицы `history`, `history_uint`, `history_str`, `history_text`, `history_log`, `history_bin` разбиваются **по дням**, а `trends` и `trends_uint` — **по месяцам**. У каждого типа таблиц сначала проверяют **самую раннюю временную метку `clock`**, включая случаи `NULL` и старые данные ([p0467](../../../rag/chunks/p0401-p0500/p0467-c01.md)–[p0469](../../../rag/chunks/p0401-p0500/p0469-c01.md)).

Учебный пример `ALTER TABLE history PARTITION BY RANGE(clock)` охватывает **11–18 июня 2023**, а `trends` — **июнь–август 2023**. Это **исторические примеры**, не диапазоны текущей базы. Операция DDL на крупном history может выполняться несколько дней, поэтому источник рекомендует резервное копирование, `tmux`, перенос на более мощную машину или остановку Zabbix server при невозможности безопасно выполнять преобразование онлайн ([p0466](../../../rag/chunks/p0401-p0500/p0466-c01.md)–[p0469](../../../rag/chunks/p0401-p0500/p0469-c01.md)).

После первоначального разбиения книга скачивает внешний `mysql_zbx_part.pl`, изменяет `$db_schema`, `$db_user_name`, `$db_password`, таблицы/retention (по умолчанию **30 дней history и 12 месяцев trends**) и `$curr_tz`; запускает его вручную, сверяет журнал `journalctl -t mysql_zbx_part`, затем планирует `55 22 * * * /usr/lib/zabbix/mysql_zbx_part.pl`. Только после подтверждения работы внешнего скрипта предлагается выключить встроенную очистку history/trends ([p0470](../../../rag/chunks/p0401-p0500/p0470-c01.md)–[p0472](../../../rag/chunks/p0401-p0500/p0472-c01.md)). Скрипт **удаляет целые старые партиции**, а также создаёт **10 будущих**; это быстро, но удаление охватывает все данные партиции и лишает возможности индивидуальной retention для каждого item ([p0473](../../../rag/chunks/p0401-p0500/p0473-c01.md)–[p0474](../../../rag/chunks/p0401-p0500/p0474-c01.md)).

**Критическое ограничение:** скачиваемый Perl файл **не исследован**; включать ежедневный cron и отключать housekeeper без проверенного backup/restore и dry-run запрещено. В SQL из p467 имена таблиц заключены в одинарные кавычки вместо обычных имён/идентификаторов — нельзя считать эти строки исполнимыми; [source-findings.md](source-findings.md).

## 2. PostgreSQL/TimescaleDB: гипертаблицы и чанки

На Ubuntu и RHEL источник устанавливает PostgreSQL и TimescaleDB, запускает `timescaledb-tune`, создаёт пользователя и базу `zabbix`, импортирует схему и активирует `CREATE EXTENSION IF NOT EXISTS timescaledb CASCADE`. Далее выполняет SQL из `/usr/share/doc/zabbix-sql-scripts/postgresql/timescaledb.sql`, настраивает `pg_hba.conf`, Zabbix server и `Administration → Housekeeping` ([p0474](../../../rag/chunks/p0401-p0500/p0474-c01.md)–[p0478](../../../rag/chunks/p0401-p0500/p0478-c01.md)).

В отличие от внешнего Perl-скрипта, здесь гипертаблица разбивается на **time chunks**, которыми может управлять TimescaleDB. Книга указывает две характеристики: потенциальное **сжатие данных** и возможность задавать **глобальную retention через Zabbix UI**, однако **разные сроки по отдельным items недоступны** ([p0479](../../../rag/chunks/p0401-p0500/p0479-c01.md)).

**Ограничения:** текст p475 устанавливает `timescaledb-2-postgresql-15`, но называет запуск «PostgreSQL 12»; p477 содержит слитые имена пакетов, p478 — разрывы строк правил `pg_hba.conf`. Это несогласованные части рецепта, а не проверенный playbook. В частности, изменение `pg_hba.conf` и миграция схемы требуют окна работ, контроля ролей и восстановления ([source-findings.md](source-findings.md)).

## 3. Защита внешней MariaDB: CA, серверные сертификаты и проверка имени

Модель угроз: MariaDB и Zabbix расположены на разных хостах, их трафик проходит по сети и может быть перехвачен. В источнике создаётся CA, ключи/CSR для обеих сторон, подписанные сертификаты, файлы размещаются на сервере БД и Zabbix server. MariaDB использует `ssl-ca`, `ssl-cert`, `ssl-key`, а сервер Zabbix задаёт [p0486](../../../rag/chunks/p0401-p0500/p0486-c01.md):

```ini
DBHost=lar-book-secure-db
DBName=zabbix
DBUser=zabbix
DBPassword=<SECRET_FROM_SECURE_STORE>
DBTLSConnect=verify_full
DBTLSCAFile=/var/lib/zabbix/ssl/cacert.pem
DBTLSCertFile=/var/lib/zabbix/ssl/zbx-srv.crt
DBTLSKeyFile=/var/lib/zabbix/ssl/zbx-srv.key
```

В книге CA генерируется на **3650 дней**, а конечные сертификаты подписываются на **365 дней**. Требуется своевременная замена, авторы предлагают контролировать срок действия средствами Zabbix ([p0482](../../../rag/chunks/p0401-p0500/p0482-c01.md)–[p0484](../../../rag/chunks/p0401-p0500/p0484-c01.md), [p0488](../../../rag/chunks/p0401-p0500/p0488-c01.md)).

**Важная исходниковая несогласованность:** p480 создаёт пользователя `zabbix@10.16.16.171`, p485 требует `alter user 'zabbix'@'10.16.16.152' require ssl;` — это разные адреса. Кроме того, p480 одновременно называет `lar-book-secure-db` хостом «только Zabbix» и MariaDB, хотя в вводной Zabbix установлен на `lar-book-secure-zbx`; p486 имеет повреждённый путь `cp` без пробела. Не исполнять буквально ([source-findings.md](source-findings.md)).

**Разграничение достигнутого:** источник утверждает, что данные Zabbix server и frontend к MariaDB передаются зашифрованно; при этом приведённый текст конфигурации Zabbix server **не доказывает отдельно** параметры TLS подключения frontend, поскольку поля показаны на рисунке 12.16 — `RAG_MISS` ([p0487](../../../rag/chunks/p0401-p0500/p0487-c01.md)–[p0489](../../../rag/chunks/p0401-p0500/p0489-c01.md)). Не приписывать браузерному доступу HTTPS на основании настройки DB TLS.

## Операционная приемка

1. До изменений: подтвердить тип СУБД, версию, объём данных и возраст `history*`/`trends*`, расписание retention, доступный объём, RPO/RTO, полноценный tested backup/restore.
2. Для MySQL выполнить согласованный план начального DDL; далее проверить партиции, внешний скрипт и его журнал; только после успешной приемки менять housekeeper/cron.
3. Для PostgreSQL проверить реально установленные версии PostgreSQL/TimescaleDB и SQL schema, загрузку extension, подготовку SQL, конфигурацию доступа и фактическую работоспособность Zabbix.
4. Для TLS отдельно удостовериться в соответствии IP пользователя, CN/SAN имён сертификатов, CA chain, ключей и прав; проверить соединения **server→DB и frontend→DB**, затем сроки сертификатов.
5. Зафиксировать влияние на задержки ingest, число ошибок, размер БД и успешность постоянного обслуживания; не удалять существующие данные для теста.

Файлы: [cheatsheet.md](cheatsheet.md) · [commands.md](commands.md) · [diagram.md](diagram.md) · [visual-cheatsheet.svg](visual-cheatsheet.svg) · [visual-cheatsheet-detailed.svg](visual-cheatsheet-detailed.svg) · [source-findings.md](source-findings.md).

**Граница:** нет подтверждённого source-end summary/review questions на p0489, p0490 начинает главу 13; условные файлы не создаются. Статус чтения **не меняется**. Контракты: chapter request v1.4, collection v1.8, publication v1.0, session recovery v1.0.
