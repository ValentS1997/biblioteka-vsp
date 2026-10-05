# Шпаргалка: Chapter 11 — Scope Activity

## Core objective

```text
verified incident
      ↓
identify IOCs
      ↓
search broadly
      ↓
reconstruct timeline
      ↓
define breadth/depth
      ↓
handoff to response actions
```

## Fundamental questions

- single system or widespread?
- what is compromised?
- what is unaffected?
- when did access begin?
- what data was accessed/exfiltrated?
- what persistence exists?
- what alternate vectors exist?

## IOC classes

### Technical
- files/hash/path;
- IP/domain/URL;
- process/service;
- registry/config;
- account.

### Behavioral
- timing patterns;
- data movement;
- lateral movement.

## Scoping methodologies

### Enterprise-wide hunting
Search across:
- SIEM;
- EDR;
- log aggregation;
- inventory;
- network;
- custom scripts;
- threat-hunting platforms.

### Progressive scoping
```text
critical assets
    ↓
connected/related systems
    ↓
environment-wide sweep
```

## Timeline ownership

Scope should maintain:
- initial compromise;
- patient zero;
- attacker movement;
- persistence;
- sensitive-data access;
- exfiltration.

## Visibility gaps

Watch for:
- BYOD;
- shadow IT;
- legacy;
- IoT;
- ICS;
- ephemeral cloud;
- limited retention.

Alternative evidence:
- flow data;
- authentication logs;
- adjacent-system logs;
- cloud audit logs.

## Anti-forensics

| Technique | Counter |
|---|---|
| log deletion | gaps / alternate logs / event-ID anomalies |
| log flooding/replay | volume baseline / cross-source correlation |
| timestomping | MFT/backups/network timestamps |
| encryption/obfuscation | behavioral/memory analysis |
| living off the land | command line + context + baseline |

## Cloud-specific

Include:
- audit logs;
- image history;
- registries;
- IaC;
- identity activity;
- short-lived resources.

## Handoff artifacts

Downstream teams should receive:
- scoped-system list;
- canonical IOC inventory;
- canonical attack timeline;
- visibility gaps;
- unresolved questions.

## Main takeaway

```text
one IOC
  ↓
pivot
  ↓
search related systems
  ↓
expand timeline
  ↓
repeat until boundaries stabilize
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

