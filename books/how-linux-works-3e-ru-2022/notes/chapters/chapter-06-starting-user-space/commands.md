# Команды и интерфейсы главы 6

Только элементы, явно подтверждённые RAG главы 6.

| Команда / интерфейс | Назначение | Тип | Verification / risk |
|---|---|---|---|
| `systemd-analyze dot` | Построить dependency graph systemd | read-only/workload-generating | Полный graph может быть очень большим |
| `systemctl -p UnitPath show` | Показать unit search path и priority | read-only | Проверить источник unit file |
| `pkg-config systemd --variable=systemdsystemunitdir` | Показать vendor system unit dir | read-only | Обычно /lib или /usr/lib/systemd/system |
| `pkg-config systemd --variable=systemdsystemconfdir` | Показать local config dir | read-only | Обычно /etc/systemd/system |
| `systemctl list-units` | Показать active units | read-only | `--full` и `--all` также упомянуты |
| `systemctl status sshd.service` | Unit status + process/cgroup/log context | read-only | Базовый troubleshooting check |
| `systemd-cgls` | Показать system cgroup hierarchy | read-only | Связь processes с units |
| `journalctl --unit=unit_name` | Показать journal messages unit | read-only | Права доступа зависят от системы |
| `systemctl start unit` | Активировать unit | state-changing | Проверить status |
| `systemctl stop unit` | Деактивировать unit | state-changing | Проверить dependents/impact |
| `systemctl restart unit` | Перезапустить unit | state-changing | Возможен service interruption |
| `systemctl reload unit` | Reload configuration одного unit/service | state-changing | Проверить результат через status |
| `systemctl daemon-reload` | Перечитать все unit files | state-changing | Нужен после unit-file changes |
| `systemctl list-jobs` | Показать pending/running systemd jobs | read-only | Полезно при долгом boot/start |
| `systemctl start test2.target` | Source example activation with dependency | state-changing | Проверить оба target units |
| `systemctl status test1.target test2.target` | Verify example target state | read-only | Проверка activation graph |
| `systemctl enable unit` | Создать persistent enablement links | state-changing | Enable не равно start |
| `systemctl disable unit` | Удалить enablement links | state-changing | Disable не равно stop |
| `systemctl show -p type unit` | Показать dependency property, где type = Wants/Requires и т. п. | read-only | Generic form из source |
| `systemctl start echo.socket` | Запустить socket unit example | state-changing | Открывает resource unit |
| `telnet localhost 22222` | Проверить echo.socket example | workload-generating | Test connection к localhost |
| `systemctl stop echo.socket` | Остановить socket example | state-changing | Завершает resource activation |
| `who -r` | Показать System V runlevel | read-only | Legacy context |
| `mv S99httpd _S99httpd` | Исключить rc link из обработки без потери исходного имени | state-changing | Legacy System V example |
| `telinit 3` | Перейти на runlevel 3 | state-changing | Init может остановить процессы, которых нет в новом runlevel |
| `telinit q` | Перечитать System V init configuration | state-changing | Source management operation |
| `telinit s` | Перейти в single-user mode | state-changing | Legacy recovery path |
| `shutdown -h now` | Managed immediate halt | state-changing | Дождаться нормального shutdown |
| `shutdown -r +10` | Managed reboot через 10 минут | state-changing | Delayed shutdown создаёт /etc/nologin |
| `unmkinitramfs` | Inspect/extract initramfs archive | read-only/extraction | Exact invocation в главе не задан |
| `mkinitramfs` | Создание initramfs | state-changing | Universal workflow в source не задан |
| `dracut` | Создание initramfs | state-changing | Distribution-dependent |

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
