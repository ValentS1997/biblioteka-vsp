---
book_id: dynamic-incident-response-joshua-wright-en-2026
chapter_number: 13
source_title: "Eradicate Activity"
source_pdf_page_range: "300-404"
rag_chunk_range:
  first: "dynamic-incident-response-joshua-wright-en-2026:p0300:c01"
  last: "dynamic-incident-response-joshua-wright-en-2026:p0404:c01"
translation_status: "DRAFT_FOR_QA"
license_notice: "Неофициальный русский перевод / unofficial Russian translation; original work CC BY 4.0. См. ../ATTRIBUTION.md."
third_party_review_policy: "Figures, external quotations, product screenshots, and executable third-party/malicious payload material remain fail-closed where marked."
source_repair:
  - range: "references [26]-[36]"
    status: "REPAIRED_FROM_OFFICIAL_HTML"
    source: "https://dynamicincidentresponse.com/chapters/eradicate.html"
translation_notes:
  - "Canonical English RAG is source of truth."
  - "Assembled from full-fidelity source-range segments."
  - "Bibliography references [26]-[36] were restored into canonical RAG from the official book HTML after a PDF extraction gap was detected."
---

# Глава 13. Искоренение угрозы

Activity **eradicate — искоренение угрозы** — важная waypoint incident response, где focus смещается от containment attacker operations к systematic removal attacker presence и reversal изменений, внесённых в environment.

Containment стремится:

- остановить ongoing attacker activity;
- предотвратить continued access.

Eradication стремится:

- устранить attacker access;
- удалить persistence/artifacts;
- вернуть systems в secure state.

Eradication ещё не является full recovery. Она создаёт understanding и secure baseline, необходимые для безопасного возвращения normal operations в Recover activity.

### Рисунок 91. Eradicate Activity Waypoint

THIRD_PARTY_REVIEW_REQUIRED — visual asset не воспроизводится автоматически; сохраняются caption и cross-reference.

Chapter рассматривает:

- eradication objectives;
- timing/sequencing;
- investigation methods;
- removal attacker artifacts;
- persistence removal;
- validation eradication success;
- documentation;
- practical examples.

# ERADICATE OBJECTIVES

Effective eradication требует comprehensive insight, полученного через investigation и analysis collected evidence.

Как и Contain, Eradicate состоит из двух основных компонентов:

1. analyze collected data;
2. eliminate attacker presence.

Eradication decisions могут существенно менять environment, поэтому responders должны балансировать:

- investigative rigor;
- urgency restoration;
- organizational needs.

В этой части source объясняет:

- почему investigation предотвращает recurrence;
- как short-form и long-form investigation идут параллельно;
- как root cause analysis выявляет conditions, позволившие compromise.

## Preventing Incident Recurrence Through Investigation

Common mistake — пропустить investigation и сразу rebuild system.

Типичный shortcut:

1. wipe drive;
2. reinstall OS;
3. restore backup;
4. return system to production.

Decision makers могут предпочитать такой path, потому что Business Disaster Recovery (BDR) часто даёт predictable recovery timeline.

Но rebuild сам по себе не отвечает на underlying causes.

Если не определить:

- initial access vector;
- compromised credentials;
- other affected systems;
- persistence mechanisms;
- exploited vulnerability;

то same vector может привести к recompromise после возврата system.

Source выделяет вопросы, на которые investigation должна дать ответ:

- What was the initial access vector? Закрыт ли он?
- Какие credentials compromised? Rotated ли они?
- К каким other systems attacker получил access? Eradicated ли они?
- Какие persistence mechanisms deployed? Все ли identified/removed?
- Какая vulnerability enabled attack? Patched ли она?

Investigation — механизм предотвращения incident recurrence.

## Investigation During Eradication

Containment завершено, но business pressure остаётся:

- systems offline;
- users disrupted;
- productivity lost;
- owners хотят production back immediately.

Rushing eradication risks:

- missed persistence;
- missed compromised systems;
- unpatched entry vectors;
- new incident shortly after restoration.

Но forensic analysis требует time.

Potential data sources:

- logs;
- memory;
- disk images;
- network traffic.

Deep analysis может занимать days/weeks.

Эта tension определяет Eradicate:

> Нужно понимать attacker sufficiently для reliable removal, но не удерживать business operations offline дольше, чем необходимо.

DAIR разделяет investigation на два параллельных tracks:

- **short-form investigation**;
- **long-form investigation**.

### Рисунок 92. Short-Form vs Long-Form Investigation

THIRD_PARTY_REVIEW_REQUIRED — visual asset не воспроизводится.

## Short-Form Investigation

Short-form investigation быстро analyzes evidence from Contain, чтобы определить:

- attacker methods;
- persistence;
- compromised systems;
- minimum eradication actions.

Goal — sufficient understanding для prompt action при minimal business disruption.

Responders должны ответить:

- Что сделал attacker?
- Как он вошёл?
- Где ещё он может присутствовать?
- Что необходимо удалить/изменить, чтобы он не вернулся тем же способом?

Short-form investigation должна дать practical understanding TTPs, достаточный для removal.

Если в ходе eradication обнаружены:

- new IOC;
- new persistence mechanisms;
- additional compromised systems;

это input для следующей iteration Response Actions Loop.

Eradication требует practical remediation:

- remove attacker-installed components;
- close exploited entry points;
- restore confidence that compromise will not immediately recur.

## THE DIRTY KEBAB: SHORT-FORM INVESTIGATION

Source приводит метафору от technical editor Steve Armstrong.

Смысл: иногда responder не нужен forensic masterpiece; нужен быстрый, достаточно надёжный assessment, позволяющий принять operational decision.

`THIRD_PARTY_REVIEW_REQUIRED` — direct quotation и персональный colloquial wording third-party speaker не воспроизводятся verbatim.

В incident context metaphor означает:

- определить, compromised ли system;
- понять minimum required eradication;
- дать early assessment;
- позволить team двигаться дальше.

Не каждый incident и не каждая system требуют deep-dive.

Short-form — один из resource-management tools.

Главное — правильно определить, когда достаточен focused assessment, а когда required long-form forensic depth.

# Long-Form Investigation for Comprehensive Understanding

Long-form investigation, также называемая deep-dive investigation, может идти параллельно short-form.

Goal — comprehensive understanding incident.

Она часто использует forensic techniques, требующие:

- more time;
- specialized expertise;
- additional cost/resources.

Long-form может быть нужна для:

- regulatory compliance;
- litigation;
- insurance;
- threat intelligence;
- organizational learning;
- comprehensive timeline;
- complete data-impact assessment;
- legal-standard evidence packages.

Эта depth часто incompatible с urgent restoration timelines.

Поэтому organization должна балансировать:

- fast short-form support for eradication;
- parallel long-form work for broader requirements.

### Long-Form Scope Governance

Scope определяется совместно с decision makers.

**Legal counsel**

- evidence standards;
- litigation/regulatory requirements.

**Compliance**

- required records;
- audit/regulatory documentation.

**Risk management**

- appropriate investigation depth;
- severity/impact threshold.

Resources следует направлять на work, который даёт tangible organizational value.

## LONG-FORM INVESTIGATION EXAMPLE: IDAHO MURDERS

Source приводит criminal-forensics example из RSAC 2025 presentation Heather Barnhart, SANS DFIR Curriculum Lead / Head of Faculty.[1]

Case связан с расследованием убийств четырёх University of Idaho students и forensic analysis Android device Bryan Kohberger.

### Рисунок 93. BK Android Device Log

THIRD_PARTY_REVIEW_REQUIRED — third-party visual не воспроизводится.

Source describes workflow:

- seizure Android phone;
- unlocking/extraction via Magnet GrayKey;
- full storage image;
- analysis in Cellebrite Physical Analyzer;
- native-log review;
- manual analysis Android `eRR.p` log;
- timeline reconstruction.

Analysis identified phone power-down/power-up events and battery state, used as evidence relevant to movement/alibi assessment.

`THIRD_PARTY_REVIEW_REQUIRED` — claims and direct framing concerning third-party criminal proceeding are retained only as source-attributed summary; no additional assertion beyond canonical source.

Lesson for IR:

Long-form rigor can require:

- full imaging;
- native low-level logs;
- manual artifact analysis;
- timeline reconstruction;
- anti-forensic/evasion analysis.

Criminal forensics and incident response have different goals, but both require meticulous evidence work when comprehensive proof is needed.

# Pursuing Root Cause Analysis

Root cause analysis (RCA) remains central in both short-form and long-form tracks.

Purpose:

- understand vulnerabilities/shortcomings creating attacker opportunity.

Correcting broader security weaknesses may extend into Recover, but understanding **how attacker exploited them** is required for Eradicate.

If responders see only symptoms, they may:

- miss persistence;
- miss other compromised systems;
- remove malware but not causal attack path.

Example:

- malware on one system = symptom;
- phishing compromise of multiple users = root-cause context expanding eradication scope.

During Eradicate, responders work backward from compromise symptoms to weaknesses in defenses.

Modern attacks often chain multiple opportunities, so RCA should identify all meaningful contributing conditions rather than one visible cause.

## FINTECH SSH COMPROMISE: ROOT CAUSE ANALYSIS

Source recounts an incident involving Linux transaction-processing cluster at a fintech company.

A junior sysadmin changed root password to a weak value.

An internet-facing Linux server allowed SSH password authentication and remote root access.

Attacker guessed the password and gained root.

Security lead initially blamed the junior administrator.

`THIRD_PARTY_REVIEW_REQUIRED` — direct dialogue involving third parties is not reproduced verbatim.

Independent RCA found a stack of contributing failures:

- SSH exposed to Internet without documented business justification;
- remote root login enabled;
- password authentication allowed instead of key-based authentication;
- failed authentication logged but not monitored;
- no password-complexity policy;
- no change-control approval for root-password changes on production.

Further context showed management/security decisions had prioritized easier remote administration while deprioritizing SSH protections.

Lesson:

> Root cause analysis is not about identifying a person to blame; it is about identifying what must be fixed.

# Assessing Root Cause

Without RCA responders risk:

- leaving persistence;
- missing compromised systems;
- allowing same attack via another entry point.

RCA goals:

1. understand complete attack chain;
2. identify systems/artifacts requiring eradication;
3. reveal systemic weaknesses in controls/processes/policies;
4. distinguish symptoms from underlying causes;
5. prioritize remediation.

Structured process:

1. **Define the effect**
   - what happened;
   - systems compromised;
   - data accessed;
   - business impact.

2. **Group possible causes**
   - framework such as four P's.

3. **Populate categories**
   - investigation findings.

4. **Identify remediation**
   - action for each root cause.

5. **Prioritize**
   - changes addressing multiple/high-risk contributing factors.

## Four P's Framework

The four P's categorize root causes:

- **People** — training, awareness, staffing, human practices;
- **Process** — reviews, change management, vulnerability scanning, monitoring;
- **Product** — software flaws, misconfiguration, missing technical controls, inadequate logging, end-of-life technology;
- **Policy** — governance, accountability, requirements, enforcement.

This framework helps avoid oversimplifying incidents into a single human or technical mistake.

## Root Cause Analysis Example: Public S3 Bucket Exposure

Source описывает customer incident: S3 bucket

`dat-ng-cdn-890378906859`

с customer data несколько месяцев был доступен unauthorized users.

Initial cause выглядел просто:

- developer deployed new feature;
- bucket ACL/policy оказался overly permissive;
- любой authenticated AWS principal мог list/read bucket.

### Listing 62. Permissive Principal Policy for S3 Bucket

~~~json
{
  "Id": "dat-ng-cdn-890378906859-Policy",
  "Statement": [
    {
      "Action": [
        "s3:Get*",
        "s3:List*"
      ],
      "Effect": "Allow",
      "Principal": {
        "AWS": "*"
      },
      "Resource": [
        "arn:aws:s3:::dat-ng-cdn-890378906859",
        "arn:aws:s3:::dat-ng-cdn-890378906859/*"
      ],
      "Sid": "AllowPublicRead"
    }
  ]
}
~~~

`"AWS": "*"` grants Get/List access to any AWS user/principal within source context.

Surface-level conclusion: developer misconfiguration.

Systematic RCA reveals broader organizational exposure.

### Рисунок 94. S3 Bucket Root Cause Analysis

THIRD_PARTY_REVIEW_REQUIRED — visual not reproduced.

### People

Findings:

- developers lacked cloud-security training;
- no training on S3 access controls;
- no clear data-classification understanding;
- unclear ownership for cloud-infrastructure security review;
- assumption that another person/team would catch issues.

### Process

Findings:

- no peer review/approval for IaC templates;
- Terraform defining public access was not independently reviewed;
- no automated IaC security scanning;
- no security approval gate before externally accessible deployment;
- no periodic audit for public S3 buckets.

### Product

Technical control failures:

- insecure defaults in IaC templates;
- developers had to manually configure secure access;
- CloudTrail enabled but no alerting for unusual bucket access;
- no AWS Config-like auto-remediation for dangerous policy changes.

### Policy

Governance gaps:

- no data-classification policy;
- no explicit least-privilege cloud policy;
- no security review requirement in change-management policy;
- no audit process for cloud-resource security/regulatory conformance.

Comprehensive RCA transformed one developer error into systemic remediation targets:

- training;
- code review;
- IaC scanning;
- secure defaults;
- alerting;
- auto-remediation;
- cloud-security policy.

Benefit: reduce probability of similar incident across entire cloud environment, not just one bucket.

# Fishbone Diagram Mapping

Fishbone diagram = cause-and-effect / Ishikawa diagram.

Developed by Kaoru Ishikawa for quality management.

Visual structure:

- fish head = effect/problem;
- branches/bones = causal categories.

Purpose:

- systematic cause exploration;
- avoid stopping at symptoms;
- collaborative visual analysis.

Traditional six-M categories:

- Man / People;
- Machine;
- Materials;
- Methods;
- Measurement;
- Milieu / Environment.

### Рисунок 95. Fishbone Diagram Example

THIRD_PARTY_REVIEW_REQUIRED — visual not reproduced.[2]

For IR, source simplifies the model using four P's:

- People;
- Process;
- Product;
- Policy.

Fintech SSH example can be mapped into these branches.

Fishbone is not strict taxonomy; overlap between categories is acceptable.

### Рисунок 96. Fishbone Illustration: Fintech SSH Compromise

THIRD_PARTY_REVIEW_REQUIRED — visual not reproduced.

The value is not category purity but systematic identification/documentation of contributing factors.

## ALTERNATIVE TO FISHBONE DIAGRAM: THE FIVE WHYS

Five Whys is a simpler RCA technique associated with Sakichi Toyoda.[3]

Process:

1. begin with observed problem;
2. ask why it happened;
3. use answer as next why;
4. continue until underlying cause identified.

The number five is heuristic, not fixed.

Could require:

- 3 iterations;
- 5 iterations;
- 7 iterations.

### Fintech SSH Example

Problem:

- attacker obtained unauthorized root access through SSH.

Causal chain:

1. Why root access?  
   Successful authentication as root.

2. Why successful authentication?  
   Weak root password was guessed.

3. Why weak password accepted?  
   No enforced password-complexity policy.

4. Why no complexity enforcement?  
   No governance process requiring SSH hardening.

5. Why Internet-exposed SSH with password authentication?  
   Deployment lacked security review/exposure management.

This reveals intervention points at multiple levels:

- credential strength;
- policy;
- governance;
- exposure management.

### When to Use Five Whys

Best for:

- focused linear causal chain;
- rapid insight;
- small teams;
- limited documentation overhead.

### When to Prefer Fishbone

Best when:

- multiple parallel causal factors;
- cross-functional collaboration;
- need stakeholder visualization;
- complex incident.

# INVESTIGATION TECHNIQUES FOR ERADICATION

Before eradication actions, responders need sufficient investigation to identify all artifacts requiring removal.

Short-form investigation should be:

- focused;
- time-boxed;
- proportional to restoration urgency.

Goal is not comprehensive digital-forensics coverage.

Goal:

- enough understanding to revoke attacker access;
- remove relevant artifacts;
- inform eradication actions.

Source explicitly notes investigation tooling/techniques evolve continuously.

Responders should maintain current skills through:

- training;
- professional development;
- tool familiarity.

Techniques covered:

- log analysis;
- live investigation;
- endpoint telemetry/EDR;
- memory forensics;
- network analysis;
- malware analysis;
- BEC;
- insider threat;
- supply-chain;
- cloud incidents.

This chapter is a representative practical guide, not complete DFIR reference.

# Log Investigation

Log investigation examines data collected during Contain to reconstruct attacker actions and identify eradication targets.

Log sources can include:

- OS events;
- application logs;
- firewall;
- VPN;
- authentication;
- security appliances;
- cloud logs.

Value:

- temporal history;
- lateral movement visibility;
- system involvement;
- artifact creation;
- account activity;
- exfiltration clues.

Problem: volume.

A single server may generate gigabytes over attacker dwell time.

Without aggregation/correlation, manual analysis delays eradication.

## Sigma for Log Analysis

Sigma provides portable detection-rule format.[4]

Sigma logic can describe threats across:

- Windows Event Logs;
- Syslog;
- cloud logs;
- web logs;
- other structured logs.

Sigma itself is not the backend analysis system.

Sigma rules can be converted to queries for:

- Splunk;
- Elasticsearch;
- other platforms.

Some tools directly apply Sigma.

## Hayabusa

Hayabusa is open-source Windows EVTX forensic timeline/threat analysis tool with Sigma support.[5]

It can:

