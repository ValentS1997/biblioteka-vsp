# Глава 6 — команды, UI-действия и эффекты

**RAG-only:** PDF 229–290, [provenance](README.md). Большинство рецептов — GUI. Никаких непроверенных URL, IP, секретов или команд отката не добавляется. **Read-only** — чтение, **Workload-generating** — сетевые вызовы/рендер/отправка, **State-changing** — запись настроек/сервисов.

## 1. Графики, прототипы и карты

| UI/CLI из источника | Класс | Эффект, риск и проверка |
|---|---|---|
| `Data collection → Templates → Custom Linux by SNMP → Items` | Read-only при просмотре; State-changing при Create item | Элемент ICMP и его теги; конкретный key из рис. 6.1 = `RAG_MISS`; [p0230](../../../rag/chunks/p0201-p0300/p0230-c01.md)–[p0231](../../../rag/chunks/p0201-p0300/p0231-c01.md) |
| `Templates → Graphs → Create graph` | State-changing | Добавить обычный график (книга сначала называет Uptime, позднее `Incoming ICMP messages` — фиксируется в findings), проверить `Monitoring → Hosts → Graphs`; [p0231](../../../rag/chunks/p0201-p0300/p0231-c01.md)–[p0232](../../../rag/chunks/p0201-p0300/p0232-c01.md) |
| `ping <TEST_SNMP_HOST>` | Workload-generating | ICMP к согласованному host, создаёт трафик и значение счётчика; учебный IP `10.16.16.153` не переносить; [p0232](../../../rag/chunks/p0201-p0300/p0232-c01.md) |
| `Templates → Discovery rules → Item prototypes → Create item prototype` | State-changing | Новая метрика интерфейса, preprocessing `(current - previous) / time_delta * 8` для бит/с; влияние на данные/хранение, [p0233](../../../rag/chunks/p0201-p0300/p0233-c01.md)–[p0234](../../../rag/chunks/p0201-p0300/p0234-c01.md) |
| `Discovery rules → Graph prototypes → Create graph prototype` | State-changing | График для каждого interface; `{#IFNAME}` формирует уникальное имя; [p0234](../../../rag/chunks/p0201-p0300/p0234-c01.md)–[p0236](../../../rag/chunks/p0201-p0300/p0236-c01.md) |
| `Monitoring → Maps → All maps → Create map → Edit map` | State-changing | Карта `Templated SNMP host map`, два элемента host/vSwitch, link; в тексте координаты X400/Y100 и X150/Y80 — это позиции на холсте, **не географические координаты**; [p0238](../../../rag/chunks/p0201-p0300/p0238-c01.md)–[p0241](../../../rag/chunks/p0201-p0300/p0241-c01.md) |
| `Edit link → Link indicators → Add → Apply/Update` | State-changing | Индикатор связи по trigger, label с показателями; точное имя host обязательно, macro `{HOST.HOST}` в link неоднозначен; [p0241](../../../rag/chunks/p0201-p0300/p0241-c01.md)–[p0243](../../../rag/chunks/p0201-p0300/p0243-c01.md) |

Форма конкретных preprocessing-expression и дополнительных label-полей доступна только на рисунках → `RAG_MISS`; их нельзя заменять кодом из другой версии Zabbix.

## 2. Общие и шаблонные панели

| UI | Класс | Последствия и контроль |
|---|---|---|
| `Dashboards → All dashboards → Create dashboard` | State-changing | Общая dashboard для Linux; владельца/Share проверить прежде изменения, иначе возможна потеря собственного доступа; [p0244](../../../rag/chunks/p0201-p0300/p0244-c01.md) |
| `Add widget → Problems/Map/Graph/Item value/Top Hosts` | State-changing | Фильтры problems severity Warning+, Linux servers, dataset выбранных элементов; проверка — отображаемые host/значения; [p0245](../../../rag/chunks/p0201-p0300/p0245-c01.md)–[p0251](../../../rag/chunks/p0201-p0300/p0251-c01.md) |
| `Add page → Host data`, `Gauge`, `Pie chart`, `Save changes` | State-changing | Gauge: `Zabbix server → Available memory in %`; Pie chart `CPU timings`, host `Zabbix server`, item pattern `CPU * time`, legend rows 3; [p0252](../../../rag/chunks/p0201-p0300/p0252-c01.md)–[p0254](../../../rag/chunks/p0201-p0300/p0254-c01.md) |
| `Templates → Custom Linux by SNMP → Dashboards → Create dashboard` | State-changing | Шаблон `Host overview`, widgets Item value/Graph/Problems; **данные не появляются на template**, проверка — `Monitoring → Hosts → Dashboards`; [p0255](../../../rag/chunks/p0201-p0300/p0255-c01.md)–[p0258](../../../rag/chunks/p0201-p0300/p0258-c01.md) |

