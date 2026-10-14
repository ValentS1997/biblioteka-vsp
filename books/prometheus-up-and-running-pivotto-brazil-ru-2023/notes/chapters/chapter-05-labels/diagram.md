# Глава 5 — RAG-grounded Mermaid

**Источник:** PDF 97–111 (`p0097:c01`–`p0111:c01`). Диаграммы построены по тексту главы.

## Имя, метки и временные ряды

```mermaid
flowchart TD
  FAMILY["Семейство: http_requests_total"]
  NAME["Имя метрики"]
  LABELS["Метки: path, method; неупорядоченный набор"]
  TARGET["Целевые метки: job, instance"]
  A["Ряд: path=/foo, method=GET"]
  B["Ряд: path=/foo, method=POST"]
  C["Ряд: path=/bar, method=GET"]
  FAMILY --> NAME
  FAMILY --> LABELS
  LABELS --> A
  LABELS --> B
  LABELS --> C
  TARGET --> A
  TARGET --> B
  TARGET --> C
```

PDF 97–101. В источнике метрики с метками создаются через `labelnames` + `labels`, целевые метки назначаются Prometheus при сборе (PDF 98–100).

## Агрегирование

```mermaid
flowchart LR
  R["rate(hello_worlds_total[5m])<br/>по instance, path, method"]
  P["sum without(path)<br/>оставляет instance и method"]
  M["sum without(path, instance)<br/>оставляет method + прочие labels"]
  N["GET = 45, POST = 18<br/>таблица 5.3"]
  R --> P --> M --> N
```

Источник: PDF 103–104. Таблица 5.4 имеет конфликтующую строку по `sum without(method, instance)` (см. [source-findings.md](source-findings.md)).

## Выбор меток и контроль кардинальности

```mermaid
flowchart TD
  A["Нужно дополнительное измерение?"]
  B{"Можно осмысленно агрегировать<br/>по его значениям?"}
  C["Стабильная метка с ограниченным<br/>множеством значений"]
  D["Отдельные метрики или логи<br/>(особые случаи — экспортеры)"]
  E{"Число рядов приемлемо?<br/>экземпляры × значения × buckets"}
  F["Инструментировать и проверить<br/>PromQL и суммарную стоимость"]
  G["Снизить кардинальность<br/>или пересмотреть данные"]
  A --> B
  B -->|"да"| C
  B -->|"нет"| D
  C --> E
  E -->|"да"| F
  E -->|"нет"| G
```

Источник: PDF 108–111. Эвристика ниже 10 рядов для обычной метрики/экземпляра — рекомендация авторов, не запрет платформы.
