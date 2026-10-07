# Cheatsheet — глава 5 «Загрузка ядра Linux»

**Source:** `how-linux-works-brian-ward-3e-ru-2022:p0156:c01`–`p0175:c01`; PDF/печатные страницы 156–175. Только `rag_only`.

## Symptom / problem framing

Глава поддерживает разбор ситуаций, когда нужно понять **на каком этапе загрузки находится система, какие параметры получил kernel, какой boot mode используется, что GRUB считает своим root, какой kernel/initrd выбран и как persistent GRUB configuration формируется из user-space файлов**. Она не даёт универсального recovery procedure для конкретного сервера.

## Baseline / context

| Объект | Смысл | PDF |
|---|---|---:|
| Firmware | BIOS/UEFI запускает bootloader code | 156,160–161,173–175 |
| Bootloader | Находит kernel image, загружает его и передаёт parameters | 160–162 |
| Kernel cmdline | Активные параметры видны в `/proc/cmdline` | 159–160 |
| `root=` | Указывает root filesystem source для kernel | 159 |
| `ro` | Начальная root FS read-only до дальнейшей проверки/remount | 160 |
| GRUB root | Файловая система, в которой сам GRUB ищет kernel/initrd/config | 164–167 |
| `$prefix` | GRUB filesystem/path с configuration and support files | 167 |
| `grub.cfg` | Generated configuration executed by GRUB | 167–169 |
| ESP | UEFI filesystem containing `.efi` bootloaders | 171,174 |
| Secure Boot | UEFI boot chain requires acceptable signatures according to platform policy | 171–172 |

## Read-only checks

Ниже только операции наблюдения, прямо поддержанные главой. Реальные пути/режимы не предполагать.

```sh
journalctl -k
dmesg
cat /proc/cmdline
efibootmgr
grub-mkconfig
```

- `journalctl -k` — kernel messages текущей загрузки; параметр `-b` описан для просмотра других boots (§5.1).
- `dmesg` — kernel ring buffer в системах/сценариях без systemd (§5.1).
- `cat /proc/cmdline` — фактически применённая kernel command line (§5.3).
- `efibootmgr` — если возвращает boot targets, книга использует это как признак UEFI; сообщение об отсутствии EFI variables интерпретируется как BIOS (§5.4).
- Проверка наличия `/sys/firmware/efi` также названа как признак UEFI, но конкретная shell-команда для проверки в тексте не дана.
- `grub-mkconfig` **без `-o`** выводит generated configuration в stdout и в контексте §5.5.2 не перезаписывает active file.

### В GRUB command line — отдельная среда

```text
grub> ls
grub> ls -l
grub> echo $root
grub> ls ($root)/
grub> ls ($root)/boot
grub> set
```

Эти команды относятся к **GRUB**, а не к Linux shell. Они наблюдают GRUB-visible devices, filesystems, root/prefix and variables (§5.5.1).

## Interpretation

| Наблюдение | Интерпретация по главе | Неизвестное |
|---|---|---|
| `journalctl -k` показывает kernel command line и disk discovery | Kernel прошёл ранние стадии и генерировал diagnostics | Причина failed boot, если система не дошла до journal access: [Needs confirmation] |
| `/proc/cmdline` содержит `root=UUID=...` | Kernel получил UUID-based root selector | Валидность конкретного UUID для будущего boot: проверить фактически |
| `ro` в cmdline | Начальный mount root read-only | Кто/когда remounts rw в конкретной системе: [Needs confirmation] |
| `efibootmgr` показывает targets | В модели главы система использует UEFI variables | Secure Boot enabled/disabled этим alone не доказывается |
| GRUB `ls` → `(hd0,msdos1)` | GRUB видит MBR partition; `gpt` prefix для GPT | Correspondence to Linux `/dev/sdX`: [Needs confirmation] |
| GRUB `echo $root` | Где GRUB ищет filesystem content | Это **не** kernel `root=` |
| GRUB `set` показывает `prefix` | Directory/filesystem for GRUB modules/config | Реальное persistent config origin требует проверки `/etc/grub.d` |
| `grub-mkconfig` stdout looks correct | Generator sees fragments and builds config text | Active `grub.cfg` не изменён без `-o` |

