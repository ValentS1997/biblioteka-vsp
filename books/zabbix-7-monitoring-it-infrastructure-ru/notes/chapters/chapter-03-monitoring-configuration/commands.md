# Глава 3 — команды и операции, подтверждённые RAG

Источник: глава 3, PDF 93–160, `zabbix-7-monitoring-it-infrastructure-ru:p0093:c01` … `:p0160:c01`. Классы: **Read-only** (смотрит локальное состояние); **Workload-generating** (сеть/нагрузка на систему без намеренной перенастройки); **State-changing** (устанавливает пакеты, меняет состояние сервисов, пишет значения или конфигурацию). **Ни одна команда с учебными IP/паролями не является универсальной production-инструкцией.**

## Zabbix Agent 2 и режимы

| Команда/параметр источника | Тип | Эффект / граница / проверка |
|---|---|---|
| `rpm -Uvh <ZABBIX_RELEASE_RPM>` (RHEL), `wget <ZABBIX_RELEASE_DEB>` + `dpkg -i <ZABBIX_RELEASE_DEB>` (Ubuntu) | State-changing | Установка репозитория Zabbix 7.0 с дистрибутивно-специфичным пакетом; актуальный пакет = `[Needs confirmation]` ([p0094](../../../rag/chunks/p0001-p0100/p0094-c01.md)) |
| `dnf -y install zabbix-agent2` / `apt install zabbix-agent2` | State-changing | Установка Agent 2, требуется root/пакетный менеджер; [p0094](../../../rag/chunks/p0001-p0100/p0094-c01.md) |
| `ip addr` | Read-only | Обнаружить IP хоста для конфигурации; [p0095](../../../rag/chunks/p0001-p0100/p0095-c01.md) |
| `vim /etc/zabbix/zabbix_agent2.conf` | State-changing при сохранении | Обычный режим: `Server=<ZABBIX_SERVER_IP>`, `Hostname=<HOST_NAME>`. Активный: `ServerActive=<ZABBIX_SERVER_OR_PROXY>`; активный Hostname должен совпадать с именем узла в Zabbix. Для HA в источнике отдельная пунктуация списков `;` и `,`; [p0095](../../../rag/chunks/p0001-p0100/p0095-c01.md), [p0098](../../../rag/chunks/p0001-p0100/p0098-c01.md)–[p0099](../../../rag/chunks/p0001-p0100/p0099-c01.md) |
| `systemctl enable zabbix-agent2`, `systemctl restart zabbix-agent2` | State-changing | Автозапуск, перезагрузка агента. Риск временного пропуска метрик; проверить `Monitoring → Latest data`, ZBX badge ([p0095](../../../rag/chunks/p0001-p0100/p0095-c01.md), [p0100](../../../rag/chunks/p0001-p0100/p0100-c01.md)); rollback `[Needs confirmation]` |

В GUI: `Data collection → Hosts → Create host`; правильная группа, Agent interface/IP, шаблон пассивного/активного агента. Затем `Monitoring → Hosts → Latest data` (**Read-only GUI**) ([p0096](../../../rag/chunks/p0001-p0100/p0096-c01.md)–[p0100](../../../rag/chunks/p0001-p0100/p0100-c01.md)). После сохранения **State-changing**. Не считать зелёный badge единственным подтверждением; просматривать фактические значения.

## SNMPv3 и новый GetBulk

```sh
# State-changing: установка SNMP-пакетов (выполняется на соответствующей ОС)
dnf install net-snmp net-snmp-utils
apt install snmp snmpd libsnmp-dev
# State-changing: изменение конфигурации
vim /etc/snmp/snmpd.conf
# источниковый фрагмент конфигурации: расширяет видимые OID
view systemview included .1
systemctl enable snmpd
systemctl start snmpd
```

Рецепт p102–103 и p107–108. В источнике также есть `net-snmp-create-v3-user` с паролями `my_authpass` / `my_privpass` и именем `snmpv3user`. **Не переносить эти значения**; создание пользователя — State-changing, значение view `.1` расширяет объектную область. Проверка через SNMPv3-опрос, rollback/сузить view = `[Needs confirmation]`.

Пример диагностического запроса по OID интерфейсов из [p0110](../../../rag/chunks/p0101-p0200/p0110-c01.md) (Workload-generating; параметры `-A`/`-X` содержат секреты, **здесь они заменены placeholders**, не запускать без безопасного управления секретами):

```sh
snmpwalk -On -v3 -l authPriv -u <SNMP_USER> -a SHA -A "<AUTH_SECRET>" -x AES -X "<PRIV_SECRET>" <SNMP_HOST_IP> .1.3.6.1.2.1.2.2.1.2
```

