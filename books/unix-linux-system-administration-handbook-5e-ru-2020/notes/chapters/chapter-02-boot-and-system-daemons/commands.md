# Команды главы 2

Таблица включает только команды и интерактивные команды, подтверждённые RAG главы 2.

| Команда | Назначение | Что проверить | Тип |
|---|---|---|---|
| `efibootmgr -v` | Показать UEFI boot configuration | `BootCurrent`, `BootOrder`, записи загрузки | read-only |
| `sudo efibootmgr -o 0004,0002` | Изменить UEFI BootOrder | новый порядок загрузки | state-changing |
| `update-grub` | Перегенерировать GRUB config в Debian/Ubuntu | успешное создание `grub.cfg` | state-changing |
| `grub2-mkconfig` | Перегенерировать GRUB config в Red Hat/CentOS | успешное создание `grub.cfg` | state-changing |
| `gpart show` | Просмотреть разметку диска FreeBSD | EFI/UFS/swap partitions | read-only |
| `mount` | Просмотреть текущие mounts | состояние boot/root filesystem | read-only |
| GRUB `help` | Помощь по команде GRUB | доступный синтаксис | read-only |
| GRUB `search` | Искать устройство по файлу/label/UUID | найденное boot device | read-only |
| GRUB `linux` | Задать Linux kernel для загрузки | выбранный kernel и параметры | state-changing |
| GRUB `boot` | Продолжить загрузку выбранного образа | переход к kernel boot | state-changing |
| GRUB `reboot` | Перезагрузить систему из GRUB | reboot | state-changing |
| GRUB `usb` | Проверить поддержку USB | доступность USB в GRUB | read-only |
| loader `ls` | Просмотреть filesystem из FreeBSD loader | доступные файлы/каталоги | read-only |
| loader `unload` | Выгрузить текущий kernel/module selection | очищенное состояние loader | state-changing |
| loader `load /boot/kernel/kernel.old` | Загрузить старое ядро FreeBSD | выбран старый kernel | state-changing |
| loader `boot` | Продолжить boot FreeBSD | запуск выбранного ядра | state-changing |
| `man loader` | Документация FreeBSD loader | доступные команды | read-only |
| `mount -t msdos ...` | Смонтировать ESP FreeBSD для просмотра | содержимое EFI filesystem | state-changing |
| `sudo dd if=/boot/boot1.efifat of=/dev/ada0p1` | Восстановить ESP из образа FreeBSD | запись EFI filesystem image | state-changing |
| `systemctl list-units --type=service` | Список загруженных/активных services | active service units | read-only |
| `systemctl list-unit-files --type=service` | Список installed unit files | enabled/disabled/static/masked state | read-only |
| `systemctl status -l <unit>` | Статус unit и последние journal entries | Loaded/Active/PID/logs | read-only |
| `systemctl get-default` | Показать default target | текущий boot target | read-only |
| `systemctl list-units --type=target` | Показать targets | доступные/активные targets | read-only |
| `sudo systemctl enable <unit>` | Включить unit для нормальной активации при boot | enabled state/symlinks | state-changing |
| `sudo systemctl disable <unit>` | Отключить normal activation path | disabled state | state-changing |
| `sudo systemctl start <unit>` | Немедленно активировать unit | active/running | state-changing |
| `sudo systemctl stop <unit>` | Немедленно деактивировать unit | inactive/stopped | state-changing |
| `sudo systemctl restart <unit>` | Перезапустить unit | успешный restart | state-changing |
| `sudo systemctl isolate <target>` | Перевести систему к target и деактивировать остальные units | новый operating mode | state-changing |
| `sudo systemctl set-default multi-user.target` | Изменить default boot target | `get-default` после изменения | state-changing |
| `sudo systemctl daemon-reload` | Перечитать unit files/config | systemd принял новую конфигурацию | state-changing |
| `sudo systemctl add-wants <target> <unit>` | Добавить Wants dependency | dependency target → unit | state-changing |
| `sudo systemctl edit <unit>` | Создать/edit local override | override config в `/etc/systemd/system` | state-changing |
| `journalctl` | Показать journal | boot/kernel/service events | read-only |
| `journalctl --list-boots` | Показать известные boots | boot indexes/IDs | read-only |
| `journalctl -b -1` | Journal предыдущей загрузки | события перед последним reboot | read-only |
| `journalctl -b <boot-id>` | Journal конкретной загрузки | события выбранного boot | read-only |
| `journalctl -u <unit>` | Journal конкретного unit | ошибки/старты/остановки службы | read-only |
| `sudo service sshd stop` | Остановить FreeBSD rc service | остановка sshd | state-changing |
| `fdisk -l` | Показать partitions Linux в recovery/single-user | local disk partitions | read-only |
| `camcontrol devlist` | Идентифицировать FreeBSD disk devices | список устройств | read-only |
| `fdisk -s <device>` | Показать partition info FreeBSD | layout выбранного диска | read-only |
| `mount -o rw,remount /` | Перемонтировать Linux root read-write | root доступен для записи | state-changing |
| `mount -o rw <device> /` | Перемонтировать FreeBSD root read-write | root доступен для записи | state-changing |
| `fsck` | Проверить/восстановить filesystem | filesystem errors | state-changing |
| `exit` | Выйти из single-user shell и продолжить boot | продолжение normal boot | state-changing |
| `halt -p` | Корректно остановить и выключить систему | clean shutdown | state-changing |
| `reboot` | Корректно перезагрузить систему | reboot | state-changing |
| `shutdown` | Scheduled shutdown / warnings; также участвует в переходах режима | запрошенное состояние системы | state-changing |
| `gcloud compute instances get-serial-port-output <instance>` | Получить serial boot output GCE | сообщения загрузки cloud instance | read-only |

## Boot parameters, подтверждённые главой

Это не shell-команды, а параметры, передаваемые ядру через bootloader:

| Параметр | Назначение |
|---|---|
| `debug` | Включить kernel debugging |
| `init=/bin/bash` | Запустить bash как init для recovery |
| `root=/dev/foo` | Указать root device |
| `single` | Single-user mode |
| `systemd.unit=rescue.target` | Boot в rescue target |
| `systemd.unit=emergency.target` | Boot в emergency target |

## Safety / rollback

- Перед изменением UEFI BootOrder сначала сохранить вывод `efibootmgr -v`. Для rollback потребуется прежний порядок; конкретные значения зависят от системы.
- После изменения GRUB глава указывает на возможность выбрать предыдущее ядро, если новое перестало загружаться.
- `systemctl start/stop` и `enable/disable` имеют обратные операции, явно перечисленные в главе.
- Перед `systemctl set-default` полезно зафиксировать `systemctl get-default`; rollback — вернуть прежний target.
- `dd` в ESP — высокорисковая запись на block device. Rollback после неверного `dd` в главе не приведён: `[Needs confirmation]`.
- `fsck` способен изменять filesystem при восстановлении. Rollback в главе не задан: `[Needs confirmation]`.
- Не выполнять destructive команды вроде `rm -rf /`; глава приводит это только как предупреждение о возможности повредить UEFI state.
