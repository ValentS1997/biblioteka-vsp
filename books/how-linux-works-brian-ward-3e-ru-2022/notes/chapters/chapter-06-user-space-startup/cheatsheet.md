# Cheatsheet — глава 6 «Запуск пользовательского пространства»

**Source:** `how-linux-works-brian-ward-3e-ru-2022:p0176:c01`–`p0207:c01`, PDF/печатные страницы 176–207. Только `rag_only`.

## Symptom / problem framing

Глава помогает определить **какая init-система используется, какой systemd unit находится в нужном состоянии, какие зависимости/задания блокируют запуск, где лежит unit file, как service type влияет на readiness, и что происходит при shutdown или initramfs handoff**. Она не является универсальным incident runbook для любого сервиса.

## Baseline / context

| Объект | Смысл | PDF |
|---|---|---:|
| PID 1 / init | Первый user-space process; запускает/останавливает системные службы | 176–178 |
| systemd unit | Конкретная управляемая сущность: service/target/socket/mount и др. | 178–180 |
| `default.target` | Высокоуровневый target, активируемый при boot | 179–180 |
| Unit search path | Приоритет каталогов виден через `systemctl -p UnitPath show` | 181 |
| Distribution units | Обычно `/lib/systemd/system` или `/usr/lib/systemd/system` | 181 |
| Local units | Обычно `/etc/systemd/system`; туда автор рекомендует вносить локальные изменения | 181 |
| cgroups | systemd использует их для отслеживания процессов unit-а | 184,187 |
| Jobs | Запросы start/restart/state transition unit-ов | 184–185 |
| System V runlevel | Числовое состояние 0–6 для старой init model | 197–203 |
| initramfs | Early user space before the real root filesystem | 205–206 |

## Read-only checks

```sh
systemctl list-units
systemctl status unit
systemctl list-jobs
systemctl -p UnitPath show
systemd-cgls
journalctl --unit=unit_name
systemctl show -p type unit
systemd-analyze dot
pkg-config systemd --variable=systemdsystemunitdir
pkg-config systemd --variable=systemdsystemconfdir
who -r
```

Пояснения:

- `systemctl list-units` показывает active units; `--full` и `--all` упомянуты для полного имени и неактивных units (§6.3.4).
- `systemctl status unit` показывает state, tracked process/cgroup and recent journal lines (§6.3.4).
- `systemctl list-jobs` помогает увидеть waiting/running jobs during boot (§6.3.4).
- `journalctl --unit=unit_name` показывает все сообщения выбранного unit-а (§6.3.4).
- `systemd-analyze dot` строит dependency graph; автор предупреждает, что полный граф типичной системы большой и тяжёлый для визуализации (§6.3.2).
- `systemctl show -p type unit` в источнике использует placeholder `type` для property вроде Wants/Requires; **не** подставлять значение без конкретной задачи (§6.3.6).
- `who -r` относится к System V/runlevel context (§6.4).

Определение init system в §6.2 дано через наличие каталогов/files (`/usr/lib/systemd`, `/etc/systemd`, `/etc/init`, `/etc/inittab`), но конкретная shell-команда проверки в тексте не задана.

## Interpretation

| Наблюдение | Интерпретация из главы | Неизвестное |
|---|---|---|
| `systemctl status`: active/running | Unit активен, cgroup показывает связанные процессы | Application-level health: [Needs confirmation] |
| `list-jobs`: unit waiting | Его активация ожидает завершения другого job/dependency | Точный blocker требует dependency/status analysis |
| `Loaded: ... /usr/lib/systemd/system/...` | Unit file принадлежит distribution path | Local override location/value: [Needs confirmation] |
| `UnitPath=...` | Показывает реальные search paths и priority | Какой файл effective без конкретного unit readback: [Needs confirmation] |
| `Type=simple` | Main process не fork-ится; readiness не сигнализируется отдельно | Когда service фактически готов к requests: [Needs confirmation] |
| `Type=forking` | Parent exits after fork; systemd считает service ready afterward | Correct PID/process behavior depends on service |
| `Type=notify/dbus` | Service explicitly signals readiness / registers on D-Bus | Correct implementation by specific daemon: [Needs confirmation] |
| `Wants=` failure | Failure dependency не обязана stop dependent unit | Ordering still requires separate Before/After |
| `Requires=` failure | Failure propagates to dependent unit | Whether strict dependency is desirable: [Needs confirmation] |
| `enable` output creates `.wants/` symlink | Persistent dependency is installed | Unit is **not** necessarily running now |
| `who -r` | Current System V runlevel | systemd target mapping is not inferred here |

