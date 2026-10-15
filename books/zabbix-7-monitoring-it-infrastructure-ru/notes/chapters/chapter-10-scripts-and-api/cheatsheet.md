# Глава 10 — cheatsheet: Zabbix API, jumphost, scripts

**Источник:** accepted RAG PDF **412–433**. [Граница и provenance](README.md). **Не исполнять сторонний скрипт без review и согласованного rollback.**

## Symptom / problem framing

| Симптом | Первый диагностический вопрос | RAG |
|---|---|---|
| API `host.get` возвращает ошибку | Корректны URL `api_jsonrpc.php`, токен пользователя, его права на host/template groups, Python/requests? | [p0417](../../../rag/chunks/p0401-p0500/p0417-c01.md)–[p0421](../../../rag/chunks/p0401-p0500/p0421-c01.md) |
| `host.get` успешен, но файла нет | Запускается ли внешняя точка входа `api_test.py`, вызваны ли обе функции, какой реальный output path? p421 и p422 дают **разные пути** | [p0420](../../../rag/chunks/p0401-p0500/p0420-c01.md)–[p0422](../../../rag/chunks/p0401-p0500/p0422-c01.md) |
| В output нет IP | `selectInterfaces` возвращает `interfaces` и поле `main = "1"`; у host есть main interface? | [p0420](../../../rag/chunks/p0401-p0500/p0420-c01.md) |
| После jumphost-скрипта изменилось разрешение имён | Не перезаписан ли целиком `/etc/hosts`, был ли backup? Периодическая cron-задача не перезаписывает ли снова | [p0423](../../../rag/chunks/p0401-p0500/p0423-c01.md)–[p0426](../../../rag/chunks/p0401-p0500/p0426-c01.md) |
| Jumphost перестал обновляться | Соответствует ли фактический путь скрипта `/home/host_pull_zabbix.py` из cron? В репозитории скрипт отсутствует | [p0424](../../../rag/chunks/p0401-p0500/p0424-c01.md), [p0426](../../../rag/chunks/p0401-p0500/p0426-c01.md) |
| На карте нет Host/Enable/Host/Disable | Созданы ли оба `Alerts → Scripts`, задан ли scope и корректны ли команды из внешнего файла, host map доступен? | [p0428](../../../rag/chunks/p0401-p0500/p0428-c01.md)–[p0431](../../../rag/chunks/p0401-p0500/p0431-c01.md) |
| User может менять состояние хоста, несмотря на низкие права | Скрипт запускается от **другого повышенного пользователя**; определить effective rights и целевой host | [p0431](../../../rag/chunks/p0401-p0500/p0431-c01.md)–[p0432](../../../rag/chunks/p0401-p0500/p0432-c01.md) |
| Manual input действует на неожиданный host | Настроены ли `{MANUALINPUT}` и `Input validation rule`; точная форма только на рисунке 10.23 (`RAG_MISS`) | [p0432](../../../rag/chunks/p0401-p0500/p0432-c01.md) |

## Baseline / context

Для главы нужны Zabbix 7, пользователь/API token, второй Linux host с Python 3/`requests`, для jumphost — **отдельная чистая лабораторная Linux VM**, не производственный bastion. Для scripts-on-map — Zabbix server и сторонний проект `zabbix-toggle-hosts-from-frontend`; его код **не входит** в принятый RAG ([p0412](../../../rag/chunks/p0401-p0500/p0412-c01.md), [p0418](../../../rag/chunks/p0401-p0500/p0418-c01.md), [p0423](../../../rag/chunks/p0401-p0500/p0423-c01.md), [p0428](../../../rag/chunks/p0401-p0500/p0428-c01.md)).

## Read-only checks

- `Users → API tokens`: имя, owner, expiry; `Users → Users / User groups`: role и host/template permissions. **Не копировать токен в отчёт**, даже если интерфейс показывает его при создании ([p0413](../../../rag/chunks/p0401-p0500/p0413-c01.md)–[p0417](../../../rag/chunks/p0401-p0500/p0417-c01.md)).
- Читать `api_test.py` и downloaded `host_pull_zabbix.py` перед запуском (**Read-only**, внешние файлы в данном RAG не проверены). Сопоставить переменные, target path и программу entrypoint.
- Проверить сохранённую информацию из **учебного** `/home/zabbix/results` через `cat` (**Read-only**) **только после** безопасного запуска в лаборатории; альтернатива `/home/results` в тексте — source discrepancy ([p0421](../../../rag/chunks/p0401-p0500/p0421-c01.md)–[p0422](../../../rag/chunks/p0401-p0500/p0422-c01.md)).
- `cat /etc/hosts` (**Read-only**) и `grep agent` после лабораторного теста; **не запускать запись** как способ проверки живого bastion ([p0425](../../../rag/chunks/p0401-p0500/p0425-c01.md)–[p0426](../../../rag/chunks/p0401-p0500/p0426-c01.md)).
- `Monitoring → Maps` и `Monitoring → Hosts` (**Read-only** при просмотре): найти Host/Enable, Host/Disable и фактический Status. Нажатие **Execute — State-changing** ([p0429](../../../rag/chunks/p0401-p0500/p0429-c01.md)–[p0431](../../../rag/chunks/p0401-p0500/p0431-c01.md)).

