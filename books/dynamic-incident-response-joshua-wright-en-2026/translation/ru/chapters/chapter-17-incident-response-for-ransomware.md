---
book_id: dynamic-incident-response-joshua-wright-en-2026
chapter_number: 17
source_title: "Incident Response for Ransomware"
source_pdf_page_range: "546-583"
rag_chunk_range:
  first: "dynamic-incident-response-joshua-wright-en-2026:p0546:c01"
  last: "dynamic-incident-response-joshua-wright-en-2026:p0583:c01"
translation_status: "ACCEPTED"
license_notice: "Неофициальный русский перевод / unofficial Russian translation; original work CC BY 4.0. См. ../ATTRIBUTION.md."
third_party_review_policy: "Third-party figures, quoted report text, screenshots, and external materials remain fail-closed where marked."
translation_notes:
  - "Canonical English RAG is source of truth."
  - "Assembled from full-fidelity source-range segments."
  - "Commands, identifiers, metrics, and references are preserved where represented."
---

# Глава 17. Реагирование на инциденты с программами-вымогателями

# RANSOMWARE INTRODUCTION

Ransomware остаётся одним из наиболее disruptive и financially damaging типов инцидентов.

Эта глава не заменяет общий DAIR lifecycle из Part 2. Она добавляет ransomware-specific considerations для тех же waypoints:

- Prepare;
- Verify/Triage;
- Scope;
- Contain;
- Eradicate;
- Recover;
- Debrief.

Организациям следует использовать общие главы DAIR как baseline и дополнять их рекомендациями этой главы.

В introductory section рассматриваются:

- текущие ransomware trends;
- финансовый impact;
- различные модели ransomware/extortion operations;
- multi-vector extortion beyond encryption.

# Ransomware Attack Trends

Ransomware и data-extortion threats остаются одной из ключевых угроз across sectors.

Source отмечает рост data leak events с 2022 по конец 2025 года.

Chainalysis 2026 Crypto Crime Report сообщает:

- data-leak-site postings выросли примерно на 50% YoY между 2024 и 2025;
- в 2025 victims платили ransom менее чем в 30% reported cases;
- несмотря на это, общий volume ransomware/extortion продолжил расти.[1]

Даже когда ransom не выплачивается, incident cost включает:

- business interruption;
- forensic investigation;
- legal fees;
- regulatory penalties;
- reputational damage.

### Рисунок 178. Chainalysis 2026 Crypto Crime Report

THIRD_PARTY_REVIEW_REQUIRED — chart and quoted report text not reproduced verbatim.

Source reports more than $820M in identified on-chain ransomware payments for 2025, with expectation that attribution could later increase the total.

Modern ransomware evolved from simple encryption into multi-stage extortion operations.

Boundaries between:

- ransomware;
- data theft;
- broader cyber extortion;

have become blurred.

Some campaigns now rely more on stolen-data leverage than on encryption itself.

# Initial Access Trends

Common access paths include:

- RDP;
- RMM tools;
- exposed VPN/authentication endpoints;
- stolen credentials;
- phishing;
- voice phishing;
- SMS phishing;
- remote-access portals;
- cloud services.

Credential compromise may have happened:

- weeks/months earlier;
- on personal devices;
- on mobile systems;
- on systems outside enterprise telemetry.

Therefore the initial credential-theft event may leave no evidence in organizational logs.

# SIDEBAR: THE UNTRACEABLE CREDENTIAL PROBLEM

A common ransomware investigation finding:

- attacker used valid credentials;
- first malicious authenticated session is visible;
- the origin of credential theft is unknown.

Possible credential origins:

- phishing;
- infostealer on personal system;
- underground marketplace;
- unrelated earlier breach;
- other off-network compromise.

This uncertainty affects:

## Investigation scope

Without knowing where the credentials came from, responders cannot prove the initial-access vector is fully closed.

## Lessons learned

“Deploy MFA everywhere” is not always sufficient because AitM attacks may bypass some MFA implementations.

The credential-harvesting activity itself may occur beyond the visibility of the victim organization.

## Stakeholder communication

Executives often ask:

- How did they get in?
- How do we prevent recurrence?

Sometimes the correct answer is:

- exact initial credential compromise cannot be determined.

Source recommends focusing on controls that reduce the value of stolen credentials:

- MFA broadly deployed;
- conditional access;
- PAM;
- anomalous-authentication monitoring.

Accepting uncertainty is better than false confidence.

# Legitimate RMM as Attacker Infrastructure

Some ransomware campaigns avoid dedicated C2 and use legitimate tools such as:

- ScreenConnect;
- AnyDesk;
- TeamViewer.

These blend into normal environments because IT/support may legitimately use the same software.

# Initial Access Brokers

Initial Access Brokers (IABs) specialize in:

1. compromising environments;
2. maintaining access;
3. selling access to ransomware affiliates.

This creates:

- longer gap between initial access and encryption;
- multiple actor handoffs;
- extended dwell time;
- reduced visibility into exact credential provenance.

IAB activity may predate ransomware deployment by weeks or months.

### Рисунок 179. BreachStars Forum Credential Sales Post

THIRD_PARTY_REVIEW_REQUIRED.

# Infrastructure Targets

Ransomware operators increasingly target:

- VMware ESXi and other hypervisors;
- backup servers;
- storage platforms;
- lights-out management systems;
- virtualization consoles.

Compromise of a single hypervisor can affect many VMs.

Destroying backups or management planes reduces recovery options before encryption starts.

# Attack Differentiation

Different ransomware categories require different response assumptions.

## Human-Operated Ransomware (HumOR)

Human-operated attacks include active hands-on-keyboard operations:

- reconnaissance;
- privilege escalation;
- lateral movement;
- disabling defenses;
- backup destruction;
- data exfiltration;
- timed encryption.

Operators adapt decisions in real time.

Long dwell time increases risk of:

- persistence;
- broad credential theft;
- high-value data exposure;
- extensive environment preparation before encryption.

