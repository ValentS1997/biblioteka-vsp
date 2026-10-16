# Глава 11. Поддержка и обслуживание Zabbix

**Книга:** «Zabbix 7: мониторинг ИТ-инфраструктуры», третье обновлённое русское издание (2025). Инвентарный номер **0020**; book ID `zabbix-7-monitoring-it-infrastructure-ru`.

## Проверенная provenance

- **RAG-only**: информация из принятого книжного корпуса `rag/acceptance.yaml: ACCEPTED`, не из прямого доступа к PDF, внешних URL или памяти модели.
- Глава **PDF 434–464 включительно**, chunks `zabbix-7-monitoring-it-infrastructure-ru:p0434:c01` … `zabbix-7-monitoring-it-infrastructure-ru:p0464:c01`. [Первая страница](../../../rag/chunks/p0401-p0500/p0434-c01.md); [глава 12 начинается на p0465](../../../rag/chunks/p0401-p0500/p0465-c01.md).
- Source SHA256 `07204d885d4bf4c6c2de7c71ae42a4e3ed4cea794169cbe07985552e63875a27`; corpus generation `6a5221f8e8a0f88b400905d7334879edff6f5451d9ab7f6e56bb203809018986`.
- Скриншоты форм и диагностических графиков 11.1–11.22 не извлечены как отдельные структурированные значения. Недостающие поля обозначены `RAG_MISS`.

## Карта разделов главы

| Раздел | Страницы PDF | Главное |
|---|---:|---|
| [Настройка периодов обслуживания](../../../rag/chunks/p0401-p0500/p0435-c01.md) | 435–437 | `Data collection → Maintenance`, тип обслуживания, Active since/till, Periods, Host groups, подавление операций |
| [Резервное копирование Zabbix](../../../rag/chunks/p0401-p0500/p0438-c01.md) | 438–441 | `/etc/zabbix`, NGINX/Apache, PHP-файлы, библиотеки, MySQL/MariaDB `mysqldump`, PostgreSQL `pg_dump`, cron, retention |
| [Обновление PHP до 8.2 или новее](../../../rag/chunks/p0401-p0500/p0442-c01.md) | 442–445 | RHEL8 AppStream PHP 8.2/REMI PHP 8.3; Ubuntu PPA PHP 8.3; проверки версий |
| [Обновление СУБД MariaDB](../../../rag/chunks/p0401-p0500/p0445-c01.md) | 445–450 | Предусловия и backup; источник показывает MariaDB 11.4 LTS, RHEL/Ubuntu команды остановки/обновления |
| [Обновление Zabbix](../../../rag/chunks/p0401-p0500/p0450-c01.md) | 450–454 | Переход 6.0→7.0, последовательность, пакеты, сохранение конфигураций, логи, UI |
| [Оптимизация производительности](../../../rag/chunks/p0401-p0500/p0455-c01.md) | 455–464 | `StartDiscoverers`, `HousekeepingFrequency`, `MaxHousekeeperDelete`, MySQLTuner, очередь процессов, асинхронные pollers |

## Главные выводы и безопасные границы

**Maintenance windows.** Повторяющееся окно на учебных Linux servers в книге: **вторник 22:00–04:00**, интервал активности в примере кончается **31 декабря 2023 г.** ([p0437](../../../rag/chunks/p0401-p0500/p0437-c01.md)). **`With data collection`** — продолжать сбор, подавлять оповещения только если у action включено **`Pause operations for suppressed problems`**. Источник далее пишет, что для прекращения сбора следует выбрать «With data collection» второй раз; это внутреннее расхождение, нельзя считать строку проверенной инструкцией для выключения сбора. `nodata` не срабатывает во время обоих режимов по тексту ([source-findings.md](source-findings.md)).

**Backup перед изменениями.** Zabbix состоит из server config, frontend/web server + PHP, library files и базы; достаточность резервной копии требует проверки каждого компонента и **успешного восстановления**, а не только команды копирования. Книга создаёт `/opt/zbx-backup`, копирует `/etc/zabbix`, `/etc/nginx`, `/usr/share/zabbix`, `/usr/share/doc/zabbix-*`, `/usr/lib/zabbix`, а затем делает дамп DB `mysqldump --single-transaction` или `pg_dump` ([p0438](../../../rag/chunks/p0401-p0500/p0438-c01.md)–[p0441](../../../rag/chunks/p0401-p0500/p0441-c01.md)). Автор предпочитает хранить backups на другом разделе/машине, а не полагаться только на `/opt`. Примеры cron содержат опечатки путей и небезопасные inline passwords; команды **не являются** готовым production расписанием.

