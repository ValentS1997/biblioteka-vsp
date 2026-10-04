---
book_id: dynamic-incident-response-joshua-wright-en-2026
chapter_number: 14
source_title: "Recover Activity"
source_pdf_page_range: "405-433"
rag_chunk_range:
  first: "dynamic-incident-response-joshua-wright-en-2026:p0405:c01"
  last: "dynamic-incident-response-joshua-wright-en-2026:p0433:c01"
translation_status: "ACCEPTED"
license_notice: "Неофициальный русский перевод / unofficial Russian translation; original work CC BY 4.0. См. ../ATTRIBUTION.md."
third_party_review_policy: "Figures and external third-party visuals remain fail-closed."
translation_notes:
  - "Canonical English RAG is source of truth."
  - "Assembled from full-fidelity source-range segments."
  - "Commands, identifiers, event IDs, and platform names are preserved."
---

# Глава 14. Восстановление

Activity **recover — восстановление** представляет переход от устранения угроз к восстановлению normal operations.

Она использует результаты detection, scoping, containment и eradication, чтобы test/validate systems перед возвратом в production.

Recovery — это не просто снять containment и включить systems. Это orchestrated process, который должен подтвердить, что restored systems:

- secure;
- functional;
- готовы поддерживать operations;
- могут безопасно вернуться в production.

### Рисунок 122. Recover Activity Waypoint

THIRD_PARTY_REVIEW_REQUIRED — visual asset не воспроизводится; сохраняются caption и cross-reference.

Recovery балансирует две competing pressures:

- urgency восстановления operations;
- необходимость thorough validation для предотвращения recompromise.

Слишком быстрая recovery может вернуть environment в состояние, где attacker снова использует те же vulnerabilities или persistence mechanisms.

Слишком медленная recovery увеличивает business impact и stakeholder frustration.

Chapter рассматривает:

- recovery objectives;
- strategies возвращения systems в production;
- recovery challenges;
- system validation;
- enhanced monitoring;
- coordinated restoration;
- activity examples.

# RECOVERY OBJECTIVES

Recover activity обеспечивает controlled, validated return systems в production.

Source выделяет:

- pre-restoration verification;
- system validation testing;
- system owner acceptance;
- enhanced monitoring;
- coordinated production restoration;
- containment action removal;
- metrics capture.

## Pre-Restoration Verification

Перед возвратом любой system в production responders должны подтвердить:

- eradication была successful;
- conditions initial compromise устранены.

Это transition validation между Eradicate и Recover.

Цель — не допустить premature restoration и rapid recompromise.

### Таблица 32. Pre-Restoration Verification Checklist

| Verification area | Verification activities |
|---|---|
| Root Cause Remediation | Confirm vulnerability patched, credentials rotated, or misconfiguration corrected based on RCA |
| System Patching | Apply outstanding OS, firmware, and application patches beyond root-cause remediation |
| Persistence Removal | Verify all identified persistence mechanisms removed |
| Backup Validation | For backup restoration, confirm backup predates initial compromise using incident timeline |
| Rebuild Verification | For rebuilt systems, verify trusted sources and clean installation media |
| Security Control Status | Confirm EDR reporting, host firewall configured, logging enabled |
| IOC Scanning | Scan restored system for IOC after patching/hardening so result reflects final production configuration |

Start with root cause.

If initial access was:

- unpatched vulnerability → verify patch applied;
- compromised credentials → confirm credentials rotated/replaced everywhere relevant;
- misconfiguration → confirm corrected.

Then apply outstanding:

- OS updates;
- firmware updates;
- application updates.

Systems offline for days/weeks often fall behind routine patching.

Next verify removal of identified persistence.

For rebuilt systems:

- verify trusted installation sources;
- ensure compromised components were not reintroduced.

For backup-based recovery:

- verify backup predates initial compromise;
- use scope/eradicate timeline as reference.

Finally run IOC scan **after** patching/hardening/security controls are complete.

### Рисунок 123. Pre-Restoration Verification Process

THIRD_PARTY_REVIEW_REQUIRED.

# System Validation Testing

After pre-restoration verification, validation testing checks both:

- functional correctness;
- security-control correctness.

Functional testing should verify intended business functions.

Use existing test plans/UAT where available.

Test:

- data access;
- transaction processing;
- core workflows.

Security validation includes:

- EDR agent running/reporting;
- host firewall configured;
- logging enabled and forwarding correctly;
- patches/hardening from eradication still present.

Interconnectivity testing validates dependencies:

- databases;
- other application servers;
- user authentication;
- service-account authentication;
- required internal/external network resources.

