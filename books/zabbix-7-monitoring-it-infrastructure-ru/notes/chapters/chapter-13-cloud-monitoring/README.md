# Глава 13. Мониторинг облачной инфраструктуры

**Книга:** «Zabbix 7: мониторинг ИТ-инфраструктуры» (русское обновлённое третье издание, 2025). Inventory `0020`; book_id `zabbix-7-monitoring-it-infrastructure-ru`.

## Provenance, scope и границы

- Только **принятый RAG**; `rag/acceptance.yaml: ACCEPTED`. Прямого PDF-доступа, проверки внешних API, доступа к AWS/Azure/Docker или подстановки данных из памяти модели не было.
- **PDF 490–510 включительно**: [p0490 — начало главы](../../../rag/chunks/p0401-p0500/p0490-c01.md); [p0510 — заключительный текст главы](../../../rag/chunks/p0501-p0600/p0510-c01.md). Страница 511 не представлена содержательным chunk, [p0512](../../../rag/chunks/p0501-p0600/p0512-c01.md) — реклама иной книги и **не входит в главу 13**. Источниковый план указывает 13 глав; следующей пронумерованной главы нет.
- Адресуемый интервал: `zabbix-7-monitoring-it-infrastructure-ru:p0490:c01` … `zabbix-7-monitoring-it-infrastructure-ru:p0510:c01` (21 текстовый chunk).
- Source SHA-256: `07204d885d4bf4c6c2de7c71ae42a4e3ed4cea794169cbe07985552e63875a27`; corpus generation `6a5221f8e8a0f88b400905d7334879edff6f5451d9ab7f6e56bb203809018986`.
- В source имеются рисунки 13.1–13.36. Значения политик IAM, полей форм и script-кода, присутствующие **только на рисунках**, из текстового RAG не восстанавливаются — `RAG_MISS`.

## Карта главы

| Раздел | PDF-страницы | Задача |
|---|---:|---|
| Настройка мониторинга AWS | 491–498 | IAM, ключи, шаблон `AWS by HTTP`, регион, LLD EC2/RDS/S3 |
| Настройка мониторинга Microsoft Azure | 498–507 | Enterprise application + App registration, client secret, subscription Reader, `Azure by HTTP`, LLD Azure resources |
| Настройка мониторинга Docker | 507–510 | Zabbix Agent 2, доступ к Docker, `Docker by Zabbix agent 2`, master/dependent items и LLD контейнеров/образов |

## Основные идеи

**AWS:** Zabbix использует `AWS by HTTP`, HTTP/API Script item и JavaScript для обращений к AWS и разбора полученных ответов в JSON. Три LLD правила создают *host prototypes* для EC2, RDS и S3; обнаруженные узлы применяют специализированные templates, например `AWS EC2 by HTTP` ([p0497](../../../rag/chunks/p0401-p0500/p0497-c01.md)–[p0498](../../../rag/chunks/p0401-p0500/p0498-c01.md)). Перед использованием выделяются IAM пользователь, inline policy и access key/secret. **Сам текст JSON IAM policy не содержится в RAG**: показан на рисунке 13.5. Не разворачивать разрешения по догадке. Источник советует проверять список разрешений конкретного AWS template, т.к. он может изменяться ([p0493](../../../rag/chunks/p0401-p0500/p0493-c01.md)–[p0494](../../../rag/chunks/p0401-p0500/p0494-c01.md)). Amazon CloudWatch **может тарифицироваться**; надо оценить расходы до включения ([p0491](../../../rag/chunks/p0401-p0500/p0491-c01.md)).

На стороне Zabbix `Data collection → Hosts → Create host`: учебное имя `lar-book-aws`, группа `Cloud`, template `AWS by HTTP` и **macros с учётными данными и регионом** (подтверждено `{$AWS.REGION}`; полные поля AWS access key из рисунка 13.12 = `RAG_MISS`). Для ресурсов разных регионов источник предлагает отдельный host на регион. Состояние **после discovery** проверяется наличием EC2/RDS/S3 host prototypes и данными привязанных templates; создание собственного нового EC2/RDS/S3 для выполнения задания **не требуется**, готовая облачная инфраструктура предпосылка ([p0496](../../../rag/chunks/p0401-p0500/p0496-c01.md)–[p0498](../../../rag/chunks/p0401-p0500/p0498-c01.md)).

