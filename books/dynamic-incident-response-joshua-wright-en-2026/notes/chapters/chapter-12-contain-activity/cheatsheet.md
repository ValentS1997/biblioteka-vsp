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
