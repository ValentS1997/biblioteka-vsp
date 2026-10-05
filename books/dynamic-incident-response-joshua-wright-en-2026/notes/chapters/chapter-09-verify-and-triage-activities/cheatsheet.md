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

