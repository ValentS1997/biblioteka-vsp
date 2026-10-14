# Cheatsheet — глава 19: Alertmanager

**Источник:** PDF 321–343, `p0321:c01`–`p0343:c01`, strict `rag_only`. Ни одна конфигурация/команда не применена; текущая версия и реальные receiver [Needs confirmation].

## Symptom / context / checks

| Симптом | Контекст из источника | Read-only проверка | Интерпретация / next action |
| --- | --- | --- | --- |
| Уведомление ушло не той команде | `route`/nested `routes`; первый match | Пройти `team`, `severity`, `env` по порядку routes (PDF 323–326) | Root fallback применяется при отсутствии дочерних matches; `continue:true` может выбрать несколько routes |
| Одно событие создало сотни сообщений | `group_by` определяет keys | Сравнить `group_by:[region,env,alertname]` и `instance` (PDF 326–327) | Укрупнить группировку по инциденту, не по каждой машине, если уместно |
| Первое уведомление задержалось | `group_wait` | Проверить route-specific interval и время первого firing (PDF 328) | Default из книги 30s; дополнительная задержка **после** решения Prometheus о firing |
| Группа повторно уведомляет при новом alert | `group_interval` | Сопоставить timeline с PDF 328–329 | Default 5m; изменение группы имеет свою частоту; каждый group независимо |
| Проблема остаётся, повторов нет | `repeat_interval` | Проверить интервал и отправки в группе (PDF 329–330) | Default 4h; отправка из-за group_interval сбрасывает отсчёт repeat |
| Отправка безуспешна | Receiver credentials / endpoint | Прочитать routing, name, notifier fields, сверить доступность назначения (PDF 330–333) | Источник не содержит диагностики сетевой/TLS ошибки конкретного SaaS: [Needs confirmation] |
| Оповещение пропало при массовом сбое | `inhibit_rules` | Сверить `source_matchers`, `target_matchers`, `equal` (PDF 340–341) | Не подавлять симптом локально слишком широко, особенно без совпадения region |
| Подавление действует дольше ожидаемого | Silences через UI | Открыть Silences: active/pending/expired, labels, owner/comment (PDF 341–343) | Просмотреть scope, отменить только после согласования; действия state-changing |
| Resolved уведомление пришло без исправления | `send_resolved` | Сверить состояние группы и actual incident (PDF 339–340) | Закрытие alert != закрытие инцидента, нужна проверка человеком |
| Клиентский адрес появился в метках | `email_to` label | Проверить labels alerts и group_by (PDF 338–339) | Это потенциальная утечка приватности, не размещать конфиденциальное в labels |

## Базовые параметры

- **Маршрутизация:** root `route` без matchers как fallback; nested routes проверяются по порядку, матчеры `=`, `!=`, `=~`, `!~`; `continue: true` разрешает дальнейшие совпадения. Настройки группировки/интервалов наследуются от родителей, кроме `continue` (PDF 323–326).
- **Группировка:** `group_by` задаёт ключ по меткам. У `[...]` в PDF 327 специальное значение: отменить группирование между разными alerts; это обычно порождает шум.
- **Интервалы (defaults данного издания):** `group_wait=30s`, `group_interval=5m`, `repeat_interval=4h` (PDF 328–329). Не использовать `repeat_interval` короче `group_interval`.
- **Receiver:** объект с `name` и нулём/несколькими типами notifier; поддержанные по тексту версии 0.24.0: email, PagerDuty, Pushover, Slack, Opsgenie, VictorOps, WeChat, AWS SNS, Telegram, webhook (PDF 330–332).
- **Templates:** `.GroupLabels`, `.CommonLabels`, `.CommonAnnotations`, `.Status`, `.Receiver`, `.GroupKey`, `.Alerts`, `.ExternalURL`. Для alert: `.Labels`, `.Annotations`, `.Status`, `.StartsAt`, `.EndsAt`, `.GeneratorURL` (PDF 334–336). Источник на PDF 340 содержит `.Alert.Firing`/ `.Alert.Resolved` — зафиксировано как несоответствие, **не подтверждать синтаксис молча**.
- **Silences** — временное подавление по labels в UI; **inhibition** — постоянное правило YAML, основанное на активном source alert (PDF 340–343).

## Safe read-only preflight

1. Прочитать `alertmanager.yml` и сверить fallback/root, уникальность имён receivers, наличие всех receiver references. Проверить с `amtool check-config` **до reload**; путь файла подставляется по реальному deployment, источник полного вызова не даёт (PDF 322–323).
2. Проследить route tree по реальному набору labels; проверить `continue:true` только там, где нужна параллельная доставка (PDF 323–326).
3. Для каждого route вычислить group key, наследуемые `group_by` и интервалы, затем сравнить timeline уведомлений (PDF 326–330).
4. Проверить, что примеры SMTP, Slack, Telegram, PagerDuty используют **фиктивные** токены `XXXXXXXX`, а не настоящие секреты. Не публиковать реальные значения, проверить хранение/permissions [Needs confirmation] (PDF 323, 330–332).
5. В шаблонах проверить метки: `GroupLabels` только labels `group_by`, `CommonLabels` — общие по всей группе, а `.Alerts` — все alerts (PDF 334–336).
6. Просмотреть suppression: `inhibit_rules` с `equal:['region']` только подавляет target при соответствующем source; Silences ограничены временем/labels и должны иметь комментарий (PDF 340–343).

## Modifying actions / impacts

- **State-changing:** правка `alertmanager.yml`, `SIGHUP`, POST `/-/reload`, изменение `route`, `receivers`, `inhibit_rules`, `send_resolved`; влияют на доставку уведомлений и могут скрыть инцидент. Source не даёт безопасного универсального rollback: **[Needs confirmation]** (PDF 323–340).
- **State-changing:** создание/отмена/повторное включение Silences в веб-интерфейсе; может выключить уведомления широкого охвата (PDF 341–343).
- **Workload-generating/side effects:** webhook уведомления — HTTP POST и возможные внешние автоматические действия; пример Python пишет alerts на stdout и слушает `:1234`. Автор советует не строить цепь автоматики через Alertmanager для локального перезапуска процесса (PDF 332–333).
- **Privacy:** `email_to` в alert labels раскрывает адрес пользователям Prometheus/Alertmanager, значит доступ к меткам надо оценить заранее (PDF 338–339).

## Verification и rollback

- **Acceptance checks:** контроль выбранного receiver для `severity`/`team`/`env`, отсутствие неожиданного double-route, разумное объединение group_by, timeline относительно group_wait/group_interval/repeat_interval, содержимое шаблона, `resolved` по выбранной политике, ограничения inhibition и Silences.
- **Rollback [Needs confirmation]:** глава описывает reload и UI-отмену Silence, но не полную процедуру rollback неправильного route/receiver/secrets или доставленных уведомлений. До правок нужны владельцы, архив конфигурации и проверенный план отката среды. Ничего не применялось.