Source notes AI/LLMs are lowering the skill barrier:

- social engineering generation;
- identity-permission analysis;
- target selection;
- tool adaptation.

This can increase campaign volume/sophistication without equivalent attacker expertise.

## Automated or Mass-Distributed Ransomware

These campaigns favor scale over precision.

Typical characteristics:

- malicious attachments;
- exploit kits;
- immediate execution;
- limited reconnaissance;
- limited lateral movement.

Recovery can be simpler when compromise remains constrained to directly infected systems.

## Encryptionless Extortion

Attacker steals data but does not encrypt systems.

Leverage comes from:

- disclosure risk;
- regulatory exposure;
- reputational impact.

Response emphasis shifts toward:

- breach notification;
- data classification;
- exposed-data determination;
- legal/compliance workflows.

## Pseudo-Ransomware and Wipers

Some incidents appear to be ransomware but recovery via payment is not possible.

Possibilities:

- attacker never intended to provide a decryptor;
- destructive implementation;
- wiper disguised as ransomware.

Consider this when:

- ransom note lacks normal negotiation details;
- decryption fails despite apparently valid keys;
- artifacts indicate destructive rather than recoverable encryption.

# SIDEBAR: RANSOMWARE-AS-A-SERVICE — LOCKBIT

RaaS separates roles:

**Operator**

- develops ransomware;
- maintains infrastructure;
- provides negotiation platform.

**Affiliate**

- gains access;
- conducts intrusion;
- exfiltrates data;
- deploys ransomware.

Revenue is shared.

Source uses the May 2025 LockBit affiliate-panel breach as a window into a mature RaaS operation.[2]

Leaked backend reportedly showed:

- tiered affiliate management;
- standardized tooling;
- formalized revenue sharing;
- customized payload builds;
- victim-specific configuration;
- negotiation records.

### Рисунок 180. LockBit Data Breach Defacement

THIRD_PARTY_REVIEW_REQUIRED.

### Рисунок 181. LockBit RaaS Database Schema

THIRD_PARTY_REVIEW_REQUIRED.

Source figures and narrative report:

- 1,183 ransomware builds;
- 631 unique organizations;
- five-month period;
- tags such as:
  - verified;
  - pentester;
  - newbie;
  - scammer;
- new affiliate access about $777;
- approximately 75 registered affiliates;
- common 20/80 operator/affiliate split;
- ransom demands ranging from about $3,800 to $4.5M;
- fewer than 10% of negotiations resulting in payment.

These details illustrate how industrialized RaaS has become.

# Multi-Vector Extortion Campaigns

Modern extortion combines multiple pressure channels.

### Таблица 50. Ransomware Extortion Strategies

| Attack technique | Description |
|---|---|
| Encryption | Disrupt operations and demand payment for decryption |
| Data Theft | Exfiltrate sensitive information and threaten disclosure |
| Data Leaks | Publish stolen data or contact customers/regulators |
| DDoS Attacks | Disrupt public services to increase pressure |
| Harassment | Contact executives, employees, customers, or regulators directly |

### Рисунок 182. Multi-Vector Extortion Campaign Tiers

THIRD_PARTY_REVIEW_REQUIRED.

Practical implication:

the problem is no longer merely “systems are encrypted.”

The organization may simultaneously face:

- operational disruption;
- data exposure;
- regulatory obligations;
- reputational damage;
- customer/partner pressure;
- executive harassment.

Preparation should include:

- data classification/mapping;
- legal/regulatory planning;
- customer/partner communications;
- crisis PR;
- technical and information-impact detection.

Scoping should evaluate:

- encrypted systems;
- accessed/exfiltrated data;
- business impact;
- reputational risk.

Response requires coordination among:

- IR;
- legal;
- communications;
- executive leadership.

Modern ransomware response therefore extends beyond restoration of encrypted systems.

# PREPARE

Preparation is the most effective ransomware-impact reduction phase.

General preparation is covered in the DAIR Prepare Activity.

This chapter adds ransomware-specific preparation for:

- crisis communications;
- CTI;
- employee training;
- identity/tier-0 hardening;
- resilient backup architecture.

# PREPARE — Ransomware-Specific Preparation

Source emphasizes repeatedly:

> Preparation is the most effective way to reduce ransomware impact.

Ransomware response after compromise is:

- complex;
- expensive;
- time-consuming.

Investment before an incident reduces:

- damage;
- recovery time;
- operational disruption;
- decision pressure.

# Crisis Communications and Public Relations

Ransomware creates immediate communication demand.

Preparation should include either:

- internal crisis-communications capability with IR experience;
- retainer with an external crisis-communications firm.

Do not wait until encryption is active to:

- find a PR partner;
- approve a spokesperson;
- draft first public language.

Information often escapes quickly because ransom notes can appear on hundreds or thousands of systems simultaneously.

Employees may:

- post on social media;
- contact friends/family;
- speak to journalists.

Without prepared messaging, external narratives may form before the response team understands the incident.

A ransomware crisis-communications plan should include:

- pre-drafted holding statements;
- designated external spokespersons;
- internal communication channels;
- instructions that only authorized staff discuss the incident publicly;
- escalation criteria for external communications support;
- social-media monitoring;
- coordination between:
  - IR;
  - legal;
  - communications;
  - leadership.

# THE VALUE OF A GOOD HOLDING STATEMENT

A holding statement is a short pre-approved message acknowledging that:

- an issue exists;
- investigation is underway;
- facts are still being gathered.

It avoids:

- silence;
- speculation;
- premature factual commitments.

Preparation should answer in advance:

- What do we say first?
- Who approves it?
- How do we avoid overstating or understating impact?

A generic template can still be valuable, e.g. a message stating that a technical issue affecting some systems is under active investigation.

The point is not polished PR copy; it is controlled, approved communication under pressure.

# CTI for Ransomware

Cyber Threat Intelligence supports ransomware preparation by identifying:

- active groups;
- current TTPs;
- infrastructure;
- likely defensive gaps.

