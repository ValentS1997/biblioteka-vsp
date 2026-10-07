# Команды и интерфейсы — глава 6 «Запуск пользовательского пространства»

**Provenance:** `p0176:c01`–`p0207:c01`, PDF/печатные страницы 176–207. Включены только команды и конфигурационные элементы, явно поддержанные RAG главы. `unit`, `unit_name`, `test1.target`, `echo.socket` и другие имена примеров — placeholders/учебные объекты автора.

Классы: **RO** — read-only; **WG** — workload-generating / interactive observation; **SC** — state-changing.

## 1. systemd: наблюдение

| Команда | Класс | Назначение | PDF |
|---|---|---|---:|
| `systemd-analyze dot` | WG/RO | Dependency graph; полный граф может быть очень большим | 180 |
| `systemctl -p UnitPath show` | RO | Effective systemd unit search path | 181 |
| `pkg-config systemd --variable=systemdsystemunitdir` | RO | Distribution unit directory | 181 |
| `pkg-config systemd --variable=systemdsystemconfdir` | RO | Local system configuration directory | 181 |
| `systemctl list-units` | RO | Active units; `--full`, `--all` discussed | 183 |
| `systemctl status sshd.service` | RO | State, process/cgroup and recent logs for example service | 183–184 |
| `systemd-cgls` | RO | System control-group hierarchy | 184 |
| `journalctl --unit=unit_name` | RO | Journal for chosen unit | 184 |
| `systemctl list-jobs` | RO | Current systemd jobs and waiting/running state | 184–185 |
| `systemctl show -p type unit` | RO | Query dependency/property named by placeholder `type` | 189 |

The exact property substituted for `type` must come from the diagnostic question (e.g. the text discusses Wants/Requires); do not silently rewrite the source command.

## 2. systemd: runtime and persistent state changes

| Команда / action | Класс | Effect | Verification | Rollback |
|---|---|---|---|---|
| `systemctl start unit` | SC | Activate unit/dependencies | `status`, `list-jobs` | `stop` only if prior state known |
| `systemctl stop unit` | SC | Deactivate unit | `status` | `start` only if prior state known |
| `systemctl restart unit` | SC | Restart unit | `status`, journal | [Needs confirmation] |
| `systemctl reload unit` | SC | Reload unit/service configuration | `status`, journal | [Needs confirmation] |
| `systemctl daemon-reload` | SC manager state | Reload all unit definitions | Recheck unit state/config behavior | [Needs confirmation] |
| `systemctl enable unit` | SC persistent | Create dependency symlink(s) from `[Install]` | Command output + future dependency | `disable unit` if previous state was disabled |
| `systemctl disable unit` | SC persistent | Remove enable-created symlink(s) | Command output | `enable unit` if previous state was enabled |
| `systemctl start test2.target` | SC example | Activates test target and its Wants dependency | Status both test targets | Stop/remove test units when safe: [Needs confirmation] |
| `systemctl status test1.target test2.target` | RO | Validate example targets active | Both target states shown | [Not applicable] |
| `systemctl start echo.socket` | SC/WG | Opens resource/socket activation example | Status / client test | `systemctl stop echo.socket` |
| `systemctl stop echo.socket` | SC | Stops example socket activation | Status | Restart if prior state required |

### Unit-file changes from source

Local files are created under `/etc/systemd/system`; distribution-owned unit definitions are typically under `/lib/systemd/system` or `/usr/lib/systemd/system` and should not be locally edited (§6.3.3).

Source-confirmed unit/config keys include:

- `[Unit]`: `Description=`, `Documentation=`, `Requires=`, `Wants=`, `Requisite=`, `Conflicts=`, `Before=`, `After=`, `ConditionPathExists=`, `ConditionPathIsDirectory=`, `ConditionFileNotEmpty=`, `DefaultDependencies=no`.
- `[Service]`: `ExecStart=`, `ExecStartPre=`, `ExecReload=`, `EnvironmentFile=`, `Type=simple|forking|notify|dbus|oneshot|idle`, `RemainAfterExit=yes`, `StandardInput=socket`.
- `[Socket]`: `ListenStream=22222`, `Accept=true`.
- `[Install]`: `WantedBy=`, `RequiredBy=`.
- Specifiers/variables: `$MAINPID`, environment variables, `%n`, `%H`, `%I`, `%i`, instance naming with `@`.

