# Chapter 19 — Segment 04

Source RAG: `p0631:c01`–`p0636:c01`

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

[1] Purdue Enterprise Reference Architecture (PERA); ISA-95; ISA/IEC 62443.

[2] IEC 61511, "Functional safety - Safety instrumented systems for the process industry sector," International Electrotechnical Commission.

[3] NERC, "High-Impact, Low-Frequency Event Risk to the North American Bulk Power System," June 2010.

[4] CISA, "Compromise of U.S. Water Treatment Facility," Alert AA21-042A, February 2021.

[5] Ben Miller, Dragos, "Recommendations Following the Oldsmar Water Treatment Facility Cyber Attack," February 2021.

[6] CISA, NSA, FBI and international partners, "People’s Republic of China State-Sponsored Cyber Actor Living off the Land to Evade Detection," February 2024.

[7] Locard’s Exchange Principle.

[8] SANS, "The Five ICS Cybersecurity Critical Controls"; Dragos, "ICS/OT Cybersecurity Year in Review."

[9] SANS Institute, "The Five ICS Cybersecurity Critical Controls."