Для большего объёма данных в источнике запрашивается родительский OID `.1.3.6.1.2.1.2.2.1`. В учебном примере интерфейсу `ens192` соответствует **индекс 2** — это не универсальная константа ([p0110](../../../rag/chunks/p0101-p0200/p0110-c01.md)–[p0112](../../../rag/chunks/p0101-p0200/p0112-c01.md)). Опрашиваемые SNMPv3 host interfaces и макросы `{$SNMPV3_AUTH}`, `{$SNMPV3_PRIV}` добавляются через `Data collection → Hosts` и `Administration → Macros`; эффект — настройка SNMP/секретов. Проверка: `Latest data` и extracted dependent value.

**Новый вариант:** `walk[]` мастер-элемент использует GetBulk и зависимые элементы + preprocessing для выделения OID/index ([p0111](../../../rag/chunks/p0101-p0200/p0111-c01.md)–[p0115](../../../rag/chunks/p0101-p0200/p0115-c01.md)). `Do not keep history` для сырого item в книге рекомендован против дублей; это меняет политику сохранения истории, не следует включать без проверки необходимости сырого потока. `Secret text` скрывает макрос из UI, но книга отмечает, что значение остаётся незашифрованным в базе ([p0105](../../../rag/chunks/p0101-p0200/p0105-c01.md)).

## Simple check и Zabbix sender

- `Data collection → Hosts → Items → Create item` (State-changing при Add), тип **Simple check**, ключ в RAG **`net.tcp.services[ssh,,22]`** ([p0116](../../../rag/chunks/p0101-p0200/p0116-c01.md)). Форму ключа не исправляем по памяти: она требует подтверждения, см. [source-findings.md](source-findings.md). Цель — доступность SSH по TCP 22 **со стороны Zabbix**, результат `0/1`, затем Value mapping `Up/Down` ([p0118](../../../rag/chunks/p0101-p0200/p0118-c01.md)–[p0122](../../../rag/chunks/p0101-p0200/p0122-c01.md)).
- `Data collection → Hosts → Items → Create item` с типом **Zabbix trapper** (State-changing). `dnf -y install zabbix-sender` или `apt install zabbix-sender` (State-changing). В источнике пример передачи с ключом `trap` ([p0120](../../../rag/chunks/p0101-p0200/p0120-c01.md)–[p0121](../../../rag/chunks/p0101-p0200/p0121-c01.md)):

```sh
# Workload-generating И state-changing результат в Zabbix: отправляет новое значение trapper
zabbix_sender -z <ZABBIX_SERVER_IP> -s "<REGISTERED_HOST_NAME>" -k trap -o "<TEST_VALUE>"
```

`-z` server, `-s` host name, `-k` item key, `-o` value. Передача изменяет собранную историю и может повлиять на downstream-настройки; выверить host/key до отправки, затем `Monitoring → Latest data` (Read-only). Откат уже отправленных значений источником не представлен: `[Needs confirmation]`.

## Calculated, dependent и external checks

Через `Data collection → Hosts → Items → Create item` (State-changing):
- **Calculated item:** пример — 15-минутное среднее использования памяти. Точная формула находится на рис. 3.42, текстовым RAG не подтверждена → `RAG_MISS`. Проверка — Latest data / memory ([p0124](../../../rag/chunks/p0101-p0200/p0124-c01.md)–[p0125](../../../rag/chunks/p0101-p0200/p0125-c01.md)).
- **Dependent item:** основная SSH-проверка выдаёт несколько переменных MariaDB, зависимая через preprocessing извлекает отдельную (пример — `Aborted_clients`), проверяется в Latest data ([p0125](../../../rag/chunks/p0101-p0200/p0125-c01.md)–[p0129](../../../rag/chunks/p0101-p0200/p0129-c01.md)). Параметры/выражения, показанные только на рисунках 3.45–3.49: `RAG_MISS`.
- Макросы `{$USERNAME}` и `{$PASSWORD}` из p127 — **State-changing**; учётные данные не записывать в исходные артефакты.

Внешние проверки из [p0130](../../../rag/chunks/p0101-p0200/p0130-c01.md)–[p0132](../../../rag/chunks/p0101-p0200/p0132-c01.md):

```sh
# Read-only: посмотреть каталог внешних скриптов
cat /etc/zabbix/zabbix_server.conf | grep ExternalScripts=
# State-changing при записи/изменении прав: учебный тестовый script
vim /usr/lib/zabbix/externalscripts/test_external
chmod +x /usr/lib/zabbix/externalscripts/test_external
chown zabbix:zabbix /usr/lib/zabbix/externalscripts/test_external
```

