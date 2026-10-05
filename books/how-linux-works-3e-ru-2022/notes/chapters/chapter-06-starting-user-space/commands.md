# Команды и интерфейсы главы 6

Только элементы, явно подтверждённые RAG главы 6.

| Команда / интерфейс | Назначение | Тип | Effect | Risk | Verification | Rollback |
|---|---|---|---|---|---|---|
| `systemd-analyze dot` | Dependency graph systemd | read-only/workload-generating | Генерирует graph output | Полный graph может быть очень большим | Проверить ожидаемые связи | N/A |
| `systemctl -p UnitPath show` | Unit search path и priority | read-only | Не меняет state | Нет state change | Сопоставить Loaded path | N/A |
| `pkg-config systemd --variable=systemdsystemunitdir` | Vendor unit dir | read-only | Не меняет state | Нет state change | Сверить path | N/A |
| `pkg-config systemd --variable=systemdsystemconfdir` | Local config dir | read-only | Не меняет state | Нет state change | Сверить path | N/A |
| `systemctl list-units` | Active units | read-only | Не меняет state | Нет state change | `--full`/`--all` при необходимости | N/A |
| `systemctl status sshd.service` | Unit/process/cgroup/log status | read-only | Не меняет state | Нет state change | Проверить Loaded/Active/PID/CGroup | N/A |
| `systemd-cgls` | Cgroup hierarchy | read-only | Не меняет state | Нет state change | Сопоставить process tree | N/A |
| `journalctl --unit=unit_name` | Journal unit | read-only | Не меняет state | Может требовать elevated access | Проверить сообщения unit | N/A |
| `systemctl list-jobs` | Pending/running jobs | read-only | Не меняет state | Нет state change | Проверить waiting/running jobs | N/A |
| `systemctl show -p type unit` | Dependency property, где type = Wants/Requires и т. п. | read-only | Не меняет state | Нет state change | Сверить dependency value | N/A |
| `systemctl status test1.target test2.target` | Проверка example targets | read-only | Не меняет state | Нет state change | Оба target имеют ожидаемый state | N/A |
| `who -r` | System V runlevel | read-only | Не меняет state | Нет state change | Сверить текущий runlevel | N/A |
| `unmkinitramfs` | Inspect/extract initramfs | read-only/extraction | Распаковывает archive в user space | Exact invocation в главе не задан | Проверить извлечённое содержимое | Удалить extracted copy при необходимости |
| `systemctl start unit` | Активировать unit | state-changing | Меняет runtime unit state | Service side effects / dependencies | `systemctl status unit` + journal | `systemctl stop unit`, если semantics допускают |
| `systemctl stop unit` | Деактивировать unit | state-changing | Останавливает runtime unit | Service interruption | `systemctl status unit` | `systemctl start unit`, если semantics допускают |
| `systemctl restart unit` | Перезапустить unit | state-changing | Stop + start | Service interruption/state loss possible | Status + journal | `[Needs confirmation]` |
| `systemctl reload unit` | Reload одного unit/service | state-changing | Перечитывает поддерживаемую service config | Может изменить runtime behavior | Status + journal | `[Needs confirmation]` |
| `systemctl daemon-reload` | Перечитать unit files | state-changing | Обновляет manager view of units | Ошибочный unit file станет активной конфигурацией manager | Повторный status/show | Вернуть unit file и повторить daemon-reload |
| `systemctl start test2.target` | Активировать target с dependency | state-changing | Активирует target и зависимые units | Зависимые units тоже могут измениться | Status обоих target | Stop affected target(s), `[Needs confirmation]` по impact |
| `systemctl enable unit` | Создать persistent enablement links | state-changing | Меняет future boot/activation graph | Unit начнёт участвовать в future activation | Проверить enabled state/links | `systemctl disable unit` |
| `systemctl disable unit` | Удалить enablement links | state-changing | Меняет future boot/activation graph | Unit может не стартовать при следующей загрузке | Проверить disabled state | `systemctl enable unit`, если исходное состояние известно |
| `systemctl start echo.socket` | Запустить socket unit example | state-changing | Активирует listener/resource unit | Открывается локальный service resource | Status socket + test connection | `systemctl stop echo.socket` |
| `telnet localhost 22222` | Test echo.socket example | workload-generating | Создаёт local connection | Генерирует service instance/input | Проверить echo behavior | Закрыть connection |
| `systemctl stop echo.socket` | Остановить socket example | state-changing | Деактивирует listener | Новые connections перестанут приниматься | Status socket | `systemctl start echo.socket` |
| `mv S99httpd _S99httpd` | Исключить rc link из обработки | state-changing | Меняет legacy boot sequence | Service не стартует через этот link | Проверить имя link и runlevel behavior | Переименовать обратно в исходное имя |
| `telinit 3` | Перейти на runlevel 3 | state-changing | Меняет System V system state | Init может завершить процессы, отсутствующие в новом runlevel | `who -r` + service checks | `[Needs confirmation]` для исходного runlevel |
| `telinit q` | Перечитать System V init config | state-changing | Init перечитывает configuration | Ошибочная config может повлиять на поведение init | Проверить ожидаемый init behavior | Вернуть config и повторить reread, если возможно |
| `telinit s` | Single-user mode | state-changing | Переводит system в recovery state | Services/network могут исчезнуть | Проверить single-user state | `[Needs confirmation]` |
| `shutdown -h now` | Managed immediate halt | state-changing | Инициирует shutdown/halt | System becomes unavailable | Нормальный shutdown path до halt | N/A после halt; повторный boot |
| `shutdown -r +10` | Managed delayed reboot | state-changing | Планирует reboot и ограничивает login | System becomes unavailable at deadline | Проверить scheduled behavior/users notification | `[Needs confirmation]` |
| `mkinitramfs` | Создать initramfs | state-changing | Создаёт boot artifact | Ошибочный image может нарушить boot при его использовании | `[Needs confirmation]` — source не даёт universal validation workflow | `[Needs confirmation]` |
| `dracut` | Создать initramfs | state-changing | Создаёт boot artifact | Distribution-dependent boot risk | `[Needs confirmation]` | `[Needs confirmation]` |

