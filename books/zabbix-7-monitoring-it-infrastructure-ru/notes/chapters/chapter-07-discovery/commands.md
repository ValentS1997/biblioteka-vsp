# Глава 7 — команды и операции из RAG

**Источниковый режим:** RAG-only PDF 291–335. `Read-only` — просмотр без сохранения, `Workload-generating` — запросы/проверки с нагрузкой, `State-changing` — запись конфигурации, создание хостов, установка пакетов или отправка данных. Секреты, адреса и учебные имена **не являются** production-значениями.

## 1. Сетевое обнаружение Zabbix Agent 2

Учебные источниковые пути и параметры ([p0292](../../../rag/chunks/p0201-p0300/p0292-c01.md)–[p0297](../../../rag/chunks/p0201-p0300/p0297-c01.md)):

```ini
# Linux: /etc/zabbix/zabbix_agent2.conf
Hostname=lar-book-disc-lnx
# Windows: C:\Program Files\Zabbix Agent 2\zabbix_agent2.conf
Hostname=lar-book-disc-win
```

`vim /etc/zabbix/zabbix_agent2.conf` / сохранение Windows config — **State-changing**: меняет идентификацию агентного узла; проверка — фактический ответ `agent.hostname`. В главе не описан точный restart Zabbix Agent 2 после редактирования и полный rollback: `[Needs confirmation]`.

| UI-действие | Класс | Эффект и контроль |
|---|---|---|
| `Data collection → Discovery → Create discovery rule` | State-changing | Создаёт сетевой scan по IP-range и агентному check `agent.hostname`; нагрузка зависит от диапазона и update interval (в примере 5 минут, возможен 1 час). Проверить в `Monitoring → Discovery`; [p0292](../../../rag/chunks/p0201-p0300/p0292-c01.md)–[p0293](../../../rag/chunks/p0201-p0300/p0293-c01.md) |
| `Alerts → Actions → Discovery actions → Create action` | State-changing | Условия service=Zabbix Agent, discovery status UP и `lnx`/`win` из имени; операции создают host, группу (включая `Discovered hosts`) и template; [p0294](../../../rag/chunks/p0201-p0300/p0294-c01.md)–[p0297](../../../rag/chunks/p0201-p0300/p0297-c01.md) |
| `Data collection → Host groups → Create host group` | State-changing | Группа Windows, затем Windows-specific Discovery action; риск неверной классификации; [p0295](../../../rag/chunks/p0201-p0300/p0295-c01.md) |
| `Monitoring → Discovery` и `Data collection → Hosts` | Read-only | Сверить IP/service, rule, новое имя, group и linked template; [p0295](../../../rag/chunks/p0201-p0300/p0295-c01.md)–[p0297](../../../rag/chunks/p0201-p0300/p0297-c01.md) |

Большой диапазон/малый интервал могут чрезмерно нагружать сервер. Не сканировать чужие/неразрешённые IP. Все конкретные параметры rule и operations на рисунках 7.1–7.7 = `RAG_MISS`.

## 2. Сетевое SNMP discovery

```sh
# State-changing: учебное изменение системного имени и рестарт SNMP.
hostnamectl set-hostname <TRAINING_SNMP_HOSTNAME>
exec bash
systemctl restart snmpd
```

Эти формы зафиксированы на [p0298](../../../rag/chunks/p0201-p0300/p0298-c01.md). Они могут повлиять на имя и непрерывность SNMP-сбора; выполнять только после согласования влияния и подготовленного отката `[Needs confirmation]`.

Далее `Data collection → Discovery → Create discovery rule` (**State-changing**) по проверке **SNMPv2 agent**, IP range, community, OID hostname; затем `Alerts → Actions → Discovery actions → Create action` (**State-changing**) с привязкой groups/templates и `Monitoring → Discovery` (**Read-only**) для результата ([p0299](../../../rag/chunks/p0201-p0300/p0299-c01.md)–[p0302](../../../rag/chunks/p0301-p0400/p0302-c01.md)).

Точные OID текстового источника ([p0302](../../../rag/chunks/p0301-p0400/p0302-c01.md)):

```text
.1.3.6.1.2.1.1.5.0       # sysName / device hostname
.1.3.6.1.2.1.25.1.4.0    # учебный boot-image признак OS
```

