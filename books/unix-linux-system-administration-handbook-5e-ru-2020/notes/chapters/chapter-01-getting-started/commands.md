# Команды и инструменты главы 1

Таблица включает только команды и инструменты, подтвержденные RAG главы 1. Примеры, используемые лишь для объяснения синтаксиса, отмечены как такие.

| Команда / инструмент | Назначение | Что проверить | Тип |
|---|---|---|---|
| `vimtutor` | Интерактивное введение в Vim | базовые навыки работы в редакторе | read-only |
| `grep Bob /pub/phonelist` | Пример поиска строк | совпадения по шаблону | read-only |
| `sudo su - root` | Пример перехода в привилегированную оболочку | что приглашение изменилось на root-контекст | state-changing |
| `passwd` | Пример изменения пароля root | успешное изменение пароля | state-changing |
| `dpkg -l` | Пример списка установленных пакетов Debian/Ubuntu | наличие пакета в установленном наборе | read-only |
| `man <topic>` | Открыть man-страницу | синтаксис, опции, примеры и связанные команды | read-only |
| `man <section> <topic>` | Открыть одноимённую страницу из конкретного раздела | правильный объект: команда, syscall, файл и т. п. | read-only |
| `man -k <keyword>` | Искать man-страницы по ключевому слову | список релевантных страниц | read-only |
| `apropos <keyword>` | Альтернатива `man -k` | список релевантных страниц | read-only |
| `makewhatis` | Перестроить keyword database man в Red Hat/FreeBSD | обновление индекса | state-changing |
| `mandb` | Перестроить keyword database man в Ubuntu | обновление индекса | state-changing |
| `manpath` | Показать путь поиска man-страниц | каталоги документации | read-only |
| `export MANPATH=...` | Изменить путь поиска man в текущем shell environment | новое значение `MANPATH` | state-changing |
| `which <command>` | Проверить, доступен ли binary через текущий PATH | путь к найденной команде | read-only |
| `whereis <name>` | Искать объект в более широком наборе системных каталогов | найденные пути | read-only |
| `locate <pattern>` | Найти имена файлов по файловому индексу | совпадающие пути; учитывать возможную устарелость индекса | read-only |
| `updatedb` | Обновить базу `locate` в Linux | свежесть индекса | state-changing |
| `locate.updatedb` | Обновить базу `locate` в FreeBSD | свежесть индекса | state-changing |
| `rpm -q <package>` | Проверить наличие и версию RPM-пакета | установлен ли пакет и какая версия | read-only |
| `rpm -qf <path>` | Определить RPM-пакет-владельца файла | имя пакета | read-only |
| `pkg which <path>` | Определить package owner в FreeBSD | имя пакета | read-only |
| `dpkg-query -S <path>` | Определить package owner в Debian/Ubuntu | имя пакета | read-only |
| `sudo apt-get install tcpdump` | Пример установки пакета Debian/Ubuntu | успешная установка пакета | state-changing |
| `sudo yum install tcpdump` | Пример установки пакета Red Hat/CentOS | успешная установка пакета | state-changing |
| `sudo pkg install -y tcpdump` | Пример установки пакета FreeBSD | успешная установка пакета | state-changing |
| `git clone <repo>` | Получить исходный код из Git | локальный clone репозитория | state-changing |
| `git checkout tags/<tag> -b <branch>` | Выбрать нужный tagged release для сборки | активная локальная ветка/версия | state-changing |
| `./configure` | Подготовить исходный код к сборке | успешное определение build environment | state-changing |
| `./configure --help` | Показать параметры configure | доступные опции сборки | read-only |
| `make` | Скомпилировать ПО | завершение сборки без ошибки | workload-generating |
| `sudo make install` | Установить собранное ПО | размещение файлов установки | state-changing |
| `curl -o /tmp/saltboot -sL https://bootstrap.saltstack.com` | Сохранить web installer во временный файл | успешное завершение загрузки | state-changing |
| `sudo sh /tmp/saltboot` | Запустить сохранённый installer отдельно | завершение установки | state-changing |
| `curl -L https://... \| sudo sh` | Показанный в главе опасный anti-pattern | не использовать как рекомендуемый install flow | state-changing |

## Правила, которые следует вынести из главы

1. Для установки предпочитать пакет, созданный для конкретной системы, а не просто пакет того же формата.
2. Перед установкой сначала проверить, существует ли команда/файл уже сейчас.
3. Пакетный вариант удобнее отслеживать, обновлять и удалять, чем web installer.
4. Web installer должен загружаться по HTTPS.
5. Не передавать поток `curl` напрямую в привилегированную оболочку: при частичной загрузке shell может выполнить неполный сценарий.
6. Если используется web installer, глава рекомендует сначала сохранить сценарий во временный файл и запускать его отдельным этапом после успешной загрузки.

## Rollback coverage

Глава 1 не приводит конкретные команды удаления пакетов, отката `make install` или восстановления изменений web installer. Для этих state-changing действий rollback в рамках RAG главы: `[Needs confirmation]`.
