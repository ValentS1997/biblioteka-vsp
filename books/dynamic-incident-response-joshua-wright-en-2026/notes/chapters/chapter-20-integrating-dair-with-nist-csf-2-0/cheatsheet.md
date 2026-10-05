# Шпаргалка: Chapter 20 — DAIR + NIST CSF 2.0

## Core mapping

| CSF 2.0 | DAIR |
|---|---|
| Govern / Identify | Decision Maker coordination |
| Protect | Prepare |
| Detect | Detect + Verify + Triage |
| Respond | Scope + Contain + Eradicate + Recover |
| Recover | Recover + Debrief |

## Compliance requires

- documented capabilities;
- demonstrated effectiveness;
- metrics;
- continuous improvement.

## Strong evidence

### Prepare
- plans;
- playbooks;
- contact lists;
- training records.

### Detect / Verify / Triage
- alerts;
- dashboards;
- threat intel;
- triage decisions;
- declarations;
- false-positive records.

### Response Actions Loop
- scope;
- containment rationale;
- eradication records;
- recovery validation;
- iteration history.

### Debrief
- lessons learned;
- RCA;
- recommendations;
- implementation tracking.

### Decision Maker
- consultation;
- guidance;
- business impact;
- risk rationale.

## Iteration is not failure

```text
iteration count
+ trigger
+ decision rationale
+ extra remediation
=
evidence of adaptive response
```

## Govern categories emphasized

- GV.OC
- GV.RM
- GV.RR
- GV.PO
- GV.SC

## Audit rule

Document:
- action;
- owner;
- timestamp;
- rationale;
- evidence;
- outcome.

## Tooling

Incident platform should support:
- iterative states;
- Decision Maker fields;
- evidence links;
- CSF/DAIR tags;
- retention.

## Main takeaway

```text
good IR documentation
→ compliance artifacts
→ control evidence
→ easier audit
```
