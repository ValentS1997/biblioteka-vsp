# Commands / API — глава 4

**Источник:** только RAG PDF 76–96. Ниже примеры книги, не проверенные на пользовательской инфраструктуре и не рекомендации по текущим версиям библиотек. Признаки `read-only`, `workload-generating`, `state-changing` относятся к действию, а не к строкам описания.

## Read-only: доступ к метрикам и проверка

| Источник | Команда / API | Роль и ожидание |
| --- | --- | --- |
| PDF 94 | `curl http://localhost:8000/metrics \| promtool check metrics` | Анализ текста формата Prometheus; HTTP endpoint может отвечать даже при ошибках формата. |
| PDF 82 | `curl -v -H 'Accept: application/openmetrics-text; version=1.0.0; charset=utf-8' http://127.0.0.1:8000/metrics` | Передача Accept для демонстрации OpenMetrics; читает ответ. |
| PDF 90 | `CollectorRegistry.collect()` (Python) | Снимок метрик реестра; потребление как источник мостов. |
| PDF 91 | `text_string_to_metric_families(u"counter_total 1.0\\n")` | Синтаксический анализ текста в Python. |

`curl` — read-only HTTP GET; даже читательские запросы могут отражаться в служебных счётчиках запросов приложения. Полный ответ сервера и действующая конфигурация: [Needs confirmation].

## Python: экспозиция метрик

- **State-changing (код и работа сервера)** `start_http_server(8000)` создаёт отдельный HTTP-сервер метрик (PDF 77).
- **State-changing (код/маршрутизация)** `make_wsgi_app()` позволяет отдавать метрики в существующей WSGI-службе (PDF 77–78).

```python
from prometheus_client import make_wsgi_app
from wsgiref.simple_server import make_server

metrics_app = make_wsgi_app()

def my_app(environ, start_fn):
    if environ['PATH_INFO'] == '/metrics':
        return metrics_app(environ, start_fn)
    start_fn('200 OK', [])
    return [b'Hello World']

if __name__ == '__main__':
    httpd = make_server('', 8000, my_app)
    httpd.serve_forever()
```

Пример 4.1, PDF 78. Эффект: служба слушает HTTP (адрес `''` в коде); риск публичного раскрытия метрик зависит от сетевых правил, не подтверждён. Проверка: `/metrics` и обычный путь. Rollback: [Needs confirmation].

- **State-changing (код):** Twisted использует `WSGIResource(reactor, reactor.getThreadPool(), make_wsgi_app())`, `root.putChild(b'metrics', metrics_resource)`, `reactor.listenTCP(8000, Site(root))`, `reactor.run()` (PDF 78–79). Риск: порт и зависимость на Twisted. Проверка: endpoint. Rollback: [Needs confirmation].

## Gunicorn multiprocess — изменения и риск удаления

- **State-changing (код):** `multiprocess.mark_process_dead(worker.pid)` в `child_exit(server, worker)` (PDF 79).
- **State-changing (код):** `CollectorRegistry()`, `multiprocess.MultiProcessCollector(registry)`, `make_wsgi_app(registry)`; `Gauge(..., multiprocess_mode='livesum')` для суммы по живым worker (PDF 80).
- **State-changing (окружение):** `export prometheus_multiproc_dir=$PWD/multiproc`, `mkdir -p $prometheus_multiproc_dir` и `gunicorn -w 2 -c config.py app:app` (PDF 81).
- **Опасная команда из книги:** `rm -rf $prometheus_multiproc_dir` (PDF 81). **Не запускать как copy-paste.** В частности, переменная должна содержать корректный изолированный путь к каталогу состояния данного приложения, каталог используется только после остановки связанных worker; произвольное удаление может разрушить данные. Без подтверждения окружения и rollback исполнение **запрещено**.

```python
# Отдельный config.py (пример 4.3, PDF 79)
from prometheus_client import multiprocess

def child_exit(server, worker):
    multiprocess.mark_process_dead(worker.pid)
```

Ожидание по книге: совокупные значения, `http_requests_total` и `http_requests_inprogress`, без `python_info` и `process_`. Ограничения: недоступность custom collectors и Pushgateway для этого multiprocess-режима; старые mmap-файлы, retention по worker и агрегация требуют контроля (PDF 79–82). Rollback: [Needs confirmation].

## Go и Java

| API/команда | Класс | Эффект, проверка, rollback |
| --- | --- | --- |
| `promhttp.Handler()` и `http.Handle("/metrics", promhttp.Handler())` (PDF 82–83) | state-changing (код) | Встраивает endpoint; проверить `/metrics`; rollback [Needs confirmation]. |
| `promauto.NewCounter(prometheus.CounterOpts{...})` (PDF 82–83) | state-changing (код) | Создаёт и регистрирует метрику; проверить вывод и отсутствие конфликтов; rollback [Needs confirmation]. |
| `prometheus.MustRegister(requests)` (PDF 83) | state-changing (код) | Явная регистрация альтернативного счётчика; забытый вызов оставляет его неэкспортируемым. |
| `go get -d -u github.com/prometheus/client_golang/prometheus` (PDF 83) | state-changing | Получение/обновление зависимостей в историческом примере; текущая совместимость [Needs confirmation]. |
| `go run example.go` (PDF 83) | state-changing / workload-generating | Запуск локальной демонстрационной службы на `:8000`; проверка endpoint; rollback [Needs confirmation]. |
| Java `Counter.build().name(...).help(...).register()` (PDF 84–85) | state-changing (код) | Регистрирует счётчик; проверить endpoint; rollback [Needs confirmation]. |
| Java `DefaultExports.initialize()` (PDF 84–85) | state-changing (код) | Включает метрики process/JVM; в тексте названа идемпотентной. |
| Java `new HTTPServer(8000)` (PDF 84) | state-changing (код) | Отдельный HTTP endpoint; проверить метрики; rollback [Needs confirmation]. |
| Java `new MetricsServlet()` (PDF 85) | state-changing (код) | Встраивается в Jetty через servlet-mapping `/metrics`. |

