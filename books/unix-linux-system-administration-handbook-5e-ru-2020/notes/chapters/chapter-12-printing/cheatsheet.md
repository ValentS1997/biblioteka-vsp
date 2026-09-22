# Шпаргалка: печать и CUPS

Цель: локализовать print failure по конкретному слою — submission, queue, filter, backend, network или physical device.

## 1. Общая модель печати

~~~text
user/app
  ↓
CUPS client command
  ↓
cupsd
  ↓
queue
  ↓
MIME detection
  ↓
PPD + filter chain
  ↓
backend
  ↓
printer
~~~

CUPS — client/server printing system.

## 2. Базовые компоненты

Глава выделяет:

- spool/queue;
- user-level utilities;
- server services;
- network protocol;
- filters;
- backends;
- printer device.

Одна команда lpr не равна всей системе печати.

## 3. CUPS / IPP

CUPS clients и servers взаимодействуют через HTTP-oriented IPP.

Administrative web interface chapter связывает с CUPS server на port 631.

CLI и GUI являются разными frontends к одному server state.

## 4. Отправка job

~~~bash
lpr foo.pdf /tmp/testprint.ps
~~~

Что происходит:

~~~text
copy files to cupsd
   ↓
queue
   ↓
wait until printer available
   ↓
process filters
   ↓
backend sends job
~~~

## 5. Queue inspection

~~~bash
lpq
lpstat -t
~~~

Use job ID from queue output for job-level actions.

Cancel:

~~~bash
lprm <job-id>
~~~

## 6. Default printer

Shell-local:

~~~bash
export PRINTER=<printer>
~~~

CUPS option:

~~~bash
lpoptions -d <printer>
~~~

Inspect options:

~~~bash
lpoptions -l
~~~

## 7. Printer instances

One physical queue can have several logical instances with different defaults.

Chapter example:

~~~bash
lpoptions -p Phaser_6120/2up \
  -o number-up=2 \
  -o job-sheets=standard
~~~

Then:

~~~bash
lpr -P Phaser_6120/2up biglisting.ps
~~~

Use case: draft/production behavior without redefining physical printer each time.

## 8. PPD

PPD describes printer capabilities.

CUPS uses document properties + PPD to decide what processing is required before sending data to printer.

Despite name, PPD is used beyond strictly PostScript printers in chapter model.

## 9. MIME detection

Source:

~~~text
/etc/cups/mime.types
~~~

Purpose:

~~~text
document bytes / extension
        ↓
MIME type
~~~

Example in chapter identifies PDF via extension/content signature.

## 10. Filter graph

Source:

~~~text
/etc/cups/mime.convs
~~~

Concept:

~~~text
input MIME
  ↓
candidate conversion chains
  ↓
cost
  ↓
lowest-cost valid chain
  ↓
printer-ready format
~~~

## 11. Filters

Filters may:

- convert document formats;
- alter layout;
- rasterize;
- add printer-specific control data;
- prepare job for backend.

Find installed filters near pstops:

~~~bash
locate pstops
~~~

## 12. Backend

Backend is the last server-side stage.

It handles transport to printer.

Inspect visible backend/device types:

~~~bash
lpinfo -v
~~~

Chapter URI examples include:

- ipp;
- lpd;
- serial;
- socket;
- usb.

## 13. Printer creation

Local example:

~~~bash
sudo lpadmin -p groucho -E \
  -v parallel:/dev/lp0 \
  -m pxlcolor.ppd
~~~

Network example:

~~~bash
sudo lpadmin -p fezmo -E \
  -v socket://192.168.0.12 \
  -m laserjet.ppd
~~~

Verify queue, URI, PPD and device before accepting production jobs.

## 14. Delete printer

~~~bash
lpadmin -x fezmo
~~~

This removes queue definition.

Rollback requires prior URI/PPD/options: [Needs confirmation].

## 15. Queue has two sides

Input side:

~~~text
accept / reject
~~~

Output side:

~~~text
cupsenable / cupsdisable
~~~

