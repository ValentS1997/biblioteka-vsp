---
book_id: dynamic-incident-response-joshua-wright-en-2026
chapter_number: 19
source_title: "Incident Response for Operational Technology"
source_pdf_page_range: "613-636"
rag_chunk_range:
  first: "dynamic-incident-response-joshua-wright-en-2026:p0613:c01"
  last: "dynamic-incident-response-joshua-wright-en-2026:p0636:c01"
translation_status: "ACCEPTED"
license_notice: "Неофициальный русский перевод / unofficial Russian translation; original work CC BY 4.0. См. ../ATTRIBUTION.md."
third_party_review_policy: "Third-party figures, quoted report text, screenshots, and external materials remain fail-closed where marked."
translation_notes:
  - "Canonical English RAG is source of truth."
  - "Assembled from full-fidelity source-range segments."
  - "OT safety and engineering context preserved as primary response constraints."
  - "Commands, identifiers, metrics, and references are preserved where represented."
---

# Глава 19. Реагирование на инциденты в операционных технологиях

# РАЗЛИЧИЯ МЕЖДУ IT И OT

Когда решения по кибербезопасности могут напрямую влиять на физические процессы, оборудование и безопасность людей, реагирование инженеров и операторов должно учитывать особенности промышленной среды. На протяжении многих лет conventional incident response, заимствованный из IT, адаптировали к Operational Technology (OT), однако различия в миссии, controls, skill sets и risk tolerance требуют более осторожного подхода, чем допускают типовые enterprise-модели.

Эта глава рассматривает применение incident response в OT в рамках DAIR. Организациям следует использовать соответствующие разделы Part 2 как основную методологию, дополняя ее OT-specific considerations.

IT и OT security преследуют общую цель — снижение cyber risk и реагирование на инциденты. Однако среды принципиально различаются по:

- угрозам;
- последствиям;
- типам атак;
- задачам.

OT systems взаимодействуют напрямую с физическими процессами, поэтому cybersecurity events способны влиять на:

- поведение оборудования;
- работу объектов;
- critical infrastructure.

OT incident response должен учитывать engineering workflows, длительный asset lifecycle, vendor dependencies и control system architecture.

OT IR нельзя рассматривать как расширение enterprise response. Он должен выполняться с engineering context и operational awareness. Это требует понимания того, как работают конкретные assets и процессы, причем это различается между секторами critical infrastructure.

В этой главе рассматриваются:

- почему response actions должны учитывать control-system context;
- почему safety важнее confidentiality;
- какие engineering skills нужны responders;
- как lifecycle и vendor support ограничивают remediation;
- чем industrial architecture и protocols отличаются от enterprise;
- почему OT имеет низкую tolerance к false positives;
- как cyber incidents переходят в physical consequences.

Термин Industrial Control Systems (ICS) традиционно описывает системы мониторинга и управления физическими процессами, включая:

- SCADA;
- DCS;
- PLC.

Operational Technology (OT) — более широкий термин, включающий ICS и все hardware/software, которое monitor или control физические устройства, процессы и инфраструктуру. В этой главе используется OT, кроме ссылок на frameworks, сохраняющие термин ICS.

# Выполнение Incident Response в OT Environments

Критическое различие: действия, обычные для enterprise environments, могут создать неприемлемый operational и safety risk в OT.

К таким действиям относятся:

- aggressive isolation;
- automated blocking;
- immediate host rebuild.

Эффективный OT IR требует сначала оценить, как response action повлияет на:

- control system behavior;
- operator visibility;
- возможность поддерживать safe operations.

В IT threat часто быстро сдерживается через isolation, disable account, communication blocking или reimage. В OT необдуманное действие по непроверенному событию может:

- нарушить operations;
- лишить операторов visibility;
- нарушить process control;
- создать больший ущерб, чем сама угроза.

Поэтому OT events следует сначала verify и triage с участием engineering staff.

# Safety как основная миссия OT Security

OT systems управляют physical processes в реальном времени. Cybersecurity decision может влиять на:

- valves;
- temperature;
- pressure;
- flow;
- machinery;
- infrastructure.

