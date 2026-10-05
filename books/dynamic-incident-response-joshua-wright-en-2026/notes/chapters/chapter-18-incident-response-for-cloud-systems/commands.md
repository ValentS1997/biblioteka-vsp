# Команды и cloud IR artifacts Chapter 18

Только source-supported material.

## Listing 141 — Entra ID retention check

Source uses Azure CLI to inspect diagnostic/log retention configuration.

Purpose:
- verify log retention before an incident;
- determine whether historical authentication/audit evidence will exist.

Classification:
- read-only.

## Listing 142 — Azure role assignment scope

Source uses Azure CLI role-assignment enumeration with the `--all` scope.

Purpose:
- identify direct role assignments;
- understand effective scope across resource groups and subscriptions.

Classification:
- read-only.

## Listings 143–144 — authentication and CloudTrail evidence

Source includes:
- Azure sign-in detail;
- AWS CloudTrail resource-creation event.

Purpose:
- reconstruct identity activity;
- identify attacker-created resources.

## Listing 145 — Azure VM isolation

Source demonstrates a state-changing Azure NSG quarantine workflow.

Conceptual sequence:
- create an isolation policy;
- preserve access from the forensic network;
- block other inbound/outbound traffic;
- attach the isolation policy to the compromised VM interface.

Risk:
- may interrupt legitimate production traffic.

Verification:
- confirm quarantine is applied;
- confirm forensic access remains;
- confirm unwanted connectivity is blocked.

Rollback:
- restore previous network policy `[Needs confirmation]`.

## Listing 146 — storage access remediation

Source demonstrates provider-specific restriction of exposed cloud storage.

Operational pattern:
- preserve evidence;
- verify intended exposure;
- restrict access;
- validate resulting access state;
- review historical access logs.

## Listing 147 — IAM persistence enumeration

Purpose:
- identify unauthorized users, roles, policies, keys and application credentials.

Classification:
- enumeration is read-only.

## Listing 148 — cross-region serverless enumeration

Purpose:
- identify persistence in regions the organization does not normally use.

Key lesson:
`single-region check != cloud eradication`.

## Listing 149 — automated cloud isolation/snapshot

Source demonstrates a provider-native automated investigation workflow triggered by detection.

Actions conceptually include:
- isolate workload;
- preserve network telemetry;
- snapshot evidence;
- tag resources;
- initiate investigation.

Required controls:
- precise trigger;
- bounded permissions;
- audit trail;
- rollback/exception procedure;
- post-action validation.

## Listing 150 — immutable forensic storage

Source configures immutable object storage for evidence.

Purpose:
- tamper resistance;
- chain-of-custody support;
- controlled retention.

Acceptance:
- test retention and immutability behavior before operational reliance.

## Listing 151 — cloud-hosted forensic platform

Source demonstrates deployment of Velociraptor using container/cloud infrastructure.

Purpose:
- create on-demand forensic capability.

Operational consideration:
- protect forensic management access and evidence;
- separate forensic trust from compromised production trust where practical.

## Command discipline

Before any state-changing cloud action:
- verify tenant/account/subscription/project;
- verify region;
- verify exact resource;
- capture current configuration;
- preserve evidence;
- define rollback;
- document approval.

After:
- inspect audit logs;
- validate effective permissions/networking;
- confirm attacker access stopped;
- continue multi-region enumeration;
- update incident timeline.
