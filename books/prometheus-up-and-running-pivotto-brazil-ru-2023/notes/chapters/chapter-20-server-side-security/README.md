# Глава 20. Безопасность на стороне сервера

**Книга:** «Запускаем Prometheus. Мониторинг инфраструктуры и приложений» (Жюльен Пивотто, Брайан Бразил, Books.kz, 2023). **Inventory:** `0040`; **book_id:** `prometheus-up-and-running-pivotto-brazil-ru-2023`.  
**Контракт:** `BIBLIOTEKA-VSP-CHAPTER-ARTIFACT-COLLECTION v1.7`; **статус:** `RAG_GROUNDED`, не `VERIFIED`/`ACCEPTED`.  
**Source policy:** строгий `rag_only` — только канонические чанки RAG; без прямого PDF, веб-поиска и подмены текста знаниями модели.

## Границы и provenance

- **PDF 345** (`p0345:c01`) — «Глава 20. Безопасность на стороне сервера».
- **PDF 349** (`p0349:c01`) — заключение раздела Basic Authentication; **PDF 350** (`p0350:c01`) открывает главу 21 «Собираем все вместе».
- **Диапазон: PDF 345–349**, `source_locator: pdf_page=345..349`, **пять адресуемых RAG-чанков** `p0345:c01`–`p0349:c01` в `rag/chunks/p0301-p0400/`.
- **Source PDF SHA256:** `ab45c7bc9a393b15bc60628dfceaa45db71388fd28e75c5c55ab6eaf5930f787`. `rag/acceptance.yaml: ACCEPTED`; `rag/manifest.yaml: READY_WITH_KNOWN_LIMITATIONS`. Исходник не менялся.

## Структура главы

| Тема | PDF | Суть |
| --- | --- | --- |
| Средства защиты Prometheus | 345 | Обратный прокси или встроенные TLS/Basic Auth; единые server-side настройки Prometheus и многих официальных экспортеров; `--web.config.file` |
| Сертификат и TLS | 346 | Self-signed RSA-2048 через OpenSSL, `tls_server_config.cert_file/key_file`, `promtool check web-config`, запуск сервера |
| HTTPS self-scrape и client TLS | 346–347 | `scheme: https`, `tls_config.ca_file`; `client_auth_type: RequireAndVerifyClientCert` и `client_ca_file`; TLS versions/ciphers |
| Basic Authentication | 347–348 | Bcrypt-хеши пользователей, `htpasswd -nBC 10`, `basic_auth_users`, рекомендация защищать Basic Auth посредством TLS |
| Self-scrape с Basic Auth | 349 | `basic_auth.username/password`, `curl -u`; финальные замечания |

## Содержание и технические выводы

1. **Нативная server-side защита** настраивается в отдельном `web.yml` через `--web.config.file`. По главе файл перечитывается при каждом HTTP-запросе и его изменения не требуют перезапуска сервера или экспортера (PDF 345). Это **не** то же самое, что изменение `scrape_configs` в `prometheus.yml`: для последнего на PDF 347 дан `killall -HUP prometheus`.
2. **TLS** использует сертификат и приватный ключ, может аутентифицировать клиентов. Для обучения создан self-signed сертификат, но для реальной системы книга рекомендует внутренний или общедоступный CA (PDF 346). Конфигурация `web.yml`: `tls_server_config.cert_file`, `key_file`; проверка `./promtool check web-config web.yml`, запуск `./prometheus --web.config.file web.yml`.
3. **HTTPS self-scrape** требует `scheme: https` и `tls_config.ca_file` (PDF 346–347). В источнике `curl --cacert prometheus.crt https://127.0.0.1:9090/metrics` не согласован с именами `CN=localhost`, `subjectAltName=DNS:localhost`; это **риск несовпадения имени сертификата и адреса URL**, не подтверждённый успешный тест (см. [source-findings.md](source-findings.md)).
4. **mTLS:** `client_auth_type: RequireAndVerifyClientCert` и `client_ca_file: client_ca.crt` — **дополнительные параметры** к серверной TLS-конфигурации, а не отдельно приведённая полная конфигурация (PDF 347). Другие настройки: `min_version`, `max_version`, `cipher_suites`, `prefer_cipher_suites`, `curve_preferences`; не менять defaults без необходимости.
5. **Basic Authentication** хранит bcrypt-хеши паролей в `basic_auth_users`, но пароль передаётся в HTTP-заголовке таким образом, что **TLS необходим для защиты при передаче** (PDF 347–348). В source используется `julien/demo` и заранее напечатанный bcrypt-хеш: **это публичные учебные credentials, непригодные для реального доступа**.
6. **Настройка самого Prometheus как клиента:** при HTTPS + Basic Auth требуется аналогичная настройка `scrape_configs` с `basic_auth.username/password` и `tls_config.ca_file` (PDF 349). Листинг 20.5 в RAG содержит `- targets:` без `static_configs`; **буквально его нельзя считать проверенным YAML для Prometheus**.
7. **Пределы авторизации:** продвинутые ACL/OAuth/LDAP отсутствуют в описанной серверной функциональности; автор предлагает перед Prometheus reverse proxy, выполняющий эти функции (PDF 348). Здесь не описаны ни защита proxy, ни список реальных пользователей, ни server network hardening.

## Обязательные source findings

- **F-01 PDF 346:** `DNS:localhost` против HTTPS URL с `127.0.0.1`; сертификат не заявляет IP SAN, подтверждённая успешность проверки имени **[Needs confirmation]**.
- **F-02 PDF 348:** после включения TLS читателю предлагают открыть `http://127.0.0.1:9090` вместо HTTPS. Не считать указанный URL готовым шагом проверки.
- **F-03 PDF 349:** пример 20.5 имеет `- targets` не под `static_configs`, в отличие от PDF 346–347. Требует отдельной валидации, не silent correction.
- **F-04 PDF 348–349:** пароль `demo` и соответствующий публичный bcrypt-хеш полностью напечатаны; это **не секрет**, а демонстрация, которую запрещено копировать как production identity.
- **F-05 PDF 346:** `openssl ... -nodes` создаёт приватный ключ без парольной защиты (не описаны права файла, lifecycle, rotation). Не обещать безопасную эксплуатацию по одному примеру.
- **F-06 PDF 347:** mTLS-выдержка показывает только дополнительные поля, а не полную `tls_server_config`.
- Детальные locators, отклонения и границы доказуемого: [source-findings.md](source-findings.md).

## Артефакты

[cheatsheet.md](cheatsheet.md) — эксплуатационные сценарии и проверки; [commands.md](commands.md) — исходные команды/YAML с классификацией; [diagram.md](diagram.md) — Mermaid; [visual-cheatsheet.svg](visual-cheatsheet.svg) — компактная схема; [visual-cheatsheet-detailed.svg](visual-cheatsheet-detailed.svg) — подробная схема; [source-findings.md](source-findings.md) — реестр фактов источника.

Отдельного авторского `summary`, review questions или упражнений в PDF 345–349 **нет**; условные `summary.md`, `review-questions.md`, `review-answers.md` не создаются.

**Без изменений:** PDF, RAG, metadata, workflows, `reading/progress.yaml`. **Введение TLS/Basic Auth и генерация файлов — state-changing действия; этот анализ ничего не выполняет.**
