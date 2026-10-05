# Шпаргалка: Chapter 14 — Recover Activity

## Recovery gate

```text
eradication complete enough
      ↓
pre-restoration verification
      ↓
functional + security validation
      ↓
system owner acceptance
      ↓
enhanced monitoring
      ↓
production restoration
      ↓
remove containment incrementally
      ↓
capture metrics
```

## Pre-restoration checklist

Confirm:
- root cause fixed;
- exploited vulnerability patched;
- credentials rotated;
- persistence removed;
- backup predates compromise;
- rebuild source trusted;
- EDR/firewall/logging active;
- final IOC scan clean.

## Functional validation

Test:
- business workflow;
- data access;
- transactions;
- dependencies;
- authentication;
- integrations.

## Security validation

Check:
- EDR reporting;
- firewall;
- logging delivery;
- hardening;
- patches;
- IOC/TTP detections.

## Owner acceptance

Record:
- who tested;
- what was tested;
- result;
- accepted limitations;
- owner sign-off.

## Enhanced monitoring

Temporarily increase:
- auth logging;
- process creation;
- network events;
- filesystem/config events;
- admin actions.

Before enabling:
- verify forwarding capacity;
- verify ingestion;
- assign monitoring ownership.

## Phased recovery

Good when:
- uncertainty remains;
- capacity constrained;
- batches can be observed.

## Coordinated recovery

Good when:
- systems are tightly coupled;
- partial startup breaks dependencies.

## Containment removal

```text
inventory
→ remove one measure
→ validate
→ monitor
→ continue
```

Do not assume every containment control must be removed.

## Cloud recovery

Verify:
- snapshot date vs incident timeline;
- IAM/role correctness;
- audit logging;
- IaC integrity;
- cloud/on-prem dependencies.

## Recovery metrics

Track:
- start;
- validation;
- acceptance;
- production;
- issues;
- cost;
- resource hours.

## Main takeaway

```text
secure
+ functional
+ accepted
+ monitored
= ready for production
```