Приоритеты:

1. защита людей;
2. сохранение контроля над процессом;
3. integrity control logic;
4. reliability safety functions;
5. stable operations.

Response decisions оцениваются не только по cybersecurity value, но и по impact на physical process.

# Требуемые Skill Sets для OT Defenders и Responders

Engineering understanding — часть OT IR role.

Responders должны понимать:

- типы industrial assets;
- как они работают;
- как ими может злоупотребить attacker;
- как industrial protocols используются при normal operations, maintenance и production workflows.

Это позволяет отличать legitimate activity от malicious use:

- trusted engineering tools;
- asset credentials;
- industrial communications.

Многие серьезные OT attacks не требуют:

- malware;
- known vulnerability;
- zero-day.

Они используют:

- valid credentials;
- approved engineering software;
- authorized remote access;
- native industrial protocols.

Без engineering context malicious activity может выглядеть нормальной.

# Vendor Support и Industrial System Lifecycle Constraints

Industrial systems часто работают десятилетиями.

OT assets могут эксплуатироваться 10 лет и дольше. Patch или upgrade ограничиваются:

- operational risk;
- vendor support;
- maintenance windows;
- certification;
- regulatory requirements.

Во время инцидента не всегда безопасно немедленно patch, reboot или replace system. Иногда monitored/contained state безопаснее, чем forced disruption.

Особенно это важно для:

- oil and gas;
- electric power;
- water;
- heavy manufacturing.

Shutdown может занимать часы или дни, а restart — требовать значительных engineering усилий. Containment и remediation необходимо поэтапно согласовывать с engineering и operations. Vendor support особенно важен при recovery.

# Различия Industrial System Design и Network Architecture

OT networks часто строятся по Purdue-like architecture и используют industrial protocols:

- Modbus;
- DNP3;
- EtherNet/IP;
- PROFINET;
- ICCP.[1]

Эти protocols обеспечивают deterministic control и supervisory functions, напрямую влияющие на physical world.

Responders должны понимать роль:

- HMI;
- engineering workstation;
- historian;
- SCADA server;
- PLC;
- RTU;
- protection relay.

# SIDEBAR: PURDUE MODEL ДЛЯ INDUSTRIAL NETWORK ARCHITECTURE

Purdue Enterprise Reference Architecture (PERA), обычно называемая Purdue model, — наиболее распространенная модель сегментации OT network.

### Рисунок 191. Современная Purdue Model

THIRD_PARTY_REVIEW_REQUIRED — схема не воспроизводится дословно.

Уровни:

- Level 0 — физический процесс: sensors, actuators, controlled equipment;
- Level 1 — basic control devices: PLC, RTU;
- Level 2 — supervisory systems: HMI, local SCADA;
- Level 3 — site operations и manufacturing management: historians, engineering workstations, domain services;
- Level 3.5 — industrial DMZ, разделяющий IT и OT;
- Levels 4–5 — enterprise IT и internet-facing services.

Purdue model используется в ISA/IEC 62443 и ISA-95. Для IR она помогает определить:

- где произошла attacker activity;
- какие trust boundaries были пересечены;
- какие systems способны напрямую влиять на physical process.

# Security Control Design и Operational Risk Tolerance

OT environments имеют крайне низкую tolerance к false positives.

В enterprise ошибочная isolation host обычно создает inconvenience. В OT она может:

- нарушить control loop;
- ухудшить process visibility;
- повлиять на product quality;
- нарушить protective functions.

Поэтому OT предпочитает:

- passive monitoring;
- engineering-informed validation;
- tightly coordinated response actions.

### Рисунок 192. Взаимосвязанные области OT Constraints и Considerations

THIRD_PARTY_REVIEW_REQUIRED — внешний визуальный материал не воспроизводится.

Шесть взаимосвязанных областей:

- safety;
- skill sets;
- system design;
- support;
- cybersecurity controls;
- security incident response.

Containment decision влияет сразу на все эти области.

# SIDEBAR: ПОЧЕМУ СТАНДАРТНЫЙ IT CONTAINMENT МОЖЕТ БЫТЬ ОПАСЕН В OT

