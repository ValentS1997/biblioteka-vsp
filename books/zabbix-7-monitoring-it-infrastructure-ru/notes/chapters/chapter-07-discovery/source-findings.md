# Глава 7 — source findings (RAG-only)

Все находки основаны на исходном **PDF 291–335**, сохранённом через addressable RAG. Ни один внешний адрес и никакой исходный PDF напрямую не использовались для исправления или подтверждения команд. **Варианты источника сохраняются рядом**, статус воспроизводимости фиксируется явно.

## 1. [Source code mismatch] cron с zabbix_sender содержит повреждённые кавычки/JSON

- **Вариант A, команда:** на [p0329](../../../rag/chunks/p0301-p0400/p0329-c01.md) учебная строка начинается как `* * * * * zabbix_sender -z 127.0.0.1 -s lar-lldhost-creation -k 200",` (после `-k` остаётся не относящийся к key фрагмент), далее JSON разорван переносами и обрывком `"vmip":"10.16.16.`; продолжение списка содержит искажённые кавычки и данные.
- **Вариант B, объяснение на той же p329:** ниже авторы разбирают общую форму `* * * * *`, `zabbix_sender -z 127.0.0.1 -s lar-lldhost-creation -k lldhosts.raw -o СОДЕРЖИМОЕ ФАЙЛА С GITHUB` и `>/dev/null 2>&1`.
- **Дополнительная проверка внутри книги:** [p0331](../../../rag/chunks/p0301-p0400/p0331-c01.md) и [p0333](../../../rag/chunks/p0301-p0400/p0333-c01.md) дают связный JSON с `vmname`/`vmip`/`vmlocation`, но **не приводят ни безопасную для shell quoting, ни проверенную cron-конфигурацию с итоговым валидным payload**.
- **Решение:** источниковая cron строка **не исполнима как приведена**, не восстанавливать молча и не запускать. Для демонстрации можно показывать только схему аргументов, а валидный JSON, экранирование, ограничения sender, logging, проверка IP и расписание = `[Needs confirmation]`. Перенаправление stderr в `/dev/null` скрывает ошибки.

## 2. [Source code mismatch] Два регистра имени внешнего файла JSON

- **Вариант A:** [p0328](../../../rag/chunks/p0301-p0400/p0328-c01.md) ссылка на GitHub содержит `chapter07/lldhosts.json` (нижний регистр `h`).
- **Вариант B:** следующая строка на p328 содержит URL к сырому `chapter07/lldHosts.json` (заглавное `H`).
- **Решение:** обе исходные формы сохранены; внешняя ссылка **не открывалась**. На регистрозависимом сервере разные пути не эквивалентны. Реальный файл, формат, его существование и содержимое = `[Needs confirmation]`. JSON в тексте книги воспроизведён только в корректных отрывках, не как загруженный внешний artefact.

## 3. [Source wording/code mismatch] HostMetadata и название события в авторегистрации

- **Вариант A:** [p0304](../../../rag/chunks/p0301-p0400/p0304-c01.md) явно направляет в `Alerts → Actions → Autoregistration actions`; [p0307](../../../rag/chunks/p0301-p0400/p0307-c01.md) описывает, что active agent по `ServerActive` обращается на Zabbix server/proxy.
- **Вариант B:** [p0308](../../../rag/chunks/p0301-p0400/p0308-c01.md) в пояснении к `HostMetadata` говорит: «можно использовать HostMetadata в Discovery action», хотя раздел посвящён именно авторегистрации и UI-вкладка в рецепте называется `Autoregistration actions`.
- **Решение:** не считать одинаковыми два вида actions; настроенный `Discovery action` сам по себе не реализует described active-agent autoregistration. Исходное словоупотребление сохраняется как потенциальное смешение, UI-/API-проверка для реальной версии = `[Needs confirmation]`.

## 4. [Needs confirmation] SNMPv2 в отдельном рецепте и SNMPv3 из предпосылок

- [p0298](../../../rag/chunks/p0201-p0300/p0298-c01.md) отсылает к SNMP-мониторингу главы 3; [p0299](../../../rag/chunks/p0201-p0300/p0299-c01.md) предлагает `SNMPv2 agent` + community/OID, тогда как многие предыдущие учебные SNMP-примеры используют SNMPv3. Автор отмечает необходимость подбирать check type под фактическую SNMP version.
- **Решение:** это **не обязательно доказанное противоречие**: могли применяться разные целевые устройства. SNMPv2-команду с community нельзя выдавать за безопасный default. Версия, credentials, поддерживаемые OID и политика сети = `[Needs confirmation]`.

