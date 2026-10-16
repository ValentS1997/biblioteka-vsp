# Глава 6 — cheatsheet

**Источник:** принятый RAG PDF 229–290; подробная provenance — [README](README.md).

## Symptom / problem framing

| Симптом | Проверяемый слой | RAG |
|---|---|---|
| График пустой | Существование item, история, время появления данных, шаблон/host, правильный LLD index | [p0230](../../../rag/chunks/p0201-p0300/p0230-c01.md)–[p0236](../../../rag/chunks/p0201-p0300/p0236-c01.md) |
| На карте неверный traffic label / indicator | Link element, точное имя host, item key, триггер; `{HOST.HOST}` в link не даёт однозначный контекст | [p0241](../../../rag/chunks/p0201-p0300/p0241-c01.md)–[p0243](../../../rag/chunks/p0201-p0300/p0243-c01.md) |
| Dashboard не показывает ожидаемые проблемы | Filters по host group, severity, acknowledgement, шаблон, наборы данных виджета | [p0244](../../../rag/chunks/p0201-p0300/p0244-c01.md)–[p0254](../../../rag/chunks/p0201-p0300/p0254-c01.md) |
| Панель template выглядит пустой | Template не содержит измерений: открыть `Monitoring → Hosts → Dashboards` у host | [p0255](../../../rag/chunks/p0201-p0300/p0255-c01.md)–[p0258](../../../rag/chunks/p0201-p0300/p0258-c01.md) |
| Inventory не заполняется на существующих hosts | Глобальный `Default host inventory mode` действует только на **новые** hosts; отдельный host mode и `Populates host inventory` item | [p0259](../../../rag/chunks/p0201-p0300/p0259-c01.md)–[p0260](../../../rag/chunks/p0201-p0300/p0260-c01.md) |
| На Geomap отсутствует host | Inventory не содержит корректных latitude/longitude или фильтр виджета не включает host | [p0261](../../../rag/chunks/p0201-p0300/p0261-c01.md)–[p0264](../../../rag/chunks/p0201-p0300/p0264-c01.md) |
| PDF scheduled report не отправляется | Наличие Chrome, Zabbix web service, AllowedIP, WebServiceURL/StartReportWriters, Frontend URL, TLS и media user | [p0270](../../../rag/chunks/p0201-p0300/p0270-c01.md)–[p0273](../../../rag/chunks/p0201-p0300/p0273-c01.md) |
| SLA не соответствует доступности отдельного агента | Дерево услуг, problem tags, порог children High, `Set status to OK`, SLA/tag selection | [p0274](../../../rag/chunks/p0201-p0300/p0274-c01.md)–[p0289](../../../rag/chunks/p0201-p0300/p0289-c01.md) |

## Baseline / context

Zabbix server, SNMP host и Custom Linux by SNMP из главы 5. Для Graph prototypes — правило LLD; для service monitoring — frontend, ICMP и agent items/triggers. Для scheduled PDF нужны собственные SMTP/media credentials и web service; тестовые имена `lar-book-templated_snmp` и `Global view` являются только примерами ([p0229](../../../rag/chunks/p0201-p0300/p0229-c01.md), [p0230](../../../rag/chunks/p0201-p0300/p0230-c01.md), [p0270](../../../rag/chunks/p0201-p0300/p0270-c01.md)).

## Read-only checks

- `Monitoring → Hosts → Graphs` — данные и графики конкретного host, в том числе из LLD; отсутствие значений сразу после добавления graph может быть временным ([p0232](../../../rag/chunks/p0201-p0300/p0232-c01.md)–[p0236](../../../rag/chunks/p0201-p0300/p0236-c01.md)).
- `Monitoring → Maps` — состояние host/links и labels; если link red, проверить привязанный trigger ([p0242](../../../rag/chunks/p0201-p0300/p0242-c01.md)–[p0243](../../../rag/chunks/p0201-p0300/p0243-c01.md)).
- `Dashboards → All dashboards` / `Monitoring → Hosts → Dashboards` — глобальные и host-level панели отличаются и применяют разные фильтры ([p0254](../../../rag/chunks/p0201-p0300/p0254-c01.md)–[p0258](../../../rag/chunks/p0201-p0300/p0258-c01.md)).
- `Inventory → Hosts` — актуальные поля, координаты и System name ([p0260](../../../rag/chunks/p0201-p0300/p0260-c01.md)–[p0261](../../../rag/chunks/p0201-p0300/p0261-c01.md)).
- `Reports → System information` — backend/frontend versions, enabled/disabled items, unsupported items, NVPS, HA; `Availability report`, `Trigger top 100`, `Audit`, `Action log`, `Notifications` — встроенная диагностика ([p0265](../../../rag/chunks/p0201-p0300/p0265-c01.md)–[p0269](../../../rag/chunks/p0201-p0300/p0269-c01.md)).
- `Reports → Action log → Info` — источник показывает ошибку при отсутствии подходящей user media; это диагностический показатель, не гарантированная доставка письма ([p0269](../../../rag/chunks/p0201-p0300/p0269-c01.md)).
- `Services → SLA report` — фильтр времени, соблюдение SLA и error budget; исторические проценты книги не являются текущими данными ([p0287](../../../rag/chunks/p0201-p0300/p0287-c01.md)–[p0289](../../../rag/chunks/p0201-p0300/p0289-c01.md)).

