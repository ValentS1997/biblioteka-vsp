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
