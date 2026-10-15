# Глава 11 — команды и действия UI (RAG-only)

**Источник:** PDF 434–464, принятый книжный RAG. Это справочник издания, **не готовый исполняемый сценарий**. `Read-only` — чтение; `Workload-generating` — создаёт запросы/выгрузки; `State-changing` — изменяет систему; `Destructive` — удаляет данные.

## 1. Maintenance

`Data collection → Maintenance → Create maintenance period → Periods → Host groups` — **State-changing**. В книге выбран `Linux servers` и еженедельное окно вторник 22:00–04:00 с ограничением до 31.12.2023. Для подавления оповещений у action нужен `Pause operations for suppressed problems` ([p0435](../../../rag/chunks/p0401-p0500/p0435-c01.md)–[p0437](../../../rag/chunks/p0401-p0500/p0437-c01.md)). Фраза источника об остановке сбора данных повторно упоминает `With data collection`: противоречие, [source-findings.md](source-findings.md).

## 2. Backup

Команды из [p0438](../../../rag/chunks/p0401-p0500/p0438-c01.md)–[p0439](../../../rag/chunks/p0401-p0500/p0439-c01.md) — **State-changing**, они создают новые каталоги и резервные файлы:

```sh
mkdir /opt/zbx-backup/
mkdir /opt/zbx-backup/database/
mkdir /opt/zbx-backup/zbx-config/
mkdir /opt/zbx-backup/nginx/
mkdir /opt/zbx-backup/lib/
mkdir /opt/zbx-backup/shared/
mkdir /opt/zbx-backup/shared/zabbix/
mkdir /opt/zbx-backup/shared/doc/
cp -r /etc/zabbix/ /opt/zbx-backup/zbx-config/
cp -r /etc/nginx/ /opt/zbx-backup/nginx/
cp -r /usr/share/zabbix/ /opt/zbx-backup/shared/zabbix/
cp -r /usr/share/doc/zabbix-* /opt/zbx-backup/shared/doc/
cp -r /usr/lib/zabbix/ /opt/zbx-backup/lib/
```

Для Apache пути могут отличаться: `/etc/httpd` или `/etc/apache2`. Книга рекомендует хранить backups **на другом разделе или машине**, а не ограничиваться `/opt` ([p0440](../../../rag/chunks/p0401-p0500/p0440-c01.md)).

```text
# Источник, DB backup:
mysqldump --add-drop-table --add-locks --extended-insert --single-transaction --quick -u USER -p DBNAME > BACKUP.sql
pg_dump DBNAME > BACKUP.bak
```

Это **Workload-generating** для БД и **State-changing** для backup-файла. Подставлять секреты в командную строку не требуется. Cron примеры p439–440 **не исполнять буквально**: `web-config` не создавался, есть сломанные переносы и пути; пароль MySQL встроен в расписание, `~/.pgpass` показан без безопасных прав. Очистка через `find ... -delete` — **Destructive**; безопасные правила retention и restore test: `[Needs confirmation]`.

## 3. Version readback и PHP

**Read-only**:

```sh
zabbix_server --version
php-fpm --version
php --version
mysql --version
mariadb --version
dnf module list php
```

RHEL8 AppStream источник предлагает `dnf module reset php` → `dnf module enable php:8.2` → `dnf update`; альтернативно REMI PHP 8.3. Всё это **State-changing**, доступность и безопасность сторонних RPM не проверены ([p0443](../../../rag/chunks/p0401-p0500/p0443-c01.md)–[p0444](../../../rag/chunks/p0401-p0500/p0444-c01.md)).

Ubuntu раздел предлагает подключить PPA, затем установить PHP 8.3. В тексте команды `apt install software-properties-common add-apt-repository ppa:ondrej/php` и `apt-key ... --recv- keys` **не подтверждены как корректный синтаксис**; [source-findings.md](source-findings.md). Выполнение команд изменения PHP может нарушить frontend.

## 4. MariaDB и Zabbix upgrade

Из [p0446](../../../rag/chunks/p0401-p0500/p0446-c01.md)–[p0454](../../../rag/chunks/p0401-p0500/p0454-c01.md) источник предлагает остановку `mariadb`, `nginx`, `zabbix-server`, настройку репозитория MariaDB **11.4** и пакетное обновление; в Ubuntu промежуточное удаление MariaDB-пакетов. Это **State-changing / high-impact downtime**, включая изменения schema/data. Подача удалённого скрипта настройки репозитория сразу в shell — **security-sensitive**, точные URL не проверялись.

Для Zabbix 6→7 source перечисляет `dnf upgrade zabbix-server-mysql zabbix-web-mysql zabbix-agent2` либо Ubuntu `apt install --only-upgrade zabbix-server-mysql zabbix-frontend-php zabbix-agent2`. Обязательно сохранить `zabbix_server.conf`; несовместимость пакетов/изменение схемы DB и rollback `[Needs confirmation]`.

**Read-only после обновления:**
```sh
systemctl status zabbix-server
tail -f /var/log/zabbix/zabbix_server.log
```

Исправность frontend и фактических collected values должна подтверждаться отдельно.

## 5. Тюнинг процессов и БД

Текст [p0455](../../../rag/chunks/p0401-p0500/p0455-c01.md)–[p0463](../../../rag/chunks/p0401-p0500/p0463-c01.md) предлагает редактировать `/etc/zabbix/zabbix_server.conf`:

```ini
StartDiscoverers=2
HousekeepingFrequency=2
MaxHousekeeperDelete=20000
```

Редактирование и `systemctl restart zabbix-server` — **State-changing**, влияет на доступность, нагрузку CPU/RAM и количество DB-соединений. После каждого изменения проверять `Utilization of discovery worker internal processes, in %`, очередь и DB. Числа — пример, не рекомендация для любой системы.

В [p0459](../../../rag/chunks/p0401-p0500/p0459-c01.md)–[p0460](../../../rag/chunks/p0401-p0500/p0460-c01.md) упомянут сторонний `mysqltuner.pl`, `perl mysqltuner.pl`, рекомендации `Variables to adjust`, редактирование `/etc/my.cnf.d/server.cnf` и перезапуск MariaDB. **Нельзя без проверки исполнять скачанный скрипт или автоматически применять его советы**.

При больших объёмах данных автор предлагает partitioning/TimescaleDB (глава 12), а в [p0464](../../../rag/chunks/p0401-p0500/p0464-c01.md) описывает async pollers и `MaxConcurrentChecksPerPoller`.

**Rollback:** источник не показывает проверенное восстановление после major MariaDB/Zabbix/PHP обновления, не предоставляет restore test или безопасные права на DB secrets. Эти процедуры требуют самостоятельного подтверждения, `[Needs confirmation]`.
