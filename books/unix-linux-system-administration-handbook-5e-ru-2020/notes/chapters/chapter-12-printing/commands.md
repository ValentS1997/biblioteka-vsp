# Команды главы 12

Только команды и формы команд, подтверждённые RAG главы 12.

| Команда | Назначение | Что проверить | Тип |
|---|---|---|---|
| `lpr foo.pdf /tmp/testprint.ps` | Отправить files в CUPS queue | job получил ID и появился в queue | state-changing / workload-generating |
| `lpq` | Показать состояние print queue | job IDs, queue order/status | read-only |
| `lprm <job-id>` | Отменить конкретное print job | job исчез из queue | state-changing |
| `lpstat -t` | Сводное состояние CUPS server/queues/printers | server, default printer, queues, jobs | read-only |
| `export PRINTER=<printer>` | Задать default printer в shell environment | subsequent CLI uses intended queue | state-changing / session-local |
| `lpoptions -d <printer>` | Задать default printer через CUPS options | default points to intended printer | state-changing |
| `lpoptions -l` | Показать текущие printer options | available/current options | read-only |
| `lpoptions -p Phaser_6120/2up -o number-up=2 -o job-sheets=standard` | Создать printer instance с отдельными defaults | instance exists with intended options | state-changing |
| `lpr -P Phaser_6120/2up biglisting.ps` | Отправить job в конкретный printer instance | job enters intended instance queue | state-changing / workload-generating |
| `locate pstops` | Найти installed CUPS filters рядом с pstops | filter binaries/files are present | read-only |
| `lpinfo -v` | Показать доступные devices/backends и URI types | intended backend/device appears | read-only |
| `sudo lpadmin -p groucho -E -v parallel:/dev/lp0 -m pxlcolor.ppd` | Создать/настроить local printer example | queue/device URI/PPD match intended printer | state-changing |
| `sudo lpadmin -p fezmo -E -v socket://192.168.0.12 -m laserjet.ppd` | Создать network printer example | queue, URI and PPD are correct | state-changing |
| `lpadmin -x fezmo` | Удалить printer/class | queue removed; no required jobs/options lost | state-changing / destructive |
| `sudo cupsdisable groucho` | Остановить output side queue: jobs могут приниматься, но не печататься | printer disabled; queued jobs retained | state-changing |
| `cupsenable <printer>` | Возобновить output side queue | printer enabled and can process queued jobs | state-changing |
| `sudo reject corbet` | Запретить прием новых jobs в queue | new submissions rejected | state-changing |
| `accept <printer>` | Разрешить прием новых jobs | submissions accepted again | state-changing |
| `systemctl restart org.cups.cupsd.service` | Restart cupsd after manual configuration change, as shown in chapter | daemon returns healthy and queues remain visible | state-changing |
| `/usr/lib/cups/backend/usb` | Напрямую проверить USB backend/device visibility | physical printer URI appears/disappears with connection | read-only / hardware probe |
| `telnet <host> 631` | Проверить TCP reachability of remote CUPS daemon | connection to CUPS port succeeds/fails | read-only / network |
| `cancel <job-id>` | System V-compatible job cancellation command listed by CUPS | target job cancelled | state-changing |
| `lp <file>` | System V-compatible print submission command listed by CUPS | job enters intended queue | state-changing / workload-generating |
| `lpmove ...` | Переместить print job, command listed by CUPS | target job moved to intended destination | state-changing |
| `lpc` | BSD-compatible printer-control frontend listed by CUPS | requested printer-control/status action | depends on subcommand |

## CUPS pipeline behind the commands

~~~text
lpr/lp
  ↓
cupsd
  ↓
queue
  ↓
MIME type + PPD
  ↓
filter chain
  ↓
backend
  ↓
printer
~~~

Troubleshooting command should target a specific layer instead of changing multiple layers at once.

## Queue semantics

Output side:

~~~bash
cupsdisable <printer>
cupsenable <printer>
~~~

Input side:

~~~bash
reject <printer>
accept <printer>
~~~

Chapter distinction:

- short maintenance: stopping printer/output side can preserve incoming jobs;
- long outage: rejecting new jobs avoids accumulating jobs that cannot be printed soon.

## Printer configuration examples

Local parallel printer:

~~~bash
sudo lpadmin -p groucho -E -v parallel:/dev/lp0 -m pxlcolor.ppd
~~~

Network printer:

~~~bash
sudo lpadmin -p fezmo -E -v socket://192.168.0.12 -m laserjet.ppd
~~~

Other URI forms shown in the chapter include IPP, LPD, serial, raw socket and USB.

Before applying a printer definition, verify target device/host, URI scheme, PPD/model choice, access policy and whether an existing queue will be replaced or removed.

## Configuration locations

- `/etc/cups/cupsd.conf` — CUPS server configuration.
- `/etc/cups/lpoptions` — system defaults when lpoptions is run as root.
- per-user CUPS options — user-local CUPS options file as described in chapter.
- `/etc/cups/mime.types` — MIME detection rules.
- `/etc/cups/mime.convs` — conversion/filter graph.
- printer PPD — capabilities and printer-specific filter information.
- CUPS logs — paths configured from cupsd.conf, normally under `/var/log` in chapter examples.

## Network configuration

Chapter shows CUPS network access/advertising through cupsd.conf, including location access rules, BrowseAddress, BrowsePoll and BrowseRelay.

These are configuration directives, not shell commands. Exact network values are environment-specific and must not be copied blindly.

## Read-only troubleshooting order

~~~bash
lpstat -t
lpq
lpinfo -v
~~~

Then inspect CUPS page/access/error logs.

For direct USB visibility:

~~~bash
/usr/lib/cups/backend/usb
~~~

For remote daemon reachability:

~~~bash
telnet <host> 631
~~~

Interpretation:

- queue healthy, backend missing device → problem is below queue/filter layer;
- backend sees printer, job fails before backend → inspect MIME/filter/PPD and logs;
- remote port unreachable → network/daemon path before queue analysis;
- queue rejects jobs → inspect input-side state/access policy;
- queue accepts jobs but never prints → inspect output-side state/backend/device.

## Safety / rollback

- lprm/cancel remove queued work; deleted print jobs are not recoverable from the queue unless source data is resubmitted.
- lpadmin -x removes a printer/class definition. Exact rollback requires the previous configuration/PPD/URI: `[Needs confirmation]`.
- cupsdisable and reject are reversible with cupsenable and accept.
- Manual cupsd.conf changes require preserving the prior configuration for rollback: `[Needs confirmation]`.
- After manual server configuration changes, restart/reload behavior must be verified by lpstat -t and a controlled test job.
