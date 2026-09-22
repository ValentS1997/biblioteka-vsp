# Команды главы 6

Таблица включает только команды и формы команд, подтверждённые RAG главы 6. Установка, обновление, удаление и изменение installation/configuration state помечены как state-changing.

| Команда | Назначение | Что проверить | Тип |
|---|---|---|---|
| `openssl passwd -1` | Получить зашифрованное представление пароля для Kickstart | hash используется вместо plaintext password | read-only / output-generating |
| `debconf-get-selections --installer > preseed.cfg` | Экспортировать installer answers Debian/Ubuntu | installer selections записаны в файл | read-only / output-generating |
| `debconf-get-selections >> preseed.cfg` | Дописать остальные debconf selections | preseed содержит нужные answers | read-only / output-generating |
| `sudo mkdir FreeBSD` | Создать каталог для распаковки installer image | directory exists | state-changing |
| `sudo tar xpCf FreeBSD <FreeBSD.iso>` | Извлечь содержимое ISO FreeBSD в каталог | extracted tree соответствует image | state-changing |
| `rpm --help` | Показать режимы и опции RPM | нужный режим операции | read-only |
| `rpm -qa` | Перечислить установленные RPM packages | installed package set | read-only |
| `rpm -qa \| grep -i <name>` | Найти установленный RPM package | package/version | read-only |
| `sudo rpm -U <package.rpm>` | Обновить RPM package | dependency checks и результат upgrade | state-changing |
| `rpm -q --whatrequires <package>` | Показать packages, зависящие от target | reverse dependencies | read-only |
| `rpm -q <package>` | Запросить установленную версию package | installed version | read-only |
| `sudo rpm -U <packages...>` | Обновить несколько взаимозависимых RPM packages | dependency set установлен согласованно | state-changing |
| `dpkg -l` | Перечислить Debian packages | status + version | read-only |
| `dpkg -l \| grep -i <name>` | Найти package по имени | status `ii` и version | read-only |
| `sudo dpkg --install <package.deb>` | Установить/заменить Debian package | package successfully configured | state-changing |
| `dpkg -l <pattern>` | Проверить конкретный package после install | status/version | read-only |
| `sudo apt update` | Обновить package metadata | metadata refresh completed | state-changing / network |
| `sudo apt install <package>` | Найти, скачать и установить package + dependencies | package configured, dependencies resolved | state-changing |
| `apt upgrade` | Обновить установленные packages до доступных versions | proposed removals/changes и результат | state-changing |
| `apt-get update` | Обновить APT package information | repository metadata refreshed | state-changing / network |
| `apt-get --download-only ...` | Скачать packages без установки | packages downloaded for review | workload-generating / network |
| `apt-get autoclean` | Удалить неиспользуемые cached packages | cache reduced | state-changing |
| `sudo apt install apt-mirror` | Установить tool для локального mirror | apt-mirror installed | state-changing |
| `sudo apt-mirror` | Синхронизировать локальное repository mirror | mirror data downloaded/updated | workload-generating / network |
| `yum install <package>` | Установить package и dependencies из yum repository | requested package installed | state-changing |
| `yum update` | Обновить packages системы | planned package changes | state-changing |
| `yum upgrade` | Альтернативная команда upgrade, описанная в главе | planned package changes | state-changing |
| `yum makecache` | Обновить локальный yum cache | package cache current | workload-generating / network |
| `uname -r` | FreeBSD: определить текущую release branch/version | RELEASE/STABLE/CURRENT identifier | read-only |
| `sudo freebsd-update fetch install` | Получить и установить updates base system RELEASE | base update completed | state-changing |
| `sudo freebsd-update -r <RELEASE> upgrade` | Начать upgrade FreeBSD release | target release selected | state-changing |
| `pkg help` | Показать доступные pkg subcommands | command syntax | read-only |
| `pkg install -y <package>` | Установить binary package без confirmation | package installed | state-changing |
| `pkg backup` | Создать backup local package database | backup created | state-changing / output-generating |
| `pkg info` | Перечислить installed packages | installed set | read-only |
| `pkg info <package>` | Показать расширенную package information | metadata/version | read-only |
| `pkg search -i <term>` | Искать package в repository без учёта регистра | matching packages | read-only / network |
| `pkg audit -F` | Показать packages с известными security vulnerabilities | vulnerable package set | read-only / network |
| `pkg which <file>` | Найти package-владельца файла | package owner | read-only |
| `pkg autoremove` | Удалить неиспользуемые packages | removal set | state-changing |
| `pkg delete <package>` | Удалить package | package removed | state-changing |
| `pkg clean -ay` | Удалить cached packages | cache reduced | state-changing |
| `pkg update` | Обновить local copy package catalog | catalog current | state-changing / network |
| `pkg upgrade` | Обновить installed packages | packages upgraded | state-changing |
| `pkg version -vIL=` | Показать packages, требующие update | outdated package list | read-only |
| `portsnap fetch extract` | Инициализировать FreeBSD ports tree | ports metadata extracted | workload-generating / network |
| `portsnap fetch update` | Обновить ports tree | ports metadata current | workload-generating / network |
| `whereis <port>` | Найти port directory | path in `/usr/ports` | read-only |
| `make install clean` | Собрать и установить port, затем очистить work data | port installed | workload-generating / state-changing |
| `make deinstall` | Удалить software, установленное как port | port removed | state-changing |
| `portmaster -L` | Показать ports с доступными updates | outdated ports | read-only |
| `portmaster -a` | Обновить ports | updated port set | workload-generating / state-changing |
| `portmaster <category/port>` | Установить port | port built/installed | workload-generating / state-changing |
| `portmaster -c` | Очистить work directories ports | disk space reclaimed | state-changing |

## Installation configuration points

### Kickstart

Подтверждённая структура `ks.cfg`:

- command section;
- `%packages`;
- `%pre`;
- `%post`.

Глава отдельно рекомендует хранить root password в hashed form через `--iscrypted`, а не plaintext.

### Debian/Ubuntu preseed

Preseed answers передаются installer через kernel parameter вида:

`preseed/url=http://host/path/preseed.cfg`

Глава рекомендует hashed passwords, поскольку preseed files могут храниться на HTTP server.

## Package-management safety

- Не обходить dependency checks через `rpm --force` без серьёзной причины: глава приводит это как плохую идею.
- Package version string не обязательно полностью совпадает с version фактически установленной программы.
- High-level APT/yum предпочтительнее ручного разрешения dependency graph для ежедневного администрирования.
- Перед широким `apt upgrade`/yum/pkg upgrade проверять предполагаемые изменения и сначала тестировать rollout.
- Для большого числа hosts repository/mirror traffic нужно разносить по времени.
- `apt-get --download-only` позволяет отделить download от install, если source нужно дополнительно проверить.
- Не удалять FreeBSD package database; глава рекомендует `pkg backup`.

## Rollback

- Package systems стремятся поддерживать обратимость/атомарность, но глава прямо предупреждает: теоретическая rollback-возможность не заменяет предварительное тестирование.
- Для ОС installation, release upgrade, mass package upgrade и ports build универсальный rollback в RAG главы не задан: `[Needs confirmation]`.
