# Шпаргалка: Chapter 12 — Contain Activity

## Core objective

```text
stop attacker harm
+ preserve evidence
+ maintain acceptable operations
```

## Strategy selection

### Passive
Use when:
- intelligence collection valuable;
- attacker behavior unclear;
- aggressive action may trigger damage.

### Active
Use when:
- impact ongoing;
- destruction/encryption active;
- exfiltration active;
- safety/critical systems at risk.

### Adaptive
Start narrow and escalate:
- monitoring;
- progressive restrictions;
- deceptive containment;
- hard isolation when needed.

## Identity containment order

```text
1. revoke credentials
2. terminate sessions
3. revoke refresh/offline tokens
4. conditional access
5. SSO/application coordination
6. third-party integration containment
```

## Residual-access warning

```text
password reset
   ≠
session termination
   ≠
token revocation
```

Treat time between these actions as an SLA.

## Network/host controls

- VLAN / ACL / security groups;
- DNS sinkholes;
- EDR isolation;
- local firewall;
- process termination;
- WAF;
- database restrictions.

## Cloud controls

- revoke IAM/service-principal access;
- remove instances from load balancers;
- quarantine security groups/NSGs;
- snapshot;
- termination/deletion protection;
- IR tags;
- disable triggers/serverless permissions.

## Remote worker controls

- EDR isolation;
- MDM/MAM;
- per-user/device VPN restrictions;
- identity-based SaaS controls;
- replacement-device process.

## Evidence timing

### Isolate first
when:
- robust external telemetry exists;
- attacker interference risk high.

### Collect first
when:
- volatile connection state may be lost;
- alternate telemetry weak.

## Validation

### Network
- C2 stopped?
- new outbound patterns?
- tunneling?

### Process
- malware respawn?
- new services/persistence?
- abnormal parent-child chains?

### Logs
- failed re-auth?
- privilege escalation?
- exfiltration signs?
- new IOC?

## Main takeaway

```text
contain
  ↓
validate
  ↓
observe attacker adaptation
  ↓
adjust containment
  ↓
validate again
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

