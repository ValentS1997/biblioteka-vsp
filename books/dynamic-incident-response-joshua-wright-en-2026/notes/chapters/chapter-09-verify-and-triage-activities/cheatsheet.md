# Шпаргалка: Chapter 9 — Verify + Triage

## Core flow

```text
Detect
  ↓
Verify
  ├─ Continue
  ├─ Stop
  └─ Defer
  ↓
Initial Risk
  ↓
Triage with Decision Makers
  ↓
Response Actions
```

## Verify questions

- Is the incident real?
- What evidence supports compromise?
- What evidence argues against compromise?
- What data/time windows were checked?
- What evidence sources were unavailable?
- Is more information needed?

## Verification outcomes

### Continue
Incident real:
- escalate;
- engage broader IRT;
- move toward response actions.

### Stop
Incident not real:
- document why;
- classify closure;
- notify reporter/stakeholders;
- add benign source to local knowledge base when useful.

### Defer
Not enough information:
- request more evidence;
- wait for owner/vendor/reporting party;
- keep decision open.

## Documentation

Capture:
- incident ID;
- title;
- handler;
- summary;
- classification;
- evidence references.

Rule:
```text
if you are too busy to take notes,
you are moving too fast
```

## Initial risk

Typical classes:
- Low
- Medium
- High
- Critical

Consider:
- financial impact;
- operational impact;
- reputation;
- regulation;
- attacker capability;
- CTI relevance.

## CTI use

CTI helps with:
- EOI enrichment;
- attribution/context;
- related indicators;
- risk calibration.

But:

```text
no CTI hit ≠ no threat
```

## Proving a negative

A defensible "not compromised" conclusion should document:
- processes checked;
- persistence checked;
- filesystem;
- network;
- auth logs;
- memory/logs;
- time window;
- inaccessible evidence.

## Triage

Analyst:
- explains;
- contextualizes;
- recommends.

Decision maker:
- prioritizes;
- allocates resources;
- balances business/legal constraints.

## Third-party incidents

Never accept vendor numbers blindly.

Independently verify:
- affected records;
- access logs;
- auth events;
- egress;
- CASB/other telemetry;
- regulatory implications.

## Main takeaway

```text
Verify = is it real?
Triage = what should we do about it?
```