**PHP и MariaDB.** В рамках **издания** Zabbix 7 требует PHP **8.0+**, MariaDB **10.5+**; рецепты обновляют PHP до **8.2/8.3**, MariaDB до **11.4** и Zabbix 6.0 до **7.0** ([p0442](../../../rag/chunks/p0401-p0500/p0442-c01.md)–[p0454](../../../rag/chunks/p0401-p0500/p0454-c01.md)). Это **версионный контекст учебной книги**, не проверенные на текущую дату требования или работающие ссылки репозиториев. `AllowUnsupportedDBVersions=1` в [p0450](../../../rag/chunks/p0401-p0500/p0450-c01.md) описан как **не рекомендуемый** обход проверки версии. Рецепт `curl ... | sudo bash` передаёт скрипт напрямую оболочке; требуется отдельное подтверждение репозитория, подписей, совместимости, окон и rollback.

**Порядок обновления.** Задокументировать исходные версии `zabbix_server --version`, `php-fpm --version`, `mariadb --version` и целевой набор пакетов; сделать backups/снапшоты; обновить PHP/DB в контролируемых окнах **до** Zabbix 7; остановить и обновить server/agent/frontend; сохранить `zabbix_server.conf`; проверить `systemctl status zabbix-server`, `/var/log/zabbix/zabbix_server.log`, web UI и реальные items/alerts. При сбое не продолжать необдуманные рестарты/обновления. Полный корректный rollback схемы DB **не описан** ([p0450](../../../rag/chunks/p0401-p0500/p0450-c01.md)–[p0454](../../../rag/chunks/p0401-p0500/p0454-c01.md)).

**Оптимизация процессов.** В учебном примере Discovery workers почти постоянно загружены на **100%**; `StartDiscoverers=2` добавляет процесс и уменьшает ожидание нескольких независимых LLD rules, но повышает потребление CPU/RAM/DB-connections ([p0455](../../../rag/chunks/p0401-p0500/p0455-c01.md)–[p0462](../../../rag/chunks/p0401-p0500/p0462-c01.md)). `HousekeepingFrequency=2` и `MaxHousekeeperDelete=20000` — пример настройки housekeeping, автор сам предупреждает: увеличение интервала **не решает** главную проблему, только позволяет выиграть время до работ ([p0458](../../../rag/chunks/p0401-p0500/p0458-c01.md)–[p0463](../../../rag/chunks/p0401-p0500/p0463-c01.md)). В будущем для больших БД рассматриваются partitioning/TimescaleDB (следующая глава).

**MySQLTuner**: `mysqltuner.pl` предлагает переменные в секции `Variables to adjust`, но их **нельзя применять автоматически** без изучения ([p0459](../../../rag/chunks/p0401-p0500/p0459-c01.md)–[p0463](../../../rag/chunks/p0401-p0500/p0463-c01.md)). Zabbix 7 также описан с асинхронными pollers Agent, HTTP Agent и SNMP walk/get: **до 1000 проверок на poller** при конфигурации `MaxConcurrentChecksPerPoller` ([p0464](../../../rag/chunks/p0401-p0500/p0464-c01.md)), не все старые правила линейного масштабирования применимы.

## Практический порядок изучения

1. Подтвердить actual versions/health и выбранные host groups, настроить нужное окно Maintenance, проверить checkbox подавления операций.
2. Сделать независимые backups конфигурации, frontend и DB; проверить наличие файлов, права, место, копирование off-host и **restore test** (последнее — критерий приёмки, а не выполненное действие книги).
3. Сверить целевой PHP, DB и Zabbix со средой и release notes, спланировать отдельные maintenance windows; не запускать исторические `dnf/apt/curl|` рецепты напрямую на работающей системе.
4. Провести изолированное обновление в разрешённом окне; проверять здоровье/логи до следующей стадии.
5. Исследовать Utilization discovery workers и housekeeping, отличать дефицит процессов от плохой конфигурации и от проблемы хранения/удаления history.
6. Планировать партиционирование/TimescaleDB по росту данных, а tuning MySQL выполнять только после оценки альтернатив и изменения одних параметров за раз.

## Артефакты

[Cheatsheet](cheatsheet.md) · [Команды/UI](commands.md) · [Mermaid](diagram.md) · [Компактная SVG](visual-cheatsheet.svg) · [Подробная SVG](visual-cheatsheet-detailed.svg) · [Source findings](source-findings.md).

**Ограничения:** в источнике нет полного восстановления после неудачного PHP/MariaDB/Zabbix upgrade, отдельного подтверждённого restoration runbook, требований безопасного хранения DB-пароля и верифицированных на текущую дату repo URLs. Для них `[Needs confirmation]`. В конце [p0464](../../../rag/chunks/p0401-p0500/p0464-c01.md) нет отдельного chapter-end summary/review questions; условные файлы `summary.md`, `review-questions.md`, `review-answers.md` не создаются. **Статус чтения не изменяется.**

Процесс: router v1.2, recovery v1.0, chapter-analysis-request v1.4, chapter-artifact-collection v1.8, publication v1.0.
