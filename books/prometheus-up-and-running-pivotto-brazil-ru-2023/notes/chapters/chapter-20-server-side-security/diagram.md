# Mermaid — глава 20 «Безопасность на стороне сервера»

**Источник:** PDF 345–349, `p0345:c01`–`p0349:c01`, strict `rag_only`. Диаграммы синтезированы по тексту, не являются проверенной схемой сети конкретного deployment.

## Контур доступа

```mermaid
flowchart TD
 CLIENT["Клиент: браузер или API"]
 PROXY["Опциональный reverse proxy<br/>OAuth, LDAP или тонкие ACL"]
 WEB["Prometheus: --web.config.file web.yml"]
 TLS["TLS: cert_file, key_file"]
 AUTH["Basic Auth: bcrypt hash users"]
 METRICS["Prometheus /metrics и web endpoints"]
 CLIENT --> PROXY --> WEB
 CLIENT --> WEB
 WEB --> TLS --> AUTH --> METRICS
```

PDF 345, 347–348. Не означает, что Basic Auth всегда обязательно включена при TLS: главы описывают эти функции отдельно и затем вместе. Клиентская TLS-аутентификация — дополнительный вариант.

## Разделение файлов и reload

```mermaid
flowchart LR
 W["web.yml"]
 FLAG["--web.config.file"]
 READ["Перечитывается<br/>при каждом запросе"]
 MAIN["prometheus.yml"]
 SCRAPE["HTTPS self-scrape<br/>scheme/ca_file/basic_auth"]
 HUP["reload конфигурации<br/>SIGHUP"]
 W --> FLAG --> READ
 MAIN --> SCRAPE --> HUP
```

PDF 345–349. Изменение `prometheus.yml` не тождественно обновлению `web.yml`. Операции конфигурации и HUP — **state-changing**, здесь не выполнялись.

## Контроль TLS hostname

```mermaid
flowchart TD
 CERT["openssl SAN: DNS:localhost"]
 TARGET["prometheus.yml target: localhost:9090"]
 CURL["curl URL: https://127.0.0.1:9090"]
 OK["Имя target соответствует DNS SAN"]
 RISK["IP SAN 127.0.0.1 не показан<br/>hostname check: Needs confirmation"]
 CERT --> TARGET --> OK
 CERT --> CURL --> RISK
```

PDF 346–347. Схема показывает буквальную несогласованность source; не утверждает о фактическом результате выполнения curl.

## Basic Auth и пределы доверия

```mermaid
flowchart TD
 PASS["Пароль, выбранный пользователем"]
 BCRYPT["htpasswd bcrypt hash"]
 FILE["web.yml: basic_auth_users"]
 HEADER["Клиент: Basic Auth HTTP header"]
 HTTPS["Защищённое соединение TLS"]
 CHECK["Сопоставление пароля с hash"]
 PASS --> BCRYPT --> FILE --> CHECK
 HEADER --> HTTPS --> CHECK
```

PDF 347–349. Учебный `demo` в исходнике публичен. Нельзя переносить его как настоящий секрет.

## Разрыв исходного self-scrape YAML

```mermaid
flowchart TD
 OLD["Пример 20.2<br/>static_configs: - targets"]
 NEW["Пример 20.5<br/>basic_auth и - targets<br/>без static_configs"]
 VALID["Проверка YAML необходима<br/>не копировать как готовый config"]
 OLD --> VALID
 NEW --> VALID
```

PDF 346–349. Извлечённый код и ожидаемый runtime не проверялись; подробности — [source-findings.md](source-findings.md).