Rapid isolation, aggressive blocking и full rebuild могут создать operational risk.

Без engineering triage:

- isolation может лишить operator visibility;
- automated blocking может нарушить time-sensitive control communications.

IT response action способен причинить больше ущерба, чем threat. Containment и eradication должны быть validated с engineering и operations.

# CASE: КОГДА IT CONTAINMENT САМ СОЗДАЕТ OT INCIDENT

На refinery OT monitoring обнаружил аномальные outbound connections от недавно развернутого Windows-based HMI к нескольким internet C2 servers.

Причина быстро выяснилась: transient USB device, ранее использовавшийся вне facility, содержал commodity IT malware. Это была не targeted OT attack, а обычный Windows malware, попавший на OT asset.

Архитектура была сегментирована:

- HMI не имел direct internet access;
- upstream controls блокировали lateral movement;
- malware не мог связаться с C2;
- malware не взаимодействовал с control systems.

Engineering team подтвердила, что process stable, а HMI функционирует нормально.

План response:

- усилить monitoring;
- sinkhole attempted C2 traffic;
- удалить malware в следующем scheduled engineering maintenance window.

До выполнения плана onsite IT technician увидел endpoint protection alert и без coordination немедленно отключил HMI от сети.

С точки зрения IT это выглядело как textbook containment. В refinery это создало operational incident.

Disconnected HMI был primary operator interface. Его отключение сразу лишило operators:

- visibility;
- safety-related view;
- control functions.

Malware не влиял на operations, а containment action повлиял немедленно.

Operators пришлось выйти на plant floor в PPE для восстановления process visibility и manual control. Engineering и operations стабилизировали ситуацию и безопасно вернули HMI в сеть.

Вывод: aggressive containment без engineering context может быть опаснее threat. OT response должен учитывать process knowledge, network architecture и coordination с engineering.

# Потенциальные последствия IT и OT Incidents

## Таблица 57. Сравнение последствий инцидентов: IT и OT

| IT incident impact potential | OT incident impact potential |
|---|---|
| Недоступность business applications, обычно локальная для бизнеса/организации | Недоступность critical infrastructure, возможны региональные disruption или outages |
| Corruption digital data | Потеря контроля над physical process или его manipulation |
| Digital data loss | Personnel safety, loss of life |

Различия в potential impact определяют весь OT incident response lifecycle.

В enterprise rapid containment обычно затрагивает availability или data integrity.

В industrial environment response decision должен учитывать:

- process disruption;
- infrastructure outage;
- equipment damage;
- harm to people.

Поэтому OT IR должен опираться на engineering context, controlled operations и disciplined decision-making.

# Цель OT Incident Response

Из-за различий в mission, controls и ограниченного logging OT IR — это не только поиск malware или восстановление traditional OS на OT assets.

Главная цель — сохранить safe и reliable operation physical process, одновременно позволяя принимать informed decisions во время adverse conditions и снижать safety impact.

Industrial incidents часто используют living-off-the-land:

- уже установленное engineering software;
- valid credentials;
- trusted access paths.

Если adversary действует через legitimate tools и protocols, response нельзя ограничивать удалением malware или persistence. Необходимо остановить unauthorized use trusted capabilities во всей control environment.

Цель — не просто остановить attack как можно быстрее, а сохранить:

- control;
- visibility;
- stability;

пока incident исследуется и устраняется, не создавая дополнительного safety impact.

# Распространенные OT Assets

OT environment включает purpose-built systems для monitoring, control и protection physical processes.

Assets распределены по нескольким слоям architecture.

Можно условно разделить их на:

- non-traditional embedded OT assets;
- traditional OS-based OT assets.

# Non-Traditional Operating System OT Assets

Большинство OT assets — embedded industrial devices для deterministic control.

Основные типы:

## PLC

Programmable Logic Controllers управляют field equipment в panels, skids и process units.

### Рисунок 193. PLC с I/O Modules

THIRD_PARTY_REVIEW_REQUIRED — внешний визуальный материал не воспроизводится.

## DCS

Distributed Control Systems обеспечивают centralized control на крупных industrial sites, например refineries и LNG plants.

