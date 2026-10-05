# Шпаргалка: Chapter 16 — AI-assisted Incident Response

## Core rule

```text
AI accelerates
≠
AI decides
```

Human analyst remains accountable.

## Before using AI

Ask:
- what data will be sent?
- who stores it?
- can it be used for training/QA?
- what retention exists?
- is this allowed by policy/legal/contract?
- can data be sanitized first?

## Deployment tradeoff

| Option | Capability | Data Control | Operational Cost |
|---|---|---|---|
| Frontier SaaS | highest | lowest | low setup |
| Open-weight cloud | medium | medium | medium |
| Open-weight local | medium | highest | high |

## Core AI risks

- hallucination;
- non-determinism;
- stale knowledge;
- false positives;
- missed indicators;
- context limits;
- sensitive-data exposure.

## Prompt structure

```text
Role / Context
Task
Input
Constraints
Reasoning approach
Output format
```

## Foundational use cases

- code explanation;
- deobfuscation;
- IOC extraction;
- log orientation;
- anomaly review;
- query generation;
- stakeholder translation.

## Intermediate use cases

- DAIR playbooks;
- incident reports;
- executive summaries;
- tabletop scenarios;
- Twine interactive training.

## MCP

```text
Model
 ↓
MCP client
 ↓
MCP server
 ↓
Tool / Data
```

Use:
- threat hunting;
- enrichment;
- correlation;
- report guidance.

Risks:
- prompt injection;
- excessive permissions;
- data leakage;
- supply-chain compromise;
- weak auditability.

## Agentic workflow

```text
Reason → Act → Observe → Repeat
```

Trust controls:
- read-only default;
- deterministic tools;
- explicit approval;
- command preview;
- audit log;
- bounded permissions.

## Inference constraint

```text
raw evidence
   ↓
trusted parser
   ↓
structured facts
   ↓
AI interpretation
```

Prefer this over direct model guessing.

## Verification matrix

| AI output | Required verification |
|---|---|
| Log finding | source log/query |
| Malware/code claim | code/tool output |
| Report | evidence/timeline |
| Playbook | technical review |
| Query | syntax + scope |
| Agent action | permission + effect |

## Main takeaway

```text
evidence
+ deterministic tools
+ AI acceleration
+ human verification
+ audit trail
= defensible AI-assisted IR
```