Внутри тестового файла книга использует Bash `#!/bin/bash` и `echo $1`: на вход подаётся строковый аргумент и возвращается через STDOUT. Создание исполняемого скрипта на Zabbix server — риск запуска непроверенного кода; проверка — элемент `External check` и Latest data; rollback = `[Needs confirmation]`.

## JMX и ODBC

JMX из [p0133](../../../rag/chunks/p0101-p0200/p0133-c01.md)–[p0135](../../../rag/chunks/p0101-p0200/p0135-c01.md): `/etc/zabbix/zabbix_server.conf`:

```ini
JavaGateway=127.0.0.1
StartJavaPollers=5
```

На RHEL `dnf install zabbix-java-gateway`, Ubuntu `apt install zabbix-java-gateway`, затем `systemctl enable zabbix-java-gateway`, `systemctl start zabbix-java-gateway`, `systemctl restart zabbix-server` — **State-changing**, эффект JMX-сбора через шлюз. Тестовый Tomcat на p133 использует **`authenticate=false` и `ssl=false`**: не переносить без защиты; исходная глава не описывает безопасную замену — `[Needs confirmation]`. Для отдельного Java gateway в источнике указан порт 10052.

ODBC из [p0136](../../../rag/chunks/p0101-p0200/p0136-c01.md)–[p0139](../../../rag/chunks/p0101-p0200/p0139-c01.md):

```sh
# State-changing: установка драйвера
dnf install unixODBC mariadb-connector-odbc
# Ubuntu, альтернативная ОС
apt install odbc-mariadb unixodbc unixodbc-dev odbcinst
# Read-only: расположение ODBC-конфигов
odbcinst -j
# Workload-generating: тест DB-коннекта по DSN "book"
isql -v book
```

`/etc/odbc.ini` хранит DSN, в учебном примере `[book]`, `Driver=MariaDB`, `Server=127.0.0.1`, `Port=3306`, `Database=zabbix`. **State-changing** при записи файла, риск доступа к БД и нагрузки запросов. **Несовпадение:** p137 предлагает открыть `/etc/odbc.ini` также для проверки записи драйвера `[MariaDB]`, тогда как p136 перечисляет `/etc/odbcinst.ini` в конфигурации драйверов. Не объявлять один вариант исправленным без проверки, см. findings.

## HTTP, Selenium browser, preprocessing

- HTTP agent: GUI `Data collection → Hosts → Items`, запрос к `https://services.zabbix.com/updates/v1`, поля `type=software_update_check`, `version=1.0` и hash 64 символа (p140–141), JSONPath выделяет `latest_release` (p143). **Workload-generating**: сеть и HTTP-запрос; State-changing при сохранении item. Конкретное правило JSONPath показано на рисунке и не подтверждено в тексте → `RAG_MISS`.
- Browser item: [p0144](../../../rag/chunks/p0101-p0200/p0144-c01.md) содержит `docker run -d -p 4444:4444 -p 7900:7900 --shm-size="2g" selenium/standalone-chrome:latest` — **State-changing, риск открытых портов и неприкреплённого тега latest**; не использовать как production-рецепт без внешней проверки. В `zabbix_server.conf` исходник задаёт `WebDriverURL=http://localhost:4444`, `StartBrowserPollers=2` (State-changing), затем JS-script/host macros/зависимые элементы. В учебнике команда restart имеет опечатку, а дистрибутивная установка Docker спорна: [source-findings.md](source-findings.md). Файл JS по внешней ссылке не получен; скрипт в RAG только частично показан ([p0144](../../../rag/chunks/p0101-p0200/p0144-c01.md)–[p0152](../../../rag/chunks/p0101-p0200/p0152-c01.md)).
- Preprocessing [p0155](../../../rag/chunks/p0101-p0200/p0155-c01.md)–[p0160](../../../rag/chunks/p0101-p0200/p0160-c01.md): включение `AllowKey=system.run[*]` в Agent 2 — **State-changing security-sensitive**: разрешает очень широкое удалённое выполнение; это учебный пример, не рекомендация для production. Далее книга применяет regexp, extraction group `\2`, `Custom on fail → Discard value`, `Discard unchanged`; сохраняет счётчик RX bytes интерфейса. Значение regexp на рисунке целиком = `RAG_MISS`. Проверить поддерживаемость элемента и содержимое `History` / `Latest data` перед тем, как считать результат достоверным.

## Приёмка и восстановление

После каждого изменения сверить **наблюдаемое значение** в Latest data и его source type, интерфейс, host name, key, макросы, наличие прав доступа. Документируемый rollback — частичный (например, restart); полной обратной процедуры для установленных сервисов, новых аккаунтов/базы, контейнеров и отправленных метрик **нет**: `[Needs confirmation]`. Команды, не подтверждённые RAG, здесь не добавлены.
