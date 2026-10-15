# Глава 9 — cheatsheet: внешние уведомления и интеграции

**Основание:** accepted RAG PDF 371–411; [provenance](README.md). Конфигурации UI из иллюстраций = `RAG_MISS`. Практический scope: Slack, MS Teams, Telegram, Opsgenie.

## Symptom / problem framing

| Симптом | Диагностический вопрос | Источник |
|---|---|---|
| Нет уведомлений Slack | App установлена в Workspace? `chat:write`/`im:write`/`groups:write`? Бот добавлен в канал? `bot_token` заполнен, media enabled? | [p0375](../../../rag/chunks/p0301-p0400/p0375-c01.md)–[p0379](../../../rag/chunks/p0301-p0400/p0379-c01.md) |
| MS Teams ничего не получает | Канал и коннектор `Zabbix Webhook` созданы? Работает `teams_endpoint`? Media enabled, user/action настроены? | [p0385](../../../rag/chunks/p0301-p0400/p0385-c01.md)–[p0392](../../../rag/chunks/p0301-p0400/p0392-c01.md) |
| Telegram бот не отправляет в группу | BotFather token / присутствие бота, Group ID (обычно отрицательный), поле `Send to`, media и action? | [p0394](../../../rag/chunks/p0301-p0400/p0394-c01.md)–[p0402](../../../rag/chunks/p0401-p0500/p0402-c01.md) |
| Opsgenie не создаёт alert или не обрабатывает Recovery | API Key, package/OEC script, `config.json` (`apiKey/command_url/user/password/baseUrl`), PROBLEM/Recovery/Update operations | [p0405](../../../rag/chunks/p0401-p0500/p0405-c01.md)–[p0410](../../../rag/chunks/p0401-p0500/p0410-c01.md) |
| Все проблемы уходят во внешний канал | Action `Notify external services` создан **без conditions**; это учебный broad-match, не production default | [p0382](../../../rag/chunks/p0301-p0400/p0382-c01.md), [p0391](../../../rag/chunks/p0301-p0400/p0391-c01.md), [p0401](../../../rag/chunks/p0401-p0500/p0401-c01.md) |
| Внешний технический пользователь видит больше хостов, чем ожидается | Роль `Super admin` перекрывает Host permissions `Read`; проверить `Users → Users → Permissions` | [p0382](../../../rag/chunks/p0301-p0400/p0382-c01.md), [p0390](../../../rag/chunks/p0301-p0400/p0390-c01.md), [p0400](../../../rag/chunks/p0301-p0400/p0400-c01.md), [p0407](../../../rag/chunks/p0401-p0500/p0407-c01.md) |

## Baseline / context

Zabbix 7 с действующими PROBLEM events, преднастроенными Slack/MS Teams/Telegram media types, созданными внешними workspace/командой/группой и заранее авторизованными получателями. Для Opsgenie дополнительно команда, integration API key, Zabbix server shell, установленный OEC connector и его `actionCommand.txt`. Книга не объясняет начальную регистрацию внешних аккаунтов или их современную совместимость ([p0371](../../../rag/chunks/p0301-p0400/p0371-c01.md)–[p0372](../../../rag/chunks/p0301-p0400/p0372-c01.md), [p0403](../../../rag/chunks/p0401-p0500/p0403-c01.md)).

## Read-only checks

- `Alerts → Media types`: наличие `Slack`, `MS Teams`, `Telegram`, `Enabled`, Message templates — **Read-only при просмотре**; **не выводить token/endpoint из fields в журналы** ([p0379](../../../rag/chunks/p0301-p0400/p0379-c01.md), [p0388](../../../rag/chunks/p0301-p0400/p0388-c01.md), [p0397](../../../rag/chunks/p0301-p0400/p0397-c01.md)).
- `Users → User groups` и `Host permissions`: группы, `Read` только на нужных host groups; `Users → Users → Media / Permissions`: фактические media и role. Проверка прав **Read-only**, сохранение изменений **State-changing** ([p0380](../../../rag/chunks/p0301-p0400/p0380-c01.md)–[p0382](../../../rag/chunks/p0301-p0400/p0382-c01.md)).
- `Alerts → Actions → Trigger actions`: conditions, Operations, Recovery/Update operations для Opsgenie — **Read-only при просмотре**. Без conditions action затронет все проблемы ([p0382](../../../rag/chunks/p0301-p0400/p0382-c01.md), [p0408](../../../rag/chunks/p0401-p0500/p0408-c01.md)).
- Читать факт поступления сообщения в Slack channel, Teams channel, Telegram group, Opsgenie alerts — **Read-only** в соответствующем интерфейсе, но содержание alert может быть чувствительным.
- Для Opsgenie проверить, что файлы `/home/opsgenie/oec/opsgenie-zabbix/actionCommand.txt` и `/home/opsgenie/oec/conf/config.json` существуют **без чтения/разглашения секретов**; исходник не даёт read-only команды такой проверки.