- scan multiple EVTX files;
- produce threat report;
- build timeline.

### Listing 63. Hayabusa Windows Event Log Analysis Command

~~~bash
$ hayabusa csv-timeline -d eventlogs/ -T -o hayabusa-threathunting.csv -E   --timeline-start "2020-01-01 00:00:00 +00:00"   --timeline-end "2020-02-28 00:00:00 +00:00"   --no-color
~~~

Source output indicates:

- 361 EVTX files;
- total size 35.5 MB.

### Рисунок 97. Hayabusa Timeline Report

THIRD_PARTY_REVIEW_REQUIRED — screenshot not reproduced.

Hayabusa useful for offline Windows log review.

Sigma becomes more scalable when integrated into SIEM.

# SIEM for Log Investigation

SIEM centralizes:

- aggregation;
- normalization;
- correlation;
- querying;
- alerts.

During Eradicate analysts can pivot across environment from one IOC to related events.

Examples:

- trace compromised user from initial authentication → lateral movement → exfiltration;
- correlate failed auth + successful login from unusual location;
- deploy custom Sigma-derived detections.

### SIEM Operational Cost

SIEM requires:

- licensing/infrastructure;
- ingestion/storage capacity;
- skilled analysts;
- query-language expertise;
- log-source knowledge;
- continuous detection tuning;
- cross-team log onboarding.

A SIEM deployed without people/process/maintenance can provide little security value despite high cost.

# SAME LOGS, DIFFERENT OUTCOMES: THE RIBRIDGES DATA BREACH

Source discusses December 2024 Rhode Island government RIBridges compromise affecting services used by approximately **735,000 citizens**.[6]

Threat actor identified in source as Brain Cipher.

Initial access involved a VPN remote-access account allocated to Deloitte contractor.

Attackers reportedly:

- maintained access for months;
- exfiltrated sensitive resident data;
- used extortion.

Source states compromise of contractor VPN account occurred in July 2024 and was not reported to state until December 5, after public extortion-site activity.[7]

CrowdStrike investigation cited firewall/security telemetry showing suspicious large data transfers to external cloud storage.

`THIRD_PARTY_REVIEW_REQUIRED` — direct quotation from HIPAA Journal / CrowdStrike-derived reporting is not reproduced verbatim.

Source reports:

- firewall alerts existed during attacker dwell time;
- security operations did not effectively analyze/respond to them;
- Deloitte later agreed to pay state government $5 million without admission of liability;[8]
- a $6.3 million class-action settlement followed in October 2025.[9]

Key lesson begins here and continues in the next source range:

the same logs can be either a missed detection opportunity or a high-value post-compromise investigation resource, depending on people/process around them.

## RIBridges: Same Logs, Different Outcomes — Conclusion

Source contrasts two uses of the same firewall telemetry:

- **Missed detection opportunity:** alerts existed during attacker dwell time, but were not effectively analyzed, so organization missed an opportunity to identify exfiltration and contain earlier.
- **Investigation resource:** CrowdStrike later used those same logs to reconstruct attacker timeline, quantify exfiltration, and support eradication.

Core lesson:

> Logging supports both proactive detection/threat hunting and post-compromise investigation. Logs have value only when people/processes exist to interpret and act on them.

# Live Investigation

Live investigation uses tools directly on systems under investigation to examine current state/configuration.

Potential targets:

- Windows hosts;
- cloud control plane;
- network devices;
- applications;
- other live infrastructure.

Advantages:

- direct/current state;
- minimal interpretation layers;
- fast answers.

Risks:

- commands modify system state;
- volatile artifacts can be overwritten;
- evidence can be changed.

In DAIR, Contain should already have preserved critical evidence, allowing Eradicate live investigation to optimize for rapid assessment.

Use live investigation when:

- immediate answer is needed;
- evidence-disruption risk is acceptable;
- collected forensic evidence already meets preservation needs.

## DIFFERENTIAL ANALYSIS FOR THREAT INVESTIGATION

Differential analysis compares known-good baseline with current state.

It helps eliminate expected data and focus on:

- new artifacts;
- modified artifacts;
- state changes.

Example: Windows services.

### Listing 64. Capturing Baseline Services on Known-Good System

~~~powershell
PS C:\> Get-Service > E:\baseline-services-20251117.txt
~~~

Run on known-good system, e.g. freshly imaged workstation.

### Listing 65. Capturing Current Services on System Under Investigation

~~~powershell
PS C:\> Get-Service > E:\services-liveinvestigation.txt
~~~

Run on system under investigation.

### Listing 66. Compare Baseline and Current Services

~~~powershell
PS C:\investigation> $baseline = Get-Content .\baseline-services-20251117.txt
PS C:\investigation> $current = Get-Content .\services-liveinvestigation.txt
PS C:\investigation> Compare-Object -ReferenceObject $baseline -DifferenceObject $current

InputObject                                              SideIndicator
-----------                                              -------------
Stopped  sppsvc             Software Protection          =>
Stopped  TrustedInstaller   Windows Modules Installer    =>
Running  vjnxSoIt           HQIQATUbyNM                  =>
Running  sppsvc             Software Protection          <=
Running  TrustedInstaller   Windows Modules Installer    <=
~~~

Interpretation:

- `sppsvc` changed from Running → Stopped;
- `TrustedInstaller` changed from Running → Stopped;
- new service `vjnxSoIt` is running and absent from baseline.

Differential analysis can apply to:

- processes;
- installed software;
- scheduled tasks;
- users/groups;
- services;
- configuration;
- many structured datasets.

Its purpose is to reduce noise from known-good state.

# Endpoint Telemetry Investigation Tools

Endpoint telemetry/investigation platforms provide centralized live-query capability.

Examples:

- Velociraptor;
- GRR Rapid Response;
- Osquery.

They help query:

- system state;
- configuration;
- activity;
- IOC;
- EOI.

These tools differ from EDR.

**EDR** emphasizes:

- detection;
- prebuilt response;
- enforcement.

**Endpoint telemetry/investigation tools** emphasize:

- visibility;
- custom queries;
- analyst-driven hunts;
- state/configuration analysis.

They may have limited response capabilities, but investigation is their main role.

Platforms often use endpoint agents and support:

- canned hunts;
- custom queries;
- asynchronous collection.

Offline systems can return data when reconnecting.

## Velociraptor IOC Analysis Example

Source uses LockBit example.

On compromised host, analyst identifies use of:

`fsutil file setZeroData`

### Listing 67. LockBit fsutil SetZeroData Example

~~~text
cmd.exe /C ping 127.0.0.7 -n 3 > Nul & fsutil file setZeroData offset=0 length=524288
"C:\Users\Jeanluc\Desktop\Lsystem-7d7904945fa2.exe" & Del /f /q
"C:\Users\jeanluc\Desktop\Lsystem-7d7904945fa2.exe"
~~~

The command overwrites byte range with nulls without changing file size.

In source, LockBit uses this as anti-forensic cleanup of its executable.

Although file content is destroyed, command pattern itself becomes an IOC.

Responders can hunt for `setZeroData` across endpoint logs to identify other potentially affected systems.

### Listing 68. Custom Velociraptor Artifact for IOC Hunting: FsutilSetZeroData

~~~yaml
name: Custom.Windows.Detection.FsutilSetZeroData
author: Joshua Wright
description: |
  Hunts for invocations of `fsutil file setZeroData`, an in-place file-wiping technique that
  zeroes a byte range inside a file without changing its size. Used by LockBit and other
  ransomware platforms.

reference:
  - https://lolbas-project.github.io/lolbas/Binaries/Fsutil/
  - https://attack.mitre.org/techniques/T1485/
  - https://attack.mitre.org/techniques/T1070/004/

type: CLIENT

parameters:
  - name: IocRegex
    type: regex
    default: "(?i)setzerodata"
    description: |
      Match token `setZeroData` which is effectively unique to this fsutil verb.
  - name: ChannelRegex
    default: "(?i)security|sysmon|powershell"
    description: |
      Restrict to the channels that carry a command line.

sources:
  - query: |
      SELECT *
      FROM Artifact.Windows.EventLogs.EvtxHunter(
             IocRegex=IocRegex,
             ChannelRegex=ChannelRegex)
~~~

Running this artifact across environment can identify systems with matching execution.

### Рисунок 98. Velociraptor Artifact Hunt Results: FsutilSetZeroData

THIRD_PARTY_REVIEW_REQUIRED — screenshot not reproduced.

Primary advantage:

- rapid pivot across many endpoints;
- incident-level query reuse;
- custom detection logic;
- distributed IOC hunts.

# Memory Investigation

Memory analysis provides deep compromise visibility without relying on continuous live-system interaction.

Captured memory preserves volatile state:

- processes;
- network connections;
- loaded code;
- registry data;
- kernel structures;
- decrypted content;
- memory-only malware.

Offline analysis can be parallelized across analysts.

Two scopes:

1. process-specific;
2. whole-system.

## Process-Specific Memory Investigation

Process dump captures only target process memory.

Advantages:

- smaller dataset;
- focused scope;
- fast capture;
- useful for suspicious application/malware.

Recommended workflow:

1. suspend process;
2. dump memory;
3. resume process.

### Listing 69. Capturing Process Memory with PsSuspend and ProcDump

~~~text
C:\Users\jwrig> Z:\pssuspend.exe winword.exe

PsSuspend v1.08 - Process Suspender
Process winword.exe suspended.

C:\Users\jwrig> Z:\procdump.exe -ma winword.exe

ProcDump v11.1 - Sysinternals process dump utility

[09:15:48]Dump 1 info: Available space: 1460809175040
[09:15:48]Dump 1 initiated: C:\Users\jwrig\WINWORD.EXE_251123_091548.dmp
[09:15:48]Dump 1 writing: Estimated dump file size is 850 MB.
[09:15:49]Dump 1 complete: 851 MB written in 1.2 seconds
[09:15:49]Dump count reached.

C:\Users\jwrig> Z:\pssuspend.exe -r winword.exe

PsSuspend v1.08 - Process Suspender
Process winword.exe resumed.
~~~

`-ma` captures full accessible process memory:

- heaps;
- stacks;
- loaded modules.

### Listing 70. Extracting Strings from Process Memory Dump

~~~text
C:\Users\jwrig> Z:\strings.exe .\WINWORD.EXE_251123_091548.dmp > winword_strings.txt
~~~

### Listing 71. Searching for PowerShell Commands in Process Memory Strings

~~~powershell
C:\Users\jwrig> Select-String -Encoding Unicode -Pattern "powershell\s+-" .\winword_strings.txt

winword_strings.txt:2832782:powershell -NoProfile -NonInteractive -c "Get-Process"
winword_strings.txt:2832787:powershell -NoProfile -NonInteractive -c "Get-Process 1Password"
~~~

Process-specific dump is appropriate when:

- suspicious process already identified;
- analyst needs detailed runtime behavior;
- whole-system context is unnecessary.

# Whole-System Memory Investigation

Whole-system memory preserves complete physical memory state.

Useful for:

- unknown compromise;
- broad process/network review;
- kernel artifacts;
- registry state;
- memory-resident malware;
- lateral movement analysis.

Tools:

- WinPMEM on Windows;
- LiME on Linux.

### Listing 72. Capturing Whole-System Memory with WinPMEM

~~~text
F:\> .\go-winpmem_amd64_1.0-rc2_signed.exe acquire --nosparse ircase504.dmp
Writing driver to C:\Users\jwrig\AppData\Local\Temp\1405366611.sys
Creating service winpmem
Installed service winpmem
Started service winpmem
Memory Info:

CR3: 0x1ae002
NtBuildNumber: 0x65f4
KernelBase: 0xfffff806d4000000
[...]
Padding 8320 pages from 0x45f80000
Copying 3584 pages (0xe00000) from 0x48000000
Padding 750080 pages from 0x48e00000
Copying 3860480 pages (0x3ae800000) from 0x100000000
Completed imaging in 53.568839s
Stopped service winpmem
Removing driver from C:\Users\jwrig\AppData\Local\Temp\1405366611.sys
~~~

Source target had 32 GB RAM and capture completed under one minute.

After capture, offline analysis tools include:

- Volatility;
- MemProcFS.

Volatility can enumerate:

- processes;
- network connections;
- modules;
- registry hives;
- drivers;
- other memory structures.

Volatility runs with Python 3 and can analyze memory from Windows, Linux, and macOS.

## Vulnerable Driver Investigation

Windows driver inventory can reveal vulnerable kernel drivers that enable privilege escalation/EDR bypass.

Source example identifies `KfeCoSvc` Kyocera driver associated with known privilege-escalation risk.[10]

### Listing 73. Volatility Windows Driver Enumeration

~~~text
$ vol -qf ircase504.dmp windows.driverscan.DriverScan
Volatility 3 Framework 2.26.2

Offset         Start          Size      Name
0xbf84ba6cf4d0 0xf80666610000 0x2a000   \Driver\acpiex
0xbf84ba707e10 0xf80666860000 0x93000   \Driver\pci
0xbf84ba757cb0 0xf8067b3b0000 0x12000   \Driver\uiomap
0xbf84ba7eac10 0xf806d4000000 0x0       \Driver\WMIxWDM
0xbf84ba8ccdf0 0xf806d4000000 0x0       \Driver\PnpManager
0xbf84ba8cedf0 0xf806d4000000 0x0       \Driver\SoftwareDevice
0xbf84ba8cfdf0 0xf806d4000000 0x0       \Driver\DeviceApi
0xbf84ba8d4df0 0xf806d4000000 0x0       \Driver\ACPI_HAL
~~~

Listing continues in next source range.

## Volatility Driver Enumeration — Continuation

### Listing 73. Volatility Windows Driver Enumeration — Continuation

~~~text
0xbf84ba9d0060 0xf80666640000 0xa000    lxss
0xbf84ba9d7e20 0xf80665960000 0xe0000   CNG
[...]
0xbf84ea056e20 0xf80682840000 0x1160000 \Driver\KfeCoSvc
0xbf84ea05ee20 0xf80681cc0000 0xd5000   \Driver\PEAUTH
[...]
0xbf84fca729d0 0xf806826e0000 0x1b000   \Driver\WdNisDr
0xbf84fe14fe20 0xf806839b0000 0x10000   \Driver\winpmem
0xbf84fe2f3aa0 0xf80682800000 0xf000    \Driver\WpdUpFltr
~~~

Important entries:

- `KfeCoSvc` — Kyocera-related driver;
- `winpmem` — memory-capture driver loaded by acquisition process.

# Browsing Memory Artifacts with MemProcFS

Volatility remains one of the standard memory-analysis frameworks.

MemProcFS offers another workflow:

- mount memory image as virtual filesystem;
- browse artifacts using normal file-navigation tools;
- search with PowerShell/UNIX utilities;
- integrate memory artifacts with existing analysis tools.

MemProcFS exposes through directory structure:

- processes;
- modules;
- handles;
- registry hives;
- network connections;
- forensic timelines.

### Listing 74. Mount Memory Image with MemProcFS

~~~text
PS C:\tools\MemProcFS> .\MemProcFS.exe -device F:\memory.dmp -forensic 1
Initialized 64-bit Windows 10.0.26100

==============================  MemProcFS  ==============================
 - Author:           Ulf Frisk - pcileech@frizk.net
 - Info:             https://github.com/ufrisk/MemProcFS
 - License:          GNU Affero General Public License v3.0
 - Version:          5.16.8 (Windows)
 - Mount Point:      M:\
 - Tag:              26100_852e07b1
 - Operating System: Windows 10.0.26100 (X64)
==========================================================================
~~~

Analyst can then search mounted forensic data for known IOC.

### Listing 75. Search MemProcFS Filesystem for Indicator of Compromise

~~~powershell
PS M:\> Get-ChildItem -Path .\forensic\ -Recurse -File |
  Select-String -SimpleMatch 'backup.exe'

forensic\csv\timeline_all.csv:231:"2025-03-07 19:41:11",REG,MOD,0,0x0,0x0,\Root\InventoryApplicationFile\backup.exe|87931ab5a15fc7f5
forensic\csv\timeline_all.csv:266:"2025-03-07 19:41:09",NTFS,MOD,0,0x0,0x5efbc400,\1\Windows\Prefetch\BACKUP.EXE-AB6C9DDF.pf
forensic\csv\timeline_all.csv:277:"2025-03-07 19:41:08",NTFS,CRE,0,0x0,0x5efbc400,\1\Windows\Prefetch\BACKUP.EXE-AB6C9DDF.pf
forensic\csv\timeline_all.csv:1496:"2025-03-07 19:41:04",NTFS,RD,0,0xb49ae6,0x77d06400,"\1\Users\Robert Paulson\Downloads\backup.exe"
[...]
~~~

Findings include:

- application inventory registry entry;
- Prefetch modification;
- Prefetch creation;
- read of `backup.exe` from user Downloads.

Whole-system memory is especially useful when:

- compromise is not fully understood;
- lateral movement must be mapped;
- all attacker processes/artifacts need identification;
- recovery should not start until eradication scope is confident.

# Network Investigation

Network analysis provides cross-system view of attacker behavior.

Host analysis answers:

- what happened on a specific system.

Network analysis helps answer:

- where attacker moved;
- which systems communicated;
- where data moved;
- what infrastructure was contacted;
- what other systems require eradication.

## Network Data Sources

### Packet Capture (PCAP)

Provides deepest network visibility:

- full conversations;
- payload;
- commands/data where unencrypted;
- precise sequence.

Limitations:

