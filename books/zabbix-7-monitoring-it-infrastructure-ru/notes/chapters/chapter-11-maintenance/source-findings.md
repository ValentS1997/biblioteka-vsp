# Глава 11 — source findings и риски

**RAG-only**, PDF 434–464. Здесь сохраняются **исходниковые варианты**, ошибки и ограничения; не исправлять бесследно, не переносить учебные команды в рабочую среду без верификации.

## 1. [Source contradiction] With vs No data collection

- **Вариант A:** [p0437](../../../rag/chunks/p0401-p0500/p0437-c01.md) вводит две опции `With data collection` и `No data collection`, прямо говорит, что `With data collection` продолжает сбор и подавляет оповещения при `Pause operations for suppressed problems`.
- **Вариант B:** затем та же страница пишет, что **для прекращения сбора данных следует выбрать `With data collection`**, т.е. повторяет имя режима с противоположным эффектом.
- `nodata` по тексту не срабатывает в обоих режимах.
- **Следствие:** выбор фактического режима и эффективное подавление проверить в целевой версии. Не пересказывать вариант B как надёжную процедуру.

## 2. [Source code mismatch] Пути и переносы в cron архивов

- **Вариант A:** при `mkdir` созданы `/opt/zbx-backup/nginx`, `.../zbx-config`, `.../lib` и `.../shared` ([p0438](../../../rag/chunks/p0401-p0500/p0438-c01.md)).
- **Вариант B:** в p439 расписание пишет в `/opt/zbx-backup/web-config/zabbix-web.tar.gz`, но каталог `web-config` до этого **не создавался**; строки `tar` местами разорваны физическими строками без гарантированного shell continuation; у одной строки `/opt/zbx-backup/lib /zabbix_usr_lib.tar.gz` содержит пробел в path ([p0439](../../../rag/chunks/p0401-p0500/p0439-c01.md)).
- **Следствие:** этот фрагмент не является исполнимым надёжным cron-job. Проверить все paths, exit codes, отсутствие `>/dev/null 2>&1` при отладке, retention и restore test.

## 3. [Needs confirmation / security-sensitive] Пароли DB и PostgreSQL pgpass

- p439 использует `mysqldump -p` с вводом пароля; [p0440](../../../rag/chunks/p0401-p0500/p0440-c01.md) в cron даёт пример `-p'password'`, т.е. секрет встроен в расписание и может быть раскрыт.
- [p0440](../../../rag/chunks/p0401-p0500/p0440-c01.md) создаёт `~/.pgpass` с полем `localhost:5432:zabbixdb:zabbixuser:password`, но не даёт требуемых file mode/ownership/protection мер.
- **Следствие:** не коммитить/не публиковать реальные secret values; безопасная авторизация, права pgpass и зашифрованное внехостовое хранение `[Needs confirmation]`.

## 4. [Destructive] Ротация backup через find -delete и непроверенное восстановление

- [p0440](../../../rag/chunks/p0401-p0500/p0440-c01.md) предлагает удалять DB backups старше 60 дней через `find ... -mtime +60 -type f -delete`.
- Книга демонстрирует создание дампов и архивов, но **не показывает чтение/восстановление дампа и проверку целостности**, не задаёт исключения для «последнего рабочего backup».
- **Следствие:** не включать автоматическую очистку без защиты от потери последней копии; критерий restore test — практика приёмки, **не выполненное действие источника**.

## 5. [Source wording/code mismatch] Ubuntu PHP PPA и apt-key

- [p0444](../../../rag/chunks/p0401-p0500/p0444-c01.md) записывает `apt install software-properties-common add-apt-repository ppa:ondrej/php` в **одну строку**, смешивая установку пакета и команду добавления PPA; происхождение syntax `[Needs confirmation]`.
- [p0445](../../../rag/chunks/p0401-p0500/p0445-c01.md) пишет `apt-key adv --keyserver keyserver.ubuntu.com --recv- keys PUB_KEY_HERE`; флаг `--recv- keys` разорван пробелом.
- **Следствие:** эти буквальные строки не следует исполнять, версия и безопасность репозиториев, наличие подлинного ключа, настройки signatures не подтверждены.

## 6. [Source extraction issue / source code mismatch] Дубли repo blocks MariaDB

