# Команды главы 28

Только команды и command forms, подтверждённые RAG главы 28.

## Read-only / observation

| Команда | Назначение | Что проверить | Тип |
|---|---|---|---|
| uptime | Uptime, users, load averages | current 1/5/15-minute load | read-only |
| uptime \| perl -anF'[\\s,]+' -e 'print $F[10]' | Извлечь 1-minute load из вывода uptime | parser returns intended field | read-only |
| sysctl -n vm.loadavg | FreeBSD load average | expected load values | read-only |
| df | Disk space / inode information | capacity/inode pressure | read-only |
| du | Directory sizes | unexpected growth | read-only |
| free | Memory and swap | memory pressure | read-only |
| iostat | Disk performance / throughput | storage activity | read-only |
| lsof | Open files and network ports | owning process / unexpected handles | read-only |
| mpstat | Per-CPU utilization | CPU distribution | read-only |
| vmstat | Process, CPU and memory statistics | load/memory/process behavior | read-only |
| sar -n DEV 2 30 | Network interface statistics every 2 seconds, 30 reports | packets/bytes/interface use | workload-generating |
| snmpget ... | Read one SNMP variable | expected OID value | workload-generating |
| snmpgetnext ... | Read next SNMP variable | traversal result | workload-generating |
| snmpwalk ... | Walk MIB tree | available OIDs/values | workload-generating |
| snmpdelta ... | Observe SNMP variable changes over time | rate/change | workload-generating |
| snmpdf ... | Remote disk-space information through SNMP | capacity data | workload-generating |
| snmptable ... | Read SNMP table | table contents | workload-generating |
| snmptranslate ... | Resolve/describe OIDs | MIB/OID mapping | read-only |

Notes:
- chapter also names w and top as load sources;
- top is explicitly described as a poor choice for non-interactive automation;
- exact stable parse format must be selected per command where supported.

## Network probes

Chapter names ping and ping6 for ICMP echo probing.

Type:
- workload-generating.

Interpretation:
- successful reply confirms reachability/IP-stack response;
- it does not prove application health;
- individual packet loss should not automatically be treated as outage;
- aggregate loss over time is more meaningful.

The chapter also mentions iPerf for throughput measurement, but does not provide an exact command line here. Exact invocation: [Needs confirmation].

## StatsD test metric

Chapter example, OCR-normalized:

~~~bash
echo "sample.count:1|c" | nc -u -w0 statsd.admin.com 8125
~~~

Purpose:
- send a test counter to StatsD over UDP.

Type:
- workload-generating / writes monitoring data.

Precondition:
- StatsD endpoint and dataset are intentionally configured.

Verification:
- sample.count appears in the Graphite/monitoring view.

Rollback:
- metric write is transient; removal of already persisted time-series data is [Needs confirmation].

## Clone StatsD source

Chapter example:

~~~bash
git clone https://github.com/etsy/statsd
~~~

Purpose:
- obtain the Etsy StatsD implementation.

Type:
- state-changing: creates a local repository directory.

Verification:
- repository clone exists and contains expected source.

Rollback:
- exact source-supported cleanup command is not provided: [Needs confirmation].

## Carbon / Graphite configuration

The chapter modifies:
- /etc/carbon/storage-schemas.conf
- /etc/carbon/storage-aggregation.conf

Example retention policy:

~~~text
[stats]
pattern = ^stats.*
retentions = 10s:12h,1min:7d,10min:1y
~~~

Type:
- state-changing configuration.

Effect:
- changes retention/resolution rules.

Risk:
- inappropriate aggregation/retention can produce missing, misleading or unnecessarily expensive data.

Verification:
- expected series are retained and rolled up at intended resolution.

Rollback:
- restore previous configuration files;
- exact reload/restart command is not provided by the chapter: [Needs confirmation].

## collectd configuration

Chapter sample config sets:
- Hostname;
- Interval 30;
- syslog plugin;
- cpu, df, disk, interface, load, memory, processes, rrdtool plugins;
- DataDir /var/lib/collectd/rrd.

Type:
- state-changing configuration.

Verification:
- configured metrics are collected at expected interval;
- RRDtool-compatible data appears in configured DataDir.

Rollback:
- restore previous collectd configuration;
- exact service restart/reload command is not provided: [Needs confirmation].

## File integrity monitoring with mtree

Chapter baseline logic:

~~~bash
mtree -c -K sha512 -s <KEY> -p /sbin > <baseline-file>
~~~

Purpose:
- create a cryptographically hashed baseline for /sbin.

Type:
- state-changing: writes baseline data.

Precondition:
- system is already trusted/known-good.

Risk:
- a baseline created after compromise canonizes the compromised state.

Verification form from the chapter:

~~~bash
mtree -s <KEY> -p /sbin < <baseline-file>
~~~

Type:
- read-only comparison.

Interpretation:
- differences must be correlated with authorized maintenance/patching before being treated as malicious.

Rollback:
- baseline replacement procedure must follow local change process; exact command: [Needs confirmation].

## Net-SNMP package installation

Debian/Ubuntu example:

~~~bash
apt-get install snmp
~~~

Red Hat/CentOS example, OCR-normalized:

~~~bash
yum install net-snmp-tools
~~~

FreeBSD example:

~~~bash
pkg install net-snmp
~~~

Type:
- state-changing.

Effect:
- installs Net-SNMP client/tools packages.

Verification:
- required Net-SNMP commands become available.

Rollback:
- package-removal command is not supplied in the chapter: [Needs confirmation].

## Start SNMP agent

Linux example:

~~~bash
systemctl start snmpd
~~~

Type:
- state-changing.

Important chapter boundary:
- the chapter discourages running an SNMP agent on UNIX/Linux unless there is a specific need, such as basic network-configuration queries;
- prefer SNMP as a low-level collection protocol for specialized/network devices.

Verification:
- required monitoring queries succeed.

Rollback:
- exact source-supported stop/disable commands: [Needs confirmation].

FreeBSD boot configuration shown by chapter:

~~~text
snmpd_enable="YES"
~~~

This is a persistent state change in /etc/rc.conf.

## SNMP read example

Chapter example generalized to avoid embedding a real community string:

~~~bash
snmpwalk -c <community> -v1 <host>
~~~

Type:
- workload-generating/read-only SNMP query.

Security:
- community string is a credential and should not be exposed in logs/scripts unnecessarily.

Chapter also shows an SNMPv2c get form:

~~~bash
snmpget -v 2c -c <community> localhost <OID>
~~~

Type:
- workload-generating/read-only.

## SNMP write operations

The Net-SNMP suite includes:

~~~text
snmpset
snmptrap
~~~

snmpset:
- state-changing;
- writes an exposed SNMP variable on an agent/device;
- use only with explicit authorization and an identified rollback value.

snmptrap:
- workload-generating;
- sends an asynchronous SNMP notification.

Exact safe test OIDs/values are environment-specific: [Needs confirmation].

## Commands not expanded here

Chapter mentions sysdig and dtrace as deep tracing tools, but provides no exact command lines in this chapter.

Do not invent invocations.

## Operational rule

Monitoring commands should first answer:
~~~text
What signal do we need?
→ What source provides it?
→ Is collection stable?
→ What threshold/context makes it actionable?
→ Who responds?
~~~

Do not turn a convenient command output into a production alert without validating its semantics and parser stability.