- massive storage;
- narrow retention/coverage;
- encrypted TLS reduces payload visibility without decryption.

### Flow Data

Examples:

- NetFlow;
- IPFIX;
- sFlow;
- VPC Flow Logs.

Provides metadata:

- source/destination;
- ports;
- protocols;
- byte counts;
- timestamps.

Useful for:

- lateral movement;
- exfiltration-volume analysis;
- connectivity mapping.

### DNS Logs

DNS often preserves:

- C2 lookups;
- malware-distribution domains;
- exfiltration endpoints.

Attackers may forget or fail to erase centralized DNS history.

### Proxy Logs

Can reveal:

- URLs;
- user agents;
- response codes;
- web-tunneled attacker traffic;
- staging behavior.

### Firewall Logs

Show:

- allowed connections;
- blocked attempts;
- reconnaissance;
- perimeter communication.

# Network Detection and Response Platforms

NDR platforms can combine:

- signatures;
- anomaly detection;
- behavioral analytics;
- CTI enrichment.

During Eradicate they help surface suspicious network activity and pivots.

Source cautions:

> NDR findings are starting points, not complete truth.

Analysts should corroborate with:

- flow data;
- DNS;
- host evidence;
- firewall/proxy logs;
- memory/EDR.

# Network Data for Connection Mapping

Raw network data can map attacker connectivity even without dedicated NDR.

Source gives AWS example using VPC Flow Logs.

Open-source VPC Flow Log Analysis tooling can create graph where edge thickness represents transfer volume.[11]

### Listing 76. AWS VPC Flow Log Analysis Graph Generation

