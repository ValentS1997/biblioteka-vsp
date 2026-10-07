# Cheatsheet — глава 7 «Настройка системы»

**Источник:** `how-linux-works-brian-ward-3e-ru-2022:p0208:c01`–`p0243:c01`, PDF/печатные страницы 208–243. Только `rag_only`.

## Symptom / problem framing

Глава помогает локализовать проблемы и изменения в пяти основных областях user space:

1. журналы и диагностические сообщения;
2. пользователи/группы и account data;
3. системное время и timezone;
4. периодические/разовые задания;
5. authentication policy через PAM.

Главное ограничение: источник даёт механизмы и примеры, но не universal production change plan. Если target account, PAM stack, scheduler ownership или rollback не подтверждены, состояние остаётся **[Needs confirmation]**.

## Baseline / context

| Область | Базовая модель главы | PDF |
|---|---|---:|
| Logging | journald, syslog/rsyslog/syslog-ng, `/var/log`, facility/severity | 209–217 |
| Config | host-specific configuration обычно под `/etc` | 218 |
| Accounts | `/etc/passwd`, `/etc/shadow`, `/etc/group` | 218–223 |
| Login | getty → login → shell; PAM handles much of authentication | 223–224 |
| Time | kernel clock, RTC, UTC, `/etc/localtime`, network time | 224–226 |
| Recurring jobs | cron/crontab or systemd timer + service | 226–230 |
| One-shot jobs | `at` or transient systemd timer | 230–232 |
| UID model | euid, ruid, saved UID, setuid mechanics | 232–235 |
| PAM | `/etc/pam.d`, function + control + module stack | 237–243 |

## Read-only checks

### Logging

```sh
journalctl
journalctl -r
journalctl -S -4h
journalctl -u cron.service
journalctl -F _SYSTEMD_UNIT
journalctl -N
journalctl -g 'kernel.*memory'
journalctl -b
journalctl -b -1
journalctl --list-boots
journalctl -k
journalctl -p 3
journalctl -f
```

Also source-supported: field filters such as `journalctl _PID=8792`, severity range `-p 2..3`, traditional `tail -f` / `less +F` for text logs.

### Users / processes / PAM

```sh
groups
ps ao args | grep getty
ps -eo pid,euser,ruser,comm
man -k pam_
locate pam_unix.so
grep password.*unix /etc/pam.d/*
```

### Time / scheduling

```sh
date
date +%s
tzselect
crontab -l
atq
systemctl list-timers
```

**Caveats:** `journalctl` visibility may require elevated/group access; `locate` may depend on its index; `systemctl list-timers` is used to observe transient timers created by `systemd-run`.

## Interpretation

| Observation | Meaning in chapter | Still unchecked |
|---|---|---|
| `journalctl` works | journald is active enough to return records | Whether rsyslog/syslog-ng also persists text logs |
| `journalctl -b -1` ends with orderly shutdown messages | Previous boot appears to have shut down correctly | Application/data integrity beyond logs |
| `/etc/passwd` field 2 is `x` | Password data is expected in shadow storage | Actual authentication method may involve PAM/other backends |
| User has UID 0 | Kernel treats that identity as superuser | Policy intent / whether account should exist |
| `groups` lists supplementary groups | User-space group memberships visible | Effective authorization for a particular resource |
| `date` differs from expected wall time | Could involve kernel clock/timezone/synchronization | Exact layer causing the mismatch |
| crontab entry exists | cron will consider it according to its schedule | Job success/output/environment |
| systemd timer exists | Schedule unit exists | Linked service execution/result |
| euid ≠ ruid | Process is executing with different effective identity | Whether behavior is safe/intended |
| PAM rule uses `sufficient` | Success may short-circuit remaining rules | Other preceding/remaining stack semantics |

## Next action

1. **Logs:** filter first by time/boot/unit before broad text search.
2. **Accounts:** identify whether issue is mapping (`passwd/group`), password data (`shadow`), or PAM policy.
3. **Time:** separate system clock, RTC, timezone and network synchronization.
4. **Jobs:** identify owner and scheduler (user crontab, system crontab, timer, at).
5. **PAM:** map application → PAM file → function stack before changing any rule.
6. If change impacts login/authentication or scheduled privileged work, preserve a tested access/recovery path first.

