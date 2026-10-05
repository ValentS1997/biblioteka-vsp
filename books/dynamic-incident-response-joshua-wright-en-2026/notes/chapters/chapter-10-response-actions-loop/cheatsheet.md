# Шпаргалка: Chapter 10 — Response Actions Loop

## Core loop

```text
Scope
  ↕
Contain
  ↕
Eradicate
  ↕
Recover
  ↺
```

Не фиксированная последовательность.

## Why iterate

Single-pass response fails because of:

- incomplete understanding;
- insufficient insight;
- incomplete evidence;
- limited scope.

## Iteration triggers

### 1. New IOC
New artifact → go back to Scope.

### 2. Scope expansion
Known IOC reaches new systems/business units.

### 3. Incomplete eradication
Reinfection / persistence remains.

### 4. Evidence revelation
Memory/log/timeline/malware analysis reveals new facts.

### 5. Business/external change
Legal, regulator, insurance, law enforcement, priorities change.

## Documentation minimum

For every major action:
- what;
- when;
- who;
- why;
- business impact.

Maintain continuity across iterations.

## Exit criteria

### Technical
- no new IOC;
- no signs of attacker;
- eradication verified;
- systems stable after recovery.

### Business
- objectives met;
- acceptable risk achieved;
- cost-benefit supports closure;
- residual uncertainty accepted.

## Exit decision

Must be documented:

```text
decision maker
+ evidence
+ business context
+ accepted residual risk
+ timestamp
```

## Practical risks

- responder fatigue;
- budget pressure;
- slow tools/manual forensics;
- documentation burden;
- poor shift handoff;
- stakeholder impatience.

## Communication

Audience-specific:
- executive summary;
- technical briefing;
- user/service update.

Frequency should follow severity and phase.

## Main takeaway

```text
new evidence
   ↓
new understanding
   ↓
new response cycle
   ↓
better resolution
```