These are configuration syntax, not commands. Production values and dependencies remain **[Needs confirmation]**.

## 3. Socket activation example

| Source example | Класс | Purpose | Risk |
|---|---|---|---|
| `systemctl start echo.socket` | SC/WG | Start TCP listener on example port 22222 | Opens resource and creates service instances |
| `telnet localhost 22222` | WG | Exercise the echo service | Generates local network/session workload |
| `Ctrl+]`, then `Ctrl+D` | Interactive | Leave telnet session | [Not applicable] |
| `systemctl stop echo.socket` | SC | Stop socket unit | Ends future activation |

The chapter notes that `telnet` may not be installed. No package-install command is supplied, so none is added.

## 4. System V / runlevels

| Command / interface | Class | Effect | PDF |
|---|---|---|---:|
| `who -r` | RO | Current System V runlevel | 197 |
| `/etc/inittab` | config | Central System V init configuration | 198–199 |
| `less` on an rc/init script | RO | Inspect script contents; exact filename varies | 200 |
| `init.d/httpd start` / `httpd stop` | SC | Manually start/stop example service via init script | 201 |
| `mv S99httpd _S99httpd` | SC persistent | Disable rc link by renaming while preserving original name | 201 |
| `run-parts` | WG/SC depending directory | Executes multiple programs from a directory in order | 202 |
| `telinit 3` | SC system-wide | Switch System V runlevel | 202 |
| `telinit q` | SC manager config | Ask init to reread `inittab` | 202 |
| `telinit s` | SC system-wide | Enter single-user mode | 202 |

Changing runlevel may stop processes not present in the new `inittab` state; source explicitly warns to be careful.

## 5. Shutdown and reboot

| Command | Class | Effect | Verification / rollback |
|---|---|---|---|
| `shutdown -h now` | SC high-impact | Ordered immediate halt | System halts; rollback [Needs confirmation] |
| `shutdown -r +10` | SC high-impact | Schedule reboot in 10 minutes | Users are notified; system reboots; rollback [Needs confirmation] |
| `reboot`, `halt`, `poweroff` | SC high-impact | Helpers used in shutdown path; behavior depends on state | [Needs confirmation] |
| force option `-f` with reboot/halt | SC **high risk** | Immediate/forced path in context described | Potential damage; no safe rollback |

Orderly shutdown described by source: ask processes to exit → TERM → KILL if necessary → lock/prep → unmount → root read-only → `sync` → kernel `reboot(2)`.

For delayed shutdown, source states `/etc/nologin` may be created, preventing non-root logins.

## 6. initramfs and recovery

| Tool/action | Class | Purpose | Boundary |
|---|---|---|---|
| `unmkinitramfs` | RO/extraction | Unpack modern initramfs archives for inspection | Exact archive path/options not supplied |
| `cpio(1)` | documentation/tool reference | Older compressed initramfs archive format | Exact extraction command not supplied |
| `mkinitramfs` | SC build tool | Create initramfs | Exact command/options not supplied |
| `dracut` | SC build tool | Create initramfs | Exact command/options not supplied |
| Delete `initrd` line in temporary GRUB editor | SC boot attempt | Test whether kernel can boot without initramfs | **Temporary only**; boot can fail |
| `-s` boot parameter | boot-state change | Request single-user mode in chapter's model | Actual init implementation may differ |
| `rescue.target` | systemd target concept | systemd representation of rescue/single-user mode | Exact activation command not supplied |

The source recommends live/recovery media as a practical recovery option and lists use cases: filesystem checking, password reset, fixing `/etc/fstab`/`/etc/passwd`, restoring backups. It does not provide a complete command sequence for those tasks in this chapter.

## Discipline

1. **Observe before changing:** status, jobs, logs, UnitPath.
2. **Keep local config in `/etc/systemd/system`**, not distribution unit directories.
3. **Enabled ≠ active.**
4. **Wants/Requires ≠ Before/After.**
5. System-wide actions such as runlevel changes, shutdown and initramfs rebuilds require explicit recovery/rollback planning; unsupported details remain **[Needs confirmation]**.
