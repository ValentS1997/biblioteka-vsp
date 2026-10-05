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
