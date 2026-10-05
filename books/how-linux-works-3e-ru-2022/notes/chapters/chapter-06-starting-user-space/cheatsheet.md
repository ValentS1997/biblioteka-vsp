# Шпаргалка: systemd и запуск user space по главе 6

## Symptom / problem framing

Цель: локализовать проблему между PID 1, unit dependencies, service process и resource activation до изменения конфигурации.

Типовые симптомы главы:

- unit не запускается или долго находится в состоянии activation;
- service запущен не тогда, когда ожидается;
- зависимость блокирует дальнейший boot;
- после изменения unit file systemd использует старую конфигурацию;
- enablement и runtime state интерпретируются как одно и то же;
- boot доходит до initramfs, но не переходит к real root;
- требуется controlled shutdown или recovery environment.

## Baseline / context

Source-derived признаки init implementation:

- systemd: каталоги `/usr/lib/systemd` и `/etc/systemd`;
- Upstart: `/etc/init/*.conf`;
- System V: `/etc/inittab`, если предыдущие признаки отсутствуют.

Конфигурационная граница:

```text
vendor/distribution:
  /usr/lib/systemd/system
  /lib/systemd/system

local changes:
  /etc/systemd/system
```

Правило главы: локальные изменения размещать в `/etc`, не переписывая distribution files.

## Read-only checks

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

## Interpretation

### Unit lifecycle

```text
start         → activate
stop          → deactivate
restart       → restart
reload        → reload one unit/service configuration
daemon-reload → reread all unit files
```

### Enable != start

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

### Dependencies

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

### Service Type

```text
simple   → основной process остаётся основным service process
forking  → parent fork/exit, daemon продолжает работу
notify   → service сообщает systemd о ready state
dbus     → readiness через D-Bus registration
oneshot  → operation завершается без дочерних процессов
idle     → запуск откладывается до завершения текущих jobs
```

Cgroups позволяют systemd отслеживать process descendants.

### Socket/resource activation

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

Пример главы: `echo.socket`, `echo@.service`, TCP port 22222 и `Accept=true`.

### System V mental model

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

### Initramfs

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

Tools, названные источником: `unmkinitramfs`, `mkinitramfs`, `dracut`, `cpio(1)`.

## Next action

Для systemd troubleshooting:

1. определить проблемный unit;
2. получить `status` и unit journal;
3. проверить Loaded path, jobs, dependencies и ordering;
4. определить, требуется ли изменение unit file;
5. если требуется — менять только local configuration;
6. перечитать configuration;
7. повторно проверить status/journal.

Для раннего boot failure: определить, находится проблема в initramfs, переходе на real root или уже после запуска полного init.

## Modifying action

Подтверждённые source operations:

- `systemctl start/stop/restart unit`;
- `systemctl reload unit`;
- `systemctl daemon-reload`;
- `systemctl enable/disable unit`;
- source example с `echo.socket`;
- legacy `telinit` transitions;
- managed `shutdown`;
- initramfs generation tools `mkinitramfs` и `dracut` — без универсальной процедуры в главе.

Перед state change определить effect и affected unit/system scope. Для vendor unit files source рекомендует не редактировать их напрямую.

## Verification / acceptance checks

Для systemd change:

- unit file находится в ожидаемом local path;
- configuration перечитана;
- `systemctl status` показывает ожидаемый state;
- journal не содержит нового unexpected failure;
- dependencies/order соответствуют intended graph;
- enablement и runtime activation не перепутаны.

Для managed shutdown acceptance — система проходит normal termination/unmount/sync path, а не hard power-off.

Для initramfs recovery outcome зависит от конкретной distribution и boot state: `[Needs confirmation]`.

## Rollback

- local unit change: вернуть предыдущий local unit file/override и перечитать configuration;
- `enable` → `disable` удаляет enablement symlink;
- service stop/start обратимы только если service state и application semantics это допускают;
- runlevel/shutdown/initramfs/recovery changes: `[Needs confirmation]` без конкретной системы.

## Дополнение: managed shutdown и recovery

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

Для recovery источник предпочитает live/rescue image. Single-user alternatives: System V runlevel 1, systemd `rescue.target`, boot parameter `-s`.
