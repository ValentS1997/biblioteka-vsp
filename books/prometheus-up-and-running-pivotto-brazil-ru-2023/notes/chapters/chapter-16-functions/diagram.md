# Mermaid — глава 16 «Функции»

**Источник:** PDF 273–293, чанки `p0273:c01`–`p0293:c01`, строгий `rag_only`. Диаграммы построены по тексту, не копируют рис. 16.1.

## Типы, вход и результат

```mermaid
flowchart LR
 S["Scalar"]
 V["Instant vector"]
 R["Range vector"]
 M["vector(scalar)"]
 C["scalar(vector)"]
 T["Математика, календарь,<br/>метки, sort"]
 F["rate / increase / deriv / avg_over_time"]
 O["Instant vector result"]
 S --> M --> V
 V --> C --> S
 V --> T --> O
 R --> F --> O
```

PDF 273–275, 285–293. `scalar` возвращает NaN, если вектор пуст или содержит более одного sample. `time`, `pi` и `scalar` названы скалярными результатами в контексте издания.

## Отсутствие цели, ошибка scrape и нулевое значение

```mermaid
flowchart TD
 Q["Есть series up?"]
 E["Есть, но up == 0"]
 N["Нет series up для job"]
 R["Алерт на ошибку scrape"]
 A["absent(up{job=missing})"]
 H["absent_over_time(...[1h])"]
 Z["Нельзя смешивать отсутствие и 0"]
 Q --> E --> R
 Q --> N --> A --> H --> Z
```

PDF 274, 283–284. `absent` возвращает 1 только при пустой выборке, иногда восстанавливая labels из equality matcher.

## Counter: скорость, reset и диагностика

```mermaid
flowchart TD
 C["Counter в range vector"]
 RATE["rate: средняя скорость в секунду,<br/>reset и экстраполяция"]
 INC["increase: rate × длина окна"]
 IR["irate: последние 2 точки"]
 RESET["resets: число уменьшений"]
 AL["Для алертов: rate,<br/>окно не менее 4 scrape intervals"]
 G["Для графиков с zoom: irate"]
 C --> RATE --> AL
 C --> INC
 C --> IR --> G
 C --> RESET
```

PDF 285–289. При недостаточном числе samples ответ по серии может отсутствовать. Не каждый редкий event будет учтён.

## Gauge и временные агрегаты

```mermaid
flowchart TD
 G["Gauge range"]
 CH["changes: число изменений"]
 D["deriv: наклон"]
 P["predict_linear: прогноз"]
 W["holt_winters: сглаживание"]
 O["*_over_time: агрегировать samples"]
 WARN["Не учитывать как временно-взвешенное среднее;<br/>частота scrape меняет вклад точек"]
 G --> CH
 G --> D
 G --> P
 G --> W
 G --> O --> WARN
```

PDF 289–293. Источник рекомендует проверять линейность и пилообразность тренда для прогноза; `avg_over_time(rate(...)[1h])` без явного subquery step помечен в книге как ошибка типов.
