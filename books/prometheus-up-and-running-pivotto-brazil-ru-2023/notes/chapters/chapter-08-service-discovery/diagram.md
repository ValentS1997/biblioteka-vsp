# Глава 8 — схемы Service Discovery (Mermaid)

**Источник:** PDF 144–169 (`p0144:c01`–`p0169:c01`), только canonical RAG. Mermaid-схемы передают логику книги, не изображения рис. 8.1–8.4.

## Цель: от данных SD к успешному scrape

```mermaid
flowchart LR
 A["SD: static / file / HTTP / Consul / EC2"]
 B["Discovered targets + __meta_*"]
 C["relabel_configs<br/>keep, drop, replace, labelmap"]
 D["Итоговые target labels<br/>job, instance, __address__"]
 E["Scrape: scheme, path, params,<br/>timeout, TLS/auth"]
 F["Metric samples из /metrics"]
 G["metric_relabel_configs<br/>до хранения"]
 H["Prometheus TSDB"]
 A --> B --> C --> D --> E --> F --> G --> H
```

PDF 144–169. Обнаружение списка целей, отбор/изменение target labels и изменение полученных метрик — отдельные стадии. Сгенерированная метрика `up` не проходит `metric_relabel_configs` (PDF 168).

## Выбор источника и его риски

```mermaid
flowchart TD
 A["Источник сведений о целях"]
 B["Небольшой устойчивый набор"]
 C["Static targets"]
 D["Локальный сгенерированный список"]
 E["File SD<br/>JSON/YAML, атомарный rename"]
 F["Удалённая CMDB с JSON endpoint"]
 G["HTTP SD<br/>HTTP 200 + application/json"]
 H["Реестр или облако"]
 I["Consul / EC2 и __meta_*"]
 J["Согласованные target labels,<br/>индивидуальный scrape каждого экземпляра"]
 A --> B --> C --> J
 A --> D --> E --> J
 A --> F --> G --> J
 A --> H --> I --> J
```

PDF 144–153, 156. Для HTTP SD при недоступности сразу после рестарта список целей может быть пуст. Для файла избегать частичного обновления.

## Чем опасен двойной keep

```mermaid
flowchart TD
 A["file SD targets:<br/>team=infra и team=monitoring"]
 B["keep team == infra"]
 C["Остались только infra"]
 D["keep team == monitoring"]
 E["Ни одной цели"]
 F["Одна проверка alternatives:<br/>regex infra|monitoring"]
 G["Обе группы остаются"]
 A --> B --> C --> D --> E
 A --> F --> G
```

PDF 154–155. Правила relabel идут последовательно, альтернативы в одном regex не равны двум `keep`.

## Диагностическая последовательность

```mermaid
flowchart TD
 A["Baseline: /service-discovery<br/>цели и метаданные"]
 B["Локализация: источник SD,<br/>ошибки HTTP, path/port"]
 C["Анализ: keep/drop, job, instance,<br/>__address__, honor_labels"]
 D["Контролируемое изменение<br/>с заранее известным эффектом"]
 E["Проверка: ожидаемые targets,<br/>scrape и ряды"]
 F["Неверный результат?<br/>rollback [Needs confirmation]"]
 A --> B --> C --> D --> E --> F
```

PDF 148–169. Конкретные команды применения/rollback и инфраструктура пользователя не описаны в книге, поэтому схема не утверждает процедур, которых RAG не содержит.