Рекомендация авторов: отключить `Start slideshow automatically` на PC при troubleshooting; NOC-monitor может использовать slideshow ([p0244](../../../rag/chunks/p0201-p0300/p0244-c01.md), [p0255](../../../rag/chunks/p0201-p0300/p0255-c01.md)). В книгах конфигурация владельца Zabbix Administrator описана как удобная для коллективных панелей, но это меняет управление доступом; rollback процедуры нет: `[Needs confirmation]`.

## 3. Inventory и Geomap

- `Administration → General → Other → Default host inventory mode → Automatic → Update`: **State-changing**, только **новые** хосты; существующие через `Data collection → Hosts → Inventory` или Mass update (**State-changing**). Проверить `Inventory → Hosts` ([p0259](../../../rag/chunks/p0201-p0300/p0259-c01.md)–[p0260](../../../rag/chunks/p0201-p0300/p0260-c01.md)).
- `Templates → Items → System name → Populates host inventory`: **State-changing**, item автоматически заполняет выбранное поле inventory; конкретный dropdown из рис. 6.57 = `RAG_MISS` ([p0260](../../../rag/chunks/p0201-p0300/p0260-c01.md)).
- `Hosts → Inventory → Location latitude / Location longitude` для двух узлов: **State-changing**, реальные координаты могут раскрывать точное местонахождение системы. В рисунках 6.60–6.61 значения отсутствуют в текстовом RAG → `RAG_MISS`. Проверка `Dashboard → Geomap` ([p0261](../../../rag/chunks/p0201-p0300/p0261-c01.md)–[p0263](../../../rag/chunks/p0201-p0300/p0263-c01.md)).
- `Administration → General → Geographical maps → Tile provider / Other`: **State-changing**, возможны сетевые запросы внешнему tile provider, подробности/security-policy `[Needs confirmation]` ([p0264](../../../rag/chunks/p0201-p0300/p0264-c01.md)–[p0265](../../../rag/chunks/p0201-p0300/p0265-c01.md)).

## 4. Встроенные отчёты — преимущественно Read-only

`Reports → System information` — версии, supported/unsupported items, NVPS, HA; `Availability report` — PROBLEM/OK % за период; `Trigger top 100` — частота срабатываний; `Audit` — изменения; `Action log` — результаты и `Info` ошибок; `Notifications` — количество сообщений по пользователям. Все **Read-only** при просмотре, могут инициировать запросы к серверу и влиять на нагрузку. Скриншотные числа (например, 16 enabled hosts, 565 enabled items) относятся к примеру книги, **не к текущему Zabbix** ([p0265](../../../rag/chunks/p0201-p0300/p0265-c01.md)–[p0270](../../../rag/chunks/p0201-p0300/p0270-c01.md)).

## 5. Scheduled PDF — команды источника, не готовый production-рецепт

**Шаги для RHEL** ([p0271](../../../rag/chunks/p0201-p0300/p0271-c01.md)):
```sh
# State-changing: создать конфиг стороннего репозитория, затем установить Chrome.
vim /etc/yum.repos.d/google-chrome.repo
dnf install -y google-chrome-stable
dnf install zabbix-web-service
```

Авторский репозиторий Chrome содержит `baseurl=http://dl.google.com/linux/chrome/rpm/stable/$basearch`, `gpgcheck=1`, `gpgkey=https://dl-ssl.google.com/linux/linux_signing_key.pub`. **Не исполнять без проверки репозитория/подписей/актуальности**. Книга не содержит верифицированного rollback пакетов.