- [p0446](../../../rag/chunks/p0401-p0500/p0446-c01.md) начинается файл `/etc/yum.repos.d/mariadb.repo`, [p0447](../../../rag/chunks/p0401-p0500/p0447-c01.md) повторяет полностью секции `[mariadb-main]`, `[mariadb-maxscale]`, `[mariadb-tools]` после уже описанного `baseurl`.
- **Возможные причины:** многостраничное воспроизведение таблицы, ошибка верстки или текстовой экстракции. **Нельзя доказать по текстовому RAG**, нужно ли буквально добавлять оба блока.
- **Следствие:** конфигурация repo из p446–447 не считается готовым файлом; `RAG_MISS` для оригинальной визуальной разбивки.

## 7. [Security-sensitive] MariaDB repo setup через скачанный shell script, unsupported DB bypass

- [p0448](../../../rag/chunks/p0401-p0500/p0448-c01.md)–[p0449](../../../rag/chunks/p0401-p0500/p0449-c01.md) предлагают shell pipeline, который выполняет удалённый `mariadb_repo_setup` в privileged shell. Автор не даёт проверки SHA/signature, rollback пакетов и гарантии совместимости.
- [p0449](../../../rag/chunks/p0401-p0500/p0449-c01.md) демонстрирует `apt remove mariadb-server mariadb-client` **перед** установкой — риск остановки БД/изменения package dependencies. В [p0450](../../../rag/chunks/p0401-p0500/p0450-c01.md) `AllowUnsupportedDBVersions=1` явно **не рекомендуется**.
- **Следствие:** не исполнять эти операции на production по самому тексту книги; backup schema/data, upgrade plan и rollback `[Needs confirmation]`.

## 8. [Source code mismatch] Zabbix RHEL repo URL и версии

- На [p0451](../../../rag/chunks/p0401-p0500/p0451-c01.md) RHEL8 URL RPM указан с суффиксом `zabbix-release-7.0-1.el8noarch.rpm`. Форма вызывает сомнения в имени целевого RPM; книга сама в [p0453](../../../rag/chunks/p0401-p0500/p0453-c01.md) советует проверять repo для конкретной системы.
- **Следствие:** не принимать буквальный URL за проверенно существующий RPM. `zabbix_server.conf` не перезаписывать при upgrade без backup; rollback schema/database `[Needs confirmation]`.

## 9. [Source wording inconsistency] HousekeepingFrequency «снизили» vs «раз в два часа»

- [p0458](../../../rag/chunks/p0401-p0500/p0458-c01.md) устанавливает `HousekeepingFrequency=2` и предупреждает: увеличение интервала даёт лишь отсрочку.
- [p0463](../../../rag/chunks/p0401-p0500/p0463-c01.md) говорит «мы снизили это значение», но одновременно поясняет, что теперь housekeeper работает **каждые два часа**, а ранее — **раз в час**. Это несогласованное словоупотребление **о направлении изменения**.
- `MaxHousekeeperDelete=20000` в тексте сопоставляется с «5000 каждый час»; источник предлагает балансировку под конкретную DB.
- **Следствие:** сохранять значения и явно отделять частоту вызовов от числа строк за один запуск. Настройка `HousekeepingFrequency=2` **не исправляет корень проблемы**.

## 10. [Needs confirmation] Тюнинг процессов, mysqltuner, rollback

- `StartDiscoverers=2` [p0456](../../../rag/chunks/p0401-p0500/p0456-c01.md) увеличивает параллелизм, но может вызвать CPU/RAM/DB-connection contention ([p0461](../../../rag/chunks/p0401-p0500/p0461-c01.md)–[p0462](../../../rag/chunks/p0401-p0500/p0462-c01.md)).
- [p0459](../../../rag/chunks/p0401-p0500/p0459-c01.md) скачивает и выполняет сторонний `mysqltuner.pl`; [p0460](../../../rag/chunks/p0401-p0500/p0460-c01.md) предупреждает **не применять советы автоматически**. Подлинность/совместимость скачанного script не проверена.
- В источнике отсутствуют полноценные **DB restoration drill, rollback PHP streams/MariaDB/Zabbix schema и нагрузочные границы для всех async pollers**; `[Needs confirmation]`.

## 11. [Needs confirmation] Граница главы и условные файлы

В [p0464](../../../rag/chunks/p0401-p0500/p0464-c01.md) последняя тема — async pollers Agent, HTTP и SNMP, `MaxConcurrentChecksPerPoller`. На [p0465](../../../rag/chunks/p0401-p0500/p0465-c01.md) открывается глава 12. **Итогового отдельного summary и review questions/answers нет**, условные файлы не создаются. Конкретные значения на рисунках 11.1–11.22 = `RAG_MISS`.
