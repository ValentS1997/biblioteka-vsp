# Глава 8. Настройка прокси-серверов Zabbix

**Книга:** «Zabbix 7: мониторинг ИТ-инфраструктуры», третье обновлённое русское издание (2025). Inventory **0020**, `book_id: zabbix-7-monitoring-it-infrastructure-ru`.

## Provenance и границы

- Режим **RAG-only**: только принятый книжный RAG, `rag/acceptance.yaml: ACCEPTED`; ни исходный PDF напрямую, ни внешние ссылки, ни знания модели не использовались для заполнения пробелов.
- **PDF 336–370**, адресуемые chunks `zabbix-7-monitoring-it-infrastructure-ru:p0336:c01` … `zabbix-7-monitoring-it-infrastructure-ru:p0370:c01`; [начало главы 8](../../../rag/chunks/p0301-p0400/p0336-c01.md); [начало главы 9](../../../rag/chunks/p0301-p0400/p0371-c01.md).
- Canonical source SHA-256 `07204d885d4bf4c6c2de7c71ae42a4e3ed4cea794169cbe07985552e63875a27`. Corpus generation `6a5221f8e8a0f88b400905d7334879edff6f5451d9ab7f6e56bb203809018986`.
- Параметры форм UI и точные значения макросов, представленные **только на рисунках 8.1–8.42**, отдельно не извлечены в текстовый RAG: `RAG_MISS`.

## Карта разделов

| Раздел | PDF-страницы | Назначение |
|---|---:|---|
| Настройка Zabbix proxy | 337–340 | Релизные пакеты, SQLite3, `zabbix_proxy.conf`, режимы буфера |
| Работа с пассивными Zabbix proxy | 340–344 | `ProxyMode=1`; Zabbix server инициирует соединение на порт 10051 |
| Работа с активными Zabbix proxy | 344–347 | `ProxyMode=0`; Zabbix proxy инициирует соединение с сервером |
| Мониторинг узлов сети с помощью Zabbix proxy | 348–352 | `Monitored by → Proxy`, agent `ServerActive`, store-and-forward |
| Шифрование соединения Zabbix proxy с помощью PSK | 352–355 | `TLSConnect/TLSAccept`, уникальная пара PSK identity/secret |
| Настройка балансировки нагрузки Zabbix proxy | 355–360 | Proxy groups, active agent address, `Minimum number of proxies`, `Failover period` |
| Использование обнаружения Zabbix proxy | 360–363 | Proxy-backed Discovery и autoregistration (с рискованным удалением hosts) |
| Мониторинг состояния Zabbix proxy | 363–370 | Local/Remote Zabbix proxy health, agent, StatsAllowedIP, Queue overview |

## Архитектура и смысл

**Zabbix proxy** выполняет локальный сбор и предварительную обработку данных; Zabbix server получает их через proxy. Это позволяет разгрузить центральный сервер, сократить количество открытых соединений через периметр и мониторить удалённые площадки. При обрыве связи proxy продолжает сбор и хранение до заданного срока `ProxyOfflineBuffer`; текст источника приводит **1 час по умолчанию** ([p0336](../../../rag/chunks/p0301-p0400/p0336-c01.md), [p0350](../../../rag/chunks/p0301-p0400/p0350-c01.md)–[p0352](../../../rag/chunks/p0301-p0400/p0352-c01.md)). Это не гарантия безусловного сохранения истории.

**Passive proxy** (`ProxyMode=1`): сервер Zabbix инициирует соединение, передаёт конфигурацию и получает собранные данные по TCP/10051. **Active proxy** (`ProxyMode=0`): сам proxy обращается к серверу, запрашивает конфигурацию и отправляет данные/heartbeat. Авторы рекомендуют active как обычный вариант, оставляя passive для обоснованных случаев ([p0338](../../../rag/chunks/p0301-p0400/p0338-c01.md), [p0343](../../../rag/chunks/p0301-p0400/p0343-c01.md)–[p0347](../../../rag/chunks/p0301-p0400/p0347-c01.md)).

**База и буфер:** пример устанавливает `zabbix-proxy-sqlite3` и `DBName=/tmp/zabbix_proxy.sqlite3`. Автор описывает гибридное буферизование новых установок, режим памяти и дисковый режим; `ProxyBufferMode` определяет поведение. **Удаление SQLite-файла может уничтожить ещё не переданные метрики**, а режим только памяти приводит к потере при рестарте; гибридный режим сбрасывает данные в БД перед корректным рестартом по описанию книги ([p0338](../../../rag/chunks/p0301-p0400/p0338-c01.md)–[p0340](../../../rag/chunks/p0301-p0400/p0340-c01.md)). Условия хранения в `/tmp`, права и перенос в production не раскрыты полностью: `[Needs confirmation]`.

