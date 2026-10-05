# Команды и интерфейсы главы 7

Только элементы, явно подтверждённые RAG главы 7.

| Команда / интерфейс | Назначение | Тип | Effect | Risk | Verification | Rollback |
|---|---|---|---|---|---|---|
| `journalctl` | Просмотр system journal | read-only | Не меняет state | Большой объём output | Сузить filter | N/A |
| `journalctl -S ...` / `-U ...` | Time filtering | read-only | Не меняет state | Ошибка time window может скрыть событие | Проверить timestamps | N/A |
| `journalctl -u unit` | Filter by systemd unit | read-only | Не меняет state | Unit field может отсутствовать у short-lived cases | Сравнить с time search | N/A |
| `journalctl -F FIELD` / `-N` | Values/fields inventory | read-only | Не меняет state | Нет | Проверить найденные fields | N/A |
| `journalctl -g REGEX` | Regex text search | read-only | Не меняет state | Опция может отсутствовать в некоторых builds | При необходимости использовать time/context search | N/A |
| `journalctl -b` / `-b -1` / `--list-boots` | Boot-specific logs | read-only | Не меняет state | Нет | Подтвердить boot ID/time | N/A |
| `journalctl -p 3` / `-p 2..3` | Priority filter | read-only | Не меняет state | Можно потерять context низшего priority | Сравнить с более широким search | N/A |
| `journalctl -f` | Follow journal | workload-generating | Continuous monitoring | Можно пропустить context outside filter | Остановить monitoring | N/A |
| `groups` | Groups текущего user | read-only | Не меняет state | Нет | Сопоставить с `/etc/group` | N/A |
| `ps ao args \| grep getty` | Найти getty process | read-only | Не меняет state | Pattern noise | Проверить process args | N/A |
| `date +%s` / `date` | System time representation | read-only | Не меняет state | Нет | Сравнить expected time | N/A |
| `TZ=US/Central date` | One-command timezone override | read-only | Не меняет global state | Только process environment | Сравнить output | N/A |
| `crontab -l` | List user crontab | read-only | Не меняет state | Нет | Проверить installed entries | N/A |
| `atq` | List queued at jobs | read-only | Не меняет state | Нет | Найти expected job | N/A |
| `systemctl list-timers` | List systemd timers | read-only | Не меняет state | Нет | Проверить next/last activation | N/A |
| `ps -eo pid,euser,ruser,comm` | EUID/RUID process view | read-only | Не меняет state | Нет | Сопоставить privilege context | N/A |
| `man -k pam_` | PAM module discovery | read-only | Не меняет state | Нет | Проверить module docs | N/A |
| `locate pam_unix.so` | Найти PAM module | read-only | Не меняет state | Locate DB может быть stale | Проверить найденный path | N/A |
| `grep password.*unix /etc/pam.d/*` | Найти password rules с pam_unix | read-only | Не меняет state | Читает security config | Сопоставить generated/source files | N/A |
| `passwd` / `passwd user` | Изменить password | state-changing | Меняет authentication data | Lockout/security impact | Проверить expected authentication | `[Needs confirmation]` |
| `chfn` / `chsh` | Изменить account metadata/shell | state-changing | Меняет user account data | Invalid shell/profile impact | Проверить account entry/login shell | `[Needs confirmation]` |
| `adduser` | Добавить user | state-changing | Создаёт account | UID/home/policy impact | Проверить account/files | `userdel` только если rollback scope verified |
| `userdel` | Удалить user | state-changing | Удаляет account mapping | Data ownership/orphaning risk | Проверить intended account removal | `[Needs confirmation]` |
| `vipw` | Locked edit `/etc/passwd` | state-changing | Редактирует critical user DB | Syntax/lockout risk | Проверить file syntax/account access | Restore backup created by tool/context |
| `vipw -s` | Locked edit `/etc/shadow` | state-changing | Редактирует critical auth DB | High lockout/security risk | Проверить authentication | Restore backup/recovery path |
| `hwclock --systohc --utc` | Записать system time в RTC как UTC | state-changing | Меняет hardware clock | Wrong system time propagates to RTC | Проверить time after operation | `[Needs confirmation]` |
| `export TZ=...` | Session timezone override | state-changing in shell env | Меняет environment текущей shell | Может путать output/scripts | `date` | unset TZ / clean shell |
| `crontab file` | Install user crontab | state-changing | Заменяет current user crontab | Schedule overwrite | `crontab -l` | Restore saved previous crontab |
| `crontab -e` | Edit/install user crontab | state-changing | Меняет schedule | Incorrect job timing/commands | `crontab -l` + task result | Restore previous content |
| `crontab -r` | Remove user crontab | state-changing | Удаляет all user cron entries | High schedule loss risk | `crontab -l` should show none/error | Restore saved previous crontab |
| `at 22:30` | Queue one-time job | state-changing | Добавляет future task | Command executes later | `atq` | `atrm` before execution |
| `atrm` | Remove queued at job | state-changing | Cancels job | Wrong job ID | `atq` | Recreate job if needed |
| `systemd-run --on-calendar=...` | Create transient timer/service | state-changing | Schedules transient unit | Wrong calendar may create recurring behavior | `systemctl list-timers` | `[Needs confirmation]` |
| `loginctl enable-linger` | Keep user manager after logout | state-changing | Persistent user manager state | User services can continue without session | Verify timer survives logout | `[Needs confirmation]` |
| PAM file edit | Change authentication policy | state-changing | Alters auth/account/session/password flow | System-wide lockout/security risk | Test intended and denied paths before losing recovery session | Restore known-good config from recovery session |

## Cron format

User crontab fields:

`minute hour day-of-month month day-of-week command`

System `/etc/crontab` adds a user field before command.

## systemd timer pair

Timer unit:
- `OnCalendar=`;
- `Unit=`;
- `WantedBy=timers.target`.

Service unit example:
- `Type=oneshot`;
- `ExecStart=...`.

## PAM configuration model

Locations:
- `/etc/pam.d`;
- legacy `/etc/pam.conf`.

Functions:
- `auth`;
- `account`;
- `session`;
- `password`.

Control arguments highlighted by source:
- `sufficient`;
- `requisite`;
- `required`.

Example modules:
- `pam_rootok.so`;
- `pam_shells.so`;
- `pam_unix.so`;
- `pam_deny.so`.

## Safety notes

1. Не редактировать `/etc/passwd` и `/etc/shadow` обычным editor без необходимости.
2. PAM changes могут заблокировать authentication; сначала понять generated config и иметь recovery access.
3. `crontab -r` удаляет весь user crontab.
4. One-shot/transient timers надо проверять на предмет случайной periodic activation.
5. Setuid-root programs увеличивают privilege attack surface.