## Modifying action

| Source-supported action | Effect | Risk |
|---|---|---|
| `passwd`, `passwd user` | Changes password credentials | Account access changes; verify correct user |
| `chfn`, `chsh` | Changes account metadata/shell | Invalid shell/account state can affect login |
| `adduser`, `userdel` | Adds/removes account | UID/files/home/process ownership impact |
| `vipw`, `vipw -s` | Guarded direct edit of passwd/shadow | **High risk**; malformed entry may break account lookup/auth |
| `hwclock --systohc --utc` | Copies system time to RTC in UTC mode | Wrong system time becomes persistent RTC state |
| Copy/symlink zoneinfo to `/etc/localtime` | Changes system timezone | Alters displayed local time and job interpretation |
| `export TZ=...` | Changes timezone for current shell | Session-local; rollback by restoring prior environment |
| `crontab file`, `crontab -e` | Installs/edits recurring user jobs | Future commands execute automatically |
| `crontab -r` | Removes user's crontab | Can delete all recurring jobs for that user |
| Edit `/etc/crontab` / `/etc/cron.d` | Changes system jobs | Privileged recurring execution; wrong user/schedule dangerous |
| Create timer/service under `/etc/systemd/system` | Adds persistent scheduled unit | Requires unit validation and lifecycle management |
| `at 22:30` | Schedules one-shot commands from stdin | Future execution may be forgotten |
| `atrm` | Removes queued at job | Wrong job ID removes another scheduled task |
| `systemd-run --on-calendar=...` | Creates transient timer/service | A date omission may cause recurring behavior per source warning |
| `loginctl enable-linger [user]` | Keeps user manager after logout | User services/timers continue without logged-in session |
| PAM file edits | Changes authentication/authorization stack | **Critical risk:** can deny legitimate access or weaken auth |
| `Defaults stay_setuid` in sudoers | Alters UID handling for sudo-launched programs | Source warns of side effects |

## Verification / acceptance checks

| Change | Verification from chapter | Acceptance |
|---|---|---|
| Password/account change | Login/auth path + relevant account files/tools | Expected user authenticates; wrong/unauthorized user does not |
| Group change | `groups` / account mapping | Intended membership visible; authorization effect separately verified |
| RTC/timezone | `date`, `date +%s`; session TZ test | Expected wall time/UTC representation |
| cron edit | `crontab -l` | Exact expected entry present |
| at job | `atq` | Intended job/time visible |
| systemd transient timer | `systemctl list-timers` | Correct future activation time |
| logging filter | Known event appears under intended time/unit/boot filter | Evidence set is sufficient for diagnosis |
| PAM edit | Source gives no safe end-to-end validation workflow | **[Needs confirmation]**; preserve alternate authenticated session/recovery path |

## Rollback

- Account/password changes: inverse/recovery procedure depends on the prior credential/account state; **[Needs confirmation]** unless captured beforehand.
- `vipw` creates backup/locking behavior per source, but exact restore filename/command is not supplied: **[Needs confirmation]**.
- Session-only `TZ`: restore/unset previous environment value.
- Crontab: preserve prior `crontab -l` output before editing; source does not define a restore command sequence, so rollback from saved content is **[Needs confirmation]**.
- `at`: queued job can be removed with `atrm` if its job identity is known.
- `loginctl enable-linger`: inverse command is not supplied in chapter RAG, therefore **[Needs confirmation]**.
- PAM: no safe generic rollback sequence is given. A known-good access path and saved config are mandatory before change; otherwise **STOP**.
- Time/RTC changes: previous values are not automatically retained by source examples; capture before change or rollback is **[Needs confirmation]**.

## Guardrails

- Empty password fields in `/etc/passwd` are explicitly warned against.
- Do not directly edit account databases casually; concurrency and syntax errors are reasons to use dedicated tools.
- Do not treat `enabled/installed scheduler entry` as proof that the task executed successfully.
- PAM generated files may be overwritten; read comments before editing.
- Source examples of `nullok`, UID 0, setuid, sudoers, cron root jobs and PAM stacks are explanatory and not baseline security recommendations.
