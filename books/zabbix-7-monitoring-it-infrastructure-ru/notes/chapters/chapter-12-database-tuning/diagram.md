# Глава 12 — схемы Mermaid, связанные с источником

Основание: **accepted RAG PDF 465–489**, прямой доступ к PDF/рисункам запрещён. Все диаграммы показывают **проверенные связи текста**, не представляют восстановленные UI-формы с иллюстраций.

## 1. Разделение задач по базе данных ([p0465](../../../rag/chunks/p0401-p0500/p0465-c01.md), [p0474](../../../rag/chunks/p0401-p0500/p0474-c01.md), [p0479](../../../rag/chunks/p0401-p0500/p0479-c01.md))

```mermaid
flowchart TD
  ISSUE["Большая Zabbix DB: housekeeper не справляется"] --> ENGINE{"Движок базы данных?"}
  ENGINE -- "MySQL/MariaDB" --> MYSQL["Временные partitions + Perl maintenance"]
  ENGINE -- "PostgreSQL" --> PG["TimescaleDB hypertables/chunks"]
  ISSUE --> NETWORK["Зашифровать удалённый DB transport?"]
  NETWORK --> TLS["CA + MariaDB SSL + Zabbix DBTLS verify_full"]
  MYSQL --> BACKUP["Перед модификацией: backup/restore, окно работ"]
  PG --> BACKUP
  TLS --> BACKUP
```

Шифрование связи — **отдельный** сценарий; его не надо выполнять после партиционирования как следующую обязательную стадию.

## 2. MySQL: daily history, monthly trends и автоматическое удаление ([p0467](../../../rag/chunks/p0401-p0500/p0467-c01.md)–[p0474](../../../rag/chunks/p0401-p0500/p0474-c01.md))

```mermaid
flowchart TD
  BASE["SELECT MIN(clock) для всех таблиц"] --> DATE{"NULL или более ранний timestamp?"}
  DATE -- "NULL" --> EMPTY["Пустая таблица: требуется отдельная оценка"]
  DATE -- "Есть значение" --> RANGE["Включить самую раннюю дату и будущее"]
  RANGE --> DDL["ALTER TABLE PARTITION BY RANGE(clock)"]
  DDL --> H["history, uint, str, text, log, bin: DAILY"]
  DDL --> T["trends, trends_uint: MONTHLY"]
  H --> PL["mysql_zbx_part.pl: $tables retention"]
  T --> PL
  PL --> DELETE["Удаление целых устаревших партиций"]
  PL --> FUTURE["Создать 10 будущих партиций"]
  PL --> VERIFY["journalctl, coverage, ingest"]
  VERIFY --> HOUSE["Только после PASS — отключить built-in housekeeper"]
```

Учебная политика retention: 30 дней/12 месяцев. Длительная DDL и безвозвратная очистка требуют backup. SQL `'history_uint'` из p467 имеет дефект синтаксиса.

## 3. PostgreSQL + TimescaleDB ([p0474](../../../rag/chunks/p0401-p0500/p0474-c01.md)–[p0479](../../../rag/chunks/p0401-p0500/p0479-c01.md))

```mermaid
flowchart TD
  START["Проверить совместимость PostgreSQL / TimescaleDB"] --> PKG["Packages + timescaledb-tune"]
  PKG --> DB["Создать Zabbix role + database"]
  DB --> EXT["CREATE EXTENSION timescaledb"]
  EXT --> SQL["Zabbix timescaledb.sql schema"]
  SQL --> ACCESS["pg_hba.conf + Zabbix DB credentials"]
  ACCESS --> HYPER["Hypertables → time chunks"]
  HYPER --> HOUSE["Zabbix UI global Housekeeping retention"]
  HYPER --> COMP["Compression может уменьшить объём"]
```

Версии PostgreSQL 12/15 и broken package names из исходника не исправляются без проверки. Индивидуальная retention per item по тексту недоступна.

## 4. TLS: разделение сервера базы и сервера Zabbix ([p0480](../../../rag/chunks/p0401-p0500/p0480-c01.md)–[p0489](../../../rag/chunks/p0401-p0500/p0489-c01.md))

```mermaid
flowchart LR
  CA["Private CA root certificate"] --> DBCERT["MariaDB ssl-ca / ssl-cert / ssl-key"]
  CA --> ZCERT["Zabbix CAFile / CertFile / KeyFile"]
  DBCERT --> DB["lar-book-secure-db : MariaDB"]
  ZCERT --> ZBX["lar-book-secure-zbx : Zabbix server"]
  ZBX -->|"DBTLSConnect=verify_full"| DB
  FRONT["Zabbix web frontend"] -->|"TLS settings рисунка: RAG_MISS"| DB
  DB --> ID["MariaDB user@host REQUIRE SSL"]
  ZBX --> MATCH["DBHost / certificate name / CA match"]
  DB --> MATCH
```

Факты источника: CA срок 3650 дней, конечный сертификат — 365 дней; в p480 и p485 адреса DB account **не совпадают**, поэтому не делать автоматический cutover. Конфигурация TLS frontend представлена не текстом, а рисунком.

## 5. Риск-контур при работе с retention и сертификатами

```mermaid
flowchart TD
  CHANGE["Предлагаемая модификация DB"] --> SAFETY{"Backup проверен и rollback спланирован?"}
  SAFETY -- "Нет" --> STOP["BLOCK: без DDL/cron/TLS switch"]
  SAFETY -- "Да" --> TEST["Лаборатория / поддерживаемая версия / нагрузка"]
  TEST --> VALIDATE["Проверить source defects, имена и SQL"]
  VALIDATE --> APPLY["Контролируемая операция в окно"]
  APPLY --> CHECK["Latest data, ingest, partitions, TLS, журналы"]
  CHECK --> GATE{"Проверки прошли?"}
  GATE -- "Да" --> DONE["Документировать состояние и retention"]
  GATE -- "Нет" --> RECOVERY["Откат по локальному подтверждённому плану"]
```

Полный rollback в source RAG **отсутствует**, поэтому recovery вне рамок главы = `[Needs confirmation]`. [source-findings.md](source-findings.md).
