# Глава 12 — команды и UI: инвентаризация воздействий

**Источник:** accepted RAG, PDF 465–489. Команды приводятся **как материал книги, не как готовый производственный скрипт**. Риски классифицированы: Read-only, Workload-generating, State-changing, Destructive. По исходнику не проверялись сетевые репозитории, файлы Perl и скрипты SQL с внешних серверов.

## 1. MySQL/MariaDB: обследование и ручное разбиение

```sh
# State-changing: установка инструмента tmux при отсутствии
dnf install tmux
# или:
apt install tmux

# В отдельной терминальной сессии (не изменяет БД)
tmux

# Подключение с административными правами; никакой SQL ALTER без окна обслуживания
mysql -u root -p
```

Перечислено [p0466](../../../rag/chunks/p0401-p0500/p0466-c01.md)–[p0467](../../../rag/chunks/p0401-p0500/p0467-c01.md). Источник советует backup, альтернативные ресурсы и возможную остановку Zabbix server на время многодневного DDL. **Read-only** SQL для каждой таблицы (команды без кавычек вокруг имён являются *обобщённой схемой по источнику*; literal p467 с одинарными кавычками некорректен, см. findings):

```sql
USE zabbix;
SELECT FROM_UNIXTIME(MIN(clock)) FROM history;
SELECT FROM_UNIXTIME(MIN(clock)) FROM history_uint;
SELECT FROM_UNIXTIME(MIN(clock)) FROM history_str;
SELECT FROM_UNIXTIME(MIN(clock)) FROM history_text;
SELECT FROM_UNIXTIME(MIN(clock)) FROM history_log;
SELECT FROM_UNIXTIME(MIN(clock)) FROM history_bin;
SELECT FROM_UNIXTIME(MIN(clock)) FROM trends;
SELECT FROM_UNIXTIME(MIN(clock)) FROM trends_uint;
```

`NULL` = таблица пуста; сравнить earliest history **по дням** и earliest trends **по месяцам** ([p0467](../../../rag/chunks/p0401-p0500/p0467-c01.md)–[p0469](../../../rag/chunks/p0401-p0500/p0469-c01.md)). Перед `ALTER TABLE` следует проверить реальные типы/индексы/ключи таблиц `[Needs confirmation]`.

DDL, показанный в книге, **State-changing / high-risk**; НЕ выполнять на реальной базе по историческому диапазону:

```sql
-- ДЕМОНСТРАЦИЯ ФОРМЫ p468, не execution-ready план миграции
ALTER TABLE history PARTITION BY RANGE (clock)
 (PARTITION p2023_06_11 VALUES LESS THAN (UNIX_TIMESTAMP("2023-06-12 00:00:00")) ENGINE = InnoDB,
  PARTITION p2023_06_12 VALUES LESS THAN (UNIX_TIMESTAMP("2023-06-13 00:00:00")) ENGINE = InnoDB);
-- p468 содержит последовательность до p2023_06_18; она намеренно сокращена.
-- p469 использует PARTITION p2023_06, p2023_07, p2023_08 для trends.
```

При несовпадении ранней даты/нехватке будущей partition могут возникнуть ошибки/утрата ожидаемой возможности записи. Полный набор DDL для текущей базы и его rollback `[Needs confirmation]`.

## 2. Perl `mysql_zbx_part.pl`: внешний управляющий скрипт

Источник [p0470](../../../rag/chunks/p0401-p0500/p0470-c01.md)–[p0472](../../../rag/chunks/p0401-p0500/p0472-c01.md):

```sh
# Workload-generating: загрузка кода из внешнего GitHub (НЕ проверено)
wget https://raw.githubusercontent.com/OpensourceICTSolutions/zabbix-mysql-partitioning-perl/main/mysql_zbx_part.pl
# State-changing:
mkdir /usr/lib/zabbix/
mv mysql_zbx_part.pl /usr/lib/zabbix/
vim /usr/lib/zabbix/mysql_zbx_part.pl
chmod +x /usr/lib/zabbix/mysql_zbx_part.pl

# Destructive в зависимости от $tables/retention: запускает создание/удаление партиций
/usr/lib/zabbix/mysql_zbx_part.pl

# Read-only: просмотр сообщений скрипта
journalctl -t mysql_zbx_part

# State-changing: установка расписания через редактор cron
crontab -e
```