**Назначение хостов:** `Data collection → Hosts → Monitored by → Proxy` меняет фактический путь сбора; при активном agent нужно согласовать адрес прокси в `ServerActive`. После переназначения связь может временно выглядеть серой из-за обновления конфигурации ([p0348](../../../rag/chunks/p0301-p0400/p0348-c01.md)–[p0350](../../../rag/chunks/p0301-p0400/p0350-c01.md)).

**Шифрование PSK:** параметры `TLSConnect=psk`, `TLSAccept=psk`, `TLSPSKIdentity`, `TLSPSKFile` должны согласовываться с `Administration → Proxies → Encryption`; для passive и active используются разные направления UI. Источник рекомендует уникальную пару ключ/identity, но показывает `cat` файла с ключом, неверный синтаксис `chmod 400/etc/...` и смешанный регистр `Systemctl` — не копировать их как безопасную процедуру ([p0353](../../../rag/chunks/p0301-p0400/p0353-c01.md)–[p0355](../../../rag/chunks/p0301-p0400/p0355-c01.md), [source-findings.md](source-findings.md)).

**Proxy groups**: начиная с описанного в главе Zabbix 7, proxy group объединяет активные и пассивные экземпляры, определяет адреса для active agents и позволяет переносить работу при сбое. Необходимо выбрать `Minimum number of proxies`, `Failover period`, учитывать способность одного экземпляра выдержать нагрузку оставшихся. Для SNMP traps группа может потребовать дополнительной маршрутизации/репликации ([p0355](../../../rag/chunks/p0301-p0400/p0355-c01.md)–[p0360](../../../rag/chunks/p0301-p0400/p0360-c01.md)).

**Discovery через proxy:** network rule `Discovery by → Proxy` позволяет перенести сетевой опрос; agent autoregistration перенаправляет `ServerActive` на proxy. В сценарии предложено удаление ранее созданных hosts перед перенастройкой, но **воспроизводимый план сохранения истории отсутствует** ([p0361](../../../rag/chunks/p0301-p0400/p0361-c01.md)–[p0363](../../../rag/chunks/p0301-p0400/p0363-c01.md)).

**Наблюдаемость самого proxy:** локальный Zabbix Agent 2 + host monitored by proxy, remote `Remote Zabbix proxy health` с `StatsAllowedIP` и IP/port macros, а также `Administration → Queue → Queue overview by proxy`; долгое ожидание значений (5 минут/более 10 минут) может означать проблему производительности ([p0364](../../../rag/chunks/p0301-p0400/p0364-c01.md)–[p0370](../../../rag/chunks/p0301-p0400/p0370-c01.md)).

## Порядок практического изучения и проверки

1. Проверить сетевую архитектуру, разрешённые потоки, источник пакетов и размер нагрузки; выбрать модель SQLite3/БД и буфера.
2. Установить proxy в контролируемой лаборатории; документировать режим, `Server`, `Hostname`, `DBName`; проверить журнал и сервис.
3. Зарегистрировать proxy в `Administration → Proxies`, сверить имя, режим, `Last seen (age)` и `Encryption`; **No encryption** — учебное, не защищённый production default.
4. Подключить тестовые host через `Monitored by`, согласовать active agent `ServerActive`; проверить `Latest data`, журналы и восстановление после синхронизации.
5. Для PSK подготовить уникальный ключ и безопасную политику secrets; согласовать обе стороны **до изменения**, отдельно наблюдать возврат Last seen.
6. Создать `Proxy group` только после расчёта требуемой ёмкости и сетевого пути active agent; проверить failover согласно плану.
7. Перевести Discovery/Autoregistration на proxy **без предварительного удаления production hosts**, составить план сохранения истории/авторегистрации.
8. Настроить local и remote proxy health и регулярно разбирать `Queue overview by proxy`.

## Файлы

[Операционная памятка](cheatsheet.md) · [Команды/UI](commands.md) · [Mermaid](diagram.md) · [Компактная SVG](visual-cheatsheet.svg) · [Подробная SVG](visual-cheatsheet-detailed.svg) · [Source findings](source-findings.md).

**Границы:** рисунки UI в RAG не дают проверенных точных полей; команды с дефектами не исправляются молча. Нет полного rollback удалённой SQLite истории, пересозданных hosts, failed PSK-rotation и миграции proxy group. `[Needs confirmation]`. p0370 заканчивается очередями, p0371 — новая глава; отдельных chapter-end вопросов/упражнений нет. **Статус чтения не изменён.**

Контракты: `process-compliance-router v1.2`, `session-recovery v1.0`, `chapter-analysis-request v1.4`, `chapter-artifact-collection v1.8`, `chapter-publication v1.0`.
