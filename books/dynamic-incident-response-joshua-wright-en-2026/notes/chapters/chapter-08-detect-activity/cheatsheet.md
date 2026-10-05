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
