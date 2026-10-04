# Chapter 19 — Segment 03

Source RAG: `p0625:c01`–`p0630:c01`

Modern OT attacks все меньше зависят от technical exploitation и все чаще злоупотребляют:

- legitimate access methods;
- engineering tools;
- commercial operating systems;
- native industrial protocols.

Во многих facilities OT networks изменяются реже, чем enterprise networks, поэтому communications более predictable. Эта predictability помогает выявлять:

- abnormal behavior;
- lateral movement;
- pre-positioning activity.

Но только если:

- internal OT network monitored;
- defenders понимают normal industrial communications.

Stable OT communication patterns делают даже basic network monitoring ценным. Baseline normal industrial communications — одна из наиболее эффективных detection investments.

Ключевой вопрос уже не в том, возможен ли high-impact OT incident, а в том, будет ли он обнаружен и понят достаточно рано, чтобы сохранить operational control до того, как adversary достигнет systems, способных влиять на process.

# VERIFY AND TRIAGE ДЛЯ OT

Verify and Triage — особенно важная часть DAIR для OT.

Responders сначала должны определить:

- является ли event реальной OT threat;
- активна ли она;
- может ли она повлиять на control system operations.

Например, malware на Windows-based OT asset может быть неспособен:

- установить C2;
- выполнить lateral movement;
- взаимодействовать с control systems.

До disruptive response actions нужно собрать engineering context.

DAIR предлагает сначала подтвердить, что activity действительно означает compromise OT systems.

Сам факт malware presence не всегда означает, что system нужно немедленно отключать. Malware может находиться в contained или non-functional state.

Verify/Triage должны выполняться:

- совместно с engineering personnel;
- либо responders, понимающими control system architecture и process context.

Это особенно важно для alerts от tools, которые не понимают:

- process state;
- controller logic;
- operational dependencies.

Например EDR.

В IT containment часто выполняется немедленно. В OT aggressive containment без verification может destabilize operations.

Примеры:

- isolation power substation может лишить operator visibility breaker status и load conditions;
- blocking communications к pipeline pump station controller может нарушить pressure balancing;
- isolation SCADA server/HMI в water treatment facility может убрать visibility chemical dosing, pump operations или reservoir levels.

В OT действие по unverified alert может создать больший operational risk, чем сама suspected threat.

Поэтому mature facility перед containment:

1. собирает available forensic evidence;
2. быстро проверяет current process state;
3. оценивает operational impact вместе с engineering/operations;
4. определяет, можно ли стабилизировать system или перевести его в controlled condition.

# CASE: OPERATOR VISIBILITY КАК ПОСЛЕДНЯЯ ЛИНИЯ ЗАЩИТЫ

5 февраля 2021 года operator Oldsmar water treatment plant во Florida увидел движение mouse cursor на HMI без собственного input.[4]

Remote session через TeamViewer изменила sodium hydroxide setpoint:

- normal: 100 ppm;
- malicious: 11,100 ppm;
- увеличение в 111 раз.

При достижении distribution system для 15,000 residents последствия могли включать серьезные physical injuries.

### Рисунок 197. Inside a Water Treatment Plant

THIRD_PARTY_REVIEW_REQUIRED — внешний визуальный материал не воспроизводится.

Operator увидел manipulation в real time, быстро вернул setpoint и завершил remote session.

Investigation выявил systemic failures:

- end-of-life OS;
- один shared password для remote access;
- отсутствие firewall;
- отсутствие automated alerting;
- отсутствие endpoint security.

Detection полностью зависел от human observation HMI.

Remote session использовал legitimate pathway и valid credentials, поэтому на network level выглядел authorized. Malware не использовался.[5]

В Oldsmar detection возник не из security tooling, а из process awareness.

Operator понимал normal process behavior и распознал unauthorized change.

Без operator in the loop не было:

- automated safety interlock;
- alerting;
- firewall.

Весь Verify/Triage фактически свелся к одному human judgment moment.

# Living-off-the-Land в Modern OT Attacks

Modern OT attacks все чаще используют trusted tools и existing access paths.[6]

Поэтому может не быть:

- clear intrusion moment;
- malware alert;
- obvious IOC.

Adversaries могут использовать:

- valid credentials;
- approved engineering software;
- standard industrial protocols.

Ключевая задача responders — определить, когда legitimate tool или hardware используется против control system с malicious intent.

# Traditional vs New Forensic Areas

Locard’s Exchange Principle утверждает, что каждое взаимодействие оставляет следы.[7]

В OT evidence может находиться не только в traditional OS/logs, но и в:

- controller memory;
- project files;
- relay configurations;
- engineering workstations;
- historians;
- OT network traffic.

Особенно важны:

- engineering application logs;
- project files;
- controller memory;
- HMI actions;
- remote access systems;
- packet captures.

Packet captures — ключевой forensic и early threat-detection data source.

Во время Verify/Triage OT systems следует считать primary evidence sources, а не дополнением к enterprise logs.

# Common OT Incident Data Sources

## Таблица 59. Распространенные OT Evidence Sources