## RTU

Remote Terminal Units обеспечивают telemetry и control geographically distributed assets:

- pipelines;
- compressor stations;
- remote well sites.

## Protection Relays

Protection relays защищают:

- substations;
- pumps;
- compressors;
- feeders.

### Рисунок 194. Protection Control Relay

THIRD_PARTY_REVIEW_REQUIRED.

### Рисунок 195. Electric Power Substation Yard

THIRD_PARTY_REVIEW_REQUIRED.

## VFD

Variable Frequency Drives регулируют motor speed.

## SIS и Emergency Shutdown

Safety Instrumented Systems и emergency shutdown systems образуют independent protective layers и должны переводить process в safe state при hazardous conditions.[2]

# Traditional Operating System-Based OT Assets

Некоторые OT systems используют Windows или Linux, особенно supervisory и engineering systems.

## HMI

Human-Machine Interface дает operators real-time visibility:

- alarms;
- trends;
- equipment status.

### Рисунок 196. Embedded Human Machine Interface Panel

THIRD_PARTY_REVIEW_REQUIRED.

## Engineering Workstation

Используется для:

- configuration;
- troubleshooting;
- programming PLC и других industrial devices.

## Historian

Data historian хранит time-series operational data:

- flow;
- pressure;
- temperature;
- production metrics.

Historians часто размещаются между IT и OT для reporting и analytics.

Windows-based systems часто являются high-value pivot points, поскольку соединяют administrative, engineering и operational functions. Но большая часть physical process контролируется embedded devices.

## Таблица 58. Распространенные OT Asset Types и IR Considerations

| Asset | Primary role | OT IR consideration |
|---|---|---|
| HMI (Windows) | Operator visibility/control, alarms, trends, start/stop, setpoints | Потеря view или manipulation влияет на operator decisions; activity может выглядеть legitimate без engineering context |
| Engineering Workstation (Windows) | PLC configuration/programming, logic upload/download, firmware and point changes | Compromise позволяет выполнять legitimate-looking changes approved tools по trusted paths |
| SCADA / Supervisory Servers | Centralized monitoring, alarms, supervisory coordination | High-value pivot; evidence может находиться в application logs и command history |
| Historian | Time-series process data для operations/reporting/analytics | Показывает process deviations, operator actions, event timing; common IT/OT bridge |
| PLC | Deterministic field control | Logic integrity и runtime values определяют operational impact |
| RTU | Telemetry/control remote assets | Часто связан с remote access; communications и command sequences помогают выявить misuse |
| Protection Relay | Electrical protection/fault response | Misconfiguration влияет на protective functions; для анализа может требоваться vendor tooling |
| VFD | Motor speed regulation | Изменения могут влиять на process stability и equipment behavior |
| SIS | Independent safety protection/shutdown | Safety-critical; response/recovery должны сохранять required functions |

IT/OT convergence привел в industrial environments:

- remote access services;
- identity systems;
- engineering endpoints.

Но большинство OT assets по-прежнему specialized devices с:

- limited logging;
- proprietary protocols;
- strict reliability requirements;
- отсутствием EDR support.

OT asset inventory должен различать:

- Windows/Linux-based HMIs, engineering workstations, historians;
- embedded PLCs, RTUs, relays, VFDs.

Для этих категорий требуются разные investigation techniques и evidence sources.

Traditional host-based telemetry показывает только часть картины. OT IR сильно зависит от:

- engineering knowledge;
- equipment logs;
- network visibility;
- OT protocol analysis;
- controller logic validation.

# Преимущества DAIR для OT Incident Response

Traditional models вроде PICERL долго применялись в IT и адаптировались для OT.

DAIR улучшает investigation flow за счет акцента на:

- verification;
- scoping;
- evidence analysis с engineering context.

В OT ранний Verify/Triage позволяет определить, представляет ли activity реальную operational threat, прежде чем выполнять действия, которые могут нарушить process или удалить critical visibility.

DAIR помогает:

- validate events;
- определить scope;
- спланировать response actions;
- сохранить operational control.

# SIDEBAR: FIGHTING THROUGH THE ATTACK

