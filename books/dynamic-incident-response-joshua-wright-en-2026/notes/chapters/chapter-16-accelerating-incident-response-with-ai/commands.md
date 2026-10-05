# Команды, prompts и integration artifacts Chapter 16

Только source-supported material.

## Listing 122 — Structured Prompt for IOC Extraction

Source uses a structured prompt with:
- role;
- task;
- constraints;
- explicit output fields;
- machine-readable formatting.

Operational lesson:
structured prompts make generated output easier to review and reuse.

## Listing 123 — Suspicious Scheduled Task

Source shows a Windows scheduled-task command executing hidden PowerShell with ExecutionPolicy bypass and remote payload retrieval.

This is an attacker artifact, not a defender command.

Use:
- analysis;
- deobfuscation;
- IOC extraction.

Do not execute it.

## Listings 124–125 — Code-analysis prompts/artifacts

Source provides:
- prompt for plain-language explanation of suspicious PowerShell;
- obfuscated C# sample for iterative analysis.

Operational rule:
AI interpretation must be independently validated before response action.

## Listing 126 — Executive Summary Generation Prompt

Input:
- incident findings.

Output:
- management-oriented summary.

Verification:
- facts;
- chronology;
- impact;
- confidence wording;
- no unsupported claims.

## Listings 127–128 — IR Playbook Generation

Source builds a structured DAIR playbook prompt.

Expected sections include:
- Detect;
- Verify;
- Triage;
- Scope;
- Contain;
- Eradicate;
- Recover;
- Debrief;
- References;
- Version Control.

Risk:
generated playbook may include incorrect or environment-inapplicable steps.

Acceptance:
technical review before use.

## Listings 129–131 — Incident report + MCP guidance

Source demonstrates:
- executive report drafting;
- MCP server configuration;
- specialized report evaluation.

MCP integration changes the trust model because the model gains access to external knowledge/tools.

Required controls:
- allowlist servers;
- least privilege;
- log tool calls;
- inspect data paths.

## Listings 132–136 — Tabletop/Twine generation

Source uses prompts to generate:
- exercise concepts;
- organization-grounded scenarios;
- Twine/Twee branching content.

Use only sanitized organizational artifacts where policy requires.

## Listing 137 — OpenSearch threat-hunting query

Source provides a Lucene query for suspicious web behavior and shows natural-language MCP-driven threat hunting.

Key point:
MCP may translate natural language into executable search queries.

Verification:
- inspect generated query;
- validate index/time scope;
- compare results with raw logs.

## Protocol SIFT

Source describes AI orchestration of forensic tools.

Controls:
- read-only default;
- analyst approval before modification;
- exact command preview;
- deterministic parser/tool output;
- audit log.

## Listing 138 — Claude Code Audit Log Example

Purpose:
- preserve analyst/agent action trace;
- support defensibility and reproducibility.

## Listing 139 — Skill File

Source uses a Claude Code skill file for Sigma rule generation.

Pattern:
- reusable process;
- standardized output;
- embedded quality guidance.

Operational lesson:
prompt/skill libraries should be versioned and reviewed like other technical artifacts.

## Safety boundary

Do not treat AI-generated commands as trusted merely because they are syntactically valid.

Before execution:
1. inspect exact command;
2. confirm target/scope;
3. classify read-only vs modifying;
4. preserve rollback where needed;
5. require human approval for state change.

After execution:
1. capture output;
2. compare with expected result;
3. log action;
4. re-evaluate next step.

## Rollback

AI orchestration itself has no universal rollback.

Rollback belongs to the underlying action/tool and remains `[Needs confirmation]` per environment unless explicitly defined.