**Для Ubuntu** p271 предлагает конвейер `wget -q -O - https://dl-ssl.google.com/linux/linux_signing_key.pub | sudo apt-key add -`, добавление `deb http://dl.google.com/linux/chrome/deb/stable main`, `sudo apt update`, `sudo apt-get install google-chrome-stable`. Все установки **State-changing**, вывод ключа и `apt-key` как источниковая форма, *не рекомендовать вслепую*. Далее книга буквально пишет `apt install install zabbix-web-service`: **[Source code mismatch]**, не выдавать за проверенную исполняемую команду. [source-findings.md](source-findings.md).

**Изменение конфигураций** ([p0271](../../../rag/chunks/p0201-p0300/p0271-c01.md)–[p0272](../../../rag/chunks/p0201-p0300/p0272-c01.md)):
```ini
# /etc/zabbix/zabbix_web_service.conf — пример с локальными адресами
AllowedIP=127.0.0.1,::1

# /etc/zabbix/zabbix_server.conf — авторский пример
WebServiceURL=https://localhost:10053/report
StartReportWriters=3
```

Редактирование `vim /etc/zabbix/zabbix_web_service.conf`, `vim /etc/zabbix/zabbix_server.conf` и смена переменных — **State-changing**, может повлиять на Zabbix server и отчётный контур. В книге **нет подтверждённой команды запуска/enable/restart zabbix-web-service** в данном рецепте. HTTPS и локальные порты — строки источника, работоспособность в конкретной среде `[Needs confirmation]`.

**TLS:** авторы рекомендуют SSL на frontend (например, Let's Encrypt) и как альтернативу приводят `IgnoreURLCertErrors=1` в `/etc/zabbix/zabbix_web_service.conf`. Это **State-changing / security-sensitive**, выключает проверку ошибок URL-сертификата; как production workaround не рекомендовать ([p0272](../../../rag/chunks/p0201-p0300/p0272-c01.md)). Точные host URL, сертификаты и безопасная настройка: `[Needs confirmation]`.

**GUI:** `Administration → General → Other → Frontend URL` (**State-changing**) → `Reports → Scheduled reports → Create report` → выбрать `Global view`, Cycle `Weekly`, Monday 09:00, Subject/Message/Subscriptions с email media → `Test` (**Workload-generating**, рендер и потенциальная отправка) → `Add` (**State-changing**, активирует рассылку) ([p0272](../../../rag/chunks/p0201-p0300/p0272-c01.md)–[p0273](../../../rag/chunks/p0201-p0300/p0273-c01.md)). Исходник переводит Weekly как «Ежедневно» — сохранить расхождение в findings. Rollback scheduled report/subscription `[Needs confirmation]`.

## 6. Business service + SLA

`Data collection → Templates/Hosts/Items/Triggers` — создать template `Zabbix frontend by Zabbix agent`, host `lar-book-zabbix-frontend`, ICMP/agent items, value mapping и триггеры с тегами SLA (**State-changing**, изменение мониторинга) ([p0275](../../../rag/chunks/p0201-p0300/p0275-c01.md)–[p0280](../../../rag/chunks/p0201-p0300/p0280-c01.md)).

`Services → SLA → Create SLA` → `Services → Services → Create service`: **State-changing**; дерево `Zabbix setup` → server, DB, frontend → ICMP/agent. Для frontend авторы устанавливают базовое `Set status to OK` и Additional rule **`If at least 2 child services have High status or above`**, т.е. две проверки должны быть проблемными ([p0280](../../../rag/chunks/p0201-p0300/p0280-c01.md)–[p0288](../../../rag/chunks/p0201-p0300/p0288-c01.md)). Точные поля services/tags/screenshots = `RAG_MISS`; нельзя реконструировать settings из рисунков.

`Services → SLA report` — **Read-only**, проверка 99,9 % за месяц, downtime/uptime и error budget ([p0288](../../../rag/chunks/p0201-p0300/p0288-c01.md)–[p0289](../../../rag/chunks/p0201-p0300/p0289-c01.md)). Источниковый результат 100 % за октябрь 2021 — **история примера**, не результат вашей инфраструктуры.

**Итог:** графики, inventory, dashboard, PDF и SLA привязаны к одному набранному контексту, но каждое изменение имеет отдельный радиус действия. Все отсутствующие поля, TLS policy, rollback и подтверждение внешних пакетов = `[Needs confirmation]`.
