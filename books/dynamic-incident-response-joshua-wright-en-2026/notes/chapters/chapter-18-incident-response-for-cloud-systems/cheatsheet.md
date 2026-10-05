# Шпаргалка: Chapter 18 — Cloud Incident Response

## Core cloud IR model

```text
Identity
+ Permissions
+ Control Plane
+ Data Plane
+ Resources
+ Regions
+ Runtime Telemetry
= Cloud Scope
```

## Initial access
- weak credentials;
- missing MFA;
- misconfiguration;
- exposed API/UI;
- excessive permissions.

## Prepare
Verify before incident:
- audit logging enabled;
- retention sufficient;
- all regions/accounts covered;
- data-plane logging where needed;
- IRT read/write roles defined;
- emergency access controlled;
- SaaS logs available.

## Detect
Native tools:
- AWS GuardDuty;
- Azure Defender for Cloud;
- Google Security Command Center.

Do not rely solely on them.

## Scope
Enumerate:
- tenant/account/subscription/project;
- all regions;
- direct/inherited roles;
- service principals;
- access keys;
- sessions/tokens;
- compute/functions;
- storage;
- network resources;
- SaaS integrations.

## Critical cloud warning

```text
credential rotation
≠
session revocation
```

## Logs
Control plane: API/config actions.  
Data plane: actual data/resource access.  
Network: flow logs.  
Host/runtime: process/filesystem/container execution.

## Four common mistakes
1. terminate before snapshot/capture;
2. rotate credentials but leave sessions alive;
3. inspect only control-plane logs;
4. inspect only one region.

## Persistence
Check:
- IAM users/roles;
- app registrations;
- service principals;
- access keys;
- OAuth grants;
- serverless functions;
- automation;
- malicious images;
- trust/resource policies;
- networking changes.

## Serverless / containers
Need:
- runtime visibility;
- audit logs;
- registry/image history;
- ephemeral evidence capture.

## Main takeaway

```text
cloud IR
=
identity-centric
+ API-aware
+ multi-region
+ data-plane aware
+ runtime-aware
```
