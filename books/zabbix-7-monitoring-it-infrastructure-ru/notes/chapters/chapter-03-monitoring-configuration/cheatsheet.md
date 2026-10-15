# Глава 3 — cheatsheet

**Источник:** принят RAG PDF 93–160; полная provenance — [README](README.md). Разделяет чтение состояния и изменения в конфигурации; не предназначен для слепого запуска на production.

## Symptom / problem framing

| Признак | Первый проверяемый слой | RAG |
|---|---|---|
| Не приходят значения Agent 2 | `Server`/пассивный режим; `ServerActive` и точный `Hostname`/активный режим; соответствующий template и правильный интерфейс | [p0095](../../../rag/chunks/p0001-p0100/p0095-c01.md)–[p0100](../../../rag/chunks/p0001-p0100/p0100-c01.md) |
| Simple check сообщает, что SSH «не работает» | Проверка отражает доступность TCP-сервиса **со стороны Zabbix server/proxy**, а не обязательно локальное состояние SSH | [p0116](../../../rag/chunks/p0101-p0200/p0116-c01.md), [p0122](../../../rag/chunks/p0101-p0200/p0122-c01.md) |
| SNMP bulk пришёл, а зависимый item пуст | Сопоставить исходный OID, индекс интерфейса, мастера, dependent item, preprocessing | [p0110](../../../rag/chunks/p0101-p0200/p0110-c01.md)–[p0115](../../../rag/chunks/p0101-p0200/p0115-c01.md) |
| Trapper не показывает сообщение | Сверить `-z`, `-s` (имя хоста), `-k` (ключ), `-o` и существующий trapper item | [p0120](../../../rag/chunks/p0101-p0200/p0120-c01.md)–[p0122](../../../rag/chunks/p0101-p0200/p0122-c01.md) |
| Calculated/dependent выводит не ту метрику | Проверить исходный item, расчет/предобработку; dependent без обработки повторяет мастера | [p0125](../../../rag/chunks/p0101-p0200/p0125-c01.md)–[p0130](../../../rag/chunks/p0101-p0200/p0130-c01.md) |
| JMX item не собирает данные | Java gateway, настройки `JavaGateway` и `StartJavaPollers`, доступность target Tomcat/JMX | [p0133](../../../rag/chunks/p0101-p0200/p0133-c01.md)–[p0135](../../../rag/chunks/p0101-p0200/p0135-c01.md) |
| Не работает мониторинг SQL | ODBC, драйвер/DSN, тест `isql -v book`, DB credential/macros | [p0136](../../../rag/chunks/p0101-p0200/p0136-c01.md)–[p0139](../../../rag/chunks/p0101-p0200/p0139-c01.md) |
| HTTP/browser item не получает желаемое | Ответ HTTP/JSONPath либо Selenium/WebDriver/JS и зависимый item соответственно | [p0140](../../../rag/chunks/p0101-p0200/p0140-c01.md)–[p0153](../../../rag/chunks/p0101-p0200/p0153-c01.md) |
| `system.run` «Unsupported» | RAG связывает это с запретом ключа агента; включение ключа — изменение с повышенным риском | [p0155](../../../rag/chunks/p0101-p0200/p0155-c01.md)–[p0156](../../../rag/chunks/p0101-p0200/p0156-c01.md) |

## Baseline / context

Исходная среда книги — установленный Zabbix server с MariaDB и веб-интерфейсом; отдельные Linux-хосты и, где требуется, SNMPv3, MariaDB/ODBC, Tomcat JMX или web endpoint. Главная страница для проверки `Monitoring → Latest data`; настройка узлов/элементов через `Data collection → Hosts → Items`. В книге используется Zabbix 7.0, Rocky Linux/Ubuntu и демонстрационные адреса; версии пакетов и безопасность окружения надо подтвердить самостоятельно ([p0093](../../../rag/chunks/p0001-p0100/p0093-c01.md), [p0094](../../../rag/chunks/p0001-p0100/p0094-c01.md), [p0136](../../../rag/chunks/p0101-p0200/p0136-c01.md)).

## Read-only checks

- `ip addr` — узнать адрес на Linux-хосте до настройки пассивного агента ([p0095](../../../rag/chunks/p0001-p0100/p0095-c01.md)).
- `Monitoring → Hosts → Latest data` — подтверждать приход значений и тип item, а не только существование записи хоста ([p0097](../../../rag/chunks/p0001-p0100/p0097-c01.md), [p0113](../../../rag/chunks/p0101-p0200/p0113-c01.md)).
- `snmpwalk` — запрашивать OID/индексы интерфейсов; это **workload-generating**, а не изменение конфигурации; SNMPv3 credentials из книги нельзя публиковать буквально ([p0110](../../../rag/chunks/p0101-p0200/p0110-c01.md)).
- `cat /etc/zabbix/zabbix_server.conf | grep ExternalScripts=` — прочесть расположение каталога внешних скриптов ([p0130](../../../rag/chunks/p0101-p0200/p0130-c01.md)).
- `odbcinst -j` — вывести расположение ODBC-конфигов; `isql -v book` — **workload-generating** проверка DB-соединения ([p0136](../../../rag/chunks/p0101-p0200/p0136-c01.md)–[p0137](../../../rag/chunks/p0101-p0200/p0137-c01.md)).
- `Data collection → Hosts → Items` — читать текущие ключи, статусы поддерживаемости и шаги preprocessing перед изменением ([p0155](../../../rag/chunks/p0101-p0200/p0155-c01.md)).
- `Monitoring → Latest data → History` — изучить исходную строку, а не только финальное значение ([p0156](../../../rag/chunks/p0101-p0200/p0156-c01.md)).

## Interpretation

