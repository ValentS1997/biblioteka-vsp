# Глава 10. Расширение функциональности Zabbix с помощью пользовательских скриптов и API

**Книга:** «Zabbix 7: мониторинг ИТ-инфраструктуры», обновлённое русское третье издание (2025); inventory **0020**; book ID `zabbix-7-monitoring-it-infrastructure-ru`.

## Источник / provenance / границы

- **RAG-only**: принятый книжный корпус `rag/acceptance.yaml: ACCEPTED`. Ни прямого доступа к PDF, ни внешнего доступа к репозиториям Python-скриптов и документации Zabbix, ни восстановления команд по памяти модели.
- **PDF 412–433 включительно**; RAG chunks `zabbix-7-monitoring-it-infrastructure-ru:p0412:c01` … `zabbix-7-monitoring-it-infrastructure-ru:p0433:c01`. [Начало главы](../../../rag/chunks/p0401-p0500/p0412-c01.md), [глава 11](../../../rag/chunks/p0401-p0500/p0434-c01.md).
- Source SHA256: `07204d885d4bf4c6c2de7c71ae42a4e3ed4cea794169cbe07985552e63875a27`; generation `6a5221f8e8a0f88b400905d7334879edff6f5451d9ab7f6e56bb203809018986`.
- Точные поля веб-форм, скриптов `api_test.py`, `host_pull_zabbix.py`, `enable_disable-host.py`, картинки 10.1–10.24, не вошедшие в RAG-текст, помечены **`RAG_MISS`**. Внешний код книги и сторонних авторов не загружался и не исполнялся.

## Карта главы

| Раздел | PDF страницы | Содержание |
|---|---:|---|
| [Настройка API-токенов и управление ими](../../../rag/chunks/p0401-p0500/p0413-c01.md) | 413–417 | `API Users`, permissions на host/template, API user, `Users → API tokens`, token expiry/role |
| [Использование API для расширения функциональности](../../../rag/chunks/p0401-p0500/p0418-c01.md) | 418–422 | Python 3 + `requests`, JSON-RPC `host.get`, `selectInterfaces`, сохранение host→IP в текстовый файл |
| [Создание jumphost с помощью API Zabbix и Python](../../../rag/chunks/p0401-p0500/p0422-c01.md) | 422–427 | Внешний `host_pull_zabbix.py`, генерация `/etc/hosts` и SSH по именам, обновление каждые 15 минут |
| [Активация и деактивация узла сети из интерфейса карты сетей](../../../rag/chunks/p0401-p0500/p0427-c01.md) | 427–433 | Сторонний `enable_disable-host.py`, Zabbix `Alerts → Scripts`, `Monitoring → Maps`, `Host/Enable`/`Host/Disable`, `{MANUALINPUT}` |

## 1. API-токен должен наследовать только необходимые права

Книга создаёт группу `API Users`, выдаёт права `Read-write` на выбранные host и template groups, затем пользователя `API` и токен `API book key`. В **учебном** рецепте API user получает роль **Super admin**, а для `Expires` предлагается далёкое будущее/отключение срока. Однако тот же источник рекомендует **ограничивать** host/template permissions и назначать API-токенам разумную дату истечения ([p0413](../../../rag/chunks/p0401-p0500/p0413-c01.md)–[p0417](../../../rag/chunks/p0401-p0500/p0417-c01.md)).

Токен связан с конкретным пользователем и действует в пределах его effective permissions. Его следует сохранять в секретном хранилище; буквальный токен, показанный в книге на страницах 419, 424 и 429, здесь **не повторяется**. API endpoint из книги использует `http://<ZABBIX_SERVER>/api_jsonrpc.php` — это **источниковый учебный URL, а не рекомендация отключать TLS**.

## 2. Пример чтения API: host.get и запись результатов

Книга устанавливает Python 3, `python3-pip`, `requests`, загружает `api_test.py`, затем добавляет функции **`get_hosts(api_token, url)`** и **`generate_host_file(hosts, host_file)`**. В JSON-RPC payload: `jsonrpc: "2.0"`, `method: "host.get"`, `params.output: ["hostid","host"]`, `params.selectInterfaces: ["interfaceid","ip","main"]`, `id:2`, `auth:api_token`. Метод отправляется через `requests.post(..., json=payload)`; второй проход выбирает `interfaces` с `main == "1"` и пишет строки `<hostname> <IP>` ([p0418](../../../rag/chunks/p0401-p0500/p0418-c01.md)–[p0422](../../../rag/chunks/p0401-p0500/p0422-c01.md)).

Это **read of Zabbix object model** через API, но файл результатов — **локальный state-changing**. Проверка по примеру: `python3 api_test.py`, затем `cat /home/zabbix/results`. В пояснении p422 итоговый файл назван `/home/results`; обе версии сохранены в [source-findings.md](source-findings.md), не исправлены незаметно.

