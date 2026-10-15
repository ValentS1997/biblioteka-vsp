# Глава 12 — source findings (RAG-only)

**Граница:** PDF 465–489; факты из 25 chunks в accepted RAG. Любая неполная команда, сомнительный SQL, источник внешнего Perl-кода и схемы со скриншотов **не восстанавливаются по памяти модели**, не проверены в интернете. Сохранены обе исходные версии при расхождении.

## 1. [Source code mismatch] Одинарные кавычки вокруг MySQL table identifiers

- **Вариант A:** [p0467](../../../rag/chunks/p0401-p0500/p0467-c01.md) сначала использует `SELECT FROM_UNIXTIME(MIN(clock)) FROM history;`.
- **Вариант B:** далее на той же p467 следует `SELECT FROM_UNIXTIME(MIN(clock)) FROM 'history';`, аналогично `'history_uint'`, `'history_str'`, `'history_text'`, `'history_log'`, `'history_bin'`.
- **Последствие:** это не согласованные формы обозначения идентификаторов SQL (одинарные кавычки выглядят как строковые литералы). Второй вариант **не выдаётся за рабочую команду**. Точные фактические имена/типы таблиц и MySQL dialect в целевой версии = `[Needs confirmation]`.

## 2. [Needs confirmation / destructive] Скрипт удаляет старые партиции и выключает housekeeper

- **Источник:** [p0470](../../../rag/chunks/p0401-p0500/p0470-c01.md)–[p0472](../../../rag/chunks/p0401-p0500/p0472-c01.md) загружает внешнюю реализацию `mysql_zbx_part.pl`, устанавливает `$db_password` внутри script и включает cron `55 22 * * *`; затем отключает housekeeper History/Trends. [p0473](../../../rag/chunks/p0401-p0500/p0473-c01.md)–[p0474](../../../rag/chunks/p0401-p0500/p0474-c01.md) явно описывает **удаление целой старой партиции** и создание **10 будущих**.
- **Риск:** необратимое удаление истории, конфигурация retention без индивидуальных сроков item, хранение credentials, supply chain внешнего Perl. Файл Perl из ссылки **не скачан**, его фактическое содержимое и корректность `$tables` = `RAG_MISS`/`[Needs confirmation]`.
- Книга прямо требует backup до партиционирования (p466). Без проверенного restore, проверок будущих диапазонов и подтверждения script не отключать текущую очистку.

## 3. [Source wording/code mismatch] Несовместимые версии PostgreSQL 12/15 и слитые имена пакетов

- [p0475](../../../rag/chunks/p0401-p0500/p0475-c01.md) устанавливает `timescaledb-2-postgresql-15`, но команда старта сопровождается словами «Запустите и включите PostgreSQL 12»; RHEL-ветка той же страницы явно устанавливает `postgresql15 postgresql15-server`, [p0476](../../../rag/chunks/p0401-p0500/p0476-c01.md) перезапускает `postgresql-15`.
- [p0476](../../../rag/chunks/p0401-p0500/p0476-c01.md) содержит слитое имя `zabbix-apacheconfzabbix-agent2`; [p0477](../../../rag/chunks/p0401-p0500/p0477-c01.md) — `zabbix-frontend-phpphp-pgsql` (без разделителя), а также разрывы строк команд `zcat`.
- **Решение:** нельзя копировать список пакетов как рабочий script. Варианты 12/15 сохранены, версию/архивы схемы/путь `pg_config` и имена unit надо подтвердить до установки.

## 4. [Source extraction issue / Source code mismatch] Разорванный `pg_hba.conf`

- **Вариант текста [p0478](../../../rag/chunks/p0401-p0500/p0478-c01.md)**: `local all all` на отдельной строке, `scram-sha256` на следующей; `host all all 127.0.0.1/32` отделён от `md5` переводом строки; `host all all ::1/128` отделён от `scram-sha256`.
- **Риск:** нельзя вставлять такие строки буквально в `pg_hba.conf`; это либо разорванный формат извлечения, либо дефект верстки. Точную конфигурацию доступа и допустимый auth method для целевого PostgreSQL = `[Needs confirmation]`. Не додумывать рабочие объединённые строки без верификации.

## 5. [Source code mismatch] Настройка Ubuntu репозитория и недостаточно ясное управление доверенными ключами

- [p0475](../../../rag/chunks/p0401-p0500/p0475-c01.md) последовательность `apt install gnupg postgresql-common apt-transport-https`, затем **на новой строке** `lsb-release wget` перед запуском `pgdg/apt.postgresql.org.sh` не содержит явного продолжения команды.
- Та же страница содержит `wget ... | sudo apt-key add -`; [p0476](../../../rag/chunks/p0401-p0500/p0476-c01.md) содержит RHEL репозиторий с `repo_gpgcheck=1`, но `gpgcheck=0`, плюс фрагмент `$(rpm-E %{rhel})` со слитыми аргументами.
- **Риск:** неподтверждённая цепочка доверия и синтаксис ввода; нельзя выдавать как проверенную безопасную установку. Точное нынешнее состояние репозиториев не проверялось (RAG-only).

## 6. [Source contradiction] Перепутанные роли двух TLS-серверов

