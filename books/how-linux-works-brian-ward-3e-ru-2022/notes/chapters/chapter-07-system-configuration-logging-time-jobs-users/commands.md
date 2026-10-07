# Команды и интерфейсы — глава 7

**Source:** `p0208:c01`–`p0243:c01`, PDF/печатные страницы 208–243. Только явно поддержанные RAG команды/config elements.

Классы: **RO** — read-only; **WG** — workload-generating / follow/interactive; **SC** — state-changing.

## 1. Logging

| Команда | Класс | Назначение |
|---|---|---|
| `journalctl` | RO | Проверка наличия/чтение journald records |
| `journalctl -r` | RO | Reverse chronological order |
| `journalctl _PID=8792` | RO | Filter by field |
| `journalctl -S -4h` | RO | Last four hours |
| `journalctl -S 06:00:00` | RO | Since local time |
| `journalctl -S '2020-01-14 14:30:00'` | RO | Since exact source example time |
| `journalctl -u cron.service` | RO | Filter by systemd unit |
| `journalctl -F _SYSTEMD_UNIT` | RO | List values of a field |
| `journalctl -N` | RO | List available fields |
| `journalctl -g 'kernel.*memory'` | RO | Regex text search; support depends on build/library |
| `journalctl -b` / `-b -1` | RO | Current / previous boot logs |
| `journalctl --list-boots` | RO | Boot identifiers and time ranges |
| `journalctl -k` | RO | Kernel messages |
| `journalctl -p 3`, `-p 2..3` | RO | Severity filtering |
| `journalctl -f` | WG/RO | Follow new journal messages |
| `tail -f logfile`, `less +F logfile` | WG/RO | Follow traditional text logs |

Paths/interfaces: `/etc/rsyslog.conf`, `/etc/syslog-ng`, `/var/log`, `/var/log/journal`, `/dev/log`. Traditional log rotation is described via `logrotate`; no explicit invocation command is supplied in the retrieved section.

## 2. Accounts and groups

| Command | Class | Effect / purpose | Risk / rollback |
|---|---|---|---|
| `groups` | RO | Show user's groups | [Not applicable] |
| `ps ao args \| grep getty` | RO | Locate getty processes | [Not applicable] |
| `passwd` | SC | Change own password | Access impact; rollback [Needs confirmation] |
| `passwd user` | SC privileged | Set another user's password | Verify exact account; rollback [Needs confirmation] |
| `chfn` | SC | Change GECOS/real-name metadata | Rollback [Needs confirmation] |
| `chsh` | SC | Change shell; shell must be in `/etc/shells` | May affect login; rollback [Needs confirmation] |
| `adduser` | SC privileged | Add user | UID/home/group impact; rollback [Needs confirmation] |
| `userdel` | SC privileged | Delete user | Ownership/data impact; rollback [Needs confirmation] |
| `vipw` | SC privileged | Locked/backup-aware edit of `/etc/passwd` | High risk; restore details [Needs confirmation] |
| `vipw -s` | SC privileged | Edit `/etc/shadow` | Critical auth risk; rollback [Needs confirmation] |

Files: `/etc/passwd`, `/etc/shadow`, `/etc/group`, `/etc/gshadow`, `/etc/shells`.

## 3. Time and timezone

| Command | Class | Effect |
|---|---|---|
| `date` | RO | Display system clock |
| `date +%s` | RO | Seconds since Unix epoch used by kernel model |
| `hwclock` | RO/SC depending invocation | Source discusses reading/resetting against RTC; exact no-arg semantics not expanded |
| `hwclock --systohc --utc` | SC | Copy current system time to RTC, treating RTC as UTC |
| `tzselect` | RO/advisory | Help select timezone name |
| `export TZ=US/Central` | SC shell env | Session timezone override |
| `TZ=US/Central date` | RO with temporary env | One-command timezone view |

Paths: `/etc/localtime`, `/usr/share/zoneinfo`. Manual copy/symlink of a zoneinfo file to `/etc/localtime` is state-changing but exact source command is not given.

The second printed `hwclock --systohc …utc` example contains a malformed dash in RAG; see `source-findings.md`.

