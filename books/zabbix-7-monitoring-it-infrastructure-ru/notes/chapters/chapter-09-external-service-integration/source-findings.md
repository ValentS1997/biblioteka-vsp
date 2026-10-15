# Глава 9 — source findings / границы доверия

**Режим:** только accepted RAG PDF 371–411, без внешней верификации Slack, Teams, Telegram, Opsgenie и third-party packages. Источниковые формулировки сохраняются, пробелы `RAG_MISS` и `[Needs confirmation]` не заполняются по памяти.

## 1. [Source security contradiction / Needs confirmation] Super admin перекрывает Host permissions Read

- **Вариант A (права группы):** [p0380](../../../rag/chunks/p0301-p0400/p0380-c01.md), [p0389](../../../rag/chunks/p0301-p0400/p0389-c01.md), [p0398](../../../rag/chunks/p0301-p0400/p0398-c01.md), [p0406](../../../rag/chunks/p0401-p0500/p0406-c01.md) рекомендуют группе `External Services` разрешение `Read` на выбранные host groups, а [p0381](../../../rag/chunks/p0301-p0400/p0381-c01.md), [p0389](../../../rag/chunks/p0301-p0400/p0389-c01.md), [p0399](../../../rag/chunks/p0301-p0400/p0399-c01.md), [p0406](../../../rag/chunks/p0401-p0500/p0406-c01.md) советуют `No access to the frontend`.
- **Вариант B (роль каждого пользователя):** [p0382](../../../rag/chunks/p0301-p0400/p0382-c01.md), [p0390](../../../rag/chunks/p0301-p0400/p0390-c01.md), [p0400](../../../rag/chunks/p0301-p0400/p0400-c01.md), [p0407](../../../rag/chunks/p0401-p0500/p0407-c01.md) назначают техническому пользователю `Super admin` «для удобства»; те же абзацы прямо объясняют, что роль **переопределяет** ограничения `Read`.
- **Итог:** это явно описанное **учебное ослабление**. Не распространять роль Super admin на production integration users, не делать вывод «frontend no access = безопасно независимо от роли». Адекватная роль `User/Admin` и минимальные host permissions подлежат отдельной проверке.

## 2. [Needs confirmation / broad notification risk] Trigger action без условий охватывает все PROBLEM

- **Источник:** [p0382](../../../rag/chunks/p0301-p0400/p0382-c01.md), [p0391](../../../rag/chunks/p0301-p0400/p0391-c01.md), [p0401](../../../rag/chunks/p0401-p0500/p0401-c01.md) создают `Notify external services` **без conditions** и сами сообщают, что оно сопоставляет все проблемы. Для production авторы советуют задавать условия.
- **Техническая тонкость:** в [p0384](../../../rag/chunks/p0301-p0400/p0384-c01.md), [p0392](../../../rag/chunks/p0301-p0400/p0392-c01.md), [p0402](../../../rag/chunks/p0401-p0500/p0402-c01.md) конечный результат описан как сообщения **Warning и выше**, но **не раскрыт текстовый набор всех параметров user media/severity и operation filters из рисунков**.
- **Итог:** `Warning+` нельзя автоматически приписать условию action: в тексте action без conditions. Для production требуется раздельная проверка всех media-severity/host-group/action filters; поля рисунков = `RAG_MISS`. Массовая случайная рассылка необратима.

## 3. [Source wording ambiguity] Telegram «канал» vs «группа»

- **Вариант A:** [p0394](../../../rag/chunks/p0301-p0400/p0394-c01.md) явно начинает с `New Group`, предлагает добавить пользователя/бота; [p0399](../../../rag/chunks/p0301-p0400/p0399-c01.md) использует `/getgroupid@myidbot` в **групповом чате**.
- **Вариант B:** [p0396](../../../rag/chunks/p0301-p0400/p0396-c01.md) и [p0397](../../../rag/chunks/p0301-p0400/p0397-c01.md) при описании того же объекта называют его «каналом» и пишут «добавьте бот в канал».
- **Итог:** путь книги настраивает **Telegram group** и использует **group ID**, который по [p0400](../../../rag/chunks/p0301-p0400/p0400-c01.md) начинается с `-`. Не заменять его произвольным channel ID. Конкретный фактический идентификатор и возможность получения его через сторонний IDBot требуют `[Needs confirmation]`.

## 4. [Needs confirmation / third-party code] Opsgenie actionCommand.txt не содержится в книжном RAG

- [p0407](../../../rag/chunks/p0401-p0500/p0407-c01.md) требует скопировать содержимое **`/home/opsgenie/oec/opsgenie-zabbix/actionCommand.txt`** в `Alerts → Scripts → Opsgenie connector` (`Scope=Action operation`, `Type=Script`, `Execute on=Zabbix server`).
- **В RAG нет** содержимого file или полного Commands text из рис. 9.71: `RAG_MISS`. Исходные RPM/DEB 1.1.6 из [p0405](../../../rag/chunks/p0401-p0500/p0405-c01.md) не загружались.
- **Итог:** нет оснований публиковать «рабочий» executable OEC action script или считать внешний пакет безопасным/совместимым. Checksum/signature/supply chain, permissions, endpoint и rollback = `[Needs confirmation]`.

