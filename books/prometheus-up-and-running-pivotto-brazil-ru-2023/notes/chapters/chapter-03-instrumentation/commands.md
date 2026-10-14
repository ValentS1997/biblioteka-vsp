# Подтверждённые команды, API и PromQL — глава 3

**Источник:** RAG PDF 54–75. Команды не запускались. `state-changing` относится к коду/рабочей среде, `workload-generating` — к созданию тестового трафика. Тестовые имена `hello_world*` не являются производственными именами.

## Shell и URL из книги

| Действие | Класс | Эффект / риск | Проверка | Rollback |
| --- | --- | --- | --- | --- |
| `pip install prometheus_client` | state-changing | Установка Python-клиента в активную среду (PDF 54); изменения зависимостей | Пример Python создаёт endpoint метрик (PDF 54–55) | [Needs confirmation] |
| Запуск программы под `python3` (точная строка запуска **не приведена**) | state-changing | HTTP на `:8001`, endpoint метрик на `:8000`; требуется ограничить доступ (PDF 54–55) | `http://localhost:8001/` и `http://localhost:8000/` | [Needs confirmation] |
| Открытие `http://localhost:8001/` | workload-generating | Отправляет запрос `Hello World`, увеличивает Counter после добавления инструментирования (PDF 54–57) | Counter изменился; браузер может также вызвать `/favicon.ico` | [Not applicable] |
| Открытие `http://localhost:8000/` | read-only | Просмотр `/metrics` (PDF 55) | Видны метрики Python/приложения | [Not applicable] |
| Открытие `http://localhost:9090/` | read-only | Браузер выражений Prometheus (PDF 55) | `python_info` найден | [Not applicable] |

## Источниковый Python: приложение (пример 3.1, PDF 54–55)

**State-changing:** запуск этого кода поднимает две HTTP-службы. Код ниже структурно объединён с соседних страниц, без добавления операций.

```python
import http.server
from prometheus_client import start_http_server

class MyHandler(http.server.BaseHTTPRequestHandler):
    def do_GET(self):
        self.send_response(200)
        self.end_headers()
        self.wfile.write(b"Hello World")

if __name__ == "__main__":
    start_http_server(8000)
    server = http.server.HTTPServer(('localhost', 8001), MyHandler)
    server.serve_forever()
```

Книга использует `prometheus.yml` (PDF 55) для scrape: **state-changing** конфигурация сервера, верификация через `python_info`. Rollback: [Needs confirmation].

```yaml
global:
  scrape_interval: 10s
scrape_configs:
 - job_name: example
   static_configs:
    - targets:
      - localhost:8000
```

## API инструментирования (из примеров)

| API / выражение | Класс | Назначение | PDF |
| --- | --- | --- | --- |
| `Counter('hello_worlds_total', 'Hello Worlds requested.')` | state-changing (код) | Регистрирует счётчик | 56–57 |
| `REQUESTS.inc()` | state-changing (runtime metric) | +1 при обработке GET | 56–57 |
| `EXCEPTIONS.count_exceptions()` | state-changing (runtime metric) | Учитывает исключения; context manager / декоратор, исключения не скрывает | 58–59 |
| `SALES.inc(euros)` | state-changing (runtime metric) | Прибавляет неотрицательную дробную сумму; отрицательное запрещено | 60 |
| `INPROGRESS.inc()`, `INPROGRESS.dec()` | state-changing (runtime metric) | Количество выполняемых запросов | 61 |
| `LAST.set(time.time())` | state-changing (runtime metric) | Момент завершения обработки в секундах Unix | 61 |
| `@INPROGRESS.track_inprogress()` | state-changing (код) | Учитывает активные запросы и исключения | 62 |
| `LAST.set_to_current_time()` | state-changing (runtime metric) | Время выполнения | 62 |
| `TIME.set_function(lambda: time.time())` | state-changing (код) | Callback на scrape; требуется потокобезопасность | 62–63 |
| `LATENCY.observe(time.time() - start)` | state-changing (runtime metric) | Наблюдение задержки Summary | 63 |
| `@LATENCY.time()` | state-changing (код) | Измерение задержки Summary/Histogram | 64–65 |
| `REGISTRY.get_sample_value('foos_total')` | read-only | Получение значения метрики для теста | 69 |

