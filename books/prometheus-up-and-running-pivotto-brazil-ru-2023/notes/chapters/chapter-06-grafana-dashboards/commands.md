# Commands, PromQL и операции Grafana — глава 6

**Строгий источник:** RAG PDF 112–129. Команды **не запускались**. Все действия имеют класс `read-only`, `workload-generating` или `state-changing`. Версия Grafana и названия кнопок относятся к **Grafana 9.1.6 по книге**, не верифицированы в текущем релизе.

## Docker / инфраструктура

| Команда | Класс | Эффект и риск | Проверка | Rollback |
| --- | --- | --- | --- | --- |
| `docker run -d --name=grafana --net=host grafana/grafana:9.1.6` | state-changing | Создаёт/запускает контейнер, используется сеть хоста; без `-v` состояние внутри контейнера. HTTP на `:3000`, демонстрационные `admin/admin` (PDF 113). | Открыть `http://localhost:3000/`; сменить пароль (PDF 113). | Точной команды остановки и восстановления томов в главе нет: [Needs confirmation]. |

**Безопасность:** `--net=host` раскрывает сетевые интерфейсы хоста согласно окружению Docker; в книге не заданы production-ограничения. Учебные credentials не использовать в действующей системе. Использование версии/режима Docker на конкретной платформе — [Needs confirmation].

## Источник данных и жизненный цикл дашборда

| Действие в Grafana 9.1.6 (PDF) | Класс | Ожидание, эффект и rollback |
| --- | --- | --- |
| Открыть `http://localhost:3000/` | read-only | UI входа (113–114), rollback [Not applicable]. |
| Войти `admin/admin`, заменить пароль | state-changing | Начальная настройка локального стенда; настройки безопасности сохраняются. Rollback [Needs confirmation] (113). |
| Add your first data source → Prometheus, URL `http://localhost:9090` → Save & Test | state-changing | Создаёт источник и проверяет связь из Grafana; success/message по книге (115–116). Rollback [Needs confirmation]. |
| Create your first dashboard → Add a new panel | state-changing | Создаёт дашборд и панель (116). Для сохранения `Ctrl+S`; rollback [Needs confirmation]. |
| Dashboard settings → Save As | state-changing | Создаёт копию дашборда для эксперимента (117). Удаление/откат копии не описаны. |
| Apply → Save dashboard | state-changing | Сохраняет изменение панели и дашборда (119). Rollback [Needs confirmation]. |
| Переключить time range / refresh interval | read-only / state-changing (UI state) | Меняет представление данных и шаг оценки (119–121); не изменяет исходные временные ряды. |

`Save & Test` не гарантирует корректность каждой PromQL-панели, конкретная валидация неизвестна [Needs confirmation].

## PromQL из главы: запросы чтения

| Выражение | Панель / интерпретация | Источник |
| --- | --- | --- |
| `process_resident_memory_bytes` | Time series, память отдельного процесса | PDF 118–119 |
| `prometheus_tsdb_head_series` | Stat, приблизительное число TSDB-серий | PDF 121 |
| `node_uname_info` | Stat, метка `release` для Kernel version | PDF 122 |
| `rate(node_network_receive_bytes_total[1m])` | Table, Instant, network bytes received/sec | PDF 123–124 |
| `up` | State timeline; значение DOWN в инструкции содержит конфликт | PDF 125 |
| `rate(node_network_receive_bytes_total{device="$Device"}[$__rate_interval])` | Time series, фильтр по одному сетевому интерфейсу; шаблон Grafana подставляет значения | PDF 127 |
| `rate(node_network_receive_bytes_total{device=~"$Device"}[$__rate_interval])` | Логическое применение указанного в тексте PDF 127 режима Multi-value к предыдущему запросу; **производная интерпретация**, не буквальный самостоятельный листинг книги | PDF 127 |

`label_values(node_network_receive_bytes_total, device)` — запрос переменной **в Grafana, а не PromQL** (PDF 126, сноска). `$__rate_interval` — внутренний шаблон Grafana, выбираемый по интервалу сбора и шагу панели (PDF 128).

### Исходная проблемная строка для Bytes Transmit

Ниже **буквальный вариант из RAG p0128:c01**, а не проверенная рабочая команда:

```text
rate(node_network_transmit_bytes_total {device=~"$Device"})[$__rate_interval]
```

В тексте указан `[$__rate_interval]` после закрытия `rate(...)`, из-за чего нет обоснования утверждать, что запрос валиден как PromQL. **Не заменять silently**. См. [source-findings.md](source-findings.md).

## Операции настройки панелей

| Панель / PDF | Операции Grafana (state-changing: конфигурация UI) | Проверка |
| --- | --- | --- |
| **Time series**, 117–119 | Query A `process_resident_memory_bytes`, Run queries; Custom legend `{{job}}`; `data/bytes (IEC)`; Title `Memory Usage`; Apply и Save | График памяти с корректной легендой, заголовком и единицами |
| **Stat (series)**, 121 | `prometheus_tsdb_head_series`, Font Size 200%, Title `Prometheus Time Series`, удалить стандартный threshold 80 | Отображается количество активных рядов |
| **Stat (text)**, 122 | `node_uname_info`, Format as `Table`, Fields `release`, Title `Kernel version` | Показана метка версии ядра |
| **Table**, 123–124 | `rate(node_network_receive_bytes_total[1m])`, Range→Instant, Format Table, Transform → Organize fields (скрыть лишние), Unit bytes/sec (IEC), Title `Network Traffic Received` | Компактные строки по сетевым устройствам |
| **State timeline**, 125 | `up`; Legend `{{job}} / {{instance}}`; Single Color; Value mappings: 1→UP (зелёный) и **2→DOWN (красный, буквально по PDF)** | Требует source adjudication из-за конфликта с `up=0` главы 2 |
| **Templated Time series**, 126–129 | Variable Name `Device`, Data source Prometheus, Refresh On time range change; `label_values(node_network_receive_bytes_total, device)`; legend `{{device}}`, Title `Bytes Received`, bytes/sec; duplicate и Title `Bytes Transmit` | Выбор интерфейса обновляет график; исходящий запрос в PDF имеет несогласованные скобки |

**Классы:** выполнение PromQL для чтения данных — `read-only` относительно TSDB, создание/редактирование/сохранение dashboard/panel/data source — `state-changing`. `Run queries` генерирует запросную нагрузку на Grafana/Prometheus: `workload-generating`, хотя не изменяет хранимые значения.

## Share, сохранение и риски

- `Ctrl+S` и иконка сохранения сохраняют dashboard после правок (PDF 116, 119).
- `Save As` создаёт копию для экспериментирования (PDF 117).
- Выбор `Device` и time range изменяет параметры URL дашборда; Share dashboard создаёт URL и snapshots для after-incident анализа (PDF 129).
- Сам факт наличия URL/снимка **не** подтверждает право доступа или приватность; окружение не описано в главе — [Needs confirmation].
- Для операций выше конкретный production rollback в RAG отсутствует: [Needs confirmation].