## 5. [Needs confirmation / API freshness] Исторические Teams Connectors, Slack scopes и внешние URL

- [p0385](../../../rag/chunks/p0301-p0400/p0385-c01.md)–[p0388](../../../rag/chunks/p0301-p0400/p0388-c01.md) используют Teams `... → Connectors → Zabbix Webhook → Configure` и URL `teams_endpoint`. Это **конкретный UI книги**, а не доказательство нынешней доступности или поддержки API.
- [p0375](../../../rag/chunks/p0301-p0400/p0375-c01.md) перечисляет Slack scopes `chat:write`, `im:write`, `groups:write`, но не обсуждает минимальные версии приложения, управление истечением токенов и политику revocation.
- [p0405](../../../rag/chunks/p0401-p0500/p0405-c01.md) ссылается на исторические пакеты `opsgenie-zabbix 1.1.6` и установленный Zabbix server; [p0410](../../../rag/chunks/p0401-p0500/p0410-c01.md) содержит `baseUrl=https://api.eu.opsgenie.com` как региональный пример. **Нынешняя работоспособность Opsgenie, интеграций и API не проверялась** в рамках RAG-only.
- **Итог:** версии, актуальный UI/API, доступность сервисов, домены и security settings = `[Needs confirmation]`; внешние URL не открывались.

## 6. [Needs confirmation / secrets exposure] Четыре разных чувствительных параметра

- Slack `bot_token`, OAuth token ([p0377](../../../rag/chunks/p0301-p0400/p0377-c01.md)–[p0379](../../../rag/chunks/p0301-p0400/p0379-c01.md)).
- Teams `teams_endpoint` с URL вебхука ([p0387](../../../rag/chunks/p0301-p0400/p0387-c01.md)–[p0388](../../../rag/chunks/p0301-p0400/p0388-c01.md)).
- Telegram `Token` от BotFather, `Send to` group ID и сторонний `IDBot` ([p0396](../../../rag/chunks/p0301-p0400/p0396-c01.md)–[p0400](../../../rag/chunks/p0301-p0400/p0400-c01.md)).
- Opsgenie `API Key`, `config.json` с `apiKey`, `command_url`, `user`, `password`, `baseUrl` ([p0405](../../../rag/chunks/p0401-p0500/p0405-c01.md), [p0409](../../../rag/chunks/p0401-p0500/p0409-c01.md)–[p0410](../../../rag/chunks/p0401-p0500/p0410-c01.md)).
- **Итог:** ключи не коммитить в Git и не выводить в уведомлениях, скриншотах или диагностических командах. Ротация и безопасный rollback раскрытых токенов не документированы; `[Needs confirmation]`.

## 7. [Needs confirmation / screenshot-only] Поля UI и настройки получателей

- Значения, представленные на рисунках 9.14–9.22 (Slack), 9.30–9.38 (Teams), 9.51–9.59 (Telegram), 9.66–9.75 (Opsgenie), **не извлечены как структурированные данные**. Текст подтверждает отдельные имена `bot_token`, `teams_endpoint`, `Token`, `Send to`, Opsgenie `Scope`, `Type`, `Execute on` и список keys `config.json`.
- **Не восстановлены** точные значения URL Zabbix macro, action condition expressions, message templates, Opsgenie script text, configuration secret values и screenshots UI — `RAG_MISS`.
- Без этих полей материал — надёжная **карта рецептов источника**, не готовый для исполнения автоматизированный deploy runbook.

## 8. [Needs confirmation] Opsgenie двусторонние операции и безопасная отправка

- [p0408](../../../rag/chunks/p0401-p0500/p0408-c01.md) создаёт action `Opsgenie action` с операцией `Opsgenie connector` и аналогичными Recovery/Update operations. [p0410](../../../rag/chunks/p0401-p0500/p0410-c01.md) описывает двустороннюю связь и возможность acknowledgement.
- **Нет** подтверждённого подробного HTTP/API-protocol, retry/idempotency, mapping событий/времени, истории повторных сообщений и безопасной повторной доставки. Для этих аспектов `[Needs confirmation]`.

## 9. [Needs confirmation] Нет исходникового chapter-end summary / review и полного rollback

- [p0411](../../../rag/chunks/p0401-p0500/p0411-c01.md) заканчивается информацией об Opsgenie on-call/PagerDuty, [p0412](../../../rag/chunks/p0401-p0500/p0412-c01.md) начинает новую главу. Отдельных обязательных разделов `summary`, `review questions`, `review answers` в конце главы нет.
- Книга не даёт проверенного rollback удаления внешних apps/ботов, отзыва токенов, изменения user roles, отмены отправленных сообщений, rollback OEC package/scripts. **Не создавать** условные summary/review файлы и не сочинять процедуру восстановления.

**Статус чтения не менялся.**
