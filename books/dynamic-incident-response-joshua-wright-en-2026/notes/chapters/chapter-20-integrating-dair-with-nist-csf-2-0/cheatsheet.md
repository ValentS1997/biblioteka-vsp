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