**Важное:** авторский пример SNMPv2 требует community, но окружение предыдущих глав могло использовать SNMPv3; выбор версии не подтверждён автоматически. Строка `BOOT_IMAGE=...` свидетельствует только об учебной ОС, универсальная идентификация Linux/вендора через второй OID не гарантирована. SNMP walkthrough — **Workload-generating**, цель/credentials проверить на собственном устройстве; rollback rules `[Needs confirmation]`.

## 3. Авторегистрация активного Zabbix Agent 2

```ini
# /etc/zabbix/zabbix_agent2.conf
ServerActive=<AUTHORIZED_ZABBIX_SERVER_OR_PROXY>
Hostname=<HOSTNAME_FOR_AUTOREGISTRATION>
# Optional: HostMetadata, HostInterface, HostInterfaceItem
```

`vim /etc/zabbix/zabbix_agent2.conf` и сохранение этих параметров **State-changing** ([p0303](../../../rag/chunks/p0301-p0400/p0303-c01.md)–[p0308](../../../rag/chunks/p0301-p0400/p0308-c01.md)). В тексте имя необязательно задавать — агент может получить системное hostname. На стороне frontend:

`Alerts → Actions → Autoregistration actions → Create action` (**State-changing**), условие по имени `lar-book-lnx` (если применимо), `Operations`: добавить к `Linux servers` и связать `Linux by Zabbix agent active` ([p0304](../../../rag/chunks/p0301-p0400/p0304-c01.md)–[p0306](../../../rag/chunks/p0301-p0400/p0306-c01.md)). Проверка `Data collection → Hosts` — **Read-only** ([p0307](../../../rag/chunks/p0301-p0400/p0307-c01.md)). `HostMetadata` для host-classification — отдельная возможность, но p308 ошибочно называет маршрут `Discovery action`, см. findings.

Риск: слишком широкое Autoregistration action разрешит создание нежелательных хостов и подключение чрезмерных шаблонов. Откат/отключение действия в источнике `[Needs confirmation]`.

## 4. Windows performance counter LLD

- На Windows `perfmon.exe` (Read-only при осмотре) → Performance Monitor → + → категория `Processor` ([p0309](../../../rag/chunks/p0301-p0400/p0309-c01.md)–[p0310](../../../rag/chunks/p0301-p0400/p0310-c01.md)).
- `Data collection → Templates → Create template` с именем `Windows performance by Zabbix agent` (**State-changing**) → `Discovery rules → Create discovery rule` c ключом **`perf_instance.discovery[Processor]`**; source p311 предупреждает об интервале **1 минута** и рекомендует рассмотреть **1 час** для снижения нагрузки ([p0311](../../../rag/chunks/p0301-p0400/p0311-c01.md), [p0314](../../../rag/chunks/p0301-p0400/p0314-c01.md)).
- `Item prototypes → Create item prototype` и `Tags` (**State-changing**), host `lar-book-disc-win` → link template → `Update` (**State-changing**); `Monitoring → Latest data` (**Read-only**) для нового набора items ([p0312](../../../rag/chunks/p0301-p0400/p0312-c01.md)–[p0315](../../../rag/chunks/p0301-p0400/p0315-c01.md)).
- Текстовый LLD-result (подтверждено p314):
```json
[
  {"{#INSTANCE}":"0"},
  {"{#INSTANCE}":"1"},
  {"{#INSTANCE}":"_Total"}
]
```

`{#INSTANCE}` создаёт три экземпляра item (в книге пример `% C1 time`). Полный item key/parameter из рисунков = `RAG_MISS`; не подставлять его по догадке.

## 5. JMX MemoryPool discovery

`Data collection → Templates → Create template` → `App Apache Tomcat JMX discovery` → `Discovery rules → Create discovery rule` → `Item prototypes → Create item prototype` (**State-changing**). У item tag `component:memory pool`; шаблон link к `lar-book-jmx`, проверка `Monitoring → Latest data` с фильтром по тегу ([p0316](../../../rag/chunks/p0301-p0400/p0316-c01.md)–[p0319](../../../rag/chunks/p0301-p0400/p0319-c01.md)).

Точный ключ discovery из [p0319](../../../rag/chunks/p0301-p0400/p0319-c01.md):

```text
jmx.discovery[beans,"*:type=MemoryPool,name=*"]
```

