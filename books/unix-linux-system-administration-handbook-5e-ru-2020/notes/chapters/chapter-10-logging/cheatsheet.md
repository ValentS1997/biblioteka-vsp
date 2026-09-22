# Шпаргалка: журналирование

Цель: обеспечить полный проверяемый путь события от источника до хранения, поиска, ротации и удаления.

## 1. Logging lifecycle

~~~text
event source
   ↓
collector
   ↓
filter / route
   ↓
local or central storage
   ↓
query / analysis
   ↓
rotation / archive
   ↓
retention / expiry
~~~

Наличие одного log file не означает, что logging pipeline исправен.

## 2. Где искать журналы

Глава показывает несколько типов источников и хранилищ:

- обычные text files в `/var/log`;
- binary `wtmp`;
- sparse binary `lastlog`;
- systemd journal;
- daemon-specific logs;
- kernel ring buffer.

Первый operational question:

~~~text
Кто генерирует событие?
Куда он пишет?
Кто собирает?
Кто хранит?
~~~

## 3. Systemd journal

Journal собирает данные из нескольких источников:

- `/dev/log` для Syslog-compatible messages;
- kernel channel `/dev/kmsg`;
- stdout-oriented systemd interface;
- native journal API;
- audit messages.

Основной read-only interface:

~~~bash
journalctl
~~~

## 4. Journal: useful filters

Unit:

~~~bash
journalctl -u ssh
~~~

Follow:

~~~bash
journalctl -f
~~~

Disk usage:

~~~bash
journalctl --disk-usage
~~~

Boot inventory:

~~~bash
journalctl --list-boots
~~~

Current boot + unit:

~~~bash
journalctl -b 0 -u ssh
~~~

Time window:

~~~bash
journalctl --since=yesterday --until=now
~~~

Executable / recent entries:

~~~bash
journalctl -n 100 /usr/sbin/sshd
~~~

Kernel:

~~~bash
journalctl -k
journalctl --dmesg
~~~

## 5. Journal persistence

`journald.conf` Storage modes:

~~~text
volatile   → memory only
persistent → /var/log/journal, create if needed
auto       → use /var/log/journal if it exists
none       → discard journal data
~~~

Local overrides:

