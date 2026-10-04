# Chapter 19 — Segment 01

Source RAG: `p0613:c01`–`p0618:c01`

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