В OT immediate objective не всегда состоит в shutdown systems.

Иногда задача — продолжить controlled operation, пока:

- собирается evidence;
- подтверждается process condition;
- engineering/operations оценивают response options.

Это позволяет сохранить visibility/control и уменьшить риск того, что response сам вызовет instability.

# CASE: FIGHTING THROUGH THE ATTACK, ЧТОБЫ СОХРАНИТЬ POWER GENERATION

На hydroelectric power generation facility возник выбор:

- immediate shutdown;
- fight through the attack и сохранить stable grid operations.

Команды engineering, plant operations и physical security начали coordination.

Вместо disconnect compromised HMI был изолирован attacker access path на Level 3.5 IDMZ.

OT network отделили от IT, откуда исходила attack.

Это было deliberate engineering-informed containment:

- core plant control не зависел от IT/internet;
- после isolation perimeter remote session к HMI завершилась;
- operators сохранили visibility/control.

Operations продолжились через embedded HMI panels на dedicated control systems.

Такой containment позволил:

- сохранить power generation;
- провести forensic analysis;
- подготовить recovery.

# Распространенные типы OT Incidents

Ранее critical infrastructure incidents часто считались High-Impact, Low-Frequency (HILF).[3]

Из-за:

- increased connectivity;
- remote access;
- trusted administrative paths;
- engineering pathways

условия для high-impact events стали более распространенными.

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

Эти eradication actions требуют тесной coordination с engineering teams, чтобы:

- validate controller configurations;
- подтвердить known-good logic baselines;
- убедиться, что remediation не нарушает required control communications;
- сохранить safety-related functions.

# RECOVER

Recovery в OT — controlled restoration systems и industrial processes в known-good operational state при сохранении stable operations.

В IT recovery часто означает rebuild server и restore data. В OT дополнительно нужно подтвердить:

- control logic;
- process behavior;
- operator visibility;
- protective functions.

Recovery выполняется совместно:

- engineering;
- operations;
- cybersecurity.

Она может затрагивать несколько systems и facilities.

Recovery обычно начинается с supporting digital infrastructure:

- engineering workstations;
- historians;
- authentication services;
- patch servers;
- remote access systems.

Windows-based OT systems обычно rebuild из:

- trusted installation media;
- known-good system images;
- dedicated OT backup repositories.

Для HMI и engineering workstation необходимо:

- reinstall vendor software;
- restore project files;
- restore configuration parameters;
- reactivate licenses;
- validate USB license dongles;
- validate communication adapters;
- validate programming cables.

Embedded controllers требуют:

- reload validated logic/configuration;
- firmware verification;
- configuration validation against approved baselines;
- compare running logic с offline project files;
- checksum verification;
- I/O mapping validation;
- communication validation с HMI, historian и supervisory systems.

### Рисунок 198. Reloading Controller Logic from an Engineering Workstation

THIRD_PARTY_REVIEW_REQUIRED — внешний визуальный материал не воспроизводится.

Recovery распространяется и на physical plant.

Engineering/operations выполняют physical walkthrough и проверяют:

- pumps;
- valves;
- drives;
- motors;
- sensors;
- protective systems.

Затем facilities выполняют documented startup sequence:

1. gradually restore automation;
2. bring controllers online;
3. validate HMI visibility;
4. вернуть equipment/processes в operation в controlled order.

Vendor или system integrator может участвовать в validation:

- firmware;
- proprietary control logic;
- authoritative configurations.

OT recovery timeline определяется engineering validation requirements, а не скоростью IT restoration.

Controller с unverified logic опаснее delayed, но validated restoration.

Successful OT recovery определяется тем, можно ли доверять:

- control integrity;
- operator visibility;
- required protective functions.

Пример oil-and-gas processing facility:

1. engineering workstation rebuild из trusted image;
2. reinstall PLC/DCS engineering software;
3. restore project files из secure OT repository;
4. reactivate USB license dongles;
5. reconnect к controllers;
6. reload validated control logic;
7. verify firmware and logic checksums;
8. validate HMI/historian communications;
9. выполнить physical walkthrough;
10. проверить pumps, compressors, valves, pressure sensors, safety systems;
11. validate valve positions, pressure boundaries, emergency shutdown;
12. постепенно вернуть process в service.

