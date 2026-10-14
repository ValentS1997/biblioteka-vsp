# Commands, Python API and PromQL — глава 5

**Источник:** PDF 97–111, RAG `p0097:c01`–`p0111:c01`. Примеры Python и PromQL взяты только из главы. Операции классифицированы: `read-only`, `workload-generating`, `state-changing`. Ничего не запускалось.

## Метрика с одной меткой — Python (пример 5.1, PDF 99)

**State-changing:** изменяет код HTTP-службы, запускает два HTTP endpoint и регистрирует Counter. **Workload-generating:** открытие URL приложения увеличивает `hello_worlds_total`; `/favicon.ico` тоже может дать инкремент. Проверка: `http://localhost:8000/metrics`, где присутствуют соответствующие ряды. Rollback изменений кода: [Needs confirmation].

```python
import http.server
from prometheus_client import start_http_server, Counter

REQUESTS = Counter('hello_worlds_total',
        'Hello Worlds requested.',
        labelnames=['path'])

class MyHandler(http.server.BaseHTTPRequestHandler):
    def do_GET(self):
        REQUESTS.labels(self.path).inc()
        self.send_response(200)
        self.end_headers()
        self.wfile.write(b"Hello World")

if __name__ == "__main__":
    start_http_server(8000)
    server = http.server.HTTPServer(('localhost', 8001), MyHandler)
    server.serve_forever()
```

**Важно:** `labelnames='path'` в Python означало бы набор символов `p, a, t, h`, а не один label (сноска PDF 99).

## Две метки, child и инициализация

| API из RAG | Класс | Эффект / verification / rollback |
| --- | --- | --- |
| `Counter(..., labelnames=['path', 'method'])` (PDF 101) | state-changing (код) | Определяет два label; `labels(self.path,self.command).inc()` создаёт/увеличивает child. Проверьте ряды по path+method. Rollback [Needs confirmation]. |
| `FETCHES.labels(name)` в `MyCache.__init__` (PDF 102) | state-changing (runtime) | Сохраняет child для дешёвого `inc()` на каждом fetch; проверить `cache_fetches_total`. Rollback [Needs confirmation]. |
| `REQUESTS.labels('/foo')`, `REQUESTS.labels('/bar')` (PDF 102) | state-changing (runtime) | Инициализирует известные children до первых событий; проверить наличие рядов в `/metrics`. Rollback [Needs confirmation]. |
| `foo = LATENCY.labels('/foo')`; `@foo.time()` (PDF 103) | state-changing (код) | Декоратор на конкретный child Summary, проверка задержек для path. Rollback [Needs confirmation]. |
| Открытие `http://localhost:8001/` и `http://localhost:8001/foo` (PDF 99) | workload-generating | Вызывает сервер и меняет счётчики; проверить серию `path` в `http://localhost:8000/metrics`. |
| Просмотр `http://localhost:8000/metrics` (PDF 99) | read-only | Проверяет наличие и имена рядов; rollback [Not applicable]. |

## Запросы PromQL — read-only

```promql
rate(hello_worlds_total[5m])
```

```promql
sum without(path)(rate(hello_worlds_total[5m]))
```

```promql
sum without(path, instance)(rate(hello_worlds_total[5m]))
```

```promql
sum without(method, instance)(rate(hello_worlds_total[5m]))
```

Первые три выражения в PDF 103–104 дают агрегаты из таблиц 5.1–5.3; для `sum without(path, instance)` таблица 5.3 показывает GET=45 и POST=18 по `job="myjob"`. **Четвёртое выражение и таблица 5.4 конфликтуют по одной подписи ряда:** см. [source-findings.md](source-findings.md); исходные данные не исправлены.

```promql
avg_over_time(resource_state[1h])
```

```promql
sum without(resource) (resource_state)
```

RAG PDF 105: доля времени в перечислимом состоянии и число ресурсов по состоянию. Применение предполагает корректное формирование one-hot Gauge.

```promql
up * on (instance, job) group_left(version) python_info
```

```promql
sum by (version)(python_info)
```

RAG PDF 107–108: первое присоединяет версию к `up` при равенстве `instance`/`job`; второе считает ряды с каждой версией. Метрика `python_info` в примере содержит 1.

```promql
{__name__="up"}
```

PDF 100: эквивалент селектора `up`; `__name__` — системная метка имени метрики.

## Источниковый custom collector для состояния enum (пример 5.7, PDF 105–106)

**State-changing:** регистрация custom collector и `set_state` изменяют значения в реестре; `Lock` используется для защиты одновременного обновления и чтения. Проверка: один из четырёх рядов `resource_state` имеет значение 1, остальные 0. Rollback: [Needs confirmation].

```python
from threading import Lock
from prometheus_client.core import GaugeMetricFamily, REGISTRY

class StateMetric(object):
    def __init__(self):
        self._resource_states = {}
        self._STATES = ["STARTING", "RUNNING", "STOPPING", "TERMINATED",]
        self._mutex = Lock()

    def set_state(self, resource, state):
        with self._mutex:
            self._resource_states[resource] = state

    def collect(self):
        family = GaugeMetricFamily("resource_state",
                "The current state of resources.",
                labels=["resource_state", "resource"])
        with self._mutex:
            for resource, state in self._resource_states.items():
                for s in self._STATES:
                    family.add_metric([s, resource], 1 if s == state else 0)
        yield family

sm = StateMetric()
REGISTRY.register(sm)
sm.set_state("blaa", "RUNNING")
```

## Info-метрики: исходный пример 5.9 (PDF 107)

**State-changing (код):** создаёт метрику с версиями в атрибутах. Синтаксис приведён как в RAG; современная API-совместимость [Needs confirmation]. Проверка: `my_python_info` / экспортируемые метки в среде приложения; конкретный результат главы не показан. Rollback: [Needs confirmation].

```python
from prometheus_client import Info

version_info = {
    "implementation": "CPython",
    "major": "3",
    "minor": "5",
    "patchlevel": "2",
    "version": "3.5.2",
}

INFO = Info("my_python", "Python platform information")
INFO.labels(version_info)
```

## Риски и дисциплина меток

- Не смешивать целевые метки `instance`, `job`, `env`, `cluster`, `region` со стабильными внутренними измерениями приложения (PDF 98–100).
- Модификация набора имён меток — breaking change (PDF 108); согласовать миграцию запросов, дашбордов и правил. Подробный rollback [Needs confirmation].
- Не создавать `{label="total"}` как отдельный ряд с уже агрегированным значением — это может удвоить результат `sum` (PDF 109).
- Не использовать клиентские email, IP, безграничные пути и другие высококардинальные значения без оценки бюджета (PDF 109–111).
- `sample_limit` назван в PDF 111, но **готового YAML/команды в главе нет**: не изобретать.
