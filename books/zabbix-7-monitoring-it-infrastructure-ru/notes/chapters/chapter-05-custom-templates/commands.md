# Глава 5 — команды и операции, подтверждённые RAG

**Источниковая политика:** RAG-only PDF 197–228. В главе большинство операций выполняется через Zabbix UI. Не добавлять CLI/REST-синтаксис, которого нет в источнике. Классы: **Read-only** (наблюдение), **Workload-generating** (выполнение SNMP/LLD без изменения конфигурации), **State-changing** (запись шаблонов, хостов, сервисов).

## 1. Создание шаблона, тегов, items и триггеров

| Шаг из главы | Класс | Эффект, риск, проверка и rollback |
|---|---|---|
| `Data collection → Templates` (просмотр) | Read-only | Список template groups и имен; [p0198](../../../rag/chunks/p0101-p0200/p0198-c01.md) |
| `Create template`: имя, template group, description → `Add` | State-changing | Новый собственный `Custom Linux by SNMP`. Риск ошибок соглашения об именовании, проверка — запись в списке. Полный rollback `[Needs confirmation]`; [p0198](../../../rag/chunks/p0101-p0200/p0198-c01.md)–[p0200](../../../rag/chunks/p0101-p0200/p0200-c01.md) |
| `Templates → Custom Linux by SNMP → Tags` | State-changing при Update | Теги `class:os`, `target:linux`; проверка — `Monitoring → Problems` на связанном хосте; [p0201](../../../rag/chunks/p0201-p0300/p0201-c01.md)–[p0202](../../../rag/chunks/p0201-p0300/p0202-c01.md) |
| `Templates → Items → Create item` | State-changing | `sysName` по числовому SNMP OID `.1.3.6.1.2.1.1.5.0`; после привязки шаблона item создаётся на хосте; [p0204](../../../rag/chunks/p0201-p0300/p0204-c01.md)–[p0207](../../../rag/chunks/p0201-p0300/p0207-c01.md) |
| `Data collection → Hosts → Create host` → `Templates`/`Macros` | State-changing | SNMP-host и привязка template с учётными данными; риск раскрытия/неверного значения secrets, проверить `Monitoring → Latest data`; [p0205](../../../rag/chunks/p0201-p0300/p0205-c01.md)–[p0207](../../../rag/chunks/p0201-p0300/p0207-c01.md) |
| `Templates → Triggers → Create trigger` / `Tags → scope` | State-changing | Trigger уровня template распространяется на уже связанные host; в примере `change` для hostname, проверить полученное событие; точная expression только на рис. 5.15–5.16: `RAG_MISS`; [p0208](../../../rag/chunks/p0201-p0300/p0208-c01.md)–[p0209](../../../rag/chunks/p0201-p0300/p0209-c01.md) |
| `Templates → Macros → Update` | State-changing | Значение `{$...}` на уровне template; host-level override меняет эффективный префикс `lar-` → `dev-`; проверка унаследованных macro и нового trigger; [p0210](../../../rag/chunks/p0201-p0300/p0210-c01.md)–[p0214](../../../rag/chunks/p0201-p0300/p0214-c01.md) |

Книга рекомендует **клон** стандартного шаблона и добавление собственного префикса, а не правку исходного готового template ([p0200](../../../rag/chunks/p0101-p0200/p0200-c01.md)). Полное восстановление ранее связанных хостов после структурных изменений не описано: `[Needs confirmation]`.

## 2. SNMP CLI — диагностические запросы

Источник [p0203](../../../rag/chunks/p0201-p0300/p0203-c01.md) содержит следующую форму `snmpwalk`, **здесь только с placeholders вместо тестовых credentials**:

```sh
# Workload-generating — SNMPv3 запрос; не изменяет конфигурацию агента.
# Значения секретов в CLI могут оказаться в истории shell или списке процессов.
snmpwalk -v3 -l authPriv -u <SNMP_USER> -a SHA -A "<AUTH_SECRET>" -x AES -X "<PRIV_SECRET>" <HOST_IP> .1
```

Команда отправляет запрос по SNMP-дереву `.1`, может создавать нагрузку и раскрывать выбранные секреты в CLI. Перед запуском требуются собственные host/user и согласованный scope. Проверка: полученные OID соответствуют целевому устройству. Rollback отсутствует (настройки не менялись); **внешнее измерение всё же создаёт трафик**.

```sh
# Read-only перевод/отображение OID с доступной MIB; p204
snmptranslate .1.3.6.1.2.1.1.5.0
```

В книге `-On` используется для числовых SNMP OID ([p0204](../../../rag/chunks/p0201-p0300/p0204-c01.md)); точная строка имени из рисунка 5.9 не извлечена. Для item в примере: **SNMP OID** `.1.3.6.1.2.1.1.5.0`, **key** `sysName` ([p0207](../../../rag/chunks/p0201-p0300/p0207-c01.md)). Проверка — Latest data на host.

## 3. Тестовый hostname, SNMP daemon — меняют систему

Строки из [p0209](../../../rag/chunks/p0201-p0300/p0209-c01.md) и [p0211](../../../rag/chunks/p0201-p0300/p0211-c01.md) (параметры имени заменены там, где это нужно):

```sh
# State-changing — меняет системное имя, может повлиять на сервисы.
hostnamectl set-hostname <TEST_HOSTNAME>
# В книге затем:
exec bash
systemctl restart snmpd
```

