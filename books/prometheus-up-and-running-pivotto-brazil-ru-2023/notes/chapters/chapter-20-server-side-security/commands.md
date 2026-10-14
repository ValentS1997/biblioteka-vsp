# Команды и YAML — глава 20 «Безопасность на стороне сервера»

**Provenance:** `p0345:c01`–`p0349:c01`, PDF 345–349, strict `rag_only`. Все команды — **исторические примеры из книги**, **не запускались**. `read-only` — просмотр/валидация; `state-changing` — создаёт файлы, меняет running server/config; `request-generating` — сетевой запрос, возможная утечка credentials. Не считать примеры production-ready.

## 1. Создать self-signed сертификат: source literal, state-changing (PDF 346)

```sh
openssl req -new -newkey rsa:2048 -days 365 -nodes -x509 \
    -keyout prometheus.key -out prometheus.crt \
    -subj "/CN=localhost" -addext "subjectAltName = DNS:localhost"
```

**Побочные эффекты:** создаёт **приватный ключ** `prometheus.key` и сертификат `prometheus.crt` на файловой системе. `-nodes` означает отсутствие шифрования приватного ключа паролем. Не запускать в общем каталоге/недоверенном хосте без политики хранения ключа, доступа и удаления/rotation [Needs confirmation]. Самоподписанный сертификат — учебный; авторы рекомендуют доверенный внутренний CA или публичный CA для реальной эксплуатации.

**Source mismatch:** сертификат содержит только `DNS:localhost`, но запрос ниже использует `127.0.0.1`. Это несоответствие имени в URL и SAN; выполнение TLS проверки имени не подтверждено.

## 2. Включить TLS в web.yml, source literal (PDF 346)

**State-changing при сохранении/применении файла:**
```yaml
tls_server_config:
  cert_file: prometheus.crt
  key_file: prometheus.key
```

**Read-only локальная проверка:**
```sh
./promtool check web-config web.yml
```

По тексту успех: `web.yml SUCCESS`. Это **исходная иллюстрация**, не результат выполненной здесь команды. Файлы должны существовать и соответствовать действительному каталогу запуска: [Needs confirmation].

**State-changing запуск сервера:**
```sh
./prometheus --web.config.file web.yml
```

Источник говорит, что изменения самого `web.yml` перечитываются при каждом запросе (PDF 345). Влияние замены ключей/пользователей на работающие соединения и детали конкретного релиза: [Needs confirmation].

**Request-generating HTTPS GET, source literal — с известным риском hostname mismatch:**
```sh
curl --cacert prometheus.crt https://127.0.0.1:9090/metrics
```

`--cacert` определяет доверие сертификату CA/самоподписанному сертификату, но **не объявляет IP `127.0.0.1` частью SAN**. Для успешной валидации действительное имя URL и имена сертификата необходимо проверить отдельно, не использовать небезопасное отключение проверок молча.

## 3. HTTPS self-scrape, source examples 20.2 (PDF 346–347)

**State-changing при изменении `prometheus.yml` и reload:**
```yaml
scrape_configs:
  - job_name: 'prometheus'
    scheme: https
    tls_config:
      ca_file: prometheus.crt
    static_configs:
    - targets: ['localhost:9090']
```

Это книжный пример самосбора: target по `localhost` согласован с `DNS:localhost`; в отличие от HTTP endpoint, scrape требует `scheme: https`.

**Source literal, state-changing и широкий эффект:**
```sh
killall -HUP prometheus
```

Команда отправляет HUP процессам с именем `prometheus`, а не одному заранее выбранному PID; область воздействия и безопасный способ reload организации: **[Needs confirmation]**. Не выполнять на production по одному примеру. Изменение `prometheus.yml` и изменение `web.yml` имеют разную политику reload в тексте.

## 4. Аутентификация клиентов TLS — дополнительный фрагмент (PDF 347)