### Рисунок 124. System Validation Testing Process

THIRD_PARTY_REVIEW_REQUIRED.

# System Owner Acceptance

System owners/business units should validate restored systems before production return.

Acceptance has two purposes:

1. confirm business functionality;
2. establish accountability for operational status.

Involve owners early.

Options:

- provide validation checklists/test plans;
- let business unit perform acceptance while IR validates security controls.

Business users may identify subtle problems technical teams miss.

Document:

- what was tested;
- who tested;
- owner acknowledgment;
- production readiness;
- any accepted limitations.

Formal sign-off establishes a baseline and transfer of responsibility.

It also protects the organization from later automatically attributing unrelated post-recovery failures to IR changes.

### Рисунок 125. System Owner Acceptance Process

THIRD_PARTY_REVIEW_REQUIRED.

# Enhanced Monitoring Configuration

Recovery does not end at production restoration.

Immediately after restoration, systems require heightened monitoring for:

- recompromise;
- residual attacker activity;
- eradication failures.

## Configuring Platform-Specific Logging and Auditing

Increase logging verbosity for:

- authentication;
- process creation;
- network connections;
- filesystem changes;
- system changes;
- administrative actions;
- other incident-relevant events.

On Windows, use:

- Group Policy;
- Microsoft Intune;
- auditpol.

Important warning:

Verbose auditing can sharply increase log volume.

Windows Event ID 4688 and Linux auditd execution logging can generate high volumes.

Before enabling enhanced auditing, verify forwarding infrastructure capacity:

- WEF collectors;
- universal forwarders;
- equivalent agents.

Ensure events reach intended destination rather than being dropped.

### Listing 115. Configuring Enhanced Windows Auditing for Post-Recovery Monitoring — Beginning

~~~powershell
PS C:\> auditpol /set /subcategory:"Logon" /success:enable /failure:enable
~~~

Listing continues in next source range.

## Listing 115. Configuring Enhanced Windows Auditing for Post-Recovery Monitoring — Completion

~~~powershell
The command was successfully executed.
PS C:\> auditpol /set /subcategory:"Special Logon" /success:enable /failure:enable
The command was successfully executed.
PS C:\> auditpol /set /subcategory:"Process Creation" /success:enable
The command was successfully executed.
PS C:\> auditpol /set /subcategory:"Account Lockout" /success:enable /failure:enable
The command was successfully executed.
PS C:\> auditpol /set /subcategory:"Security Group Management" /success:enable
The command was successfully executed.
PS C:\> auditpol /set /subcategory:"User Account Management" /success:enable
The command was successfully executed.
~~~

Use:

~~~powershell
auditpol /get /category:*
~~~

to review current audit-policy configuration and confirm applied changes.

For Linux, configure auditd rules targeted to recovery monitoring.

### Listing 116. Configuring Linux auditd Rules for Post-Recovery Monitoring

~~~text
$ cat /etc/audit/rules.d/recovery-monitoring.rules
## Monitor authentication-related files
-w /etc/passwd -p wa -k identity
-w /etc/shadow -p wa -k identity
-w /etc/group -p wa -k identity
-w /etc/sudoers -p wa -k sudoers

## Monitor SSH configuration and authorized keys
-w /etc/ssh/sshd_config -p wa -k sshd_config
-w /root/.ssh/authorized_keys -p wa -k ssh_keys

## Monitor process execution
-a always,exit -F arch=b64 -S execve -k exec

## Monitor network configuration changes
-w /etc/hosts -p wa -k hosts
-w /etc/resolv.conf -p wa -k dns

$ sudo augenrules --load
$ sudo systemctl restart auditd
~~~

For ARM64 adjust the process-execution rule to:

