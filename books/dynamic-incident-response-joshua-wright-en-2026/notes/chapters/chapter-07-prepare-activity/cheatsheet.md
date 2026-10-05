# Шпаргалка: Chapter 7 — Prepare Activity

## Three objectives

```text
Prepare
├─ Organizational readiness
├─ IRT capability
└─ Proactive prevention & detection
```

## 1. Organizational readiness

Checklist:

- policy;
- incident response plan;
- playbooks;
- management sponsorship;
- risk/severity model;
- communication plan;
- backup communication channel;
- contacts;
- reporting SLA;
- Emergency Communication Plan;
- regulatory notification map;
- external reporting channel;
- incident tracking platform;
- cyber-insurance constraints.

## 2. IRT capability

Checklist:

- trained personnel;
- primary + backup roles;
- RACI;
- decision authority matrix;
- cross-functional relationships;
- backups/recovery knowledge;
- forensic workstations;
- evidence collection tools;
- analysis tools;
- evidence storage;
- jump bag/go kit;
- emergency access;
- vendor/cloud escalation paths;
- tabletop exercises;
- drills.

## 3. Proactive prevention & detection

Checklist:

- CTI capability;
- STIX/structured intelligence;
- CTI platform;
- patch/config/inventory process;
- supply-chain + EOL awareness;
- hardening;
- EDR;
- supplemental endpoint telemetry;
- network monitoring;
- detection engineering;
- threat hunting;
- asset inventory;
- ASM;
- adversary simulation;
- vulnerability prioritization;
- logging and retention.

## Critical operational rules

### Communication backup

```text
primary chat
   ↓ compromised/unavailable
backup chat with SAME directory
   ↓
not a real backup
```

Backup communication should use independent authentication.

### Access

Break-glass accounts:
- secure storage;
- alert on use;
- multi-person authorization where needed;
- periodic testing.

### Asset visibility

```text
unknown asset
    ↓
missing inventory
    ↓
missing incident scope
```

### Logging

Not all logs deserve SIEM cost.

Use:
- active-detection logs → SIEM/hot storage;
- compliance-only logs → lower-cost archive.

### Metrics

Preparation value can be demonstrated through:
- MTTD reduction;
- exercise containment time;
- coordination quality;
- coverage;
- successful drills;
- readiness improvements.

## Preparation failure modes

| Challenge | Effect |
|---|---|
| Resource constraints | prep work gets displaced |
| Readiness erosion | skills decay |
| Documentation drift | plans no longer match reality |
| Knowledge loss | key context leaves with staff |
| Value demonstration | funding becomes difficult |

## Main takeaway

```text
people
+ authority
+ communications
+ access
+ tooling
+ telemetry
+ inventory
+ practice
= response readiness
```
## v1.6 compatibility contract

### Symptom / problem framing

See the chapter-specific framing above. If the chapter is conceptual rather than diagnostic, this field is `[Not applicable]` as a troubleshooting symptom.

### Baseline / context

Use only the source-grounded chapter context documented above.

### Read-only checks

See `commands.md` for source-confirmed checks/tools. If the chapter provides no operational checks, this field is `[Not applicable]`.

### Interpretation

Use the source-grounded interpretation and chapter logic documented above.

### Next action

Follow the chapter-specific source-grounded flow above. Unsupported next actions remain `[Needs confirmation]`.

### Modifying action

See `commands.md` for source-confirmed modifying actions. If none are supplied by the chapter, this field is `[Not applicable]`.

### Verification / acceptance checks

Use the source-supported verification/acceptance criteria in this chapter and `commands.md`. If no modifying action exists, this field is `[Not applicable]`.

### Rollback

Use source-supported rollback only. If the source does not provide rollback, mark it `[Needs confirmation]`.

