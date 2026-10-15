# Глава 1 — команды и конфигурационные фрагменты из RAG

Источник: `zabbix-7-monitoring-it-infrastructure-ru:p0020:c01` … `:p0058:c01`, PDF 20–58. Следуйте **точно выбранной ветке дистрибутива**. Книга ориентируется на Rocky Linux 9 / Ubuntu 22.04 и Zabbix 7.0; актуальность репозиториев для конкретного окружения: `[Needs confirmation]`.

## Классы действий и границы

- **Read-only:** статус службы, просмотр журнала, чтение информации UI.
- **State-changing:** установка/запуск службы, редактирование конфигурации, SQL DDL/GRANT/импорт, правка HA/VIP.
- **Workload-generating:** повторный запрос веб-страниц/мастера и исследование виджетов создают небольшой прикладной трафик; специальных генераторов нагрузки в главе нет.
- Все данные вида `<DB_PASSWORD>`, `<SERVER_IP_OR_DNS>`, `<INTERFACE_NAME>` — **местозаполнители**, не запускать до подстановки. Внутренний тестовый IP из книги не является адресом пользователя.

## Обычная установка — MariaDB, Zabbix server

| Команда/параметр | Класс | Действие и проверка |
|---|---|---|
| `dnf clean all` / `apt update` | State-changing | Обновляет метаданные пакетной системы после добавления репозитория; [p0021](../../../rag/chunks/p0001-p0100/p0021-c01.md) |
| `wget https://downloads.mariadb.com/MariaDB/mariadb_repo_setup` | State-changing | Загружает script setup (запуск/доверие к источнику проверяются отдельно); [p0022](../../../rag/chunks/p0001-p0100/p0022-c01.md) |
| `chmod +x mariadb_repo_setup` / `./mariadb_repo_setup` | State-changing | Делает скрипт исполняемым и выполняет настройку репозитория; [p0022](../../../rag/chunks/p0001-p0100/p0022-c01.md) |
| `dnf install mariadb-server` или `apt install mariadb-server` | State-changing | Устанавливает сервер БД; [p0022](../../../rag/chunks/p0001-p0100/p0022-c01.md) |
| `systemctl enable mariadb` / `systemctl start mariadb` | State-changing | Автозапуск и запуск; [p0022](../../../rag/chunks/p0001-p0100/p0022-c01.md) |
| `mariadb-secure-installation` | State-changing | Защищённая первичная настройка БД; пароль должен храниться защищённо; [p0022](../../../rag/chunks/p0001-p0100/p0022-c01.md) |
| `dnf install zabbix-server-mysql zabbix-sql-scripts zabbix-selinux-policy` | State-changing | Устанавливает компоненты Zabbix на RHEL; строка пакетов показана в несколько строк — перечень восстановлен из контекста; [p0022](../../../rag/chunks/p0001-p0100/p0022-c01.md) |
| `apt install zabbix-server-mysql zabbix-sql-scripts` | State-changing | Устанавливает серверные пакеты Ubuntu; [p0022](../../../rag/chunks/p0001-p0100/p0022-c01.md) |
| `mysql -u root -p` | State-changing session | Открывает CLI для дальнейшего изменения БД; сама команда лишь инициирует подключение; [p0022](../../../rag/chunks/p0001-p0100/p0022-c01.md) |
| `vim /etc/zabbix/zabbix_server.conf` | State-changing (при сохранении) | Редактирование параметров DB; [p0023](../../../rag/chunks/p0001-p0100/p0023-c01.md) |
| `systemctl enable zabbix-server` / `systemctl start zabbix-server` | State-changing | Включает автозапуск и сервер; [p0024](../../../rag/chunks/p0001-p0100/p0024-c01.md) |
| `systemctl status zabbix-server` | Read-only | Подтверждает, что служба запускается; [p0024](../../../rag/chunks/p0001-p0100/p0024-c01.md) |
| `tail -f /var/log/zabbix/zabbix_server.log` | Read-only | Поток журнала Zabbix для диагностики старта; [p0024](../../../rag/chunks/p0001-p0100/p0024-c01.md) |

**Источник содержит повреждённый фрагмент RHEL `rpm -Uvh` на p21 (`кеhttps`).** Не восстанавливаем его молча и не объявляем пригодным для исполнения. В другом рецепте p33/p34 отображён вариант без вставки. Подробности: [source-findings.md](source-findings.md). Для Ubuntu RAG даёт `wget` URL пакета `zabbix-release_7.0-1+ubuntu22.04_all.deb`, `dpkg -i` и `apt update` ([p0021](../../../rag/chunks/p0001-p0100/p0021-c01.md)); версии внешнего URL не проверены.

### SQL — источник p23

```sql
create database zabbix character set utf8mb4 collate utf8mb4_bin;
create user zabbix@localhost identified by '<DB_PASSWORD>';
grant all privileges on zabbix.* to zabbix@localhost identified by '<DB_PASSWORD>';
set global log_bin_trust_function_creators = 1;
```

- **Все команды State-changing.** Создают БД, пользователя/права, временно меняют глобальный параметр (p23).
- Подстановка `<DB_PASSWORD>` заменяет литерал `password` из книги, а **не является оригинальным синтаксисом**. Совместимость `GRANT ... identified by` с конкретной MariaDB: `[Needs confirmation]`.
- После импорта книга возвращает `set global log_bin_trust_function_creators = 0;`; это явная обратная операция к временному переключению ([p0023](../../../rag/chunks/p0001-p0100/p0023-c01.md)).

