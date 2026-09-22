# Шпаргалка: драйверы и ядро

Цель: работать с kernel/device layer через наблюдение, минимальные изменения и обязательный fallback.

## 1. Что делает ядро

Глава выделяет пять крупных функций:

- hardware abstraction/management;
- processes and threads;
- memory management/protection;
- I/O services: filesystems, network, serial and other interfaces;
- system organization: boot/shutdown, timers, multitasking.

Для администратора kernel work обычно означает:

~~~text
inspect
→ tune runtime parameter
→ manage driver/module
→ rebuild only if necessary
→ verify boot/runtime
~~~

## 2. Kernel change policy

Глава рекомендует консервативный подход:

~~~text
конкретная проблема / выгода
        ↓
минимальное изменение
        ↓
known-good fallback
        ↓
verification
~~~

Не обновлять или пересобирать kernel только ради новизны.

Distribution kernel может быть старее upstream намеренно из-за stability/compatibility goals.

## 3. Версия ядра

~~~bash
uname -r
~~~

Running version используется для выбора matching module tree и проверки реально загруженного kernel.

## 4. Device driver model

~~~text
hardware-specific protocol
        ↓
device driver
        ↓
kernel-standard interface
        ↓
user-space abstraction
~~~

Driver скрывает hardware details от остального kernel/user space.

## 5. Device files

Device file связывает user-space path с driver через type + major + minor.

Типы:

- block;
- character.

Manual creation:

~~~bash
mknod <file> <type> <major> <minor>
~~~

Современные systems обычно автоматизируют это; manual mknod — exception path.

## 6. Linux device stack

~~~text
kernel device events
      ↓
sysfs (/sys)
      ↓
udevd
      ↓
rules
      ↓
/dev names / symlinks / actions
~~~

Ключевые paths:

~~~text
/sys
/etc/udev/udev.conf
/lib/udev/rules.d/
/etc/udev/rules.d/
~~~

Local policy should live under /etc/udev/rules.d/, not by editing distribution rules.

## 7. sysfs

/sys exposes structured device/kernel state.

Important subtrees from chapter include block, bus, class, dev, devices, firmware, fs, kernel, module and power.

Use it as observation source before writing a udev rule.

## 8. udevadm workflow

Inspect enumeration and kernel messages:

~~~bash
lsusb
dmesg
~~~

Inspect attributes:

~~~bash
udevadm info -a -n sdb
udevadm info -a -p /block/sdb/sdb1
~~~

Then choose stable identifiers. Avoid attributes that change during ordinary device use if a better identifier exists.

## 9. Udev rule logic

Conceptually:

~~~text
MATCH CONDITIONS
    ↓
ASSIGNMENT / ACTION
~~~

Chapter keys include ACTION, ATTR/ATTRS, DEVPATH, DRIVER, ENV, KERNEL, PROGRAM, RESULT, SUBSYSTEM, TEST, NAME, SYMLINK and RUN.

After editing:

~~~bash
sudo udevadm control --reload-rules
~~~

Then trigger a real attach/detach and verify behavior.

## 10. Rule verification

Chapter USB example verifies:

~~~bash
ls -l /dev/ate*
mount | grep ate
~~~

Acceptance check:

- stable name/symlink exists;
- correct device matched;
- action happened at intended event;
- mount/unmount path is correct;
- no unrelated device matched.

Udev syntax errors may be silently ignored, so actual event testing matters.

## 11. FreeBSD device stack

~~~text
kernel events
  ↓
devfs + devd
  ↓
/dev + higher-level actions
~~~

Configuration:

~~~text
/etc/devfs.conf
/etc/devfs.rules
/etc/devd.conf
~~~

Roles:

- devfs.conf — static links/owner/permissions;
- devfs.rules — dynamic/removable-device rules;
- devd.conf — event reactions;
- autofs — removable-media automount in chapter model.

## 12. Linux kernel tuning

Runtime interface:

~~~text
/proc/sys/...
~~~

Example read:

~~~bash
cat /proc/sys/fs/file-max
~~~

Example runtime write:

~~~bash
echo 32768 > /proc/sys/fs/file-max
~~~

Direct change is not persistent across reboot.

## 13. sysctl

Runtime example:

~~~bash
sysctl net.ipv4.ip_forward=0
~~~

Persistent configuration:

~~~text
/etc/sysctl.conf
~~~

FreeBSD inventory:

~~~bash
sysctl -a
~~~

Not every displayed FreeBSD parameter is writable.

## 14. Tuning discipline

Chapter examples include parameters related to file limits, panic/oops behavior, printk rate, shared memory, source validation, ICMP behavior, IP forwarding, local port range, SYN cookies, TCP timeout and virtual-memory overcommit.

Do not treat example values as universal tuning recommendations.