## 5. [Needs confirmation] Условное выявление Linux через boot-image OID

- [p0302](../../../rag/chunks/p0301-p0400/p0302-c01.md) проверяет `.1.3.6.1.2.1.25.1.4.0` и при получении `BOOT_IMAGE=(hd0,gpt2)...` рассматривает host как устройство с Linux boot.
- В источнике описан **один образец значения**; отсутствует доказательство, что все Linux hosts предоставляют его и другие ОС не могут возвращать сходные строки. Проверить на собственной SNMP среде и не строить production-classification только на одном признаке.
- Это `[Needs confirmation]`, а не исправление выражения.

## 6. [Needs confirmation] Параметры LLD/акций только на скриншотах

- [p0292](../../../rag/chunks/p0201-p0300/p0292-c01.md)–[p0301](../../../rag/chunks/p0301-p0400/p0301-c01.md): exact discovery IP range, agent check operands, SNMP community и Operations в рисунках 7.1–7.15; текст объясняет логику `agent.hostname`/UP/OS/filter и два SNMP OID, но не все поля.
- [p0304](../../../rag/chunks/p0301-p0400/p0304-c01.md)–[p0313](../../../rag/chunks/p0301-p0400/p0313-c01.md): precise autoreg action filters, `Processor` discovery prototype key/units и теговые значения в рисунках 7.17–7.35; полные значения = `RAG_MISS`.
- [p0316](../../../rag/chunks/p0301-p0400/p0316-c01.md)–[p0325](../../../rag/chunks/p0301-p0400/p0325-c01.md): ключ JMX discovery дан текстом, **точная JMX Type item prototype** в рисунке 7.41; точные шаги SNMP walk-to-JSON preprocessing — в рисунках 7.54 и 7.57, отсутствуют структурированные данные → `RAG_MISS`.
- [p0329](../../../rag/chunks/p0301-p0400/p0329-c01.md)–[p0334](../../../rag/chunks/p0301-p0400/p0334-c01.md): конкретные host prototype fields, JSONPath definitions и custom interface из рисунков 7.62–7.72 не извлечены в полном объёме, хотя текст перечисляет макросы и JSON keys. Нельзя выдавать complete deployable rule.
- **Решение:** не реконструировать Screenshot-only settings по памяти модели; ссылаться на поддержанные concepts, markers `RAG_MISS` и `[Needs confirmation]`.

## 7. [Needs confirmation] Ресурсоёмкость Discovery и безусловная автоматизация

- [p0293](../../../rag/chunks/p0201-p0300/p0293-c01.md) предлагает 5 минут для network scan, но советует более длинный интервал (например 1 час) с учётом объёма IP range и нагрузки. [p0311](../../../rag/chunks/p0301-p0400/p0311-c01.md) аналогично предупреждает о тяжести Windows LLD с update interval 1 минута.
- Production scan scope, concurrency, retries, probe rate, права создания host и защита от ложных registrations не описаны. Проверка network authorization и resource budget = `[Needs confirmation]`.

## 8. [Needs confirmation / destructive] Удаление LLD rules или исходного host удаляет автоматически созданные hosts

- **Точное смысловое предупреждение автора:** [p0335](../../../rag/chunks/p0301-p0400/p0335-c01.md) сообщает, что после удаления узла сети или LLD-правила, которое обнаружило hosts, **эти автоматически созданные hosts тоже будут удалены**. Требуется backup.
- Рецепт **не содержит** полной процедуры восстановить созданные hosts, привязанные templates, все исторические значения и rollback таких удалений. Запретить тестовое удаление ради проверки; `[Needs confirmation]`.

## 9. [Needs confirmation] Состояние после изменения agent hostname и server activation

- [p0292](../../../rag/chunks/p0201-p0300/p0292-c01.md) и [p0303](../../../rag/chunks/p0301-p0400/p0303-c01.md) меняют Zabbix agent2 config, но глава не даёт явной проверенной restart-команды и полной цепочки устранения ошибок `ServerActive`/сетевого фильтра.
- Не дописывать команды systemd/Windows по памяти: фактическая процедура apply changes зависит от целевого окружения и остаётся `[Needs confirmation]`.

**Конец главы:** [p0335](../../../rag/chunks/p0301-p0400/p0335-c01.md) — последнее предупреждение о cascade delete, [p0336](../../../rag/chunks/p0301-p0400/p0336-c01.md) — глава 8. Отдельных итоговых вопросов/ответов/упражнений нет; условные chapter-end файлы не публикуются.
