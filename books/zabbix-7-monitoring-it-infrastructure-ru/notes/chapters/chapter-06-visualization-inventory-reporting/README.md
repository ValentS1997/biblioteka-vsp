# Глава 6. Визуализация данных, инвентаризация и отчетность

**Книга:** «Zabbix 7: мониторинг ИТ-инфраструктуры», третье обновлённое русское издание (2025). Inventory `0020`, book ID `zabbix-7-monitoring-it-infrastructure-ru`.

## Provenance и границы

- Источник: **только принятый RAG**, `rag/acceptance.yaml: ACCEPTED`; прямого чтения PDF или внешних ссылок не было.
- **PDF 229–290 включительно**, адресуемые chunks `zabbix-7-monitoring-it-infrastructure-ru:p0229:c01` … `zabbix-7-monitoring-it-infrastructure-ru:p0290:c01`; [заголовок главы 6](../../../rag/chunks/p0201-p0300/p0229-c01.md), [начало главы 7](../../../rag/chunks/p0201-p0300/p0291-c01.md); [оглавление](../../../rag/chunks/p0001-p0100/p0005-c01.md).
- Source SHA-256: `07204d885d4bf4c6c2de7c71ae42a4e3ed4cea794169cbe07985552e63875a27`; RAG generation `6a5221f8e8a0f88b400905d7334879edff6f5451d9ab7f6e56bb203809018986`.
- Иллюстрации UI, формулы/координаты и значения полей, присутствующие только на рисунках 6.1–6.107, **не выделены отдельными мультимодальными объектами RAG**. Их точные значения = `RAG_MISS`, без восстановления по памяти модели.

## Карта девяти разделов

| Раздел книги | PDF-страницы | Ключевая задача |
|---|---:|---|
| Создание графиков для визуализации данных | 230–236 | Items, стандартные графики, прототипы графиков по LLD, `{#IFNAME}` |
| Создание карт сетей для визуализации инфраструктуры | 236–243 | `Monitoring → Maps`, элементы/связи, индикатор связи и trigger, подпись трафика |
| Создание информационных панелей | 243–254 | `Dashboards → All dashboards`, widgets Problems, Map, Graph, Item value, Top Hosts, Gauge, Pie chart |
| Шаблонизация панелей на уровне узла сети | 254–258 | Dashboard у шаблона, фактические данные отображаются при открытии host |
| Настройка инвентаризации в Zabbix | 259–261 | Global default и существующие hosts, `Populates host inventory` |
| Использование виджета Geomap | 261–265 | Host Inventory latitude/longitude, виджет, tile providers |
| Работа с отчетами в Zabbix | 265–270 | System information, Availability, Trigger top 100, Audit, Action log, Notifications |
| Настройка регулярных отчетов в формате PDF | 270–274 | Chrome + Zabbix web service, отчётные процессы, Scheduled reports, Email |
| Настройка улучшенного мониторинга услуг | 274–290 | Service tree, теговая привязка событий, SLA, условие «обе проверки недоступны», error budget |

## Основные концепции

**Графики и карты:** Zabbix собирает items в базу, а graph делает временной ряд читаемым. Graph prototype создаёт отдельный график для каждого интерфейса, обнаруженного LLD, используя `{#IFNAME}`; сырой счётчик трафика преобразуется в скорость: `(current − previous) / elapsed_seconds × 8` для бит/с ([p0234](../../../rag/chunks/p0201-p0300/p0234-c01.md)–[p0236](../../../rag/chunks/p0201-p0300/p0236-c01.md)). На карте можно соединять monitored host и vSwitch, добавлять labels и индикаторы по trigger; для **link между объектами** книга требует явного hostname, а не неоднозначного `{HOST.HOST}` ([p0239](../../../rag/chunks/p0201-p0300/p0239-c01.md)–[p0243](../../../rag/chunks/p0201-p0300/p0243-c01.md)).

**Глобальная и host dashboard:** первая объединяет выбранные группы, проблемы, графики и несколько hosts. Шаблонная панель конфигурируется в `Data collection → Templates → Dashboards`, но значения появляются при открытии `Monitoring → Hosts → Dashboards` конкретного host: **шаблон сам не хранит измерений** ([p0244](../../../rag/chunks/p0201-p0300/p0244-c01.md)–[p0258](../../../rag/chunks/p0201-p0300/p0258-c01.md)). В примере панели две страницы `Overview` и `Host data`; Gauge читает Available memory in %, Pie chart — CPU * time.

