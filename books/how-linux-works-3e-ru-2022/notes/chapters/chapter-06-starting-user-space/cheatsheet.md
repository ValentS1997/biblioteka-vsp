# Шпаргалка: systemd и запуск user space по главе 6

Цель: локализовать проблему между PID 1, unit dependencies, service process и resource activation до изменения конфигурации.

## Init implementation

Source-derived признаки:

- systemd: каталоги `/usr/lib/systemd` и `/etc/systemd`;
- Upstart: `/etc/init/*.conf`;
- System V: `/etc/inittab`, если предыдущие признаки отсутствуют.

## Read-only baseline

```bash
systemctl list-units
systemctl status sshd.service
systemctl list-jobs
journalctl --unit=unit_name
systemctl -p UnitPath show
pkg-config systemd --variable=systemdsystemunitdir
pkg-config systemd --variable=systemdsystemconfdir
systemd-cgls
```

Для `list-units` источник также упоминает `--full` и `--all`.

Из `systemctl status` брать:

- Loaded path;
- enabled/static state;
- Active state;
- Main PID;
- process/cgroup tree;
- последние journal messages.

## Configuration boundary

```text
vendor/distribution:
  /usr/lib/systemd/system
  /lib/systemd/system

local changes:
  /etc/systemd/system
```

Правило главы: локальные изменения размещать в `/etc`, не переписывая distribution files.

## Unit lifecycle

```text
start         → activate
stop          → deactivate
restart       → restart
reload        → reload one unit/service configuration
daemon-reload → reread all unit files
```

После изменения unit file systemd должен перечитать configuration.

## Enable != start

```text
systemctl enable unit
   ↓
dependency symlink
   ↓
future boot/activation graph

systemctl start unit
   ↓
unit active now
```

`disable` удаляет enablement links; это отдельное действие от `stop`.

## Dependencies

| Directive | Смысл |
|---|---|
| `Requires` | strict dependency; failure dependency влияет на dependent unit |
| `Wants` | activation dependency без обязательного failure propagation |
| `Requisite` | dependency уже должна быть active |
| `Conflicts` | units не должны быть active одновременно |
| `Before` | текущий unit раньше указанного |
| `After` | текущий unit позже указанного |

Activation dependency и ordering dependency — разные механизмы.

Conditional examples из главы:

- `ConditionPathExists=`;
- `ConditionPathIsDirectory=`;
- `ConditionFileNotEmpty=`.

## Service Type

```text
simple   → основной process остаётся основным service process
forking  → parent fork/exit, daemon продолжает работу
notify   → service сообщает systemd о ready state
dbus     → readiness через D-Bus registration
oneshot  → operation завершается без дочерних процессов
idle     → запуск откладывается до завершения текущих jobs
```

Cgroups позволяют systemd отслеживать process descendants.

## Socket/resource activation

```text
resource unit active
      ↓
systemd monitors/listens
      ↓
request arrives
      ↓
input buffers
      ↓
service unit starts
      ↓
service takes over resource
```

Пример главы:

- `echo.socket`;
- `echo@.service`;
- TCP port 22222;
- `Accept=true` создаёт отдельный service instance на connection.

## System V mental model

```text
/etc/inittab
   ↓ runlevel
/etc/rcN.d/
   ↓ Sxx/Kxx symlinks
/etc/init.d/script
   ↓
service process
```

- `S` → start;
- `K` → stop;
- number → execution order;
- `who -r` показывает текущий runlevel;
- `telinit` меняет runlevel или перечитывает init configuration.

## Managed shutdown

Источник показывает:

```bash
shutdown -h now
shutdown -r +10
```

Normal sequence:

1. notify users;
2. terminate processes;
3. TERM, затем KILL для оставшихся;
4. unmount filesystems;
5. root → read-only;
6. sync buffered data;
7. kernel reboot/halt.

## Initramfs

```text
bootloader loads kernel + initramfs
        ↓
kernel mounts temporary RAM filesystem
        ↓
init inside initramfs
        ↓
load required storage/root modules
        ↓
mount real root
        ↓
switch to real root
        ↓
start full init
```

Tools, названные источником:

- `unmkinitramfs`;
- `mkinitramfs`;
- `dracut`;
- `cpio(1)` для старых archives.

Глава не задаёт универсальную manual rebuild procedure.

## Recovery

Источник предпочитает live/rescue image для:

- filesystem repair;
- исправления critical configuration files;
- восстановления backups;
- других recovery tasks.

Single-user alternatives:

- System V runlevel 1;
- systemd `rescue.target`;
- boot parameter `-s`.

Источник отмечает, что single-user mode может не иметь network/UI и удобного terminal.

## Verification / acceptance

Для systemd change:

- unit file находится в ожидаемом local path;
- configuration перечитана;
- `systemctl status` показывает ожидаемый state;
- journal не содержит нового unexpected failure;
- dependencies/order соответствуют intended graph;
- enablement и runtime activation не перепутаны.

## Rollback

- local unit change: вернуть предыдущий local unit file/override и перечитать configuration;
- `enable` → `disable` удаляет enablement symlink;
- service stop/start обратимы только если service state и application semantics это допускают;
- runlevel/shutdown/initramfs/recovery changes: `[Needs confirmation]` без конкретной системы.
