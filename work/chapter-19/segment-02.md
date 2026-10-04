# Chapter 19 — Segment 02

Source RAG: `p0619:c01`–`p0624:c01`

# Потенциальные последствия IT и OT Incidents

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