## Unit file locations

Source-derived rule:

- vendor: `/lib/systemd/system` или `/usr/lib/systemd/system`;
- local: `/etc/systemd/system`.

Локальные изменения размещать в `/etc`, а не переписывать distribution-provided files.

## Service Type directives

- `Type=simple`;
- `Type=forking`;
- `Type=notify`;
- `Type=dbus`;
- `Type=oneshot`;
- `Type=idle`;
- `RemainAfterExit=yes`.

## Dependency directives

- `Requires=`;
- `Wants=`;
- `Requisite=`;
- `Conflicts=`;
- `Before=`;
- `After=`;
- `WantedBy=`;
- `RequiredBy=`;
- `DefaultDependencies=no`;
- `ConditionPathExists=`;
- `ConditionPathIsDirectory=`;
- `ConditionFileNotEmpty=`.

## System V interfaces

- `/etc/inittab`;
- `/etc/rcN.d`;
- `/etc/init.d`;
- `run-parts`;
- S-prefixed links → start;
- K-prefixed links → stop;
- numeric prefix → order.

## Safety notes

1. Не изменять vendor unit files, если local configuration может решить задачу.
2. Enable и runtime start — разные операции.
3. После unit-file changes systemd должен перечитать configuration.
4. Ordering (`Before/After`) и activation (`Wants/Requires`) — разные механизмы.
5. При смене System V runlevel init может завершить процессы.
6. Shutdown должен проходить через init system, а не hard power cut.
7. Initramfs/recovery changes зависят от distribution; source не даёт единой безопасной write procedure.
