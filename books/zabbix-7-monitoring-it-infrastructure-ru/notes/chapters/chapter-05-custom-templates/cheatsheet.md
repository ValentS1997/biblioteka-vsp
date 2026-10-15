# Глава 5 — cheatsheet

**Источник:** только принятый RAG PDF 197–228; [provenance и граница](README.md).

## Symptom / problem framing

| Признак | Диагностический вопрос | Источник |
|---|---|---|
| На host нет item из шаблона | Связан ли шаблон с host, сохранён ли item в template и заданы ли SNMP interface/macros? | [p0205](../../../rag/chunks/p0201-p0300/p0205-c01.md)–[p0207](../../../rag/chunks/p0201-p0300/p0207-c01.md) |
| `sysName` не получает значение | Совпадают ли OID `.1.3.6.1.2.1.1.5.0`, выбранный host/SNMP credentials и ожидаемый числовой OID? | [p0203](../../../rag/chunks/p0201-p0300/p0203-c01.md)–[p0207](../../../rag/chunks/p0201-p0300/p0207-c01.md) |
| Триггер `change` сработал после переименования, затем вернулся в OK | Отрабатывает ли повторный опрос, и совпадает ли шаблонный trigger с item? | [p0208](../../../rag/chunks/p0201-p0300/p0208-c01.md)–[p0209](../../../rag/chunks/p0201-p0300/p0209-c01.md) |
| При смене макроса триггер сравнивает не с тем префиксом | Проверить унаследованный template macro и переопределение на host: пример `lar-` → `dev-` | [p0212](../../../rag/chunks/p0201-p0300/p0212-c01.md)–[p0213](../../../rag/chunks/p0201-p0300/p0213-c01.md) |
| LLD не создаёт item/trigger для нового интерфейса | Проверить discovery JSON, `{#IFNAME}`, `{#SNMPINDEX}`, item/trigger prototype и статус SNMP | [p0216](../../../rag/chunks/p0201-p0300/p0216-c01.md)–[p0223](../../../rag/chunks/p0201-p0300/p0223-c01.md) |
| LLD исчезает вместе с историей после пропажи объекта | Проверить `Delete lost resources`: учебное `Immediately` может удалить историю | [p0217](../../../rag/chunks/p0201-p0300/p0217-c01.md) |
| У host не виден item из nested template | Проверить связь родительского `Custom Linux by SNMP` с `Custom Linux uptime by SNMP` | [p0225](../../../rag/chunks/p0201-p0300/p0225-c01.md)–[p0228](../../../rag/chunks/p0201-p0300/p0228-c01.md) |

## Baseline / context

Книга использует Zabbix server/веб-интерфейс, учебный SNMPv3 host из главы 3, демонстрационный шаблон `Custom Linux by SNMP` и SNMPv3 credentials. В SNMP-демонстрации OID hostname `.1.3.6.1.2.1.1.5.0`; сетевые интерфейсы `lo` и `ens192` показывают **только пример** индексов 1 и 2 ([p0203](../../../rag/chunks/p0201-p0300/p0203-c01.md), [p0222](../../../rag/chunks/p0201-p0300/p0222-c01.md)). Адрес, community/пароли, номер интерфейса и имена необходимо брать из собственных измерений.

## Read-only checks

- `Data collection → Templates`: проверить имя, template group, Tags, Macros, Items, Triggers и связанный шаблон ([p0198](../../../rag/chunks/p0101-p0200/p0198-c01.md), [p0201](../../../rag/chunks/p0201-p0300/p0201-c01.md), [p0226](../../../rag/chunks/p0201-p0300/p0226-c01.md)).
- `Monitoring → Latest data`: пришло ли значение `sysName` и с какого item/host ([p0207](../../../rag/chunks/p0201-p0300/p0207-c01.md)).
- `Monitoring → Problems`: присутствуют ли у событий `class:os` и `target:linux` ([p0202](../../../rag/chunks/p0201-p0300/p0202-c01.md)).
- `snmptranslate .1.3.6.1.2.1.1.5.0`: перевод представления OID (**read-only локально**), [p0204](../../../rag/chunks/p0201-p0300/p0204-c01.md).
- `snmpwalk` в источнике получает SNMP-дерево: **workload-generating**, не локальная модификация; не использовать в буквальном виде учебные SNMP secrets ([p0203](../../../rag/chunks/p0201-p0300/p0203-c01.md)).
- `Discovery rules` на уровне host → `Test`: получить фактический discovery JSON (**workload-generating**, выполнение проверки) и сопоставить `{#IFNAME}`/`{#SNMPINDEX}` ([p0222](../../../rag/chunks/p0201-p0300/p0222-c01.md)).
- `Data collection → Hosts → Items`: проверить, что nested uptime item действительно пришёл из второго шаблона ([p0226](../../../rag/chunks/p0201-p0300/p0226-c01.md)–[p0228](../../../rag/chunks/p0201-p0300/p0228-c01.md)).