Такой recovery может занимать от часов до дней.

# DEBRIEF

OT debrief — structured technical review того, как:

- engineering workflows;
- network architecture;
- trust relationships

повлияли на incident, response actions и operational decisions.

Цель — понять, как OT systems и dependencies сформировали:

- adversary access;
- способность организации реагировать.

В debrief должны участвовать:

- engineering leadership;
- control system specialists;
- plant operations;
- physical safety/security;
- cybersecurity teams.

Нужно оценить indicators в:

- engineering systems;
- controllers;
- network communications;
- supervisory infrastructure.

Особое внимание:

- vendor remote access;
- shared identity infrastructure;
- engineering workstations;
- jump hosts;
- historians;
- IT/OT architectural bridges.

# OT-Specific Debrief Questions

Кроме generic post-incident review следует задать вопросы, на которые могут ответить только engineering/operations.

## Cyber-Safe Position и Island Mode

- Рассматривался ли cyber-safe mode/manual operations/island mode?
- Если применялся — помог ли containment/scoping/eradication?
- Если нет — что помешало transition?

## Engineering System Exposure

- Были ли exposed engineering workstations?
- project repositories?
- configuration management systems?
- получил ли adversary доступ к PLC engineering tools?
- мог ли modify project files?

## Controller Integrity Verification

- Проверялась ли controller logic during recovery?
- Были ли baseline files available и trustworthy?
- можно ли было быстро подтвердить integrity через engineering tools/offline comparison?

## Protocol-Level Visibility

Была ли достаточная visibility по:

- Modbus;
- EtherNet/IP;
- DNP3;
- PROFINET?

Можно ли было определить unauthorized control commands или configuration changes?

## Operational Impact Awareness

- Как быстро responders поняли, затронут ли physical process?
- Было ли достаточно HMI/historian/alarm visibility?

## Backup Access and Validation

Были ли backups для:

- engineering workstation images;
- HMI;
- historians;

которые можно использовать для validation/recovery при compromise primary access?

## Architectural Trust Relationships

Какие решения позволили adversary access/lateral movement?

Примеры:

- shared Active Directory;
- vendor remote access pathways;
- flat Level 3 network;
- слабая IT/OT segmentation.

## Containment and Operational Risk Decisions

- Были ли containment actions delayed, modified или sequenced ради controlled operations?
- Был ли engineering context, чтобы понимать последствия isolation?

Ответы выявляют gaps, которые IT-focused debrief часто пропускает:

- engineering workflow weaknesses;
- protocol-monitoring blind spots;
- trust relationships.

# Engineering and Architecture Improvements

OT debrief должен приводить к actionable improvements:

- industrial protocol monitoring;
- detection engineering;
- refinement OT IR playbooks;
- containment sequencing;
- controller baseline management;
- configuration tracking;
- reduction unnecessary trust relationships;
- stronger segmentation IT/OT/remote access.

Lessons learned должны также использоваться в targeted OT tabletop exercises.

Реалистичные scenarios:

- loss of operator visibility;
- unauthorized engineering access;
- vendor compromise;
- controller logic manipulation;
- abuse trusted industrial protocols.

# THE FIVE ICS CYBERSECURITY CRITICAL CONTROLS

Эффективный OT IR требует одновременно:

- cybersecurity expertise;
- industrial engineering knowledge.

OT response находится на пересечении cyber defense и industrial engineering.

Успех зависит от collaboration:

- IT security;
- OT cybersecurity specialists;
- operators;
- engineers.

Five ICS Cybersecurity Critical Controls и ICS-specific response plan дают practical foundation для safety-focused и engineering-informed response.[9]

### Рисунок 199. The Five ICS Cybersecurity Critical Controls

THIRD_PARTY_REVIEW_REQUIRED — внешний визуальный материал не воспроизводится.

#1 ICS-Specific Incident Response

Первый и наиболее важный control — OT-specific incident response.

Он должен быть:

