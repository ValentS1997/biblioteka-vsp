# Глава 4 — cheatsheet

**Источник:** принятый RAG, PDF **161–196**. Provenance и границы: [README](README.md).

## Symptom / problem framing

| Симптом | Что локализовать | RAG |
|---|---|---|
| SSH-trigger срабатывает в неверном состоянии | Сначала проверить фактическое `1=UP / 0=DOWN` и формулу; **в книге противоречие**, не повторять непроверенный SSH-рецепт | [p0167](../../../rag/chunks/p0101-p0200/p0167-c01.md), [p0168](../../../rag/chunks/p0101-p0200/p0168-c01.md) |
| Триггер переходит обратно в OK слишком быстро | Выделить условие PROBLEM, отдельно настроить `Recovery expression` и проверить оба условия | [p0169](../../../rag/chunks/p0101-p0200/p0169-c01.md)–[p0170](../../../rag/chunks/p0101-p0200/p0170-c01.md) |
| Порог срабатывает слишком часто / событие пропущено | Severity, интервал данных, порог, логика `or`/`and`; тестирование значений | [p0166](../../../rag/chunks/p0101-p0200/p0166-c01.md)–[p0173](../../../rag/chunks/p0101-p0200/p0173-c01.md) |
| Предиктивный trigger ведёт себя неожиданно | Проверить `timeleft`: окно исходных данных, горизонт прогноза, выбранный item, прогнозируемый порог | [p0176](../../../rag/chunks/p0101-p0200/p0176-c01.md), [p0179](../../../rag/chunks/p0101-p0200/p0179-c01.md) |
| PROBLEM появляется, а Email отсутствует | Проверить Trigger action, Operations, Media type SMTP и `Users → Media`; событие и сообщение — разные этапы | [p0182](../../../rag/chunks/p0101-p0200/p0182-c01.md)–[p0190](../../../rag/chunks/p0101-p0200/p0190-c01.md) |
| Слишком много неинформативных уведомлений | Сначала стандартизировать names, severity, tags `component/scope` и message templates; потом пересматривать маршрутизацию | [p0190](../../../rag/chunks/p0101-p0200/p0190-c01.md)–[p0194](../../../rag/chunks/p0101-p0200/p0194-c01.md) |

## Baseline / context

В книге используются уже настроенные Zabbix server + MariaDB + NGINX/Apache и Linux-hosts `lar-book-agent_simple` (порт 22 / HTTP item) и `lar-book-agent_passive` (готовые items, Linux template), оставшиеся после главы 3. Требуются актуальные значения item и корректный host/template — иначе триггер нечего оценивать ([p0161](../../../rag/chunks/p0101-p0200/p0161-c01.md)–[p0165](../../../rag/chunks/p0101-p0200/p0165-c01.md)). Реальные хосты и адреса заменяются параметрами окружения.

## Read-only checks

- `Data collection → Hosts → Triggers`: просмотреть expression, recovery expression и severity; `Add → Select/Function` при создании является настройкой, но просмотр списка функций — чтение ([p0162](../../../rag/chunks/p0101-p0200/p0162-c01.md), [p0166](../../../rag/chunks/p0101-p0200/p0166-c01.md)).
- `ip addr` / `ifconfig`: исходником предложены для выяснения реального имени интерфейса; **Read-only** ([p0163](../../../rag/chunks/p0101-p0200/p0163-c01.md), [p0165](../../../rag/chunks/p0101-p0200/p0165-c01.md)).
- `Expression constructor → Test`: проверка сценарных значений в UI; без изменения конфигурации триггера, но запускает вычисление выражения (**workload-generating**) ([p0181](../../../rag/chunks/p0101-p0200/p0181-c01.md)–[p0182](../../../rag/chunks/p0101-p0200/p0182-c01.md)).
- `Dashboards` и соответствующие экраны Problems: наблюдать фактическое состояние после обновления item; это не тест маршрута Email ([p0163](../../../rag/chunks/p0101-p0200/p0163-c01.md)).
- `Alerts → Actions → Trigger actions`: просмотр условий и операций; `Alerts → Media types → Email` и `Users → Users → Media`: проверка настройки канала и адресата ([p0182](../../../rag/chunks/p0101-p0200/p0182-c01.md)–[p0189](../../../rag/chunks/p0101-p0200/p0189-c01.md)).

## Interpretation

