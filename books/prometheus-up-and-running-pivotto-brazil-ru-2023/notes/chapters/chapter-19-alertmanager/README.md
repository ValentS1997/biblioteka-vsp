# Глава 19. Alertmanager

**Книга:** «Запускаем Prometheus. Мониторинг инфраструктуры и приложений» (Жюльен Пивотто, Брайан Бразил; Books.kz, 2023). **Inventory:** `0040`; **book_id:** `prometheus-up-and-running-pivotto-brazil-ru-2023`.  
**Контракт:** `BIBLIOTEKA-VSP-CHAPTER-ARTIFACT-COLLECTION v1.7`. **Статус:** `RAG_GROUNDED` (не `VERIFIED`/`ACCEPTED`).  
**Source policy:** `rag_only`; содержание выведено строго из канонических RAG-чанков, без прямого PDF, веб-поиска и дополнения модельной памятью.

## Границы и provenance

- Глава 19 «Alertmanager» начинается PDF **321** (`p0321:c01`), заканчивается PDF **343** (`p0343:c01`). PDF **344** (`p0344:c01`) открывает часть VI «Развертывание»; PDF **345** (`p0345:c01`) — главу 20.
- **PDF/печатные страницы: 321–343**; `source_locator: pdf_page=321..343`. **23 addressable chunks:** `p0321:c01`–`p0343:c01` в `rag/chunks/p0301-p0400/`.
- Канонический SHA256 PDF: `ab45c7bc9a393b15bc60628dfceaa45db71388fd28e75c5c55ab6eaf5930f787`, `rag/acceptance.yaml: ACCEPTED`, `rag/manifest.yaml: READY_WITH_KNOWN_LIMITATIONS`.
- Версионный контекст главы: **Alertmanager 0.24.0** упоминается в списке интеграций (PDF 330); поддержка отдельных настроек в современной версии [Needs confirmation].

## Карта главы

| Раздел | PDF | Главные объекты |
| --- | --- | --- |
| Конвейер уведомлений | 321–322 | Inhibition, silences, routing, grouping, throttling/repetition, receiver |
| Конфигурация | 322–323 | `alertmanager.yml`, `amtool check-config`, SIGHUP, POST `/-/reload`, global SMTP, `route`, `receivers` |
| Дерево маршрутизации | 323–326 | Root/fallback, `matchers`, `severity`, `team`, `env`, `continue: true`, наследование |
| Группировка | 326–327 | `group_by`, метки `region`/`env`/`alertname`, исключительное `['...']` |
| Регулирование доставки | 328–330 | `group_wait=30s`, `group_interval=5m`, `repeat_interval=4h` (значения по умолчанию в источнике) |
| Приемники | 330–333 | email, PagerDuty, Slack, Telegram, Opsgenie, webhook, null receiver |
| Webhook | 332–333 | HTTP POST JSON; учебный сервер Python 3 `:1234`; `http_config` |
| Шаблоны уведомлений | 333–339 | Go `GroupLabels`, `CommonLabels`, `CommonAnnotations`, `Alerts`, `Status`, `GroupKey`, `SortedPairs`; динамическое `email_to` |
| Resolved | 339–340 | `send_resolved`, firing/resolved alerts, отделение alert от инцидента |
| Inhibition | 340–341 | `inhibit_rules`, `source_matchers`, `target_matchers`, `equal` |
| Web UI и silences | 341–343 | New Silence, Silence, preview, комментарий, срок действия и отмена |

## Основные выводы