## Interpretation

- **`host.get`**: JSON-RPC `method=host.get`, `output: hostid,host`, `selectInterfaces: interfaceid,ip,main`. Python выбирает `main == "1"` и готовит hostname/IP. Запрос **не изменяет** объекты Zabbix, но порождает API-трафик ([p0420](../../../rag/chunks/p0401-p0500/p0420-c01.md)–[p0422](../../../rag/chunks/p0401-p0500/p0422-c01.md)).
- **API token** — средство аутентификации *и* связанная с ним user identity/permissions; роль Super admin и expiry disabled в книге — учебный shortcut, источник сам рекомендует ограничение ([p0414](../../../rag/chunks/p0401-p0500/p0414-c01.md)–[p0417](../../../rag/chunks/p0401-p0500/p0417-c01.md)).
- **Jumphost**: API-read превращается в **system-file overwrite**; cron через 15 минут повторяет эффект. Удалённый inventory не проверяет пригодность имени, локальные строки или безопасность DNS/SSH ([p0423](../../../rag/chunks/p0401-p0500/p0423-c01.md)–[p0427](../../../rag/chunks/p0401-p0500/p0427-c01.md)).
- **Map commands**: пользователь уровня User может инициировать изменение через скрипт с более высокой привилегией. Пояснение p431 одновременно говорит о `Disabled` host и создании maintenance period — подтверждение точного эффекта требует проверки кода [source-findings.md](source-findings.md).

## Next action

Сначала разграничить **API authorization → read-only JSON-RPC request → локальная запись файла → privileged action**. Не диагностировать неработающий `host.get` путём выдачи Super admin. Проверить user role, доступ к конкретным host, endpoint и error response, не раскрывая `auth`.

## Modifying action

- `Users → API tokens → Create API token` и изменение группы/пользователя — **State-changing, security-sensitive**; проверить expiry и scope, rollback токена из текста `[Needs confirmation]`.
- `pip3 install requests`, `dnf/apt install python3` — **State-changing**, внешний пакет; установка только в контролируемой среде.
- `python3 api_test.py` — **Workload-generating/API-read + file-write**, результат и права локального output path проверить.
- `python3 host_pull_zabbix.py` и `crontab -e` — **State-changing / destructive** для `/etc/hosts`; до запуска нужен backup, исключения и гарантия восстановления, не данная в книге.
- `Alerts → Scripts → Host/Enable / Host/Disable`, затем `Monitoring → Maps → Execute` — **State-changing / privilege-sensitive**, может менять доступность мониторинга. Полный внешний Python code и Commands fields = `RAG_MISS`.

## Verification / acceptance checks

1. API user без лишних host/template permissions, token expiry установлен; auth token хранится вне Git/скриншотов.
2. В лаборатории `host.get` возвращает ожидаемые hostid/host и primary IP; файл results не переписывает системные пути.
3. Любой тест jumphost проводится на **изолированной чистой VM**; исходный `/etc/hosts` под контролем и есть проверенный restore.
4. `Host/Enable`/`Host/Disable` доступны только утверждённым пользователям; операцию запускает ожидаемый privileged account; target ограничен и подтверждён.
5. Проверено фактическое изменение статуса и отсутствие непредусмотренного maintenance; `{MANUALINPUT}` валидируется, не расширяя несанкционированно scope.

## Rollback

В RAG отсутствуют: полный revoke/rotation plan для токенов, безопасное восстановление перезаписанного `/etc/hosts`, откат повторяющейся cron-перезаписи, возврат по ошибке привилегированного API enable/disable и полная процедура для удалённых файлов/пакетов. Все **`[Needs confirmation]`**. Не объявлять реставрацию возможной без резервной копии. Несогласованности сохранены в [source-findings.md](source-findings.md).
