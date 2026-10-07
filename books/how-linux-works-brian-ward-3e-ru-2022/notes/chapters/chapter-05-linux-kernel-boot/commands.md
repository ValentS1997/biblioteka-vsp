# Команды и интерфейсы — глава 5 «Загрузка ядра Linux»

**Provenance:** `p0156:c01`–`p0175:c01`, PDF/печатные страницы 156–175. Только явно поддержанные chapter RAG команды/интерфейсы. Примерные UUID, `/dev/sda`, `/dev/sdc`, `hd0` и пути не считаются значениями реального хоста.

Классы: **RO** — read-only observation; **WG** — workload-generating / interactive execution; **SC** — state-changing.

## 1. Linux user space: наблюдение

| Команда / путь | Класс | Назначение по главе | PDF |
|---|---|---|---:|
| `journalctl -k` | RO | Kernel log текущей загрузки | 157 |
| `journalctl` с `-b` | RO | Просмотр другой/предыдущей загрузки; точная комбинация флагов в RAG не дана | 157 |
| `dmesg` | RO | Kernel ring buffer для систем без systemd / альтернативный просмотр | 157 |
| `/var/log/kern.log` | RO path | Возможный kernel log file в системах без systemd | 157 |
| `cat /proc/cmdline` | RO | Параметры, переданные active kernel | 159 |
| `efibootmgr` | RO | В модели главы: boot targets → UEFI; unsupported EFI variables → BIOS | 161 |
| `/sys/firmware/efi` | RO path | Наличие названо ещё одним признаком UEFI; shell-команда не задана | 161 |
| `bootparam(7)` | Documentation | Overview kernel boot parameters | 160 |
| `kernel-params.txt` | Documentation | Более детальные kernel parameter descriptions | 160 |

Примеры `root=/dev/sda1`, `root=/dev/mapper/my-system-root`, `root=UUID=...`, `ro`, `quiet`, `splash`, `vt.handoff=1`, `-s` — **значения kernel command line**, не отдельные shell commands.

## 2. GRUB interactive environment — не Linux shell

| GRUB input | Класс | Результат | PDF |
|---|---|---|---:|
| `ls` | RO in GRUB | GRUB-visible disks/partitions | 165–166 |
| `ls -l` | RO in GRUB | Filesystem type, UUID, sector/start/size metadata | 166 |
| `echo $root` | RO in GRUB | Current GRUB root | 166 |
| `ls (hd0,msdos1)/` | RO in GRUB | Files at selected partition root | 166 |
| `ls ($root)/` | RO in GRUB | Files at current GRUB root | 166 |
| `ls ($root)/boot` | RO in GRUB | Contents of `/boot` in current GRUB root | 167 |
| `set` | RO in GRUB | Current GRUB variables incl. `prefix`, `root` | 167 |
| `boot` | WG/SC boot action | Executes prepared configuration / transfers control to kernel | 167,175 |

Keyboard controls explicitly described: Shift (BIOS menu), Esc (UEFI menu / return), `e` (edit selected entry), `c` (GRUB command line), arrow keys/history/editing. These are **interactive controls**, not persistent configuration commands.

## 3. GRUB configuration — generation vs persistence

| Element | Класс | Meaning / effect | PDF |
|---|---|---|---:|
| `/boot/grub/grub.cfg`, `/boot/grub2/grub.cfg` | generated config | Main configuration; chapter says not to edit directly | 167–168 |
| `/etc/grub.d/*` | config generators | Shell scripts used by `grub-mkconfig` | 168–169 |
| `40_custom`, `41_custom`, `custom.cfg` | config inputs | Custom entries/methods discussed by chapter | 169 |
| `grub-mkconfig` | RO in described use | Writes generated config to stdout when no `-o` | 169 |
| `grub-mkconfig -o /boot/grub/grub.cfg` | SC | Writes generated configuration to target file | 169 |

Before writing the generated config, the chapter says to **back up the old configuration and verify the target directory**. Exact backup command is not provided: **[Needs confirmation]**.

### GRUB configuration statements in source

These are GRUB language, not shell:

- `menuentry`, `submenu`
- `insmod gzio`, `insmod part_msdos`, `insmod ext2`
- `set root='hd0,msdos1'`
- `search --no-floppy --fs-uuid --set=root ...`
- `linux /boot/vmlinuz-... root=UUID=... ro quiet splash ...`
- `initrd /boot/initrd.img-...`
- chainloading: `insmod chain`, `insmod ntfs` or `fat`, `chainloader +1` / `chainloader /io.sys`

These statements become state-affecting only when used to boot or persisted into future configuration. Sample OS names, UUIDs and partition indices are not portable.

## 4. Bootloader installation — high-risk SC

| Example from source | Effect | Risk / prerequisite | Verification / rollback |
|---|---|---|---|
| `grub-install /dev/sda` | Install GRUB to example MBR target | Wrong target or boot mode can make system unbootable | Boot to GRUB/kernel; backup + emergency boot plan required; exact rollback [Needs confirmation] |
| `grub-install --boot-directory=/mnt/boot /dev/sdc` | Install files/boot code for external target example | Must know target disk and where its `/boot` is mounted | Reboot target / inspect expected GRUB path; rollback [Needs confirmation] |
| UEFI `grub-install --efi-directory=efi_dir …bootloader-id=name` | Install UEFI GRUB and potentially register firmware entry | Source token before `bootloader-id` is malformed-looking; exact command **[Needs confirmation]** | `efibootmgr` evidence + successful boot; recovery plan mandatory |

The chapter states that `grub-install` can invoke `efibootmgr` during UEFI installation when available (PDF 171).

## 5. Secure Boot / firmware operations

Disabling Secure Boot is discussed as a possible firmware setting change, not as a Linux command. It changes platform security behavior and may interact with dual-boot requirements. Exact firmware UI, key enrollment, signature chain and rollback are **[Needs confirmation]**.

## 6. Command discipline

- Do not confuse GRUB's `root`, `insmod`, `ls` with Linux kernel/shell semantics.
- Do not copy sample `(hd0,msdos1)`, UUID or `/dev/sda` to a host without identification.
- Do not normalize the malformed UEFI install option from PDF 171 silently; see `source-findings.md`.
- Persistent bootloader changes require a verified rescue path before execution.
