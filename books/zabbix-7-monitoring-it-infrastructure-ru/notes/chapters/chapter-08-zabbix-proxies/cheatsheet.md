# Глава 8 — operational cheatsheet

**Источник:** accepted RAG PDF 336–370; подробности provenance в [README](README.md).

## Симптом → интерпретация → следующий шаг

| Симптом | Что проверить | RAG |
|---|---|---|
| `Last seen (age) = Never` или продолжает расти | `ProxyMode` совпадает с UI; имя, Server, firewall TCP/10051, Encryption/PSK, ошибки в журнале, интервалы reconnect | [p0341](../../../rag/chunks/p0301-p0400/p0341-c01.md)–[p0347](../../../rag/chunks/p0301-p0400/p0347-c01.md), [p0354](../../../rag/chunks/p0301-p0400/p0354-c01.md) |
| Данные host временно перестали приходить после смены `Monitored by` | Переназначен ли host на нужный proxy; время обновления конфигурации; корректный `ServerActive` на active Agent 2 | [p0348](../../../rag/chunks/p0301-p0400/p0348-c01.md)–[p0350](../../../rag/chunks/p0301-p0400/p0350-c01.md) |
| Нет данных после отключения связи site→server | `ProxyOfflineBuffer`, disk/memory buffer mode, реальный срок офлайн, свободное место, рестарты | [p0340](../../../rag/chunks/p0301-p0400/p0340-c01.md), [p0352](../../../rag/chunks/p0301-p0400/p0352-c01.md) |
| После PSK proxy offline | Совпадают ли identity и PSK на обеих сторонах, корректны ли `TLSConnect/TLSAccept`, перезапущен ли нужный сервис; не раскрывать ключ в логах | [p0353](../../../rag/chunks/p0301-p0400/p0353-c01.md)–[p0354](../../../rag/chunks/p0301-p0400/p0354-c01.md) |
| Failover не срабатывает или группа недоступна | Proxy group membership, `Minimum number of proxies`, `Failover period`, адреса active agents, capacity оставшихся экземпляров | [p0356](../../../rag/chunks/p0301-p0400/p0356-c01.md)–[p0360](../../../rag/chunks/p0301-p0400/p0360-c01.md) |
| После переноса Discovery появились дубли/пропали hosts | `Discovery by → Proxy`, host classification, источники данных и **отказаться от учебного удаления hosts без backup** | [p0361](../../../rag/chunks/p0301-p0400/p0361-c01.md)–[p0363](../../../rag/chunks/p0301-p0400/p0363-c01.md) |
| Proxy жив, но в очереди много значений старше 5–10 минут | `Administration → Queue → Queue overview by proxy`; задержки, сбор/предобработка/хранение, нагрузка | [p0368](../../../rag/chunks/p0301-p0400/p0368-c01.md)–[p0370](../../../rag/chunks/p0301-p0400/p0370-c01.md) |

## Baseline и ограничения

Нужны Zabbix server, отдельные Linux hosts `lar-book-proxy-passive` и `lar-book-proxy-active`, тестовые Zabbix Agent 2/SNMP hosts и рабочие учетные данные. Учебный SQL-файл `/tmp/zabbix_proxy.sqlite3` **нельзя считать безопасным production размещением без решения по постоянному хранению**: глава не подтверждает retention/permissions этого пути ([p0337](../../../rag/chunks/p0301-p0400/p0337-c01.md)–[p0340](../../../rag/chunks/p0301-p0400/p0340-c01.md)). Пользователь должен определять реальные IP, именование, firewall и repo версии самостоятельно.

## Read-only checks

- `Administration → Proxies`: имя, режим, группа, Last seen(age), вкладки Encryption/Timeouts — **Read-only при просмотре**, [p0341](../../../rag/chunks/p0301-p0400/p0341-c01.md)–[p0347](../../../rag/chunks/p0301-p0400/p0347-c01.md).
- `tail -f /var/log/zabbix/zabbix_proxy.log`: **Read-only** с постоянным чтением журнала; проверять ошибки старта, синхронизации, а не показывать секреты, [p0339](../../../rag/chunks/p0301-p0400/p0339-c01.md).
- `Data collection → Hosts`: `Monitored by`, linked host/proxy/group; `Monitoring → Latest data`: свежесть values, proxy health; [p0348](../../../rag/chunks/p0301-p0400/p0348-c01.md)–[p0350](../../../rag/chunks/p0301-p0400/p0350-c01.md), [p0365](../../../rag/chunks/p0301-p0400/p0365-c01.md)–[p0368](../../../rag/chunks/p0301-p0400/p0368-c01.md).
- `Administration → Queue → Queue overview by proxy`: категории 5 s, 10 s, 30 s, 1 min, 5 min, over 10 min. Частые 5+ минуты требуют диагностики и не объявляются равными любому outage ([p0370](../../../rag/chunks/p0301-p0400/p0370-c01.md)).
- Локально/удаленно health: проверить cached values, обработанные значения и queue; remote `Remote Zabbix proxy health` выполняет проверку **со стороны сервера** и требует `StatsAllowedIP` ([p0366](../../../rag/chunks/p0301-p0400/p0366-c01.md)–[p0369](../../../rag/chunks/p0301-p0400/p0369-c01.md)).

