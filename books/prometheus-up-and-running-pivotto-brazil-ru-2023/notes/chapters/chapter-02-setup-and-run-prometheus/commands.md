# Commands, expressions and configuration — глава 2

**Source mode:** RAG-only; PDF 34–52. Префикс `hostname $` в книге — приглашение оболочки, не часть вводимой команды. `*` в именах архивов — шаблон версии. Все модификации — в учебном локальном стенде.

## Команды Linux из главы

| Исходная команда / операция | Класс | Эффект и риск | Проверка | Rollback |
| --- | --- | --- | --- | --- |
| `tar -xzf prometheus-*.linux-amd64.tar.gz` | State-changing | Распаковывает файлы; запись в рабочем каталоге (PDF 35) | Перейти в распакованный каталог (PDF 35) | [Needs confirmation] |
| `cd prometheus-*.linux-amd64/` | State-changing (shell session) | Меняет текущий каталог оболочки (PDF 35) | Последующий `./prometheus` (PDF 36) | [Needs confirmation] |
| `./prometheus` | State-changing | Запускает HTTP/TSDB; лог показывает `0.0.0.0:9090`, TLS отключён (PDF 36) | Лог готовности, `localhost:9090`, Targets UP | `Ctrl+C` для остановки процесса, если запущен в указанной книге консоли (PDF 43) |
| `tar -xzf node_exporter-*.linux-amd64.tar.gz` | State-changing | Распаковка Node Exporter (PDF 43) | `cd node_exporter-*.linux-amd64/` | [Needs confirmation] |
| `cd node_exporter-*.linux-amd64/` | State-changing (shell session) | Переход в каталог Node Exporter (PDF 43) | Последующий `./node_exporter` | [Needs confirmation] |
| `./node_exporter` | State-changing | Запускает экспортер на `:9100`; TLS отключён (PDF 43) | `localhost:9100/metrics`, затем Targets после добавления job | `Ctrl+C` останавливает экспортер и вызывает DOWN (PDF 47) |
| `Ctrl+C` в консоли Prometheus | State-changing | Останавливает сервер для применения обновлённого YAML (PDF 43) | Повторный `./prometheus` и Targets UP | [Needs confirmation] |
| `Ctrl+C` в консоли Node Exporter | State-changing | Учебная симуляция отказа Node Exporter (PDF 47) | Targets DOWN, `up == 0` | Повторный запуск экспортера; подробности [Needs confirmation] |
| `tar -xzf alertmanager-*.linux-amd64.tar.gz` | State-changing | Распаковка Alertmanager (PDF 50) | `cd alertmanager-*.linux-amd64/` | [Needs confirmation] |
| `cd alertmanager-*.linux-amd64/` | State-changing (shell session) | Переход в каталог Alertmanager (PDF 50) | Последующий `./alertmanager` | [Needs confirmation] |
| `./alertmanager` | State-changing | Запускает менеджер уведомлений на `:9093`; в логе TLS отключён (PDF 51) | `localhost:9093/`, наличие InstanceDown | [Needs confirmation] |

Книга также упоминает сигнал `SIGHUP` для перезагрузки Prometheus без перезапуска (PDF 43, сноска) и параметр `--log.level debug` для отладочного логирования попыток scrape (PDF 47). **Конкретная команда отправки SIGHUP не приводится — не выдумывается.**

## PromQL: только запросы чтения

| Выражение | Назначение | PDF |
| --- | --- | --- |
| `up` | Результат последнего извлечения, с метками `job` и `instance` | 38, 44, 47 |
| `process_resident_memory_bytes` | Память процесса (байты) | 38–40 |
| `process_resident_memory_bytes / (1024*1024)` | Представить байты в МиБ | 39 |
| `prometheus_tsdb_head_samples_appended_total` | Накопительный счётчик добавленных выборок | 40–41 |
| `rate(prometheus_tsdb_head_samples_appended_total[1m])` | Средняя скорость добавления выборок в секунду | 41–42 |
| `process_resident_memory_bytes{job="node"}` | Фильтр по метке задания Node Exporter | 45 |
| `rate(node_network_receive_bytes_total[1m])` | Скорость приёма байтов по интерфейсам | 45–46 |
| `up == 0` | Временные ряды неуспешных целей | 48–49 |

Выполнять в браузере выражений `http://localhost:9090/` (Console/Graph). Это read-only запросы к TSDB; не команды shell. Проверка цели: **Status → Targets**; метрики самосбора: `http://localhost:9090/metrics` (PDF 36–38).

## `prometheus.yml` — пример 2.1 (PDF 49)

**State-changing:** редактирование конфигурации, изменяет сбор, оценку правил и направление оповещений. Последующий перезапуск обязателен в сценарии книги; критерии: две цели UP, InstanceDown виден в Alerts после симуляции отказа. Rollback прежнего файла: [Needs confirmation].

```yaml
global:
  scrape_interval: 10s
  evaluation_interval: 10s
rule_files:
 - rules.yml
alerting:
  alertmanagers:
  - static_configs:
    - targets:
       - localhost:9093
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

## `rules.yml` — пример 2.2 (PDF 49)

**State-changing:** задаёт порог устойчивого DOWN и генерирует InstanceDown; риск ложных оповещений при намеренной остановке. Книга использует `for: 1m` для демонстрации, хотя указывает типовую рекомендацию не менее 5 минут.

```yaml
groups:
 - name: example
   rules:
   - alert: InstanceDown
     expr: up == 0
     for: 1m
```

## `alertmanager.yml` — пример 2.3 (PDF 50–51)

**State-changing:** задаёт SMTP-smarthost, отправителя, группировку и получателя. Пример предполагает доступный `localhost:25`; это **предположение книги**, не проверенный ресурс. Адреса являются placeholders. Перед использованием в своей среде подтвердить почтовый маршрут; после запуска проверить `localhost:9093/` и фактическое письмо. Rollback: [Needs confirmation].

```yaml
global:
  smtp_smarthost: 'localhost:25'
  smtp_from: 'yourprometheus@example.org'
route:
  receiver: example-email
  group_by: [alertname]
receivers:
 - name: example-email
   email_configs:
    - to: 'youraddress@example.org'
```

В текстовом извлечении примеры YAML содержали печатные маркеры ❶/❷/❸ и разрыв между PDF 50–51. Здесь удалены только однозначно типографские маркеры и сведены смежные строки; оригинальный факт о разрыве описан в [source-findings.md](source-findings.md).
