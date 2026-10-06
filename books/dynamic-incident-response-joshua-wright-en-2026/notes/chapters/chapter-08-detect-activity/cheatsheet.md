# Шпаргалка: Chapter 8 — Detect Activity

## Methodologies

| Method | Strength | Limitation |
|---|---|---|
| Signature | fast, high confidence | misses novel/modified threats |
| Behavioral | catches abnormal behavior | baseline/tuning required |
| ML | scales across telemetry | drift/data quality/evasion |
| Hybrid | combines strengths | needs engineering maturity |

## Active vs Passive

```text
Passive:
alert / employee / third party
        ↓
known starting point

Active:
no alert
   ↓
hunt hypothesis
   ↓
search telemetry
```

## Detection sources

Technical:
- EDR
- NDR
- SIEM
- SOAR
- logs
- network telemetry
- cloud telemetry

Human:
- employees
- sysadmins
- help desk
- researchers
- partners

## Threat hunting priority

```text
hash / IP
  ↓ easy to change
domain
  ↓
network/host artifacts
  ↓
tools
  ↓
TTPs
  ↓ hard to change
```

Human hunters should focus higher in the Pyramid of Pain.

## Detection-driven collection

Use case first:
1. define threat;
2. identify required data;
3. filter irrelevant noise;
4. retain useful fidelity;
5. correlate signals;
6. tune continuously.

## Encrypted traffic

Look at:
- connection timing;
- duration;
- data volume;
- certificate metadata;
- TLS handshake;
- JA4 fingerprints.

## Cloud-native detection

Containers:
- eBPF
- runtime sockets
- audit logs
- service mesh

Serverless:
- provider logs
- function telemetry
- invocation anomalies

Hybrid/multi-cloud:
- unified telemetry
- control-plane analytics
- cross-environment correlation

## Challenges

- data volume/velocity;
- encryption;
- attacker evasion;
- skills gap.

## Detection improvement loop

```text
Detect
  ↓
Investigate
  ↓
Find gap
  ↓
Tune / add rule
  ↓
Purple-team validation
  ↓
Detect better
```

## Handoff to Verify/Triage

Document:
- alert/source;
- timestamps;
- affected assets;
- technical indicators;
- why event is interesting.

Do not decide full incident truth inside Detect; hand off EOI to Verify/Triage.
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

