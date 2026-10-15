# Глава 9. Интеграция Zabbix с внешними сервисами

**Книга:** «Zabbix 7: мониторинг ИТ-инфраструктуры» (русское обновлённое 3-е издание, 2025). Inventory `0020`; `book_id: zabbix-7-monitoring-it-infrastructure-ru`.

## Источник и границы

- Политика **RAG-only**: использован только книжный accepted RAG из Git, `rag/acceptance.yaml: ACCEPTED`. Не выполнялись прямое чтение PDF, переход по внешним ссылкам и проверка актуальных облачных API. Поля только со скриншотов не реконструированы.
- **PDF 371–411 включительно**; адресуемые chunks `zabbix-7-monitoring-it-infrastructure-ru:p0371:c01` … `zabbix-7-monitoring-it-infrastructure-ru:p0411:c01`. [Начало главы 9](../../../rag/chunks/p0301-p0400/p0371-c01.md); глава 10 начинается [p0412](../../../rag/chunks/p0401-p0500/p0412-c01.md).
- Source SHA256: `07204d885d4bf4c6c2de7c71ae42a4e3ed4cea794169cbe07985552e63875a27`; corpus generation `6a5221f8e8a0f88b400905d7334879edff6f5451d9ab7f6e56bb203809018986`.
- Данные форм из рисунков 9.1–9.78 не выделены в RAG как структурированные поля: для точных значений `RAG_MISS`.

## Карта главы

| Раздел | PDF-страницы | Содержание |
|---|---:|---|
| [Настройка оповещений в Slack](../../../rag/chunks/p0301-p0400/p0372-c01.md) | 372–384 | Slack workspace/channel, app, bot OAuth scopes, `bot_token`, media user, Trigger action |
| [Настройка оповещений в Microsoft Teams](../../../rag/chunks/p0301-p0400/p0385-c01.md) | 385–393 | Channel, `Zabbix Webhook` connector, `teams_endpoint`, media user, action |
| [Настройка оповещений в Telegram](../../../rag/chunks/p0301-p0400/p0393-c01.md) | 393–402 | `@BotFather`, `/newbot`, bot Token, IDBot/group ID, `Send to` и action |
| [Интеграция Atlassian Opsgenie и Zabbix](../../../rag/chunks/p0401-p0500/p0403-c01.md) | 403–411 | Opsgenie team/integration, API Key, connector package, Zabbix `Script` и PROBLEM/Recovery/Update |

## Архитектура уведомления Zabbix

В Zabbix 7 книга использует **преднастроенные webhook media types**, но для их работы всё равно нужно связать каждый из следующих слоёв:

1. **Внешняя конечная точка:** Slack bot в согласованном канале; Teams channel connector; Telegram bot в группе; Opsgenie integration.
2. **Media type в Zabbix:** `Alerts → Media types`, параметры сервиса (`bot_token`, `teams_endpoint`, `Token`), `Enabled`, шаблоны сообщений.
3. **Получатель и права:** `Users → User groups` + `Host permissions`, `Users → Users` → `Media` и `Permissions`. Пользователь-«интеграция» не обязан получать frontend-доступ; источник предлагает `No access to the frontend`.
4. **Триггерное действие:** `Alerts → Actions → Trigger Actions`, условия сопоставления и `Operations`; для Opsgenie также `Recovery operations` и `Update operations`.

От начала события до уведомления: **новая PROBLEM → соответствие conditions/severity → Action operation → media/webhook или server script → внешний сервис**. Сведения об успешно доставленном сообщении нельзя выводить только из наличия user/media/action: проверяется сам канал/чат и журнал доставки в доступном окружении ([p0382](../../../rag/chunks/p0301-p0400/p0382-c01.md)–[p0384](../../../rag/chunks/p0301-p0400/p0384-c01.md), [p0392](../../../rag/chunks/p0301-p0400/p0392-c01.md), [p0402](../../../rag/chunks/p0401-p0500/p0402-c01.md)).

## 1. Slack

В Slack создаются канал `#zabbix-notifications` и приложение `Zabbix-Alert-Bot` через Slack API Apps. Книга указывает три bot OAuth scopes: `chat:write`, `im:write`, `groups:write`; далее `Install to Workspace`, `Allow`, сохранение OAuth token и добавление приложения в целевой канал. В Zabbix активируется media type `Slack` и заполняется параметр `bot_token` ([p0373](../../../rag/chunks/p0301-p0400/p0373-c01.md)–[p0379](../../../rag/chunks/p0301-p0400/p0379-c01.md)).

Далее создать группу `External Services` (в тексте) с доступом к нужным `Host groups` по `Read`, отдельного пользователя Slack, media и trigger action `Notify external services`. Для изоляции книги используется `No access to the frontend`, однако её пример с ролью **Super admin** нарушает ожидаемую границу только для чтения: авторы прямо предупреждают об этом и допускают ограниченную роль `User` или `Admin` ([p0380](../../../rag/chunks/p0301-p0400/p0380-c01.md)–[p0384](../../../rag/chunks/p0301-p0400/p0384-c01.md)). В примере уведомления о проблеме соответствуют **Warning и выше**.

## 2. Microsoft Teams