## Next action

1. Identify the init model and the exact unit/service in question.
2. Capture state with `systemctl status`, `list-jobs`, logs and relevant dependency property.
3. Confirm the effective unit search path before editing anything.
4. Prefer local changes under `/etc/systemd/system`; do not modify distribution-owned `/usr`/`/lib` unit files per chapter guidance.
5. If a unit file changed, use the appropriate configuration reload path and verify state/logs afterward.
6. If dependency semantics or rollback are not understood, stop: **[Needs confirmation]**.

## Modifying action

| Действие из главы | Эффект | Риск |
|---|---|---|
| `systemctl start unit` | Активирует unit and dependencies | Может запустить daemon/mount/socket and workload |
| `systemctl stop unit` | Деактивирует unit | Может остановить critical service/dependents |
| `systemctl restart unit` | Stop + start transition | Service interruption / state loss depending on daemon |
| `systemctl reload unit` | Reloads service-specific configuration | Supported only if unit/service defines it |
| `systemctl daemon-reload` | Reloads all unit configuration into systemd manager | Does **not** by itself guarantee service restart/state change |
| `systemctl enable unit` | Creates persistent dependency symlink(s) from `[Install]` | Affects future boot/activation; **does not start unit** |
| `systemctl disable unit` | Removes symlink(s) created by enabling | Does not necessarily stop an active unit |
| Creating unit files under `/etc/systemd/system` | Adds new local systemd configuration | Wrong dependencies/ExecStart can break service startup |
| `systemctl start echo.socket` | Activates demonstration socket on TCP 22222 | Opens local listener/resource; test workload |
| `systemctl stop echo.socket` | Stops demonstration socket activation | Active service instances/resources may be affected |
| `telinit 3`, `telinit s` | Changes System V runlevel / single-user mode | Broad system state transition |
| `telinit q` | Requests System V init reread `inittab` | Applies changed init configuration |
| `shutdown -h now`, `shutdown -r +10` | Ordered halt/reboot | System-wide interruption; data/service impact |
| `reboot/halt ... -f` | Force path can bypass orderly shutdown behavior | **High risk**; chapter warns of potential damage |
| Removing `initrd` line in temporary GRUB editor | Tests boot without initramfs for current attempt | Boot may fail if drivers/root discovery require initramfs |

## Verification / acceptance checks

| Change | Проверка из главы | Acceptance |
|---|---|---|
| start/stop/restart | `systemctl status unit`, `list-jobs`, journal | Expected ACTIVE/SUB state and no unresolved blocking job |
| reload / daemon-reload | `systemctl status` + effective behavior/logs | Exact config-readback command not specified: [Needs confirmation] |
| enable/disable | Command output shows symlink create/remove; status can be checked separately | Remember: enabled ≠ active |
| custom target dependency | Status both target units; activation of dependent unit occurs as designed | Example only; production dependency design [Needs confirmation] |
| socket activation | Connect to local port with source example; service echoes data | Test tool/environment availability [Needs confirmation] |
| shutdown/reboot | System reaches halt/reboot and services/filesystems close orderly | Rollback after shutdown start: [Needs confirmation] |
| initramfs experiment | Successful boot reaches real root/full init | Failed attempt requires known-good GRUB entry/recovery path |

## Rollback

- `start` ↔ `stop` can be inverse actions **only if the previous state and dependency impact were captured**. Otherwise rollback: **[Needs confirmation]**.
- `enable` ↔ `disable` are explicit inverse persistent-link operations in the chapter; confirm whether the unit should also be active/stopped separately.
- Unit-file edits should retain the prior file/configuration before change; the chapter does not give a complete file-backup/restore command sequence: **[Needs confirmation]**.
- System V link-farm example recommends renaming `S99httpd` to `_S99httpd` rather than deleting it, preserving the original name for reversal (§6.5.2).
- Shutdown/reboot cannot be treated as a normal transactional change once the system is terminating; recovery depends on successful next boot.
- Temporary GRUB edit that removes `initrd` is non-persistent; reboot/select known-good configuration if available. Persistent GRUB modification is explicitly discouraged for this experiment (§6.7).

## Operational cautions

- Do not equate **enabled** with **active**.
- Do not express ordering only with `Wants`/`Requires`; `Before`/`After` are separate.
- Avoid strict dependencies that unnecessarily prevent login/recovery services from starting (§6.3.6 example).
- Do not edit packaged unit files under `/usr`/`lib` when a local `/etc/systemd/system` definition is intended.
- Current host unit names, initramfs implementation, runlevels and rescue behavior remain **[Needs confirmation]**.
