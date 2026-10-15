# Глава 9 — source-grounded команды и UI-операции

Только accepted **RAG PDF 371–411**. Типы воздействия: **Read-only**, **Workload-generating** (запросы/отправка уведомлений), **State-changing**, **Security-sensitive** (секреты, права, сторонние скрипты). Учебные интерфейсы внешних облачных продуктов **не проверены** на актуальность.

## 1. Общая схема Zabbix, необходимая для Slack / Teams / Telegram

| Операция из книги | Класс | Эффект, риск, проверка |
|---|---|---|
| `Alerts → Media types → [Slack / MS Teams / Telegram]` (просмотр) | Read-only | Проверить наличие встроенного media type и Enabled. Открытый экран может показывать секретные fields: не разглашать. [p0379](../../../rag/chunks/p0301-p0400/p0379-c01.md), [p0388](../../../rag/chunks/p0301-p0400/p0388-c01.md), [p0397](../../../rag/chunks/p0301-p0400/p0397-c01.md) |
| `Users → User groups → Create user group`, `Host permissions → Read` | State-changing / Security-sensitive | Предоставляет видимость выбранных host groups; книга предлагает External Services. Не разрешать все группы без оснований. [p0380](../../../rag/chunks/p0301-p0400/p0380-c01.md) |
| `Users → Users → Create user → Media → Add` | State-changing | Связывает alert recipient и endpoint. Убедиться в правильном `Send to`, severity и контактах. [p0381](../../../rag/chunks/p0301-p0400/p0381-c01.md), [p0399](../../../rag/chunks/p0301-p0400/p0399-c01.md)–[p0400](../../../rag/chunks/p0301-p0400/p0400-c01.md) |
| `Users → Users → Permissions`, `No access to the frontend` | State-changing / Security-sensitive | Техническая запись без UI-доступа. Книга назначает `Super admin` «для удобства», одновременно предупреждая, что это **перекрывает права Read**; не переносить в production. [p0382](../../../rag/chunks/p0301-p0400/p0382-c01.md), [p0390](../../../rag/chunks/p0301-p0400/p0390-c01.md), [p0407](../../../rag/chunks/p0401-p0500/p0407-c01.md) |
| `Administration → Macros` с URL Zabbix | State-changing | В книге macro name/value на рис. 9.21/9.37: `RAG_MISS`, не додумывать. [p0382](../../../rag/chunks/p0301-p0400/p0382-c01.md), [p0391](../../../rag/chunks/p0301-p0400/p0391-c01.md) |
| `Alerts → Actions → Trigger Actions → Create action` | State-changing / Workload-generating после события | `Notify external services` и Operations. **Action без условий** затронет каждую PROBLEM, что источник не рекомендует для production. Уточнить conditions/severity/recipients до активации. [p0382](../../../rag/chunks/p0301-p0400/p0382-c01.md), [p0391](../../../rag/chunks/p0301-p0400/p0391-c01.md), [p0401](../../../rag/chunks/p0401-p0500/p0401-c01.md) |

## 2. Slack

1. Slack: `Add channels → Create a new channel` (в книге `#zabbix-notifications`) и выбрать видимость **Public/Private**. **State-changing**, определяет круг читателей технических alerts — [p0373](../../../rag/chunks/p0301-p0400/p0373-c01.md)–[p0374](../../../rag/chunks/p0301-p0400/p0374-c01.md).
2. `https://api.slack.com/apps → Create New App → From scratch`, далее `OAuth & Permissions → Scopes → Add an OAuth Scope`: значения из текста **`chat:write`, `im:write`, `groups:write`**. **State-changing / Security-sensitive**: разрешения на запись сообщений ([p0374](../../../rag/chunks/p0301-p0400/p0374-c01.md)–[p0375](../../../rag/chunks/p0301-p0400/p0375-c01.md)).
3. `Install to Workspace → Allow` и сохранить bot OAuth token **в секретном хранилище**, не в Git. Добавить app `Zabbix-Alert-Bot` в канал через `Integrations → Add an App`. **State-changing** ([p0375](../../../rag/chunks/p0301-p0400/p0375-c01.md)–[p0378](../../../rag/chunks/p0301-p0400/p0378-c01.md)).
4. `Alerts → Media types → Slack → bot_token → Enabled → Update`. **State-changing / Security-sensitive**; `Message templates` в source уже содержит пять типов, точный текст рисунка `RAG_MISS`. Затем user, media, action и Operations. **Проверка:** поступление новой разрешённой PROBLEM в заданный канал, пример `Warning+` ([p0379](../../../rag/chunks/p0301-p0400/p0379-c01.md)–[p0384](../../../rag/chunks/p0301-p0400/p0384-c01.md)).

## 3. Microsoft Teams

1. Teams channel → `... → Connectors` → выбрать **`Zabbix Webhook`**, `Configure` и скопировать webhook URL, затем `Save`. **State-changing / Security-sensitive**: сам URL является ключом к отправке сообщений, не публиковать. Существование именно такого Connector в целевой современной среде = `[Needs confirmation]` ([p0385](../../../rag/chunks/p0301-p0400/p0385-c01.md)–[p0387](../../../rag/chunks/p0301-p0400/p0387-c01.md)).
2. `Alerts → Media types → MS Teams`; вставить URL в **`teams_endpoint`**, проверить `Enabled` и `Update`. **State-changing**, риск отправки не туда/дублирования, обратная процедура не описана ([p0388](../../../rag/chunks/p0301-p0400/p0388-c01.md)).
3. `Users → User groups/Users → Media` и при отсутствии общего action `Alerts → Actions → Notify external services`. **State-changing**; `Super admin` и action без conditions — учебные небезопасные shortcut ([p0389](../../../rag/chunks/p0301-p0400/p0389-c01.md)–[p0391](../../../rag/chunks/p0301-p0400/p0391-c01.md)). Проверка: разрешённая PROBLEM Warning+ пришла **в конкретный канал** ([p0392](../../../rag/chunks/p0301-p0400/p0392-c01.md)).

