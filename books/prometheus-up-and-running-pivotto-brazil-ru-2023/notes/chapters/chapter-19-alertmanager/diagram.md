# Mermaid — глава 19 «Alertmanager»

**Источник:** PDF 321–343, RAG `p0321:c01`–`p0343:c01`, strict `rag_only`. Новые схемы из текста; рисунки 19.1–19.5 напрямую не воспроизведены.

## Конвейер и развилка маршрутизации

```mermaid
flowchart TD
 IN["Alerts от Prometheus"]
 SUP["Inhibition: source/target/equal"]
 SIL["Silences: UI, время и labels"]
 ROUTE["Routing tree: matcher, first match"]
 GR["Grouping: group_by"]
 WAIT["group_wait / group_interval / repeat_interval"]
 REC["Receiver: email / pager / chat / webhook"]
 IN --> SUP --> SIL --> ROUTE --> GR --> WAIT --> REC
```

PDF 321–322. Схема концептуальная: подавление и Silences препятствуют отправке уведомлений, не удаляют инцидент и не доказывают, что исходный alert исчез.

## Дерево выбора получателя и continue

```mermaid
flowchart TD
 ROOT["Fallback route: fallback-pager"]
 PAGE{"severity=page?"}
 TICKET{"severity =~ ticket|issue|email?"}
 PAGER["team-pager"]
 TICK["team-ticket"]
 FALL["fallback-pager"]
 CONT["continue:true → проверить следующие sibling routes"]
 ROOT --> PAGE
 PAGE -->|"да"| PAGER
 PAGE -->|"нет"| TICKET
 TICKET -->|"да"| TICK
 TICKET -->|"нет"| FALL
 ROOT --> CONT
```

PDF 323–326. `continue` меняет только остановку поиска; другие route options наследуются от родителей.

## Отложенная отправка и повторы

```mermaid
flowchart LR
 A["Первые alerts группы"]
 GW["group_wait 30s"]
 N1["Первое notification"]
 GI["group_interval 5m"]
 N2["Новое notification<br/>при изменении группы"]
 REP["repeat_interval 4h"]
 N3["Повтор при ongoing incident"]
 A --> GW --> N1 --> GI --> N2
 N1 --> REP --> N3
```

PDF 328–330. Интервалы — source defaults конкретного издания. Последующие изменения и повторные отправки не обязаны происходить при каждом тике без соответствующих условий.

## Шаблон уведомления как group data

```mermaid
flowchart TD
 GROUP["Сгруппированные alerts"]
 LABEL["GroupLabels / CommonLabels"]
 ALERTS["Alerts: Labels, Annotations, Status"]
 FORMAT["Go templates: len, range, SortedPairs"]
 OUT["Receiver: человекочитаемое сообщение"]
 GROUP --> LABEL --> FORMAT --> OUT
 GROUP --> ALERTS --> FORMAT
```

PDF 333–337. Webhook получает JSON и не проходит через тот же template formatter (PDF 333).

## Inhibition против Silence

```mermaid
flowchart TD
 ACTIVE["Активны page-regionfail и page в region"]
 MATCH["source_matchers, target_matchers, equal=region"]
 INHIB["page подавлен для отправки"]
 MAINT["Плановое обслуживание"]
 UI["Silence по labels и времени, комментарий"]
 MUTED["Выбранные уведомления отключены временно"]
 ACTIVE --> MATCH --> INHIB
 MAINT --> UI --> MUTED
```

PDF 340–343. Настройка любого механизма **state-changing**, а чрезмерный охват способен скрыть важные инциденты.