\`arch=arm64\`.

Rules must be tailored to:

- system role;
- environment;
- incident context;
- expected log volume.

### Таблица 33. Enhanced Monitoring Log Sources by Platform

| Platform | Log source | Important events |
|---|---|---|
| Windows | Security Event Log | Logon/privilege use: 4624, 4625, 4672, 4648; account/group changes: 4720, 4722, 4738, 4728, 4732; service/task creation: 4697, 4698; audit changes: 4719; log clear: 1102; Kerberos tickets: 4769; sensitive object access: 4662 |
| Windows | PowerShell Logging | Script Block 4104, Module 4103, transcription, AMSI |
| Windows | Sysmon | Process creation ID 1; network ID 3; DNS ID 22; image load ID 7; injection/remote thread ID 8; raw disk ID 9; WMI IDs 19–21; named pipes IDs 17–18; file/registry changes |
| Linux | auditd | Authentication, sudo, file access, process execution |
| Linux | auth.log / secure | SSH, su/sudo, PAM authentication |
| AWS | CloudTrail | API calls, IAM changes, resource changes, console logins |
| Azure | Activity Log / Sign-in Logs | Resource operations, authentication, role assignments |
| GCP | Cloud Audit Logs | Admin activity, data access, system events |

## Custom Detection and Monitoring Duration

Where possible, create incident-specific rules for:

- C2 domains;
- hashes;
- behavioral IOC;
- attacker TTPs.

Known IOC rules can provide high-value / low-noise warning for attacker return.

Monitoring duration must match:

- incident severity;
- risk tolerance;
- resource/cost constraints.

Source gives **thirty days** as a common practice, not a universal rule.

A longer window allows observation across:

- scheduled tasks;
- batch jobs;
- periodic business processes.

Define:

- what counts as abnormal;
- response procedures;
- responsible monitor owner.

IRT should remain engaged and ready to investigate anomalies.

### Рисунок 126. Enhanced Monitoring Configuration Process

THIRD_PARTY_REVIEW_REQUIRED.

# Coordinated Production Restoration

Production restoration requires coordination across:

- technical teams;
- business units;
- leadership.

Goal:

- correct sequence;
- appropriate timing;
- stakeholder readiness.

## RECOVERY RACI: WHO ACTUALLY DOES THIS WORK?

In mid/large organizations:

**Responsible / Accountable**

- IT operations;
- system owners;
- infrastructure teams.

They usually:

- plan sequence;
- schedule changes;
- rebuild systems;
- bring services online.

IRT is generally **Consulted / Informed**.

IRT focuses on incident-specific questions:

- does restore point predate attacker access?
- are credential/config changes from eradication deployed consistently?
- do rebuilt systems meet hardening requirements?
- can containment be safely lifted?
- is enhanced monitoring ready?

In smaller organizations/consulting situations, IR and IT execution may overlap.

Regardless of ownership, IR must know:

- what to validate;
- what to advise;
- what to document.

IT operations/system owners identify dependencies and recovery sequence.

Foundational services often go first:

- Active Directory;
- DNS;
- core network infrastructure.

Applications may depend on:

- databases;
- load balancers;
- identity;
- other application tiers.

Dependency chain and restoration procedure should ideally be documented before incident.

# AWS OUTAGE CASE STUDY: THE CRITICAL ROLE OF DNS IN RECOVERY

Source uses the AWS us-east-1 outage of December 7, 2021 as a recovery dependency example.[1]

A network-device overload during routine scaling triggered control-plane disruption.

Reported impact included:

- Disney+;
- Netflix;
- Slack;
- Robinhood;
- Coinbase;
- Ticketmaster;
- U.S. government services including IRS;
- more than 11,000 websites;
- major economic loss.

Critical failure involved DNS resolution for DynamoDB API services.

When name resolution failed:

- applications could not reach databases;
- service failures cascaded.

Recovery lesson:

DNS/name-resolution services should be restored and validated early.

Before application restoration verify:

- internal DNS;
- external DNS;
- expected records;
- resolution from multiple locations.

Source also repeats the operational reminder that unexpected network/application failures should include DNS in troubleshooting hypotheses.

## Restoration Timing

IT operations coordinates timing with business stakeholders.

IRT advises where timing affects:

- monitoring;
- evidence collection;
- investigation.

Off-hours restoration can provide:

- fewer users;
- lower traffic;
- easier troubleshooting;
- easier rollback.

But business may demand immediate return.

Ultimate timing decision belongs to organizational leadership.

Document:

- technical recommendation;
- decision;
- decision-maker;
- rationale.

## Phased Restoration

Restore systems in groups rather than all at once.

Benefits:

- isolate failures;
- insert validation checkpoints;
- adjust plan between phases.

Source generally recommends phased recovery, but notes it is not universally optimal.

### Рисунок 127. Coordinated Production Restoration Process

THIRD_PARTY_REVIEW_REQUIRED.

# Containment Action Removal

Containment measures may include:

- firewall rules;
- segmentation;
- disabled accounts;
- blocked services;
- DNS sinkholes.

Recovery removes temporary measures when no longer needed.

Some should remain long-term.

Example:

A DNS sinkhole for known C2 may remain for months/years as a durable detection/blocking control.

Before removal, inventory each measure:

- what it does;
- implementation time;
- owner;
- rationale.

Evaluate whether temporary measures should become permanent security improvements.

Examples:

- improved firewall rules;
- useful segmentation.

Remove controls incrementally as each system returns.

After each removal:

- monitor effects;
- verify functionality;
- stop if unexpected behavior appears.

### Рисунок 128. Containment Action Removal Process

THIRD_PARTY_REVIEW_REQUIRED.

# Metrics Capture

Record recovery timeline for each system:

- restoration start;
- validation complete;
- owner acceptance;
- production return.

Use these timestamps to identify actual recovery duration and bottlenecks.

Also record:

- problems;
- resolutions;
- failed restore attempts;
- adaptations;
- additional remediation;
- personnel hours;
- third-party support;
- additional cost.

Preserve recovery documentation for debrief and future planning.

### Рисунок 129. Metrics Capture Process

THIRD_PARTY_REVIEW_REQUIRED.

# RECOVERY STRATEGIES

Organizations can choose different recovery strategies depending on:

- incident characteristics;
- business requirements;
- operational constraints.

Strategy choice affects:

- recovery speed;
- risk;
- resource demand.

Source focuses on:

- phased recovery;
- coordinated recovery;
- scheduling;
- cloud recovery.

# Phased Recovery

Phased recovery restores systems incrementally.

Each system/small group is validated before the next phase.

Advantages:

- maximum control;
- failures easier to isolate;
- troubleshooting scope smaller;
- residual compromise can be re-contained with limited blast radius;
- natural checkpoints between phases;
- later phases can incorporate early lessons.

Tradeoff:

- overall recovery takes longer;
- sequential dependency can extend downtime significantly.

Best fit:

- uncertainty about eradication completeness;
- limited system dependencies;
- limited IR/IT parallel capacity.

# Coordinated Recovery

Coordinated recovery restores multiple systems in parallel during a planned maintenance window.

Primary advantage:

- speed;
- lower overall calendar time;
- potentially lower MTTR.

It may be necessary when tightly coupled systems cannot function independently.

Requirements:

- prevalidated procedures;
- staged resources;
- parallel work teams;
- clear communication;
- well-understood dependencies.

Risks:

- errors can affect multiple systems simultaneously;
- troubleshooting becomes more complex;
- flawed restoration plan can cascade.

Best fit:

- documented interdependencies;
- phased restoration would create unacceptable business impact;
- high confidence in eradication/restoration readiness.

# COORDINATED RECOVERY AT MAERSK: AN INCIDENT OF GLOBAL SCALE

Source uses Maersk's NotPetya recovery as coordinated recovery example.[2]

Reported impact:

- 49,000 laptops destroyed;
- 3,500 of 6,200 servers wiped;
- 1,200 applications unavailable;
- global port operations affected.

Maersk depended on tightly coupled systems, making phased restoration impractical.

Recovery organization included:

- emergency center in UK;
- headquarters in Denmark as global coordination hub;
- hundreds of parallel responders;
- dedicated system groups;
- new hardware procurement/distribution.

Investigation found all **150 domain controllers** wiped.

One intact DC backup survived in Ghana because the server had been offline during a power outage.

That backup became the foundation for rebuilding the network.

Reported restoration:

- 4,000 servers in ten days;
- 45,000 PCs in ten days;
- 2,500 applications in ten days;
- full recovery of 49,000 laptops in four weeks.

Estimated cost:

- $250–300 million.

Success factors:

- centralized coordination;
- parallel work allocation;
- clear command structure;
- out-of-band communications;
- manual procedures;
- crisis-ready coordination mechanisms.

Lesson:

coordinated recovery is organizational as much as technical.

# Scheduling Considerations

Timing affects:

- restoration success;
- business impact;
- rollback flexibility.

Off-hours advantages:

- fewer active users;
- lower network traffic;
- easier anomaly monitoring;
- fewer competing demands;
- lower-cost rollback if problems appear.

But 24/7 organizations may have no true off-hours.

Business pressure may favor immediate restoration.

Responders should explain tradeoffs clearly:

- what risk delay reduces;
- what risk immediate restoration accepts.

Decision makers own final scheduling decision.

System criticality matters:

- high-criticality systems may justify aggressive timeline and accepted risk;
- lower-criticality systems may justify conservative validation.

# Cloud Recovery Considerations

Cloud recovery requires attention to:

- shared architecture;
- access models;
- snapshots;
- cloud IAM;
- SaaS dependencies;
- hybrid connectivity;
- IaC.

## Snapshot Restoration

Cloud snapshots can restore known-good state quickly.

But snapshot date must predate initial compromise.

Post-compromise snapshots can reintroduce attacker access.

### Таблица 34. Restoring Cloud Instances from Snapshots

| Cloud provider | Snapshot restoration command |
|---|---|
| AWS | aws ec2 create-volume --snapshot-id snap-0123456789abcdef0 --availability-zone us-east-1a |
| Azure | az snapshot create --resource-group RG --source /subscriptions/…/disks/disk1 --name clean-snapshot |
| Google | gcloud compute disks create restored-disk --source-snapshot=clean-snapshot --zone=us-central1-a |

Use incident timeline from Scope/Eradicate before choosing restore point.

### Listing 117. Listing AWS Snapshots with Creation Timestamps

~~~text
$ aws ec2 describe-snapshots --owner-ids self --query \
'Snapshots[*].[SnapshotId,StartTime,Description]' --output table

------------------------------------------------------------------------------------
|                                 DescribeSnapshots                                |
+-----------------------+--------------------------+-------------------------------+
| snap-0a1b2c3d4e5f6g7h | 2025-11-15T03:00:00.000Z | Weekly backup - web-server-01 |
| snap-1b2c3d4e5f6g7h8i | 2025-11-22T03:00:00.000Z | Weekly backup - web-server-01 |
| snap-2c3d4e5f6g7h8i9j | 2025-11-29T03:00:00.000Z | Weekly backup - web-server-01 |
+-----------------------+--------------------------+-------------------------------+
~~~

## IAM Recovery Validation

Review:

- passwords;
- API keys;
- access tokens;
- service-account credentials;
- role assignments;
- policies;
- groups;
- permissions.

Validate MFA for cloud users.

Apply least privilege.

## Cloud Logging

Temporarily increase logging verbosity for:

- API activity;
- network connections;
- resource changes.

Higher logging cost may be justified during critical post-recovery weeks.

## Infrastructure as Code

Validate:

- templates;
- deployment configurations;
- version-control history.

If attacker modified IaC, new resources can recreate backdoors/misconfiguration.

# RECOVERY CHALLENGES

Source highlights:

- clean-backup data loss;
- business pressure;
- uncertainty in eradication verification;
- coordination complexity;
- user communication;
- post-recovery attribution.

# Data Loss from Clean-Backup Recovery

A backup that predates compromise may also predate legitimate business changes.

Loss window may be:

- hours;
- days;
- longer.

Options:

- selectively restore user-created files from newer backups after investigation;
- restore validated application/database data separately;
- manually recreate critical changes.

Some data loss may be the unavoidable cost of avoiding attacker reintroduction.

Coordinate with data owners.

# Business Pressure for Rapid Restoration

Downtime creates:

- business loss;
- user frustration;
- financial impact.

Pressure grows as incident duration increases.

This can push teams toward:

- bypassing validation;
- reducing monitoring;
- skipping controlled rollout.

Thorough eradication can reduce urgency because organization has more confidence attacker is gone.

Some organizations extend recovery over weeks/months to address:

- technical debt;
- hardening;
- upgrades;
- replacements.

Translate recovery work into business language:

- avoid another outage;
- protect restored data;
- prevent attacker return.

Maintain regular stakeholder updates.

Document:

- timing decisions;
- scope decisions;
- decision makers;
- information available at decision time.

# Eradication Verification Uncertainty

Absolute certainty is rare.

Sophisticated attacker persistence may remain undiscovered.

Recovery therefore becomes a **risk management exercise**.

Residual risk must be accepted at system/business-process level.

Treat eradication verification as ongoing, not one-time.

Use concrete checks before/after restoration:

- registry/configuration validation;
- scheduled-task review;
- startup-item inspection;
- binary integrity checks.

Results feed go/no-go decisions.

Enhanced monitoring operationalizes uncertainty management.

Phased recovery limits impact if attacker returns.

# Coordination Complexity

Recovery involves multiple groups working in parallel:

- IR validating systems;
- IT operations restoring systems;
- network teams adjusting connectivity;
- business units conducting acceptance testing;
- leadership making timing decisions.

Complexity rises when recovery spans:

- time zones;
- vendors;
- external service providers.

Communication failures can cause:

- IT restoring system before security validation;
- network removing containment too early;
- users resuming work before acceptance testing;
- known problems appearing as surprise failures.

## Incident Response Coordinator

For multi-system/multi-team incidents, a coordinator can:

- track progress;
- facilitate communication;
- enforce sequence;
- prevent parallel-work mistakes.

For larger incidents, technical project management may help.

A Gantt chart can expose:

- resource constraints;
- critical path;
- dependency delays.

This gives leadership a business-readable basis for decisions about:

- contractors;
- change windows;
- reprioritization.

## Explicit Handoffs

Recovery plans should define conditions for moving between:

1. restoration;
2. validation;
3. acceptance testing;
4. production release.

Criteria may include:

- required logs enabled;
- health checks passing for defined period;
- UAT complete.

Explicit handoffs reduce readiness debates and coordination friction.

# User Communication and Expectations

Users need to know:

- when systems may return;
- what they must do;
- what limitations remain.

Avoid overpromising.

Repeated missed deadlines damage trust.

Technical IRT should normally provide accurate status data to:

- communication leads;
- internal communications;
- public relations where applicable.

Those roles own the messaging.

Prepare reusable templates for:

- delays;
- partial restoration;
- user action required.

For large incidents:

- establish regular cadence;
- send updates even when nothing materially changed;
- use multiple channels because email/chat may be unavailable.

# Post-Recovery Problem Attribution

After recovery, unrelated issues may be blamed on incident response.

Examples:

- hardware failure;
- latent bug;
- configuration drift;
- normal operational issue.

Acceptance testing and owner sign-off create a documented baseline:

- system met agreed requirements;
- system was functional at a known point in time.

Relationships matter too.

System owners who participate in recovery are more likely to treat recovery as shared work rather than imposed change.

# RECOVERY ACTIVITY EXAMPLE

## Phased Recovery of a Domain Controller Environment

Sarah Park, senior incident responder at Lakewood Health Systems, is recovering from ransomware.

Impact:

- domain controllers encrypted across three sites;
- clinical systems offline because AD authentication unavailable.

Investigation found:

- initial access through vulnerable VPN appliance;
- compromise began 18 days before encryption.

Backup situation was poor:

- attackers encrypted primary backup repository;
- daily incremental backups lost;
- disk-based weekly restore points lost;
- longer-retention daily/monthly tiers on same repository also lost.

Only weekly snapshots already synchronized to an offline archive survived.

Sarah reviewed DC backups.

### Listing 118. Reviewing Available Domain Controller Backups

~~~powershell
PS C:\> Get-WBBackupTarget | Get-WBBackupSet | Where-Object {$_.VersionId -like "*DC01*"} |
>>     Select-Object VersionId, BackupTime | Sort-Object BackupTime -Descending

VersionId                            BackupTime
---------                            ----------
DC01-2025-12-04                      12/4/2025 2:00:00 AM
DC01-2025-11-27                      11/27/2025 2:00:00 AM
DC01-2025-11-20                      11/20/2025 2:00:00 AM
DC01-2025-11-13                      11/13/2025 2:00:00 AM
~~~

Interpretation:

- Dec 4: post-compromise, unsafe;
- Nov 27: attacker already had AD access;
- Nov 20: predates initial access, safe.

Sarah selected Nov 20.

Before production restore:

- test-restored NTDS.dit to isolated VM;
- verified backup integrity;
- confirmed VPN vulnerability patched;
- confirmed service-account credentials rotated;
- ran IOC scan;
- documented verification.

Recovery then proceeded in phases.

## Phase 1 — Primary Domain Controller

PDC emulator restored first because other DCs and AD-dependent systems required it.

### Listing 119. Verifying Domain Controller Services Post-Restoration

~~~powershell
PS C:\> Get-Service NTDS, DNS, Netlogon, DFSR | Select-Object Name, Status

Name     Status
----     ------
NTDS     Running
DNS      Running
Netlogon Running
DFSR     Running

PS C:\> dcdiag /test:sysvolcheck /test:advertising
[...]
......................... DC01 passed test sysvolcheck
......................... DC01 passed test Advertising
~~~

Validation:

- AD DS running;
- DFSR running;
- DC advertising correctly.

Before next phase, Sarah enabled enhanced auditing.

### Listing 120. Configuring Enhanced Auditing on Restored Domain Controller

~~~powershell
PS C:\> auditpol /set /subcategory:"Kerberos Authentication Service" /success:enable /failure:enable
The command was successfully executed.
PS C:\> auditpol /set /subcategory:"Kerberos Service Ticket Operations" /success:enable /failure:enable
The command was successfully executed.
PS C:\> auditpol /set /subcategory:"Credential Validation" /success:enable /failure:enable
The command was successfully executed.
~~~

## Phase 2 — Secondary Domain Controllers

Two satellite-site DCs restored sequentially.

After each, Sarah verified replication before continuing.

### Listing 121. Verifying AD Replication Health

~~~text
PS C:\> repadmin /replsummary

Replication Summary Start Time: 2025-12-11 14:23:15

Beginning data collection for replication summary, this may take a while:
[...]

Source DSA          largest delta    fails/total %%   error
DC01                       12m:05s    0 /   5    0
DC02                       08m:32s    0 /   5    0
DC03                       15m:47s    0 /   5    0

Destination DSA     largest delta    fails/total %%   error
DC01                       12m:05s    0 /   5    0
DC02                       08m:32s    0 /   5    0
DC03                       15m:47s    0 /   5    0
~~~

All DCs replicated without failures.

A known complication appeared:

- backup was 21 days old;
- computer objects for newer workstations were missing.

Sarah documented those objects for later recreation rather than delaying DC restore.

## Phase 3 — Member Servers and Workstations

Priority:

- RADIUS;
- certificate authority;
- clinical applications;
- other AD-dependent systems.

Each server required system-owner acceptance.

Workstations were rebuilt from gold images instead of backup because this was faster and cleaner.

User data lived separately on unaffected network shares.

Deployment proceeded by department, prioritizing clinical areas.

## Radiology Dependency Problem

A radiology service-account password had been rotated:

- after backup date;
- before attacker access.

Restored AD contained old password.

Result:

- radiology application authentication failed.

Enhanced logging quickly showed failed service-account authentication.

Sarah coordinated with vendor to:

- reset service-account password;
- update application configuration.

This added one day to Phase 3.

After eight days, full restoration completed.

### Рисунок 130. Lakewood Health Systems Recovery Timeline

THIRD_PARTY_REVIEW_REQUIRED.

## Lessons Captured

1. Online backup repository was destroyed.
   - only four offline weekly snapshots survived;
   - source recommends immutable/air-gapped tier aligned with 3-2-1-1-0;
   - ninety days or more of protected weekly snapshots would improve margin.

2. Service-account inventory was incomplete.
   - future inventory should include rotation dates.

3. Gold images accelerated workstation recovery.
   - keep them current.

4. AD dependency created a bottleneck.
   - business continuity planning should explicitly model authentication dependencies.

Sarah recorded these gaps during Recover so they would flow into formal Debrief.

# RECOVER: STEP-BY-STEP

Следующие steps дают condensed operational reference для:

- validation;
- testing;
- production restoration;
- monitoring;
- containment removal;
- metrics.

Source указывает, что guide доступен в PDF/Markdown на dynamicincidentresponse.com.

### Step 1. Conduct Pre-Restoration Verification

Этот step повторно подтверждает Eradicate Step 8 exit criteria для конкретной system перед production return.

Он не повторяет eradication from scratch.

Используйте Eradicate evidence/documentation как starting point.

Focus Recover Step 1:

- findings всё ещё valid;
- backup integrity;
- rebuild integrity;
- recovery-specific validation.

#### 1. Revalidate root-cause remediation

- exploited vulnerability remains patched;
- compromised credentials remain rotated across all systems where used;
- initial-access misconfiguration remains corrected;
- eradication documentation confirms no unresolved issues/regressions.

#### 2. Revalidate persistence removal

Treat eradication verification as ongoing.

Confirm prior checks still hold.

Spot-check:

- scheduled tasks;
- services;
- registry entries;
- unauthorized accounts;
- startup items;
- critical-binary integrity;
- relevant configuration.

Use findings for go/no-go.

#### 3. Validate backup integrity

For backup restore:

- backup predates initial compromise;
- validate via checksum or test restore;
- document selection rationale;
- if no clean backup exists, document rebuild method and validation.

#### 4. Verify rebuild integrity

- trusted installation media/gold image;
- source not compromised;
- document rebuild procedure;
- record deviations.

### Step 2. Perform System Validation Testing

#### 1. Functional testing

- standard business-operation tests;
- data access;
- transactions;
- application workflows;
- UAT/test plans where available;
- document issues.

#### 2. Security controls

- EDR installed/running/reporting;
- host firewall enabled/configured;
- logs flowing;
- patches/hardening retained.

#### 3. Interconnectivity

- database connectivity/data access;
- application-server paths;
- user/service authentication;
- required internal/external resources.

### Step 3. Obtain System Owner Acceptance

#### 1. Coordinate acceptance testing

- provide test plans/checklists;
- schedule with business representatives;
- support testing;
- document identified issues.

#### 2. Obtain sign-off

- record testing and tester;
- owner acknowledgment of production readiness;
- document accepted limitations;
- obtain formal sign-off before production release.

### Step 4. Configure Enhanced Monitoring

#### 1. Elevated logging

- advanced authentication/process/system-change audit;
- PowerShell Script Block Logging;
- Linux auditd for critical files/processes;
- verify SIEM/log forwarding.

#### 2. Incident-specific detection

Confirm rules created during Contain/Eradicate are active on restored systems:

- C2 domains;
- hashes;
- behavioral TTP-based detection.

Tune:

- scope;
- threshold;
- signal-to-noise for post-recovery window.

Add any newly identified recovery rules through detection engineering rather than unmanaged ad hoc logic.

Test that rules generate expected alerts.

#### 3. Monitoring duration/procedure

- duration matched to incident severity;
- source notes thirty days minimum as typical guidance in this step;
- define abnormal behavior;
- define response process;
- assign review responsibility.

### Step 5. Execute Coordinated Production Restoration

#### 1. Identify dependencies and sequence

- map dependencies;
- identify foundational services:
  - AD;
  - DNS;
  - network infrastructure;
- document sequence;
- coordinate with owners/IT operations.

#### 2. Coordinate timing

- present timing options/risks to decision makers;
- recommend off-hours where feasible;
- recognize leadership owns final timing;
- document recommendation/decision/rationale;
- communicate schedule;
- prepare rollback.

#### 3. Select phased or coordinated restoration

**Phased**

Use when:

- eradication confidence limited;
- capacity constrained.

Restore small groups, monitor, then expand.

**Coordinated**

Use when:

- systems tightly interconnected;
- dependencies documented;
- simultaneous restoration required.

For either approach:

- follow planned sequence;
- validate before next phase;
- monitor immediately;
- document deviations.

#### 4. Manage coordination complexity

- designate IR coordinator for multi-team recovery;
- define explicit handoff criteria:
  - restoration;
  - validation;
  - acceptance;
  - production;
- translate technical state into business language;
- prepare communication templates;
- establish owner-signed post-recovery baseline.

#### 5. Cloud-specific recovery

When applicable:

- verify snapshot dates against incident timeline;
- audit IAM:
  - API keys;
  - tokens;
  - service-account credentials;
  - role assignments;
  - policies;
- validate MFA;
- review IaC/version-control history;
- consider elevated cloud logging.

#### 6. User communications

- designate communication leads;
- establish fixed cadence;
- communicate even if no new information;
- avoid overpromising exact restoration time;
- prepare delay/partial-restoration/action-required templates;
- use multiple channels.

#### 7. Address data loss from clean backup

- identify data changed after clean backup;
- recover newer files/application data only after validating them clean;
- coordinate acceptable data-loss threshold with business owner;
- document accepted loss and recovery decisions.

### Step 6. Remove Containment Measures

Containment is lifted incrementally during Step 5 as systems require connectivity for validation/production.

Step 6 consolidates status and decides what remains permanent.

#### 1. Inventory measures

- firewall rules;
- segmentation;
- access restrictions;
- disabled accounts;
- blocked services;
- DNS sinkholes;
- rationale/date;
- candidate permanent controls.

#### 2. Remove incrementally

For each validated system:

- remove relevant temporary control;
- monitor adverse effects;
- timestamp action/outcome;
- verify functionality.

#### 3. Evaluate permanent controls

- identify long-term security value;
- coordinate with security architecture;
- document keep/remove decision;
- update policies if measure becomes permanent.

### Step 7. Capture Recovery Metrics

#### 1. Timeline

For every system:

- restoration start;
- validation complete;
- owner acceptance;
- production restoration.

Calculate:

- total recovery duration;
- bottlenecks;
- variance from stakeholder estimates.

#### 2. Issues/resolutions

- restoration problems;
- resolutions;
- procedural adaptations;
- lessons while fresh;
- documentation/procedure gaps.

#### 3. Resource investment

- personnel hours;
- third-party support;
- additional costs;
- data for incident cost/future planning.

#### 4. Pass documentation to Debrief

- hand recovery documentation to Debrief Step 3 for unified incident record;
- ensure accessibility for post-incident review;
- summarize ongoing enhanced monitoring from Step 4;
- prepare AAR handoff.

# Сноски и источники

[1] Eze Sunday, "AWS Outage Breaks Most of the Internet: My Thoughts," AWS in Plain English, December 2021, aws.plainenglish.io/aws-outage-breaks-most-of-the-internet-my-thoughts-630975d88bea

[2] Andy Greenberg, "The Untold Story of NotPetya, the Most Devastating Cyberattack in History," Wired, August 2018, www.wired.com/story/notpetya-cyberattack-ukraine-russia-code-crashed-the-world/; see also Gavin Ashton, "Maersk, me & NotPetya," gvnshtn.com/posts/maersk-me-notpetya/