## Интерпретация

- **ProxyMode=1 — passive**, server инициирует TCP-соединение; **ProxyMode=0 — active**, proxy инициирует. Оба сценария описаны на **10051** ([p0343](../../../rag/chunks/p0301-p0400/p0343-c01.md), [p0347](../../../rag/chunks/p0301-p0400/p0347-c01.md)).
- **Hybrid/default** новые установки: память и fallback на диск; **memory only** после restart может потерять данные; **disk mode** для существующих установок по книге. Удаление SQLite БД уничтожает неопубликованные значения ([p0339](../../../rag/chunks/p0301-p0400/p0339-c01.md)–[p0340](../../../rag/chunks/p0301-p0400/p0340-c01.md)).
- **ProxyOfflineBuffer**: книга приводит **1 час по умолчанию**, но это ограниченное окно, не бессрочная сохранность при обрыве site-link ([p0352](../../../rag/chunks/p0301-p0400/p0352-c01.md)).
- **PSK** хранит секрет в отдельном файле; identity + PSK должны совпасть в Zabbix server/proxy UI и config. Книга разрешает `No encryption` **только в начальной демонстрации**, позднее подчёркивает риск передачи важных макросов в plaintext ([p0342](../../../rag/chunks/p0301-p0400/p0342-c01.md), [p0352](../../../rag/chunks/p0301-p0400/p0352-c01.md)–[p0355](../../../rag/chunks/p0301-p0400/p0355-c01.md)).
- **Group failover** зависит от количества готовых proxy и capacity. Если 4 proxy, `Minimum number=1`, каждый может оказаться единственным обработчиком нагрузки; `Minimum number=3` делает группу недоступной при потере 2 ([p0359](../../../rag/chunks/p0301-p0400/p0359-c01.md)).
- **Proxy self-monitoring**: локальное через агент и `Monitored by proxy` обеспечивает оценку ОС и proxy в контуре самого proxy; remote health с сервера остаётся наблюдаемым, если proxy локально неисправен. Эти контуры дополняют друг друга ([p0364](../../../rag/chunks/p0301-p0400/p0364-c01.md)–[p0369](../../../rag/chunks/p0301-p0400/p0369-c01.md)).

## Modifying action

1. `dnf/apt install zabbix-proxy-sqlite3`, `systemctl enable/start zabbix-proxy`: **State-changing**, затрагивает службу/сетевые соединения. Проверка журналов и Last seen; подтверждённого универсального rollback нет `[Needs confirmation]`.
2. `ProxyMode`, `Server`, `Hostname`, `DBName`, `ProxyBufferMode` в `/etc/zabbix/zabbix_proxy.conf`: **State-changing**; риск остановки сбора/потери значений. Сделать копию конфигурации локальным согласованным способом, проверить связь после обслуживания.
3. **Не исполнять** учебное `rm /tmp/zabbix_proxy.sqlite3` как обычную диагностику: **Destructive**, могут пропасть значения до отправки серверу ([p0339](../../../rag/chunks/p0301-p0400/p0339-c01.md)–[p0340](../../../rag/chunks/p0301-p0400/p0340-c01.md)).
4. PSK: `openssl rand -hex 128 > /etc/zabbix/proxy_psk.key` — **State-changing**, создаёт секрет; не выводить содержимое через `cat`. `chmod 400/etc/...` и `Systemctl...` исходного текста ошибочны. Подлинные права, владелец, lifecycle/rotation и cutover = `[Needs confirmation]`.
5. `Administration → Proxy groups` / `Proxy group` на proxy / `Monitored by` на host: **State-changing**, распределяет нагрузку, может вызвать недоступность мониторинга. Критерий — очередь, Last seen, фактические значения.
6. `Data collection → Discovery` → `Discovery by → Proxy`, изменение Agent `Server/ServerActive`: **State-changing**, может вызвать дубли/провал регистрации; учебная команда удаления существующих hosts **destructive**, отдельно блокировать в production.
7. `StatsAllowedIP` и templates local/remote: **State-changing**, меняет доступ к метрикам; не открывать статистику более широкому диапазону без политики безопасности.

## Verification / acceptance

- В журнале нет ошибок старта/PSK/config; Last seen(age) показывают достижимость и обновляются.
- За каждым тестовым host закреплён правильный proxy/группа; active Agent 2 отправляет на нужный адрес, Latest data обновляется.
- При согласованном тесте сбоя проверены ограничения buffering, не уничтожены ещё не переданные данные; права доступа к БД/PSK подтверждены.
- Proxy group выдерживает согласованный failover, численность и мощность отдельных узлов отвечают выбранному threshold.
- После Discovery/Autoregistration созданы ожидаемые хосты, **без удаления существующих данных**.
- Local и remote proxy health доступны, queue by proxy не накапливает долговременных задержек.

## Rollback / source limits

Книга **не содержит** готового безопасного rollback утраченных значений SQLite/memory, механизма восстановления удалённых hosts и полного PSK rotation без downtime. Для них `[Needs confirmation]`. `RAG_MISS`: fields только на рисунках 8.2–8.41. Расхождения: [source-findings.md](source-findings.md).
