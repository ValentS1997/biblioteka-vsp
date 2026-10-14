# Cheatsheet — глава 20: серверная безопасность Prometheus

**Источник:** `p0345:c01`–`p0349:c01`, PDF 345–349, строгий `rag_only`. Исторический пример, совместимость/окружение **[Needs confirmation]**. Команды не исполнялись.

## Symptom → context → проверка → next action

| Симптом | Контекст из главы | Read-only проверка | Интерпретация / действие |
| --- | --- | --- | --- |
| HTTPS не открывается | `--web.config.file` с `tls_server_config` | Проверить путь `web.yml`, `cert_file`, `key_file`, `./promtool check web-config web.yml` (PDF 345–346) | Веб-серверу нужны существующие TLS файлы; актуальные пути и права [Needs confirmation] |
| `curl --cacert` отклоняет сертификат | Self-signed `DNS:localhost`, URL `127.0.0.1` | Сопоставить SAN сертификата и имя узла в URL (PDF 346) | Вероятен mismatch: в certificate указан DNS localhost, IP SAN для 127.0.0.1 не показан. Не отключать проверку имени просто ради обхода; фактическое поведение [Needs confirmation] |
| Self-scrape Prometheus стал DOWN после TLS | Сервер теперь слушает HTTPS, `prometheus.yml` — прежние scrape settings | Проверить `scheme: https`, `tls_config.ca_file`, hostname target, status reload (PDF 346–347) | Изменения `prometheus.yml` требуют reload; изменение `web.yml` перечитывается при запросе |
| Web UI запрашивает пароль | `basic_auth_users` хранит bcrypt | Проверить наличие пользователя и хеша в web config, отсутствие plaintext (PDF 347–348) | Пароль `demo` в книге публичен и не годится для реальных credential |
| После включения Basic Auth самосбор не работает | Scrape стал HTTPS + Basic Auth | Сверить `basic_auth`, TLS scheme, CA, корректный `static_configs` (PDF 349) | Исходный YAML PDF 349 **не содержит** `static_configs`; нельзя использовать буквально |
| Требуется OAuth, LDAP или ACL для разных страниц | Описанная native Basic Auth не реализует это | Сверить требования access control и архитектуру (PDF 348) | Источник предлагает reverse proxy; его настройки и безопасность не описаны |
| Нужна проверка клиентского сертификата | `RequireAndVerifyClientCert` и `client_ca_file` | Сверить полный `tls_server_config` (PDF 347) | Фрагмент 20.3 добавляет параметры к TLS, но не является полной серверной конфигурацией |

## Baseline: поведение исходника

- `web.yml` задаётся через `--web.config.file`. По книге содержимое перечитывается при каждом запросе; restart для **правки этого файла** не нужен (PDF 345).
- Для self-signed сертификата автор использует `openssl req -new -newkey rsa:2048 -days 365 -nodes -x509 ... -subj "/CN=localhost" -addext "subjectAltName = DNS:localhost"` (PDF 346). Приватный ключ `prometheus.key` без passphrase — учебное упрощение; права, хранение и rotation **[Needs confirmation]**.
- Серверный TLS: `tls_server_config.cert_file` + `key_file`. Self-scrape TLS: `scheme: https` + `tls_config.ca_file` в **другом файле** `prometheus.yml` (PDF 346–347).
- Дополнительные опции TLS: `client_auth_type`, `client_ca_file`, `min_version`/`max_version`, `cipher_suites`, `prefer_cipher_suites`, `curve_preferences`. Авторы рекомендуют не менять безопасные defaults без необходимости (PDF 347).
- Basic Auth в web config: `basic_auth_users.<name>: <bcrypt hash>`; `htpasswd -nBC 10 "" | tr -d ':\n'` печатает хеш; рекомендованная стоимость bcrypt по источнику 10–12 — **историческая рекомендация, не проверенное актуальное требование** (PDF 348).
- Basic Auth передаёт пароль в HTTP-заголовке, поэтому авторы настоятельно рекомендуют TLS (PDF 348).
- В источнике после включения TLS упомянут `http://127.0.0.1:9090`; это конфликт с предшествующей настройкой TLS (PDF 348).

## Безопасный порядок проверки

1. Установить **реальные** hostnames, доверенный CA, способ хранения ключей и сценарий доступа (напрямую или через reverse proxy). В книге предлагаются внутренний/общедоступный CA для production, но нет рабочих настроек инфраструктуры (PDF 345–346).
2. Проверить, что сертификат соответствует используемому DNS/IP. Обратите внимание на `DNS:localhost` в source и `https://127.0.0.1` в curl (PDF 346).
3. Прочитать `web.yml` и проверить `./promtool check web-config web.yml` **до** изменения running process; исходная команда read-only (PDF 346).
4. Если нужен HTTPS self-scrape, сверить `prometheus.yml`: `scheme:https`, `tls_config.ca_file`, hostname target, а при Basic Auth — `basic_auth.username/password`. Неправильный YAML source 20.5 не применять без исправления и валидации (PDF 346–349).
5. Если речь о mTLS, проверить client CA и наличие **полной** TLS конфигурации, не копировать фрагмент 20.3 отдельно (PDF 347).
6. Проверить, не попали ли реальные секреты в документацию, репозиторий, логи, командные строки, небезопасные файлы. Глава **не описывает** полноценную secret-management процедуру, поэтому конкретные безопасные меры организации [Needs confirmation].
7. После **санкционированного** развёртывания проверить соединение и scrape по действительным адресам и credentials; результаты runtime здесь не получены.

## Modifying / side effects / rollback

- **State-changing:** OpenSSL создаёт `prometheus.key`/`prometheus.crt`; изменение `web.yml` меняет аутентификацию/TLS следующего запроса; создание/замена `prometheus.yml`; запуск `prometheus --web.config.file`; `killall -HUP prometheus` посылает сигнал процессам с именем prometheus (PDF 346–347).
- **State-changing / security-sensitive:** `htpasswd` создаёт bcrypt хеш из введённого пароля; заполнение `basic_auth_users` и `basic_auth` меняет доступ и self-scrape; нельзя использовать `demo` в настоящей инсталляции (PDF 348–349).
- **Read-only, but request-generating:** `curl` запрашивает `/metrics` и создаёт сетевую нагрузку; примеры с `-u julien:demo` могут раскрывать plaintext пароль в истории/списке процессов. Source snippet помечен как демонстрация, не рекомендован к запуску (PDF 349).
- **Verification:** валидная конфигурация, HTTPS с hostname validation, корректный self-scrape, запрос логина, отсутствие анонимного доступа там, где Basic Auth должна действовать.
- **Rollback [Needs confirmation]:** в главе нет процедур backup, recovery утерянного доступа, пересоздания клиентских сертификатов, замены secrets или корректного отката обоих файлов. Не разрывать работающий доступ без заранее проверенного пути восстановления.

См. [source-findings.md](source-findings.md) и [commands.md](commands.md).
