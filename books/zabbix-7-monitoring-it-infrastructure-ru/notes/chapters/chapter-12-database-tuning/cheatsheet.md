# Глава 12 — cheatsheet: изменение схемы, retention и TLS

**Строгий источник:** accepted RAG PDF 465–489; [границы и provenance](README.md). Операции `ALTER TABLE`, `DROP PARTITION` через скрипт, `timescaledb.sql` и смена TLS **не являются read-only**.

## Symptom / problem framing

| Признак | Возможная причина и проверка | RAG |
|---|---|---|
| База Zabbix растёт, housekeeper не успевает | Объём и возраст `history*`/`trends*`, размер таблиц, частота housekeeping, требования к retention | [p0465](../../../rag/chunks/p0401-p0500/p0465-c01.md)–[p0467](../../../rag/chunks/p0401-p0500/p0467-c01.md) |
| После партиционирования старые значения остаются или новые не поступают | Самая ранняя `clock`, покрытие диапазонов (включая будущие партиции), работоспособность Perl и cron | [p0467](../../../rag/chunks/p0401-p0500/p0467-c01.md)–[p0474](../../../rag/chunks/p0401-p0500/p0474-c01.md) |
| Скрипт `mysql_zbx_part.pl` не работает | Настройки schema/user/password, `$tables`, `$curr_tz`, зависимости Perl, `journalctl -t mysql_zbx_part` | [p0470](../../../rag/chunks/p0401-p0500/p0470-c01.md)–[p0472](../../../rag/chunks/p0401-p0500/p0472-c01.md) |
| TimescaleDB/Zabbix server не стартует после установки | Фактические версии PostgreSQL/TimescaleDB, extension, `timescaledb.sql`, `pg_hba.conf`, DBPassword и службы | [p0475](../../../rag/chunks/p0401-p0500/p0475-c01.md)–[p0478](../../../rag/chunks/p0401-p0500/p0478-c01.md) |
| Не устанавливается защищённое MariaDB-соединение | `DBTLSConnect=verify_full`, CA chain, CN/SAN/DBHost, user@host, client/server cert/key, доступ к файлам | [p0480](../../../rag/chunks/p0401-p0500/p0480-c01.md)–[p0488](../../../rag/chunks/p0401-p0500/p0488-c01.md) |
| Web frontend работает не так, как server | Настройки **frontend→DB** отдельно от **Zabbix server→DB**; форма frontend в рисунке = `RAG_MISS` | [p0487](../../../rag/chunks/p0401-p0500/p0487-c01.md)–[p0488](../../../rag/chunks/p0401-p0500/p0488-c01.md) |

## Baseline / context

Сначала зафиксировать **движок и версию СУБД**, базу Zabbix, текущие `housekeeper` и retention, минимальную и максимальную `clock`, свободное место и темп роста, окно DDL и наличие проверенного backup/restore. В книге MySQL-рецепт использует MariaDB на `lar-book-mysql-mgmt`, TimescaleDB на `lar-book-postgresql-mgmt`, шифрование между `lar-book-secure-zbx` и `lar-book-secure-db` ([p0465](../../../rag/chunks/p0401-p0500/p0465-c01.md)); названия/IP — **учебные**, не параметры рабочей системы.

## Read-only checks

- MySQL: `mysql -u root -p`; внутри клиента `USE zabbix;` и `SELECT FROM_UNIXTIME(MIN(clock)) FROM history;`, повторить для `history_uint/str/text/log/bin`, `trends` и `trends_uint`. **SELECT — Read-only**, соединение как root и `USE` само по себе не изменяет строки ([p0467](../../../rag/chunks/p0401-p0500/p0467-c01.md)–[p0469](../../../rag/chunks/p0401-p0500/p0469-c01.md)).
- `NULL` из `MIN(clock)` означает пустую таблицу; наиболее ранний `clock` определяет начальную партицию. Исторические даты **июнь 2023** из книги **не переносить** на текущие таблицы.
- `journalctl -t mysql_zbx_part` — **Read-only** локальное чтение лога; может показывать результат запуска, но не гарантирует сохранность данных ([p0472](../../../rag/chunks/p0401-p0500/p0472-c01.md)).
- Zabbix `Administration → Housekeeping` — **Read-only при просмотре** действующих настроек. Не выключать до проверки альтернативного контроллера ([p0472](../../../rag/chunks/p0401-p0500/p0472-c01.md), [p0478](../../../rag/chunks/p0401-p0500/p0478-c01.md)).
- Для PostgreSQL/TimescaleDB в книге **не приведена отдельная read-only SQL проверка** extension/chunks/размеров. Команды `CREATE EXTENSION`, `timescaledb-tune`, `timescaledb.sql` — **State-changing**. Проверка конкретных read-only SQL запросов для целевой среды = `[Needs confirmation]`.
- Для TLS убедиться в наличии CA/client/server files и полном совпадении имени `DBHost` и сертификата **не раскрывая** содержимого private key; в книге нет отдельной команды для проверки SAN или cipher — `[Needs confirmation]`.

## Interpretation