**Нельзя признать готовой самостоятельную исполнимую программу**: начальная часть `api_test.py` и точный порядок вызовов/целевой файл находятся во внешнем коде, который RAG-only не содержит. Текстовые вставки функций приведены частично и зависят от скачанного файла.

## 3. Jumphost из перечня Zabbix-хостов: удобство и разрушительный риск

Скрипт `host_pull_zabbix.py` (автор Ядвир Сингх, ссылка в книге на сторонний репозиторий) вызывает API, собирает host/IP и записывает **`/etc/hosts`**. Автор прямо предупреждает, что **каждый запуск перезаписывает файл целиком**, и требует **пустой лабораторный host без пользовательских изменений /etc/hosts** ([p0423](../../../rag/chunks/p0401-p0500/p0423-c01.md)). После работы книги предлагают `cat /etc/hosts`, `ssh lar-book-agent_passive` и `crontab -e` с периодом `*/15 * * * *` для регулярного обновления ([p0424](../../../rag/chunks/p0401-p0500/p0424-c01.md)–[p0427](../../../rag/chunks/p0401-p0500/p0427-c01.md)).

**Не применять такой скрипт к рабочему bastion host**: можно разрушить локальное сопоставление важных имён, повредить доступность служб и вновь перезаписывать данные по cron. Путь в учебной строке cron `/home/host_pull_zabbix.py` не установлен предыдущими шагами — `[Needs confirmation]`. Скрипт извне не проверен.

## 4. Интерактивная карта → привилегированный Python-скрипт

Рецепт загружает архив `zabbix-toggle-hosts-from-frontend v2.0`, распаковывает и размещает `enable_disable-host.py` в `/etc/zabbix/frontendscripts`, устанавливает Python/requests, меняет `url` и `token`. В `Alerts → Scripts` создаёт **две** команды `Host/Enable` и `Host/Disable`, доступные через меню объекта на `Monitoring → Maps` ([p0427](../../../rag/chunks/p0401-p0500/p0427-c01.md)–[p0431](../../../rag/chunks/p0401-p0500/p0431-c01.md)). Точные `Commands` из рисунков 10.18–10.19 = `RAG_MISS`.

В тексте p431 пользователь с ролью **User** способен запустить кнопку, потому что скрипт действует **от имени другого пользователя с повышенными правами**. При этом пояснение говорит о создании maintenance period, тогда как UI verification сообщает статус host `Disabled`. Это **различные управленческие эффекты**; без исходного скрипта невозможно верифицировать точную операцию: см. [source-findings.md](source-findings.md).

Дополнение Zabbix 7: замена `{HOST.HOST}` на **`{MANUALINPUT}`** в `Commands` и `Advanced configuration` с `Input prompt`, `Default input string`, `Input validation rule` позволяет вводить имя цели вручную ([p0432](../../../rag/chunks/p0401-p0500/p0432-c01.md)–[p0433](../../../rag/chunks/p0401-p0500/p0433-c01.md)). Это **расширение поверхности полномочий**: необходимо отдельно валидировать input и ограничить группу пользователей/разрешённые hosts. Полное правило validation со скриншота = `RAG_MISS`.

## Безопасный операционный вывод

1. Для обучения сначала создать API-пользователя с **ограниченными** host/template permissions и сроком действия токена; записать секрет в vault.
2. Проверить `host.get` на небольшом наборе host, не публикуя auth token; отличать API-read от локальной записи файла.
3. Jumphost пример изучать **без запуска на рабочем /etc/hosts**; документировать источник адресов, исключения, резервную копию, атомарное обновление и rollback отдельно (`[Needs confirmation]`).
4. UI script из `Monitoring → Maps` рассматривать как **делегирование привилегированной операции**, не просто визуальный shortcut. Не включать его без source code review и проверки ролей, approval/логирования и rollback.
5. Сверять утверждения об успехе по реальным host state, поддерживаемым source, а не только по клику `Execute`.

## Артефакты

[Cheatsheet](cheatsheet.md) · [Commands/UI](commands.md) · [Mermaid](diagram.md) · [Компактная SVG](visual-cheatsheet.svg) · [Подробная SVG](visual-cheatsheet-detailed.svg) · [Source findings](source-findings.md).

**Условные материалы:** страница 433 заканчивается пояснениями и ссылкой на исходники, p434 начинает главу 11; явного раздела `summary`, `review questions` или ответов в конце главы 10 нет. `summary.md`/`review-questions.md`/`review-answers.md` не создаются.

**Статус чтения не меняется.** Контракты: router v1.2, recovery v1.0, chapter analysis v1.4, artifact collection v1.8, publication v1.0.
