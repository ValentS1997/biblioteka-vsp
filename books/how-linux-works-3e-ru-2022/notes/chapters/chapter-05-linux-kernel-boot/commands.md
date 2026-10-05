# Команды и интерфейсы главы 5

Только элементы, явно подтверждённые RAG главы 5.

## v1.6 command contract normalization

Для всех строк с типом `state-changing` применяется следующий контракт:

- **Effect** — действие, явно указанное в колонке «Назначение» или в самой строке.
- **Risk** — только source-supported ограничение/риск из строки или safety notes; если отдельный риск не дан, `[Needs confirmation]`.
- **Verification** — только явно указанный source-supported check; если check не дан, `[Needs confirmation]`.
- **Rollback** — только явно указанный обратный путь; если источник его не даёт, `[Needs confirmation]`.

Этот блок является нормативной интерпретацией таблицы ниже для `BIBLIOTEKA-VSP-CHAPTER-ARTIFACT-COLLECTION v1.6`; недостающие поля не достраиваются из model knowledge.

| Команда / интерфейс | Назначение | Тип | Risk / verification |
|---|---|---|---|
| `journalctl -k` | Kernel messages текущей загрузки | read-only | Основной post-boot diagnostic source |
| parameter `-b` for journalctl | Просмотр других boot sessions | read-only | Источник указывает для previous boots |
| `dmesg` | Kernel ring buffer messages | read-only | Fallback без systemd |
| `/var/log/kern.log` | Kernel log file в некоторых non-systemd systems | read-only | Может отсутствовать |
| `cat /proc/cmdline` | Показать фактическую kernel command line | read-only | Проверить `root=`, `ro`, `quiet`, `splash` |
| `bootparam(7)` | Overview kernel boot parameters | read-only documentation | Источник рекомендует для reference |
| `efibootmgr` | Определить наличие EFI boot variables / UEFI | read-only в контексте проверки главы | Не использовать write operations без отдельной задачи |
| `/sys/firmware/efi` | Признак boot через UEFI | read-only interface | Наличие указывает на UEFI |
| GRUB `ls` | Список GRUB devices или filesystem contents в зависимости от argument | read-only | GRUB namespace, не Linux shell |
| GRUB `ls -l` | Device/partition/filesystem/UUID details | read-only | Помогает найти root by UUID |
| GRUB `echo $root` | Показать GRUB root | read-only | Не путать с Linux root filesystem |
| GRUB `set` | Показать GRUB variables | read-only | Важен `prefix` |
| GRUB `boot` | Запустить настроенную вручную boot configuration | state-changing | Выполнять только после полной конфигурации |
| `grub-mkconfig` | Сгенерировать GRUB config в stdout | read-only | Без `-o` не перезаписывает active config |
| `grub-mkconfig -o /boot/grub/grub.cfg` | Записать generated GRUB config | state-changing | Backup old config + correct target directory |
| `grub-install /dev/sda` | Установить GRUB для MBR-style target | state-changing | High risk: source warns boot sequence can break |
| `grub-install --boot-directory=/mnt/boot /dev/sdc` | Install GRUB to external/alternate target | state-changing | Подтвердить mount/layout |
| UEFI `grub-install` with `--efi-directory` and `--bootloader-id` | Install UEFI GRUB and register loader | state-changing | Подтвердить ESP + boot mode |
| GRUB `insmod` | Load GRUB module | state-changing in GRUB runtime | Это не Linux kernel `insmod` |
| GRUB `search` | Найти filesystem/partition, в том числе по UUID | read-only/discovery | Используется для установки GRUB root |
| GRUB `linux` directive | Указать kernel image и kernel parameters | state-changing in boot runtime | Определяет запускаемый kernel |
| GRUB `initrd` directive | Указать initial RAM filesystem image | state-changing in boot runtime | Связано с early boot |
| GRUB `chainloader` | Передать управление другому loader | state-changing in boot runtime | Используется для chainloading |

## Bootloader inventory из главы

- GRUB;
- LILO / ELILO;
- SYSLINUX;
- LOADLIN;
- systemd-boot;
- coreboot;
- Linux Kernel EFISTUB;
- efilinux.

Глава подробно работает с GRUB.

## GRUB navigation examples

```text
grub> ls
grub> ls -l
grub> echo $root
grub> ls (hd0,msdos1)/
grub> ls ($root)/
grub> ls ($root)/boot
grub> set
```

## GRUB configuration structure

Основные source-derived элементы:
- `menuentry`;
- `submenu`;
- `insmod`;
- `set root=...`;
- `search --fs-uuid --set=root ...`;
- `linux ... root=UUID=... ro ...`;
- `initrd ...`.

## Configuration paths

- обычно `/boot/grub` или `/boot/grub2`;
- generated file: `grub.cfg`;
- generation scripts: `/etc/grub.d`;
- custom configuration source упоминается как `custom.cfg`;
- UEFI ESP обычно смонтирован в `/boot/efi`;
- EFI loaders располагаются под `/boot/efi/EFI/.../*.efi`.

## Safety notes

1. GRUB root и Linux `root=` — разные сущности.
2. Не редактировать generated `grub.cfg` вручную.
3. Перед persistent config generation сохранить старую configuration.
4. Перед `grub-install` определить boot mode и target.
5. Неправильный `grub-install` может нарушить boot sequence.
6. До bootloader install source требует backup и emergency boot plan.
7. Secure Boot — security boundary, а не просто nuisance setting.
