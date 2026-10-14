# Mermaid — глава 18 «Оповещение»

**Источник:** PDF 307–320, RAG `p0307:c01`–`p0320:c01`; `rag_only`. Схемы составлены по тексту, а не перерисованы с недоступных в RAG оригинальных рисунков 18.1 и 18.2.

## Архитектура: alert ≠ notification

```mermaid
flowchart LR
 S["Prometheus: scrape и PromQL"]
 R["Alerting rules: expr, labels, for"]
 A["Firing alerts"]
 AM["Alertmanager: grouping, routing"]
 N["Уведомления: email, PagerDuty, chat"]
 S --> R --> A --> AM --> N
```

PDF 307–309. Несколько Prometheus могут отправлять alerts в один Alertmanager. Разделение ответственной логики: Prometheus генерирует alert, Alertmanager отправляет notification.

## Жизненный цикл правила

```mermaid
flowchart TD
 E["expr возвращает instant-vector"]
 Q{"Есть sample с теми же labels?"}
 NONE["Пусто: alert не создаётся / resolved"]
 P["pending: for ещё не истёк"]
 F["firing: for выполнен"]
 SEND["Alertmanager"]
 RESET["Sample исчез/изменились labels: for сброшен"]
 E --> Q
 Q -->|"нет"| NONE
 Q -->|"да"| P
 P -->|"сохранился for"| F --> SEND
 P -->|"исчез"| RESET --> NONE
 F -->|"условие исчезло"| NONE
```

PDF 308–313. Идентичность alert определяется labels, включая alertname. Изменяющееся `$value` нельзя помещать в label. Prometheus `ALERTS` содержит `alertstate=pending/firing`, `ALERTS_FOR_STATE` хранит начало.

## Stable labels vs dynamic annotations

```mermaid
flowchart LR
 EXPR["expr: up ratio"]
 LABEL["labels: severity, team"]
 IDENT["Stable alert identity"]
 ANN["annotations: $value, $labels, query"]
 INFO["Описание, dashboard, runbook"]
 EXPR --> LABEL --> IDENT
 EXPR --> ANN --> INFO
```

PDF 312–317. `query` в аннотации может создавать дополнительную нагрузку.

## Порядок внешних меток и маршрутизации

```mermaid
flowchart LR
 RULE["Prometheus alert rule<br/>rule evaluation"]
 EXT["external_labels<br/>если не заняты"]
 REL["alert_relabel_configs<br/>drop/keep"]
 AM["Alertmanager<br/>routes / notifications"]
 RULE --> EXT --> REL --> AM
```

PDF 318–320. Внешние метки недоступны Prometheus annotation templates, но могут использоваться в Alertmanager. Не утверждать, что downstream-политики Alertmanager здесь полностью описаны.

## Критерий полезного alert

```mermaid
flowchart TD
 A["Сигнал требует реакции человека?"]
 YES["Да: симптом для пользователя,<br/>ресурсный риск, мониторинг"]
 NO["Нет: уточнить порог или<br/>автоматизировать реакцию"]
 OWNER["Владелец + устойчивый for"]
 A -->|"да"| YES --> OWNER
 A -->|"нет"| NO
```

PDF 314, 317–318. Рекомендации про 5-минутный `for` и число инцидентов — практический опыт авторов, не автоматические стандарты.