1. **Prometheus определяет условия появления alerts, Alertmanager отвечает за уведомления.** Конвейер использует метки для выбора маршрута, группировки, ограничения частоты и получателя. Inhibition подавляет alerts при наличии других, silences временно исключают уведомления (PDF 321–322).
2. **Root route обязателен и действует как fallback.** Дочерние `routes` проверяются по порядку; первый совпавший выбирается, если не задан `continue: true`, разрешающий поиск следующих маршрутов. `matchers`: `=`, `!=`, `=~`, `!~` (RE2 и привязка строки). Дочерние маршруты наследуют настройки родителя, **кроме `continue`**. Root matcher — ошибочная настройка по тексту (PDF 323–326).
3. **`group_by` задаёт гранулярность уведомлений.** Обычно `team`, `region`, `env`, иногда `alertname`; группировка по `instance` может породить сотни сообщений. `['...']` убирает объединение разных alerts, что источник считает нежелательной нормой (PDF 326–327).
4. **Три интервала независимы по смыслу:** `group_wait` откладывает первую отправку (30s); `group_interval` регулирует новые сообщения при изменениях группы (5m); `repeat_interval` повторяет продолжающуюся проблему (4h). Длительности в книге — значения по умолчанию **своего контекста**, не универсальные текущие установки. `repeat_interval < group_interval` не имеет смысла (PDF 328–330).
5. **Receivers могут иметь несколько уведомителей.** `email_configs`, `pagerduty_configs`, `slack_configs`, `opsgenie_configs`, `telegram_configs`, `webhook_configs`; webhook передаёт JSON по POST. `receivers: [{name: null}]` как описанный null receiver отключает доставку, но авторы предпочитают не посылать ненужные alerts вовсе (PDF 330–333).
6. **Notification templates работают с *группой*, а не одним alert.** `GroupLabels` — labels из `group_by`, `CommonLabels` — общие labels всех alerts, `Alerts` — список; `GroupKey` полезен инцидентным системам, `Status` firing/resolved, `ExternalURL` — URL Alertmanager (PDF 333–336). В Go templates применяются `range`, `SortedPairs`, `len`; источник не поддерживает шаблонизацию webhook payload (PDF 333–337).
7. **Тёмные стороны динамического адресата:** метка `email_to` в recording rule/alert, `group_by: [email_to, alertname]`, template `{{ .GroupLabels.email_to }}` позволяет отправлять разным клиентам (PDF 338–339). **Email-адрес в метке доступен пользователям Prometheus и Alertmanager**, может раскрыть персональные данные; не внедрять без оценки приватности.
8. **Resolved alert не равен закрытому инциденту.** `send_resolved` может увеличить объём уведомлений, а исчезновение alert не доказывает устранение первопричины (PDF 339–340).
9. **Inhibition — для крупных зависимых сбоев**, например region-wide failure suppress severity=page для того же region. Авторы предостерегают от чрезмерных правил. Silences — временный механизм UI с метками, владельцем, комментарием и предварительным просмотром; ежедневное расписание через silences не рекомендовано (PDF 340–343).

## Source limitations и риски

- **PDF 323:** текст RAG сливает сноски `❶`/`❷` с `smtp_from`, `route` и полем получателя — этот кусок **невалиден как YAML без нормализации маркеров**. В [commands.md](commands.md) исходный фрагмент сохранён как недоверенный, а рабочий-схематический пример явно обозначен как очищенный от издательской разметки.
- **PDF 325:** вложенные `routes:` извлечены с потенциально неоднозначным отступом. Нельзя выдавать блок за проверенную конфигурацию без `amtool check-config`.
- **PDF 337:** в прозе `dashbord`, в template `.Annotations.dashboard`.
- **PDF 339:** рядом с `receiver: customer_email` находится сноска `❶`, не часть YAML.
- **PDF 340:** текст `.Alert.Firing`/`.Alert.Resolved` рядом с ранее описанным списком `.Alerts` требует проверки точного синтаксиса шаблона; исходный вариант не исправляется молча.
- **PDF 334, 337, 341–343:** рисунки 19.1–19.5 в RAG присутствуют как подписи/текст, не как исходные картинки. Все схемы здесь самостоятельные и текстово обоснованные.
- **Секреты** в шаблонах source (`service_key: XXXXXXXX`, `bot_token: XXX`, Slack `XXXXXXXX`) — фиктивные примеры; не заполнять реальными токенами в документации или коммитах.
- Все находки с точными locators: [source-findings.md](source-findings.md).
- Нет отдельного формального раздела заключительного summary либо набора review questions/exercises на PDF 321–343; `summary.md`, `review-questions.md`, `review-answers.md` не создаются.

## Артефакты

[cheatsheet.md](cheatsheet.md) · [commands.md](commands.md) · [diagram.md](diagram.md) · [visual-cheatsheet.svg](visual-cheatsheet.svg) · [visual-cheatsheet-detailed.svg](visual-cheatsheet-detailed.svg) · [source-findings.md](source-findings.md).

**Не изменяются:** canonical PDF, RAG, metadata, CI workflows, reading/progress.
