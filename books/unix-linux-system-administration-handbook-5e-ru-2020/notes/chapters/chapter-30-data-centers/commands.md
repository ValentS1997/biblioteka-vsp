# Команды и операционные проверки главы 30

Глава 30 практически не содержит shell-команд. Не добавляйте Linux/Unix CLI из других глав только ради заполнения файла.

Ниже перечислены source-supported расчёты, измерения и physical operations. Формулы не являются shell-командами.

## Read-only calculations / measurements

| Команда / расчёт | Назначение | Что проверить | Тип |
|---|---|---|---|
| PUE = total facility power / IT equipment power | Оценка facility energy overhead | measured facility and IT power use | read-only |
| kVA ≈ kW / 0.85 | Chapter approximation for power planning | real power factor may differ | read-only |
| BTUH = watts × 3.412 | Перевести electrical load в heat load | measured/estimated watts | read-only |
| cooling tons = BTUH / 12000 | Оценить cooling capacity | total thermal load | read-only |
| direct rack/device power measurement | Capacity and cooling planning | actual draw, not only nameplate maximum | read-only |
| infrared temperature measurement | Check hot/cold aisle behavior | intake/exhaust temperature pattern | read-only |
| environmental sensors | Continuous temperature/noise/power monitoring | alert delivery and abnormal trends | read-only |

### Interpretation boundaries

- Chapter formulas are planning approximations.
- Real electrical/HVAC design requires site-specific engineering: [Needs confirmation].
- Chapter-era PUE, temperature, humidity and rack-density examples are not universal current standards.

## Power redundancy operations

### UPS / generator test

Purpose:
- verify backup-power chain actually works.

Type:
- workload-generating / potentially state-affecting physical test.

Chapter recommendation:
- test backup-power components every six months;
- perform maintenance at least annually.

Risks:
- a poorly controlled test can interrupt production power;
- generator/ATS/UPS behavior may differ from assumptions.

Preconditions:
- approved maintenance procedure;
- confirmed load/coverage;
- communication with affected operators;
- rollback/fallback power path identified.

Verification:
- expected transfer occurs;
- monitored systems remain within defined power state;
- alarms/telemetry arrive;
- generator/UPS returns to normal condition.

Rollback:
- restore normal utility/power topology;
- exact facility switching procedure: [Needs confirmation].

## Remote power control

Chapter describes remotely controlled power distribution/switching equipment.

Type:
- state-changing.

Effect:
- can remove/restore power to attached equipment.

Precondition:
- verify exact rack/outlet/device;
- confirm maintenance authorization;
- confirm service impact.

Verification:
- target device reaches intended power state;
- unrelated equipment remains unaffected.

Rollback:
- restore prior power state if safe;
- exact command/API/button sequence: [Needs confirmation].

## Rack power planning

Source-supported planning workflow:

~~~text
inventory equipment
→ estimate/measure watts
→ classify rack power level
→ group similar rack loads
→ align electrical distribution
→ align cooling capacity
→ verify by measurement
~~~

The chapter's example rack classes include values from 6 kW to 40 kW/rack. Use as chapter examples only.

## Cooling-load calculation

Chapter workflow:

~~~text
building envelope heat
+ electronics
+ lighting
+ people
= total BTUH
→ convert to cooling tons
→ compare with HVAC estimate
~~~

Chapter worked example:
- electronics are calculated from measured/estimated watts;
- watts use 3.412 BTUH/W;
- total BTUH is divided by 12000 BTUH/ton;
- example applies a 50% allowance for error/future growth.

Do not apply the 50% factor as a universal engineering rule.

## Hot/cold aisle verification

Read-only observation:
- server intakes face cold aisle;
- exhausts face hot aisle;
- adjacent racks do not feed hot exhaust into another intake;
- temperature measurements show intended separation.

Modifying action:
- reorient racks/equipment, perforated tiles or cooling layout.

Type:
- state-changing physical change.

Risk:
- airflow disruption can cause rapid thermal problems.

Verification:
- remeasure intake/exhaust temperatures;
- confirm alarms remain normal;
- verify no blocked airflow.

Rollback:
- restore previous physical layout if safe;
- exact site-specific procedure: [Needs confirmation].

## Environmental monitoring

Chapter-supported signals:
- temperature;
- noise;
- power consumption.

Goal:
- detect environmental failure when facility is unattended.

Verification:
- abnormal test condition produces expected remote notification.

State-changing alert-test method:
- [Needs confirmation]; do not create unsafe heat/power conditions merely to test an alarm.

## Physical access changes

Examples:
- granting facility access;
- granting rack/cage access;
- changing badge/MFA authorization.

Type:
- state-changing.

Precondition:
- identity verified;
- authorization verified;
- scope/location verified.

Verification:
- authorized access works;
- unauthorized access remains blocked;
- access is auditable.

Rollback:
- revoke the granted access;
- exact access-control system procedure: [Needs confirmation].

## No source-supported shell CLI

The chapter does not provide exact commands for:
- UPS management;
- generator control;
- managed PDU switching;
- HVAC control;
- environmental sensor configuration;
- badge/access-control systems.

Do not invent vendor CLI/API operations.