**Минимальный Counter из примера 3.3 (PDF 56–57):**

```python
from prometheus_client import Counter
REQUESTS = Counter('hello_worlds_total', 'Hello Worlds requested.')
# Внутри MyHandler.do_GET:
REQUESTS.inc()
```

**Gauge и Summary (PDF 61, 63):**

```python
from prometheus_client import Gauge, Summary
INPROGRESS = Gauge('hello_worlds_inprogress', 'Number of Hello Worlds in progress.')
LAST = Gauge('hello_world_last_time_seconds', 'The last time a Hello World was served.')
LATENCY = Summary('hello_world_latency_seconds', 'Time for a request Hello World.')
```

**Histogram и buckets (PDF 65–66):**

```python
from prometheus_client import Histogram
LATENCY = Histogram('hello_world_latency_seconds', 'Time for a request Hello World.',
                    buckets=[0.0001, 0.0002, 0.0005, 0.001, 0.01, 0.1])
# В примере: @LATENCY.time()
```

Замечание: эти объявления показывают **альтернативные версии** метрики LATENCY, а не один исполняемый модуль. Одновременная регистрация Summary и Histogram с одним базовым именем нарушит требование уникальности имён (PDF 57). Изменение buckets увеличивает число временных рядов (PDF 66–67).

## Запросы PromQL — все read-only

| Из RAG | Описание | PDF |
| --- | --- | --- |
| `python_info` | Базовая метрика клиента Python | 55 |
| `rate(hello_worlds_total[1m])` | Частота GET | 57 |
| `rate(hello_world_exceptions_total[1m])` | Частота исключений | 59 |
| `rate(hello_world_sales_euro_total[1m])` | Сумма продаж в евро / с (учебный пример) | 60 |
| `hello_world_last_time_seconds` | Время последнего запроса | 61 |
| `time() - hello_world_last_time_seconds` | Сколько прошло после последнего запроса (сек) | 61 |
| `rate(hello_world_latency_seconds_count[1m])` | Частота наблюдений | 63 |
| `rate(hello_world_latency_seconds_sum[1m])` | Суммарная длительность / с | 64 |
| `rate(hello_world_latency_seconds_sum[1m]) / rate(hello_world_latency_seconds_count[1m])` | Средняя задержка | 64, 68 |
| `histogram_quantile(0.95, rate(hello_world_latency_seconds_bucket[1m]))` | Оценка p95 на основе bucket | 66 |

**Source finding — недописанная формула (PDF 59):** в RAG отношение исключений к запросам записано именно так; первая строка не содержит закрывающей скобки. **Не использовать как работающий запрос; не исправлять молча:**

```text
rate(hello_world_exceptions_total[1m]
/
rate(hello_worlds_total[1m])
```

**Source finding — SLA (PDF 67):** источник описывает «долю запросов, выполнявшихся дольше 500 мс», однако приведённое выражение делит количество событий `le="0.5"` на все `le="+Inf"`. Эта пара (формулировка/формула) не согласована; исходник сохранён ниже как **цитируемая структура, а не проверенная формула доли превышений**:

```promql
my_latency_seconds_bucket{le="0.5"}
/ ignoring(le)
my_latency_seconds_bucket{le="+Inf"}
```

Подробнее в [source-findings.md](source-findings.md). Для безопасной рабочей формулы нужны разбор source finding и отдельная проверка, не память модели.

## Модульный тест из примера 3.12 (PDF 69)

**State-changing (код/тестовое выполнение):** создаёт Counter и вызывает `foo()`. Проверяется не абсолютное значение, а **приращение** — устойчиво к другим вызовам в тестовом процессе.

```python
import unittest
from prometheus_client import Counter, REGISTRY

FOOS = Counter('foos_total', 'The number of foo calls.')

def foo():
    FOOS.inc()

class TestFoo(unittest.TestCase):
    def test_counter_inc(self):
        before = REGISTRY.get_sample_value('foos_total')
        foo()
        after = REGISTRY.get_sample_value('foos_total')
        self.assertEqual(1, after - before)
```

Процедуры production deployment, аутентификации HTTP и rollback кода в главе не приведены: **[Needs confirmation]**.
