# Source findings — глава 19 «Alertmanager»

**Provenance:** канонический RAG `p0321:c01`–`p0343:c01`, PDF 321–343, source SHA256 `ab45c7bc9a393b15bc60628dfceaa45db71388fd28e75c5c55ab6eaf5930f787`. `rag_only`; по внешним знаниям дефекты не исправляются. Причина и степень вины OCR/типографии без прямого PDF [Needs confirmation].

## F-01 — [Source extraction issue]: слипшийся минимальный YAML SMTP

- **RAG `p0323:c01`:** `smtp_from: 'yourprometheus@example.org'                    ❶route:` и `- to: 'youraddress@example.org'                  ❷  Адрес электронной почты для поля От`.
- **Результат:** издательские сноски `❶/❷` и пояснения стали частью text chunk около YAML; буквальный блок **нельзя считать валидным `alertmanager.yml`**.
- **Действие:** в [commands.md](commands.md) описана буквальная corruption и отдельно приведена **явно нормализованная учебная схема**, без притязания на verified runnable конфигурацию; оригинальный RAG неизменён.

## F-02 — [Source extraction issue / Needs confirmation]: вложенность routes на PDF 325

- **RAG `p0325:c01`:** после `- matchers: team=frontend` и `receiver: frontend-pager` встречается `routes:` с отступом, неочевидно относящимся к этому же объекту, затем вложенные severity cases.
- **Источник объясняет:** дочерние `severity=page/ticket` предназначены для frontend; аналогичные — для backend, включая `env=dev` (PDF 325).
- **Ограничение:** корректный YAML nesting без проверки `amtool check-config` нельзя утверждать. В commands закреплён intent, а не перенесён некритично исходный блок.

## F-03 — [Source wording mismatch]: `.Alerts` vs `.Alert.Firing`/`.Alert.Resolved`

- **RAG `p0335:c01`:** `Alerts` — список alert objects, имеющих `Labels`, `Annotations`, `Status`, `StartsAt`, `EndsAt`.
- **RAG `p0340:c01`:** говорится, что для списков активных и устранённых alerts удобны `.Alert.Firing` и `.Alert.Resolved` (singular).
- **Несогласованность:** plural `.Alerts` уже используется ранее и в template PDF 336. Конкретное правильное название accessor для версии Alertmanager отдельно **не верифицировано**, поэтому буквальный `.Alert.Firing` не представлен здесь как рабочий шаблон.

## F-04 — [Source wording mismatch]: `dashbord` и `dashboard`

- **RAG `p0336:c01`:** template `{{ if ne .Annotations.dashboard "" -}}`.
- **RAG `p0337:c01`:** в объяснении «если присутствует аннотация dashbord».
- **Действие:** это расхождение обозначений, сохраняем исходный шаблон `dashboard`, не придумываем вторую аннотацию.

## F-05 — [Source extraction issue / sensitive data]: recipient marker и label email_to

- **RAG `p0339:c01`:** `receiver: customer_email                ❶` и сноска, поясняющая необходимость `group_by` включать `email_to`.
- **RAG `p0338:c01`–`p0339:c01`:** адреса `foo@example.com`/`bar@example.com` экспортируются в label `email_to` для персонализированной маршрутизации. Источник прямо предупреждает, что адреса доступны всем, кто может читать Prometheus/Alertmanager.
- **Действие:** сноску удалить лишь из явно нормализованного примера с зафиксированным отклонением; никакие реальные recipient addresses/tokens не публиковать.

## F-06 — [Source version scope]: интеграции, ключи, идентификаторы

- **RAG `p0330:c01`:** перечень уведомителей сформулирован для **Alertmanager 0.24.0**.
- **RAG `p0330:c01`–`p0332:c01`:** используются исторические `pagerduty_configs.service_key`, `slack_configs.api_url`, `global.victorops_api_key`, `opsgenie_configs`, `telegram_configs`, `webhook_configs`. Ключи вида `XXXXXXXX`, `XXX`, `YYY`, `XXXX-XXXX` — учебные placeholders.
- **Ограничение:** compatibility с текущей версией, secret management, маршруты SaaS и аутентификация не проверены; не использовать как копипасту для production.

## F-07 — [Source semantics caution]: resolved ≠ remediation

- **RAG `p0339:c01`–`p0340:c01`:** `send_resolved=true` может посылать notification с resolved alerts; удаление alert может быть связано даже с падением системы мониторинга.
- **Ограничение:** это принципиальное различие между завершением alert и закрытием инцидента; нельзя использовать сигнал `resolved` для автоматического завершения тикета без отдельного подтверждения.
- **RAG `p0340:c01`:** в source также предупреждается о потенциальном удвоении объёма уведомлений email/Slack при `send_resolved`.

## F-08 — [Source semantics caution]: suppression scope и аварийные уведомления

- **RAG `p0340:c01`:** `inhibit_rules` с `source_matchers: severity=page-regionfail`, `target_matchers: severity=page`, `equal:['region']`; источник не рекомендует пересечение source/target матчеров.
- **RAG `p0341:c01`:** Inhibition желательно ограничивать крупными связанными отказами, а не строить сложные цепочки для каждого симптома.
- **RAG `p0341:c01`–`p0343:c01`:** создание Silence через веб-интерфейс обязательно сопровождается проверкой scope и комментарием, с отменой в Silences.
- **Риск:** неверная маршрутизация, inhibition или широкий Silence способны скрыть критическую информацию. Конкретный rollback и approval flow в книге отсутствуют.

## F-09 — [Source image limitation]: рис. 19.1–19.5

- **RAG `p0334:c01`** — скриншот Slack 19.1; **`p0337:c01`** — 19.2; **`p0341:c01`–`p0343:c01`** — Alertmanager UI/Silences 19.3–19.5.
- PDF-иллюстрации не предоставлены как изображения в текстовом RAG. Визуальные артефакты являются **схемами по тексту**, без утверждения об идентичности исходным скриншотам.

## F-10 — [Needs confirmation]: операционные процедуры и групповые defaults

- **RAG `p0323:c01`:** `amtool check-config`, SIGHUP и `POST /-/reload` указаны без конкретных аргументов/аутентификации.
- **RAG `p0328:c01`–`p0329:c01`:** defaults `group_wait=30s`, `group_interval=5m`, `repeat_interval=4h` относятся к версии книги, не доказаны для deployment пользователя.
- **Действие:** до применения нужна отдельная проверка текущего файла, прав, адресов, реальной команды, времени, корректности регулярных выражений, test routing и плана отката. Никаких реальных запросов к Alertmanager не выполнялось.

Все findings строго локализованы на уровне исходного RAG; не изменяют PDF, метрики чтения или другие главы.
