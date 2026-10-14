# Config, commands и templates — глава 19 «Alertmanager»

**Источник:** строго PDF 321–343, `p0321:c01`–`p0343:c01`; `rag_only`. Ничего не исполнялось. **Read-only**: просмотр UI/файлов, `amtool check-config`. **State-changing:** edit/reload `alertmanager.yml`, Silences, delivery through receivers/webhooks. **Workload-generating:** тестовые alerts и webhook POST. Actual versions, secrets, recipients, network and rollback [Needs confirmation].

## 1. Проверка конфигурации / reload (PDF 322–323)

**Read-only validation — буквальная команда из текста:**
```sh
amtool check-config
```
Книга называет команду, **не фиксирует обязательные аргументы или путь**. В реальной среде указать путь по help конкретного `amtool`: [Needs confirmation]. Запуск `amtool` тут не выполнялся.

**State-changing — способы перезагрузки:** сигнал `SIGHUP` действующему Alertmanager или HTTP `POST /-/reload`. Исходник **не содержит полной shell-команды** с PID/URL/permissions — не реконструировать без environment. Неверная конфигурация может прервать маршрутизацию; backup/rollback [Needs confirmation].

**PDF 323, source-extraction corrupted:** строка `smtp_from: 'yourprometheus@example.org' ❶route:`, а `to: ... ❷` содержит сноски и слипшийся переход на `route`. Не копировать как YAML. Схема ниже — **явно нормализованная иллюстрация без издательских маркеров**, а не буквальный проверенный листинг:
```yaml
global:
  smtp_smarthost: 'localhost:25'
  smtp_from: 'yourprometheus@example.org'
route:
  receiver: example-email
receivers:
  - name: example-email
    email_configs:
      - to: 'youraddress@example.org'
```
Это учебные адреса. SMTP credentials и реальная доставка [Needs confirmation].

## 2. Маршруты, regex, продолжение поиска (PDF 323–326)

**State-changing при активации**, read-only как текст конфигурации:
```yaml
route:
  receiver: fallback-pager
  routes:
    - matchers:
        - severity = page
      receiver: team-pager
    - matchers:
        - severity =~ "(ticket|issue|email)"
      receiver: team-ticket
```

Root без matchers, обязан поймать все alerts. Дочерние routes выбираются по порядку. Матчеры `=`, `!=`, `=~`, `!~`; несколько условий на одном route связаны AND. Regex привязаны к концам строки (PDF 324).

**Route по команде и окружению, **source-intent** PDF 325:** сначала `team=backend`, затем `severity=page` + `env=dev` в `backend-ticket`, потом `severity=page` в `backend-pager`, `severity=ticket` в `backend-ticket`. **Indentation source RAG у вложенного `routes:` повреждён или неоднозначен**, поэтому ниже схема маршрута, а не автоматически проверенный full YAML. Подробности [source-findings.md](source-findings.md).

**`continue: true` для логирования каждого alert, PDF 326:**
```yaml
route:
  receiver: fallback-pager
  routes:
    - receiver: log-alerts
      continue: true
    - matchers:
        - team = frontend
      receiver: frontend-pager
```

Первый route выбирается и затем производится дальнейший поиск; после выбора route потом действуют его `group_by`, интервалы и receiver. Настройки наследуются, кроме `continue`.

## 3. Группировка и интервалы (PDF 326–330)

```yaml
route:
  receiver: fallback-pager
  group_by: [team]
  routes:
    - matchers:
        - team = frontend
      group_by: [region, env]
      group_interval: 10m
      receiver: frontend-pager
      routes:
        - matchers:
            - severity = page
          receiver: frontend-pager
          group_wait: 1m
        - matchers:
            - severity = ticket
          receiver: frontend-ticket
          group_by: [region, env, alertname]
          group_interval: 1d
          repeat_interval: 1d
```

**Внимание:** показанное форматирование сохраняет семантику вложенных routes по PDF 330; фактическая YAML-схема должна проверяться `amtool check-config` и безопасным тестом маршрутизации до активации. Шаблон `group_by: ['...']` упоминается PDF 327 для выключения группировки, но авторами **не рекомендуется как default**.

Defaults в книге: `group_wait: 30s`; `group_interval: 5m`; `repeat_interval: 4h`. Пример timeline PDF 328–329: `t=0 foo`, `t=25 bar`, `t=30 foo+bar notification`, `t=120 baz`, `t=330 foo+bar+baz notification`, `t=400 foo resolved`, `t=700 quu`, `t=930 bar+baz+quu notification`. Проверять относительно настроенных значений, а не переносить эти времена как измерение текущей среды.

## 4. Receivers: фиктивные ключи и URLs (PDF 330–333)

**Все следующие примеры state-changing при применении; реальные секреты НЕ вставлять в коммит.**

```yaml
receivers:
  - name: frontend-pager
    pagerduty_configs:
      - service_key: XXXXXXXX
    slack_configs:
      - api_url: https://hooks.slack.com/services/XXXXXXXX
        channel: '#pages'
```

Источник PDF 331 приводит один receiver с PagerDuty и Slack. Пример для VictorOps использует `global.victorops_api_key` и `victorops_configs[].routing_key`; Telegram может иметь несколько `telegram_configs` у одного receiver (PDF 331–332). Не считать фиктивные `XXXXXXXX` настоящими ключами.