## 4. cron

| Command/config | Class | Effect |
|---|---|---|
| `crontab -l` | RO | List current user's jobs |
| `crontab file` | SC | Install file as current crontab |
| `crontab -e` | SC | Edit/install current crontab with format checking |
| `crontab -r` | SC destructive | Remove current crontab |
| `/etc/crontab`, `/etc/cron.d` | SC config | System-wide schedules, with explicit user field |
| `/etc/cron.daily` | config/scripts | Directory whose scripts are usually invoked by system cron configuration |

Source cron examples:

```text
15 09 * * * /home/juser/bin/spmake
15 09 14 * * /home/juser/bin/spmake
15 09 5,14 * * /home/juser/bin/spmake
42 6 * * * root /usr/local/bin/cleansystem > /dev/null 2>&1
```

The final line is structurally normalized to remove an embedded footnote marker after `root`; see `source-findings.md`.

## 5. systemd timer scheduling

Timer unit source:

```ini
[Unit]
Description=Example timer unit

[Timer]
OnCalendar=*-*-* *:00,20,40
Unit=loggertest.service

[Install]
WantedBy=timers.target
```

Service source:

```ini
[Unit]
Description=Example Test Service

[Service]
Type=oneshot
ExecStart=/usr/bin/logger -p local3.debug I'm a logger
```

These are **SC configuration** when placed under `/etc/systemd/system`.

Observation/action commands:

| Command | Class | Purpose |
|---|---|---|
| `journalctl -f -u loggertest.service` | WG/RO | Follow service journal; source notes a race where unit field may be missing |
| `systemctl list-timers` | RO | Inspect timers including transient ones |
| `systemd-run --on-calendar='2022-08-14 18:00' /bin/echo this is a test` | SC/WG | Create transient timer + service |
| `systemd-run --on-active=30m ...` | SC/WG | Relative transient scheduling; command tail is source-described placeholder form |
| `loginctl enable-linger` | SC | Keep current user's user manager after logout |
| `loginctl enable-linger user` | SC privileged | Keep another user's manager after logout |

Source warning: using `--on-calendar` with a time but no future date can leave a timer that executes every day.

## 6. at

| Command | Class | Purpose |
|---|---|---|
| `at 22:30` | SC interactive scheduling | Read command(s) from stdin; Ctrl+D finishes |
| `at 22:30 30.09.15` | SC | Schedule source example date/time |
| `atq` | RO | List queued jobs |
| `atrm` | SC | Remove queued job; job identifier required by actual use but source snippet does not show one |

## 7. UID / setuid diagnostics and config

| Item | Class | Purpose / risk |
|---|---|---|
| `ps -eo pid,euser,ruser,comm` | RO | Compare effective and real users |
| setuid executable experiment | SC/high risk | Chapter suggests a temporary demonstration using a copy of `sleep`; exact command sequence not provided and is not reconstructed |
| `Defaults stay_setuid` in `/etc/sudoers` | SC privileged config | Changes sudo UID behavior; source explicitly warns of side effects |

Do **not** create a setuid shell: the chapter uses this as a security-danger explanation, not as an exercise to execute.

## 8. PAM

Read-only discovery:

```sh
man -k pam_
locate pam_unix.so
grep password.*unix /etc/pam.d/*
```

Configuration paths: `/etc/pam.d`, older `/etc/pam.conf`, fallback `/etc/pam.d/other`, and additional module data under `/etc/security`.

Source rule examples:

```text
auth requisite pam_shells.so

auth sufficient pam_rootok.so
auth requisite  pam_shells.so
auth sufficient pam_unix.so
auth required   pam_deny.so

auth sufficient pam_unix.so nullok

password sufficient pam_unix.so obscure sha512
```

These are **SC authentication policy** if edited. `nullok` permits a user without a password in the described module context. The source also warns that some PAM files are generated; read their comments before editing.

## Command discipline

- Exact current usernames, UIDs/GIDs, dates, unit names, timezone and scheduler ownership are **[Needs confirmation]**.
- Authentication/account/scheduler changes require verification and saved prior state.
- No command absent from chapter RAG is added to provide a convenient rollback.