`name=*` используется для `{#JMXNAME}`; item prototype получает JMX-атрибут `Type` на каждом найденном pool ([p0319](../../../rag/chunks/p0301-p0400/p0319-c01.md)–[p0320](../../../rag/chunks/p0301-p0400/p0320-c01.md)). Доступность Java gateway и целевого JMX host из главы 3 обязательна; security settings JMX не пересоздаются здесь. Верификация реального target и authorization `[Needs confirmation]`.

## 6. Dependent SNMP GetBulk LLD

`Data collection → Templates → Create template BOOK Linux by SNMP → Tags` (**State-changing**), `Mass update → Value mapping → Add from host` и `Hosts → Items → Copy → Target type Templates` (**State-changing**, увеличивает переиспользование настроек; [p0321](../../../rag/chunks/p0301-p0400/p0321-c01.md)–[p0323](../../../rag/chunks/p0301-p0400/p0323-c01.md)).

`Templates → Discovery rules → Create discovery rule` типа **Dependent item**, master `SNMP interfaces bulk`; `Preprocessing` конвертирует SNMP walk → JSON; затем `Item prototypes` с обработкой по `{#SNMPINDEX}` и теги. Верификация host `lar-book-snmp_bulk` в `Monitoring → Latest data`: в книге может требоваться по одной минуте для LLD item и появления значения ([p0323](../../../rag/chunks/p0301-p0400/p0323-c01.md)–[p0327](../../../rag/chunks/p0301-p0400/p0327-c01.md)).

Текстовый OID base `.1.3.6.1.2.1.2.2.1` и поле `.1.3.6.1.2.1.2.2.1.2` для `{#IFDESCR}` подтверждены; `{#SNMPINDEX}` задаёт уникальность. **Нужные шаги/регулярные выражения из рисунков 7.54/7.57 = RAG_MISS**. Избегать раздельных избыточных SNMP polls, если master bulk уже собирает данные.

## 7. JSON host LLD: sender, trapper и cron

Из [p0328](../../../rag/chunks/p0301-p0400/p0328-c01.md)–[p0334](../../../rag/chunks/p0301-p0400/p0334-c01.md):
```sh
# State-changing: установка sender
dnf install zabbix-sender
# либо для Ubuntu:
apt install zabbix-sender
# State-changing: изменение пользовательского crontab
crontab -e
```

**Запрещён к копированию как рабочий рецепт:** p329 демонстрирует повреждённую cron строку с `-k 200",`, разрывами JSON и `vmip`; рядом правильнее показана лишь **структура**, тоже без полного валидного payload:
```text
* * * * *  zabbix_sender -z 127.0.0.1 -s lar-lldhost-creation -k lldhosts.raw -o <VALIDATED_JSON_PAYLOAD> >/dev/null 2>&1
```
Это **схема аргументов из авторского объяснения**, не команда к исполнению (placeholder, нет подтверждённой процедуры quoting, validation или rollback); частота раз в минуту **State-changing/Workload-generating**, stderr перенаправляется в `/dev/null`, что осложняет диагностику ([p0329](../../../rag/chunks/p0301-p0400/p0329-c01.md)).

Текстовые данные `vmname`, `vmip`, `vmlocation` из [p0331](../../../rag/chunks/p0301-p0400/p0331-c01.md)–[p0333](../../../rag/chunks/p0301-p0400/p0333-c01.md) превращаются в `{#VMNAME}`, `{#VMIP}`, `{#VMLOCATION}` с `LLD macros` и JSONPath. `Data collection → Hosts → Create host` `lar-lldhost-creation` + `Items → Create item` (key `lldhosts.raw` по тексту) → `Discovery rules → Create discovery rule` → `LLD macros` → `Host prototypes → Create host prototype` и Custom interface. Все **State-changing**. `Data collection → Hosts` и наблюдение новых hosts — **Read-only**.

**Критическое предупреждение [p0335](../../../rag/chunks/p0301-p0400/p0335-c01.md):** при удалении LLD rule либо исходного host созданные hosts могут быть удалены. Перед изменением жизненного цикла нужен backup и подтверждённая процедура возврата. Источник её не приводит: `[Needs confirmation]`.

## Приёмка и rollback

Проверить наличие каждого created host/template/LLD item и корректность исходных данных (особенно JSON и SNMP index), а не только зелёное действие в UI. Установку agent/sender, cron, SNMP, actions и host prototypes откатывать **только по отдельно подтверждённой процедуре** `[Needs confirmation]`. Ни команда удаления cron, ни гарантированное восстановление cascade deleted hosts в главе не предоставлены.
