# Шпаргалка: system configuration по главе 7

## Symptom / problem framing

Типовые задачи:

- найти причину service/system failure в journal;
- понять, почему scheduled task не запускается;
- проверить user identity/group membership;
- отличить system clock, RTC и timezone issue;
- понять privilege context process;
- локализовать authentication failure в PAM.

## Baseline / context

Ключевые state stores:

`/var/log` — традиционные log files;  
`/var/log/journal` — persistent journald storage, если используется;  
`/etc` — system configuration;  
`/etc/passwd` — user mapping;  
`/etc/shadow` — password/authentication data;  
`/etc/group` — group mapping;  
`/etc/localtime` — system timezone;  
`/usr/share/zoneinfo` — timezone database;  
`/var/spool/cron/crontabs` — user crontabs;  
`/etc/crontab` и `/etc/cron.d` — system cron configuration;  
`/etc/systemd/system` — local systemd timer/service units;  
`/etc/pam.d` — PAM application configuration.

## Read-only checks

### Journal

```bash
journalctl
journalctl -S -4h
journalctl -u cron.service
journalctl -F _SYSTEMD_UNIT
journalctl -N
journalctl -g 'kernel.*memory'
journalctl -b
journalctl -b -1
journalctl --list-boots
journalctl -p 3
journalctl -p 2..3
journalctl -f
```

Workflow:
1. сузить time window;
2. сузить unit/field;
3. посмотреть соседние события;
4. при boot issue выбрать нужную boot session.

### User/group state

```bash
groups
ps -eo pid,euser,ruser,comm
```

Проверять:
- username → UID;
- primary GID и supplemental groups;
- EUID vs RUID у process.

### Time

```bash
date +%s
date
TZ=US/Central date
```

`TZ` позволяет проверить другое timezone representation без system-wide change.

### Scheduled jobs

```bash
crontab -l
atq
systemctl list-timers
```

## Interpretation

### Logging

Journald и syslog могут сосуществовать. Journal search лучше начинать с time/unit filter, а text search использовать как дополнительный метод.

File logs требуют rotation; journald сам управляет retention binary journal.

### User files

`/etc/passwd` содержит identity/account mapping, а не normal readable password. Символ `x` обычно означает, что password hash находится в `/etc/shadow`.

Root определяется UID 0.

`/etc/group` хранит group name, GID и optional member list.

### Time

- kernel system clock — текущее время ОС;
- RTC — hardware clock;
- timezone — user-space conversion/representation;
- network time corrects clock drift.

### Cron vs systemd timers

Cron:
- проще;
- широко совместим;
- удобен для user jobs.

Systemd timers:
- cgroup tracking;
- journal integration;
- dependencies;
- richer activation model.

Timer unit не содержит task logic: он активирует service unit.

### Identity / privilege

`EUID` — effective identity для permission checks.  
`RUID` — исходная user identity process.  
Saved UID позволяет некоторым setuid programs временно менять effective privilege.

Setuid-root binary — security boundary.

### PAM

PAM function types:
- `auth`;
- `account`;
- `session`;
- `password`.

Control flow:
- `sufficient` — success может завершить evaluation;
- `requisite` — failure немедленно завершает evaluation;
- `required` — failure сохраняется, но последующие rules продолжают выполняться.

## Next action

### Logging problem
journal → time/unit filter → relevant neighboring events → service/config layer.

### Scheduled job problem
подтвердить installed schedule → подтвердить timer/cron service → проверить journal/output → проверить execution identity/environment.

### User/auth problem
подтвердить UID/GID/files → определить EUID/RUID → определить PAM application file → прочитать rules/modules → только затем менять policy.

## Modifying action

Source-confirmed changes включают:

- `passwd` / `passwd user`;
- `adduser` / `userdel`;
- `vipw` / `vipw -s` для emergency direct edit;
- `hwclock --systohc --utc`;
- timezone file/symlink change;
- `crontab file` / `crontab -e` / `crontab -r`;
- создание systemd timer/service unit pair;
- `at` / `atrm`;
- `systemd-run --on-calendar=...`;
- `loginctl enable-linger`;
- PAM configuration edits.

PAM/user database changes считать security-critical.

## Verification / acceptance checks

| Change | Verification |
|---|---|
| user/password | user mapping + successful expected authentication |
| group | `groups` / expected file access |
| timezone | `date` and/or one-shot `TZ=... date` comparison |
| RTC sync | compare expected system/RTC behavior after controlled sync |
| crontab | `crontab -l` + output/log of task |
| at job | `atq` |
| systemd timer | `systemctl list-timers` + journal/service result |
| linger | user timer survives logout as intended |
| PAM | expected login/auth path succeeds and unintended access stays denied |

## Rollback

- `crontab -e`: rollback procedure `[Needs confirmation]` unless a previous crontab was explicitly saved.
- `at` job: remove with `atrm` before execution.
- timer unit change: rollback procedure `[Needs confirmation]` within the verified chapter source.
- `TZ` environment override: one-command form ends with the command; rollback for an exported session value is `[Needs confirmation]` in this chapter.
- timezone/PAM/user database changes: `[Needs confirmation]` without a verified backup/recovery path.
- `loginctl enable-linger` reverse action is not provided by the source section used here: `[Needs confirmation]`.
