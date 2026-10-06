# Шпаргалка: Chapter 6 — DAIR

## Core model

```text
Prepare
   ↓
Detect
   ↓
Verify + Triage
   ↓
┌───────────────────────────────┐
│   Response Actions Loop       │
│  Scope ↔ Contain              │
│    ↕       ↕                  │
│  Eradicate ↔ Recover          │
└───────────────────────────────┘
   ↓
Debrief
```

Decision Makers influence the entire process.

## Prepare

Goal:
- readiness.

## Detect

Goal:
- find EOI / possible incidents.

Important:
- detection is continuous, not a one-time step.

## Verify

Question:
- is this really an incident?

Purpose:
- avoid wasting resources on non-incidents.

## Triage

Question:
- how important is this incident relative to others?

Inputs:
- organizational objectives;
- impact;
- criticality;
- available resources.

## Scope

Question:
- how broad is compromise?

Inputs:
- IOC;
- TTP;
- detect/verify evidence;
- affected systems;
- potential organizational impact.

## Response Actions Loop

Core actions:
- Scope
- Contain
- Eradicate
- Recover

Rule:
- repeat as many times as needed.

Exit condition:
- no new evidence;
- response team confident;
- decision makers confident.

## Decision Maker context

Technical responders know:
- threat detection;
- forensics;
- IR procedures.

Decision makers know:
- business criticality;
- acceptable downtime;
- regulatory obligations;
- customer/contract impact;
- continuity priorities.

Best response requires both.

## Main anti-pattern

```text
technically correct
      ≠
organizationally correct
```

Example:
taking every affected system offline at once for imaging may be technically defensible but operationally harmful.

## Modern response rule

```text
Observe → Verify → Prioritize → Scope → Act → Re-scope → Act again
```

## Practical acceptance

DAIR works as intended when:

- response is not forced into a linear sequence;
- new evidence can reopen earlier actions;
- scope is continuously refined;
- business context affects prioritization;
- response actions repeat until confidence is sufficient.
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

