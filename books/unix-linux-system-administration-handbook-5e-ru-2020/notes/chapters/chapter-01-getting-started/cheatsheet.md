# Шпаргалка: базовый workflow администратора

Цель: решить типичную задачу главы 1 с минимальным количеством догадок и с опорой на локальную документацию и отслеживаемые изменения.

## 1. Сначала определить область ответственности

Глава относит к системному администрированию:

- access/account management;
- hardware;
- automation;
- backup и restore;
- software installation/update;
- monitoring;
- troubleshooting;
- local documentation;
- security;
- performance;
- policy;
- vendors;
- user-facing incident response.

Interpretation: до выполнения команды определить, к какой из этих областей относится задача и кто ещё должен участвовать.

## 2. Нужна информация о команде или формате

Read-only checks:

```bash
man <topic>
man <section> <topic>
man -k <keyword>
apropos <keyword>
manpath
```

Acceptance check: найдена страница нужного объекта и раздела; понятны синтаксис и связанные команды.

Если keyword index устарел:

```bash
makewhatis   # Red Hat / FreeBSD
mandb        # Ubuntu
```

Effect: перестраивается индекс man. Rollback: `[Needs confirmation]`.

## 3. Нужно понять, установлено ли ПО

Начать с binary/file discovery:

```bash
which <command>
whereis <name>
locate <pattern>
```

Если нужен package owner:

```bash
rpm -q <package>
rpm -qf <path>
pkg which <path>
dpkg-query -S <path>
```

Interpretation:

- `which` отвечает на вопрос, доступна ли команда через текущий PATH;
- `whereis` ищет шире PATH;
- `locate` ищет файлы по индексу, который может отставать от текущего состояния файловой системы.

Next action: если индекс `locate` явно устарел, обновить его системной командой `updatedb` или `locate.updatedb`.

## 4. Нужно установить пакет

Глава показывает package-native путь как предпочтительный:

```bash
sudo apt-get install tcpdump   # Debian / Ubuntu
sudo yum install tcpdump       # Red Hat / CentOS
sudo pkg install -y tcpdump    # FreeBSD
```

Effect: изменяется установленный software set.

Verification:

```bash
which tcpdump
rpm -q tcpdump
```

или соответствующая package-query команда для системы.

Rollback: конкретная команда удаления в главе 1 не приведена — `[Needs confirmation]`.

## 5. Пакета нет или нужна конкретная версия: сборка из исходников

Примерный flow, показанный на tcpdump:

```bash
git clone https://github.com/the-tcpdump-group/tcpdump.git
cd tcpdump
git checkout tags/tcpdump-4.7.4 -b tcpdump-4.7.4
./configure
make
sudo make install
```

Перед сборкой полезно:

```bash
./configure --help
```

Risk:

- необходимы build dependencies;
- `make` создаёт нагрузку и build artifacts;
- `sudo make install` изменяет систему;
- rollback в главе не дан.

Acceptance check: configure и build завершаются успешно; после install требуемая команда должна обнаруживаться средствами discovery.

## 6. Web installer: безопаснее в два этапа

Показанный в главе подход:

```bash
curl -o /tmp/saltboot -sL https://bootstrap.saltstack.com
sudo sh /tmp/saltboot
```

Ключевое требование главы — HTTPS и отдельный этап запуска после успешной загрузки.

Не использовать как нормальный workflow:

```bash
curl -L https://badvendor.com | sudo sh
```

Почему: если загрузка оборвётся, привилегированная оболочка всё равно может выполнить полученную неполную часть сценария.

Verification: проверить наличие установленной команды через `which` или другой подтверждённый discovery-механизм.

Rollback: `[Needs confirmation]`.

## 7. После изменения

Глава многократно подчёркивает ценность:

- локальной документации;
- мониторинга;
- автоматизации повторяющихся задач;
- регулярных backup;
- периодической проверки restore;
- security monitoring;
- сотрудничества со смежными специалистами.

Acceptance check: состояние системы проверено, решение документировано, а для критичных данных восстановление backup проверяется периодически.

## Минимальный flow

```text
задача
  ↓
определить область ответственности
  ↓
найти авторитетную документацию
  ↓
проверить текущее состояние
  ↓
нужно изменение?
  ├─ нет → документировать / мониторить
  └─ да
       ↓
    package-native способ?
       ├─ да → установить → проверить
       └─ нет → source/web installer → проверить
  ↓
документировать результат
```
