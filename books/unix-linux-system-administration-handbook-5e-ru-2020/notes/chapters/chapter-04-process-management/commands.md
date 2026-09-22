# Команды главы 4

Только команды и формы команд, подтверждённые RAG главы 4.

| Команда | Назначение | Что смотреть / проверять | Тип |
|---|---|---|---|
| `kill -l` | Показать имена/номера signals | доступный signal set | read-only |
| `kill [-SIGNAL] <PID>` | Послать signal процессу; по умолчанию TERM | реакция target process | state-changing |
| `kill -9 <PID>` | Послать KILL, который нельзя перехватить/заблокировать | использовать только после неудачного graceful TERM | state-changing |
| `sudo killall httpd` | Послать signal всем процессам по имени | все matching processes | state-changing |
| `sudo pkill -u ben` | Послать TERM процессам по атрибуту пользователя | matching processes | state-changing |
| `nohup <command>` | Запустить процесс устойчивым к HUP в Bourne-like shell workflow | process продолжает работу после logout | state-changing |
| `ps aux` | Snapshot всех процессов | USER, PID, %CPU, %MEM, VSZ, RSS, STAT, TIME, COMMAND | read-only |
| `ps lax` | Более технический snapshot без username lookup | PPID, NI, WCHAN, STAT | read-only |
| `ps auxww` | Не обрезать длинную command line | полный COMMAND/args | read-only |
| `ps aux \| grep sshd` | Найти процесс по строке | matching PID/command | read-only |
| `ps aux \| grep -v grep \| grep sshd` | Убрать self-match grep | matching target process | read-only |
| `pidof /usr/sbin/sshd` | Получить PID по executable | PID(s) | read-only |
| `pgrep sshd` | Найти PID по имени/атрибуту | PID(s) | read-only |
| `top` | Continuous process/system monitor | load, CPU, RAM, swap, active processes | read-only |
| `top -P` | FreeBSD: показать CPU по ядрам | per-CPU activity | read-only |
| `top -q` | Запустить top с максимально возможным priority | доступность monitoring under overload | state-changing |
| `nice -n 5 /bin/longtask` | Запустить command с пониженным CPU priority | NI/priority target process | state-changing |
| `sudo renice -5 8829` | Изменить nice value running process | новое NI/priority | state-changing |
| `sudo renice 5 -u boggs` | Изменить priority процессов пользователя | NI выбранных процессов | state-changing |
| `man proc` | Документация Linux `/proc` | process/kernel pseudo-files | read-only |
| `cat /proc/<PID>/<file>` | Читать process state напрямую | cmdline, status, maps, statm и др. | read-only |
| `less /proc/<PID>/<file>` | Просматривать текстовые `/proc` data | process state | read-only |
| `tr '\\000' '\\n'` | Сделать NUL-separated `cmdline`/environment читаемыми | отдельные arguments/env entries | read-only |
| `sudo mount -t procfs proc /proc` | FreeBSD: смонтировать deprecated procfs | наличие `/proc` | state-changing |
| `sudo strace -p 5810` | Attach к Linux process и смотреть syscalls/signals | syscall args, return codes, errors | read-only with side-effect risk |
| `strace -f ...` | Trace child processes | forked process activity | read-only with side-effect risk |
| `strace -e trace=file ...` | Ограничить trace файловыми операциями | missing/permission/config paths | read-only with side-effect risk |
| `truss cp /etc/passwd /tmp/pw` | FreeBSD syscall trace запускаемой команды | syscalls, args, errors | read-only with side-effect risk |
| `uptime` | Быстро посмотреть load averages | 1/5/15-minute load | read-only |
| `df -h` | Найти заполненную filesystem | filesystem usage | read-only |
| `du -h` | Найти directory/file growth внутри filesystem | space by subtree | read-only |
| `fuser ...` | Найти processes, удерживающие file/filesystem | PIDs | read-only |
| `lsof ...` | Найти open files | process ↔ file descriptors | read-only |
| `crontab <file>` | Установить user's crontab, заменив прежний | active crontab | state-changing |
| `crontab -e` | Редактировать crontab через supported interface | новая schedule entries | state-changing |
| `crontab -l` | Показать current crontab | jobs | read-only |
| `crontab -r` | Удалить user's crontab | absence of crontab | state-changing |
| `crontab -r jsmith` | Root: удалить crontab другого пользователя | target user's crontab removed | state-changing |
| `crontab -e jsmith` | Root: редактировать crontab другого пользователя | target user's jobs | state-changing |
| `crontab -u jsmith crontab.new` | Linux: установить файл для указанного user | target crontab | state-changing |
| `chmod +x <script>` | Сделать cron script executable | executable bit | state-changing |
| `systemctl list-timers` | Показать systemd timers | NEXT/LAST/UNIT/ACTIVATES | read-only |
| `cat /usr/lib/systemd/system/<name>.timer` | Посмотреть timer unit | OnBootSec/OnCalendar и др. | read-only |
| `cat /usr/lib/systemd/system/<name>.service` | Посмотреть service action | ExecStart и dependencies | read-only |
| `systemctl start <service-or-timer>` | Запустить service/timer | active state / action result | state-changing |
| `systemctl enable <timer>` | Включить timer на boot | enabled state | state-changing |
| `systemd-run --on-calendar '*:0/10' /bin/sh -c "cd /app && git pull"` | Создать transient timer | generated timer/service unit | state-changing |
| `systemctl list-timers <unit>.timer` | Проверить transient timer | next/last run | read-only |
| `systemctl list-units <unit>.timer` | Проверить unit state | LOAD/ACTIVE/SUB | read-only |
| `sudo systemctl stop <unit>.timer` | Остановить/удалить transient timer | unit stopped | state-changing |
| `rsync` | Периодически поддерживать mirror в актуальном состоянии | sync result | state-changing |