- **Вариант A:** [p0465](../../../rag/chunks/p0401-p0500/p0465-c01.md) явно говорит, что `lar-book-secure-db` — MariaDB, а `lar-book-secure-zbx` — Zabbix 7; [p0480](../../../rag/chunks/p0401-p0500/p0480-c01.md) показывает `10.16.16.170 lar-book-secure-db` и `10.16.16.171 lar-book-secure-zbx`.
- **Вариант B:** подготовка на [p0480](../../../rag/chunks/p0401-p0500/p0480-c01.md) говорит, что на `lar-book-secure-db` «установлен только Zabbix», а на том же `lar-book-secure-db` уже установлена MariaDB.
- **Решение:** не считать два одинаковых имени доказательством одновременной установки на одной машине; контекст/начальная спецификация подтверждает **два узла разного назначения**, но исходное расхождение сохранено. Структура фактической среды = `[Needs confirmation]`.

## 7. [Source code mismatch / high risk] MariaDB пользователь создан для IP .171, TLS затребован для .152

- **Вариант A:** [p0480](../../../rag/chunks/p0401-p0500/p0480-c01.md) создаёт `create user 'zabbix'@'10.16.16.171' identified BY 'password';` и grants этому `user@host`; таблица `/etc/hosts` указывает `.171` серверу Zabbix.
- **Вариант B:** [p0485](../../../rag/chunks/p0401-p0500/p0485-c01.md) выполняет `alter user 'zabbix'@'10.16.16.152' require ssl;`, при этом текст требует «убедиться, что IP совпадает».
- **Риск:** `REQUIRE SSL` может примениться **не к той учётной записи** либо завершиться ошибкой. `10.16.16.152` здесь не соответствует объявленному `lar-book-secure-zbx`. Не применять без проверки точных users/grants, адресов frontend и server, а также защищённых подключений.

## 8. [Source code mismatch] Отсутствие пробелов в командах копирования сертификатов

- **Вариант A:** [p0486](../../../rag/chunks/p0401-p0500/p0486-c01.md) содержит `cp /etc/pki/CA/certs/zbx-srv_crt.pem/var/lib/zabbix/ssl/zbx-srv.crt` и `cp /etc/pki/CA/private/zbx-srv_key.pem/var/lib/zabbix/ssl/zbx-srv.key` — нет разделения source/destination аргументов.
- **Вариант B:** на той же странице корректно разделена `cp /etc/pki/CA/cacert.pem /var/lib/zabbix/ssl/`.
- **Риск:** скопированный literal p486 не создаёт нужный файл и может привести к TLS outage после `DBTLSConnect=verify_full`. Не приводить «исправленный» command как проверенный без выяснения реальных путей и ownership.

## 9. [Source wording/code mismatch] CSR, private key без пароля и запросы на passphrase

- [p0483](../../../rag/chunks/p0401-p0500/p0483-c01.md) для Zabbix CSR задаёт `openssl req -nodes -new ...`, а [p0484](../../../rag/chunks/p0401-p0500/p0484-c01.md) повторяет `-nodes` для MariaDB и утверждает, что файлы нужно создавать **без пароля**, иначе Zabbix/MariaDB не смогут пользоваться ими.
- При этом p484 говорит, что пользователю «снова будет предложено добавить пароль», что **неоднозначно** с учётом `-nodes`.
- **Решение:** не предполагать, что ключ автоматически хранится безопасно. Права, ownership, защита безпарольного ключа, SAN/CN, trust chain и практика ротации = `[Needs confirmation]`. Секреты не показывать.

## 10. [Needs confirmation] `verify_full`, frontend TLS и истечение сертификатов

- [p0486](../../../rag/chunks/p0401-p0500/p0486-c01.md) конкретно задаёт Zabbix server `DBTLSConnect=verify_full`, CAFile, CertFile и KeyFile; [p0487](../../../rag/chunks/p0401-p0500/p0487-c01.md) требует настроить frontend по **рисунку 12.16**, а [p0488](../../../rag/chunks/p0401-p0500/p0488-c01.md) заявляет, что данные frontend↔MariaDB тоже шифруются.
- Поля frontend не доступны в text RAG: `RAG_MISS`. Нельзя подтвердить наличие frontend TLS только конфигурацией Zabbix server.
- CA срок **3650 дней** p482, конечные certs **365 дней** p484; p488 требует отслеживать истечение. Конкретная цепочка автоматического перевыпуска, тест имён/SAN, отказоустойчивый cutover и rollback `[Needs confirmation]`.

## 11. [Needs confirmation] Ограничения retention и внешняя актуальность

- p474: MySQL external partitions лишают индивидуальной retention для items. p479: TimescaleDB позволяет менять **глобальную** retention через UI, но тоже **не даёт разного срока для каждого item**.
- Исторические партиции с датами 2023, внешние Perl/TimescaleDB/Zabbix package URLs, flags и версии не означают актуальную безопасную инструкцию для текущих хостов. Режим главы — RAG-only, ссылки не проверялись.

## 12. [Needs confirmation] Нет полного rollback и chapter-end контрольных вопросов

На [p0489](../../../rag/chunks/p0401-p0500/p0489-c01.md) финальный абзац о шифровании, [p0490](../../../rag/chunks/p0401-p0500/p0490-c01.md) начинает главу 13. Отдельных source-end `summary`, `review questions`, `review answers` нет; условные файлы не создаются. Нет source-backed полного rollback удалённой истории/партиций, Timescale миграции, неверных ACL и cert switch — `[Needs confirmation]`. Резервная копия и тест восстановления необходимы до работ.