**Webhook, PDF 332:**
```yaml
route:
  receiver: fallback-pager
  routes:
    - receiver: log-alerts
      continue: true
receivers:
  - name: log-alerts
    webhook_configs:
      - url: http://localhost:1234/log
```

Учебный receiver Python 3, пример 19.1 PDF 333 — **state-changing при запуске** (открывает порт 1234 и выводит потенциально чувствительные alerts в stdout). Source literal:
```python
import json
from http.server import BaseHTTPRequestHandler
from http.server import HTTPServer

class LogHandler(BaseHTTPRequestHandler):
    def do_POST(self):
        self.send_response(200)
        self.end_headers()
        length = int(self.headers['Content-Length'])
        data = json.loads(self.rfile.read(length).decode('utf-8'))
        for alert in data["alerts"]:
            print(alert)

if __name__ == '__main__':
    httpd = HTTPServer(('', 1234), LogHandler)
    httpd.serve_forever()
```

**Предостережения:** обработчик печатает данные alert и слушает все интерфейсы. Источник не описывает аутентификацию/TLS, ограничения размера и безопасное выключение. Не применять на открытом интерфейсе. PDF 332 рекомендует локальные supervisors вместо цепочки Prometheus → Alertmanager → webhook для перезапуска процессов.

## 5. Notification templates (PDF 333–337)

**State-changing при включении notifier template**, не исполнялось:
```yaml
receivers:
  - name: frontend-pager
    slack_configs:
      - api_url: https://hooks.slack.com/services/XXXXXXXX
        channel: '#pages'
        title: 'Alerts in {{ .GroupLabels.region }} {{ .GroupLabels.env }}!'
        text: >
          {{ .Alerts | len }} alerts:
          {{ range .Alerts }}
          {{ range .Labels.SortedPairs }}{{ .Name }}={{ .Value }} {{ end }}
          {{ if eq .Annotations.wiki "" -}}
          Wiki: http://wiki.mycompany/{{ .Labels.alertname }}
          {{- else -}}
          Wiki: http://wiki.mycompany/{{ .Annotations.wiki }}
          {{- end }}
          {{ if ne .Annotations.dashboard "" -}}
          Dashboard: {{ .Annotations.dashboard }}&region={{ .Labels.region }}
          {{- end }}
          {{ end }}
```

`.GroupLabels`: `group_by` labels; `.CommonLabels` labels у всех alerts; `.Alerts`: list; `.GroupKey` — машинный групповой ключ; `.Status` — firing/resolved для группы; `.ExternalURL` — URL Alertmanager (PDF 334–336). Источник PDF 337 в прозе пишет `dashbord` рядом с шаблонным `dashboard`: [source-findings.md](source-findings.md). Webhooks получают JSON, а не template-formatted сообщения (PDF 333).

## 6. Динамический адрес получателя — учебная демонстрация / privacy risk (PDF 338–339)

**Sensitive design, НЕ production recommendation:** в source PDF 338 два `record: latency_too_high_threshold` с метками `email_to: foo@example.com`/`bar@example.com`, порогами 0.5/0.7, затем `LatencyTooHigh` c `owner:latency:mean5m > on(owner) group_left(email_to) latency_too_high_threshold`. Второй source-фрагмент PDF 339:
```yaml
route:
  group_by: [email_to, alertname]
  receiver: customer_email
receivers:
  - name: customer_email
    email_configs:
      - to: '{{ .GroupLabels.email_to }}'
        headers:
          subject: 'Alert: {{ .GroupLabels.alertname }}'
```

Издательский маркер `❶` PDF 339 исключён из форматированного YAML. `group_by` обязан включать email_to, иначе сообщения разных клиентов могут смешаться. **Адреса в labels общедоступны в Prometheus/Alertmanager по источнику**. Проверка доступа, приватности и политики доставки до внедрения обязательна; rollback [Needs confirmation].

## 7. Inhibition, resolved, silences (PDF 339–343)

```yaml
inhibit_rules:
  - source_matchers:
      - severity = page-regionfail
    target_matchers:
      - severity = page
    equal: ['region']
```

**State-changing и риск потери уведомления**: при firing alert `severity=page-regionfail` подавляются `severity=page` с тем же `region` (PDF 340–341). `send_resolved: true` — параметр notifier (PDF 339–340), но получение resolved не означает закрытие инцидента.

**Silences UI**: New Silence / Silence по меткам, предпросмотр охвата, комментарий/ответственный, отслеживание active/pending/expired, отмена/reactivation (PDF 341–343); все эти действия **state-changing**. Для ежедневного ограничения времени авторы предлагают условие `hour()` в alert rule главы 18, не повторяющиеся ручные silences.

## Verification / rollback

- До deployment проверить YAML через `amtool check-config`, уникальность receiver, matchers, route priority/continue, group_by, inheritance и интервалы (PDF 323–330); source не даёт формального набора unit tests.
- После безопасного согласованного применения сравнить actual notification batches и group keys с ожидаемыми, качество templates, наличие suppression и UI silences. **Не выполнялось**.
- **Rollback [Needs confirmation]:** нет source-defined плана отката отправленных сообщений, ошибочных receivers, скопированных адресов или всех silences. Принимать изменения только после снапшота конфигурации и разрешения владельца.