Important distinction:

~~~text
reject
→ no new jobs

cupsdisable
→ jobs may still enter queue, but printing stops
~~~

## 16. Short vs long outage

Short maintenance:

~~~bash
cupsdisable <printer>
~~~

Use when interruption is brief.

Long outage:

~~~bash
reject <printer>
~~~

Use when accepting more jobs would only build a useless backlog.

After recovery:

~~~bash
cupsenable <printer>
accept <printer>
~~~

## 17. CUPS server config

Main configuration:

~~~text
/etc/cups/cupsd.conf
~~~

Manual configuration changes require daemon restart to take effect in chapter workflow.

Example shown:

~~~bash
systemctl restart org.cups.cupsd.service
~~~

Then verify:

~~~bash
lpstat -t
~~~

## 18. Network access

CUPS server must satisfy all of:

~~~text
daemon reachable
+
queue exists
+
client knows destination
+
server allows request
+
backend can reach printer
~~~

Chapter shows network policy/advertising directives in cupsd.conf.

## 19. Printer discovery across subnets

Within one subnet CUPS can advertise printers.

Across subnet boundaries chapter shows poll/relay pattern:

~~~text
remote CUPS servers
      ↓
BrowsePoll
      ↓
subordinate CUPS server
      ↓
BrowseRelay
      ↓
local subnet
~~~

Do not copy network addresses from example; they are source examples only.

## 20. Direct USB diagnostic

Run backend directly:

~~~bash
/usr/lib/cups/backend/usb
~~~

Interpretation:

- printer URI present → CUPS backend can see device;
- printer URI disappears when cable/device is absent → physical/USB layer is confirmed.

This is a strong layer-localization check.

## 21. Remote CUPS diagnostic

~~~bash
telnet <host> 631
~~~

Purpose: verify basic TCP path to remote cupsd.

Failure here means queue/filter debugging is premature.

## 22. Logs

CUPS maintains three log classes in chapter:

- page log;
- access log;
- error log.

Paths and logging level are configured via cupsd.conf, commonly under /var/log in chapter examples.

## 23. Troubleshooting order

~~~text
1. lpstat -t
2. lpq
3. check input/output queue state
4. inspect CUPS logs
5. lpinfo -v
6. verify PPD/filter path
7. run direct backend if local printer
8. test TCP/631 if remote server
9. verify physical/network printer
10. make one change
11. submit controlled test job
~~~

## 24. Failure interpretation

Symptom:

~~~text
job never enters queue
~~~

Check:

- reject state;
- access policy;
- client destination;
- server reachability.

Symptom:

~~~text
job enters queue but does not start
~~~

Check:

- cupsdisable state;
- printer availability;
- queue status;
- daemon/log errors.

Symptom:

~~~text
job starts but output is wrong
~~~

Check:

- MIME detection;
- PPD;
- filter chain;
- printer capabilities.

Symptom:

~~~text
backend does not see USB printer
~~~

Check cable/device presence and local USB/device layer.

Symptom:

~~~text
network printer unreachable
~~~

Check IP configuration, route/reachability, backend URI and remote print server port.

## 25. Operational workflow

~~~text
Need printer
  ↓
discover backend/device
  ↓
create queue + URI + PPD
  ↓
verify queue state
  ↓
submit test job
  ↓
observe filters/backend
  ↓
verify physical output
  ↓
publish/accept production jobs
~~~

Troubleshooting:

~~~text
symptom
  ↓
queue?
  ↓
filter?
  ↓
backend?
  ↓
network/device?
  ↓
one controlled change
  ↓
test job
~~~

## Acceptance criteria

- intended queue is visible in lpstat;
- default printer/instance is explicit;
- URI points to intended device/server;
- PPD/model choice is known;
- queue input/output state is intentional;
- CUPS server is reachable where network printing is required;
- direct backend sees local printer when expected;
- CUPS logs show the expected job/filter/backend sequence;
- one controlled test job prints correctly;
- destructive queue removal has prior config or rollback is [Needs confirmation].