Пример задачи книги:

```cron
55 22 * * * /usr/lib/zabbix/mysql_zbx_part.pl
```

Переменные Perl: `$db_schema`, `$db_user_name`, `$db_password`, `$tables` (30 дней/12 месяцев по умолчанию), `$curr_tz`. **Нельзя коммитить пароль БД** или доверять непроверенному файлу. Внешний сценарий удаляет целые партиции. Зависимости RHEL в p471: `perl-Sys-Syslog`, `perl-DateTime`, `perl-DBD-mysql`, `perl-DBI`; Ubuntu `liblogger-syslog-perl`, `libdatetime-perl`; каждое `dnf/apt install` — **State-changing**. После accept — `Administration → Housekeeping` отключает очистку History/Trends (**State-changing**, риск бесконтрольного роста если cron не работает). Конкретные флажки рисунка 12.7 — `RAG_MISS`.

## 3. PostgreSQL/TimescaleDB

**Версионные/дистрибутивные строки p475–477 являются только учебным материалом**, требует подтверждения пакетов, подписей и совместимости. В частности, `apt install timescaledb-2-postgresql-15` соответствует PostgreSQL 15, но на той же p475 сказано «PostgreSQL 12». Команды `apt-key`, `repo_gpgcheck=1, gpgcheck=0`, сторонние источники, выключение модуля — security-sensitive.

```sh
# State-changing — авторский вариант установки в подходящей lab
apt install timescaledb-2-postgresql-15
# либо RHEL:
dnf -qy module disable postgresql
dnf install postgresql15 postgresql15-server
/usr/pgsql-15/bin/postgresql-15-setup initdb
dnf install timescaledb-2-postgresql-15

# State-changing: tuning + restart
timescaledb-tune
# При необходимости исходник предлагает:
timescaledb-tune --pg-config=/usr/pgsql-15/bin/pg_config
systemctl restart postgresql-15
```

Точные имена запущенных служб на Ubuntu/RHEL и безопасный порядок restart в реальной версии `[Needs confirmation]`.

SQL/команды включения TimescaleDB из [p0477](../../../rag/chunks/p0401-p0500/p0477-c01.md):

```sh
# State-changing: create database role and database
sudo -u postgres createuser --pwprompt zabbix
sudo -u postgres createdb -O zabbix zabbix

# State-changing: import Zabbix SQL schema (проверить точную версию архива)
zcat /usr/share/doc/zabbix-server-pgsql*/create.sql.gz | sudo -u zabbix psql zabbix

# State-changing: extension
echo "CREATE EXTENSION IF NOT EXISTS timescaledb CASCADE;" | sudo -u postgres psql zabbix

# State-changing: Zabbix-specific Timescale schema
gunzip /usr/share/doc/zabbix-sql-scripts/postgresql/timescaledb.sql.gz
cat /usr/share/doc/zabbix-sql-scripts/postgresql/timescaledb.sql | sudo -u zabbix psql zabbix
```

Источник также содержит слитые package names `zabbix-apacheconfzabbix-agent2` и `zabbix-frontend-phpphp-pgsql`, **не считать их валидными** ([p0476](../../../rag/chunks/p0401-p0500/p0476-c01.md)–[p0477](../../../rag/chunks/p0401-p0500/p0477-c01.md)).

`vim /etc/zabbix/zabbix_server.conf` с `DBHost=` / `DBPassword=<DB_SECRET>`, `vim /var/lib/pgsql/15/data/pg_hba.conf`, `systemctl restart ...`: всё **State-changing**, влияет на доступность БД. В p478 строки правил local/host и методов SCRAM/MD5 разорваны переносами — **не копировать** как целостный `pg_hba.conf`; см. [source-findings.md](source-findings.md). `Administration → Housekeeping` — позволяет менять глобальную retention на TimescaleDB; проверить version compatibility и реальные параметры.