Для первого примера текст использует `lar-book-agent-t`, для второго `dev-book-agent`. **Не выполнять на рабочем хосте ради демонстрации**. `exec bash` изменяет текущую shell-сессию; `systemctl restart snmpd` прерывает/перезапускает SNMP обслуживание. Проверка: следующий SNMP poll и событие trigger change; в книге указывается исчезновение PROBLEM при очередной проверке через 30 минут ([p0209](../../../rag/chunks/p0201-p0300/p0209-c01.md)). Полный rollback hostname и восстановления соединений: `[Needs confirmation]`.

## 4. Low-level Discovery и управление жизненным циклом

| GUI-действие | Класс | Что меняет и как проверять |
|---|---|---|
| `Templates → Value mapping → Add → Update` | State-changing | Преобразование значений scoped на template/host, не глобальное в Zabbix 6+; проверить применённое значение; [p0215](../../../rag/chunks/p0201-p0300/p0215-c01.md)–[p0216](../../../rag/chunks/p0201-p0300/p0216-c01.md) |
| `Templates → Discovery rules → Create discovery rule` | State-changing | Новый LLD для интерфейсов SNMP, источник указывает дерево `.1.3.6.1.2.1.2`; поля со скриншотов = `RAG_MISS`; [p0216](../../../rag/chunks/p0201-p0300/p0216-c01.md)–[p0217](../../../rag/chunks/p0201-p0300/p0217-c01.md) |
| `Delete lost resources = Immediately` | **State-changing / destructive** | Учебная настройка удаляет LLD items и triggers вместе с историей при исчезновении интерфейса. **Нельзя использовать для production по умолчанию**; [p0217](../../../rag/chunks/p0201-p0300/p0217-c01.md) |
| `Discovery rules → Item prototypes → Create item prototype` | State-changing | Создаёт шаблон будущего item, например Operational status, привязанный к `{#IFNAME}` и `{#SNMPINDEX}`; проверить экземпляры на host; [p0218](../../../rag/chunks/p0201-p0300/p0218-c01.md)–[p0223](../../../rag/chunks/p0201-p0300/p0223-c01.md) |
| `Clone` prototype | State-changing при сохранении | Повторное использование формы для другого item, требует независимой проверки key/OID; [p0220](../../../rag/chunks/p0201-p0300/p0220-c01.md) |
| `Trigger prototypes → Create trigger prototype` + Tags | State-changing | Триггер для каждого обнаруженного интерфейса; в тексте p224 `Operational status=0`, `Admin status=1`; исходниковая семантика значения требует `[Needs confirmation]`; [p0221](../../../rag/chunks/p0201-p0300/p0221-c01.md)–[p0224](../../../rag/chunks/p0201-p0300/p0224-c01.md) |
| `Data collection → Hosts → Discovery rules → Test` | Workload-generating | Посмотреть фактический JSON обнаружения и `{#IFNAME}`; не считать скриншот JSON поддержанным текстом; [p0222](../../../rag/chunks/p0201-p0300/p0222-c01.md) |

**Конкретные текстовые SNMP-данные** (из [p0222](../../../rag/chunks/p0201-p0300/p0222-c01.md)–[p0223](../../../rag/chunks/p0201-p0300/p0223-c01.md)):

```text
.1.3.6.1.2.1.2.2.1.2.1 = STRING: lo
.1.3.6.1.2.1.2.2.1.2.2 = STRING: ens192
.1.3.6.1.2.1.2.2.1.8.1 = INTEGER: up(1)
.1.3.6.1.2.1.2.2.1.8.2 = INTEGER: up(1)
```

Индексы 1 и 2 принадлежат **конкретному учебному устройству**. В абзаце на p222 перед этими значениями указан несогласованный OID с дополнительным сегментом: он зафиксирован в [source-findings.md](source-findings.md), не «исправлен» здесь по памяти.

Для SNMP-видимости книга приводит пример `/etc/snmp/snmpd.conf`: `view systemview included .1` ([p0216](../../../rag/chunks/p0201-p0300/p0216-c01.md)). **State-changing при редактировании**, расширяет видимое SNMP-дерево. Риск расширения поверхности данных; проверка — согласованный SNMPwalk, безопасная роль/view и rollback: `[Needs confirmation]`. Не рекомендовать вслепую.

## 5. Вложенные шаблоны

`Data collection → Templates → Create template`, создать `Custom Linux uptime by SNMP` (State-changing) → `Items → Create item` (System Uptime; параметры из рисунков `RAG_MISS`) → вернуться в `Custom Linux by SNMP` → поле `Templates` и `Update` (**State-changing**, создаёт связь) → `Data collection → Hosts → Items` (**Read-only**) и проверить появление item из вложенного template ([p0225](../../../rag/chunks/p0201-p0300/p0225-c01.md)–[p0228](../../../rag/chunks/p0201-p0300/p0228-c01.md)). Откат и предотвращение циклической структуры не обсуждаются: `[Needs confirmation]`.

**Общие ограничения:** точные credentials SNMP/macro из скриншотов и реальные значения принадлежат конкретному окружению. Полные обратные процедуры восстановления удалённых LLD resources и их истории отсутствуют. Проверка фактических Zabbix API/пакетов и нынешней документации не выполнялась (RAG-only).