## Interpretation

- **Template vs host:** шаблон определяет общие items, triggers и tags; каждый host хранит собственные значения ([p0207](../../../rag/chunks/p0201-p0300/p0207-c01.md)).
- **Item name/key/OID:** в примере числовой `SNMP OID` и символический key `sysName`; текст рекомендует не зависеть от MIB ([p0204](../../../rag/chunks/p0201-p0300/p0204-c01.md), [p0207](../../../rag/chunks/p0201-p0300/p0207-c01.md)).
- **Macros:** `{$...}` — пользовательские; `{HOST.HOST}` — встроенный; host-level значение может переопределить template-level ([p0212](../../../rag/chunks/p0201-p0300/p0212-c01.md)–[p0214](../../../rag/chunks/p0201-p0300/p0214-c01.md)).
- **LLD:** обнаружение возвращает имя интерфейса и SNMPINDEX; item prototypes создают элементы для каждого интерфейса, trigger prototypes — триггеры; Value mapping живёт на template/host, а не на глобальном уровне ([p0215](../../../rag/chunks/p0201-p0300/p0215-c01.md)–[p0224](../../../rag/chunks/p0201-p0300/p0224-c01.md)).
- **Nested templates:** второй шаблон входит в первый, поэтому item наследуется хостом через цепочку; это уменьшает дублирование, но усложняет дерево ([p0225](../../../rag/chunks/p0201-p0300/p0225-c01.md)–[p0228](../../../rag/chunks/p0201-p0300/p0228-c01.md)).

## Next action

Локализовать **первый несогласованный слой**: template item/trigger → host binding/macros/SNMP → discovery raw JSON → item/trigger prototype → final Latest data/Problems. Прежде чем менять `Delete lost resources`, определить последствия для истории. Неподтверждённый OID из примера не исправлять по памяти модели.

## Modifying action

- `Create template`, `Tags`, `Items`, `Triggers`, `Macros`: **State-changing**, влияет на все связанные host; проверка — отображение у host и фактическое значение, rollback полной цепочки `[Needs confirmation]`.
- `hostnamectl set-hostname ...`, `systemctl restart snmpd`: **State-changing**, может нарушить разрешение имён/наблюдение; перед тестом требуется восстановительный план и проверка после изменения ([p0209](../../../rag/chunks/p0201-p0300/p0209-c01.md), [p0211](../../../rag/chunks/p0201-p0300/p0211-c01.md)).
- `Create discovery rule`/Item prototypes/Trigger prototypes: **State-changing**, создаёт новые наборы monitored resources и нагрузку SNMP; проверка — host-level discovery test и созданные items ([p0216](../../../rag/chunks/p0201-p0300/p0216-c01.md)–[p0223](../../../rag/chunks/p0201-p0300/p0223-c01.md)).
- `Delete lost resources = Immediately`: **State-changing и потенциально destructive**, в книге только для учебного шаблона. Не выбирать для production без политики retention ([p0217](../../../rag/chunks/p0201-p0300/p0217-c01.md)).
- `Templates` в редакторе родителя: привязка вложенного шаблона **State-changing**, влияет на связанные host; верификация — uptime item виден у host ([p0226](../../../rag/chunks/p0201-p0300/p0226-c01.md)).

## Verification / acceptance checks

1. Шаблон создан с осмысленным именем, SNMP-префиксом и группой; стандартный шаблон не изменён напрямую.
2. Теги `class:os` и `target:linux` видимы у соответствующих событий.
3. Значение `sysName` получено, item относится к правильному host и OID, не к чужому интерфейсу.
4. Проверены триггер `change` и macro overrides; тест hostname произведён только безопасным способом.
5. Discovery `Test` возвращает ожидаемые интерфейсы; item/triggers созданы по обоим индексам.
6. Настройка исчезающих ресурсов не приводит к нежелательной потере истории.
7. Uptime item вложенного шаблона появился у host без прямого дублирования.

## Rollback

Книга предлагает клонировать стандартный шаблон для возможности вернуться к исходному, но **не описывает полный rollback** hostname/snmpd, SNMP-пользователя, macro permissions, template inheritance и **восстановление истории после удаления LLD resources**. Для них `[Needs confirmation]`, потерянная история не объявляется восстановимой ([p0200](../../../rag/chunks/p0101-p0200/p0200-c01.md), [p0217](../../../rag/chunks/p0201-p0300/p0217-c01.md)).

**Ограничение:** точные item prototype/trigger expression/macro fields, показанные только на рисунках, помечены `RAG_MISS` и не додумываются. Несогласованность OID и статусов — [source-findings.md](source-findings.md).
