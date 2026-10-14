# Configurations, commands и PromQL — глава 17

**Источник:** RAG `p0294:c01`–`p0305:c01`, PDF 294–305, `rag_only`. Примеры не запускались. **read-only**, **state-changing** и **workload-generating** отмечены отдельно. Файлы исторические учебные, не готовая production-конфигурация.

## 1. prometheus.yml — пример 17.1 (PDF 294–295)

**State-changing при применении:** изменение конфигурации Prometheus, её перечитывание/запуск; требует согласования, владельца и rollback [Needs confirmation].

```yaml
global:
  scrape_interval: 10s
  evaluation_interval: 10s
rule_files:
 - rules.yml
scrape_configs:
 - job_name: prometheus
   static_configs:
    - targets:
      - localhost:9090
 - job_name: node
   static_configs:
    - targets:
      - localhost:9100
```

`rule_files` поддерживает glob-подстановки, но **изменения не подхватывает автоматически**. Отдельные сервисы/доступность адресов [Needs confirmation].

## 2. rules.yml — пример 17.2 (PDF 295)

**State-changing при включении:** регулярное вычисление и запись новых samples в TSDB. Проверка `promtool` до reload обязательна как эксплуатационное условие примера.

```yaml
groups:
 - name: example
   rules:
    - record: job:process_cpu_seconds:rate5m
      expr: sum without(instance)(rate(process_cpu_seconds_total[5m]))
    - record: job:process_open_fds:max
      expr: max without(instance)(process_open_fds)
```

Имя группы должно быть уникально в пределах файла. Правила внутри группы упорядочены; `labels` и локальный `evaluation_interval` возможны, но в примере не указаны (PDF 295–296).

## 3. Проверка и reload (PDF 295–296)

**Read-only validation, не меняет активную конфигурацию:**

```sh
promtool check config prometheus.yml
promtool check rules rules.yml
```

В исходнике указаны команды `promtool check config`/`promtool check rules` без всех аргументов, поэтому имена файлов выше **добавлены из примеров 17.1–17.2 для конкретизации**, а не объявлены дословной полной командой из PDF. Убедиться, что они соответствуют реальным путям: [Needs confirmation]. Первая проверка анализирует и `rule_files`.

**State-changing — сигнал на активный процесс, source literal (не исполнять без согласования):**

```sh
kill -HUP <pid>
```

`<pid>` — текстовый placeholder из PDF, **не реальный PID**. Отправка сигнала или restart изменяет активную конфигурацию. Rollback/source-safe preflight [Needs confirmation].

**State-changing — HTTP POST `/-/reload`** при `--web.enable-lifecycle`. Источник называет HTTP метод и endpoint, **не приводит законченной команды curl**; curl или скрипт для POST здесь не изобретаются. Не открывать endpoint без контроля доступа. Read-only observability: `http://localhost:9090/rules`, `prometheus_config_last_reload_successful`, `prometheus_rule_group_last_duration_seconds`.

## 4. Предварительная агрегация для дашборда (PDF 297)

**State-changing при активации, workload-generating при каждом evaluation:**

```yaml
groups:
 - name: node
   rules:
    - record: job:process_cpu_seconds:rate5m
      expr: >
        sum without(instance)(
          rate(process_cpu_seconds_total{job="node"}[5m])
        )
```

После активации ряд `job:process_cpu_seconds:rate5m` считывается вместо дорогого запроса для каждого графика. Не гарантировать единственный ряд при дополнительных labels: итоговая кардинальность зависит от реально сохранённых меток.

## 5. Зависимые записи в одной группе (PDF 298)

```yaml
groups:
 - name: node
   rules:
    - record: job_device:node_disk_read_bytes:rate5m
      expr: >
        sum without(instance)(
          rate(node_disk_read_bytes_total{job="node"}[5m])
        )
    - record: job:node_disk_read_bytes:rate5m
      expr: >
        sum without(device)(
          job_device:node_disk_read_bytes:rate5m{job="node"}
        )
```

Первый результат записывается до выполнения второго. Группы независимы; зависимые правила не разносить по разным группам ради гарантий порядка.

## 6. Подготовка диапазона для `_over_time` (PDF 299)

**State-changing / workload-generating при расписании:**

```yaml
groups:
 - name: j_job_rules
   rules:
    - record: job:x:rate5m
      expr: >
        sum without(instance)(
          rate(x_total{job="j"}[5m])
        )
    - record: job:x:max_over_time1h_rate5m
      expr: max_over_time(job:x:rate5m{job="j"}[1h])
```

Исходный **нерабочий без подзапроса** пример (не выполнять как правило):

```text
max_over_time(sum without(instance)(rate(x_total[5m]))[1h])
```

Ключевое правило: `rate` **до** `sum`. `rate(sum(x_total)[5m])` — нежелательный алгоритм: reset отдельного счётчика вызывает ложный пик (PDF 299).

## 7. Запрет на перенос значений labels в имена (PDF 300)

**Учебный антипаттерн — не применять:**

```yaml
- record: job_device:node_disk_read_bytes_sda:rate5m
  expr: >
    sum without(instance)(
      rate(node_disk_read_bytes_total{job="node",device="sda"}[5m])
    )
- record: job_device:node_disk_read_bytes_sdb:rate5m
  expr: >
    sum without(instance)(
      rate(node_disk_read_bytes_total{job="node",device="sdb"}[5m])
    )
```

Используйте отдельные значения label `device` в одном имени ряда, чтобы избежать размножения правил на каждый диск.

## 8. Именование: показательная цепочка (PDF 302–304)

```yaml
- record: job_bar:foo:rate5m
  expr: sum without(instance)(rate(foo_total{job="j"}[5m]))
- record: job:foo:rate5m
  expr: sum without(bar)(job_bar:foo:rate5m{job="j"})
```

**Намеренно ошибочный пример PDF 303:**
```yaml
- record: job:foo_per_bar:ratio_rate5m
  expr: >
    (
      job:foo:rate5m{job="j"}
      /
      job:bar:rate10m{job="j"}
    )
```
Несовместимость `rate5m` и `rate10m` делает ratio сомнительным; источник приводит это **как тест способности читать имена**, а не как конфигурацию к запуску.

**Среднее: не усреднять средние (PDF 304)**. На правильном концептуальном уровне требуется `sum(...._sum:rate5m)/sum(...._count:rate5m)` до деления. **Буквальный «правильный» блок в PDF 304 содержит лишние закрывающие скобки;** исходник приведён в [source-findings.md](source-findings.md), но здесь не оформлен как готовый YAML для применения. Не исправлять silently.

## Приёмка, безопасность, rollback

- Развёртывание/reload меняет TSDB: предварительная проверка, backup файлов, получение разрешения, контроль статуса и журналов, наблюдение за расходом ресурсов. Конкретная политика и rollback **[Needs confirmation]**.
- Правила вызываются периодически: особенно осторожно с длинными range и `evaluation_interval` (PDF 297–301).
- Издательская глава не содержит команд безопасного удаления ранее записанных samples или точного механизма rollback; **ничего не запускалось**, данные не изменены.
