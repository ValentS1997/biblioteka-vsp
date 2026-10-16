# Глава 1 — cheatsheet

Опора: RAG PDF pages **20–58**; исходный SHA-256 в [README](README.md). Действия ниже следуют главе; это не обобщённое руководство по всем версиям Zabbix.

## Symptom / problem framing

- **Zabbix server не запускается:** сначала проверить состояние systemd и журнал Zabbix ([p0024](../../../rag/chunks/p0001-p0100/p0024-c01.md)).
- **Нет страницы frontend:** проверить NGINX-конфигурацию, IP/DNS, порт и веб-мастер; глава упоминает возможную опечатку как причину ([p0026](../../../rag/chunks/p0001-p0100/p0026-c01.md), [p0027](../../../rag/chunks/p0001-p0100/p0027-c01.md)).
- **Мастер frontend не проходит prerequisites или подключение к БД:** не продолжать, пока параметры не покажут `OK` и соединение с MariaDB не соответствует созданным БД/учётной записи ([p0027](../../../rag/chunks/p0001-p0100/p0027-c01.md), [p0028](../../../rag/chunks/p0001-p0100/p0028-c01.md)).
- **В HA пропал frontend/сервер:** разделить отказ Zabbix server (active/passive и NodeAddress) от отказа NGINX/VIP (keepalived) и от отказа общей БД ([p0041](../../../rag/chunks/p0001-p0100/p0041-c01.md), [p0043](../../../rag/chunks/p0001-p0100/p0043-c01.md)).

## Baseline / context

Тестовая основа книги: Rocky Linux 9 или Ubuntu 22.04; MariaDB/MySQL, Zabbix server, NGINX/PHP frontend. Для обычной установки используется одна машина; для HA — два Zabbix server/frontend + одна MariaDB. Адреса из книги: `192.168.0.1`, `.2`, `.10`, VIP `.5` в той же учебной подсети ([p0020](../../../rag/chunks/p0001-p0100/p0020-c01.md), [p0031](../../../rag/chunks/p0001-p0100/p0031-c01.md), [p0032](../../../rag/chunks/p0001-p0100/p0032-c01.md)).

## Read-only checks

| Проверка | Что она подтверждает | Источник |
|---|---|---|
| `systemctl status zabbix-server` | Состояние процесса Zabbix server, но не frontend/БД целиком | [p0024](../../../rag/chunks/p0001-p0100/p0024-c01.md) |
| `tail -f /var/log/zabbix/zabbix_server.log` | Сообщения запуска и проблемы серверного процесса | [p0024](../../../rag/chunks/p0001-p0100/p0024-c01.md) |
| Открыть адрес frontend в браузере | Доступность веб-страницы через NGINX | [p0027](../../../rag/chunks/p0001-p0100/p0027-c01.md) |
| Wizard: предварительные требования = OK | Соответствие проверок frontend | [p0027](../../../rag/chunks/p0001-p0100/p0027-c01.md) |
| `Reports → System information` | Состояние сервера и HA cluster/failover delay | [p0041](../../../rag/chunks/p0001-p0100/p0041-c01.md) |
| System information: versions, NVPS, items | Обзор процесса, версий и масштаба получаемых данных | [p0046](../../../rag/chunks/p0001-p0100/p0046-c01.md) |
| Problems / Host availability | Текущие проблемы, критичность и доступность узлов | [p0047](../../../rag/chunks/p0001-p0100/p0047-c01.md), [p0049](../../../rag/chunks/p0001-p0100/p0049-c01.md) |

## Interpretation