## Interpretation

**Webhook pipeline:** событие PROBLEM соответствует severity, условиям action и операциям; Zabbix отправляет уведомление через Media type внешнему endpoint. Slack OAuth bot и Telegram BotFather дают отдельные tokens, Teams connector создаёт канал-специфичный endpoint ([p0384](../../../rag/chunks/p0301-p0400/p0384-c01.md), [p0392](../../../rag/chunks/p0301-p0400/p0392-c01.md), [p0402](../../../rag/chunks/p0401-p0500/p0402-c01.md)).

**Access ≠ recipient:** User group `Host permissions: Read`, user `Media`, `No access to the frontend`, `Role` решают разные задачи. Роль `Super admin` **не должна** использоваться для компенсации отсутствующих разрешений у технического адресата ([p0381](../../../rag/chunks/p0301-p0400/p0381-c01.md)–[p0382](../../../rag/chunks/p0301-p0400/p0382-c01.md)).

**Telegram:** создаётся `New Group`, а не гарантированный broadcast channel; `/getgroupid@myidbot` получает ID для `Send to` (источник предупреждает о начальном «-»). Bot username из книги учебный и **не может быть переиспользован** всеми читателями ([p0394](../../../rag/chunks/p0301-p0400/p0394-c01.md)–[p0400](../../../rag/chunks/p0301-p0400/p0400-c01.md)).

**Opsgenie:** в отличие от первых трёх media webhook настройка включает серверный script `Opsgenie connector` и отдельные операции PROBLEM/Recovery/Update, ориентированные на двусторонний процесс подтверждения alert ([p0407](../../../rag/chunks/p0401-p0500/p0407-c01.md)–[p0410](../../../rag/chunks/p0401-p0500/p0410-c01.md)). Точный shell-script body не включён в текстовый RAG.

## Next action

Локализовать **первую неисправную границу**: external bot/connector → Zabbix `Media types` and credentials → user/media/role/host-group access → trigger action conditions/operations → фактическое сообщение. Для Opsgenie вставить также **пакет OEC/script + конфигурацию/регион**. Секреты не раскрывать в diagnostic output.

## Modifying action

- Slack `Create App`, scopes, `Install to Workspace`, `Add app to channel`: **State-changing**, затрагивает границы доступа к сообщениям в организации; scoped permissions из источника требуют согласования.
- Teams `Connectors → Zabbix Webhook → Configure`, Telegram `/newbot`/Add bot/IDBot в группу: **State-changing**; API token и endpoint являются секретами.
- `Alerts → Media types → bot_token / teams_endpoint / Token → Update`: **State-changing**; потеря/ошибка секрета прерывает доставку.
- `Users → User groups` / `Users → Users → Media/Permissions`: **State-changing / security-sensitive**. Использовать ограниченный доступ только к нужным host groups, ограниченную роль и `No access to the frontend` когда это необходимо.
- `Alerts → Actions → Create action`: **State-changing / notification-generating**. Без conditions соответствует всем PROBLEM; перед enable указать severity, host group и recipients. `Warning+` — пример книги, а не универсальное правило.
- Opsgenie `rpm -i` / `dpkg -i`, `Alerts → Scripts`, `config.json`: **State-changing и execution-sensitive**; сторонний пакет и script исполняются от контекста Zabbix server, требуют отдельной проверки provenance/совместимости. Нельзя выполнять скачанный 1.1.6 пакет на production только потому, что он есть в книге.

## Verification / acceptance checks

1. Тестовая PROBLEM разрешённого host group и severity попала только в назначенный Slack/Teams/Telegram канал; **ни одного нецелевого события**.
2. User media активен, роль/host permissions проверены; **технический пользователь не Super admin**, frontend-доступ ограничен.
3. Нет публичной записи bot token, Teams webhook URL, Opsgenie API key/пароля; оценены сроки и ротация секретов.
4. Для Telegram действителен group ID в `Send to`; для Teams endpoint относится к правильному каналу.
5. Для Opsgenie проверены создание, Recovery/Update и корректный регион (если не США), без регистрации одних и тех же проблем несколько раз.
6. Исторические скриншотные параметры и старые внешние компоненты проверяются в целевой среде: `[Needs confirmation]`.

## Rollback

В главе **нет полного плана** revoke/reinstall/rotate tokens, отмены Telegram/Teams bots, сохранения истории при перестройке действий, удаления сервера Opsgenie OEC и восстановления доставок. `[Needs confirmation]`. Перед изменениями сохранить текущие фильтры/permissions/recipients по утверждённой локальной процедуре. Ошибочные массовые уведомления отменить задним числом нельзя.

Расхождения и `RAG_MISS`: [source-findings.md](source-findings.md). **Статус чтения не меняется.**
