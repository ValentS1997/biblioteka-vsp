# Глава 7 — архитектура прогнозирования

Источник: канонический RAG, PDF p.202–232, chunks p0207-c01–p0229-c01. Диаграммы — логическое обобщение, не копии рисунков книги.

## Batch и online

```mermaid
flowchart TD
  A[Historical data] --> B[Batch feature pipeline]
  B --> C[Precomputed features]
  C --> D[Batch prediction store]
  D --> E[Fetch prepared response]
  C --> F[Online prediction service]
  G[Streaming events] --> H[Streaming features]
  H --> F
  I[User request] --> F
  F --> J[On-demand prediction]
```

Три режима: пакетное прогнозирование; онлайн-прогнозирование только с пакетными признаками; онлайн-прогнозирование с пакетными и потоковыми признаками. [p0207-c01–p0210-c01]

## Train-serving consistency

```mermaid
flowchart TD
  A[Batch training] --> C[Train feature values]
  B[Streaming inference] --> D[Serving feature values]
  C --> E{Same feature semantics?}
  D --> E
  E -->|No| F[Investigate skew]
  E -->|Yes| G[Check serving quality]
```

Различие вычисления скользящих признаков и риск ошибок — p0212-c01–p0213-c01.

## Optimization path

```mermaid
flowchart LR
  A[Model] --> B[Compression candidate]
  B --> C[Intermediate representation]
  C --> D[Runtime optimization]
  D --> E[Target hardware]
  E --> F[Check latency and quality]
```

Сжатие, компиляция и проверка качества — p0214-c01–p0229-c01. Численные пороги PASS и rollback: [Needs confirmation].