**Azure:** авторы сначала создают Enterprise application, затем отдельную App registration, новый client secret с ограниченным сроком и assignment роли **Reader** на Subscription. В Zabbix создают host `lar-book-azure`, группу `Cloud` и шаблон `Azure by HTTP` ([p0499](../../../rag/chunks/p0401-p0500/p0499-c01.md)–[p0505](../../../rag/chunks/p0501-p0600/p0505-c01.md)). Четыре подтверждённых macros:

| Macro | Значение из своей среды |
|---|---|
| `{$AZURE.APP.ID}` | Application ID |
| `{$AZURE.PASSWORD}` | Secret **Value**, не отображаемое позднее повторно |
| `{$AZURE.SUBSCRIPTION.ID}` | Subscription ID |
| `{$AZURE.TENANT.ID}` | Tenant ID |

Azure template содержит по тексту **шесть discovery rules**, которые посредством host prototypes создают отдельные host для VM и разных типов DB; специализированные templates и Script JavaScript items получают API data, преобразуют в JSON для LLD ([p0505](../../../rag/chunks/p0501-p0600/p0505-c01.md)–[p0507](../../../rag/chunks/p0501-p0600/p0507-c01.md)). **Временной жизненный цикл secret и роли Reader важнее удобства разового примера**; не публиковать IDs/значения credential в Git и не выдавать старую последовательность экранов как проверенную текущую UI-процедуру.

**Docker:** в отличие от cloud API, контейнеры мониторятся **локально с Zabbix Agent 2**. Установить Agent 2 на host с Docker и привязать к Zabbix host template `Docker by Zabbix agent 2`. Источник показывает `Server=10.16.16.102` лишь как учебный адрес, а также команду `gpasswd -a zabbix docker`: это изменение прав доступа к Docker engine и потенциальное существенное повышение привилегий, не универсально безопасный production шаг ([p0507](../../../rag/chunks/p0501-p0600/p0507-c01.md)–[p0509](../../../rag/chunks/p0501-p0600/p0509-c01.md)).

Обычные зависимые items получают значения из master `Docker: Get info` с Agent 2 key `docker.info`. Обнаружение использует два LLD rules — контейнеров и образов; ключ `docker.containers.discovery` формирует `{#NAME}`. Для статистики отдельного контейнера применяются `docker.container_info`, item prototypes, dependent items и preprocessing ([p0509](../../../rag/chunks/p0501-p0600/p0509-c01.md)–[p0510](../../../rag/chunks/p0501-p0600/p0510-c01.md)). Код ключей и фильтров, не находящийся в тексте источника, **не домысливается**.

## Проверяемая последовательность

1. Зафиксировать облачный scope, регионы, оплачиваемые сервисы и реальные ресурсы. До выдачи разрешений изучить фактический список IAM/API permissions в целевой среде.
2. AWS: выдать отдельному пользователю **только необходимые** permissions, безопасно получить ключи, связать `AWS by HTTP` и `{$AWS.REGION}`; проверить host discovery EC2/RDS/S3 и значения.
3. Azure: проверить связь идентичности App/Registration и client secret, назначение Reader **на нужную Subscription**, сохранить четыре macros с безопасным управлением секретами, проверить discovery и шаблоны.
4. Docker: проверить установку Agent 2/доступ к Docker socket, отдельно оценить повышенные права группы `docker`; подключить `Docker by Zabbix agent 2`, подтвердить master `docker.info`, LLD containers/images, получение зависимых метрик.
5. При проблемах: не расширять IAM роль или Docker privileges вслепую; диагностировать по цепочке **auth → API/master item → JSON → LLD → prototypes → dependent items**.

## Комплект главы и ограничения

[Cheatsheet](cheatsheet.md) · [Команды/UI](commands.md) · [Mermaid](diagram.md) · [Компактная SVG](visual-cheatsheet.svg) · [Детальная SVG](visual-cheatsheet-detailed.svg) · [Source findings](source-findings.md).

**Source findings:** AWS credential step mismatch на p0496; Azure Tenant ID ссылка на шаг не совпадает с нумерацией; отдельные Enterprise application и App registration не следует автоматически отождествлять. Полный rollback IAM/ключей, Azure role, `docker` group privileges и массово созданных LLD hosts **в этой главе не приведён**: `[Needs confirmation]`.

На p0510 расположен блок «Дополнительная информация» по Docker без отдельных итоговых review questions, review answers или summary. Соответствующие условные файлы не создаются.

**Статус чтения не изменяется.** Контракты: chapter request v1.4, artifacts v1.8, publication v1.0, recovery v1.0, process router v1.2.