**Инвентаризация:** `Default host inventory mode = Automatic` меняет поведение **вновь создаваемых** hosts; существующие требуют индивидуального изменения или Mass update ([p0259](../../../rag/chunks/p0201-p0300/p0259-c01.md)–[p0260](../../../rag/chunks/p0201-p0300/p0260-c01.md)). Item `System name` связывается с полем `Populates host inventory`. Geomap читает именно inventory latitude/longitude; точные координаты из рисунков не доступны в текстовом RAG, значит `RAG_MISS` ([p0261](../../../rag/chunks/p0201-p0300/p0261-c01.md)–[p0264](../../../rag/chunks/p0201-p0300/p0264-c01.md)).

**Отчётность:** встроенные страницы позволяют наблюдать здоровье Zabbix, доступность trigger, частоту PROBLEM, аудит изменений, историю actions и уведомлений ([p0265](../../../rag/chunks/p0201-p0300/p0265-c01.md)–[p0270](../../../rag/chunks/p0201-p0300/p0270-c01.md)). Периодические PDF — отдельная цепочка: **Zabbix frontend/dashboard → Web service/Chrome → PDF → Email subscription**. Книга требует `Frontend URL`, `WebServiceURL`, `StartReportWriters` и email media подписчика ([p0270](../../../rag/chunks/p0201-p0300/p0270-c01.md)–[p0274](../../../rag/chunks/p0201-p0300/p0274-c01.md)). Пример команд/SSL содержит замечания, требующие подтверждения, см. [source-findings.md](source-findings.md).

**Бизнес-услуги / SLA:** пример моделирует Zabbix setup как дерево из Zabbix server, DB и frontend; frontend зависит от двух дочерних проверок — ICMP и Zabbix agent. Для frontend дополнительное правило **`If at least 2 child services have High status or above`**, при базовом `Set status to OK`: нарушение засчитывается, если **обе** дочерние проверки проблемны ([p0286](../../../rag/chunks/p0201-p0300/p0286-c01.md)–[p0288](../../../rag/chunks/p0201-p0300/p0288-c01.md)). Через `Services → SLA report` смотрят SLO **99,9 %**, фактический SLA и оставшийся error budget ([p0288](../../../rag/chunks/p0201-p0300/p0288-c01.md)–[p0289](../../../rag/chunks/p0201-p0300/p0289-c01.md)); пример результатов относится к **октябрю–ноябрю 2021**, не текущим измерениям.

## Практический порядок

1. Проверить исходные items, SNMP host и Custom Linux by SNMP из главы 5. Создать график и LLD graph prototype; контролировать правильные единицы и историю.
2. Создать карту, сопоставить два map elements с конкретным host и привязать link indicator по триггеру; убедиться, что имя host совпадает.
3. Создать общую dashboard из Problems/Map/Graph/Item value/Top Hosts, при необходимости страниц Gauge/Pie chart. Проверить фильтр и владельца/share.
4. Добавить dashboard к template и открыть её на конкретном host, не ожидая данных в редакторе шаблона.
5. Настроить inventory mode для новых и **отдельно** существующих hosts, связать item с inventory field и проверить `Inventory → Hosts`.
6. Для Geomap заполнить latitude/longitude в inventory обоих hosts, добавить Geomap widget и при необходимости выбрать tile provider.
7. Использовать встроенные `Reports` для анализа проблем и действий; для scheduled PDF создать web-service контур лишь после проверки TLS, пакетов, URL и email.
8. Построить бизнес-сервис, сопоставить problem tags и дерево, настроить SLA и дополнительное правило, затем проверить `Services → SLA report` и error budget.

## Публикуемые артефакты

[Cheatsheet](cheatsheet.md) · [Команды и UI](commands.md) · [Mermaid](diagram.md) · [Компактная SVG](visual-cheatsheet.svg) · [Подробная SVG](visual-cheatsheet-detailed.svg) · [Source findings](source-findings.md).

**Границы:** полный rollback установки Chrome/Zabbix web service, глобальных настроек inventory, рассылок и SLA-дерева в главе отсутствует: `[Needs confirmation]`. Отдельных итоговых упражнений или review questions на [p0290](../../../rag/chunks/p0201-p0300/p0290-c01.md) нет; условные `summary.md`, `review-questions.md`, `review-answers.md` не создаются. **Статус чтения не изменяется.**

Контракты: `chapter-analysis-request v1.4`, `chapter-artifact-collection v1.8`, `chapter-publication v1.0`, `session-recovery v1.0`.