- operations-informed;
- engineered for control-system realities;
- safety-first;
- process-integrity focused;
- controlled-recovery oriented.

OT response plan должен предполагать, что attacker может напрямую target engineering systems, а response может происходить при active incident с сохранением operations.

Exercises должны моделировать:

- loss of view;
- logic manipulation;
- unauthorized remote access.

Без control-system-specific preparation response будет либо слишком aggressive, либо слишком slow.

#2 Defensible Control System Network Architecture

Второй control — defensible architecture.

Нужны:

- segmentation;
- clear trust boundaries;
- industrial DMZ;
- control traffic visibility;
- asset identification;
- log collection;
- deterministic communication enforcement.

В poorly segmented environment сложно:

- scope incident;
- trace lateral movement;
- assess blast radius.

Это ведет к overly broad или disruptive response actions.

#3 OT Network Visibility and Monitoring

Третий control — OT network visibility.

Поскольку многие OT assets не поддерживают endpoint agents, continuous protocol-aware monitoring становится primary forensic evidence source.

Visibility в industrial protocols позволяет:

- verify incidents;
- identify affected assets/processes;
- понять adversary interactions;
- отличать malicious activity от legitimate engineering behavior;
- уменьшать false positives;
- принимать safe response decisions.

#4 Secure Remote Access

Remote access — один из наиболее часто abused paths в OT.

Нужно четко знать:

- как реализован access;
- какие users/vendors authorized;
- к каким systems они могут подключаться.

Secure design использует:

- time-based controlled access;
- strong authentication;
- MFA where feasible;
- controlled jump hosts;
- segmentation;
- monitoring.

Во время incident remote access pathways часто становятся containment chokepoints.

#5 Risk-Based Vulnerability Management

В OT vulnerability management — не "patch everything".

Нужно понимать:

- какие vulnerabilities реально важны;
- какие systems можно safe update;
- где нужны compensating controls;
- где лучше monitoring;
- каковы operational safeguards;
- potential exploit paths.

Remediation может быть:

- immediate;
- deferred;
- monitored.

Главный критерий — response action не должен ухудшить safety/reliability.

Вместе пять controls создают repeatable и defensible OT IR capability, выравнивая security operations с engineering reality.

# Ссылки

[1] The Purdue Enterprise Reference Architecture (PERA), developed by Theodore J. Williams at Purdue University in the 1990s. See ISA-95 (Enterprise-Control System Integration) and ISA/IEC 62443 (Industrial Automation and Control Systems Security).

[2] IEC 61511, "Functional safety - Safety instrumented systems for the process industry sector," International Electrotechnical Commission, www.iec.ch/homepage.

[3] NERC, "High-Impact, Low-Frequency Event Risk to the North American Bulk Power System," June 2010, www.nerc.com/pa/CI/Resources/Documents/High-Impact_Low-Frequency_Event_Risk_to_the_North_American_Bulk_Power_System_-_2010.pdf

[4] CISA, "Compromise of U.S. Water Treatment Facility," Alert AA21-042A, February 2021, www.cisa.gov/news-events/cybersecurity-advisories/aa21-042a

[5] Miller, Ben, "Recommendations Following the Oldsmar Water Treatment Facility Cyber Attack," Dragos, Inc., February 2021, www.dragos.com/blog/industry-news/recommendations-following-the-oldsmar-water-treatment-facility-cyber-attack/

[6] CISA, NSA, FBI, and international partners, "People’s Republic of China State-Sponsored Cyber Actor Living off the Land to Evade Detection," Joint Cybersecurity Advisory, February 2024, www.cisa.gov/news-events/cybersecurity-advisories/aa24-038a

[7] Locard’s Exchange Principle, attributed to French forensic scientist Edmond Locard (1877–1966).

[8] The concept of manual operations or "island mode" during OT incidents is discussed in SANS, "The Five ICS Cybersecurity Critical Controls," and Dragos, "ICS/OT Cybersecurity Year in Review," www.dragos.com/year-in-review/

[9] SANS Institute, "The Five ICS Cybersecurity Critical Controls," www.sans.org/white-papers/five-ics-cybersecurity-critical-controls/