- **MySQL**: `history*` daily, `trends*` monthly; внешний script `mysql_zbx_part.pl` создаёт будущие партиции и **удаляет целые устаревшие**. Учебная retention — **30 дней history / 12 месяцев trends**; отдельные сроки items после этой схемы недоступны ([p0470](../../../rag/chunks/p0401-p0500/p0470-c01.md)–[p0474](../../../rag/chunks/p0401-p0500/p0474-c01.md)).
- **TimescaleDB**: PostgreSQL hypertables/chunks, глобальные retention настройки через Housekeeping и потенциальное сжатие. Индивидуальная retention per item также недоступна ([p0478](../../../rag/chunks/p0401-p0500/p0478-c01.md)–[p0479](../../../rag/chunks/p0401-p0500/p0479-c01.md)).
- **TLS**: зашифрованный транспорт к MariaDB для Zabbix server требует `DBTLSConnect=verify_full`, `DBTLSCAFile`, `DBTLSCertFile`, `DBTLSKeyFile`; отдельно проверяются MariaDB `ssl-ca/cert/key` и требование `REQUIRE SSL` у правильного DB user@host. Исходник содержит **разные IP** `10.16.16.171` и `10.16.16.152` — [source-findings.md](source-findings.md).

## Next action

1. Выбрать **один** сценарий: MySQL maintenance vs TimescaleDB vs TLS внешней MariaDB; они **не составляют одну последовательность**.
2. До DDL/partition maintenance проверить резервное копирование, восстановление, RPO/RTO, нагрузку, покрытие `clock` и границы данных; для MySQL исходник рекомендует `tmux` и может требовать остановки Zabbix server.
3. Перед Timescale миграцией сверить пакеты PostgreSQL 12/15 и слитые имена из RAG; остановиться при несовпадении версии/schema.
4. Перед TLS cutover составить матрицу двух IP/хостов, `user@host`, CA-chain, имён и ключей; **не переносить** ошибочный p485 IP.

## Modifying action

| Действие | Класс | Существенный риск |
|---|---|---|
| `ALTER TABLE … PARTITION BY RANGE(clock)` | **State-changing / high-risk DDL** | Длительная блокировка/нагрузка, неправильный диапазон, потеря возможности ingest при отсутствии нужной партиции; [p0468](../../../rag/chunks/p0401-p0500/p0468-c01.md)–[p0469](../../../rag/chunks/p0401-p0500/p0469-c01.md) |
| `mysql_zbx_part.pl` и `55 22 * * *` в cron | **Destructive / recurring** | Автоматически удаляет старые партиции целиком; credentials в Perl конфиге; скрипт внешнего источника не верифицирован; [p0470](../../../rag/chunks/p0401-p0500/p0470-c01.md)–[p0474](../../../rag/chunks/p0401-p0500/p0474-c01.md) |
| Отключить `History/Trends` housekeeper | **State-changing / retention control** | При неисправном внешнем скрипте БД перестанет очищаться; [p0472](../../../rag/chunks/p0401-p0500/p0472-c01.md) |
| `timescaledb-tune`, `CREATE EXTENSION`, `timescaledb.sql`, `pg_hba.conf` | **State-changing / database access** | Изменение параметров PostgreSQL, схемы, возможности подключения; в книге версии/строки противоречат друг другу; [p0475](../../../rag/chunks/p0401-p0500/p0475-c01.md)–[p0478](../../../rag/chunks/p0401-p0500/p0478-c01.md) |
| Создать CA, CSR, ключи, `REQUIRE SSL`, MariaDB/Zabbix restart | **State-changing / security-sensitive** | Перерыв связи, неправильные права на ключи и неверное имя/IP нарушают доступ; [p0482](../../../rag/chunks/p0401-p0500/p0482-c01.md)–[p0487](../../../rag/chunks/p0401-p0500/p0487-c01.md) |

## Verification / acceptance checks

- Подтверждено, что initial и future partition coverage **включает всю фактическую историю** и следующий ingest; после преобразования данные и очереди Zabbix на месте.
- Результат Perl-скрипта получен в `journalctl`, реальный cron/ретенция сверены; housekeeper переведён **только после** приемки альтернативы.
- Zabbix server и frontend работают на TimescaleDB, схема и extension реально готовы, политики хранения соответствуют заданным срокам.
- В TLS-сценарии MariaDB и сервер Zabbix используют одни и те же CA/имена; `verify_full` включён, сертификаты не истекли; отдельно проверен frontend-DB link.
- Проверены ошибки, backlog, свободный диск и последствия перевода на новую retention, с заранее документированными criteria rollback.

## Rollback

В главе **нет** исчерпывающего rollback преобразованной MySQL-схемы, удаления партиций/истории, переноса Timescale chunks или восстановления прежних подключений/TLS с гарантией нулевой потери. Для них `[Needs confirmation]`; резервная копия **до** операций обязательна по предупреждению книги. Не подменять восстановление удалённых данных возвратом настроек.

Регистр расхождений и `RAG_MISS`: [source-findings.md](source-findings.md). Статус чтения не изменяется.
