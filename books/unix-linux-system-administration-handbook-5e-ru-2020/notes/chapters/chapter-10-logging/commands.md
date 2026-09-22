# Команды главы 10

Только команды и формы команд, подтверждённые RAG главы 10.

| Команда | Назначение | Что проверить | Тип |
|---|---|---|---|
| `journalctl -u ssh` | Показать journal messages для SSH unit | timestamps, process/unit messages | read-only |
| `journalctl -f` | Follow новых journal messages | новые записи появляются в реальном времени | read-only / long-running |
| `journalctl --disk-usage` | Показать объем journal на диске | current journal footprint | read-only |
| `journalctl --list-boots` | Показать boots, известные journal | boot IDs и time ranges | read-only |
| `journalctl -b 0 -u ssh` | Показать SSH messages текущей загрузки | только current boot/unit | read-only |
| `journalctl --since=yesterday --until=now` | Ограничить journal time range | нужный интервал времени | read-only |
| `journalctl -n 100 /usr/sbin/sshd` | Показать последние 100 записей для executable | count и executable filter | read-only |
| `journalctl --help` | Краткая справка по journalctl | available options | read-only |
| `journalctl --setup-keys` | Создать keys для Forward Secure Sealing | keys созданы и защищены | state-changing / credential-generating |
| `mkdir /etc/systemd/journald.conf.d/` | Создать directory для local journald overrides | directory exists | state-changing |
| `systemctl restart systemd-journald` | Применить измененную journald configuration | service restarted; logging continues | state-changing |
| `last` | Прочитать binary `wtmp` login/reboot history | decoded session records | read-only |
| `cat /var/log/syslog` | Пример чтения text Syslog file | timestamp/host/process/payload fields | read-only |
| `grep <pattern> <log>` | Фильтровать text log | expected matching lines | read-only |
| `less <log>` | Просматривать text log | log content without modifying it | read-only |
| `awk ... <log>` | Text processing Syslog messages | selected/transformed fields | read-only |
| `sudo kill -HUP <rsyslogd-pid>` | Заставить rsyslogd закрыть/reopen open log files | daemon продолжает logging в current file | state-changing |
| `logger -p local5.warning "test message"` | Сгенерировать test Syslog message с facility/severity | message arrives at configured destination | workload-generating / test |
| `journalctl -k` | Показать kernel messages из journal | kernel event stream | read-only |
| `journalctl --dmesg` | Alias-style kernel journal view, указанный в главе | kernel event stream | read-only |
| `dmesg` | Показать kernel ring buffer | boot/kernel messages | read-only |
| `sudo dmesg -n 2` | Изменить console threshold kernel messages | console verbosity changed; collection continues | state-changing |

## Journald persistent-storage workflow

Глава показывает local override вместо прямого редактирования основного `journald.conf`:

~~~bash
mkdir /etc/systemd/journald.conf.d/
cat <<'END' > /etc/systemd/journald.conf.d/storage.conf
[Journal]
Storage=persistent
END
systemctl restart systemd-journald
~~~

Тип: state-changing.

Проверка после изменения:

~~~bash
journalctl --disk-usage
journalctl --list-boots
~~~

Критерий: journal сохраняется и содержит ожидаемые boot/session records.

## Rsyslog configuration fragments из главы

Rsyslog рассматривается как:

~~~text
input → filter → action
~~~

Пример загрузки UDP/TCP inputs в RainerScript:

~~~text
module(load="imudp")
input(type="imudp" port="514")

module(load="imtcp" KeepAlive="on")
input(type="imtcp" port="514")
~~~

Пример filtering по property:

~~~text
if $syslogfacility-text == 'auth' then {
    action(type="omfile" file="/var/log/auth.log")
}
~~~

Это configuration, не shell commands. После изменения rsyslog configuration daemon должен перечитать/перезапустить configuration согласно platform workflow; конкретная универсальная restart-command для всех рассматриваемых систем в RAG не зафиксирована.

## Rotation-related configuration из главы

`logrotate` поддерживает, среди прочего:

- `compress`;
- `daily` / `weekly` / `monthly`;
- `delaycompress`;
- `missingok`;
- `notifempty`;
- `olddir`;
- `prerotate` / `postrotate`;
- `rotate N`;
- `sharedscripts`;
- `size <threshold>`.

Глава показывает `postrotate` с HUP daemon после rotation. Причина: compress/rename open log без reopen может привести к непредсказуемому поведению.

## Safety / operational notes

- `journalctl -f` и `tail -f` — long-running observation, не modification.
- `systemctl restart systemd-journald` изменяет runtime state; после restart проверить, что logging не прервался.
- `journalctl --setup-keys` создает cryptographic key material; universal rollback в главе не описан: `[Needs confirmation]`.
- `dmesg -n 2` меняет только console threshold; kernel messages продолжают попадать в log buffer/Syslog.
- HUP для rsyslogd используется перед/после rotation, чтобы daemon reopen log descriptors.
- Network Syslog может использовать UDP/TCP; chapter отдельно рассматривает TLS configuration для защищенной передачи.
- Не считать наличие local log доказательством end-to-end logging: проверять source → collector → routing → storage → retention.