- Триггер состоит из функции, host/template, item key, оператора, константы; поддерживает арифметические/логические операции, `change`, `and`, `or`, `not`. Новый синтаксис начинается **с функции**, путь host/item разделяется `/`; старый (до 5.4) начинался с `{host:key.function()}` ([p0167](../../../rag/chunks/p0101-p0200/p0167-c01.md)–[p0173](../../../rag/chunks/p0101-p0200/p0173-c01.md)).
- Для возвращения при наличии recovery expression требуется **PROBLEM = FALSE** и **RECOVERY = TRUE** ([p0170](../../../rag/chunks/p0101-p0200/p0170-c01.md)).
- `trendavg` — агрегаты часовых трендов, пример недельной давности и порога 800 Мбит/с; `timeleft` — прогноз достижения 100 % на основе 7 часов истории, меньше чем через неделю; time shift — сравнение средних прошлой и текущей недель ([p0178](../../../rag/chunks/p0101-p0200/p0178-c01.md)–[p0181](../../../rag/chunks/p0101-p0200/p0181-c01.md)).
- `Operations` уведомляют при появлении PROBLEM, `Recovery operations` при OK, `Update operations` при обновлениях; способ доставки и аккаунт получателя конфигурируются отдельно ([p0183](../../../rag/chunks/p0101-p0200/p0183-c01.md)–[p0190](../../../rag/chunks/p0101-p0200/p0190-c01.md)).

## Next action

Выбрать конкретное наблюдаемое расхождение: **item/value → trigger expression/recovery → action condition/operation → media type → user media → информативность сообщения**. Исправлять минимальный слой после проверки предыдущего. Для SSH **не пользоваться ошибочно трактуемым 0/1** без проверки исходного item и реальной функции; findings сохраняет обе формулировки.

## Modifying action

- `Create trigger` / `Update`: сохраняет expression, severity, tags; **State-changing** — может вызвать события/инциденты. Проверка: Expression Test + наблюдаемое событие, процедура полного отката не приведена `[Needs confirmation]`.
- **Не выполнять** тестовое правило `iptables -A INPUT ... --destination-port 22 -j DROP` на production; это **State-changing / service-disrupting**, может отрезать SSH и меняет firewall. Исходник не даёт команд безопасного восстановления: `[Needs confirmation]` ([p0163](../../../rag/chunks/p0101-p0200/p0163-c01.md)).
- `Alerts → Actions → Create action`: Enabled, Operations/Recovery/Update; **State-changing**, риск оповещения неверного списка пользователей; проверить на согласованном учебном событии. Rollback `[Needs confirmation]`.
- `Alerts → Media types → Email`: SMTP и Message templates; `Users → Media`: адрес и способ. **State-changing**, риск утечки деталей инцидентов или недоставки. Проверка end-to-end на получателе; точный тест/обратная операция **не описаны** `[Needs confirmation]`.
- `Administration → General → Trigger displaying options`: меняет название уровней важности глобального интерфейса, необязательно для функциональности триггеров; оценить влияние на командный словарь ([p0194](../../../rag/chunks/p0101-p0200/p0194-c01.md)–[p0196](../../../rag/chunks/p0101-p0200/p0196-c01.md)).

## Verification / acceptance checks

1. Исходный item возвращает ожидаемое значение; trigger expression фактически выдаёт ожидаемый TRUE/FALSE, без неоднозначности SSH 0/1.
2. Severity соответствует важности события; при необходимости recovery expression сохраняет PROBLEM до правильного момента.
3. `trendavg`/`timeleft`/time shift проверены на подходящих интервалах и тестовых цифрах (`Expression constructor → Test`).
4. Для уведомления есть сопоставленные action, операции PROBLEM/RECOVERY/UPDATE, media type, пользователь и адрес — и получатель действительно подтвердил тестовое сообщение. Конкретная процедура тестирования доставки из главы `[Needs confirmation]`.
5. Имя и теги передают смысл; шаблон сообщения содержит полезные поля, нет лишних дублей.

## Rollback

Глава **не содержит** полной процедуры удаления firewall `DROP`, возврата предыдущих action/SMTP, шаблонов, severity и подавления уже отправленных писем. Для таких операций: `[Needs confirmation]`. До модификаций сохранять существующие значения; автоматическое восстановление не предполагается.

**Ограничения:** точные значения trigger builder, SMTP, значения скриншотов p163–p195 = `RAG_MISS`. [Source findings](source-findings.md).