Примеры Java используют зависимости `simpleclient 0.16.0` и `jetty-servlet 11.0.11` (PDF 84–86), как в источнике. Проверка совместимости выбранных версий: [Needs confirmation].

## Pushgateway (PDF 86–89)

**State-changing:** конфигурация Prometheus опрашивает кеш. В книге:

```yaml
scrape_configs:
 - job_name: pushgateway
   honor_labels: true
   static_configs:
    - targets:
      - localhost:9091
```

**State-changing (удалённые метрики)** Python API:

| API | HTTP | Эффект | Verification / rollback |
| --- | --- | --- | --- |
| `push_to_gateway` | PUT | Заменяет метрики группы целиком | проверить группу и `push_time_seconds`; прежние данные не восстанавливаются автоматически |
| `pushadd_to_gateway` | POST | Перезаписывает метрики совпадающих имён; остальные остаются | проверить группу, новые значения; возврат старых значений [Needs confirmation] |
| `delete_from_gateway` | DELETE | Удаляет метрики указанной группы | проверить исчезновение группы; восстановление требует нового push [Needs confirmation] |

Исходная последовательность batch (пример 4.12, PDF 88–89): `CollectorRegistry()`; `Gauge('my_job_duration_seconds', ..., registry=registry)` и `with duration.time(): ...`; после успешного завершения `g = Gauge('my_job_last_success_seconds', ..., registry=registry)` и `g.set_to_current_time()`; `finally: pushadd_to_gateway('localhost:9091', job='batch', registry=registry)`. **Это изменяет данные Pushgateway**; произвольный запуск создаёт устойчивую группу. Имя `my_job_last_success_seconds#` в прозе p0088 — извлечение/исходная опечатка, не использовать как имя метрики.

## Мост и парсер

```python
# GraphiteBridge (пример 4.13, PDF 90); state-changing: внешняя передача
import time
from prometheus_client.bridge.graphite import GraphiteBridge

gb = GraphiteBridge(['graphite.your.org', 2003])
gb.start(10)
while True:
    time.sleep(1)
```

Сетевой destination — **placeholder**, его доступность неизвестна. Проверить на тестовом endpoint; rollback [Needs confirmation].

```python
# Парсер текстового формата (пример 4.14, PDF 91); read-only
from prometheus_client.parser import text_string_to_metric_families

for family in text_string_to_metric_families(u"counter_total 1.0\n"):
    for sample in family.samples:
        print("Name: {0} Labels: {1} Value: {2}".format(*sample))
```

## Exposition форматы — структура по RAG

**Prometheus 0.0.4** — `Content-Type: text/plain; version=0.0.4; charset=utf-8` (PDF 91–94). Метки в `{...}`; `HELP`, `TYPE`; `le="+Inf"` обязателен; `_count` совпадает с `+Inf`. Перевод строки `\n`, timestamps в миллисекундах, осторожное экранирование `\\`, переводов строк и кавычек меток.

```text
# HELP my_counter_total Пример счетчика
# TYPE my_counter_total counter
my_counter_total 14
# HELP latency_seconds Пример гистограммы
# TYPE latency_seconds histogram
latency_seconds_bucket{le="0.1"} 7
latency_seconds_bucket{le="+Inf"} 29
latency_seconds_sum 0.6
latency_seconds_count 29
```

Это **сокращение** примера 4.15 (PDF 92), оставлены две исходные границы вместо полного набора. Не выдавать за идентичный оригинальный листинг.

**OpenMetrics 1.0.0** — `Content-Type: application/openmetrics-text; version=1.0.0; charset=utf-8`, закрытие `# EOF`, `# UNIT`, типы `info`, `stateset`, `gaugehistogram`; `_gcount`, `_gsum`, timestamps в секундах по пояснению и сноске (PDF 94–96). В тексте p0096 противоречивое упоминание миллисекунд — см. [source-findings.md](source-findings.md).

**Пример формата OpenMetrics (структурная выдержка):**

```text
# TYPE my_build_info info
my_build_info{branch="HEAD",version="0.16.0rc1"} 1.0
# EOF
```

Это только фрагмент исходного примера 4.16, не полный файл всех типов.

## Отдельные source-findings

- Python `start_http_server` на PDF 77 сопровождается строкой `// Далее следует ваш код.`, похожей на комментарий, **не являющийся Python-синтаксисом**. Не запускать как готовый листинг и не исправлять оригинал (PDF 77).
- OpenMetrics timestamp на PDF 96 описан одновременно как «в миллисекундах» и «в секундах», а код записан как `1.5100992e9`. Не считать текст однозначным (PDF 96).
- RAG содержит полиграфические маркеры ❶/❷ и разрывы длинных строк в листингах (PDF 88, 92–96). Детали: [source-findings.md](source-findings.md).
