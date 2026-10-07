# Mermaid — глава 7 «Настройка системы»

Источник: **RAG `p0208:c01`–`p0243:c01`**, PDF/печатные страницы 208–243. Диаграммы — аналитическое представление текстовых связей главы; оригинальные рисунки 7.1–7.4 не реконструируются.

## 1. Диагностика через journald

```mermaid
flowchart TD
  P["Проблема / событие"] --> T["Ограничить время: journalctl -S / -b"]
  T --> U["Ограничить unit: -u"]
  U --> F["Поле / PID: _PID=... / -F / -N"]
  F --> G["Regex text: -g"]
  G --> PR["Severity: -p"]
  PR --> CTX["Расширить временной контекст вокруг совпадения"]
  CTX --> E["Evidence for next action"]
```

Глава прямо рекомендует начинать troubleshooting с журналов и использовать time/unit filters вместо чтения всего потока (§7.1.1–7.1.2).

## 2. Logging stack

```mermaid
flowchart LR
  APP["Application / service"] --> J["journald"]
  APP --> S["syslog / rsyslog / syslog-ng"]
  J --> BIN["/var/log/journal"]
  S --> TXT["Traditional files under /var/log"]
  J --> S
  S --> REM["Remote / DB destinations"]
  ROT["logrotate"] --> TXT
```

journald and syslog may coexist; syslog is historically useful for aggregation, while journald emphasizes structured collection on one host (§7.1.3–7.1.5).

## 3. User/account mapping

```mermaid
flowchart TD
  NAME["Username"] --> PW["/etc/passwd"]
  PW --> UID["UID + primary GID + home + shell"]
  PW --> SH["x → /etc/shadow auth data"]
  UID --> K["Kernel sees numeric identity"]
  G["/etc/group"] --> GID["Group IDs + supplementary members"]
  GID --> K
  PAM["PAM authentication policy"] --> AUTH["Login / chsh / passwd / other apps"]
  SH --> PAM
```

Names/password policy live in user space; kernel authorization centers on numeric IDs and setuid transitions (§7.3, §7.9).

## 4. Time layers

```mermaid
flowchart TD
  RTC["RTC hardware clock"] --> BOOT["Kernel initializes system clock"]
  NET["Network time daemon"] --> SYS["System clock"]
  BOOT --> SYS
  SYS --> UTC["Epoch / UTC representation"]
  UTC --> TZ["/etc/localtime / TZ conversion"]
  TZ --> APP["date / user-visible local time"]
```

Source advises network synchronization for drift instead of abrupt manual correction (§7.5).

## 5. Scheduling choices

```mermaid
flowchart TD
  TASK["Need future execution"] --> REP{"Recurring?"}
  REP -->|Yes| CRON["cron / crontab"]
  REP -->|Yes| TIMER["systemd timer + service"]
  REP -->|No| AT["at"]
  REP -->|No| TRANS["systemd-run transient timer"]
  CRON --> VERIFY1["crontab -l"]
  TIMER --> VERIFY2["systemctl list-timers + journal"]
  AT --> VERIFY3["atq"]
  TRANS --> VERIFY2
```

cron is simpler/portable; systemd timers add cgroup/process tracking, richer timing/dependencies and journal integration (§7.6–7.8).

## 6. UID semantics

```mermaid
flowchart LR
  PROC["Process"] --> R["ruid: initiator/owner context"]
  PROC --> E["euid: access/permission identity"]
  PROC --> S["saved UID"]
  SUID["setuid executable / setuid()"] --> E
  SUID --> R
  E --> FS["File/resource authorization"]
```

The chapter stresses that names/passwords are user-space concepts; kernel transitions operate on numeric user IDs (§7.9.1–7.9.2).

## 7. PAM stack control flow

```mermaid
flowchart TD
  APP["Application requests PAM function"] --> R1["Rule 1: function + control + module"]
  R1 --> C1{"Result + control"}
  C1 -->|sufficient success| OK["Return success"]
  C1 -->|requisite failure| FAIL["Return failure"]
  C1 -->|continue| R2["Next rule"]
  R2 --> C2{"required failure?"}
  C2 -->|Yes| MARK["Remember failure, continue stack"]
  C2 -->|No| R3["Continue"]
  MARK --> END["End of stack → failure"]
  R3 --> END2["Final result"]
```

The concrete chsh example stacks `pam_rootok.so`, `pam_shells.so`, `pam_unix.so`, then `pam_deny.so` (§7.10.1).

## 8. Safe configuration-change boundary

```mermaid
flowchart TD
  O["Read-only baseline"] --> OWNER["Identify owning subsystem/file"]
  OWNER --> B["Capture current value/config + access path"]
  B --> CHANGE{"Change required?"}
  CHANGE -->|No| STOP["Keep state"]
  CHANGE -->|Yes| ACT["Narrow account/time/scheduler/PAM change"]
  ACT --> VERIFY["Readback / logs / auth test / schedule list"]
  VERIFY --> OK{"Acceptance?"}
  OK -->|Yes| KEEP["Keep"]
  OK -->|No| RB["Restore prior state or recovery path"]
```

For PAM/authentication especially, exact generic rollback is not provided by the chapter and must remain **[Needs confirmation]** unless captured before the change.
