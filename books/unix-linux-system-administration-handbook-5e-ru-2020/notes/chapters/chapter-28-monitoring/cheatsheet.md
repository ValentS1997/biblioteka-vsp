# Шпаргалка: Monitoring

## 1. Production gate

~~~text
No monitoring
→ no production
~~~

Server/service enters production only after monitoring coverage exists.

## 2. Monitoring pipeline

~~~text
source
→ collect
→ normalize/store
→ evaluate
→ alert / automate / retain
→ investigate
→ improve
~~~

## 3. Data classes

Real-time metrics:
- numbers/booleans;
- threshold/range based.

Events:
- log records;
- state changes;
- subsystem notifications.

Historical trends:
- time series;
- baselines;
- long-term comparison.

## 4. Metric-selection rule

For every metric ask:
- Why collect it?
- Who uses it?
- What decision/action follows?
- How long must it be retained?

No clear purpose → do not collect it.

## 5. Time-series retention

Fresh data:
- high resolution.

Older data:
- aggregate/roll up.

Aggregation depends on semantics:
- counters → sum;
- utilization → average;
- bounds → min/max.

Chapter example:
~~~text
10s → 12h
1m  → 7d
10m → 1y
~~~

Example only, not a universal policy.

## 6. Alert design

Good alert:
~~~text
signal
→ owner
→ expected action
→ escalation
→ runbook
~~~

Bad alert:
- no action;
- false-positive;
- too noisy;
- wakes on-call for noncritical issue.

## 7. Dashboards

A dashboard should:
- select important metrics;
- show context;
- group related values;
- visualize trends;
- support quick health assessment.

Not every collected metric belongs on a dashboard.

## 8. Monitoring culture

Monitor:
- user/service dependencies;
- hardware health;
- every HA member;
- the monitoring platform itself.

After missed outage:
~~~text
incident
→ identify missing signal
→ add monitoring
~~~

## 9. Platform families

Threshold / real-time:
- Nagios;
- Icinga;
- Sensu.

Time-series:
- Graphite;
- Prometheus;
- InfluxDB;
- Munin.

Visualization:
- Grafana;
- Graphite UI.

Current product status outside the chapter:
[Needs confirmation].

## 10. Platform selection

Evaluate:
- source flexibility;
- dashboard quality;
- cost;
- discovery;
- notifications/reporting;
- config-management integration;
- plugin deployment;
- network requirements.

## 11. StatsD

~~~text
app/script
→ StatsD UDP
→ monitoring backend
→ time series
→ dashboard/alerts
~~~

Test write:
~~~bash
echo "sample.count:1|c" | nc -u -w0 statsd.admin.com 8125
~~~

Verify in backend before scaling use.

## 12. Parse command output carefully

Example:
~~~bash
uptime
uptime | perl -anF'[\s,]+' -e 'print $F[10]'
~~~

Before parsing:
- inspect man page;
- prefer machine-friendly output if available;
- request only required fields;
- suppress headers where supported.

## 13. Network monitoring

ICMP echo:
~~~text
reply = network path + target IP stack responds
~~~

It does not prove application health.

Use packet-loss trend, not one failed packet, as stronger evidence.

## 14. System monitoring commands

~~~text
df      disk/inodes
du      directory size
free    RAM/swap
iostat  disk throughput/performance
lsof    open files/ports
mpstat  per-CPU use
vmstat  process/CPU/memory
sar     system activity
uptime  load/uptime
~~~

Linux source:
~~~text
/proc
~~~

FreeBSD example:
~~~bash
sysctl -n vm.loadavg
~~~

## 15. sar example

~~~bash
sar -n DEV 2 30
~~~

Interpret:
- packets/s;
- bytes/s;
- active/unused interfaces.

## 16. collectd

Continuous daemon-based collection.

Chapter sample:
- Interval 30;
- CPU;
- filesystem;
- disk;
- interface;
- load;
- memory;
- processes;
- RRDtool output.

Verify actual metrics and destination after config change.

## 17. Deep tracing

Mentioned:
- sysdig;
- dtrace.

Use for deep kernel/process visibility.

Exact chapter command examples:
[Needs confirmation].

## 18. Application monitoring

Work with developers/business owners.

Possible chapter examples:
- page load time;
- PHP errors;
- MySQL behavior;
- connection failures;
- sales/cart metrics.

Best signal may exist above OS/network layers.

## 19. Log monitoring

~~~text
logs
→ parse/aggregate
→ event/rate
→ alert/report/search
~~~

Chapter tools:
- logwatch → batch summaries;
- OSSEC → more real-time monitoring.

## 20. Security monitoring

Minimum continuous functions:
- FIM;
- IDS.

Tools mentioned:
- Tripwire;
- OSSEC;
- AIDE;
- mtree;
- Snort.

## 21. FIM

~~~text
trusted baseline
→ current state
→ hash comparison
→ investigate difference
~~~

Baseline must be trusted before capture.

Authorized updates can legitimately change files.

## 22. mtree

Create baseline:
~~~bash
mtree -c -K sha512 -s <KEY> -p /sbin > <baseline-file>
~~~

Verify:
~~~bash
mtree -s <KEY> -p /sbin < <baseline-file>
~~~

Do not silently replace baseline after unexplained change.

## 23. HIDS / NIDS

NIDS:
- observes network traffic.

HIDS:
- observes host state;
- checksums/files;
- connections;
- logs;
- privilege events;
- rootkit indicators.

Alerts must enter normal ticket/incident workflow.

## 24. SNMP model

~~~text
manager
↕ get / get-next / set
agent
→ trap
~~~

Data model:
~~~text
MIB
→ OID
→ value
~~~

Best chapter use:
- specialized/network devices;
- low-level collection;
- forward data to general monitoring platform.

## 25. Net-SNMP reads

~~~bash
snmpwalk -c <community> -v1 <host>
snmpget -v 2c -c <community> localhost <OID>
~~~

Treat community string as credential.

## 26. SNMP writes

~~~text
snmpset = state-changing
snmptrap = sends notification
~~~

Never use snmpset without:
- exact target OID;
- intended current/new value;
- authorization;
- rollback value.

## 27. On-call discipline

Avoid burnout:
- rotate responders;
- identify true 24×7 conditions;
- keep nonurgent work for business hours.

Alert existence ≠ immediate page.

## 28. Noise control

False positive:
~~~text
do not ignore
→ fix threshold/check/design
~~~

Alert fatigue makes real incidents invisible.

## 29. Runbooks

Routine:
- restart;
- reset;
- repair;

should have a documented procedure understandable by an administrator unfamiliar with the system.

## 30. Monitor monitoring

Monitoring platform failure can hide every downstream incident.

Therefore:
~~~text
monitoring platform
→ independent health check
~~~

## 31. Acceptance checklist

Before production:
- owner known;
- dependencies known;
- metrics/events selected;
- collection works;
- history retained;
- alerts actionable;
- escalation configured;
- runbook exists;
- monitoring platform health checked.

Environment-specific thresholds:
[Needs confirmation].