- Zabbix server пишет историю и конфигурацию через БД; frontend также использует эту БД для настроек ([p0024](../../../rag/chunks/p0001-p0100/p0024-c01.md), [p0030](../../../rag/chunks/p0001-p0100/p0030-c01.md)).
- В режиме HA одно активное серверное звено принимает работу при сбое другого, но **общая нерезервированная БД — предел готовности** ([p0031](../../../rag/chunks/p0001-p0100/p0031-c01.md), [p0032](../../../rag/chunks/p0001-p0100/p0032-c01.md)).
- `HANodeName` обозначает узел серверного HA, `NodeAddress` позволяет frontend обращаться к текущему активному узлу ([p0035](../../../rag/chunks/p0001-p0100/p0035-c01.md), [p0043](../../../rag/chunks/p0001-p0100/p0043-c01.md)).
- При наличии nginx на ha1 вес `chk_nginx` даёт `244+10=254`; на ha2 `243+10=253`. Без nginx на ha1 приоритет становится 244, и резервный ha2 (253) получает VIP ([p0043](../../../rag/chunks/p0001-p0100/p0043-c01.md)).
- Виджет `System information` показывает оценки NVPS; `Graph` даёт более детальный обзор значений за секунду ([p0046](../../../rag/chunks/p0001-p0100/p0046-c01.md), [p0050](../../../rag/chunks/p0001-p0100/p0050-c01.md)).

## Next action

После диагностики выберите **конкретный слой** (server, DB, NGINX/frontend, HA/VIP, UI) и только затем соответствующий рецепт. Не запускать все установки повторно для устранения одного симптома.

## Modifying action

По главе: установка репозиториев и пакетов, создание БД/учётной записи, правка `/etc/zabbix/zabbix_server.conf`, настройка NGINX и keepalived, запуск/restart служб, настройка виджетов ([p0021](../../../rag/chunks/p0001-p0100/p0021-c01.md)–[p0026](../../../rag/chunks/p0001-p0100/p0026-c01.md), [p0033](../../../rag/chunks/p0001-p0100/p0033-c01.md)–[p0038](../../../rag/chunks/p0001-p0100/p0038-c01.md)). **Эффект:** изменение пакетов, служб, БД, интерфейса либо маршрутизации VIP. **Риски:** недоступность мониторинга/интерфейса, ошибки прав доступа, секреты в конфигурации и невыполненный failover. Точный план изменений на существующей production-системе: `[Needs confirmation]`.

## Verification / acceptance checks

1. Zabbix server активен, журнал запуска проверен; база доступна серверу.
2. Frontend открывается; wizard подтверждает prerequisites/DB; вход успешен.
3. Для HA — оба узла отображаются в `Reports → System information`, frontend переходит на нужный адрес при переключении; журнал не сообщает ошибок.
4. В интерфейсе доступны `Monitoring → Problems/Hosts/Latest data`, `Reports → System information`, `Data collection → Hosts/Templates`, `Users` и `Administration` (как описано в главе) ([p0054](../../../rag/chunks/p0001-p0100/p0054-c01.md)–[p0058](../../../rag/chunks/p0001-p0100/p0058-c01.md)).

## Rollback

- Глава **явно** возвращает `log_bin_trust_function_creators` к `0` после импорта ([p0023](../../../rag/chunks/p0001-p0100/p0023-c01.md)).
- Для демонстрации переключения frontend книга останавливает nginx и затем снова запускает ([p0040](../../../rag/chunks/p0001-p0100/p0040-c01.md), [p0041](../../../rag/chunks/p0001-p0100/p0041-c01.md)).
- Восстановление исходных пакетов, БД, конфигураций NGINX/keepalived, схемы и учетных записей **не описано как полная процедура rollback**: `[Needs confirmation]`.

## Карта интерфейса

`Monitoring` — Problems/Hosts/Latest data/Maps/Discovery; `Services` — Services/SLA/SLA report; `Inventory` — Overview/Hosts; `Reports` — System information/Availability/Audit/Action; `Data collection` — Templates/Hosts/Maintenance/Discovery; `Alerts` — Actions/Media types/Scripts; `Users` — groups/roles/accounts/tokens/auth; `Administration` — General/Housekeeping/Proxies/Queue ([p0054](../../../rag/chunks/p0001-p0100/p0054-c01.md)–[p0058](../../../rag/chunks/p0001-p0100/p0058-c01.md)).

**Ограничение источника:** потенциальные несовпадения команд — [source-findings.md](source-findings.md); отсутствующие сведения помечены `[Needs confirmation]`.
