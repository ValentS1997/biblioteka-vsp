# Глава 13 — cheatsheet: AWS / Azure / Docker

Только accepted RAG PDF **490–510**. Точные данные полей, находящиеся на рисунках, — `RAG_MISS`. В главе нет разрешения на изменение реальных облачных аккаунтов.

## Symptom / problem framing

| Симптом | Первый вопрос | Источник |
|---|---|---|
| `AWS by HTTP` не находит EC2/RDS/S3 | Верно ли настроены credentials/policy, нужный AWS region и три discovery rules? | [p0494](../../../rag/chunks/p0401-p0500/p0494-c01.md)–[p0498](../../../rag/chunks/p0401-p0500/p0498-c01.md) |
| Некоторые ресурсы AWS не видны | Ресурсы в разных регионах? Каждый host в примере содержит `{$AWS.REGION}`; для нескольких регионов нужны отдельные hosts | [p0496](../../../rag/chunks/p0401-p0500/p0496-c01.md) |
| AWS metrics присутствуют, но растёт стоимость | Учитывается ли оплачиваемое использование CloudWatch, частота API запросов и масштабы discovery? | [p0491](../../../rag/chunks/p0401-p0500/p0491-c01.md) |
| Azure template не получает данные | Какой Application ID выбран, существует ли действующий client secret Value, назначена ли роль Reader на нужной Subscription, верен Tenant ID? | [p0501](../../../rag/chunks/p0501-p0600/p0501-c01.md)–[p0505](../../../rag/chunks/p0501-p0600/p0505-c01.md) |
| Azure host создан, но VM/DB не появляется | Сработали ли шесть LLD rules `Azure by HTTP` и применены ли host prototypes/templates нужного resource type? | [p0505](../../../rag/chunks/p0501-p0600/p0505-c01.md)–[p0507](../../../rag/chunks/p0501-p0600/p0507-c01.md) |
| `Docker by Zabbix agent 2` нет данных | Установлен ли **Agent 2**, есть ли доступ к Docker, работает ли master `docker.info`? | [p0507](../../../rag/chunks/p0501-p0600/p0507-c01.md)–[p0509](../../../rag/chunks/p0501-p0600/p0509-c01.md) |
| Контейнер обнаружен, но метрики пусты | `docker.containers.discovery` создал `{#NAME}`, `docker.container_info` возвращает master data, preprocessing/dependent item связан? | [p0509](../../../rag/chunks/p0501-p0600/p0509-c01.md)–[p0510](../../../rag/chunks/p0501-p0600/p0510-c01.md) |

## Baseline / context

Нужен установленный Zabbix 7, готовые AWS ресурсы EC2/RDS/S3 и Azure DB/VM, host с работающим Docker и Zabbix Agent 2. Текст **не обучает созданию облачной инфраструктуры или Docker containers** ([p0490](../../../rag/chunks/p0401-p0500/p0490-c01.md), [p0491](../../../rag/chunks/p0401-p0500/p0491-c01.md), [p0499](../../../rag/chunks/p0401-p0500/p0499-c01.md), [p0507](../../../rag/chunks/p0501-p0600/p0507-c01.md)). `lar-book-rocky`, `lar-book-aws`, `lar-book-azure`, `Docker containers`, `zbx-home` и IP `10.16.16.102` — учебные значения.

## Read-only checks

- **AWS:** `Data collection → Hosts`, template `AWS by HTTP`, macro name `{$AWS.REGION}` и факт присутствия credentials (без их вывода). `Data collection → Templates → AWS by HTTP → Discovery`: ожидаются три LLD rules EC2/RDS/S3. `Monitoring → Latest data` и созданные hosts показывают результат ([p0496](../../../rag/chunks/p0401-p0500/p0496-c01.md)–[p0498](../../../rag/chunks/p0401-p0500/p0498-c01.md)).
- **AWS IAM:** убедиться, что policy scoped к фактическому Zabbix template и разрешённым API. JSON inline policy на рисунке, точные IAM Actions в RAG **не содержатся** — `RAG_MISS` ([p0493](../../../rag/chunks/p0401-p0500/p0493-c01.md)–[p0494](../../../rag/chunks/p0401-p0500/p0494-c01.md)).
- **Azure:** проверить **факт** наличия App ID, secret Value, Subscription ID и Tenant ID, дату истечения client secret и роль Reader на выбранной Subscription. Чувствительное значение не копировать в лог или разговор ([p0501](../../../rag/chunks/p0501-p0600/p0501-c01.md)–[p0505](../../../rag/chunks/p0501-p0600/p0505-c01.md)).
- **Azure:** `Azure by HTTP → Discovery` — шесть правил; подтверждение созданных VM/DB hosts и зависимых resource templates ([p0505](../../../rag/chunks/p0501-p0600/p0505-c01.md)–[p0507](../../../rag/chunks/p0501-p0600/p0507-c01.md)).
- **Docker:** проверить Agent 2, `docker.info`, `docker.containers.discovery`, `{#NAME}`, `docker.container_info`, зависимые items. Чтение frontend — **Read-only**; сами API/agent polls **Workload-generating** ([p0508](../../../rag/chunks/p0501-p0600/p0508-c01.md)–[p0510](../../../rag/chunks/p0501-p0600/p0510-c01.md)).