## 15. IPv4 / IPv6 consistency

If both stacks are supported:

~~~text
change IPv4 behavior
      ↓
check equivalent IPv6 behavior
~~~

Chapter explicitly warns against tuning only one protocol family.

## 16. Linux kernel build

Preferred configuration interfaces:

~~~bash
make xconfig
make gconfig
make menuconfig
~~~

Migration:

~~~bash
make oldconfig
~~~

Less preferred:

~~~bash
make config
~~~

Generated configuration source of truth is .config.

## 17. Linux build pipeline

~~~bash
make clean
make
make modules_install
make install
~~~

Conceptual flow:

~~~text
source tree
  ↓
.config
  ↓
clean
  ↓
compile
  ↓
install modules
  ↓
install kernel
  ↓
boot with fallback available
~~~

Compilation is workload-generating; install steps change boot/kernel state.

## 18. Kernel source patch

Chapter example:

~~~bash
cd <kernel-source>; patch -p1 < <patch-file>
~~~

Before applying, source tree/version must match and the patch must apply cleanly. Rollback command is [Needs confirmation].

## 19. FreeBSD kernel build

Start from GENERIC:

~~~text
GENERIC → MYCUSTOM
~~~

Chapter workflow:

~~~text
cd /usr/src/sys/<arch>/conf
copy GENERIC → MYCUSTOM
edit MYCUSTOM
cd /usr/src
make buildkernel KERNCONF=MYCUSTOM
make installkernel KERNCONF=MYCUSTOM
~~~

Rule from chapter: if you are not sure an option is unnecessary, leave it enabled.

## 20. Linux loadable modules

Inventory:

~~~bash
lsmod
~~~

Load:

~~~bash
sudo modprobe snd-usb-audio
~~~

Unload:

~~~bash
modprobe -r snd-usb-audio
~~~

Configuration view:

~~~bash
modprobe -c
~~~

modprobe resolves dependencies and chooses a module matching the running kernel.

## 21. Module risk

Load/unload happens inside the live kernel.

Therefore:

- use tested modules;
- check references before unload;
- have console/recovery path;
- verify device/service behavior immediately after change.

## 22. FreeBSD modules

~~~bash
kldload foo
kldunload foo
kldstat
~~~

Persistent boot loading is configured through /boot/loader.conf.

Chapter example form:

~~~text
zfs_load="YES"
~~~

## 23. Boot messages as diagnostics

Kernel boot log is an ordered initialization trace.

Look for:

- kernel version/build;
- kernel command line;
- CPU/memory discovery;
- hypervisor detection;
- PCI/USB/SCSI initialization;
- driver registration;
- network interface discovery;
- storage devices;
- root filesystem mount.

Do not discard boot messages as noise.

## 24. Alternate kernels / cloud

Chapter discusses custom kernel boot in cloud environments.

Operational requirement:

~~~text
custom kernel
+
known-good fallback kernel
~~~

Fallback is the key rollback point if custom kernel cannot boot or is unstable.

## 25. Kernel failures

Linux categories in chapter:

- soft lockup;
- hard lockup;
- panic;
- oops.

Oops may or may not escalate to panic.

Diagnostic source:

~~~bash
dmesg
~~~

Preserve full trace; the beginning is often most valuable.

## 26. Panic-oriented sysctl examples

Chapter shows:

~~~bash
sudo sysctl kernel.softlockup_panic=1
sudo sysctl kernel.nmi_watchdog=1
~~~

These are policy changes, not generic recommendations.

## 27. FreeBSD panic analysis

Chapter workflow:

~~~text
build debug-capable kernel
→ reproduce panic
→ crash dump in /var/crash
→ analyze with kgdb
~~~

Crash dump capacity can approach physical RAM size.

Before relying on dump capture:

- verify /var/crash capacity;
- confirm dump configuration;
- preserve the dump before cleanup.

## 28. Minimal troubleshooting workflow

~~~text
Device/kernel problem
   ↓
uname -r
   ↓
dmesg / journal / sysfs
   ↓
identify device + driver/module
   ↓
read-only inspect with udevadm / lsmod / sysctl
   ↓
choose smallest change
   ↓
preserve fallback
   ↓
apply one change
   ↓
retest device/boot
   ↓
rollback or keep
~~~

## Acceptance criteria

- running kernel version is known;
- device identity/driver path is observed before changing rules;
- local udev/devfs changes are separated from vendor defaults;
- runtime vs persistent kernel tuning is explicit;
- IPv4/IPv6 symmetry is checked where relevant;
- kernel rebuild has an explicit reason;
- known-good fallback kernel exists before boot-level changes;
- module load/unload is verified immediately;
- panic/oops diagnostics can be captured;
- crash-dump storage is sufficient where used;
- unknown rollback remains [Needs confirmation].