## 4. MariaDB TLS, CA и ключи

Текст [p0480](../../../rag/chunks/p0401-p0500/p0480-c01.md)–[p0486](../../../rag/chunks/p0401-p0500/p0486-c01.md) создаёт две Linux машины, private CA и серверные сертификаты. Приведённые literal адреса `10.16.16.170` (MariaDB) и `10.16.16.171` (Zabbix) **пример**. Исходная команда `alter user 'zabbix'@'10.16.16.152' require ssl` **не совпадает** с созданным пользователем на p480 — нельзя использовать без проверки.

```sh
# State-changing / high sensitivity: private CA, server and client key material
mkdir -p /etc/pki/CA/private
openssl req -new -x509 -keyout /etc/pki/CA/private/cakey.pem -out /etc/pki/CA/cacert.pem -days 3650 -newkey rsa:4096
touch /etc/pki/CA/index.txt
echo 01 > /etc/pki/CA/serial
mkdir /etc/pki/CA/unsigned
mkdir /etc/pki/CA/newcerts
mkdir /etc/pki/CA/certs

# Source p483: Zabbix key/certificate request; -nodes means key unencrypted
openssl req -nodes -new -keyout /etc/pki/CA/private/zbx-srv_key.pem -out /etc/pki/CA/unsigned/zbx-srv_req.pem -newkey rsa:2048

# Source p484: cert signing (interactive; state changing)
openssl ca -policy policy_anything -days 365 -out /etc/pki/CA/certs/zbx-srv_crt.pem -infiles /etc/pki/CA/unsigned/zbx-srv_req.pem
```

Сюда **не включён исполняемый полный PKI playbook**: проверка SAN, роли client/server certificates, владельцев/криптографии, CA хранение, процедуры rotation и revoke отсутствуют. Файлы private keys не выводить, не хранить в repo. Пример p485 копирует *секретный ключ* через `scp` от root — **Security-sensitive**, не повторять без согласованной защиты.

MariaDB `/etc/my.cnf.d/server.cnf`, раздел `[mysqld]` ([p0485](../../../rag/chunks/p0401-p0500/p0485-c01.md)):

```ini
bind-address=lar-book-secure-db
ssl-ca=/etc/my.cnf.d/certificates/cacert.crt
ssl-cert=/etc/my.cnf.d/certificates/mysql-srv.crt
ssl-key=/etc/my.cnf.d/certificates/mysql-srv.key
```

Zabbix server `/etc/zabbix/zabbix_server.conf` ([p0486](../../../rag/chunks/p0401-p0500/p0486-c01.md)):

```ini
DBHost=lar-book-secure-db
DBName=zabbix
DBUser=zabbix
DBPassword=<SECURE_SECRET>
DBTLSConnect=verify_full
DBTLSCAFile=/var/lib/zabbix/ssl/cacert.pem
DBTLSCertFile=/var/lib/zabbix/ssl/zbx-srv.crt
DBTLSKeyFile=/var/lib/zabbix/ssl/zbx-srv.key
```

Реальное `ALTER USER ... REQUIRE SSL` — **State-changing**, должно относиться **точно к существующему user@host**, проверить соединение *перед* разрывом прежнего канала; `systemctl restart mariadb` / `systemctl restart zabbix-server ...` могут вызвать outage. p486 содержит ошибочные `cp` строки со слитными путями; не повторять.

## 5. Приёмка, rollback и оговорки

Проверить минимальные timestamps, покрытие partitions, доступность ingest, результаты журналов, housekeeper, PostgreSQL extension/chunks, MariaDB TLS verification и отдельно frontend connection. Полный rollback, lost historical data, безопасная переинициализация CA и схема резервного восстановления **не представлены**; `[Needs confirmation]`. Конфигурация/команды из внешних GitHub и пакетов не проверялись (RAG-only).