## 4. Telegram BotFather / групповой адресат

```text
# Сообщения, посылаемые самому @BotFather в Telegram (не shell commands).
/start
/newbot
# Команда книги в группе с IDBot; требует внешнего участника и может раскрыть ID:
/getgroupid@myidbot
```

Эти действия **State-changing** (`/newbot` создаёт бота, добавление IDBot расширяет список участников группы); `/start` информативна, `/getgroupid...` обращается к стороннему боту и может быть чувствительной по privacy. Источник использует именно `New Group` и группового получателя, а не произвольный broadcast-канал ([p0394](../../../rag/chunks/p0301-p0400/p0394-c01.md)–[p0399](../../../rag/chunks/p0301-p0400/p0399-c01.md)).

В Zabbix: `Alerts → Media types → Telegram → Token → Enabled → Update` (**State-changing / Security-sensitive**); затем пользователь Telegram, его `Media → Send to = <TELEGRAM_GROUP_ID>` (ID по примеру начинается с `-`), permissions и `Notify external services` action. Книга задаёт username бота `lar_zbx_notification_bot`, но **сама** указывает, что username обязан быть уникальным, поэтому буквальное копирование может не сработать ([p0396](../../../rag/chunks/p0301-p0400/p0396-c01.md)–[p0402](../../../rag/chunks/p0401-p0500/p0402-c01.md)).

## 5. Atlassian Opsgenie: пакет OEC, script и два направления данных

Внешняя система: `Settings → Notifications → Add email/phone`; `Teams → Add team` (`Consultancy`); `Integrations → Add integration → Zabbix`; копировать API key. **State-changing / Security-sensitive**, контакты и API key не хранить в репозитории ([p0403](../../../rag/chunks/p0401-p0500/p0403-c01.md)–[p0405](../../../rag/chunks/p0401-p0500/p0405-c01.md)).

**Синтаксис пакетов, сохранённый из источника p405 — только исторический пример, не подтверждённый production install script:**

```sh
# Workload-generating network download; authenticity/version/status not verified
wget https://github.com/opsgenie/oec-scripts/releases/download/Zabbix-1.1.6_oec-1.1.3/opsgenie-zabbix-1.1.6.x86_64.rpm
wget https://github.com/opsgenie/oec-scripts/releases/download/Zabbix-1.1.6_oec-1.1.3/opsgenie-zabbix_1.1.6_amd64.deb

# State-changing package install; execute only in isolated validated lab
rpm -i opsgenie-zabbix-1.1.6.x86_64.rpm
dpkg -i opsgenie-zabbix_1.1.6_amd64.deb
```

Выбирается **одна** ветка по ОС. Пакеты могут устанавливать исполнимые компоненты/сервис с правами на Zabbix server. Источник не содержит checksum, signature verification, актуальной совместимости и rollback: `[Needs confirmation]`. Внешние URL не открывались.

**Zabbix UI/script** ([p0407](../../../rag/chunks/p0401-p0500/p0407-c01.md)–[p0408](../../../rag/chunks/p0401-p0500/p0408-c01.md)): `Alerts → Scripts → Create script` с именем `Opsgenie connector`, `Scope=Action operation`, `Type=Script`, `Execute on=Zabbix server`. Команда берётся из файла **`/home/opsgenie/oec/opsgenie-zabbix/actionCommand.txt`** — его содержимого **нет** в RAG → `RAG_MISS`. Нельзя воссоздать исполнимый shell текст из памяти.

`Alerts → Actions → Trigger Actions → Opsgenie action` добавляет выбранный script отдельно в **`Operations`, `Recovery operations`, `Update operations`**. Точные условия из рисунка 9.72 = `RAG_MISS`, нужно проверить условия и не дублировать broad default ([p0408](../../../rag/chunks/p0401-p0500/p0408-c01.md)–[p0409](../../../rag/chunks/p0401-p0500/p0409-c01.md)).

```text
# File location; editing with vim is State-changing / contains secrets.
/home/opsgenie/oec/conf/config.json
# Source-provided field names:
apiKey
command_url
user
password
baseUrl
# Example regional baseUrl used in source (EU, only if needed):
https://api.eu.opsgenie.com
```

Источник приводит `vim /home/opsgenie/oec/conf/config.json`, но значения `apiKey`, `command_url`, `user`, `password` из рисунка 9.75 = **`RAG_MISS`**. **Ни один секрет не вставлять в Git, чат, shell history или диагностику.** Проверка: alert в Opsgenie, последующее подтверждение / recovery отражаются в обеих системах ([p0409](../../../rag/chunks/p0401-p0500/p0409-c01.md)–[p0410](../../../rag/chunks/p0401-p0500/p0410-c01.md)).

## Приёмка и rollback

Все UI-writes **State-changing**; внешний alert и установка пакета также создают нагрузку/побочные эффекты. Верификация — события только выбранных hosts/severity, корректные получатели, отсутствие лишнего frontend/admin-доступа, реальная доставка и recovery. Rollback для revoke/reissue tokens, Teams Connector/Telegram IDBot, удаления сторонних пакетов/скриптов, и доставки уже разосланных сообщений в главе **не описан**, `[Needs confirmation]`. См. [source-findings.md](source-findings.md).
