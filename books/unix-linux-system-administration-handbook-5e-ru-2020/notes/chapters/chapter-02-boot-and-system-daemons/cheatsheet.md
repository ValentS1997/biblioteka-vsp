# Шпаргалка: загрузка и системные демоны

Цель: локализовать boot/service failure по этапу и менять только соответствующий слой.

## 0. Symptom / baseline

Зафиксировать:

- система вообще не доходит до bootloader?
- GRUB/loader виден, но kernel не стартует?
- kernel стартует, но PID 1 / target не достигается?
- система загружается, но отдельная service не работает?
- проблема появилась после kernel/GRUB/unit/config change?
- есть ли known-good kernel, snapshot или предыдущий boot journal?

Ключевая цепочка главы:

```text
firmware → bootloader → kernel → PID 1 → target/services
```

## 1. Firmware / UEFI

Read-only:

```bash
efibootmgr -v
```

Проверить `BootCurrent`, `BootOrder` и существование нужной boot entry.

Если подтверждён неправильный порядок:

```bash
sudo efibootmgr -o <known-order>
```

Verification: повторно `efibootmgr -v`.

Rollback: восстановить ранее зафиксированный BootOrder. Если старый порядок не записан — `[Needs confirmation]`.

## 2. GRUB / kernel selection

После изменения `/etc/default/grub` или `/etc/grub.d/40_custom` глава требует регенерации конфигурации:

```bash
update-grub
# или
grub2-mkconfig
```

При boot failure после kernel update попробовать предыдущий kernel из boot menu.

Во временном recovery boot можно передать параметры:

```text
single
systemd.unit=rescue.target
systemd.unit=emergency.target
```

Изменения boot parameters, внесённые только через bootloader во время старта, непостоянны.

## 3. systemd: сначала наблюдение

```bash
systemctl list-units --type=service
systemctl list-unit-files --type=service
systemctl status -l <unit>
systemctl get-default
systemctl list-units --type=target
journalctl -b -1
journalctl -u <unit>
```

Interpretation:

- `disabled` не означает, что unit нельзя запустить вручную;
- `static` обычно активируется вручную или как dependency;
- dependency и ordering — разные понятия;
- `Wants/Requires` определяют зависимость, а `Before/After` — порядок.

## 4. systemd: controlled change

Для service:

```bash
sudo systemctl start <unit>
sudo systemctl stop <unit>
sudo systemctl restart <unit>
sudo systemctl enable <unit>
sudo systemctl disable <unit>
```

Verification:

```bash
systemctl status -l <unit>
journalctl -u <unit>
```

Rollback для start/stop и enable/disable — обратная операция.

### Локальный override

Не редактировать package unit в `/usr/lib/systemd/system`.

Использовать local override:

```bash
sudo systemctl edit <unit>
sudo systemctl daemon-reload
sudo systemctl restart <unit>
```

Verification: `systemctl status -l <unit>` и journal.

Rollback конкретного override-файла в главе не описан: `[Needs confirmation]`.

## 5. Targets / operating mode

Read-only:

```bash
systemctl get-default
```

Переход к target:

```bash
sudo systemctl isolate multi-user.target
```

Изменение default boot target:

```bash
sudo systemctl set-default multi-user.target
```

Risk: `isolate` деактивирует units, не входящие в выбранный target.

Verification: повторно проверить target и необходимые services.

Rollback: вернуть ранее записанный default target; exact previous value: `[Needs confirmation]`.

## 6. FreeBSD rc

Конфигурацию задавать в:

- `/etc/rc.conf`
- `/etc/rc.conf.local`

Не редактировать `/etc/defaults/rc.conf`.

Пример управления service:

```bash
sudo service sshd stop
```

Если service не включена через rc.conf, глава указывает на подкоманды `onestop`, `onestart`, `onerestart`.

## 7. Filesystem / single-user recovery

Read-only discovery:

```bash
fdisk -l
camcontrol devlist
fdisk -s <device>
```

Если root смонтирован read-only:

Linux:

```bash
mount -o rw,remount /
```

FreeBSD:

```bash
mount -o rw <device> /
```

Filesystem check:

```bash
fsck
```

Risk: mount в RW и особенно `fsck` изменяют state. Rollback для repair в RAG не задан.

После завершения single-user работы:

```bash
exit
```

для продолжения обычной загрузки.

## 8. Shutdown / reboot

Глава не рекомендует reboot как первый troubleshooting step. Сначала искать root cause.

Корректное выключение:

```bash
halt -p
```

Перезагрузка:

```bash
reboot
```

После значительных изменений startup configuration глава рекомендует выполнить реальный reboot как acceptance check: система должна снова загрузиться успешно.

## 9. Cloud recovery

Предпочтительный путь главы:

1. Вернуть known-good image/snapshot, если это разумно.
2. Либо загрузить recovery instance.
3. Остановить неисправный instance.
4. Подключить его volume к recovery instance.
5. Смонтировать и исправить filesystem/config.
6. Отсоединить volume и вернуть его исходному instance.
7. Запустить систему и проверить boot.

Для Google Compute Engine read-only boot evidence:

```bash
gcloud compute instances get-serial-port-output <instance>
```

Critical risk: не путать stop/reboot с destructive terminate. Глава отдельно предупреждает, что terminate может удалить root storage.

## Acceptance criteria

- boot stage локализован до изменения;
- изменение сделано только в соответствующем слое;
- для systemd проверены `status` и journal;
- после startup/kernel/GRUB change система проходит реальный reboot;
- для cloud recovery есть known-good snapshot/image или recovery path;
- неизвестный rollback помечен `[Needs confirmation]`.