Source recommends prioritizing **TTPs over payload-specific IOC** for proactive defense.

Why:

- payloads are often victim-specific;
- hashes change frequently;
- RaaS affiliates create custom builds;
- attacker behaviors are usually more stable.

### Listing 140. LockBit RaaS Database Victim Build Statistics

~~~sql
mysql> SELECT DATABASE();
+--------------+
| DATABASE()   |
+--------------+
| paneldb_dump |
+--------------+
1 row in set (0.00 sec)

mysql> SELECT COUNT(*) AS "Total Builds", COUNT(DISTINCT company_website) AS "Unique Orgs" FROM builds;
+--------------+-------------+
| Total Builds | Unique Orgs |
+--------------+-------------+
|         1183 |         631 |
+--------------+-------------+
1 row in set (0.01 sec)
~~~

Example of behavior-oriented detection:

Ransomware groups commonly attempt to destroy recovery options using commands/tools such as:

- \`vssadmin\`;
- \`wbadmin\`;
- \`bcdedit\`.

Detecting unexpected execution of those techniques is more durable than tracking one malware hash.

Important CTI sources:

- CISA/FBI/international advisories;
- ISACs;
- commercial CTI;
- vendor research;
- community/open-source threat tracking.

# Employee Training and Awareness

Social engineering remains a common ransomware entry path.

Training should help users identify:

- urgency/emotional manipulation;
- threats of immediate consequences;
- requests for credentials/financial information;
- shortened/untrusted URLs;
- lookalike domains;
- unexpected communications.

AI-generated phishing makes poor grammar/style less reliable as detection clues.

Training should therefore emphasize:

- verification procedure;
- known reporting channel;
- support-desk validation;
- process compliance.

## Help Desk Impersonation

Employees should know whether legitimate support staff will ever:

- ask for passwords;
- request installation of unfamiliar remote-access software;
- initiate unexpected remote-support sessions.

Source recommends clear organizational rules stating legitimate support will not request password disclosure.

## Continuous Training

Annual “click-through” compliance is insufficient.

Use:

- repeated engagement;
- phishing simulations;
- recognition/reporting metrics;
- follow-up feedback.

Useful metrics:

- reporting rate;
- click rate;
- time-to-report.

Users who report suspicious activity should receive:

- acknowledgement;
- next steps;
- feedback.

Ignored reports discourage future reporting.

# Identity, Access, and Tier-0 Protection

Modern ransomware actors aim to control the identity/administration layer before mass encryption.

Tier-0/high-value systems include:

- domain controllers;
- IdPs;
- remote management platforms;
- virtualization consoles;
- backup servers.

These platforms can become distribution mechanisms for broad ransomware deployment.

Preparation goals:

- prevent persistent global admin control;
- preserve options when primary identity systems are untrusted/unavailable.

Recommended measures:

- harden DCs, IdPs, remote management, virtualization, backup systems;
- minimize internet exposure;
- strong segmentation;
- aggressive patching;
- separate admin roles/credentials;
- avoid shared domain-admin accounts;
- use JIT privilege elevation;
- phishing-resistant MFA for privileged/remote access;
- monitor:
  - admin-group changes;
  - new privileged accounts;
  - unusual logons;
  - IdP/federation modifications;
- maintain tested break-glass accounts/procedures.

Break-glass access should use:

- separate credentials;
- strong storage/access controls;
- tabletop and technical testing.

Protecting tier-0 assets limits:

- broad ransomware distribution;
- backup destruction;
- identity takeover.

# Backups

Backups are the primary ransomware recovery mechanism, but attackers explicitly target them before encryption.

Targets include:

- backup servers;
- backup repositories;
- hypervisors;
- storage snapshots.

# THE CRUSHING DISAPPOINTMENT OF ENCRYPTED BACKUPS

Source describes a common ransomware-response failure:

leadership asks whether backups can restore operations, only to discover:

- backup repository contains ransom notes;
- backup server is encrypted;
- accessible backups were deleted;
- newest clean copy is months old.

The failure is architectural, not merely operational.

“Have backups” is insufficient.

Backup design should assume attacker has privileged network access.

Required resilience may include:

- immutable storage;
- air-gapped/offline copies;
- separate backup authentication;
- integrity monitoring.

Tabletop question:

> If attacker has domain-admin credentials, can they destroy our backups?

If yes, backup architecture has a critical ransomware-resilience gap.

# Ransomware-Resistant Backup Strategies

## Pull-Based Architecture

Prefer backup systems retrieving data from production rather than production pushing to backup.

Benefit:

- compromised production systems have less ability to overwrite/delete backup history.

## Network Isolation

Backup infrastructure should be accessible through:

- dedicated management networks;
- specialized agents.

A compromised workstation/DC should not have direct network path to backup storage.

## Immutability

Use:

- WORM;
- immutable retention;
- storage-layer snapshots.

Credential compromise should not permit deletion before retention expiry.

Snapshot methods may improve recovery speed for virtual workloads but can require more storage.

## Air-Gapped / Offline Copies

At least one copy should be disconnected from normal network access.

Examples:

- removable media;
- offline libraries;
- systems powered on only during controlled windows.

## Identity Separation

Backup administration should not automatically trust the same identity plane as production.

Options:

- separate IdP;
- dedicated local accounts;
- third-party authentication.

Compromised domain-admin credentials should not automatically grant backup control.

## Hypervisor-Level Protection

For virtual environments:

- snapshots;
- replication;
- separate hypervisor admin identity.

Source also notes replica-from-backup capabilities.[3]

This can let organizations restore priority workloads directly from backup data while production remains untrusted.

Cross-cloud storage with separate identity can add further isolation.

# Prioritize Critical Systems

Backup/recovery strategy should reflect business criticality.

Do not assume everything can be restored simultaneously.

Predefine recovery priority based on:

- mission-critical workloads;
- infrastructure dependencies;
- verified restoration paths.

# The 3-2-1-1-0 Backup Rule

Source extends traditional 3-2-1 to ransomware resilience.[4]

- **3** copies of data;
- **2** different media types;
- **1** off-site copy;
- **1** immutable or air-gapped copy;
- **0** recovery-verification errors.

The extra immutable/offline copy protects against privileged attacker access.

The zero-errors requirement shifts recovery from assumption to verification.

Organizations should test:

- actual restoration;
- Recovery Time Objective (RTO);
- Recovery Point Objective (RPO);
- data completeness.

Automated/scheduled restoration verification can detect broken backups before crisis.

Source warns ransomware recovery often takes much longer than theoretical estimates because hundreds of systems may require:

- restoration;
- validation;
- sequencing.

Use measured restore performance, not optimistic assumptions, when setting stakeholder expectations.

# Backups Are Your Last Line of Defense

Backups are insurance, not prevention.

Even excellent backup architecture does not replace:

- defense in depth;
- early detection;
- effective incident response.

# VERIFY/TRIAGE

General guidance comes from DAIR Verify/Triage.

Ransomware-specific verification focuses on:

- confirming ransomware;
- distinguishing encryption/data theft/extortion;
- communicating uncertainty;
- planning for extended response.

# Ransomware Verification Indicators

Common indicators:

- encrypted files;
- modified extensions;
- ransom notes;
- mass file modifications;
- widespread service disruption;
- failed backup jobs;
- shadow-copy deletion.

Early family identification helps responders:

- research decryptors;
- understand attacker behavior;
- identify likely evidence sources.

Ransom notes can contain:

- group name;
- contact channel;
- payment portal;
- victim identifier.

# PROTECT VICTIM IDENTIFIERS IN RANSOM NOTES

Victim IDs may grant access to ransomware negotiation portals.

Anyone with the identifier may be able to impersonate the victim in negotiation.

Therefore:

- do not post ransom notes publicly;
- do not forward unsanitized screenshots broadly;
- redact:
  - victim ID;
  - chat URL;
  - sensitive paths;
- restrict negotiation details to authorized:
  - response personnel;
  - legal counsel;
  - law enforcement.

Source cites incidents where leaked negotiation details contributed to attackers ending negotiations and publishing stolen data.[5][6]

### Рисунок 183. Ransom Note with Victim Identifier

THIRD_PARTY_REVIEW_REQUIRED.

Source cites Conti's 2021 warning that leaked negotiation details could trigger immediate data publication.[6]

Operational rule:

- treat ransom notes and negotiation details as confidential;
- instruct employees to report internally rather than photograph/post them;
- redact victim identifiers, chat URLs, and sensitive paths before broader distribution.

# Distinguishing Attack Types

Not every ransomware incident includes exfiltration.

Source cites Verizon DBIR data:

- 2025 report: ransomware/extortion appeared in 44% of reviewed breaches, up from 32% prior year.[7]
- 2024 report: pure extortion 9% of breaches versus encryption-based ransomware 23%.[8]

Data theft as a parallel extortion lever became prominent around 2019, with Maze cited as an early adopter.[9]

### Таблица 51. Attack Type Indicators

| Attack type | Indicators |
|---|---|
| Encryption-only | Rapid/widespread file modification; limited prior attacker activity |
| Data theft + encryption | Longer dwell time; large outbound transfers; staging before encryption |
| Extortion without encryption | Threats referencing stolen data; no matching encryption activity |

Early classification affects:

- technical priorities;
- legal/compliance workflows;
- executive communications;
- staffing.

# Communicating with Decision Makers

Ransomware response requires communication of uncertainty.

Separate:

- confirmed;
- suspected;
- still under investigation.

Source example framing:

- attacker likely accessed customer-data file server;
- exact files/exfiltration are not yet known;
- team expects improved visibility within a defined investigation window.

Early incident briefings may occur every few hours, later daily.

Communication should:

- show progress;
- avoid overpromising;
- acknowledge that some questions may never be answered conclusively.

# THE INCIDENT COMMANDER ROLE IN RANSOMWARE RESPONSE

Ransomware produces sustained requests from:

- executives;
- legal;
- insurers;
- communications;
- external parties.

An Incident Commander (IC) acts as a single coordination point so analysts are not constantly interrupted.

IC does not have to be the most technical person.

IC needs:

- technical literacy;
- business awareness;
- communication skill;
- ability to translate findings into decisions;
- comfort saying:
  - “we don't know yet”;
  - “the timeline changed.”

Organizations should identify/train IC candidates before incidents and exercise the role in tabletops.

# Resource Planning for Extended Response

Ransomware response may last:

- weeks;
- months.

Triage should consider early engagement of:

- external forensics;
- legal counsel;
- crisis communications;
- negotiation expertise;
- regulatory specialists.

Decision makers need realistic estimates of:

- duration;
- specialist skills;
- cost/resource demand.

# SCOPE

Ransomware scoping should generally be broader than visible encryption.

The largest failure mode is scoping only:

- encrypted hosts.

Responders must also find systems the attacker:

- accessed;
- authenticated to;
- used for staging;
- used for persistence;
- used for exfiltration;
- used for credential theft.

Incomplete scope causes:

- incomplete containment;
- missed data exposure;
- attacker persistence;
- prolonged recovery.

# Framework for Ransomware Scoping

### Таблица 52. Ransomware Scoping Checklist

| Category | Key questions |
|---|---|
| Incident Overview | How detected? Known impacted hosts? Actions already taken? Sensitive assets? Backups? Current diagrams? |
| Host Inventory | Windows/Linux/macOS/ESXi count? Domain joined? Virtualization? Backup locations? |
| Host Data Sources | Windows Event Logs retention? Linux audit/syslog? App logs? EDR? |
| Network Data Sources | Firewall? VPN auth? NetFlow? NDR? |
| Security Systems | SIEM contents? EDR coverage? AV/endpoint protection? Entra ID/CloudTrail? |
| Cloud Logging | AWS/Azure/GCP? CloudTrail/Azure Monitor? Retention? SaaS logs such as M365/Google Workspace? |

This supports:

- environment understanding;
- evidence-source mapping;
- collection planning.

# Scoping Activities for Ransomware

## Identify All Affected Systems

Do not limit scope to visibly encrypted hosts.

Include every system attacker:

- accessed;
- authenticated to;
- used for tooling;
- used for staging.

## Determine Data Exposure

Review:

- file servers;
- databases;
- document repositories;
- backups;
- other sensitive-data systems.

## Map Lateral Movement

Reconstruct:

- initial access;
- credentials/vulnerabilities used;
- systems traversed;
- final encryption targets.

## Identify Persistence

Examples:

- backdoors;
- scheduled tasks;
- registry changes;
- unauthorized accounts.

## Establish Timeline

Determine:

- initial access;
- dwell time;
- exfiltration window;
- encryption time.

This is essential for selecting clean restore points.

# ERADICATE

Ransomware eradication has two parallel objectives:

1. determine what data was accessed/exfiltrated;
2. remove attacker presence.

Recovery should not proceed until both are sufficiently addressed.

# Assessing Data Access and Exfiltration

Data exposure affects:

- breach notification;
- regulatory obligations;
- business risk;
- extortion assessment.

Useful evidence:

## AAA / Authentication Records

Where did compromised identities authenticate?

## File Access Telemetry

Which files were opened/copied/modified?

## Network Shares

Which shares/file servers were browsed?

## Databases

Did attackers connect to sensitive databases?

Data classification helps translate technical findings into impact.

Example:

“Attacker accessed backup server” becomes meaningful when responders know the server contains:

- customer PII;
- financial records;
- other regulated data.

# Investigative Techniques for Data Exfiltration Hunting

Attackers often stage data before transfer.

### Таблица 53. Exfiltration Hunting Techniques

| Technique | What to look for |
|---|---|
| Archival artifacts | WinRAR/7-Zip/native compression; archive history; password-protected archives split into 1–2 GB pieces |
| Staging locations | \`C:\Users\Public\`, \`C:\Perflogs\`, \`%TEMP%\`, hidden/public shares |
| Exfiltration tools | WinRAR, 7-Zip, FileZilla, WinSCP, rclone, Mega, Dropbox, cURL, Wget, FTP |
| Deleted artifacts | NTFS \`$UsnJrnl\`; file-system timeline; deleted archive creation/deletion |

Registry/artifact examples:

- \`NTUSER.DAT\Software\WinRAR\ArcHistory\`;
- \`NTUSER.DAT\Software\7-Zip\`.

# Data Exfiltration Detection Strategies

When exact stolen data is unknown, hunt anomalous movement.

Review:

- large outbound transfers;
- hosting providers;
- file-sharing/cloud-storage destinations;
- sudden traffic-volume spikes;
- creation of large archives in unusual locations.

### Рисунок 184. Cacti Network Monitoring Reveals Egress Data Transfer Spikes

THIRD_PARTY_REVIEW_REQUIRED.

UEBA may also help identify:

- archival tools run by unusual accounts;
- cloud-storage access from systems without normal business use.

# Decryption Possibilities

Before committing entirely to:

- backup restore;
- system rebuild;
- ransom decision;

check whether legitimate free decryption exists.

Possible sources:

## Implementation Vulnerabilities

Some ransomware contains cryptographic mistakes.

Less common in mature modern families, but still possible.

## Law Enforcement Operations

Seized infrastructure/keys have produced decryptors for families including:

- Hive;
- ALPHV/BlackCat;
- LockBit.

## Leaked Keys

Can result from:

- affiliate conflict;
- insider leak;
- operational-security failure.

## Security Research

Researchers/vendors may publish decryptors after finding implementation flaws.

# No More Ransom

Source identifies the No More Ransom Project as the primary repository for free ransomware decryptors.

It aggregates tools for over 150 ransomware families.

Other resources include:

- Kaspersky;
- Avast;
- Emsisoft;
- Bitdefender;
- law enforcement;
- security researchers;
- commercial decryption services such as Coveware Unidecrypt.

# Decryptor Limitations

For modern ransomware, free decryption may not exist.

Even valid decryptors may have constraints:

- family/version specific;
- incomplete file recovery;
- slow at enterprise scale;
- file corruption;
- poor scalability.

Responders should investigate decryption early while continuing in parallel with:

- clean backup planning;
- rebuild planning.

# DECRYPTOR LIMITATIONS — HSE Example

Source cites the 2021 Conti attack on Ireland's Health Service Executive.[10]

Even after obtaining a decryptor, restoration of critical healthcare services took approximately four months.

Lesson:

**Decryption is not recovery.**

Systems still require:

- validation;
- rebuild where needed;
- reintegration;
- security controls;
- eradication assurance.

Stakeholders should be told this early to avoid unrealistic timelines.

# Decryption Assessment Process

1. Identify the ransomware family.
2. Search No More Ransom/vendor/security resources.
3. Confirm decryptor matches exact variant/version.
4. Test on sample files.
5. Measure time/resource needs.
6. Plan prioritized decryption.
7. Back up encrypted data before attempts.
8. Execute on copies/dedicated systems where possible.
9. Validate recovered data and monitor progress.

Where a working decryptor exists, it can be the least costly recovery path, but it must be tested before broad use.

# RECOVER

Recovery is often the longest and most resource-intensive ransomware phase.

Organizations frequently underestimate recovery, especially when attackers compromise:

- domain controllers;
- identity platforms;
- backup systems;
- virtualization infrastructure.

Paying ransom and receiving a decryptor does not mean the organization will be operational within hours.

# Recovery Planning and Prioritization

Recovery order should reflect:

- business criticality;
- infrastructure dependencies;
- clean-data availability;
- regulatory deadlines;
- available staff/hardware/licenses/vendor support.

Foundational services generally precede dependent applications.

Important questions:

- Which systems are required to resume critical operations?
- What workarounds can sustain the business?
- What resources can accelerate priority-system recovery?

Priorities should be agreed with decision makers.

# Restoration from Backups

Backup restoration is preferred when:

- backups are available;
- backups are verified clean.

Critical requirements:

## Clean Restore Point

Restore point must predate **initial compromise**, not merely encryption.

An IAB or affiliate may have been present weeks/months before encryption.

## Backup Infrastructure Verification

Confirm:

- backup server not compromised;
- repository not manipulated;
- control plane not attacker-controlled.

## Backup Integrity

Test restore in isolation before production use.

## Data-Loss Acceptance

Data created after the last clean restore point may be lost.

Challenges include:

- uncertain dwell time;
- old clean backups;
- large restore volume;
- long transfer/restoration time.

# System Rebuild

For high-trust infrastructure, rebuild may be safer than restoration.

Especially consider rebuild for:

- Active Directory domain controllers;
- identity infrastructure.

Attackers with domain-admin access can persist in:

- AD objects;
- Group Policy;
- trust relationships.

Restoring a compromised DC can reintroduce attacker access.

Rebuild is favored when:

- DC/identity infrastructure was compromised;
- backup cleanliness is uncertain;
- system is significantly outdated;
- validation time exceeds rebuild time.

# Decrypted Does Not Mean Clean

A decrypted system still contains whatever existed before encryption:

- attacker tools;
- backdoors;
- persistence;
- compromised configs.

Therefore:

> Decryption restores data accessibility, not security trust.

Validate or rebuild decrypted systems before production return.

# Watching for Attacker Return

Ransomware victims may face elevated re-attack risk, especially after payment.

Source reasoning:

- payment demonstrates willingness to pay;
- attacker access/root cause may remain;
- victim details may circulate among criminal groups.

Maintain heightened monitoring:

- TTP-specific detections;
- privileged-authentication monitoring;
- C2/network monitoring;
- hunting for group-associated artifacts.

Recovery is complete only when:

- attacker access eliminated;
- enabling vulnerabilities remediated;
- organization has reasonable confidence in restored trust.

# Communication During Recovery

Ransomware recovery can span weeks/months.

Communication needs sustained management.

## Internal Communication

### Leadership Updates

Focus on:

- business impact;
- recovery progress;
- resource requirements;
- decisions required;
- realistic timelines.

Cadence example from source:

- daily during active recovery;
- transition to weekly later.

### User Communication

Users need:

- service availability;
- workarounds;
- expected timelines.

Do not repeatedly provide unrealistic optimistic dates.

### Recovery Team

Multiple teams may include:

- infrastructure;
- applications;
- security;
- business units.

Use regular coordination and document:

- priorities;
- dependencies;
- decisions;
- assignments.

## External Communication

Coordinate through:

- technical teams;
- legal;
- communications;
- leadership.

### Regulatory Notifications

Potential frameworks/laws mentioned:

- HIPAA;
- state breach laws;
- GDPR;
- NIS2;
- DORA;
- SEC 8-K transparency reporting;
- sector-specific obligations.

Legal counsel should identify applicable deadlines.

### Customers and Partners

May require notice about:

- disruption;
- exposure;
- process changes.

Messaging should be legally and operationally coordinated.

### Cyber Insurance

Contact carrier early, ideally before:

- engaging outside forensics;
- executing major remediation;
- signing vendor contracts.

Policies may specify:

- approved vendors;
- evidence handling;
- prior approvals.

Failure to notify early can jeopardize cost coverage.

### Law Enforcement

Coordinate disclosure to avoid compromising ongoing investigations.

# DEBRIEF

Ransomware debrief converts incident cost/disruption into measurable improvements.

Failure to:

- eradicate fully;
- remediate root causes;
- implement lessons;

can lead to repeat ransomware.

General AAR guidance comes from Debrief Activity.

Ransomware-specific debrief should address:

# Ransomware-Specific Debrief Questions

## Backup and Recovery

- Did backups survive?
- If not, why?
- What architecture would have protected them?
- How did real recovery time compare to RTO?
- Was data loss accepted?

## Dwell Time

- How long before encryption?
- What detection opportunities existed?
- Could earlier detection have reduced/prevented encryption?

## Data Exfiltration

- Can organization determine what data was accessed/exfiltrated?
- What logging gaps created uncertainty?
- How did uncertainty affect notification?

## Ransom Decision

If payment considered/made:

- Did policy work?
- Were decision makers prepared?
- Did decryptor work?
- If no payment, what happened to stolen data?

## Multi-Vector Extortion

How effectively did:

- legal;
- communications;
- executives;
- technical responders;

coordinate across leak/harassment/reputation pressure?

## Identity and Privilege Exposure

- Which privileged accounts were compromised?
- Was credential scope understood?
- Were break-glass procedures needed?
- Did they work?

# Ransomware-Specific Metrics

Beyond standard MTTD/MTTR, source recommends considering ransomware-specific metrics.

### Таблица 54. Ransomware-Specific Metrics

| Metric | Description | Value |
|---|---|---|
| Attacker dwell time | Initial access → encryption | Measures detection opportunity |
| Backup survival rate | Percentage of backups remaining usable | Measures ransomware resilience |
| Data exfiltration confidence | High/medium/low/unknown confidence about accessed data | Measures logging/monitoring maturity |
| Recovery method distribution | Restored vs rebuilt vs decrypted | Validates recovery strategy |
| Encryption spread rate | Systems encrypted per hour | Measures containment effectiveness |

These metrics are opportunities, not mandatory fields for every incident.

Select metrics based on:

- organizational priorities;
- available data;
- consistency across incidents.

Sharing anonymized metrics through:

- ISACs;
- industry reports;
- community forums;

can improve collective resilience.

# WHEN RECOVERY LESSONS STAY BEHIND CLOSED DOORS

Source uses the October 2019 Ryuk attack against DCH Health System.[11]

Reported impact:

- three hospitals in Tuscaloosa County;
- diversion protocols;
- paper-based clinical workflows;
- ransom payment;
- staged decrypt/test/restore;
- thousands of devices;
- diversions lifted around ten days after attack start.

Public reporting contained little detail about operational restoration sequence.

Source argues that high-value lessons often remain private:

- which clinical systems restored first;
- sequencing;
- failed/successful recovery approaches;
- backup survival;
- workflow adaptations.

Sharing anonymized recovery data could help hospitals prepare without exposing sensitive incident specifics.

# FINAL CONSIDERATIONS

Ransomware stresses every aspect of IR.

Strongest outcomes come from:

- preparation;
- practiced teams;
- resilient business processes;
- technical defenses.

# The Human Element

Long incidents create:

- fatigue;
- burnout;
- decision degradation.

Plan for:

- shift rotation;
- rest;
- support resources;
- cross-training.

Avoid single points of failure in staffing as well as infrastructure.

# A HANGRY RESPONSE TEAM IS NOT AN EFFECTIVE RESPONSE TEAM

Source emphasizes a practical leadership lesson:

response teams working very long days need active support.

Leadership should:

- empower technical decision-making;
- remove unnecessary procurement/access friction;
- shield responders from organizational politics;
- provide food, water, coffee, and practical logistics for all shifts.

This is framed not as a perk but as a performance/reliability control.

Exhausted teams:

- make more mistakes;
- lose focus;
- burn out faster.

# Legal and Regulatory Complexity

Ransomware intersects with:

- breach-notification laws;
- sector regulations;
- contractual obligations;
- sanctions;
- potential litigation.

Technical responders should not navigate this alone.

Engage legal counsel early, preferably counsel experienced in ransomware.

# AI as an Evolving Ransomware Threat

Source argues that historical assumptions linking attack complexity to attacker skill are becoming less reliable.

AI coding/agent systems can give less-skilled actors operational capability across:

- reconnaissance;
- exploitation;
- lateral movement;
- data exfiltration;
- tooling development.

# AI Across the Attack Lifecycle

AI is moving from advisory support to active execution of attack phases.

Source cites documented cases where AI systems performed:

- scanning;
- credential harvesting;
- lateral movement;
- exfiltration;

with limited human oversight.[12]

Anthropic's November 2025 report is cited as claiming AI performed approximately 80–90% of operational work in one campaign, with only a small number of human decision points per engagement.[13]

Operational implication:

a single operator may conduct parallel, technically complex campaigns against multiple organizations.

# AI-Optimized Extortion

Extortion requires selecting the data most likely to create leverage.

AI can accelerate review of large stolen datasets by classifying:

- PII;
- financial data;
- health data;
- trade secrets;
- regulatory-sensitive material.

AI can also relate stolen data to likely:

- notification requirements;
- penalties;
- reputational consequences.

Source cites Anthropic August 2025 reporting on actors using AI to create victim-specific monetization strategies.[14]

Reported extortion options included:

- direct organization ransom;
- resale of stolen data;
- individual targeting;
- regulatory leverage.

Reported demands in that cited case ranged from roughly:

- $75,000;
- to $500,000;

calibrated to organizational size, industry, and exposure.

AI may also generate:

- targeted negotiation messaging;
- victim-specific ransom notes;
- financial figures;
- regulatory references;
- adaptive communication based on victim responses.

# AI-Generated Ransomware Development

Source cites cases in which actors with limited development skill used AI to produce sellable ransomware packages.[15]

Reported packages:

- approximately $400–$1,200;
- ChaCha20 encryption;
- EDR-evasion techniques;
- anti-analysis capabilities.

AI permits iterative feature development through repeated model interaction.

Potential consequence:

- more ransomware families;
- lower barrier to RaaS participation;
- greater campaign volume.

# Attribution Complexity

AI-generated code may reflect model-specific coding patterns rather than an individual developer's distinctive style.

This makes attribution from code characteristics less reliable.

Source gives examples of model-family differences such as:

- Claude Sonnet;
- GPT/Codex generation patterns.

Core point:

AI adds another confounder to already difficult ransomware attribution.

# AI for Defenders

The same capabilities can accelerate defenders.

Chapter 16 use cases apply here:

- preparation;
- IOC analysis;
- containment support;
- evidence collection;
- recovery guidance.

Organizationally grounded AI can use:

- playbooks as skills;
- RAG;
- internal procedures;
- infrastructure context.

Source conclusion:

AI-enhanced attacks make foundational ransomware preparation **more** important, not less.

Key defensive foundations remain:

- identity protection;
- backup resilience;
- detection;
- preparation.

# Recovery Is Not the End

Technical recovery does not end ransomware impact.

Long-tail consequences include:

- regulatory review;
- litigation;
- insurance claims;
- stakeholder trust;
- extortion/data-leak risk.

# Regulatory and Legal Exposure

Notification and legal timelines may continue long after systems return.

Possible post-recovery work:

- regulator inquiries;
- evidence production;
- discovery;
- depositions;
- breach litigation.

Maintain access to:

- documentation;
- evidence;
- knowledgeable personnel.

# BLACKBAUD: FOUR YEARS OF REGULATORY CONSEQUENCES

Source uses the 2020 Blackbaud ransomware incident as a long-tail case.[16]

Reported chronology:

- attacker gained access February 7, 2020;
- remained undetected for more than three months;
- intrusion discovered in May 2020;
- data from about 13,000 customer organizations was exfiltrated;
- exposed data reportedly included:
  - SSNs;
  - bank details;
  - healthcare information;
  - donation histories.

Blackbaud reportedly paid about $250,000 in Bitcoin for a promise of deletion, which could not be independently verified.

Source notes customer notification delay and incomplete early disclosure of breach scope.

Regulatory consequences cited:

- March 2023 — SEC: $3M penalty;
- October 2023 — 49 states + DC: $49.5M settlement;
- May 2024 — FTC settlement with 20 years of security oversight/data deletion requirements;
- June 2024 — California AG: $6.75M additional fine.

Source states combined regulatory penalties exceeded $59M.

Lesson:

post-incident regulatory scrutiny evaluates not only the security failure but also:

- notification timing;
- disclosure accuracy;
- data-retention practices;
- representations made to affected parties.

# Insurance Resolution

Cyber-insurance claims may continue months after incident closure.

Carriers may request:

- detailed cost documentation;
- justification of response decisions;
- additional evidence;
- proof of covered services.

Preserve incident records and access to personnel who can explain decisions.

# Stakeholder Confidence

Customers, partners, and boards often expect evidence of improved posture, not merely service restoration.

Trust can be rebuilt through:

- concrete security investment;
- external assessments;
- enhanced monitoring;
- transparent communication.

Source uses Blackbaud to warn against minimizing severity in initial notifications.

Overly optimistic messages that later require correction can damage trust more than difficult but accurate communication.

# Ongoing Extortion Risk

Double-extortion actors retain stolen data regardless of payment.

Ransom payment buys a promise, not proof of deletion.

Data may later reappear because of:

- group conflict;
- affiliate splits;
- resale;
- infrastructure seizure;
- dishonesty;
- later re-extortion.

Therefore organizations should maintain:

- notification templates;
- legal response plans;
- customer communication procedures;
- incident context for possible future data exposure.

# KADOKAWA: PAYMENT DID NOT PREVENT DISCLOSURE

Source cites the 2024 BlackSuit attack on Kadokawa Corporation.[17]

Reported facts:

- attack: June 8, 2024;
- impact included Niconico;
- attackers claimed 1.5 TB stolen;
- initial extortion demand: $8.25M;
- source reports Kadokawa transferred about $2.98M in Bitcoin;
- stolen data was still leaked;
- later investigation confirmed exposure involving 254,241 individuals;
- stock price reportedly fell more than 20%;
- expected extraordinary losses about ¥2.3B (~$15M);
- full services resumed August 5, 2024.

Source notes BlackSuit fragmentation and former members moving to other operations as a possible explanation for broken commitments.[18]

Lesson:

criminal payment agreements are not enforceable guarantees.

# Prevention Remains Essential

Ransomware response capability is a fallback, not a substitute for prevention.

Preventive foundations include:

- strong access controls;
- current patching;
- effective endpoint protection;
- employee social-engineering awareness;
- identity protection;
- resilient backups;
- monitoring.

# Сноски и источники

[1] Chainalysis, "The 2026 Crypto Crime Report," March 2026, www.chainalysis.com/wp-content/uploads/2026/03/the-2026-crypto-crime-report-release.pdf

[2] Elsad, Amer, Gumarin, JR, and Barr, Abigail, "LockBit 2.0: How This RaaS Operates and How to Protect Against It," Palo Alto Networks Unit 42, June 2022, unit42.paloaltonetworks.com/lockbit-2-ransomware/

[3] Veeam, "Replica from Backup," Veeam Backup & Replication User Guide, helpcenter.veeam.com/docs/vbr/userguide/replica_from_backup.html?ver=13

[4] Veeam, "3-2-1-1-0 Backup Rule," www.veeam.com/blog/321-backup-rule.html

[5] Trend Micro Research, "What To Expect In A Ransomware Negotiation," October 2021, www.trendmicro.com/en_us/research/21/j/what-to-expect-in-a-ransomware-negotiation-.html

[6] Cimpanu, Catalin, "Conti gang threatens to dump victim data if ransom negotiations leak to reporters," The Record, October 2021, therecord.media/conti-gang-threatens-to-dump-victim-data-if-ransom-negotiations-leak-to-reporters

[7] Verizon, "2025 Data Breach Investigations Report," www.verizon.com/business/resources/reports/dbir/

[8] Verizon, "2024 Data Breach Investigations Report," www.verizon.com/business/resources/reports/dbir/

[9] Check Point Research, "Ransomware Evolved: Double Extortion," 2020, research.checkpoint.com/2020/ransomware-evolved-double-extortion/

[10] PricewaterhouseCoopers, "Conti Cyber Attack on the HSE - Independent Post Incident Review," December 2021, www.hse.ie/eng/services/publications/conti-cyber-attack-on-the-hse-full-report.pdf

[11] Petcu, Alina Georgiana, "The DCH Ransomware Attack: A Teachable Moment in Cyber-History," Heimdal Security, January 2021, heimdalsecurity.com/blog/dch-ransomware-attack/

[12] Anthropic, "Detecting and countering misuse of AI: August 2025," August 2025, www.anthropic.com/news/detecting-countering-misuse-aug-2025

[13] Anthropic, "Disrupting the first reported AI-orchestrated cyber espionage campaign," November 2025, www.anthropic.com/news/disrupting-AI-espionage

[14] Anthropic, "Detecting and countering misuse of AI: August 2025," August 2025, www.anthropic.com/news/detecting-countering-misuse-aug-2025

[15] Anthropic, "Detecting and countering misuse of AI: August 2025," August 2025, www.anthropic.com/news/detecting-countering-misuse-aug-2025

[16] Federal Trade Commission, "FTC Order Will Require Blackbaud to Delete Unnecessary Data, Boost Safeguards to Settle Charges its Lax Security Practices Led to Data Breach," February 2024, www.ftc.gov/news-events/news/press-releases/2024/02/ftc-order-will-require-blackbaud-delete-unnecessary-data-boost-safeguards-settle-charges-its-lax

[17] Antoniuk, Daryna, "Japanese game and anime publisher reportedly pays $3 million ransom to Russia-linked hackers," The Record, August 2024, therecord.media/kadokawa-japan-reported-ransomware-payment

[18] Lyngaas, Sean, "Details emerge on BlackSuit ransomware takedown," CyberScoop, August 2025, cyberscoop.com/blacksuit-ransomware-takedown/; citing Cisco Talos research indicating former BlackSuit members dispersed to new operations including the Chaos ransomware group.