| Evidence source | Example systems/data | Что показывает |
|---|---|---|
| Engineering Workstations | Engineering application logs, PLC tools, configuration logs, project files | Logic downloads, configuration changes, firmware updates, engineering activity |
| PLCs | Controller memory, ladder logic changes, firmware | Unauthorized logic changes, altered setpoints, modified parameters, direct process manipulation |
| Industrial Network Traffic | SPAN/TAP captures, protocol-aware monitoring | Lateral movement, abnormal commands, write operations, remote engineering sessions |
| HMIs | HMI logs, operator commands, alarm acknowledgements, setpoint changes | Operator/attacker actions affecting physical process |
| Historians | Time-series data, trends, production metrics | Process anomalies, timing, correlation cyber activity ↔ process behavior |
| Remote Access Systems | VPN logs, jump hosts, vendor access platforms | External pathways into OT and possible entry points |
| Authentication Services | OT Active Directory logs, identity providers | Credential use, account compromise, movement between IT and OT |

Даже если supervisory/engineering systems работают на Windows/Linux, investigation не должен на них заканчиваться.

Многие industrial devices имеют limited/no logging.

Поэтому incident reconstruction требует комбинации:

- engineering knowledge;
- network analysis;
- configuration validation.

В OT operational impact часто подтверждается только после проверки:

- controller logic;
- runtime values.

Unauthorized logic/setpoint changes означают verified operational incident.

Controller integrity verification — core triage activity. Пока logic не trusted, true scope и impact остаются uncertain.

# SCOPE

OT scoping отвечает на вопрос:

какие control zones, industrial assets и physical processes могли подвергнуться adversary interaction?

Главный критерий — достигла ли activity systems, способных влиять на:

- control logic;
- safety functions;
- engineering workflows.

Если suspicious activity обнаружена на engineering workstation, программирующей PLC, нужно проверить:

- осталась ли activity только на workstation;
- были ли communications с PLC;
- были ли logic downloads;
- были ли configuration changes;
- имеет ли workstation programming access к другим controllers, production cells или facilities.

Одна workstation может управлять несколькими production lines, поэтому blast radius может быть большим.

Как и в IT, scoping включает:

- initial access;
- credential abuse;
- trust relationships.

Но OT особенно фокусируется на crossing architectural boundaries между IT-adjacent systems и control layer.

Многие PLC, RTU, relays и embedded devices не поддерживают endpoint agents.

Поэтому network visibility часто является основным источником scoping evidence.

Industrial communications позволяют определить:

- кто общался с controllers;
- были ли write operations;
- выполнялись ли engineering workflows;
- использовались ли native OT protocols для issuing commands.

Где endpoint telemetry невозможен, network traffic и industrial protocol analysis часто являются единственными reliable sources.

Scoping строится вокруг monitoring key collection points:

- PLC;
- HMI;
- historian;
- engineering workstation.

Responders используют:

## Firewall/Security Control Logs

Показывают, инициировал ли compromised system connections в control zones или PLC subnets по EtherNet/IP, Modbus, PROFINET.

## Packet Capture / Flow Logs / Protocol Analysis

Позволяют обнаружить:

- write commands;
- program downloads;
- configuration changes;
- abnormal session patterns.

## Engineering Validation

Engineers сравнивают running logic с known-good baseline project files и проверяют:

- unauthorized changes;
- firmware updates;
- configuration modifications.

Так определяется, осталась ли activity на supervisory systems или дошла до control layer.

# CONTAINMENT

После подтверждения реальной threat containment должен учитывать:

- control network architecture;
- operational role affected assets;
- consequences of disrupting communication;
- safety-critical functions.

Вместо aggressive IT-style isolation OT containment стремится:

- ограничить adversary access;
- сохранить operator visibility;
- сохранить process stability;
- сохранить safety functions.

# Island Mode

Один из legitimate defensive options — OT cyber-safe state, manual operations или island mode.[8]

В этом состоянии OT network намеренно изолируется от:

- corporate IT;
- internet;
- vendor remote access.

Industrial process продолжает работать под local control.

Island mode дает responders время:

- investigate;
- validate system integrity;
- определить safe remediation.

В зависимости от sector process может работать так:

- часы;
- дни;
- недели.

Также возможен controlled safe shutdown.

Island mode нужно заранее:

- plan;
- test;
- exercise с engineering/operations.

Непроверенный переход в island mode сам создает operational risk.

# ERADICATE

OT eradication — controlled removal adversary persistence без destabilization control systems.

Цель:

- убрать adversary access;
- сохранить stable plant operation.

Credential-based persistence на Windows systems может затрагивать:

- engineering workstations;
- jump hosts;
- historians;
- domain infrastructure.

Eradication включает:

- credential resets;
- privilege reduction;
- account restrictions;
- authentication changes.

Все это должно учитывать dependencies:

- historian collection;
- OT patching;
- engineering software;
- HMI functions.

OT-specific persistence также включает:

- unauthorized engineering software access;
- modified controller logic;
- retained remote access pathways;
- trusted relationships между IT и OT zones.