~~~bash
$ gzcat ~/flowlogs/*.log.gz > flowlogs_combined.txt

$ head -4 ../flowlogs_combined.txt
2 058390152209 eni-e362dfbb 10.0.2.1 10.0.3.1 50413 5432 6 11 34622 1764152928 1764152962 REJECT OK
2 058390152209 eni-e978320b 10.0.2.2 10.0.3.1 56261 5432 6 74 64131 1764153408 1764153436 ACCEPT OK
2 058390152209 eni-9991a6a9 10.0.5.1 10.0.4.1 65098 443 6 254 2911921 1764155508 1764155560 ACCEPT OK
2 058390152209 eni-429b8a69 10.0.1.1 10.0.2.2 32540 443 6 214 4242067 1764151368 1764151400 ACCEPT OK

$ LOG_TEXT=../flowlogs_combined.txt npm run build-graph

> vpc-flow-log-analysis@1.0.0 build-graph
> ts-node ./graph-generator/build-graph.ts

read and parse requests: 63.438ms
Found 90436 requests.
generate nodes and edges: 23.035ms
export graph data to file: 0.718ms
Exported log graph to /Users/jwright/flowlogs/vpc-flow-log-analysis/client/graph.json

$ npm run client

> vpc-flow-log-analysis@1.0.0 client
> ./node_modules/http-server/bin/http-server client

Starting up http-server, serving client
Available on:
  http://127.0.0.1:8080
  http://192.168.1.140:8080
Hit CTRL-C to stop the server
~~~

Workflow:

1. decompress/combine flow logs;
2. generate graph;
3. run local visualization service.

### Рисунок 99. AWS VPC Flow Log Connection Graph

THIRD_PARTY_REVIEW_REQUIRED — visual not reproduced.

Network findings feed eradication directly:

- every accessed system → examine persistence;
- every external attacker IP → block/monitor;
- every compromised credential used for lateral movement → rotate/remediate.

# Malware Investigation

When malware is found, eradication requires understanding:

- is file malicious?
- what artifacts does it create?
- how does it persist?
- what processes does it launch?
- what network infrastructure does it use?
- which other systems may host same family?

Malware investigation combines:

- static analysis;
- dynamic analysis.

Comprehensive malware reverse engineering is specialized, but IR teams need enough capability for practical eradication.

## SAFETY IN MALWARE ANALYSIS

Malware handling has direct operational risk.

Source recommends strict isolation:

- dedicated analysis system;
- never connected to production;
- no production credentials/data;
- use VM snapshots;
- disable shared folders;
- disable clipboard sharing;
- disable drag-and-drop;
- avoid broadly accessible network storage;
- transport samples on clearly labeled encrypted/password-protected media;
- use air-gapped systems for high-risk samples.

Goal: prevent accidental execution, distribution, environment compromise, or attacker awareness.

# Static Analysis

Static analysis examines binary without executing it.

Techniques:

- file identity/metadata;
- hashes;
- strings;
- PE structure;
- disassembly;
- CTI correlation.

Hashing is useful for external intelligence without uploading sample itself.

Platforms referenced:

- VirusTotal;
- Hybrid Analysis;
- other CTI sources.

### Рисунок 100. VirusTotal Search Result for File Hash

THIRD_PARTY_REVIEW_REQUIRED — third-party platform visual not reproduced.

Known family reports may reveal:

- behavior;
- persistence;
- network infrastructure;
- related sample knowledge.

## PE Structure Analysis

Windows PE tools:

- PE Studio;
- PE-Bear.

Potential insight:

- compilation time;
- imports;
- resources;
- digital signatures.

Examples:

- `ws2_32.dll` imports may indicate network behavior;
- `crypt32.dll` suggests cryptographic routines;
- `advapi32.dll` / `RegSetValueEx` suggests registry modification.

### Рисунок 101. PE-Bear PE Malware Analysis Example

THIRD_PARTY_REVIEW_REQUIRED.

Ghidra can provide deeper disassembly/reverse engineering, but requires more expertise/time.

Static analysis limitations:

- obfuscation;
- packing;
- anti-analysis;
- dormant/triggered behavior.

Therefore dynamic analysis may be needed.

# Dynamic Analysis

Dynamic analysis executes malware inside controlled environment and observes real behavior.

Tradeoff:

- stronger behavioral evidence;
- higher safety risk.

Basic workflow:

1. prepare monitoring tools;
2. snapshot analysis VM;
3. enable monitoring;
4. execute sample;
5. interact as needed to trigger behavior;
6. terminate malware;
7. stop monitoring;
8. review artifacts.

Dynamic analysis is iterative; multiple runs may be needed to build complete behavior picture.

## Dynamic Analysis — Continued

После execution sample analysts review captured output for:

- created files;
- persistence;
- registry changes;
- network activity;
- child processes.

Dynamic analysis is iterative: one run rarely reveals everything.

Windows instrumentation example:

- Sysinternals Process Monitor.

Process Monitor can capture:

- filesystem;
- registry;
- network;
- process activity.

Filters can focus on:

- malware process;
- child processes.

### Рисунок 102. Process Monitor Dynamic Analysis Example

THIRD_PARTY_REVIEW_REQUIRED — product screenshot not reproduced.

## Automated Sandboxes

Examples in source:

- Hybrid Analysis;
- Joe Sandbox.

Automated sandboxes:

- execute samples in instrumented environment;
- report file changes;
- registry changes;
- process tree;
- network indicators.

For known malware families, sandbox report may provide enough eradication insight without manual reverse engineering.

## Practical Limitations

Basic analysis may be insufficient for:

**Heavy packing/obfuscation**

- strings unreadable;
- encrypted/compressed sections;
- specialized unpacking required.

**Anti-analysis**

Malware may detect:

- VM;
- debugger;
- sandbox.

It may refuse to execute or alter behavior.

**Kernel-mode rootkits**

Require:

- kernel debugging;
- specialist tooling;
- deeper expertise.

**Cryptographic analysis**

Ransomware decryptability may require:

- reverse engineering;
- cryptographic expertise.

Source recommends engaging specialized resources when needed:

- internal malware-research team;
- MSSP;
- external forensic consultant;
- IR retainer.

Signals favoring escalation:

- sample absent from VirusTotal/community corpus;
- heavy packing/obfuscation;
- internal team not making progress.

Waiting several days before calling specialist may cost more than early escalation.

Goal remains practical:

- what malware creates;
- persistence location;
- removal requirements;
- new IOC for scoping.

# Business Email Compromise Investigation

BEC uses legitimate identity/email mechanisms rather than conventional malware persistence.

Typical attacker mechanisms:

- stolen credentials;
- forwarding rules;
- OAuth grants;
- legacy protocol access;
- token reuse.

Source cites more than **$55 billion** in BEC losses since 2013.[12]

BEC actors often research:

- org structure;
- finance roles;
- executives;
- attorneys;
- payment authorities;
- communication patterns.

Cloud identity/mail systems hold most useful artifacts.

Investigation needs to determine:

- initial access;
- mailbox changes;
- OAuth/app persistence;
- fraud activity;
- affected accounts;
- financial transactions.

# Email System Investigation

Inspect mailbox rules and forwarding.

BEC attackers may create rules to:

- forward inbound email externally;
- delete selected mail;
- move messages into obscure folders;
- suppress security alerts;
- hide responses from fraud targets.

### Listing 77. Enumerating Inbox Rules for BEC Investigation

~~~powershell
PS C:\> Get-InboxRule -Mailbox "jwalcott@falsimentis.com" |
  Select-Object Name, Description, Enabled, ForwardTo, DeleteMessage, MoveToFolder |
  Format-List

Name          : Daily Reports
Description   : Move daily reports to Reports folder
Enabled       : True
ForwardTo     :
DeleteMessage : False
MoveToFolder  : Reports

Name          : auto-archive
Description   :
Enabled       : True
ForwardTo     : dxvpflrcdhquzyixdn@midnitemeerkats.com
DeleteMessage : True
MoveToFolder  :
~~~

Suspicious rule:

- forwards externally;
- deletes original message.

If attacker had administrative access, also inspect:

- organization-wide transport rules;
- mail-flow rules;
- security-notification suppression;
- domain bypass rules.

## SUBLIME EML ANALYZER

Source highlights Sublime EML Analyzer as free message-analysis tool.

It can:

- parse raw EML;
- apply Sublime Core Feed rules;
- identify phishing;
- detect spoofing;
- detect malicious attachments;
- identify social-engineering patterns.

### Рисунок 103. Sublime EML Analyzer Message Analysis Sample

THIRD_PARTY_REVIEW_REQUIRED — screenshot not reproduced.

Value:

- speed;
- broad rule coverage;
- prioritized severity;
- timeline support;
- reduced manual header/URL analysis.

# Identity and Access Investigation

OAuth consent phishing can create persistence independent of password.

A malicious application may retain access after:

- password reset;
- session cleanup.

For Microsoft 365 source references Microsoft's `Get-AzureADPSPermissions.ps1`.[13]

### Listing 78. Enumerate Delegated Permissions in Microsoft Entra

~~~powershell
PS C:\IR> .\Get-AzureADPSPermissions.ps1
Connecting to Microsoft Graph…
Retrieving OAuth2PermissionGrants…
Exporting results to .\Permissions.csv

PS C:\IR> Get-Item .\Permissions.csv

    Directory: C:\IR

Mode                 LastWriteTime         Length Name
----                 -------------         ------ ----
-a---         11/28/2025  10:13 AM         24576 Permissions.csv
~~~

### Listing 79. Review Delegated Permissions in Microsoft Entra

~~~text
PS C:\IR> Import-Csv .\Permissions.csv
[...]

TenantId           : 7f3e74e1-3855-4d44-a3db-5f3f9b37a1f9
UserDisplayName    : Lukas Dolman
UserPrincipalName  : ldolman@falsimentis.com
UserObjectId       : ecb20947-41fd-47c3-b27a-31c88a0e2a69
ClientAppId        : 7486f14b-2bc5-42f8-87bd-a2d1b5725db6
ClientName         : Power BI Reports Viewer
Permission         : Calendars.Read, Calendars.Read.Shared
ConsentType        : Principal
ConsentCreatedDate : 2024-05-09T16:22:54Z

TenantId           : 7f3e74e1-3855-4d44-a3db-5f3f9b37a1f9
UserDisplayName    : <tenant-wide>
UserPrincipalName  : <tenant-wide>
UserObjectId       : 00000000-0000-0000-0000-000000000000
ClientAppId        : 67c06044-2e2d-4cae-91e3-32ba827ac202
ClientName         : SecureSync Data Connector
Permission         : email, offline_access, Mail.ReadWrite, Mail.Send, Files.ReadWrite.All
ConsentType        : AllPrincipals
ConsentCreatedDate : 2025-11-26T03:41:09Z
~~~

High-risk permissions include:

- `email`;
- `Mail.ReadWrite`;
- `Mail.Send`;
- `MailboxSettings.ReadWrite`;
- `Files.ReadWrite.All`;
- `offline_access`.

Review apps granted during compromise window.

Also investigate mailbox delegation:

- Full Access;
- Send As;
- delegated mailbox permissions.

Commands:

- `Get-MailboxPermission`;
- `Get-RecipientPermission`.

These permissions survive password reset until explicitly revoked.

# Financial Transaction Investigation

Coordinate with finance/accounting.

Review transactions initiated during compromise window:

- wire transfers;
- invoice payments;
- vendor bank-account changes.

BEC attackers may monitor for weeks before acting during:

- payment periods;
- quarter-end;
- high workload.

## Sign-In Analysis

Review:

- impossible travel;
- unusual geolocation;
- unusual IPs;
- same attacker IP across multiple accounts.

### Listing 80. Analyzing Sign-In Locations from Exported Logs

~~~powershell
PS C:\IR> $signins = Get-Content .\SignInLogs.json | ConvertFrom-Json

PS C:\IR> $signins |
  Select-Object userPrincipalName, createdDateTime,
    @{Name='Location';Expression={"$($.location.city), $($.location.state)"}},
    ipAddress |
  Sort-Object userPrincipalName, createdDateTime |
  Format-Table

userPrincipalName        createdDateTime          Location           ipAddress
-----------------        ---------------          --------           ---------
ldolman@falsimentis.com  11/26/2025 3:35:25 AM   Ashburn, Virginia  44.206.5.255
ldolman@falsimentis.com  11/26/2025 3:37:10 AM   Ashburn, Virginia  3.216.143.186
ldolman@falsimentis.com  11/26/2025 3:38:14 AM   Columbus, Ohio     3.12.218.40
ldolman@falsimentis.com  11/26/2025 3:39:18 AM   Ashburn, Virginia  44.220.31.71
ldolman@falsimentis.com  11/26/2025 3:40:22 AM   Columbus, Ohio     3.145.230.62
[...]
~~~

Alternation between Virginia and Ohio over minutes is impossible physical travel and supports credential-compromise hypothesis.

# Victim by Proxy

Not every BEC incident means victim organization itself was compromised.

Common pattern:

1. supplier mailbox compromised;
2. attacker joins existing payment thread;
3. victim receives convincing payment-change instruction;
4. victim sends funds to fraudulent account;
5. real supplier later asks about unpaid invoice.

### Рисунок 104. Victim-by-Proxy BEC Scenario

THIRD_PARTY_REVIEW_REQUIRED — visual not reproduced.

Victim organization may have no local compromise evidence.

Available evidence may be only:

- received email;
- payment records;
- data supplier shares.

Source recommends three focus areas.

## Email Header and Content Analysis

Check:

- lookalike domain substitutions;
- Reply-To divergence;
- sender-domain anomalies.

Example lookalikes from source:

- `wehost4every1.com`;
- `wehost4evrey1.com`.

## Domain Registration Timing

WHOIS can show newly registered lookalike domains.

A domain registered shortly before first suspicious email supports staged BEC hypothesis.

Attackers may also register victim lookalike domain after receiving payment to intercept supplier follow-up and delay discovery.

## Information Flow Analysis

Ask whether attacker introduced genuinely new supplier information or mostly replayed information already present in thread.

A legitimate supplier may provide new invoice/payment details unavailable to victim previously.

A thread hijacker may mirror known details with plausible filler.

### Supplier-Mailbox Compromise Limitation

If attacker operates from supplier's legitimate mailbox:

- same mail server;
- valid SPF;
- valid DKIM;
- matching user agent;
- consistent headers.

Victim may have no technical basis to distinguish fraudulent from legitimate supplier mail.

That consistency itself supports request for supplier-side investigation.

Coordinate with supplier security team if possible.

But victim should not delay recovery while commercial liability is disputed.

Source recommends rapid coordination with:

- law enforcement;
- receiving bank.

Funds recovery probability drops sharply after first **72 hours**, as money may be moved through layered transfers.

# Insider Threat Investigation

Insider-threat investigation differs from external-attacker investigation because subject often has legitimate access.

Main challenge:

- distinguish authorized use from malicious/unauthorized behavior.

Investigation should focus on three primary areas.

## 1. Data Access Patterns

Review:

- data-access logs;
- application access;
- cloud storage activity.

Questions:

- what data was accessed?
- was volume unusual?
- was data downloaded/transferred outside normal pattern?
- were sensitive repositories accessed without business need?

## 2. Privilege Changes

Review:

- user-account changes;
- group membership;
- permission grants;
- role changes;
- elevation events.

Goal: identify deliberate privilege expansion.

## 3. Exfiltration Methods

Review:

- email;
- cloud uploads;
- USB device connections;
- data-loss alerts;
- external transfers.

Sophisticated insiders may establish persistence before primary credential revocation.

Look for:

- remote-access tools;
- secondary accounts;
- modified configurations;
- alternate access paths.

Documentation is especially important because insider cases often become legal matters.

Maintain detailed records of:

- authorized vs unauthorized activity;
- accessed data;
- exfiltration;
- account changes;
- timeline;
- evidence sources.

Coordinate with:

- HR;
- legal;
- leadership.

## INSIDER THREAT FROM DAY ONE: KNOWBE4'S NORTH KOREAN IT WORKER

Source discusses KnowBe4's July 2024 disclosure involving a North Korean threat actor posing as a remote IT worker.[14]

According to source:

- candidate passed four video interviews;
- used an AI-enhanced identity image;
- passed background checks with stolen U.S. identity;
- provided references.

### Рисунок 105. Stock Photo and AI Fake Used by North Korean Threat Actor

THIRD_PARTY_REVIEW_REQUIRED — visual not reproduced.

Company-issued workstation was sent to a U.S. address.

Source says an accomplice connected it through a Raspberry Pi, enabling remote access from the threat actor's actual location.

KnowBe4 SOC detected anomalous behavior shortly after hire.

`THIRD_PARTY_REVIEW_REQUIRED` — source's direct quoted incident statement is not reproduced verbatim.

Subsequent suspicious behavior included:

- manipulated session history;
- harmful file transfer;
- unauthorized software execution attempts.

KnowBe4 terminated access and investigated.

Source reports no company data compromise due to restricted new-hire access.

Case lesson:

- insider risk can begin immediately;
- least privilege limits blast radius;
- robust monitoring matters;
- rapid containment matters.

# Supplier and Supply Chain Investigation

Supply-chain incidents are difficult because malicious access/code may arrive through trusted channels.

Eradication must address both:

- local artifacts/access;
- broader supplier/ecosystem implications.

Source defines four categories:

1. hardware supply-chain attack;
2. software supply-chain compromise;
3. SaaS vendor compromise;
4. managed-service-provider/staff-access compromise.

# Software Supply Chain Compromises

Software supply-chain compromise affects software run in organization's environment.

Two major subtypes:

## Boundary Software

Examples:

- firewalls;
- VPN concentrators;
- remote-access gateways;
- edge appliances.

Risks:

- attacker gains privileged network position;
- security device itself may be compromised;
- detection telemetry may be untrustworthy.

## Internal Software

Examples:

- libraries;
- data-center appliances;
- internal applications;
- developer toolchains.

Attackers may still need lateral movement after initial software compromise.

Dependency breadth makes investigation difficult.

Log4j is cited as example of broad supply-chain/search-surface risk.

## Investigation Approach

Start by identifying all systems with compromised version.

Review:

- deployment logs;
- package-manager history;
- endpoint-management inventory.

Then analyze malicious code to identify:

- capabilities;
- artifacts;
- persistence;
- lateral-movement potential.

Coordinate with vendor for:

- version-specific IOC;
- compromise window;
- advisory data.

Threat-intelligence community may publish IOC quickly for widespread incidents.

## 2025 NPM / Shai-Hulud Example

Source references GitLab Vulnerability Research Team research into multiple compromised NPM packages distributing Shai-Hulud malware.[15]

### Таблица 26. GitLab NPM Supply Chain Compromise IOCs

| Type | Indicator | Description |
|---|---|---|
| File | `bun_environment.js` | malicious post-install script in node_modules |
| Directory | `.truffler-cache/` | hidden home directory for Trufflehog binary |
| Directory | `.truffler-cache/extract/` | temp extraction directory |
| File | `.truffler-cache/trufflehog` | downloaded Trufflehog binary, Linux/macOS |
| File | `.truffler-cache/trufflehog.exe` | downloaded Trufflehog binary, Windows |
| Process | `del /F /Q /S "%USERPROFILE%"` | Windows destructive payload indicator |
| Process | `shred -uvz -n 1` | Linux/macOS destructive payload indicator |
| Process | `cipher /W:%USERPROFILE%` | Windows secure-deletion payload indicator |
| Command | `curl -fsSL https://bun.sh/install | bash` | suspicious Bun installation during package install |
| Command | `powershell -c "irm bun.sh/install.ps1|iex"` | Windows Bun installation via PowerShell |

These strings are preserved as detection indicators from canonical source, not as recommended operational actions.

Use CTI/malware-analysis tools to expand IOC set.

Supply-chain malware goals may include:

- financial/crypto theft;
- persistence;
- data exfiltration;
- hacktivism.

If supply-chain payload supports remote access/persistence, investigate whether it was used as foothold for lateral movement.

Eradication may need to extend far beyond removing poisoned package.

## VENDOR BREACH ACCOUNTABILITY: MARQUIS V. SONICWALL

Source discusses litigation trend where downstream organizations pursue security vendors following vendor compromise.

It describes 2025 ransomware breach of Marquis and later SonicWall disclosure about stolen cloud-backup firewall configurations.[16]

Source says SonicWall initially communicated a much smaller affected-customer fraction before revising scope upward.

Marquis filed suit in February 2026 alleging delayed/incomplete vendor disclosure prevented timely mitigation.

`THIRD_PARTY_REVIEW_REQUIRED` — legal allegations remain source-attributed; no independent factual adjudication is asserted in translation.

Source also mentions:

- Barracuda-related litigation;
- ongoing MOVEit litigation.

IR lesson:

Document vendor interactions:

- disclosure timestamps;
- scope statements;
- changes in vendor claims;
- mitigation advice.

Vendor contracts should address:

- notification obligations;
- indemnification;
- security accountability.

# Hardware Supply Chain Attacks

Hardware compromise may involve physical modification during:

- manufacturing;
- shipping;
- maintenance.

Possible indicators:

- unexpected firmware;
- unauthorized components;
- unexplained hardware-level network behavior.

Software remediation may be insufficient.

Often require:

- physical inspection;
- hardware replacement;
- serial-number tracking;
- procurement-chain review;
- supplier coordination;
- law-enforcement coordination where appropriate.

## COUNTERFEIT CISCO EQUIPMENT IN MILITARY SYSTEMS

Source cites 2024 U.S. DOJ sentencing tied to long-running counterfeit network-equipment scheme.[17]

Counterfeit devices reportedly reached:

- hospitals;
- schools;
- government;
- military systems.

Security research analyzed counterfeit Cisco switches with hardware modifications bypassing Secure Boot protections.[18]

### Рисунок 106. Counterfeit Cisco WS-2960X-48TS-L V01 Switch with Hardware Modification

THIRD_PARTY_REVIEW_REQUIRED — third-party hardware image not reproduced.

Source notes analyzed implants were reportedly used to bypass authenticity controls/run pirated software, while similar techniques could theoretically support persistent hardware-level backdoor behavior.

# SaaS Vendor Compromises

In SaaS vendor compromise:

- vendor hosts application;
- organization data/tokens/integrations reside at vendor;
- local infrastructure may remain uncompromised.

Eradication focuses on:

- stop data flows;
- rotate credentials stored by vendor;
- revoke OAuth grants;
- audit downstream systems trusting vendor-held credentials/tokens.

Start by inventorying:

- data stored at vendor;
- OAuth tokens;
- API keys;
- service credentials;
- integration scope.

Work with vendor to obtain:

- timeline;
- IOC;
- affected data;
- token exposure details.

Then check own logs for:

- unexpected API calls;
- unusual token refreshes;
- automated enumeration;
- suspicious access timing.

Use NDA if necessary for detailed partner disclosure.

## SUPPLY CHAIN COMPROMISE: THE SALESLOFT DRIFT INCIDENT

Source discusses August 2025 compromise of Salesloft Drift, a marketing/chat platform with broad third-party integrations.[19]

According to source, attackers stole OAuth tokens enabling access to connected customer environments.

Google Threat Intelligence reportedly identified more than **700 potentially impacted organizations**.[20]

Attackers queried connected platforms and extracted:

- customer records;
- sales data;
- support data;
- stored credentials/secrets.

Source lists examples of stolen downstream credentials:

- AWS access keys;
- VPN credentials;
- Snowflake tokens;
- other secrets.

`THIRD_PARTY_REVIEW_REQUIRED` — direct quotation from Krebs on Security is not reproduced verbatim.[21]

Source says on August 20, 2025:

- Salesloft/Salesforce revoked active access and refresh tokens;
- Salesforce removed Drift from partner marketplace.

Affected organizations needed to:

- identify credentials stored in connected systems;
- rotate potentially exposed secrets;
- audit AWS/Azure and other downstream platforms;
- monitor extortion attempts.

Lesson:

> Integration chains amplify blast radius: one provider compromise may expose tokens to other platforms, which themselves contain credentials to further infrastructure.

Remediation:

- rotate all credentials stored with vendor;
- revoke vendor OAuth grants;
- assess whether data can safely remain at compromised provider.

# Managed Service Provider and Staff Access Compromises

This category covers vendors with legitimate access to organization.

Examples:

- outsourced IT;
- consultants;
- managed services;
- specialist admin engagements.

If vendor identity environment is compromised, their authorized access becomes attack path.

Investigation should identify all vendor access points:

- VPN;
- API;
- federation;
- shared infrastructure;
- vendor staff accounts.

Review authentication logs for:

- unexpected locations;
- abnormal times;
- activity during vendor compromise window.

Before declaring eradication complete:

- rotate vendor-held credentials;
- reissue tokens;
- reprovision accounts if needed;
- re-establish federation trust where appropriate.

Maintain coordination with compromised supplier.

They may provide:

- IOC;
- attacker behavior;
- compromise timeline;
- broader ecosystem findings.

Findings should be shared reciprocally where allowed.

# Cloud Investigation — Introduction

Cloud environments differ from traditional on-prem due to:

- ephemeral resources;
- IaC;
- distributed IAM;
- control-plane APIs.

Two broad incident categories:

- IaaS compromises;
- SaaS compromises.

For IaaS, investigation must distinguish:

1. cloud control plane;
2. infrastructure itself.

## Cloud Control Plane Investigation

Control plane includes:

- management APIs;
- IAM;
- configuration services.

Attacker with control-plane access may:

- create resources;
- change IAM;
- alter security groups;
- establish persistence surviving host rebuild.

Primary investigation methods:

- audit logs;
- differential analysis.

Provider logs:

- AWS CloudTrail;
- Azure Activity Log;
- GCP Cloud Audit Logs.

Search for:

- resource creation;
- IAM modifications;
- security-group changes;
- persistence-related API operations.

## Cloud Control Plane Investigation — Continued

Differential analysis compares deployed cloud state against known-good baseline.

For IaC environments, compare current deployment with source-controlled definitions:

- Terraform;
- CloudFormation;
- Pulumi.

Without IaC, compare against:

- architecture diagrams;
- previous configuration exports;
- pristine/reference environments.

Focus especially on:

- IAM policies;
- assume-role trusts;
- security groups;
- resource configurations.

## IAM Investigation

Attackers may:

- create new roles;
- modify policies;
- add principals to privileged groups;
- create cross-account trust;
- establish external persistence.

Review assume-role policies for unexpected principals.

### Listing 81. Enumerate AWS IAM Roles with AssumeRole Permissions

~~~bash
$ aws iam list-roles | jq -r '
        .Roles[]
        | .RoleName as $r
        | .AssumeRolePolicyDocument.Statement[]
        | select(.Effect=="Allow" and (.Action|tostring|contains("sts:AssumeRole")))
        | ($r), (.Principal | tojson), ""'

[...]

aws-elasticbeanstalk-ec2-role
{"Service":"ec2.amazonaws.com"}

survivorBingo-role-jv27lw38
{"Service":"lambda.amazonaws.com"}

survivorBingo-role-jv27lw38
{"AWS":"arn:aws:iam::013628954028:root"}
~~~

Interpretation:

- first entries show service principals;
- last entry allows assumption from external AWS account `013628954028`.

### Таблица 27. Cloud Role and Trust Enumeration Quick Reference

| Objective | AWS | Azure | GCP |
|---|---|---|---|
| List role assignments/permissions | `aws iam list-roles`; `aws iam list-attached-role-policies --role-name <role>` | `az role assignment list --all --query "[].{Principal:principalName, Role:roleDefinitionName, Scope:scope}"` | `gcloud projects get-iam-policy <project-id> --format=json` |
| Identify cross-account/cross-tenant trust | inspect `AssumeRolePolicyDocument` | `az ad sp list --query "[?appOwnerOrganizationId!='<tenant-id>']"` | inspect IAM policy for external service accounts |

Pay particular attention to roles allowed to modify IAM:

- `iam:PutRolePolicy`;
- `iam:AttachUserPolicy`;
- `iam:CreateRole`;
- `iam:UpdateAssumeRolePolicy`.

If attacker retains these permissions, they can continuously recreate persistence.

# Infrastructure Investigation

For cloud VMs/containers/storage/databases, use many of the same forensic concepts as on-prem systems, enhanced by cloud-native:

- snapshots;
- audit logs;
- image history;
- API metadata.

## VM and Container Images

Review recent image changes.

Attackers may modify:

- gold images;
- AMIs;
- container registry images;

so newly deployed instances inherit backdoors.

Compare against trusted baselines.

## Storage Access and Exfiltration

Review:

- S3;
- Azure Blob;
- Google Cloud Storage.

Questions:

- which objects were read?
- downloaded?
- permissions changed?
- buckets made public?
- high-volume exfiltration?

### Listing 82. AWS S3 Log Analysis with s3logparse.py

~~~text
$ s3logparse.py
s3logparse.py: Extract useful information from AWS S3 logs.
Usage: ./s3logparse.py [useragent|toptalkers|topuploaders|topdownloaders|topfiles] <log files>

$ s3logparse.py useragent ../mys3logs/* | cut -c 1-72
34140 - aws-cli/1.16.192 Python/2.7.10 Darwin/18.7.0 botocore/1.12.182
876 - Amazon CloudFront
222 - Cyberduck/7.1.1.31577 (Mac OS X/10.14.6) (x86_64)
69 - S3Console/0.4, aws-internal/3 aws-sdk-java/1.11.915 Linux/4.9.230-0
44 - S3Console/0.4, aws-internal/3 aws-sdk-java/1.11.991 Linux/5.4.109-5
[...]

$ s3logparse.py toptalkers ../mys3logs/*
20.43 GiB - 254.59.11.25
15.95 GiB - 253.252.70.185
13.80 GiB - 252.59.250.11
12.85 GiB - 251.252.12.173
12.81 GiB - 251.252.12.190
[...]
~~~

Interpretation:

- AWS CLI dominates accesses → scripted activity;
- top IP shows highest transfer volume.

## Serverless and Event-Driven Infrastructure

Review:

- recently created/modified functions;
- code changes;
- trigger sources;
- IAM roles;
- excessive privileges.

Malicious serverless functions can provide persistence without traditional host.

## Network Configuration

Review changes to:

- security groups;
- NACLs;
- firewall rules;
- VPC peering;
- VPN;
- transit gateways.

These may enable:

- external access;
- lateral movement;
- C2;
- pivot to on-prem.

# SaaS Investigation and Eradication

SaaS compromises often involve:

- account takeover;
- OAuth abuse;
- application-level privileges;
- API token persistence.

Major limitation:

- customer lacks underlying host access;
- cannot take disk/memory images;
- native logs may be limited.

Start by identifying provider logging capabilities.

Major platforms:

- Microsoft 365;
- Google Workspace;
- Salesforce.

Smaller platforms may require support case for logs.

Request:

- access logs;
- activity reports;
- compromise-period telemetry;
- any non-default/provider-internal logging available.

## Integration-Side Logs

Even when SaaS logs are weak, own infrastructure may retain evidence through:

- IdP;
- API gateway;
- SIEM;
- middleware;
- custom integration services;
- webhooks.

## SaaS Privilege Enumeration

Review:

- newly created admins;
- role elevation;
- API keys;
- OAuth grants;
- third-party apps;
- suspicious high-scope consent.

# MIDNIGHT BLIZZARD OAUTH CAMPAIGN

Source discusses Microsoft's January 2024 disclosure involving Midnight Blizzard/NOBELIUM, described as Russian state-sponsored actor.[23]

According to source:

- initial access involved password spray against legacy non-production tenant account without MFA;
- attackers reached legacy test OAuth application with elevated permissions;
- obtained Microsoft Graph API scopes including:
  - `Directory.ReadWrite.All`;
  - `RoleManagement.ReadWrite.Directory`;
  - `Application.ReadWrite.All`;
  - `AppRoleAssignment.ReadWrite.All`.[24]

### Рисунок 107. Microsoft Legacy Test Application

THIRD_PARTY_REVIEW_REQUIRED — screenshot/diagram not reproduced.

Source says attackers then:

- created new user;
- granted Global Administrator;
- created malicious OAuth applications;
- granted broad app permissions including `full_access_as_app`;
- accessed Exchange Online mailboxes.

Lesson:

Password reset alone does not eradicate OAuth-based persistence.

Required actions include:

- enumerate OAuth apps;
- identify apps created/modified in attack window;
- inspect high-privilege consent;
- revoke malicious apps;
- remove attacker-created accounts;
- audit service-principal credentials.

# ERADICATE ATTACKER ACCESS

After sufficient investigation for current loop iteration, team transitions from understanding to removal.

Major eradication categories:

- persistence removal;
- account/access remediation;
- credential rotation;
- system restoration;
- vulnerability remediation;
- defense-in-depth.

### Рисунок 108. Eradicate Attacker Access Process

THIRD_PARTY_REVIEW_REQUIRED — visual not reproduced.

# Removing Persistence Mechanisms

Use systematic process.

## Build Persistence Inventory

For every mechanism document:

- type;
- affected system;
- file path / registry key;
- process/service;
- hash;
- configuration;
- evidence/screenshot where appropriate.

Documentation before removal supports:

- IOC creation;
- legal evidence;
- post-incident review.

## Plan Removal Sequence

Identify dependencies.

Some malware uses watchdog processes that recreate removed component.

Sequence:

1. remove/disable watchdog;
2. remove protected persistence;
3. verify;
4. monitor reappearance.

## Verify Immediately

Re-run same enumeration used during investigation.

Previously malicious locations should now be clean.

Any remaining artifact means incomplete eradication.

Continue monitoring after removal.

Reappearance can mean:

- missed component;
- hidden malicious process;
- reinfection from still-open vector.

# Windows Persistence Removal Considerations

Common locations:

- registry Run keys;
- scheduled tasks;
- services;
- WMI event subscriptions;
- startup folders;
- other autorun points.

Sysinternals Autoruns provides centralized enumeration.

### Рисунок 109. Sysinternals Autoruns Persistence Enumeration

THIRD_PARTY_REVIEW_REQUIRED — product screenshot not reproduced.

Before removal, export results.

Autoruns GUI can save `.arn`; command-line `autorunsc.exe` can generate CSV.

### Listing 83. Exporting Autoruns CSV Results for Analysis

~~~powershell
PS C:\Users\ttidmas> C:\tools\Sysinternals\autorunsc.exe -nobanner -c -o autoruns-ws1-ttidmas-20251201.txt

PS C:\Users\ttidmas> Get-Content .\autoruns-ws1-ttidmas-20251201.txt | Select-Object -First 4

Time,Entry Location,Entry,Enabled,Category,Profile,Description,Company,Image Path,Version,Launch String
12/7/2019 9:15 AM,HKLM\System\CurrentControlSet\Control\Terminal Server\Wds\rdpwd\StartupPrograms,,,"Logon",System-wide,,,,,,
1/26/2007 2:00 AM,"HKLM\System\CurrentControlSet\Control\Terminal Server\Wds\rdpwd\StartupPrograms","rdpclip",enabled,"Logon",System-wide,"RDP Clipboard Monitor","Microsoft Corporation","c:\windows\system32\rdpclip.exe",10.0.19041.746,"rdpclip"
11/30/2025 1:49 PM,HKLM\SOFTWARE\Microsoft\Windows NT\CurrentVersion\Winlogon\Userinit,,,"Logon",System-wide,,,,,,
~~~

Compare against clean same-configuration baseline.

### Listing 84. Removing a Malicious Windows Service

~~~powershell
PS C:\> Get-Service "Evast Updater"

Status   Name               DisplayName
------   ----               -----------
Running  Evast Updater      fznRlhbehmol

PS C:\> Set-Service -Name "Evast Updater" -StartupType Disabled
PS C:\> Stop-Service "Evast Updater" -Force
PS C:\> sc.exe delete "Evast Updater"
[SC] DeleteService SUCCESS

PS C:\> Get-Service "Evast Updater" -ErrorAction SilentlyContinue
PS C:\>
~~~

Sequence:

1. disable service;
2. stop service;
3. delete service registration;
4. verify no result.

Using `sc.exe delete` supports older Windows versions where `Remove-Service` may not be available.

Same systematic pattern applies to other Windows persistence types.

# Linux Persistence Removal Considerations

Linux persistence differs from Windows, but eradication workflow is the same:

1. use investigation inventory;
2. remove every identified mechanism;
3. verify;
4. monitor recurrence.

Source recommends performing comprehensive enumeration/removal with root privileges where appropriate.

### Таблица 28. Linux Persistence Types and Removal Methods

| Persistence type | Removal method |
|---|---|
| At jobs | `atq`; remove with `atrm <job_number>` |
| Cron jobs | remove malicious entries via `crontab` or system cron files |
| Git hooks | remove/sanitize scripts in `.git/hooks/` |
| Library hijacking | remove malicious `/etc/ld.so.preload`; inspect `LD_PRELOAD` |
| Malicious kernel modules | unload with `rmmod` / `modprobe -r`; remove `.ko`; clean module-load configs |
| PAM backdoors | restore legitimate modules in `/etc/pam.d/`, `/lib/security/` |
| Package-manager hooks | clean `/etc/apt/apt.conf.d/`, `/etc/yum/pluginconf.d/` |
| SSH authorized keys | remove unauthorized keys from each user's `~/.ssh/authorized_keys` |
| Sudo configuration | review `sudo -l`; remove unauthorized entries via `visudo` |
| SUID/SGID binaries | remove binary or clear bits with `chmod u-s` / `chmod g-s` |
| Shell RC/profile files | remove malicious entries from `.bashrc`, `.bash_profile`, `/etc/profile`, `/etc/profile.d/*` |
| systemd services | stop, disable, remove unit files |
| udev rules | remove malicious rules; reload with `udevadm control --reload` |

Verification should repeat enumeration and inspect relevant configuration directories.

# Web Shell Removal

Web shells provide interactive access to web servers.

Eradication must remove:

- shell file;
- related configuration;
- supporting logs/artifacts if malicious;
- redundant copies.

Web shell may exist as:

- standalone file;
- embedded code;
- application plugin/module;
- server configuration.

### Listing 85. Standalone Web Shell Backdoor File

Canonical source contains a simple PHP web shell that executes a `cmd` GET parameter.

`THIRD_PARTY_REVIEW_REQUIRED` — executable web-shell code is not duplicated in the reader-facing translation; filename, behavior, removal logic, and forensic significance are retained. Canonical English RAG remains source of truth for verbatim code.

Source path:

`/var/www/html/imgupload.html`

Behavior:

- reads `cmd` query parameter;
- executes it through PHP system execution.

Eradication:

- preserve evidence first;
- remove file;
- search for duplicates/related shells;
- validate application integrity.

### Listing 86. Obfuscated Web Shell Embedded in HTML File

Canonical source contains obfuscated PHP embedded in `index.html`.

`THIRD_PARTY_REVIEW_REQUIRED` — obfuscated executable backdoor payload is not reproduced verbatim.

Eradication challenge:

- file may be legitimate application file;
- only injected PHP portion may be malicious.

Need:

- compare against known-good source/version control;
- remove malicious modification;
- retain legitimate application content.

### Listing 87. Web Shell via Configuration Modification

Canonical source shows PHP `auto_prepend_file` loading a backdoor script for every request.

Relevant configuration:

`auto_prepend_file = /etc/php7/runmeconfig.php`

`THIRD_PARTY_REVIEW_REQUIRED` — executable PHP backdoor body is not duplicated verbatim.

Eradication requires:

- revert PHP config;
- remove malicious script;
- restart web server;
- verify no in-memory persistence;
- review application code/plugins/modules for additional shells.

Web shells can exist at both:

- web-server layer;
- web-application layer.

# Cloud Persistence Removal

Cloud persistence can exist without traditional host startup mechanism.

Investigation should identify:

- unauthorized serverless functions;
- IAM changes;
- malicious images;
- event triggers;
- access keys;
- cross-account trusts.

## Lambda / Serverless Functions

Delete malicious functions and associated triggers.

### Таблица 29. Removing Malicious Serverless Functions

| Provider | Removal command |
|---|---|
| AWS | `aws lambda delete-function --function-name MaliciousFunction` |
| Azure | `az functionapp delete --name MaliciousFunctionApp --resource-group ResourceGroup` |
| GCP | `gcloud functions delete malicious-function --region us-central1` |

After deletion, verify via:

- CloudTrail;
- Azure Activity Log;
- GCP Cloud Audit Logs.

Also remove associated triggers:

- API Gateway;
- S3 event notifications;
- CloudWatch/EventBridge rules;
- equivalent event sources.

# IAM Policy Modifications

IAM persistence grants access rather than running code.

It can survive credential rotation.

Eradication:

- compare IAM against baseline/IaC;
- remove unauthorized users;
- remove unauthorized service principals;
- revoke unexpected admin grants;
- revert policy modifications;
- rotate compromised access keys.

# Container Image Modifications

Modified container images can persist across:

- container restarts;
- autoscaling;
- cluster redeployment.

Actions:

- remove manipulated images from local hosts;
- remove from registries;
- redeploy workloads from known-good images;
- review CI/CD pipeline;
- validate trusted base images/build path.

# Account and Identity Remediation

Identity remediation removes authentication/authorization paths that survive host cleanup.

Modern compromise may require changes across:

- local accounts;
- Active Directory;
- federation;
- Entra ID;
- SaaS;
- cloud IAM.

This should be structured, not ad hoc.

Any replacement/temporary accounts created during remediation must be documented with:

- purpose;
- owner;
- intended lifespan.

Closure should review them for removal/retention.

# Local Account and Credential Remediation

Attackers may create local accounts for persistence.

Before removal:

> Always verify account is not legitimately required.

### Listing 88. Removing Unauthorized Local Windows Account

~~~powershell
PS C:\WINDOWS\system32> Get-LocalUser EVASTUtilityAccount

Name                Enabled Description
----                ------- -----------
EVASTUtilityAccount True

PS C:\WINDOWS\system32> Get-LocalUser EVASTUtilityAccount | Remove-LocalUser

PS C:\WINDOWS\system32> Get-LocalUser EVASTUtilityAccount -ErrorAction SilentlyContinue
PS C:\>
~~~

Verification returns no result.

### Listing 89. Removing Unauthorized Local Linux Account

~~~bash
$ grep apache2 /etc/passwd
apache2:x:1000:1000:Apache Service Account,,,:/home/apache2:/bin/bash

$ sudo userdel -r apache2
userdel: apache2 mail spool (/var/mail/apache2) not found

$ grep apache2 /etc/passwd
$
~~~

`-r` removes:

- account;
- home directory;
- mail spool where present.

Evidence from home directory should be preserved during Contain before destructive account removal.

# Active Directory Account and Credential Remediation

AD compromise may expose cryptographic materials allowing attacker to:

- forge auth tokens;
- persist across password reset;
- reuse multiple authorization paths.

Simple mass reset is insufficient for serious AD compromise.

Source recommends phased resets based on privilege tiers.

Microsoft tier model:[25]

- **Tier 0:** domain/enterprise/schema admins;
- **Tier 1:** server/application admins;
- **Tier 2:** workstation users.

## Phase 1: Privileged Account Reset

Reset Tier 0/Tier 1 first.

Priority includes:

- built-in Administrator;
- Domain Admins;
- Enterprise Admins;
- Schema Admins;
- Backup Operators/equivalent effective admins;
- AD FS service accounts;
- Entra Connect;
- certificate services;
- nested/delegated effective domain-admin accounts.

Also reduce privileged group membership to minimum required.

### Listing 90. Eradicate Unauthorized Domain Admin Group Membership

~~~powershell
PS C:\> Remove-ADGroupMember -Identity "Domain Admins" -Members "ttidmas" -Confirm:$false

PS C:\> $cred = Get-Credential "CORP\ttidmas"

PS C:\> Set-ADAccountPassword -Identity "ttidmas" -Reset -NewPassword $cred.Password

PS C:\> Set-ADUser -Identity "ttidmas" -ChangePasswordAtLogon $true
~~~

# ACCOUNT RECREATION VS. PASSWORD RESET FOR SEVERE COMPROMISES

For severe AD compromise involving:

- domain-controller access;
- DCSync;
- long undetected dwell;

source cites Microsoft guidance favoring **new privileged accounts** instead of only password reset.[26]

Reason:

existing account object itself may be modified:

- SPNs;
- account attributes;
- SID-linked persistence;
- delegated rights.

Recommended pattern:

1. create new Tier 0 accounts;
2. verify functionality;
3. disable, not delete, old accounts;
4. move old accounts to quarantine OU;
5. preserve them for forensic analysis.

### Рисунок 110. Microsoft's Account Recreation Approach

THIRD_PARTY_REVIEW_REQUIRED — visual not reproduced.

Disadvantages:

- application dependencies;
- group membership recreation;
- delegated permissions;
- hardcoded SIDs;
- operational complexity.

Account recreation is most appropriate when:

- attacker likely modified directory objects;
- domain-controller access occurred;
- organization cannot confidently bound attacker activity.

For credential theft without DC compromise, password reset + krbtgt rotation may be sufficient.

# Phase 2: Service Account and Identity Infrastructure Reset

Reset:

- directory-sync accounts;
- CA service accounts;
- database service accounts;
- application service accounts;
- accounts that authenticated to compromised systems.

Coordinate with application owners before cutover.

Pay particular attention to:

- Entra Connect;
- AD FS;
- AD CS;
- federation/identity-bridge accounts.

# Phase 3: General User Reset

After privileged/service accounts:

- reset targeted high-risk users;
- then general user population.

Plan helpdesk/support impact.

Where appropriate use SSPR with strong identity proofing.

Communicate schedule in advance.

But password reset alone does **not** revoke:

- existing sessions;
- pre-issued tokens.

Additional cryptographic-root/session/hybrid remediation is required.

# Krbtgt Account Reset — Introduction

`krbtgt` is Kerberos cryptographic root of trust in AD.

If attacker obtains krbtgt hash, they can forge Golden Tickets.[27]

User password resets do not invalidate forged tickets.

When investigation indicates:

- DC compromise;
- DCSync;
- krbtgt hash theft;

reset `krbtgt` **twice**, with appropriate replication delay.

# Krbtgt Account Reset

The krbtgt account keeps password history of two keys.

Therefore:

- first reset invalidates tickets signed with oldest stored key;
- second reset invalidates tickets signed with key current at compromise time.

### Listing 91. Resetting the krbtgt Account Password

~~~powershell
PS C:\> Set-ADAccountPassword -Identity krbtgt -Reset -NewPassword (ConvertTo-SecureString -AsPlainText "initialresetpassword" -Force)

PS C:\> repadmin /replsum

Replication Summary Start: 2025-12-14 09:32:10

 Source DSA          largest delta    fails/total    %%   error
 FM-SRV-DC01          00h:12m:33s        0 /   12     0
 FM-SRV-FS01          00h:10m:51s        0 /   12     0
 FM-NET-FW01          00h:09m:14s        0 /   12     0

 Destination DSA     largest delta    fails/total    %%   error
 FM-SRV-DC01          00h:12m:33s        0 /   12     0
 FM-SRV-FS01          00h:10m:51s        0 /   12     0
 FM-NET-FW01          00h:09m:14s        0 /   12     0

Replication Summary End: 2025-12-14 09:32:12
~~~

Source notes supplied password value is not operationally significant because AD generates strong internal key independently.

Wait at least maximum Kerberos ticket lifetime between reset 1 and reset 2.

Default cited by source: 10 hours.

Operationally, longer delay such as 24–48 hours may accommodate offline systems returning and receiving replication.

After each reset, repadmin /replsum must confirm healthy replication before proceeding.

Incomplete replication can cause authentication failures against DCs with inconsistent krbtgt keys.

## Multi-Domain Forest Considerations

Each domain has its own krbtgt.

Source recommends:

- child domains before parent domains;
- two resets per domain;
- appropriate delay;
- replication verification each time.

# Domain Controller Machine Account Reset

DCs authenticate to each other with machine-account passwords.

If attacker compromised DC, those machine credentials may also be exposed.

After krbtgt reset, reset DC machine account passwords individually.

### Listing 92. Resetting Domain Controller Machine Account Password

~~~powershell
PS C:\> netdom resetpwd /server:FM-SRV-DC01 /userd:FALSIMENTIS\Administrator /passwordd:*
Type the password associated with the domain user: ************

The machine account password for the local machine has been successfully reset.
The command completed successfully.
~~~

/passwordd:* prompts interactively and avoids exposing password in command line.

Execute on each domain controller, using another DC as target server.

Allow replication between resets because DC machine accounts also maintain limited password history.

# Trust Password Reset

If incident affects inter-domain/inter-forest trust:

- re-establish control over DCs;
- complete krbtgt resets;
- then reset trust passwords.

Trust password protects authentication channel between domains/forests.

If compromised, attacker may persist across trusted environment boundaries.

Reset trust password on trusting side of each affected trust relationship.

# Disabling Unconstrained Delegation

Unconstrained delegation allows service to:

- impersonate authenticating users;
- cache Kerberos tickets;
- reuse them later.

Compromise of unconstrained-delegation host can expose privileged tickets.

Identify computer/user objects with delegation enabled.

### Listing 93. Identifying Unconstrained Delegation in Active Directory

~~~powershell
PS C:\> Get-ADComputer -Filter {TrustedForDelegation -eq $true} -Properties TrustedForDelegation

Name          DNSHostName                    TrustedForDelegation
----          -----------                    --------------------
FM-SRV-DC01   FM-SRV-DC01.falsimentis.local  True
FM-SRV-FS01   FM-SRV-FS01.falsimentis.local  True
FM-WEBDEV     FM-WEBDEV.falsimentis.local    True

PS C:\> Get-ADUser -Filter {TrustedForDelegation -eq $true} -Properties TrustedForDelegation

DistinguishedName                              SamAccountName
-----------------                              --------------
CN=svcWebKrb,CN=Users,DC=falsimentis,DC=local  svcWebKrb
~~~

Disable where unnecessary.

### Listing 94. Disabling Unconstrained Delegation

~~~powershell
PS C:\> Set-ADComputer -Identity "FM-WEBDEV" -TrustedForDelegation $false

PS C:\> Set-ADUser -Identity "svcwebkrb" -TrustedForDelegation $false
~~~

Where delegation required, source recommends constrained delegation or resource-based constrained delegation.[28]

These reduce services to which credentials can be delegated.

# Hybrid and Entra ID Remediation

Hybrid AD + Entra adds cross-environment remediation requirements.

On-prem password reset alone does not terminate cloud sessions.

Compromise may persist in:

- Entra tokens;
- synchronized identities;
- OAuth grants;
- federation configuration.

Goal:

- on-prem credential reset;
- cloud session revocation;
- conditional access;
- sync/federation validation.

# Entra ID Session and Token Revocation

Revoke all refresh tokens and active sessions for compromised users.

Password reset alone is insufficient.

### Listing 95. Revoke Entra ID User Sessions

~~~powershell
PS C:\> Connect-MgGraph -Scopes "User.ReadWrite.All"
Welcome To Microsoft Graph!

PS C:\> Revoke-MgUserSignInSession -UserId "ttidmas@falsimentis.com"

Id                                   DisplayName   UserPrincipalName
--                                   -----------   -----------------
d13a91fb-4b4c-43c8-9034-3ae8947c3121 Tamra Tidmas ttidmas@falsimentis.com
~~~

Equivalent admin-center workflow:

Identity → Users → select user → Revoke sessions.

If attacker may still perform SSPR or MFA challenge, disable account.

### Listing 96. Disable Entra ID User Account

~~~powershell
PS C:\> Update-MgUser -UserId "ttidmas@falsimentis.com" -AccountEnabled:$false
~~~

Entra UI alternative:

Identity → Users → user → Properties → Block sign in = Yes.

## Back-Channel Logout

Some integrations support back-channel logout, allowing IdP to notify applications to terminate sessions.

Without support, app session may remain active until token expiry.

For those apps, manually terminate sessions via application admin interface.

# THE FOUR-MONTH ZOMBIE ACCOUNT

Source recounts a consultant anecdote about disabled account that continued functioning for approximately four months due to:

- unmanaged personal laptop;
- local admin rights;
- cached credentials;
- bypassing VPN enforcement;
- long-lived access tokens.[29]

THIRD_PARTY_REVIEW_REQUIRED — direct first-person quotations from third-party consultant are not reproduced verbatim.

Lesson:

Disabling account or changing password only affects future authentication.

It may not invalidate:

- cached credentials;
- active sessions;
- long-lived tokens.

Without session/token revocation, attacker may retain access long after organization believes access is gone.

# Entra Connect and Directory Synchronization

If Entra Connect or another sync service compromised:

- reset synchronization service account;
- review synchronization config;
- inspect inbound/outbound rules;
- check unauthorized synced objects;
- validate group changes;
- validate identity mappings.

Attackers controlling directory synchronization can:

- create cloud backdoors;
- modify group membership;
- propagate persistence.

Review via:

- Entra admin center;
- Synchronization Rules Editor on Entra Connect host.

# Session and Token Revocation

Modern authentication produces access paths independent of password:

- SSO sessions;
- browser cookies;
- refresh tokens;
- OAuth grants;
- PATs;
- API keys.

Comprehensive identity remediation requires revoking all active authorization materials.

For every IdP:

- revoke refresh tokens;
- revoke active sessions.

For apps without IdP logout support:

- terminate sessions manually.

Prioritize systems holding sensitive data or critical infrastructure.

Use application inventory from investigation to avoid omissions.

# OAuth Application and Consent Revocation

Malicious OAuth app can persist after password reset and session termination.

Review OAuth apps authorized by compromised accounts.

Focus on:

- broad mail access;
- file access;
- admin permissions;
- grants during compromise window.

Verify even legitimate-looking names against known app inventory.

Apply across IdPs and SaaS platforms.

GitHub example: unauthorized GitHub Apps can retain organization/repository API access.

### Рисунок 111. GitHub App Integration Example

THIRD_PARTY_REVIEW_REQUIRED — product UI screenshot not reproduced.

### Рисунок 112. GitHub App Integration Permissions and Access

THIRD_PARTY_REVIEW_REQUIRED.

# Personal Access Tokens and Long-Lived Credentials

PATs may remain valid months/years and survive password reset.

Examples:

- GitHub/GitLab PAT;
- AWS IAM access keys;
- Azure credentials;
- Heroku/Replit/Render platform tokens.

Attackers may extract these from developer workstations, config files, or CI secrets.

Revoke all PATs/long-lived credentials associated with compromised identities.

### Listing 97. Revoking AWS IAM User Access Keys

~~~bash
$ aws iam list-access-keys --user-name gmurphy
{
    "AccessKeyMetadata": [
        {
            "UserName": "gmurphy",
            "AccessKeyId": "AKIAQ3GCTAHPXBGQVE7W",
            "Status": "Active",
            "CreateDate": "2025-12-02T20:30:56+00:00"
        },
        {
            "UserName": "gmurphy",
            "AccessKeyId": "AKIAQ3GCTAHP2ZIMVBUU",
            "Status": "Active",
            "CreateDate": "2025-12-02T20:30:54+00:00"
        }
    ]
}

$ aws iam delete-access-key --user-name gmurphy --access-key-id AKIAQ3GCTAHPXBGQVE7W
$ aws iam delete-access-key --user-name gmurphy --access-key-id AKIAQ3GCTAHP2ZIMVBUU

$ aws iam list-access-keys --user-name gmurphy
{
    "AccessKeyMetadata": []
}
~~~

Final empty list confirms deletion.

Cross-provider revocation table continues in next source range.

## Table 30. Cloud Credential Revocation Quick Reference — Continuation

| Action | AWS | Azure | GCP |
|---|---|---|---|
| List credentials for principal | aws iam list-access-keys --user-name <user> | az ad sp credential list --id <service-principal-id> | gcloud iam service-accounts keys list --iam-account=<email> |
| Revoke/delete credentials | aws iam delete-access-key --user-name <user> --access-key-id <key-id> | az ad sp credential delete --id <service-principal-id> --key-id <key-id> | gcloud iam service-accounts keys delete <key-id> --iam-account=<email> |

Generate new tokens only after eradication is complete and account security is confirmed.

Browser-stored credentials are another persistence path. Browsers may retain saved passwords, authentication cookies, and session tokens. Attackers can extract and reuse them elsewhere.

On compromised systems:
- clear browser profiles where appropriate;
- rotate credentials saved in affected browser stores.

# API Keys and Service Credentials

Service credentials provide programmatic access independent of individual user authentication.

Examples:
- SaaS API keys;
- webhook secrets;
- database connection strings;
- service-to-service tokens;
- integration credentials;
- Azure service-principal secrets;
- GCP service-account keys.

These credentials often have broad scope, outlive individual sessions, and have weaker lifecycle management.

Rotate all potentially compromised secrets through the platform's supported management interface.

### Listing 98. Rotating Azure Service Principal Credentials

~~~powershell
PS C:\> Get-AzADSpCredential -ObjectId "2f91a3be-9c3c-4f6b-9cf7-1fb2e6e37ad2"

CustomKeyIdentifier :
EndDate             : 12/02/2026 05:41:17 PM
KeyId               : 3c8fcd5b-2c1d-4a96-90c9-5d9cd8f8ea21
StartDate           : 12/02/2025 05:41:17 PM

PS C:\> New-AzADSpCredential -ObjectId "2f91a3be-9c3c-4f6b-9cf7-1fb2e6e37ad2"

CustomKeyIdentifier :
EndDate             : 12/02/2027 05:44:02 PM
KeyId               : 9e5a7e8b-52af-4fc0-a2d3-cc91e0c6fa81
StartDate           : 12/02/2026 05:44:02 PM
SecretText          : tZp4K9Q~F8r1VdM2pJ7wHqL6xU3sN0Bg

PS C:\> Remove-AzADSpCredential -ObjectId "2f91a3be-9c3c-4f6b-9cf7-1fb2e6e37ad2" -KeyId "3c8fcd5b-2c1d-4a96-90c9-5d9cd8f8ea21"
~~~

The UUID values are source example identifiers.

Safe rotation order:
1. create replacement credential;
2. deploy it to dependent applications;
3. validate dependencies;
4. delete old credential.

This avoids unnecessary service interruption.

# Targeted Removal vs. System Rebuild

Targeted artifact removal is appropriate when responders can confidently enumerate attacker artifacts.

Rebuild provides stronger assurance when compromise is deep or uncertain, but usually costs more time/planning. In some incidents rebuild may actually be faster and less expensive than attempting exhaustive cleanup.

Three key factors:

## Severity of Compromise
Full rebuild is favored for rootkits, kernel-mode malware, firmware compromise, and other below-OS threats. Less severe, well-bounded compromise may be cleanable in place.

## System Criticality
Production criticality affects acceptable downtime and sequencing. Decision makers must balance confidence, restoration speed, and operational cost.

## Availability of Clean Sources
Rebuild requires trusted backups, gold images, or installation media.

A backup is useful only if it predates compromise and does not contain attacker artifacts. Older clean backups imply data loss between backup time and incident response. Managing that data-loss tradeoff belongs primarily to Recover.

# Vulnerability Remediation

Removing attacker artifacts without closing initial access leaves environment vulnerable to immediate recurrence.

Eradication must close the security gap that enabled the attack before recovery.

Focus first on vulnerabilities/misconfigurations proven relevant to this incident. Broader vulnerability cleanup is valuable but should not distract from the actual root cause.

# Identifying Exploited Vulnerabilities

Use evidence and RCA to identify exploited CVEs, misconfigurations, weak controls, and attack-path dependencies. Prioritize vulnerabilities confirmed exploited.

Use CVE identifiers for documentation, vendor guidance, patch tracking, and CTI correlation.

Vulnerability remediation must account for actual software version, environment, deployment model, and operational dependencies.

## Threat Intelligence / KEV Context

Vendor advisories explain technical details and fixes. Threat intelligence can add exploitation-in-the-wild context, TTPs, IOC, and known campaigns.

CISA Known Exploited Vulnerabilities (KEV) catalog is cited as a source of active-exploitation context.[30]

Source example: CVE-2025-64446, Fortinet FortiWeb path-traversal vulnerability, described as allowing administrative actions through crafted HTTP requests.[31]

### Рисунок 113. FortiWeb CVE-2025-64446 Advisory Excerpt
THIRD_PARTY_REVIEW_REQUIRED — external advisory screenshot not reproduced.

### Рисунок 114. FortiWeb KEV Catalog Entry
THIRD_PARTY_REVIEW_REQUIRED.

Source also describes CTI linking to a working exploit and using GitHub Copilot integration to inspect exploit functionality/IOC.

### Рисунок 115. GitHub Copilot IOC Analysis for FortiWeb Exploit
THIRD_PARTY_REVIEW_REQUIRED — product/external-code visual not reproduced.

Additional exploit context may improve detections, IOC development, and remediation validation.

## Configuration Weaknesses

Not every attack uses a software CVE.

Examples:
- permissive firewall;
- default credentials;
- exposed management UI;
- missing web security headers.

Corrective action must fix both the specific misconfiguration and the operational process that allowed it.

# Patch Management During Eradication

Apply patches for exploited vulnerabilities before recovery.

## Test and Verify Before Broad Rollout
Create documented procedure containing deployment steps, expected result, verification, and rollback. Test non-production first where feasible.

## Track Patch Status
Use CMDB, vulnerability scanner, inventory platform, tickets, or spreadsheet if nothing better exists. Need clear visibility into patched, pending, and failed systems.

## Balance Change Management with Speed
Normal change process is useful, but active exploitation often justifies expedited patching. Prepare should predefine who can authorize emergency change-window bypass and acceptable risk. Document deviations.

## Consider Phased Rollout
For large fleets: patch a lower-risk group, verify, advance to the next group, then critical systems. This reduces blast radius of patch problems.

## Verify System Functionality
After patching, validate business function, coordinate with owner, resolve compatibility/configuration issues, and document failures/resolutions.

# Addressing Unpatchable Systems

Some systems cannot be patched due to end-of-life, vendor restriction, or operational dependency.

Use compensating controls temporarily.

## Network Segmentation
Isolate vulnerable system, allow minimum inbound/outbound flows, and monitor closely.

## Application-Layer Controls
Examples include WAF and virtual patching. These can block known exploit patterns but are temporary.

## Enhanced Monitoring
Monitoring does not fix vulnerability, but can reduce time to detection. Alert on access to vulnerable service, abnormal process execution, and exploit-associated network traffic.

## Permanent Remediation Plan
Define migration/replacement/upgrade timeline. Compensating controls degrade over time and consume ongoing resources. Treat unpatchable systems as technical debt.

In regulated environment, known critical residual vulnerability may also require formal risk/disclosure tracking. Once IRT has implemented appropriate compensating control, business/system owner should carry residual risk in organization's risk-management process rather than let it disappear with incident closure.

> Compensating controls are temporary mitigation, not permanent remediation.

# WAF BYPASS OPPORTUNITIES

WAF can reduce risk from common web attacks such as SQL injection, XSS, and remote file inclusion, but it cannot be assumed to make a vulnerable application safe.

Source cites examples of WAF bypass research/incidents:
- parsing discrepancy bypass research in 2025;[32]
- reflected XSS bypass write-up in 2025;[33]
- shared-infrastructure bypass reporting in 2023;[34]
- JSON-based SQL payload bypass techniques in 2022.[35]

Practical lesson: WAF adds defensive depth and telemetry, but permanent remediation of underlying vulnerability remains required.

# Broader Vulnerability Assessment

If one system was exploited because of a vulnerability, find all systems sharing the vulnerable condition.

Tools may include commercial scanners, Greenbone/OpenVAS, EDR agent-based assessment, and Nuclei.

Nuclei uses YAML templates and can support custom CVE/weakness checks.

## IP Camera SSRF Example

Source uses a network camera with vulnerable /fetch endpoint accepting url parameter.

The SSRF can cause camera to request local/internal resources, including an administrative endpoint that exposes stored AWS credentials.

### Listing 99. IP Camera SSRF Vulnerability Discloses AWS Credentials

~~~bash
$ curl -s "http://192.168.1.140/fetch?url=http://127.0.0.1/internal-admin"
{
  "content_length": 169,
  "content_preview": "{\n  \"AccessKeyId\": \"AKIAQ3GCTAHP6WCRSYYK\",\n  \"SecretAccessKey\": \"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\",\n  \"Status\": \"Active\",\n  \"UserName\": \"cameralogic-s3export\"\n}\n",
  "status_code": 200,
  "url": "http://127.0.0.1/internal-admin"
}
~~~

The credentials are canonical source example data.

To find other affected cameras, source creates a Nuclei template.

### Listing 100. Nuclei Template for IP Camera SSRF Vulnerability Test — Beginning

~~~yaml
id: ssrf-url-fetcher

info:
  name: SSRF in CameraLogic URL Fetcher Endpoint
  author: Joshua Wright
  severity: high
  tags: ssrf

http:
  - method: GET
    path:
      - "{{BaseURL}}/fetch?url=http://127.0.0.1/internal-admin"
~~~

Matcher and execution continue in next source range.

## Listing 100. Nuclei Template for IP Camera SSRF Vulnerability Test — Completion

~~~yaml
matchers:
  - type: word
    words:
      - "AccessKeyId"
      - "SecretAccessKey"
~~~

The template tests the vulnerable endpoint/parameter against each target and matches strings expected in a response disclosing AWS credential fields.

### Listing 101. Nuclei Scan for Vulnerable IP Cameras

~~~text
$ nuclei -t ssrf-url-fetcher.yaml -list hosts-to-scan.txt

[INF] nuclei-templates are not installed, installing…
[INF] Successfully installed nuclei-templates at /root/nuclei-templates
[INF] Supplied input was automatically deduplicated (1 removed).
[WRN] Loading 1 unsigned templates for scan. Use with caution.
[INF] Current nuclei version: v3.5.1 (latest)
[INF] Current nuclei-templates version: v10.3.4 (latest)
[INF] Templates loaded for current scan: 1
[INF] Targets loaded for current scan: 27
[INF] Running httpx on input host
[INF] Found 8 URL from httpx
[ssrf-url-fetcher] [http] [high] http://172.16.40.20/fetch?url=http://127.0.0.1/internal-admin
[ssrf-url-fetcher] [http] [high] http://192.168.1.140/fetch?url=http://127.0.0.1/internal-admin
[INF] Scan completed in 557.642459ms. 2 matches found.
~~~

The scan identifies another vulnerable camera at 172.16.40.20.

Broader vulnerability scanning ensures eradication is not limited to the originally compromised host.

# Configuration Hardening

Eradication is not only patching.

Misconfiguration can be part of the attack chain and should be corrected according to:

- investigation findings;
- security baselines;
- operational requirements.

> Vulnerability remediation should cover supporting conditions that enabled the incident, not software patching alone.

## Harden System Configurations

Source points back to preparation guidance using CIS Benchmarks and similar hardening standards.[36]

Configuration drift can occur because of:

- updates;
- feature changes;
- temporary exceptions;
- operational changes.

During Eradicate, validate that intended hardening still exists.

# Enumerate Accessible Services

Review attack surface from both:

- external/network perspective;
- local host perspective.

Compare discovered services to documented requirements.

Pay special attention to:

- management interfaces;
- legacy protocols;
- unplanned exposure.

### Listing 102. Nmap Service Enumeration Example

~~~text
$ sudo nmap -p 1-65535 -sV 192.168.1.119
Starting Nmap 7.98 at 2025-12-04 06:29 -0500
Nmap scan report for 192.168.1.119
Host is up (0.0054s latency).
Not shown: 65528 closed tcp ports (reset)

PORT      STATE SERVICE       VERSION
22/tcp    open  ssh           OpenSSH 9.9 (protocol 2.0)
88/tcp    open  kerberos-sec  Heimdal Kerberos
2222/tcp  open  EtherNetIP-1?
5000/tcp  open  rtsp
5900/tcp  open  vnc           Apple remote desktop vnc
7000/tcp  open  rtsp
49185/tcp open  unknown

2 services unrecognized despite returning data.
[...]
Nmap done: 1 IP address (1 host up) scanned in 180.93 seconds
~~~

Notable exposure:

- SSH on 22;
- VNC on 5900.

Network scanning can stress fragile systems, so local enumeration is an alternative.

Windows:

- Get-NetTCPConnection;
- Get-NetUDPEndpoint.

Linux:

- ss -tuln;
- netstat -tuln.

macOS:

- lsof -i -n -P | grep LISTEN.

### Listing 103. PowerShell Listening Services Example

~~~powershell
PS C:\> Get-NetTCPConnection -State Listen |
  Select-Object -Property LocalAddress,LocalPort,OwningProcess,
    @{Name='ProcessName'; Expression={(Get-Process -Id $_.OwningProcess).ProcessName}}

LocalAddress    LocalPort OwningProcess ProcessName
------------    --------- ------------- -----------
::                  20718           676 services
::                   1540          2348 spoolsv
::                   1539          1096 svchost
::                   1538          1200 svchost
::                   1537           540 wininit
::                   1536           684 lsass
::                    445             4 System
::                    135           916 svchost
0.0.0.0             20718           676 services
0.0.0.0              9001          5896 nginx
0.0.0.0              5040          5056 svchost
[...]
~~~

Source highlights Nginx listening on port 9001.

Local enumeration is accurate but requires host-by-host access and collection coordination.

# Review Network Device Configurations

Review:

- firewall;
- router;
- switch;

against least privilege.

Temporary rules often become permanent and obsolete rules accumulate.

### Listing 104. FortiGate Firewall Policy Example

~~~text
FGT-Edge # show firewall vip
config firewall vip
    edit "WEBSERVER-8080"
        set uuid 7a3d9f2e-4b8c-51ef-a6d2-8c4e7f1b3a5d
        set extip 45.60.31.34
        set extintf "wan1"
        set portforward enable
        set mappedip "10.10.10.10"
        set extport 11111
        set mappedport 8080
    next
end

FGT-Edge # show firewall policy 15
config firewall policy
    edit 15
        set uuid 2f8a1c4d-6e9b-47d3-b5f1-9a2c8d4e6f7a
        set name "Allow-WEBSERVER-8080"
        set srcintf "wan1"
        set dstintf "internal"
        set action accept
        set srcaddr "all"
        set dstaddr "WEBSERVER-8080"
        set schedule "always"
        set service "TCP-11111"
        set logtraffic all
        set nat enable
    next
end
~~~

This stale configuration exposes internal server 10.10.10.10:8080 through public 45.60.31.34:11111 to any external source.

Eradication/hardening should:

- remove obsolete exposure;
- narrow broad allow rules;
- ensure business requirement exists.

# Disable Unnecessary Services

Disable unneeded:

- Telnet;
- FTP;
- RDP;
- SMB;
- other remotely reachable services.

Where remote access is required, prefer secure controlled methods such as:

- SSH;
- VPN;
- MFA.

After hardening:

- update CMDB;
- create change record;
- make new configuration authoritative.

Otherwise routine operations may later restore unsafe stale state.

# ERADICATION CHALLENGES

Modern incidents may require multiple Response Actions Loop iterations.

Source highlights four recurring challenges:

1. living off the land;
2. fileless malware;
3. legitimate RMM abuse;
4. cross-trust-boundary threats.

# Living Off the Land

Attackers use legitimate binaries/scripts/libraries — LOLBins — so defenders cannot simply remove the tool.

Examples:

- PowerShell;
- WMI;
- Windows Script Host;
- csc.exe;
- built-in utilities;
- authorized third-party tools.

Challenges:

- legitimate and malicious use can look similar;
- memory execution leaves few files;
- core system tools cannot simply be deleted.

Mitigations:

- behavioral detection;
- PowerShell logging;
- detect encoded commands;
- detect unusual parent process;
- constrained language mode where appropriate;
- application allowlisting;
- permit only approved scripts.

## THIRD-PARTY LOLBIN ACCESS

Source recounts a penetration test in a VDI environment where common offensive tools were blocked by endpoint protection.

Testing allowed applications revealed python.exe was permitted, even though Python was not installed by default.

The team could copy a Python runtime into the VDI and execute scripts, bypassing the practical intent of the allowlist.

### Рисунок 116. Blocked Executable Alert

THIRD_PARTY_REVIEW_REQUIRED — product screenshot not reproduced.

Lesson:

LOLBins are not only OS-native tools. Authorized third-party interpreters/scripting runtimes can provide equivalent attacker capability.

Defenders should audit allowlists for:

- scripting engines;
- interpreters;
- compilers;
- code-execution platforms.

# Fileless Malware

Memory-resident malware may use:

- PowerShell;
- injected code;
- process hollowing;
- scheduled execution.

A persistence artifact may launch a payload directly in memory without writing a conventional malware file.

### Listing 105. Windows Scheduled Task Fileless Persistence Example

Canonical source contains a scheduled-task command that downloads and executes an attacker-hosted PowerShell payload in memory after failed-logon events.

THIRD_PARTY_REVIEW_REQUIRED — the executable persistence command is not duplicated verbatim in the reader-facing translation. Canonical English RAG remains the verbatim technical source.

Preserved behavioral details:

- Windows Task Scheduler;
- trigger: Security Event ID 4625;
- execution as SYSTEM;
- hidden PowerShell;
- remote payload;
- in-memory execution via Invoke-Expression.

Investigation may identify the scheduled task, but understanding the remotely hosted script still requires:

- PowerShell script-block logging;
- endpoint telemetry;
- memory evidence;
- network capture/CTI where available.

Reboot may clear current memory-resident payload, but if persistence remains it will reload.

Eradication therefore requires removal of both:

- runtime payload;
- persistence mechanism.

# Legitimate Remote Monitoring and Management Tool Investigation

Attackers increasingly use legitimate RMM tools:

- TeamViewer;
- AnyDesk;
- ConnectWise ScreenConnect.

Advantages to attacker:

- valid signatures;
- common network traffic;
- approved vendor cloud infrastructure;
- resilience;
- unattended access.

Source cites Akira ransomware group and reported use of AnyDesk.[37][38]

### Рисунок 117. AnyDesk Remote Desktop Access

THIRD_PARTY_REVIEW_REQUIRED — product visual not reproduced.

### Рисунок 118. AnyDesk File Transfer Access

THIRD_PARTY_REVIEW_REQUIRED.

Simple process termination may fail because RMM tools can:

- run as auto-restarting services;
- support unattended access;
- use vendor cloud instead of attacker C2.

Effective remediation requires:

- authoritative inventory of approved RMM;
- detect unauthorized installations;
- endpoint controls to block unapproved RMM;
- centralized management for approved tools;
- visibility into active sessions;
- vendor-side access revocation when necessary.

# Cross-Trust Boundary Threat Investigation

A compromise in one domain or identity provider can propagate through trust relationships.

Examples:
- forest trusts;
- external domain trusts;
- federated identity;
- hybrid AD/Entra synchronization.

Attackers may establish persistence in connected environments even after the original environment is cleaned.

Evidence analysis is difficult because attacker-created artifacts in the trusted environment can appear legitimate.

Example:
- attacker gains Domain Admin in pseudovision.com;
- two-way trust exists with corp.falsimentis.com;
- attacker uses trust to create/modify privileged access in corporate forest.

### Рисунок 119. Cross-Forest Attack Path Example

THIRD_PARTY_REVIEW_REQUIRED — visual not reproduced.

Federated identity has similar risk.

If compromised IdP continues issuing valid SAML/OIDC tokens, cleaning individual relying-party applications does not remove attacker access.

Hybrid synchronization can also propagate compromised identity state between on-prem AD and Entra ID.

## Scoping Trust Relationships

Enumerate all trust paths.

For Active Directory:

### Listing 106. Active Directory Trust Enumeration

~~~powershell
PS C:\> Get-ADTrust -Filter *

Name             Source                 Target                Direction       TrustType
----             ------                 ------                ---------       ---------
pseudovision.com corp.falsimentis.com   pseudovision.com      Bidirectional   Forest
genusight.com    corp.falsimentis.com   genusight.com         Outbound        External
~~~

Also identify:
- realm trusts;
- federated relying parties;
- trusted SaaS applications;
- cross-tenant identity relationships.

Review authentication logs in trusted environments for activity from compromised source during incident window.

Artifact removal must be coordinated across trust boundaries.

Disabling account in one domain does not automatically remove:
- group membership created in trusted domain;
- delegated rights;
- cached sessions;
- federated application sessions.

Sequencing:
- if trusted source/IdP is compromised, remediate source first;
- then remediate downstream trusted environments;
- verify cross-boundary artifacts removed everywhere.

# ERADICATE ACTIVITY EXAMPLES

# The Memory Forensics Discovery

Greystone Manufacturing contained workstation of a senior engineer.

Initial assessment looked like routine malware:
- endpoint alert on suspicious process;
- connection to known C2 123.188.115.243.

The engineer had access to:
- ICS designs;
- supplier pricing.

Analyst Maya Rodriguez reviewed whole-system memory using Volatility.

## Process Enumeration

### Listing 107. Process Listing with Volatility

~~~text
$ vol -qf greystone_eng_caseir0523.raw windows.pslist.PsList
Volatility 3 Framework 2.26.2

PID     PPID    ImageFileName   Offset(V)       Threads Handles SessionId
4       0       System          0xbf84ba8b4040  167     -       N/A
[...]
6824    856     svchost.exe     0xbf84c1234560  8       -       0
7012    856     svchost.exe     0xbf84c2345670  6       -       0
7156    7012    rundll32.exe    0xbf84c3456780  3       -       0
8234    1       smss.exe        0xbf84c4567890  0       -       0
[...]
~~~

Anomalies:
- rundll32.exe child of svchost.exe;
- smss.exe PPID 1 instead of expected System PID 4.

These suggest:
- injection / DLL side-loading;
- process manipulation.

## Injected Code

### Listing 108. Detecting Injected Code with Malfind

~~~text
$ vol -qf greystone_eng_caseir0523.raw windows.malfind.Malfind --pid 7156
Volatility 3 Framework 2.26.2

PID     Process         Start VPN       End VPN         Tag     Protection              CommitCharge
7156    rundll32.exe    0x1d0000        0x1d2fff        VadS    PAGE_EXECUTE_READWRITE   3

0x1d0000        4d 5a 90 00 03 00 00 00 04 00 00 00 ff ff 00 00   MZ...
[...]
~~~

MZ header indicates PE code injected into rundll32 memory.

## Network Connections

### Listing 109. Network Connection Analysis

~~~text
$ vol -qf greystone_eng_caseir0523.raw windows.netscan.NetScan
Volatility 3 Framework 2.26.2

Offset          Proto   LocalAddr      LocalPort  ForeignAddr      ForeignPort  State        PID   Owner
0xbf84c8901234  TCPv4   10.50.23.42   49234      123.188.115.243  443          ESTABLISHED  7156  rundll32.exe
0xbf84c8902345  TCPv4   10.50.23.42   49567      10.50.20.15      445          ESTABLISHED  8234  smss.exe
0xbf84c8903456  TCPv4   10.50.23.42   49892      10.50.20.18      3389         ESTABLISHED  8234  smss.exe
[...]
~~~

Findings:
- injected rundll32 maintains C2 to 123.188.115.243;
- fake smss connects via SMB to file server 10.50.20.15;
- fake smss connects via RDP to engineering server 10.50.20.18.

This reveals missed lateral movement.

## Command Line Analysis

### Listing 110. Command Line Analysis

~~~text
$ vol -qf greystone_eng_caseir0523.raw windows.cmdline.CmdLine --pid 7156,8234
Volatility 3 Framework 2.26.2

PID     Process         Args
7156    rundll32.exe    C:\Windows\System32\rundll32.exe C:\Users\bthompson\AppData\Local\Temp\update.dll,DllMain
8234    smss.exe        C:\Windows\Fonts\smss.exe -enc aQBlAHgAIAAoAE4AZQB3AC0ATwBiAGoAZQBjAHQA...
~~~

The fake smss command line includes Base64-encoded PowerShell.

Decoded content revealed a second-stage loader supporting persistence/lateral movement.

## Handle Analysis

### Listing 111. Handle Analysis for Malicious Process

~~~text
$ vol -qf greystone_eng_caseir0523.raw windows.handles.Handles --pid 8234
Volatility 3 Framework 2.26.2

PID   Process   Offset          HandleValue  Type  GrantedAccess  Name
8234  smss.exe  0xbf84d1234560  0x4          Key   0x20019
\REGISTRY\MACHINE\SOFTWARE\Microsoft\Windows\CurrentVersion\Run

8234  smss.exe  0xbf84d2345670  0x1c         File  0x100081
\Device\HarddiskVolume3\Users\bthompson\Documents\ICS_Designs

8234  smss.exe  0xbf84d3456780  0x24         File  0x100081
\Device\HarddiskVolume3\Users\bthompson\Documents\Supplier_Pricing
[...]
~~~

Evidence shows access to sensitive engineering directories.

Maya documents eradication implications:

- remove injected rundll32 PID 7156;
- remove fake smss PID 8234 at C:\Windows\Fonts\smss.exe;
- remove Registry Run persistence;
- remove C:\Users\bthompson\AppData\Local\Temp\update.dll;
- investigate 10.50.20.15 and 10.50.20.18;
- determine whether ICS_Designs / Supplier_Pricing data was exfiltrated.

Memory analysis transforms apparent single-host malware cleanup into multi-system incident and triggers new Scope iteration.

# The Coordinated Credential Reset

Northwind Financial Services confirmed:
- attacker obtained domain-admin access;
- compromise lasted at least three weeks;
- Mimikatz executed on two DCs;
- credentials likely harvested.

Incident manager approved comprehensive credential reset.

Analyst David Barrett maps scope using tier model:

- 12 Tier 0 accounts;
- 47 Tier 1 accounts;
- more than 200 Tier 2 accounts;
- 83 service accounts.

Critical prerequisite:

> Administrative workstations and jump hosts used to perform resets must themselves be verified clean.

Resetting credentials from compromised admin workstation simply exposes the new credentials.

### Рисунок 120. Northwind Financial Account Tiers

THIRD_PARTY_REVIEW_REQUIRED — visual not reproduced.

Dependencies:
- svc_tradingdb for SQL trading platform;
- svc_backup for backup software;
- legacy service accounts with old passwords;
- uncertain application credential-update procedures.

David proposes 72-hour phased reset.

### Таблица 31. Credential Reset Phases

| Phase | Scope | Timing |
|---|---|---|
| Phase 1 | KRBTGT twice, Tier 0 | Friday 11 PM – Saturday 3 AM |
| Phase 2 | Tier 1 + critical service accounts | Saturday 6 AM – 12 PM |
| Phase 3 | Tier 2 + remaining service accounts | Saturday 2 PM – Sunday 6 PM |

## Phase 1

### Listing 112. KRBTGT Reset — Phase 1

~~~powershell
PS C:\> Set-ADAccountPassword -Identity krbtgt -Reset -NewPassword (ConvertTo-SecureString -AsPlainText "K3rb3r0s#R3s3t#Ph4s31!" -Force)
PS C:\>
~~~

After replication confirmation, second reset occurs after ten hours to invalidate previously forged tickets.

Then Tier 0 accounts are reset during maintenance window.

Two on-call admin users receive temporary limited-lifetime accounts for emergency access.

## Phase 2

Application-team coordination is required.

David tracks for every service account:
- dependent application;
- owner contact;
- reset procedure.

### Рисунок 121. Service Account Reset Coordination

THIRD_PARTY_REVIEW_REQUIRED — visual not reproduced.

Trading database account procedure was tested in staging.

Backup service account exposed an unexpected dependency: backup configuration encryption depended on old password. Vendor support was needed to export, update, and re-import configuration, extending Phase 2 by two hours.

## Phase 3

Tier 2 accounts are reset in departmental batches.

### Listing 113. Tier 2 Batch Password Reset

~~~powershell
PS C:\> $tier2Users = Get-ADUser -Filter * -SearchBase "OU=Tier2Admins,DC=northwind,DC=local"

PS C:\> foreach ($user in $tier2Users) {
>>     $tempPassword = ConvertTo-SecureString -AsPlainText ( -join (1..16 | ForEach-Object {
>>       [char](Get-Random -Minimum 33 -Maximum 127) }) ) -Force
>>     Set-ADAccountPassword -Identity $user -Reset -NewPassword $tempPassword
>>     Set-ADUser -Identity $user -ChangePasswordAtLogon $true
>>     Write-Host "Reset password for $($user.SamAccountName)"
>> }

Reset password for jsmith_admin
Reset password for mwilliams_admin
Reset password for kjohnson_admin
[...]
~~~

During reset window monitoring includes:
- failures from attacker IP ranges;
- new account creation;
- attempts to use old KRBTGT-derived credentials;
- DC Event ID 4768 Kerberos TGT requests.

### Listing 114. Credential Reset Validation

~~~powershell
PS C:\> Get-ADUser krbtgt -Properties PasswordLastSet | Select-Object PasswordLastSet

PasswordLastSet
---------------
11/16/2025 9:15:22 AM

PS C:\> Get-ADUser -Filter * -SearchBase "OU=Tier0,DC=northwind,DC=local" -Properties PasswordLastSet |
>> Where-Object -Property PasswordLastSet -LT (Get-Date).AddDays(-1) |
>> Select-Object SamAccountName, PasswordLastSet

PS C:\>
~~~

No result from second query means no Tier 0 passwords older than reset window.

Incident record:
- KRBTGT: 2 resets, ten hours apart, replication verified;
- Tier 0: 12 reset, 2 temporary accounts later disabled;
- Tier 1: 47 reset;
- Tier 2: 214 reset;
- service accounts: 83 reset;
- backup dependency required vendor coordination.

The phased approach removed harvested-credential access while minimizing disruption to critical trading operations.

## Coordinated Credential Reset — Conclusion

Incident record also captured:

- backup software configuration encryption extended Phase 2 by two hours;
- no authentication attempts using old credentials were detected during or after the reset window.

The phased reset eliminated use of harvested credentials while preserving critical operations and avoiding unplanned service disruption.

# ERADICATE: STEP-BY-STEP

This guide condenses the eradication workflow for:
- investigation;
- root cause analysis;
- persistence removal;
- identity remediation;
- rebuild/targeted removal;
- vulnerability remediation;
- challenge handling;
- validation;
- documentation.

Source notes the guide is available in PDF/Markdown at dynamicincidentresponse.com.

### Step 1. Conduct Short-Form Investigation to Inform Eradication

Short-form investigation provides enough insight to proceed without waiting for complete long-form forensics. Long-form work may continue in parallel for regulatory, legal, and organizational-learning needs.

#### 1. Answer key eradication questions

- What was the initial access vector, and is it closed?
- Which credentials were compromised, and are they rotated?
- What other systems did attacker access, and are they included in eradication?
- Which persistence mechanisms were deployed, and are all known?
- What vulnerability enabled attack, and is it remediated?

#### 2. Apply log investigation

- use portable detection rules and fast event-log analysis;
- query SIEM for IOC across ingested sources;
- correlate authentication, application, and network-flow logs;
- annotate the canonical attack timeline from Scope with eradication sequencing markers for persistence deployment/removal.

Scope owns the canonical attack-progression timeline; Eradicate annotates it.

#### 3. Conduct live investigation

- enumerate processes;
- enumerate connections;
- inspect system configuration;
- compare current state to known-good baselines;
- identify new services, tasks, accounts;
- document findings for eradication planning.

#### 4. Perform memory investigation when needed

- analyze memory captured during Contain;
- if memory was not captured, acquire whole-system memory before analysis;
- examine processes, network connections, loaded drivers;
- identify injected code;
- extract command line and handles.

Volatile acquisition itself belongs primarily to Contain.

#### 5. Analyze network data

- PCAP;
- NetFlow;
- firewall logs;
- DNS;
- cloud flow graphs;
- exfiltration volume/destination analysis.

#### 6. Use EDR for centralized endpoint investigation

- query multiple endpoints;
- correlate EDR with log/memory/network findings.

#### 7. Investigate malware

Static:
- hashes;
- strings;
- PE structure;
- CTI correlation.

Dynamic:
- isolated execution;
- monitoring;
- sandbox reports.

Extract:
- created files;
- registry artifacts;
- processes;
- persistence;
- C2 domains/IPs.

#### 8. Investigate BEC where relevant

- mailbox rules/forwarding;
- organization mail-flow rules;
- OAuth permissions;
- integrations;
- impossible travel/sign-in anomalies;
- fraudulent transactions with finance/accounting.

#### 9. Investigate insider threat where relevant

- coordinate HR/legal/leadership;
- inspect data access;
- privilege changes;
- exfiltration;
- remote tools;
- secondary accounts;
- altered configurations;
- preserve detailed evidence.

#### 10. Investigate supply-chain compromise

- software: all systems with compromised version + vendor IOC;
- hardware: serial numbers, procurement and shipping chain;
- service providers: enumerate all vendor access paths;
- coordinate findings with supplier/partner.

#### 11. Investigate cloud environments

- audit logs;
- differential IaC/baseline analysis;
- IAM roles and assume-role trusts;
- cross-account access;
- storage logs;
- serverless deployments;
- container-image modifications;
- SaaS provider activity reports;
- integration logs;
- privileges and OAuth apps.

### Step 2. Perform Root Cause Analysis

#### 1. Identify root cause

- trace attack chain to initial compromise;
- distinguish immediate vs underlying cause;
- document sequence;
- identify systemic weaknesses.

#### 2. Use structured analysis

- fishbone with four P's: People, Process, Product, Policy;
- or Five Whys for linear investigation;
- involve IT/security/business;
- validate against evidence.

#### 3. Document findings for remediation

- vulnerabilities;
- misconfigurations;
- process failures;
- preventive actions;
- risk/feasibility priorities;
- immediate and long-term improvements.

### Step 3. Remove Persistence Mechanisms

#### 1. Windows persistence

- consolidated autorun enumeration;
- registry Run keys;
- scheduled tasks;
- services;
- startup folders;
- WMI event subscriptions;
- DLL search-order hijacking;
- Group Policy scripts/software deployment.

#### 2. Linux persistence

- /etc/crontab, /etc/cron.d/, user crontabs;
- pending at jobs;
- systemd;
- shell profiles;
- SSH authorized_keys;
- kernel modules;
- /etc/ld.so.preload and LD_PRELOAD;
- PAM;
- SUID/SGID;
- sudo;
- package hooks;
- git hooks;
- udev.

#### 3. Service/application persistence

- suspicious encoded/eval files;
- compare web directories with known-good;
- web logs;
- file-integrity comparison against manifests/version control.

#### 4. Cloud persistence

- unauthorized IAM users/roles/policies;
- serverless functions;
- container images;
- event triggers;
- API keys;
- access tokens;
- service credentials;
- resource/bucket policies;
- cross-account access;
- OAuth registrations/consent.

### Step 4. Remediate Accounts and Identity Systems

This step expands beyond the known-compromised set already handled in Contain to:
- blast-radius accounts discovered during Scope;
- KRBTGT;
- trust passwords;
- delegation;
- hybrid AD/Entra.

#### 1. Local accounts and credentials

- remove unauthorized local accounts;
- reset additional legitimate affected accounts;
- clear cached credentials from LSASS, browser stores, credential managers;
- rotate local admin passwords using managed local-admin password solution.

#### 2. Active Directory

- prioritize Tier 0 → Tier 1 → Tier 2;
- reset compromised/high-risk accounts;
- remove unauthorized group memberships;
- rotate service accounts with application-team coordination.

#### 3. KRBTGT

- reset twice;
- wait at least ten hours between resets;
- verify replication after each;
- child domains before parent domains in multi-domain forest;
- monitor for Golden Ticket use;
- document timings.

#### 4. Domain-controller machine accounts

- reset individually after KRBTGT;
- allow replication between resets.

#### 5. Trust passwords

- reset on trusting side of affected trusts;
- verify trust functionality.

#### 6. Unconstrained delegation

- enumerate affected computer/user objects;
- disable where unnecessary;
- migrate required cases to constrained or resource-based constrained delegation.

#### 7. Hybrid/cloud identity

- coordinate AD and Entra;
- revoke sessions/refresh tokens;
- reset passwords in both environments;
- account for synchronization delay;
- remove malicious Entra app registrations;
- validate Entra Connect rules;
- reset sync-service credentials;
- audit federation.

#### 8. Extend session/token revocation

For additional accounts discovered after Contain:
- terminate active sessions;
- revoke OAuth access/refresh tokens;
- revoke PATs/API keys;
- rotate service credentials;
- clear browser cookies/tokens;
- monitor token reuse across both containment-era and eradication-era revocation sets.

### Step 5. Execute Targeted Removal or Rebuild

#### 1. Choose strategy

- targeted removal when scope is well understood;
- full rebuild when scope uncertain;
- restore from verified clean backup where appropriate.

#### 2. Validate method

- confirm clean backup exists for restore path;
- close root cause before rebuild/restore;
- test rebuilt system in isolation before handing to Recover;
- document chosen method and validation.

Per-system backup integrity validation at restore time belongs to Recover Step 1.

### Step 6. Remediate Vulnerabilities

#### 1. Patch exploited vulnerabilities

- map to CVE where possible;
- check CISA KEV;
- prioritize actively exploited vulnerabilities;
- test patches in non-production before broad rollout.

#### 2. Patch management

- track status;
- balance change-control with urgent eradication;
- use phased rollout;
- verify functionality.

#### 3. Unpatchable systems

- compensating controls;
- document temporary status;
- replacement/upgrade timeline;
- ongoing vulnerability management.

#### 4. Broader assessment

- scan for related vulnerabilities across environment;
- compare hardening to CIS Benchmarks or equivalent;
- enumerate accessible services;
- remove unnecessary services;
- review network-device rules;
- remove obsolete/excess exposure;
- disable Telnet/FTP/RDP/SMB unless explicitly required.

### Step 7. Address Eradication Challenges

#### 1. Living off the land

- review legitimate system tools used maliciously;
- analyze command-line arguments;
- baseline admin usage;
- improve logging.

#### 2. Fileless malware

- memory analysis;
- injected/reflected loading;
- PowerShell Script Block Logging;
- WMI traces;
- registry/WMI persistence;
- controlled restarts after persistence removal.

#### 3. RMM abuse

- audit installed RMM;
- identify unauthorized tools;
- review authorized-tool access;
- allowlist approved tools.

#### 4. Cross-trust persistence

- enumerate domain/forest/federation trusts;
- review trusted-environment auth logs;
- coordinate admins/IdPs;
- verify removal in every affected environment.

### Step 8. Validate Eradication Success

#### 1. Verify persistence removal

- re-scan IOC;
- confirm tasks/services/registry entries gone;
- monitor authentication for account remediation;
- verify blocked network indicators alert when touched.

#### 2. Monitor for continued attacker activity

- revoked credential use;
- known attacker infrastructure;
- suspicious process creation;
- canary files/honeypot credentials where appropriate.

#### 3. Confirm vulnerability remediation

- patches installed;
- compensating controls effective;
- hardening active;
- initial access vector closed.

### Step 9. Document Eradication Actions

#### 1. Investigation findings

- IOC;
- persistence mechanisms;
- RCA;
- contributing factors;
- attacker timeline;
- evidence gaps.

#### 2. Remediation actions

- each persistence removal with timestamp/method;
- credential resets;
- account scope;
- restoration decisions;
- validation;
- patches;
- compensating controls.

#### 3. Stakeholder communication

- executive outcome summary;
- technical brief for IT/security;
- legal/compliance documentation;
- Recover handoff.

#### 4. Feed Debrief

Capture:
- detection gaps;
- investigation/tool limitations;
- security-control gaps;
- playbook gaps.

Debrief Step 8 consolidates these into prioritized organizational improvements rather than each activity independently implementing every long-term change.

# Сноски и источники

[1] Barnhart, Heather, "Inside the Five Most Dangerous New Attack Techniques" RSAC Webcast, 2025, www.youtube.com/watch?v=JrmYKm0tihk&t=2093s

[2] Fishbone Diagram, Lean Six Sigma Definition, www.leansixsigmadefinition.com/glossary/fishbone-diagram/

[3] The Five Whys technique is attributed to Sakichi Toyoda, founder of what later became Toyota Industries. See en.wikipedia.org/wiki/Sakichi_Toyoda.

[4] Sigma HQ - Generic Signature Format for SIEM Systems, sigmahq.io/

[5] Hayabusa - Windows Event Log Fast Forensics Timeline Generator, github.com/Yamato-Security/hayabusa

[6] HIPAA Journal, "Rhode Island RIBridges System Hack," www.hipaajournal.com/rhode-island-ri-bridges-system-hack/

[7] State of Rhode Island, "RIBridges Investigation Summary," May 2025, admin.ri.gov/sites/g/files/xkgbur536/files/2025-05/RIBridges%20Investigation%20Summary%20FINAL%20-%20External%20Release.pdf

[8] HIPAA Journal, "Rhode Island RIBridges System Hack," www.hipaajournal.com/rhode-island-ri-bridges-system-hack/

[9] Rhode Island Current, "Deloitte Reaches $6.3M Deal to Settle Class Action Lawsuit in RIBridges Data Breach," October 17, 2025, rhodeislandcurrent.com/2025/10/17/deloitte-reaches-6-3m-deal-to-settle-class-action-lawsuit-in-ribridges-data-breach/

[10] Kyocera Document Solutions, "Security Advisory: Vulnerabilities in KfeCoSvc Driver," August 29, 2023, www.kyoceradocumentsolutions.com/en/our-business/security/information/2023-08-29.html

[11] VPC Flow Log Analysis, github.com/joswr1ght/vpc-flow-log-analysis/tree/master

[12] FBI Internet Crime Complaint Center, "Business Email Compromise: The $55 Billion Scam," September 2024, www.ic3.gov/PSA/2024/PSA240911

[13] Microsoft, "Detect and Remediate Illicit Consent Grants," learn.microsoft.com/en-us/defender-office-365/detect-and-remediate-illicit-consent-grants

[14] KnowBe4, "How a North Korean Fake IT Worker Tried to Infiltrate Us," July 2024, blog.knowbe4.com/how-a-north-korean-fake-it-worker-tried-to-infiltrate-us

[15] GitLab, "GitLab discovers widespread npm supply chain attack," about.gitlab.com/blog/gitlab-discovers-widespread-npm-supply-chain-attack/

[16] Nelson, Nate, "Marquis v. SonicWall Lawsuit Ups the Breach Blame Game," Dark Reading, February 2026, www.darkreading.com/cloud-security/marquis-sonicwall-lawsuit-breach-blame-game

[17] U.S. Department of Justice, "Leader of Massive Scheme to Traffic in Fraudulent and Counterfeit Cisco Networking Equipment Sentenced to Prison," May 2024, www.justice.gov/archives/opa/pr/leader-massive-scheme-traffic-fraudulent-and-counterfeit-cisco-networking-equipment

[18] Janushkevich, Dmitry, "The Fake Cisco: Hunting for backdoors in Counterfeit Cisco devices," F-Secure Labs, July 2020, labs.withsecure.com/publications/the-fake-cisco

[19] Salesloft, "Drift Integrations," September 2025, help.salesloft.com/s/topic/0TOPD0000002N2C4AU/drift-integrations

[20] Google Threat Intelligence, "Data Theft from Salesforce Instances via Salesloft’s Drift Third-Party Application," August 2025, cloud.google.com/blog/topics/threat-intelligence/data-theft-salesforce-instances-via-salesloft-drift

[21] Krebs on Security, "The Ongoing Fallout from a Breach at AI Chatbot Maker Salesloft," September 2025, krebsonsecurity.com/2025/09/the-ongoing-fallout-from-a-breach-at-ai-chatbot-maker-salesloft/

[22] s3logparse - S3 Access Log Parser, github.com/joswr1ght/s3logparse

[23] Microsoft Security Response Center, "Microsoft Actions Following Attack by Nation State Actor Midnight Blizzard," January 2024, msrc.microsoft.com/blog/2024/01/microsoft-actions-following-attack-by-nation-state-actor-midnight-blizzard/

[24] Wiz Research, "Midnight Blizzard breach: analysis and best practices," January 2024, www.wiz.io/blog/midnight-blizzard-microsoft-breach-analysis-and-best-practices

[25] Microsoft, "Tier model for partitioning administrative privileges," learn.microsoft.com/en-us/microsoft-identity-manager/pam/

[26] Microsoft, "Planning for compromise," Windows Server AD DS security best practices, learn.microsoft.com/en-us/windows-server/identity/ad-ds/plan/security-best-practices/planning-for-compromise

[27] Medin, Tim, "Kerberos 101," Red Siege, April 2020, www.redsiege.com/wp-content/uploads/2020/04/20200430-kerb101.pdf

[28] Microsoft, "Security posture assessments - Accounts," Microsoft Defender for Identity, learn.microsoft.com/en-us/defender-for-identity/security-posture-assessments/accounts

[29] Reddit r/cybersecurity, "Cached credentials and long-lived tokens," www.reddit.com/r/cybersecurity/comments/1gy6ynf/comment/lyosx5d/

[30] CISA, "Known Exploited Vulnerabilities Catalog," www.cisa.gov/known-exploited-vulnerabilities-catalog

[31] CVE-2025-64446, www.cve.org/CVERecord?id=CVE-2025-64446

[32] Qi, Ryan et al., "WAFFLED: Exploiting Parsing Discrepancies to Bypass Web Application Firewalls," arXiv, March 2025, arxiv.org/abs/2503.10846

[33] Prajapati, Pranav, "XSS: Bypassing Cloudflare WAF with a Simple Trick," Medium, 2025, medium.com/@pranavrp77/xss-bypassing-cloudflare-waf-with-a-simple-trick-12aff8ce87c7

[34] SOCRadar, "Cloudflare Protection Bypass Vulnerability on Threat Actors' Radar," 2023, socradar.io/blog/cloudflare-protection-bypass-vulnerability-on-threat-actors-radar/

[35] Claroty Team82, "JS-ON Security: Off - Abusing JSON-Based SQL to Bypass WAF," 2022, claroty.com/team82/research/js-on-security-off-abusing-json-based-sql-to-bypass-waf

[36] CIS Benchmarks - Security Configuration Guides, www.cisecurity.org/cis-benchmarks

[37] CISA, "#StopRansomware: Akira Ransomware," April 2024, www.cisa.gov/news-events/cybersecurity-advisories/aa24-109a

[38] ThreatDown, "Akira ransomware drops AnyDesk client on compromised systems," www.threatdown.com/blog/akira-ransomware-drops-anydesk-client-on-compromised-systems/