Импорт в обычном и HA-рецепте **показан с двумя разными путями**, поэтому не предлагается одна безусловно верная строка для копирования:

```text
p23: /usr/share/zabbix-sql-scripts/mysql/server.sql.gz
p34: /usr/share/doc/zabbix-sql-scripts/mysql/server.sql.gz
```

Обе команды используют `zcat` + подключение MariaDB/MySQL (`--default-character-set=utf8mb4`); **State-changing**, эффект — начальная схема Zabbix; путь и права пользователя нужно проверить до импорта. См. [source-findings.md](source-findings.md).

Конфигурация обычного узла, значения книги ([p0024](../../../rag/chunks/p0001-p0100/p0024-c01.md)):

```ini
DBName=zabbix
DBUser=zabbix
DBPassword=<DB_PASSWORD>
```

Риск: несоответствие SQL-учётной записи и конфигурации не даст стартовать серверу. Проверка: `systemctl status` и `zabbix_server.log`. Полный rollback БД/пакетов: `[Needs confirmation]`.

## NGINX и мастер web frontend

Установка: `dnf module switch-to php:8.3`, `dnf install zabbix-web-mysql zabbix-nginx-conf` для RHEL ([p0025](../../../rag/chunks/p0001-p0100/p0025-c01.md)); для Ubuntu `apt install zabbix-frontend-php zabbix-nginx-conf` ([p0026](../../../rag/chunks/p0001-p0100/p0026-c01.md)). **State-changing**. Учтите необходимость доступности web-портов 80/443, обозначенную в книге (p26).

Редактируемые пути: `/etc/nginx/conf.d/zabbix.conf` (RHEL), `/etc/zabbix/nginx.conf` (Ubuntu). Изменяемые строки из p26, с переменной вместо конкретного IP:

```nginx
listen 80;
server_name <SERVER_IP_OR_DNS>;
```

**State-changing**; изменяет адрес и порт слушателя виртуального хоста. Команды p26: `systemctl enable nginx php-fpm` и `systemctl restart nginx php-fpm` (RHEL); `systemctl enable nginx`, `systemctl restart nginx php-fpm` (Ubuntu). Проверка: web wizard `http://<SERVER_IP>/` (возможное `:8080` для Ubuntu в источнике) и все prerequisites `OK` ([p0027](../../../rag/chunks/p0001-p0100/p0027-c01.md)–[p0030](../../../rag/chunks/p0001-p0100/p0030-c01.md)). Откат настройки веб-сервера: `[Needs confirmation]`.

## HA — Zabbix active/passive и frontend VIP

Файлы/параметры показаны в [p0035](../../../rag/chunks/p0001-p0100/p0035-c01.md)–[p0038](../../../rag/chunks/p0001-p0100/p0038-c01.md); любые адреса заменить параметрами окружения:

```ini
# zabbix_server.conf, узел HA1
DBHost=<DB_HOST>
DBPassword=<DB_PASSWORD>
HANodeName=lar-book-ha1
NodeAddress=<HA1_IP>
# узел HA2 использует HANodeName=lar-book-ha2 и NodeAddress=<HA2_IP>
```

**State-changing**. Общее хранилище MariaDB используется обоими серверными узлами. Команды запуска `systemctl enable zabbix-server` / `systemctl start zabbix-server` показаны в p36.

Для frontend VIP книга ставит `keepalived` (`dnf install -y keepalived` / `apt install keepalived`) и редактирует `/etc/keepalived/keepalived.conf`, задавая `vrrp_track_process chk_nginx` (`process nginx`, `weight 10`), `vrrp_instance ZBX_1`, `state MASTER/BACKUP`, `virtual_router_id 51`, `priority 244/243`, `advert_int 1`, VRRP-аутентификацию и виртуальный IP ([p0036](../../../rag/chunks/p0001-p0100/p0036-c01.md), [p0037](../../../rag/chunks/p0001-p0100/p0037-c01.md)). Пароль `auth_pass`, интерфейс и VIP — только `<VRRP_PASSWORD>`, `<INTERFACE_NAME>`, `<VIP>`. **State-changing; HA rollout требует контролируемого окна** `[Needs confirmation]`.

После запуска `systemctl enable nginx keepalived`, `systemctl start nginx keepalived` ([p0038](../../../rag/chunks/p0001-p0100/p0038-c01.md)) проверить `Reports → System information` и Zabbix-server log. Для демонстрации переключения в книге используются `systemctl stop nginx` (p40) и `systemctl start nginx` (p41); **State-changing / service-disrupting**, выполнять только в контролируемом сценарии с проверкой возврата VIP. Не рекомендовать как постоянный режим.

## UI без CLI-команд

- Read-only навигация: `Monitoring → Problems / Hosts / Latest data`; `Reports → System information`; `Administration → Queue` ([p0054](../../../rag/chunks/p0001-p0100/p0054-c01.md)–[p0058](../../../rag/chunks/p0001-p0100/p0058-c01.md)).
- State-changing по роли оператора: `Data collection → Hosts/Templates`, `Users → User roles`, `Alerts → Actions`, `Administration → General`. Изменения требуют соответствующих прав; глава здесь объясняет назначение, а не пошаговое внедрение ([p0056](../../../rag/chunks/p0001-p0100/p0056-c01.md)–[p0058](../../../rag/chunks/p0001-p0100/p0058-c01.md)).

**Итоговый критерий:** наблюдаемое состояние серверной службы и логов, доступный wizard/frontend, корректная БД; в HA — проверенный active/passive и VIP плюс осознанное ограничение одиночной БД. Полный откат всех файлов/установок/схемы: `[Needs confirmation]`.