## Signals, которые глава выделяет

| Signal | Смысл по главе | Особенность |
|---|---|---|
| TERM | graceful termination request | процесс может перехватить/игнорировать |
| KILL | безусловное завершение | нельзя перехватить, блокировать или игнорировать |
| STOP | приостановить | нельзя перехватить, блокировать или игнорировать |
| CONT | продолжить после STOP | нельзя блокировать |
| TSTP | terminal stop request | обычно Ctrl+Z; можно перехватить |
| INT | interrupt current operation | обычно Ctrl+C |
| HUP | hangup/reload semantics | многие daemons используют как reload |
| QUIT | termination-like signal | default action может создать core dump |
| USR1/USR2 | application-defined | semantics задаёт программа |

## Scheduling reference

### Cron fields

```text
minute hour day-of-month month day-of-week command
```

Глава отдельно предупреждает:

- `* * * * *` означает запуск каждую минуту;
- day-of-week и day-of-month при одновременном задании образуют альтернативные условия, а не обязательное AND;
- cron command выполняется через `sh`, но не login shell;
- PATH/environment могут отличаться от интерактивной сессии;
- использовать полные пути команд;
- не редактировать spool crontab напрямую — использовать `crontab`;
- сотни одинаковых jobs в одну секунду могут создать сетевой/ресурсный spike; использовать random delay.

### Systemd timer structure

```text
<name>.timer   → schedule
<name>.service → action
```

Подтверждённые time directives:

`OnActiveSec`, `OnBootSec`, `OnStartupSec`, `OnUnitActiveSec`, `OnUnitInactiveSec`, `OnCalendar`, `AccuracySec`.

## Rollback / safety

- `kill -9` необратим для target process; использовать только после попытки graceful termination.
- Перед `renice` зафиксировать исходный NI; универсальный rollback зависит от предыдущего значения.
- `strace` attach обычно observational, но глава предупреждает, что tracing может прерывать syscalls; target должен корректно повторять их.
- `crontab <file>` заменяет предыдущую версию; если prior content не сохранён, rollback: `[Needs confirmation]`.
- `crontab -r` удаляет crontab; rollback без сохранённой копии: `[Needs confirmation]`.
- transient systemd timer можно остановить через `systemctl stop <timer>`.