**Дополнительные поля, НЕ полный `web.yml`:**
```yaml
tls_server_config:
  client_auth_type: RequireAndVerifyClientCert
  client_ca_file: client_ca.crt
```

В source это «пример 20.3» в разделе дополнительных настроек. Этот блок сам по себе **не содержит** `cert_file`/`key_file` из примера 20.1. Нельзя подменять им рабочую TLS-конфигурацию без объединения и проверки нужного состава параметров. В книге также названы `min_version`, `max_version`, `cipher_suites`, `prefer_cipher_suites`, `curve_preferences`; готовых безопасных значений для среды **нет**.

## 5. Bcrypt: создать хеш пароля — sensitive local operation (PDF 348)

**Источниковая команда (запрашивает пароль интерактивно, выводит его bcrypt-хеш):**
```sh
htpasswd -nBC 10 "" | tr -d ':\n'
```

PDF показывает ввод `demo`, результат bcrypt с префиксом `$2y$10$` и совет выбирать cost 10–12 по состоянию издания. Не делать cost текущей универсальной нормой без проверки. Не вводить настоящий пароль в неподконтрольный terminal, не публиковать полученный hash без оценки угроз [Needs confirmation]. **Это не проверка текущей конфигурации**, а изготовление учетного материала.

**Источник, пример 20.4: TLS + Basic Auth (state-changing):**
```yaml
tls_server_config:
  cert_file: prometheus.crt
  key_file: prometheus.key
basic_auth_users:
  julien: $2y$10$LbwE6OVsPc4PqDFaYwvw/uOkMMficVQrQjtY5KT/BGnAKPa0vK45C
```

**ВАЖНО:** это **публичный учебный хеш для пароля `demo`**. Не использовать ни пароль, ни хеш в настоящих учетных записях. Bcrypt позволяет хранить в web config не plaintext, но Basic Auth передаёт credential в HTTP headers; TLS обязателен для защиты транспорта по книге.

**[Source contradiction] PDF 348:** сразу после активации TLS автор предлагает открыть браузером `http://127.0.0.1:9090` (не `https://`). Этот URL не переносится как подтверждённый рабочий тест.

## 6. Prometheus self-scrape + Basic Auth: исходный некорректный пример 20.5 (PDF 349)

**Буквальный текст книги, НЕ применять — `static_configs` отсутствует:**
```text
scrape_configs:
  - job_name: 'prometheus'
    scheme: https
    tls_config:
      ca_file: prometheus.crt
    basic_auth:
      username: julien
      password: demo
    - targets: ['localhost:9090']
```

В отличие от примера 20.2, `- targets` не помещён под `static_configs:`; это не подтверждённая рабочая конфигурация. Также пароль `demo` полностью публичен. Запрос Basic Auth по книге:

```sh
curl --cacert prometheus.crt -u julien:demo https://127.0.0.1:9090/metrics
```

**Request-generating и credential-exposing:** пароли в аргументах командной строки могут попасть в history/прочие средства наблюдения процесса. Здесь показана точная учебная строка **только для анализа**, она одновременно имеет риск несовпадения IP SAN и публичный пароль; **не выполнять**. Настоящий метод передачи secret не описан в этом RAG: [Needs confirmation].

## Приёмка / verification / rollback

- До модификации проверить действительные пути, права доступа, hostnames/SAN, CA, консистентность `web.yml` и `prometheus.yml`, необходимость reverse proxy или client TLS.
- Валидировать web config `./promtool check web-config web.yml`; **не заявлять успешную проверку исходного 20.5**, отсутствующую в книге.
- После только санкционированного запуска/reload подтвердить hostname-verified HTTPS и self-scrape, запрос Basic Auth и отсутствие анонимного доступа. Runtime здесь не проверялся.
- **Rollback [Needs confirmation]:** глава не описывает восстановление доступа, безопасное возвращение прежней конфигурации, замену сертификата/ключа или секретов. Никакие state-changing операции не выполнялись.