~~~text
/etc/systemd/journald.conf.d/*.conf
~~~

Chapter workflow:

~~~bash
mkdir /etc/systemd/journald.conf.d/
cat <<'END' > /etc/systemd/journald.conf.d/storage.conf
[Journal]
Storage=persistent
END
systemctl restart systemd-journald
~~~

Acceptance check:

~~~bash
journalctl --disk-usage
journalctl --list-boots
~~~

## 6. Forward Secure Sealing

Chapter mentions FSS as journal integrity mechanism.

Key generation:

~~~bash
journalctl --setup-keys
~~~

Operational consequence:

- key material becomes part of security boundary;
- access and backup policy for those keys matters;
- rollback details are `[Needs confirmation]`.

## 7. Journal + Syslog coexistence

Linux systems in the chapter commonly run both:

~~~text
systemd-journald
        ↓
Syslog / rsyslog
~~~

Two integration paths described:

1. journald forwards through Syslog-compatible socket;
2. rsyslog reads journal API directly.

Trade-off:

- socket forwarding can lose journal-specific metadata;
- direct journal integration preserves richer metadata.

## 8. Syslog message model

Typical fields shown in chapter:

~~~text
timestamp
hostname
process[pid]
message payload
~~~

Applications may add their own metadata inside payload.

## 9. Syslog architecture

Rsyslog model:

~~~text
INPUT
  ↓
FILTER
  ↓
ACTION / OUTPUT
~~~

Possible inputs:

- local Syslog socket;
- UDP;
- TCP;
- files;
- journal integration;
- other modules.

Possible outputs:

- local files;
- remote hosts;
- additional processing destinations.

## 10. Facility and severity

Syslog routes based on two major dimensions:

~~~text
facility = source category
severity = importance level
~~~

This lets different event classes go to different files/servers/actions.

Do not treat all logs as one undifferentiated stream.

## 11. RainerScript

Rsyslog 8 chapter examples use RainerScript.

Input example:

~~~text
module(load="imudp")
input(type="imudp" port="514")

module(load="imtcp" KeepAlive="on")
input(type="imtcp" port="514")
~~~

Filter/action example:

~~~text
if $syslogfacility-text == 'auth' then {
    action(type="omfile" file="/var/log/auth.log")
}
~~~

Properties include:

- `$msg`;
- `$rawmsg`;
- `$hostname`;
- facility text/number;
- severity text/number;
- generated/reported timestamps.

## 12. Rsyslog reopen after rotation

When rsyslog holds a log file open:

~~~text
rename/compress without reopen
        ↓
undefined / misleading result
~~~

Chapter uses HUP to force daemon to close/reopen log files.

Conceptual workflow:

~~~text
rotate file
   ↓
HUP daemon
   ↓
daemon opens current target again
   ↓
verify new messages enter new file
~~~

## 13. Centralized logging

Centralization goals:

- one place to search across hosts;
- security/audit retention;
- off-host copy if source host fails or is compromised;
- easier fleet-wide analysis.

Transport chapter covers:

- UDP;
- TCP;
- TLS-protected forwarding.

For security-sensitive environments, encrypted forwarding is part of the design.

## 14. Kernel logging

Kernel writes into bounded internal buffer.

Linux:

~~~bash
journalctl -k
journalctl --dmesg
dmesg
~~~

FreeBSD / older Linux:

~~~bash
dmesg
~~~

Console output and stored kernel log are different concerns.

## 15. Kernel console level

Example:

~~~bash
sudo dmesg -n 2
~~~

Effect:

- reduces which kernel messages appear on console;
- does not stop messages entering kernel buffer / logging path.

Verification:

~~~bash
dmesg
journalctl -k
~~~

## 16. Special binary logs

`wtmp`:

- login/logout;
- shutdown/reboot;
- binary append-style history.

Read with:

~~~bash
last
~~~

`lastlog`:

- records most recent login per UID;
- sparse binary structure;
- should not be rotated like ordinary text log.

## 17. Rotation problem

Unbounded log growth can fill a filesystem.

Rotation must answer:

- how often?
- how many generations?
- compress when?
- what size threshold?
- what daemon reopen step?
- where archive?
- when delete?

## 18. logrotate

Main configuration:

~~~text
/etc/logrotate.conf
/etc/logrotate.d/
~~~

Useful directives from chapter:

~~~text
compress
daily / weekly / monthly
delaycompress
missingok
notifempty
olddir
prerotate
postrotate
rotate N
sharedscripts
size <threshold>
~~~

## 19. delaycompress

Use when application may keep writing to the previously rotated file.

Resulting generations:

~~~text
active log
previous rotated, still uncompressed
older rotated, compressed
~~~

This avoids compressing a file still referenced by an application.

## 20. FreeBSD newsyslog

FreeBSD default rotation tool in chapter:

~~~text
/etc/newsyslog.conf
~~~

It is typically invoked by cron.

Same operational goal as logrotate:

~~~text
limit growth
retain useful history
expire old data
~~~

## 21. Large-scale logging

When fleet size grows, local files stop being a usable analysis interface.

Chapter presents:

### ELK

~~~text
shipper
  ↓
Logstash
  ↓
Elasticsearch
  ↓
Kibana
~~~

Roles:

- Logstash → ingest/parse/filter/route;
- Elasticsearch → indexed storage/search;
- Kibana → search/UI/visualization;
- Filebeat → lightweight shipping.

## 22. ELK operational warning

ELK adds its own operational burden.

Chapter explicitly notes:

- large deployments require expertise;
- software/operations errors can lose data;
- self-hosting may cost more operationally than a managed service.

So:

~~~text
centralized logging platform
≠ zero-maintenance solution
~~~

## 23. Graylog

Graylog:

- also uses Elasticsearch;
- can ingest directly or through pipeline;
- provides different UI;
- includes RBAC/LDAP-oriented features described in chapter.

Use case: alternative centralized logging platform.

## 24. Logging as a service

Chapter names hosted/commercial options.

Core design trade-off:

~~~text
self-host
  vs
managed logging service
~~~

Compare:

- operational burden;
- cost;
- retention;
- security;
- integration;
- search/analysis capability.

## 25. Retention policy

Do not choose retention arbitrarily.

Inputs:

- business requirements;
- security policy;
- legal/regulatory requirements;
- storage capacity;
- event usefulness.

Questions from chapter:

- how many systems/apps?
- what storage exists?
- how long retain?
- which events matter?

## 26. What to capture

Chapter recommends considering at least:

- username/user ID;
- event success/failure;
- source address for network events;
- accurate date/time;
- changes to important data;
- detailed event context.

Time synchronization is therefore part of logging quality.

## 27. Tiered retention

Conceptual model from chapter:

~~~text
hot / immediately accessible
        ↓
longer-term object/archive storage
        ↓
expiry
~~~

Retention architecture should be adaptable because requirements may change.

## 28. Access control

Central log server is sensitive infrastructure.

Access should be restricted to relevant privileged operators/security/compliance roles.

Chapter additionally says:

~~~text
access to central logs should itself be logged
~~~

## 29. Monitor the logging system itself

Monitor not only log content, but the pipeline.

Examples:

- log stopped growing;
- collector stopped receiving;
- disk nearing full;
- forwarding broken;
- rotation not happening;
- archive/retention job failed.

Absence of events can be an event.

## 30. Minimal troubleshooting flow

~~~text
Problem observed
   ↓
identify service/source
   ↓
journalctl / text log / dmesg
   ↓
confirm event is generated
   ↓
confirm collector receives it
   ↓
confirm filter/routing rule
   ↓
confirm destination/storage
   ↓
confirm rotation/retention
   ↓
fix one layer
   ↓
generate test event
   ↓
verify end-to-end
~~~

For Syslog testing chapter provides:

~~~bash
logger -p local5.warning "test message"
~~~

## Acceptance criteria

- source of each critical event class is known;
- journal persistence policy is explicit;
- current boot/time/unit filters work;
- rsyslog input/filter/action path is documented;
- central forwarding is verified with a test event;
- kernel logs are retrievable independently of console verbosity;
- rotation prevents uncontrolled disk growth;
- daemon reopen semantics are accounted for;
- retention period has an explicit owner/reason;
- central log access is restricted and auditable;
- pipeline health is monitored, including stopped log growth;
- unknown rollback is marked `[Needs confirmation]`.