В Teams авторы создают канал, открывают `Connectors`, выбирают `Zabbix Webhook`, копируют URL вебхука и сохраняют соединение. В Zabbix в `Alerts → Media types → MS Teams` параметр **`teams_endpoint`** получает этот URL, включается `Enabled`, затем создаются группа/пользователь с media и trigger action ([p0385](../../../rag/chunks/p0301-p0400/p0385-c01.md)–[p0392](../../../rag/chunks/p0301-p0400/p0392-c01.md)).

Этот процесс отражает **интерфейс конкретного издания**: нынешняя доступность Teams Connectors, точный API или возможность повторения без изменений **не проверены** в режиме RAG-only. Реальный endpoint — секретный адрес; не публиковать его в репозитории. Источник подтверждает фильтрацию отправленных событий **Warning и выше** ([p0392](../../../rag/chunks/p0301-p0400/p0392-c01.md)).

## 3. Telegram

Создаётся группа, бот через `@BotFather`, команды `/start` и `/newbot`; после выбора уникального username хранится token HTTP API. Бот добавляется в группу, в Zabbix для media type `Telegram` используется поле **`Token`**. Для получения идентификатора группы книга предлагает временно добавить `IDBot` и отправить `/getgroupid@myidbot` ([p0394](../../../rag/chunks/p0301-p0400/p0394-c01.md)–[p0399](../../../rag/chunks/p0301-p0400/p0399-c01.md)).

Полученный отрицательный числовой group ID записывается в пользовательский media `Send to`; снова настраивается `Notify external services` и операции, при которых в чат приходят проблемы Warning+ ([p0400](../../../rag/chunks/p0301-p0400/p0400-c01.md)–[p0402](../../../rag/chunks/p0401-p0500/p0402-c01.md)). Текст использует «канал» и «группу» непоследовательно; для практики он пошагово создаёт **New Group** и использует **group ID**, не следует заменять их Telegram channel ID по догадке.

## 4. Atlassian Opsgenie

Opsgenie добавляет к доставке alerts возможность звонков/SMS, дежурств и ответов. В аккаунте настраиваются контакты, команда `Consultancy`, `Integrations → Zabbix`, копируется **API Key** ([p0403](../../../rag/chunks/p0401-p0500/p0403-c01.md)–[p0405](../../../rag/chunks/p0401-p0500/p0405-c01.md)).

Вместо media webhook из первых трёх сценариев этот раздел устанавливает отдельный RPM/DEB `opsgenie-zabbix 1.1.6` (конкретные старые файлы из книги) и создаёт `Alerts → Scripts → Opsgenie connector` с `Scope: Action operation`, `Type: Script`, `Execute on: Zabbix server`. Содержимое script берётся из **`/home/opsgenie/oec/opsgenie-zabbix/actionCommand.txt`**, а не из текста книги — поэтому точные команды скрипта = **`RAG_MISS`** ([p0405](../../../rag/chunks/p0401-p0500/p0405-c01.md)–[p0408](../../../rag/chunks/p0401-p0500/p0408-c01.md)).

В `Alerts → Actions` действие `Opsgenie action` включает обычные, recovery и update operations с script; конфигурация `/home/opsgenie/oec/conf/config.json` содержит `apiKey`, `command_url`, `user`, `password`, а источник указывает возможность настройки региона `baseUrl=https://api.eu.opsgenie.com` вне США ([p0408](../../../rag/chunks/p0401-p0500/p0408-c01.md)–[p0410](../../../rag/chunks/p0401-p0500/p0410-c01.md)). Содержимое этих секретов в Git/чат не переносится. Нынешнее существование и актуальная совместимость пакета/сервиса **не проверялись**.

## Контроль корректности и ограничений

- До активации action зафиксировать целевые severity/host groups, пользователей и каналы. **Действие без условий** у всех трёх chat-рецептов сопоставляет **любую** проблему: автор прямо предостерегает от такого production-режима ([p0382](../../../rag/chunks/p0301-p0400/p0382-c01.md), [p0391](../../../rag/chunks/p0301-p0400/p0391-c01.md), [p0401](../../../rag/chunks/p0401-p0500/p0401-c01.md)).
- Не давать **Super admin** пользователю интеграции: примеры p382/p390/p400/p407 показывают это ради удобства и **сами предупреждают**, что роль снимает ограничения `Read`.
- Токены OAuth, Telegram bot token, Teams webhook URL и Opsgenie API key относятся к **секретам**; источник не содержит безопасной production-процедуры ротации, audit/expiry и rollback — `[Needs confirmation]`.
- Скриншотные поля `Send to`, дополнительные macros, action operations, точные Opsgenie conditions/script command, формы Opsgenie integration и message templates = `RAG_MISS`.
- В тексте [p0411](../../../rag/chunks/p0401-p0500/p0411-c01.md) нет отдельного chapter-end summary/review questions, [p0412](../../../rag/chunks/p0401-p0500/p0412-c01.md) начинает следующую главу; условные файлы не создаются.

## Артефакты

[Операционная памятка](cheatsheet.md) · [Команды и UI](commands.md) · [Mermaid](diagram.md) · [Компактная SVG](visual-cheatsheet.svg) · [Подробная SVG](visual-cheatsheet-detailed.svg) · [Source findings](source-findings.md).

**Статус чтения не меняется.** Контракты: router v1.2, recovery v1.0, chapter request v1.4, artifacts v1.8, publication v1.0.