## Interpretation

**Cloud by HTTP**: Zabbix `Script` item выполняет JavaScript→cloud API→JSON. **LLD host prototypes** создают дочерние hosts и привязывают специализированные templates. AWS — **три** LLD правила, Azure — **шесть**. Успех добавления host *не доказывает* ни факт получения данных, ни полноту регионов/подписок ([p0497](../../../rag/chunks/p0401-p0500/p0497-c01.md)–[p0498](../../../rag/chunks/p0401-p0500/p0498-c01.md), [p0505](../../../rag/chunks/p0501-p0600/p0505-c01.md)–[p0507](../../../rag/chunks/p0501-p0600/p0507-c01.md)).

**Docker agent 2**: вместо облачного HTTP-key сбор начинается с **локального агента**, ключа `docker.info`, зависимых item, discovery контейнеров и образов. `docker.containers.discovery` публикует `{#NAME}`, а `docker.container_info` даёт данные одного контейнера; препроцессинг разбивает master на отдельные метрики ([p0509](../../../rag/chunks/p0501-p0600/p0509-c01.md)–[p0510](../../../rag/chunks/p0501-p0600/p0510-c01.md)).

**IAM и privilege:** AWS inline policy и Azure Reader — отдельные scopes; нельзя утверждать безопасность без проверки текущего состава прав. `gpasswd -a zabbix docker` может выдать широкие права на Docker daemon, не следует автоматически применять на production host. Источник её приводит, но не оценивает безопасность ([p0508](../../../rag/chunks/p0501-p0600/p0508-c01.md)).

## Next action

Диагностическая цепочка: **scope/регион → auth/permissions → API или docker.info → JSON raw → LLD rules → host/item prototypes → Latest data**. Остановиться на первом недоказанном шаге. Для AWS сначала понять стоимость, для Azure — IAM и expiration, для Docker — права и источник master.

## Modifying action

- Создание AWS IAM user/inline policy/access keys: **State-changing / Security-sensitive**, риск избыточных прав и утечки; перед запуском потребуется формальная проверка policy JSON `RAG_MISS`.
- Azure Enterprise app/App registration/client secret/role assignment: **State-changing / Security-sensitive**, область роли — только необходимая Subscription; проверить сроки и необходимость каждого принципала.
- `Data collection → Hosts → Create host`, Macros, template binding: **State-changing**, запускает LLD и может создать много hosts, API requests и стоимость; проверка — обнаруженные ресурсы, Latest data.
- Установка/перезапуск Agent 2 и `gpasswd -a zabbix docker`: **State-changing / Privileged**, меняет пакеты, сервис и разрешения Docker. Без оценки эквивалентных привилегий не выполнять.
- Сетевые/облачные проверки: **Workload-generating**, могут влиять на CloudWatch/API quotas и Docker host.

## Verification / acceptance checks

1. AWS template корректно собирает данные из **предусмотренных регионов**, API permissions минимальны и стоимость CloudWatch заранее оценена.
2. EC2/RDS/S3 обнаружены правильным template, специализированные hosts имеют актуальные значения, нет случайного массового создания.
3. Azure четыре macro **привязаны к правильным идентификаторам**, Reader назначен на нужную Subscription, secret действителен, VM/DB обнаружены.
4. Docker Agent 2 работает; master `docker.info` отдаёт данные, LLD обнаруживает ожидаемые контейнеры/образы, per-container items обновляются.
5. Не осталось неразрешённого широкого доступа к Docker, IAM и открытых credentials в logs/Git.

## Rollback

Текст главы **не описывает** полный безопасный rollback AWS IAM access key/policy, Azure App/role/client secret, установленных пакетов/группы `docker`, удаления LLD-created hosts, расходов за ранее сделанные API calls. Любое восстановление, key rotation, пользовательская политика Docker socket = `[Needs confirmation]`. Не объявлять исторические значения восстановимыми без плана.

[Source findings](source-findings.md) сохраняет ошибки нумерации и непроверенные значения рисунков. Статус чтения не изменяется.
