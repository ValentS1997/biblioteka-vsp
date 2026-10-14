# Source findings — глава 20 «Безопасность на стороне сервера»

**Provenance:** PDF 345–349, `p0345:c01`–`p0349:c01`; source SHA256 `ab45c7bc9a393b15bc60628dfceaa45db71388fd28e75c5c55ab6eaf5930f787`; strict `rag_only`. Фиксируем факты и риски извлечённого текста, не исправляя PDF или RAG. Привязка к фактическому runtime отсутствует.

## F-01 — [Source configuration mismatch]: сертификат DNS vs curl IP

- **RAG `p0346:c01`:** `openssl req ... -subj "/CN=localhost" -addext "subjectAltName = DNS:localhost"`.
- **Там же:** `curl --cacert prometheus.crt https://127.0.0.1:9090/metrics`. На PDF 349 эта же IP-форма повторена с `-u julien:demo`.
- **Суть:** source показывает **DNS SAN localhost**, а соединение инициирует к **IP literal 127.0.0.1**. В напечатанном сертификате IP SAN не заявлен. Поэтому пример потенциально не проходит проверку hostname, несмотря на `--cacert`.
- **Решение:** не утверждать успешный `curl` или необходимость отключить проверку. Для действительной среды hostname, SAN, endpoint и результат проверки **[Needs confirmation]**; никаких внешних исправлений в исходник не внесено.

## F-02 — [Source contradiction]: HTTP-адрес после активации TLS

- **RAG `p0346:c01`:** после запуска `./prometheus --web.config.file web.yml` автор переходит к HTTPS.
- **RAG `p0348:c01`:** после настройки `tls_server_config` + `basic_auth_users` сказано «откройте в браузере страницу `http://127.0.0.1:9090`».
- **Проблема:** `http://` не соответствует только что описанному серверу с включённым TLS; автоматический redirect/parallel HTTP endpoint в главе не заявлен. Не представлять URL как надёжный шаг проверки.
- **Решение:** оставить буквальную цитату с оговоркой, не «исправлять» silent.

## F-03 — [Source code mismatch]: неправильно оформлен self-scrape YAML с Basic Auth

- **RAG `p0346:c01`–`p0347:c01`, пример 20.2:** после `tls_config.ca_file` присутствует `static_configs:` и затем `- targets: ['localhost:9090']`.
- **RAG `p0349:c01`, пример 20.5:** после `basic_auth.username` и `password: demo` сразу идёт `- targets: ['localhost:9090']` **без `static_configs:`**.
- **Проблема:** пример 20.5 неполон/неправильно структурирован по отношению к предыдущему авторскому примеру и не может приниматься как проверенная scrape configuration. Причина (типографика/извлечение) **[Needs confirmation]**.
- **Решение:** исходный фрагмент сохранён в [commands.md](commands.md) как `text` (не runnable YAML); корректный вариант не изобретается и не применялся.

## F-04 — [Source security limitation]: опубликованный пароль и bcrypt hash

- **RAG `p0348:c01`:** используется пароль **`demo`**, аккаунт **`julien`**, bcrypt-хеш целиком напечатан; cost 10, рекомендация «10–12» в контексте издания.
- **RAG `p0349:c01`:** `basic_auth.username: julien`, `password: demo`, `curl -u julien:demo`.
- **Проблема:** исходный пароль известен читателю; публикация хеша не превращает публичный пароль в безопасный. Примеры Basic Auth также показывают передачу credentials в аргументах программы. В production эти строки **непригодны**.
- **Решение:** конфигурации приведены только как учебные, помечены state-changing; не вставлять реальные секреты, не использовать `julien/demo`. Политики хранения/ротации и безопасного command-line ввода источником не определены: **[Needs confirmation]**.

## F-05 — [Source security limitation]: приватный ключ без passphrase

- **RAG `p0346:c01`:** команда `openssl req -new -newkey rsa:2048 -days 365 -nodes -x509 -keyout prometheus.key ...` создаёт приватный ключ; `-nodes` означает ключ без шифрования паролем.
- **Ограничение:** нет инструкций о owner/mode, секретном хранилище, безопасности каталога, rotation, сроке сертификата для реального сервиса или контроле доступа к нему.
- **Источник рекомендует:** в реальной среде внутренний или публичный CA, а не учебную самоподписанную пару.
- **Решение:** не объявлять учебный one-liner production-ready.

## F-06 — [Source fragment limitation]: mTLS TLS-секция неполная

- **RAG `p0346:c01`, пример 20.1:** `tls_server_config.cert_file/key_file`.
- **RAG `p0347:c01`, пример 20.3:** `tls_server_config.client_auth_type: RequireAndVerifyClientCert` и `client_ca_file: client_ca.crt`, **без cert_file/key_file**.
- **Контекст:** пример 20.3 прямо под заголовком «Дополнительные параметры TLS», значит это добавление к ранее описанному server TLS, а не самостоятельный полнофункциональный deployment.
- **Решение:** явно обозначать source example 20.3 как фрагмент. Совместимость текущих TLS settings **[Needs confirmation]**.

## F-07 — [Source operational limitation]: разная политика reload и широкая команда

- **RAG `p0345:c01`:** `web.yml` по `--web.config.file` перечитывается при каждом запросе.
- **RAG `p0347:c01`:** после изменения `prometheus.yml` приводится `killall -HUP prometheus`.
- **Ограничение:** это два файла с разной моделью загрузки; `killall` влияет на процессы с указанным именем. Процедуры поиска правильного PID, резерва, подтверждения успешного reload и rollback не представлены.
- **Решение:** классифицировать HUP как state-changing; не выполнять на реальном хосте.

## F-08 — [Source scope]: авторизация и безопасные defaults

- **RAG `p0347:c01`:** перечислены `min_version/max_version` (включая `TLS10`/ `TLS11` как names), `cipher_suites`, `prefer_cipher_suites`, `curve_preferences`. Автор предупреждает, что не следует изменять defaults без понимания последствий.
- **RAG `p0348:c01`:** нативная конфигурация не обеспечивает тонкие ACL/OAuth/LDAP и предлагает reverse proxy.
- **Ограничение:** перечисление возможных версий TLS **не является рекомендацией включить устаревшие версии**. Нет проверенной схемы identity provider, network ACL, reverse proxy, актуальных cipher suites или политик. Не восполнять по памяти модели.

**Статус реестра:** `source_findings_recorded`. Ни одна исходная ошибка, пользовательский файл или конфигурация не исправлены и не исполнены.
