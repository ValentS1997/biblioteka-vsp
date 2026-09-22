# Команды главы 11

Только команды и формы команд, подтверждённые RAG главы 11.

| Команда | Назначение | Что проверить | Тип |
|---|---|---|---|
| `uname -r` | Показать running kernel version | version соответствует ожидаемой distribution/kernel line | read-only |
| `mknod <file> <type> <major> <minor>` | Вручную создать device file | type/major/minor совпадают с driver documentation | state-changing |
| `udevadm info -a -n sdb` | Показать udev attributes и parent chain для device | stable attributes, пригодные для rule matching | read-only |
| `udevadm info -a -p /block/sdb/sdb1` | Исследовать partition/device path относительно `/sys` | attributes/model/size/parent values | read-only |
| `lsusb` | Показать USB bus/device identifiers | vendor/product/device enumeration | read-only |
| `dmesg` | Посмотреть kernel ring buffer / boot-device messages | driver detection, attach/errors, panic/oops trace | read-only |
| `journalctl` | Альтернативно проверить kernel/device journal events в показанном workflow | device attach/detach messages | read-only |
| `sudo udevadm control --reload-rules` | Перезагрузить udev rules после изменения | new rules actually match intended device events | state-changing |
| `ls -l /dev/ate*` | Проверить созданную udev symlink в chapter example | symlink points to expected device | read-only |
| `mount \| grep ate` | Проверить automount result в example workflow | expected device mounted to intended path | read-only |
| `cat /proc/sys/fs/file-max` | Прочитать runtime kernel parameter | current open-file limit | read-only |
| `echo 32768 > /proc/sys/fs/file-max` | Изменить Linux kernel parameter напрямую через procfs | new runtime value; change is nonpersistent | state-changing |
| `sysctl net.ipv4.ip_forward=0` | Изменить Linux runtime kernel parameter через sysctl | forwarding state changed as intended | state-changing |
| `sysctl -a` | Показать доступные FreeBSD kernel parameters | tunables vs read-only parameters | read-only |
| `make xconfig` | GUI kernel configuration | generated `.config` matches intended options | state-changing / build-prep |
| `make gconfig` | GUI kernel configuration | generated `.config` | state-changing / build-prep |
| `make menuconfig` | Text UI kernel configuration | generated `.config` | state-changing / build-prep |
| `make config` | Sequential prompt-based kernel configuration | generated `.config`; chapter discourages routine use | state-changing / build-prep |
| `make oldconfig` | Reuse prior `.config` and prompt for new/changed options | old config migrated intentionally | state-changing / build-prep |
| `make clean` | Remove build leftovers before kernel compilation | stale build artifacts removed | state-changing |
| `make` | Compile Linux kernel tree | build succeeds | workload-generating |
| `make modules_install` | Install built kernel modules | modules installed for target kernel | state-changing |
| `make install` | Install built Linux kernel | kernel/boot artifacts installed | state-changing |
| `cd <kernel-source>; patch -p1 < <patch-file>` | Apply kernel source patch | patch applies cleanly to intended source tree | state-changing |
| `make buildkernel KERNCONF=MYCUSTOM` | FreeBSD: build custom kernel | build succeeds from intended config | workload-generating |
| `make installkernel KERNCONF=MYCUSTOM` | FreeBSD: install custom kernel | target kernel installed | state-changing |
| `lsmod` | Linux: list loaded kernel modules | module, size, reference count | read-only |
| `sudo modprobe snd-usb-audio` | Load Linux kernel module with dependency handling | module loaded; device/function appears | state-changing |
| `modprobe -r snd-usb-audio` | Remove module if reference count permits | module removed and dependent functionality gone | state-changing |
| `modprobe -c` | Generate current modprobe configuration view | aliases/options/path rules | read-only / output-generating |
| `kldload foo` | FreeBSD: load kernel module | module appears loaded | state-changing |
| `kldunload foo` | FreeBSD: unload kernel module | module removed safely | state-changing |
| `kldstat` | FreeBSD: list loaded modules | module inventory | read-only |
| `sudo sysctl kernel.softlockup_panic=1` | Linux: make soft lockup trigger panic behavior | runtime policy changed intentionally | state-changing |
| `sudo sysctl kernel.nmi_watchdog=1` | Linux: set NMI watchdog parameter shown with lockup handling | runtime value changed | state-changing |
| `kgdb` | FreeBSD: analyze crash dump / stack trace | useful backtrace from `/var/crash` | read-only / diagnostic |

## Не включено как canonical command

RAG содержит параметризованный пример `modprobe snd-usb-audio ...`, но имя одного параметра и его значение искажены OCR неоднозначно. Он не нормализован и помечен `[Needs confirmation]`.

## Configuration locations and structures

### Linux devices

- `/sys` — structured device/kernel view used by udev.
- `/etc/udev/udev.conf` — udev configuration.
- `/lib/udev/rules.d/` — distribution/default rules.
- `/etc/udev/rules.d/` — local rules.
- Rule structure: match conditions → assignments/actions.
- Chapter examples use keys such as `ACTION`, `ATTR/ATTRS`, `KERNEL`, `SUBSYSTEM`, `PROGRAM`, `RESULT`, `RUN`, `NAME`, `SYMLINK`.

### FreeBSD devices

- `/etc/devfs.conf` — static device aliases/owner/mode.
- `/etc/devfs.rules` — dynamic/removable device rules.
- `/etc/devd.conf` — higher-level device-event handling.
- `autofs` handles removable-media automount in the chapter model.

### Kernel tunables

Linux:
- transient path: `/proc/sys/...`;
- persistent file: `/etc/sysctl.conf`.

FreeBSD:
- runtime via `sysctl`;
- persistent values also described via `/etc/sysctl.conf`.

## Safety rules from the chapter

- Do not change kernel settings simply because a value exists; many defaults are workload/distribution specific.
- Direct writes to `/proc/sys` are runtime-only and vanish on reboot.
- If IPv4 and IPv6 both matter, do not tune one stack and forget the other.
- Prefer distribution-supported kernel build/update path when available.
- Avoid rebuilding/replacing a kernel without a concrete benefit.
- Keep a known-good fallback kernel/boot entry before testing a custom kernel.
- Loading/unloading modules can destabilize the kernel; do not use untested modules casually.
- Before removing a module, verify it is not in use.
- Udev rule typos may be silently ignored; syntax and resulting behavior must be verified.
- For panic/oops analysis, preserve full diagnostics, especially the beginning of the trace.
- FreeBSD crash dumps may require space comparable to physical RAM; capacity must be checked before relying on dumps.

## Rollback

- Runtime `sysctl` changes can be reverted only if the previous environment-specific value is known: `[Needs confirmation]`.
- Custom kernel rollback point is the known-good boot/fallback kernel.
- Module load rollback is unload only if the module is safe to remove and not referenced.
- Source patch rollback commands are not provided in the chapter: `[Needs confirmation]`.
- Udev/devfs rule rollback requires restoration of the prior local rule state plus reload/retest: exact prior state `[Needs confirmation]`.