## Next action

1. Зафиксировать текущую загрузку: `journalctl -k`, `cat /proc/cmdline`.
2. Определить BIOS/UEFI evidence: `efibootmgr` и наличие `/sys/firmware/efi`.
3. Если проблема в выборе kernel/parameters — различить **temporary edit in GRUB menu** и persistent generator inputs.
4. Для persistent GRUB change сначала выяснить actual config directory, generator inputs and backup location.
5. Перед `grub-install`: подтвердить boot mode, target disk, GRUB directory, ESP mountpoint if UEFI, backup и emergency boot path.
6. Если target/boot mode/recovery path не подтверждены — **[Needs confirmation], STOP**.

## Modifying action

| Действие из главы | Эффект | Риск |
|---|---|---|
| Нажать `e` в GRUB menu и отредактировать entry | Temporary boot configuration for current attempt | Ошибочные kernel/root parameters могут сделать boot неуспешным; persistent config не меняется (§5.5). |
| GRUB `boot` | Выполняет подготовленную GRUB configuration | Запускает выбранный kernel/config; rollback — reboot и другая entry при доступности |
| Редактирование custom config / `40_custom` / `custom.cfg` | Меняет будущую generated/runtime GRUB config | Package/generated-file interactions; точный workflow зависит от system layout |
| `grub-mkconfig -o /boot/grub/grub.cfg` | Перезаписывает generated GRUB configuration file | Неверный target/config может нарушить future boot; книга требует backup |
| `grub-install /dev/sda` | Устанавливает GRUB в MBR target example | **High risk:** wrong disk/boot mode may break boot |
| `grub-install --boot-directory=/mnt/boot /dev/sdc` | Installs bootloader/files for external MBR-target example | Must know mounted target root/boot exactly |
| UEFI `grub-install --efi-directory=... --bootloader-id=...` | Installs UEFI loader and may register firmware boot entry | Source command has extraction anomaly; exact syntax [Needs confirmation] |
| Secure Boot disable in UEFI setup | Changes platform boot security policy | Security impact; no rollback procedure beyond firmware setting context |

`grub-install` examples are **not** approved production commands. The chapter explicitly warns to back up MBR/current GRUB directory and have an emergency boot plan before installation (§5.5.3).

## Verification / acceptance checks

| Change | Source-grounded check | Acceptance |
|---|---|---|
| Temporary GRUB entry edit | Successful boot, then `/proc/cmdline` | Running kernel received intended parameters |
| Generated config | Run `grub-mkconfig` without `-o` first and inspect output | Expected menu/kernel/root/initrd lines appear |
| Persistent config generation | Re-open/read target `grub.cfg` / boot via GRUB menu | Exact file-read command not prescribed: [Needs confirmation] |
| GRUB installation | Boot reaches GRUB then selected kernel | Requires recovery media/backup because failed verification may mean no normal boot |
| UEFI registration | `efibootmgr` shows boot target | Secure Boot signature acceptance still separate |
| Boot diagnostics | `journalctl -k`, `/proc/cmdline` | Correct kernel/root parameters and hardware initialization evidence |

## Rollback

- Temporary GRUB menu edits are not persistent; rebooting and selecting a known-good entry is the natural recovery path **if such an entry remains available**.
- Before overwriting `grub.cfg`, source recommends a backup; exact restore command: **[Needs confirmation]**.
- Before `grub-install`, source requires MBR/current GRUB backup and an emergency boot plan. Exact backup/restore commands are **not provided in this chapter**: **[Needs confirmation]**.
- Secure Boot policy changes are firmware-level; exact rollback UI/procedure depends on platform and is **[Needs confirmation]**.
- If no known-good boot path exists, do not apply persistent bootloader changes.

## Source limitations

- GRUB and Linux use overlapping words (`root`, `insmod`, `ls`) with different semantics; artifacts explicitly keep the namespaces separate.
- PDF 171 has a malformed-looking dash before `bootloader-id`; not silently corrected.
- Figures 5.1–5.2 are unavailable as multimodal RAG objects. Menu/editor appearance is not reconstructed.
