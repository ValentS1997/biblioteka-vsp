# Mermaid — глава 21 «Собираем все вместе»

**Источник:** PDF 350–374, RAG `p0350:c01`–`p0374:c01`, strict `rag_only`. Схемы построены по тексту; не воспроизводят графические оригиналы рис. 21.1, 21.2.

## Последовательность внедрения

```mermaid
flowchart LR
 START["Prometheus + Node Exporter<br/>локальная инфраструктура"]
 EXPORT["Готовые exporters<br/>SNMP, JMX, Blackbox"]
 RED["Инструментировать приложения<br/>RED в общих библиотеках"]
 LABELS["Управлять labels/cardinality"]
 LOCAL["Самостоятельные Prometheus<br/>по зонам отказов"]
 START --> EXPORT --> RED --> LABELS --> LOCAL
```

PDF 350–353. Для Windows источником указан Windows Exporter. Порядок адаптируется под зрелость/масштаб организации.

## ЦОД и глобальная федерация

```mermaid
flowchart TD
 TARGET1["Цели ЦОД Dublin"]
 TARGET2["Цели ЦОД Berlin"]
 TARGET3["Цели ЦОД New York"]
 P1["Prometheus Dublin<br/>локальные alerts"]
 P2["Prometheus Berlin<br/>локальные alerts"]
 P3["Prometheus New York<br/>локальные alerts"]
 AGG["Recording rules: job:*<br/>агрегаты"]
 GLOBAL["Global Prometheus<br/>/federate match[]"]
 GRAF["Глобальные dashboards<br/>и запросы"]
 TARGET1 --> P1
 TARGET2 --> P2
 TARGET3 --> P3
 P1 --> AGG
 P2 --> AGG
 P3 --> AGG
 AGG --> GLOBAL --> GRAF
```

PDF 353–356. Логически `AGG` означает агрегаты **на каждом локальном сервере**, а не один общий сервер до federation. Цели/алерты остаются в своих областях отказа; глобальный сервер не собирает все сырые instance series.

## HA оповещений, federation и уникальные внешние метки

```mermaid
flowchart TD
 TARGET["Общие цели"]
 P1["Prometheus replica 1<br/>external region=dublin1"]
 P2["Prometheus replica 2<br/>external region=dublin2"]
 REL1["alert_relabel_configs:<br/>region=dublin"]
 REL2["alert_relabel_configs:<br/>region=dublin"]
 AM["Alertmanager cluster<br/>dedupe идентичных alerts"]
 PERSIST["remote_write / federation:<br/>уникальные source labels"]
 TARGET --> P1
 TARGET --> P2
 P1 --> REL1 --> AM
 P2 --> REL2 --> AM
 P1 --> PERSIST
 P2 --> PERSIST
```

PDF 364–367. Alert labels нормализуются **только** перед Alertmanager, не перед записью/федерацией.

## Метамониторинг и сквозная проверка уведомлений

```mermaid
flowchart TD
 LOCAL["Prometheus локальный"]
 META["Meta-Prometheus в ЦОД<br/>scrape остальных Prometheus"]
 GLOBAL["Global Prometheus A/B<br/>cross-monitoring"]
 AM["Alertmanager"]
 CHANNEL["Провайдер уведомлений"]
 DEAD["Dead-man switch<br/>нет heartbeat → тревога"]
 LOCAL --> META
 META --> GLOBAL
 GLOBAL --> META
 LOCAL --> AM --> CHANNEL --> DEAD
```

PDF 367–368. Периодические alerts проверяют всю цепочку, включая провайдера; реализация внешнего переключателя в главе не специфицирована.

## Диагностическая последовательность производительности

```mermaid
flowchart TD
 SLOW["Медленные dashboards / scrape"]
 SCRAPE["scrape_samples_scraped<br/>scrape_duration_seconds"]
 RULES["missed rules<br/>last_duration vs interval"]
 EXP["topk(count by(__name__))<br/>дорогой запрос"]
 FIX["Снизить кардинальность в источнике"]
 DROP["metric_relabel_configs drop<br/>экономит storage, не network"]
 HASH["hashmod 10% для диагностики<br/>modulus 4 для shards"]
 SLOW --> SCRAPE
 SLOW --> RULES
 SCRAPE --> EXP --> FIX
 FIX --> DROP
 DROP --> HASH
```

PDF 368–373. Эта последовательность — карта выбора, не безусловная команда применять drop или отключать 90% целей.

## Локальное хранилище / длительная история

```mermaid
flowchart LR
 SCR["Scrapes"]
 TSDB["Local TSDB<br/>retention time / size"]
 SNAP["Snapshot<br/>admin API"]
 WRITE["remote_write<br/>write_relabel_configs"]
 REMOTE["Long-term store"]
 READ["remote_read<br/>historical queries"]
 SCR --> TSDB
 TSDB --> SNAP
 TSDB --> WRITE --> REMOTE --> READ
```

PDF 356–359. Snapshot и delete admin API, remote-write endpoints и retention изменения — **state-changing/destructive**; не выполнять без подтверждённого плана восстановления.