- **Agent passive:** запрос инициирует server/proxy; **active:** агент отправляет значения. Режим определяется типом элемента и `ServerActive`/условиями сети, активному важно имя хоста ([p0098](../../../rag/chunks/p0001-p0100/p0098-c01.md)–[p0101](../../../rag/chunks/p0101-p0200/p0101-c01.md)).
- **SNMP:** OID — путь к конкретной метрике; новый `walk[]` собирает пачку OID, а preprocessing извлекает нужный индекс/поле; сырое значение при необходимости не хранить ([p0106](../../../rag/chunks/p0101-p0200/p0106-c01.md), [p0112](../../../rag/chunks/p0101-p0200/p0112-c01.md)–[p0115](../../../rag/chunks/p0101-p0200/p0115-c01.md)).
- **Simple check:** измеряет доступность с точки обзора Zabbix, в примере порт 22; **trapper:** принимает отправку через `zabbix_sender` ([p0121](../../../rag/chunks/p0101-p0200/p0121-c01.md)–[p0122](../../../rag/chunks/p0101-p0200/p0122-c01.md)).
- **Calculated:** вычисляет среднюю память за 15 минут; **dependent:** из master item извлекает значение по заданной предобработке, собственного интервала не имеет ([p0124](../../../rag/chunks/p0101-p0200/p0124-c01.md)–[p0129](../../../rag/chunks/p0101-p0200/p0129-c01.md)).
- **External:** скрипт Zabbix server отдаёт результат через STDOUT/STDERR; **JMX:** Java gateway; **ODBC:** SQL-запрос через ODBC-драйвер; **HTTP:** извлечение части ответа JSONPath; **browser:** JavaScript/WebDriver с зависимыми метриками ([p0131](../../../rag/chunks/p0101-p0200/p0131-c01.md)–[p0153](../../../rag/chunks/p0101-p0200/p0153-c01.md)).
- **Preprocessing:** операции выполняются последовательно; пример Regexp с выводом `\2` извлекает счётчик RX bytes, `Discard unchanged` отбрасывает повторы. `Custom on fail` определяет обработку неудачи регулярного выражения ([p0157](../../../rag/chunks/p0101-p0200/p0157-c01.md)–[p0160](../../../rag/chunks/p0101-p0200/p0160-c01.md)).

## Next action

Сначала выбрать, какая сторона инициирует передачу (server/proxy, agent, sender, web/DB/JMX, browser), найти **первое место без проверенного значения** и использовать относящийся к нему раздел. Не смешивать неисправность сети, ошибку ключа, отсутствие прав, ошибку preprocessing и неправильное сопоставление OID. Результат сверять в Latest data и в состоянии item.

## Modifying action

- **Agent:** установка `zabbix-agent2`, настройка `zabbix_agent2.conf`, перезапуск; эффект — новый сбор/потоки; риск — неправильный `Hostname` и нет метрик; проверка — зелёный ZBX и Latest data ([p0094](../../../rag/chunks/p0001-p0100/p0094-c01.md)–[p0100](../../../rag/chunks/p0001-p0100/p0100-c01.md)).
- **SNMP:** создание пользователя SNMPv3, изменение `snmpd.conf`, SNMP interface и макросов; эффект — включение SNMP доступа; риск — секреты и слишком широкая view `.1`; проверка — SNMPwalk/Latest data; rollback `[Needs confirmation]` ([p0102](../../../rag/chunks/p0101-p0200/p0102-c01.md)–[p0110](../../../rag/chunks/p0101-p0200/p0110-c01.md)).
- **Trapper:** установка sender и передача значений в item; эффект — новое значение на сервере; риск — ошибочное значение/хост/ключ; проверка — Latest data; откат отправленных данных `[Needs confirmation]` ([p0120](../../../rag/chunks/p0101-p0200/p0120-c01.md)–[p0121](../../../rag/chunks/p0101-p0200/p0121-c01.md)).
- **JMX/ODBC/browser/external:** установка/конфигурация шлюза, драйвера, Selenium или исполняемого скрипта меняет службы и файловую систему. **Не использовать примеры с отключённым JMX TLS/auth и безусловным `system.run[*]` в production**; подробности в [source-findings](source-findings.md).
- **Preprocessing:** редактирование item может изменить формат/частоту сохранения данных; сначала проверить исходную строку, затем регулярное выражение, потом сохранённое значение ([p0156](../../../rag/chunks/p0101-p0200/p0156-c01.md)–[p0160](../../../rag/chunks/p0101-p0200/p0160-c01.md)).

## Verification / acceptance checks

1. Для Agent — нужный шаблон, интерфейс (где требуется), правильный host name, фактические значения.
2. Для SNMP — проходит опрос по нужным OID; dependent извлекает ожидаемые поля/индекс.
3. Для simple check — интерпретация относительно сетевого пути Zabbix server/proxy. Для trapper — совпадают имя и ключ, появилось переданное значение.
4. Для JMX/ODBC/HTTP/browser — не только доступен endpoint, но и получена ожидаемая измеримая метрика.
5. Для regex — финальные RX bytes появились; прежний дубль не хранится, если включено `Discard unchanged`.
6. Изменения средств мониторинга не ослабили защиту удалённого выполнения и не опубликовали тестовые пароли.

## Rollback

Глава показывает restart после исправления конфигурации и `Do not keep history`/Discard для ограничения хранения, но **не содержит полного отката** установки пакетов, user SNMP, изменений TLS/JMX, подключения БД, контейнера Selenium, agent `AllowKey` или изменений данных, уже принятых trapper. Для каждого: `[Needs confirmation]`. Не придумывать команды остановки/удаления не из RAG.

**Оговорка:** команды и спорные источниковые строки вынесены в [commands.md](commands.md) и [source-findings.md](source-findings.md); внешние файлы по ссылкам книги в RAG не скачивались.
