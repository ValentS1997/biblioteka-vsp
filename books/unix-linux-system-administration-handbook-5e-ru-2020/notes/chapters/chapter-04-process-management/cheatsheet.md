# Шпаргалка: управление процессами

Цель: понять, что делает process, собрать evidence, и только затем менять его state.

## 1. Базовая модель процесса

Процесс = address space + kernel-maintained metadata.

Администратору важны:

- PID и PPID;
- UID/EUID и GID/EGID;
- process state;
- priority / nice value;
- open files и network resources;
- signal mask;
- controlling terminal;
- threads.

Lifecycle:

```text
parent
  ↓ fork/clone
child
  ↓ exec
new program
  ↓ _exit
zombie / exit status
  ↓ wait by parent
process removed

parent died early?
  ↓
PID 1 adopts child and performs wait
```

## 2. Сначала snapshot

```bash
ps aux
ps lax
```

`ps aux` — USER/PID/CPU/RAM/state/command.

`ps lax` — PPID, NI, WCHAN и технический state без username lookup; глава отмечает, что это может быть полезнее на перегруженной системе.

Найти PID:

```bash
pidof /usr/sbin/sshd
pgrep sshd
ps aux | grep -v grep | grep sshd
```

## 3. Затем continuous monitoring

```bash
top
uptime
```

Смотреть:

- load averages;
- CPU usage;
- memory/swap;
- active processes;
- VIRT / RES;
- process state;
- рост resource usage во времени.

Для runaway memory глава предлагает добавить в Linux top поле DATA; в FreeBSD похожую роль играет SIZE.

## 4. Signals: graceful прежде force

Обычный termination flow:

```bash
kill <PID>
```

По умолчанию это TERM: process получает возможность cleanup.

Только если graceful request не сработал:

```bash
kill -9 <PID>
```

KILL нельзя перехватить или заблокировать.

Важно: process в uninterruptible sleep (`D`) может не завершиться даже от KILL; глава связывает типичный постоянный D-state с I/O/NFS problems. Тогда нужно исправить underlying problem или reboot.

## 5. Не убивать runaway process до сбора evidence

Глава прямо рекомендует сначала понять поведение: после уничтожения процесса большая часть доказательств исчезает.

Workflow:

```text
ps / top / uptime
   ↓
что потребляется?
CPU / RAM / filesystem
   ↓
/proc
   ↓
logs / verbose mode
   ↓
strace / truss, если обычных данных недостаточно
   ↓
только потом corrective action
```

## 6. /proc: process internals

Полезные process entries, перечисленные главой:

- `cmdline`;
- `cwd`;
- `environ`;
- `exe`;
- `fd/`;
- `fdinfo/`;
- `maps`;
- `ns/`;
- `root`;
- `stat`;
- `statm`.

Read-only:

```bash
man proc
cat /proc/<PID>/cmdline
cat /proc/<PID>/environ
```

Для NUL-separated data:

```bash
tr '\000' '\n'
```

## 7. strace / truss: deeper analysis

Linux:

```bash
sudo strace -p <PID>
```

Useful filters from chapter:

```bash
strace -f ...
strace -e trace=file ...
```

FreeBSD:

```bash
truss <command>
```

Что искать:

- failing syscalls;
- nonzero/error return codes;
- permission errors;
- missing files;
- socket conflicts;
- unexpected file paths.

Глава рекомендует переходить к syscall tracing после logs и обычных diagnostic methods.

## 8. Runaway CPU / RAM / disk

### CPU/load

```bash
uptime
top
ps aux
```

Глава связывает high load с CPU и, в Linux, также с I/O wait-like activity. Для CPU-bound system load выше числа available cores указывает на overload; около 100% CPU usage может указывать на CPU bottleneck.

### Memory

В `top`:

- VIRT — virtual allocation;
- RES — resident memory;
- DATA — process-specific data+stack indicator в Linux.

Смотреть не только абсолютное число, но и рост.

### Filesystem full

```bash
df -h
du -h
```

Workflow:

```text
df -h → определить filesystem
du -h → спускаться по дереву до large file/directory
```

Если `df` показывает usage, а `du` не объясняет его, глава указывает на возможный удалённый, но всё ещё открытый файл.

Тогда:

```bash
fuser ...
lsof ...
```

## 9. Priority: nice/renice

Higher nice value = lower CPU scheduling priority.

```bash
nice -n 5 /bin/longtask
sudo renice -5 <PID>
sudo renice 5 -u <user>
```

Ограничение: nice влияет на CPU priority, но не решает memory или I/O contention.

Перед изменением зафиксировать current NI.

## 10. Cron: recurring work

Не редактировать spool напрямую. Использовать:

```bash
crontab -e
crontab -l
```

Формат:

```text
minute hour day month weekday command
```

Operational rules:

- полный path к командам;
- учитывать, что cron запускает `sh`, но не login shell;
- environment задать явно при необходимости;
- executable script должен иметь execute bit;
- проверять cron log/syslog при проблемах;
- не запускать одну тяжёлую job одновременно на сотнях хостов — добавить random delay.

Risky:

```bash
crontab -r
```

Перед удалением сохранить текущий `crontab -l`.

## 11. Cron access control

Linux:

```text
/etc/cron.allow
/etc/cron.deny
```

FreeBSD:

```text
/var/cron/allow
/var/cron/deny
```

Глава подчёркивает: access enforcement обычно делает программа `crontab`, а не daemon `cron`; поэтому spool directories должны оставаться под контролем root.

## 12. Systemd timers

Проверить existing timers:

```bash
systemctl list-timers
```

Timer = schedule, service = action.

Перед debugging расписания удобно запускать service отдельно:

```bash
systemctl start <name>.service
```

Постоянный timer:

- `.timer` + `.service` в `/etc/systemd/system`;
- `systemctl enable <name>.timer`;
- при необходимости `systemctl start <name>.timer`.

Transient timer:

```bash
systemd-run --on-calendar '*:0/10' /bin/sh -c "cd /app && git pull"
systemctl list-timers <generated>.timer
sudo systemctl stop <generated>.timer
```

Transient units живут под `/run/systemd/system` и не сохраняются после reboot.

## 13. Что удобно планировать

Глава приводит recurring use cases:

- mail/report delivery;
- cleanup core/temporary files;
- log rotation;
- batch/database maintenance;
- backup;
- mirroring через `rsync`.

## Acceptance criteria для process troubleshooting

- process идентифицирован по PID/PPID/owner;
- state и resource usage измерены до вмешательства;
- syscall trace используется только после базовой диагностики;
- TERM предпочтён KILL;
- underlying I/O problem исключён для D-state;
- priority change проверяется через NI;
- scheduled job протестирована отдельно от scheduler;
- cron/timer state и logs проверены после настройки;
- rollback неизвестного изменения помечен `[Needs confirmation]`.