## Interpretation

- **Graph prototype** автоматически создаёт графики для LLD-обнаруженных интерфейсов; traffic preprocessing использует дельту за время × 8 для перевода байтов в биты ([p0234](../../../rag/chunks/p0201-p0300/p0234-c01.md)–[p0236](../../../rag/chunks/p0201-p0300/p0236-c01.md)).
- **Map** связывает элементы и link indicator с trigger; точный host name обязателен в link label (в отличие от скопированного host macro) ([p0241](../../../rag/chunks/p0201-p0300/p0241-c01.md)–[p0243](../../../rag/chunks/p0201-p0300/p0243-c01.md)).
- **Dashboard** фильтрует наборы; Top Hosts, Problems, Graph, Map, Item value, Gauge и Pie chart отличаются назначением. Панель template даёт одинаковую компоновку для многих hosts, но значения — раздельные ([p0246](../../../rag/chunks/p0201-p0300/p0246-c01.md)–[p0258](../../../rag/chunks/p0201-p0300/p0258-c01.md)).
- **Inventory global mode** затрагивает новых hosts, не задним числом; `Populates host inventory` связывает item с конкретным полем ([p0259](../../../rag/chunks/p0201-p0300/p0259-c01.md)–[p0260](../../../rag/chunks/p0201-p0300/p0260-c01.md)).
- **Scheduled PDF** рендерит выбранную dashboard через web service/Chrome и рассылает подписчикам, требуются корректные URL/TLS/media. В книге `IgnoreURLCertErrors=1` предлагается как workaround; это **не рекомендация для production** ([p0271](../../../rag/chunks/p0201-p0300/p0271-c01.md)–[p0274](../../../rag/chunks/p0201-p0300/p0274-c01.md)).
- **Service/SLA** — не сумма всех alerts: дополнительное правило frontend учитывает **двух** проблемных child High+ одновременно. Отдельный упавший agent при живом ICMP согласно рецепту не понижает frontend SLA ([p0286](../../../rag/chunks/p0201-p0300/p0286-c01.md)–[p0289](../../../rag/chunks/p0201-p0300/p0289-c01.md)).

## Next action

Диагностика по цепочке: **исходная метрика → график/map/dashboard → inventory → отчёт/почтовый маршрут → service tags/сервисное дерево → SLA report**. Не изменять другие звенья, пока предыдущие не подтверждены наблюдением. Открывать исходные values и UI-only поля `RAG_MISS` только в разрешённой среде.

## Modifying action

- `Templates → Graphs → Create graph` / `Discovery rules → Graph prototypes`: **State-changing**; создаёт графики, нагрузка на UI/историю; проверка — host graphs; откат `[Needs confirmation]`.
- `Monitoring → Maps → Create/Edit map`: **State-changing**, влияет на общие карты, связи и trigger-indicators; проверить правильный host, отделить тестовые события.
- `Dashboards → Create/Edit` / `Templates → Dashboards`: **State-changing**, меняет общую визуализацию и права доступа. Риск владельца/share при передаче на Zabbix Administrator; до изменения проверять собственный доступ ([p0244](../../../rag/chunks/p0201-p0300/p0244-c01.md)).
- `Administration → General → Other` / `Hosts → Inventory`: **State-changing**, глобальный default и host settings — разные scope; [p0259](../../../rag/chunks/p0201-p0300/p0259-c01.md)–[p0260](../../../rag/chunks/p0201-p0300/p0260-c01.md).
- `Reports → Scheduled reports → Create report/Test`: **State-changing** при сохранении и **workload-generating** при Test — PDF и внешняя отправка могут раскрыть данные панели; проверить recipient/email/media и TLS ([p0271](../../../rag/chunks/p0201-p0300/p0271-c01.md)–[p0273](../../../rag/chunks/p0201-p0300/p0273-c01.md)).
- `Services → SLA/Create SLA` и `Services → Services/Create service`: **State-changing**, меняет оценку доступности, уровни важности, SLA и eligibility; проверка по Service tree и отчёту ([p0280](../../../rag/chunks/p0201-p0300/p0280-c01.md)–[p0289](../../../rag/chunks/p0201-p0300/p0289-c01.md)).

## Verification / acceptance checks

1. График использует правильный item/шкалу и имеет историю; LLD создаёт графики с корректным IFNAME.
2. Карта показывает host/link и ожидаемую реакцию на trigger, без неоднозначного host macro в link.
3. Обе категории dashboard открываются в правильном месте; template dashboard не оценивается по отсутствию данных на уровне template.
4. Existing hosts inventory переведены отдельно при необходимости; Geomap отображает ожидаемые точки.
5. При PDF получатель получил согласованное тестовое письмо; нет отключённой TLS-проверки без решения владельца безопасности.
6. SLA 99,9 % и правило frontend High+ проверены на согласованном сервисном сценарии; SLA report отражает ожидания.

## Rollback

Пошаговый rollback для удаления/восстановления карт, общего dashboard ownership, inventory mode, Chrome/web service, PDF recipients или SLA rules **не описан**. Для этих действий `[Needs confirmation]`. До изменений документировать начальные значения; не предполагать, что удалённые данные восстановятся.

**Расхождения исходника:** установка `apt install install ...`, обозначение `Weekly (Ежедневно)`, отключение TLS проверки и некоторые поля только на рисунках — в [source-findings.md](source-findings.md).
