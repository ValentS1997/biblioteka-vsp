---
book_id: dynamic-incident-response-joshua-wright-en-2026
chapter_number: 12
source_title: "Contain Activity"
source_pdf_page_range: "244-299"
rag_chunk_range:
  first: "dynamic-incident-response-joshua-wright-en-2026:p0244:c01"
  last: "dynamic-incident-response-joshua-wright-en-2026:p0299:c01"
translation_status: "DRAFT_FOR_QA"
license_notice: "Неофициальный русский перевод / unofficial Russian translation; original work CC BY 4.0. См. ../ATTRIBUTION.md."
third_party_review_policy: "Figures and embedded third-party visuals remain fail-closed."
translation_notes:
  - "Canonical English RAG is source of truth."
  - "Assembled from full-fidelity source-range segments."
  - "Technical commands, code, identifiers, and source-authored listings are preserved."
---

# Глава 12. Сдерживание

Activity **contain — сдерживание** является поворотной точкой incident response: team переходит от определения breadth incident к decisive action против threat.

Containment преследует две цели одновременно:

- остановить attacker и предотвратить additional harm;
- сохранить evidence для investigation.

Баланс между aggressive action и careful evidence preservation требует technical sophistication и strategic thinking.

### Рисунок 74. Contain Activity Waypoint

THIRD_PARTY_REVIEW_REQUIRED — visual asset не воспроизводится автоматически; сохраняются caption и cross-reference.

Chapter рассматривает:

- containment objectives;
- implementation strategies;
- timing considerations;
- technical methods;
- cloud-specific challenges;
- remote-work containment;
- encrypted communications;
- validation containment success;
- documentation actions.

## CONTAINMENT OBJECTIVES

Containment имеет две primary objectives:

1. stopping attacker activity;
2. collecting and preserving evidence.

### Stopping Attacker Activity

Первая objective — не дать attacker продолжать malicious actions.

Раньше это часто означало physically unplug affected systems. Для modern distributed environments такой approach обычно непрактичен.

Современные containment strategies должны балансировать security и operations.

Typical techniques:

- network isolation;
- account restrictions;
- process termination.

**Network isolation** использует:

- private VLANs;
- ACLs;
- cloud security groups;
- software-defined networking.

Цель — ограничить movement attacker без полной остановки business.

Например, compromised web server можно isolate from internal systems, сохранив internet-facing service.

**Account restrictions** могут включать:

- password changes;
- privilege revocation;
- conditional-access policies.

Credential resets следует coordinate carefully: containment должен быть effective, но premature visible action может alert attacker.

**Process termination** прекращает known malicious processes, но также может alert sophisticated adversary.

Advanced attackers могут:

- использовать watchdog processes, respawning malware;
- accelerate ransomware encryption;
- trigger destructive payloads при обнаружении defensive action.

> Aggressive containment может backfire. Если attacker behavior ещё не полностью understood, subtle coordinated action часто safer, чем immediate process killing.

### Evidence Collection and Preservation

Вторая objective — сохранить critical evidence до того, как оно исчезнет или будет corrupted.

Evidence используется later для:

- understanding attacker TTPs;
- eradicate activity;
- attack reconstruction;
- legal action;
- impact assessment.

Collection следует prioritize by volatility.

**Memory acquisition**

Memory dumps могут сохранить:

- running processes;
- decrypted credentials;
- host configuration;
- active network connections;
- malware runtime state.

Tools:

- WinPMEM;
- Linpmem.

**Forensic imaging**

Full disk imaging сейчас используется реже из-за:

- storage cost;
- acquisition time.

Но selective imaging остаётся valuable для:

- initial compromise systems;
- systems with custom attacker tools;
- specific high-value directories.

**Log preservation**

Нужно сохранить:

- security logs;
- application logs;
- authentication records;
- network flow data.

Logs следует forward в centralized secure location сразу после compromise discovery, чтобы attacker не смог delete/modify local evidence.

## CONTAINMENT STRATEGIES

Organizations выбирают containment strategy по:

- incident specifics;
- operational impact;
- attacker awareness;
- monitoring maturity;
- risk tolerance.

Source рассматривает:

- passive containment;
- active containment;
- adaptive containment.

### Рисунок 75. Containment Strategy Evolution

THIRD_PARTY_REVIEW_REQUIRED — visual asset не воспроизводится.

### TERMINATE OR MONITOR: ORGANIZATIONAL CONSIDERATIONS

Containment часто требует выбора:

- immediately terminate attacker access;
- или продолжить monitoring для intelligence collection.

**Immediate termination** быстро останавливает:

- exfiltration;
- ransomware deployment;
- persistence creation;
- lateral movement.

Но premature action может alert attacker и вызвать:

- accelerated encryption;
- rapid data destruction;
- faster fallback/persistence activity.

**Continued monitoring** помогает понять:

- attacker objectives;
- techniques;
- full scope;
- targeted data;
- affected systems.

Это может быть особенно relevant во время ransomware negotiations, где partial isolation attacker infrastructure может trigger immediate encryption или changed demands.

Decision зависит от:

- risk tolerance;
- incident specifics;
- operational constraints;
- backup quality;
- forensic capability;
- system criticality;
- regulatory environment.

High-value/safety-critical/regulated systems обычно require immediate protection.

Organizations с mature monitoring и robust backups могут позволить себе short intelligence-gathering window.

### Таблица 16. Factors Influencing Containment Strategy Selection

| Factor | Passive | Adaptive | Active |
|---|---|---|---|
| Active destruction/ransomware underway | — | — | Required |
| Regulated data with compliance-driven timeline | — | — | Required |
| Safety-critical/high-availability system at risk | — | — | Required |
| Attacker aware of defenders | — | — | Strongly favored |
| Short dwell time / limited monitoring maturity | — | — | Strongly favored |
| Extended dwell time / mature monitoring | — | Strongly favored | — |
| Unknown scope / attacker sophistication uncertain | — | Preferred | — |
| Commodity malware on low-value asset | Possible | — | — |
| Controlled deception environment | Possible | — | — |

## Passive Containment

Passive containment ограничивает damage без явного disclosure defensive action.

Он полезен, когда organization:

- имеет strong monitoring;
- может tolerate limited continued attacker presence;
- хочет gather intelligence.

Monitoring attacker TTPs помогает:

- identify additional compromised systems;
- understand targeting;
- improve remediation planning.

Examples:

- observe lateral movement attempts;
- identify high-value targets;
- monitor C2 behavior.

**Honeypots/deception technologies** redirect attacker в controlled decoy systems без sensitive data.

Decoys должны быть clearly marked in backend systems, чтобы defenders отличали deception detections от production incidents.

> Passive containment uncommon in modern incidents. Capable attackers быстро замечают monitoring, accelerate actions или burn access. Strategy следует использовать в narrow scenarios: commodity malware, low-value assets, controlled deception.

## Active Containment

Active containment означает decisive action для stopping attacker, даже если это alerts adversary.

Use cases:

- active destruction;
- ongoing exfiltration;
- critical-system risk;
- insufficient monitoring maturity.

Typical measures:

**Network segmentation**

- firewall rules;
- ACLs;
- preconfigured isolation policies;
- physical disconnect where necessary.

**System isolation**

EDR can quarantine host while preserving management/forensic channel.

Source recommends prefer EDR isolation over coarse network isolation where possible, because EDR can continue:

- evidence collection;
- process inspection;
- remote investigation.

**Service disruption**

When other methods insufficient:

- stop compromised web service;
- disable RDP/SSH;
- shut down compromised business application.

Service disruption must be coordinated with business stakeholders and alternative workflows.

## WHEN RMM TOOLS TURN AGAINST YOU: THE STRYKER COMPROMISE

Stryker — large global medical-technology company with:

- approximately $25 billion annual revenue;
- about 56,000 employees;
- operations impacting hospitals and manufacturing.

In March 2026 attackers compromised Stryker Microsoft Intune environment.

Intune is a Mobile Device Management (MDM) platform.

Attackers used compromised management plane to remotely wipe devices:

- laptops;
- phones;
- other managed endpoints.

Source attributes attack to Handala, described as Iran-linked and believed connected to Void Manticore.

Handala claimed to have wiped more than **200,000 systems/devices**.

Stryker reportedly shut offices in **79 countries**.

Impact included:

- wiped devices;
- loss of eSIMs;
- loss of two-factor authentication;
- email/collaboration disruption;
- offices closed;
- staff instructed to stay off network/Wi-Fi;
- work phones advised to remove management profile.

### Рисунок 76. Stryker Facility Employee Notice

THIRD_PARTY_REVIEW_REQUIRED — third-party visual not reproduced.

Attack also affected manufacturing and digital product/supply-chain tooling.

At Cork, Ireland headquarters, more than **4,000 employees** lost network access, and regional manufacturing output slowed.

Lesson: remote-management platforms are both response tools and potential attack vectors.

If MDM/RMM is compromised, normal containment channel itself becomes untrusted.

Preparation should include:

- out-of-band communication;
- offline containment procedures;
- response methods independent of device-management infrastructure.

## Adaptive Containment

Adaptive containment evolves with attacker behavior and incident intelligence.

It combines passive and active methods.

### Progressive Restrictions

Measures increase over time according to observed behavior.

Example sequence:

1. monitor lateral movement;
2. identify attacker targets;
3. block high-value targets;
4. leave controlled low-value decoys accessible;
5. escalate to full active containment when needed.

### Deceptive Containment

Attacker believes access remains intact while actually operating in controlled environment.

Examples:

- redirect tools to honeypots;
- present realistic but false data;
- sandbox access;
- preserve observation while reducing production risk.

## TIMING AND COORDINATION

Containment timing affects both security outcome and business impact.

**Premature containment** may:

- alert attacker;
- accelerate destruction;
- trigger ransomware;
- reduce visibility before scope understood.

**Delayed containment** may:

- increase exfiltration;
- expand compromise;
- raise regulatory impact;
- increase remediation cost.

Organizations should define timing criteria before incidents where possible.

## Immediate Containment Triggers

Certain scenarios demand action even if scope incomplete.

These are examined in the next source range.

## Immediate Containment Triggers

Некоторые scenarios требуют immediate containment независимо от incomplete scoping.

### Таблица 17. Considerations for Immediate Containment

| Trigger | Indicators | Recommended action |
|---|---|---|
| Active Data Destruction | ransomware encryption spreading, event-log wiping, database tables dropped | Immediate isolation |
| Data Exfiltration | large transfers, bulk PII queries, archives sent external | Urgent containment |
| Safety/Critical Systems | ICS, medical devices, payment processing, safety-critical infrastructure | Immediate action |
| Regulatory Requirements | HIPAA, PCI DSS, GDPR, NIS2, DORA, CRA и equivalent frameworks | Rapid containment |

Regulatory examples in source are illustrative, not exhaustive.

European organizations should additionally consider:

- NIS2;
- DORA;
- CRA;
- PSD2;
- UK FCA operational resilience PS21/3;
- sector/jurisdiction-specific obligations.

> Ideally decision makers define applicable triggers during Prepare activity and map each trigger to pre-approved actions. This avoids fresh policy interpretation under incident pressure.

### Active Data Destruction

Самый urgent trigger.

Examples:

- ransomware encrypting shares;
- attackers wiping logs;
- database tables being dropped.

Modern ransomware can encrypt thousands files per minute, поэтому delays directly increase loss and recovery effort.

### Ongoing Data Exfiltration

Urgent containment especially important for:

- intellectual property;
- customer records;
- regulated information;
- large database exports;
- archives transmitted to external sites.

Example: compromised service account executes bulk sensitive PII queries and communicates with suspicious external IP.

Containment may be justified before initial compromise path is known.

### Safety/Critical Systems

Immediate action warranted when attacker activity threatens:

- ICS;
- medical devices;
- payment infrastructure;
- safety-critical systems;
- business-critical systems.

These environments often cannot tolerate extended attacker presence for intelligence gathering.

### Regulatory Requirements

Regulatory frameworks may impose notification/response expectations that effectively favor rapid containment.

Source references:

- HIPAA;
- PCI DSS;
- GDPR.[2][3][4]

Severity may depend on:

- affected record count;
- duration unauthorized access;
- data sensitivity.

Example: unauthorized access to Protected Health Information database should be contained within hours rather than days where possible, to limit exposure population and legal/regulatory impact.

## Coordinated Containment

Multi-system incidents require coordinated action to prevent attacker pivoting.

### Simultaneous Isolation

If attacker controls multiple systems, sequential isolation can alert them.

Risks of one-at-a-time containment:

- privilege escalation;
- new persistence;
- destructive payload activation;
- move to not-yet-contained hosts.

Coordinate:

- network team;
- endpoint team;
- identity team;
- application team.

Example: 15 compromised workstations across 3 departments can be isolated through simultaneous:

- EDR isolation;
- VLAN/firewall restrictions;
- account disabling.

> Sequential containment is a common mistake. Narrow execution windows reduce attacker reaction time.

### Credential and Infrastructure Coordination

Credential theft may require environment-wide reset strategy.

Reset sequencing should prioritize:

1. most privileged accounts;
2. service accounts;
3. potentially all users.

Coordinate with business units and maintenance windows.

#### Kerberos Golden Ticket Example

For suspected Golden Ticket:

1. reset KRBTGT account;
2. reset KRBTGT **twice** to invalidate existing tickets;
3. rotate Domain Administrator credentials;
4. rotate privileged service accounts;
5. rotate standard users.

Changes should occur in rapid succession to reduce re-entry window.

Infrastructure changes such as broad firewall rules or topology modifications require:

- planning;
- testing;
- rollback;
- network-operations coordination.

Poorly scoped containment can itself create outage or new exposure.

## TECHNICAL IMPLEMENTATION

Containment operates across multiple control layers.

### Рисунок 77. Containment Implementation Layers

THIRD_PARTY_REVIEW_REQUIRED — visual asset not reproduced.

## Network-Level Containment

Network controls can rapidly manage many systems.

### Network Isolation Techniques

**VLAN isolation**

Move compromised systems into quarantine segment with restricted access.

Private VLANs can preserve management connectivity while blocking attacker lateral movement.

**Firewall rules**

Block:

- protocols;
- ports;
- destinations;
- known C2 addresses.

Rules should preserve business-critical traffic and be refined as intelligence improves.

**Micro-segmentation**

Use:

- host firewalls;
- SDN controls;

when network-wide controls are too broad.

**Route manipulation**

Large organizations can redirect network ranges into containment infrastructure.

This requires network-engineering coordination due outage risk.

## DNS Sinkholes

DNS sinkhole redirects attacker domains to internal systems.

Benefits:

- stops C2 hostname resolution to attacker infrastructure;
- preserves visibility through DNS/redirect logs;
- helps identify additional compromised systems.

Source example attacker domain:

`www[dot]thirtjo13ht[dot]top`

Adding `thirtjo13ht[dot]top` to internal DNS redirects C2 traffic to quarantine server.

### Рисунок 78. DNS Resolution Resolves Attacker C2 Server

THIRD_PARTY_REVIEW_REQUIRED.

### Рисунок 79. DNS Sinkhole Redirects Attacker C2 Traffic

THIRD_PARTY_REVIEW_REQUIRED.

### Sinkhole Limitations

DNS sinkholes do not work when attacker uses:

- hardcoded IP addresses;
- encrypted DNS;
- broad legitimate hosting domains.

Example malicious application:

`live-okta-verify[dot]vercel[dot]app`

Sinkholing whole `vercel.app` would disrupt legitimate users.

## DNS over HTTPS and Sinkhole Limitations

DoH encrypts DNS queries in HTTPS traffic.

Browsers such as Chrome/Firefox may use external DoH resolvers, bypassing traditional internal DNS controls.

Source example:

~~~bash
$ curl -H 'accept: application/dns-json' 'https://cloudflare-dns.com/dns-query?name=www.toteslegit.us&type=A'
{"Status":0,"TC":false,"RD":true,"RA":true,"AD":true,"CD":false,"Question":[{"name":"www.toteslegit.us","type":1}],"Answer":[{"name":"www.toteslegit.us","type":1,"TTL":300,"data":"172.104.10.22"}]}
~~~

Containment alternatives:

- local hosts-file overrides;
- local DoH server with precedence;
- browser group policy disabling public DoH;
- endpoint-management controls.

Host overrides require administrative control.

Unmanaged BYOD devices may remain outside sinkhole policy.

## Host-Level Containment

Host containment allows granular enforcement while preserving investigation access.

### EDR Isolation

EDR quarantine can:

- block attacker network access;
- retain management channel;
- preserve remote forensic access;
- allow evidence collection.

### Local Firewall

If EDR unavailable, configure host firewall to block traffic except required management paths.

Examples:

- Windows Firewall;
- Linux Netfilter/iptables.

Possible allowed dependencies:

- domain controllers;
- DNS;
- IR management systems.

### Process and Service Restrictions

Application-control technologies can block unauthorized execution.

Examples:

- Windows AppLocker;
- macOS Gatekeeper;
- Linux AppArmor.

Rules may target:

- publisher;
- path;
- hash;
- scripts;
- libraries.

## Application-Level Containment

Application-specific controls reduce business impact compared with full service shutdown.

### Web Application Firewalls

WAF can block malicious requests while preserving authorized access.

Examples:

- Cloudflare SaaS WAF;
- ModSecurity.

WAF is containment, not substitute for fixing underlying vulnerability.

### Database Access Restrictions

Controls can:

- limit compromised account queries;
- block large result sets;
- detect schema enumeration;
- monitor sensitive-table access.

Example product in source: IBM Security Guardium.

## AI Agent / MCP Containment

Organizations increasingly use AI agents with broad internal-system access through frameworks such as Model Context Protocol (MCP).

Potential agent capabilities:

- query databases;
- access file systems;
- send messages;
- execute code.

Containment must account for:

- compromised human accounts invoking agents;
- prompt-injection/platform exploits;
- agent service principals/API keys independent from user credentials.

Actions may include:

- disable agent tool access;
- disable MCP server connections;
- revoke service principals/API keys;
- monitor generated outputs for data leakage.

> Revoking user credentials may not revoke AI-agent integration credentials. These should be inventoried during Prepare.

## Identity and Access Management Containment

Modern containment often treats identity as primary security perimeter.

IdP becomes control plane across:

- hybrid cloud;
- remote work;
- SaaS.

Comprehensive identity containment requires:

1. credential invalidation;
2. active-session termination;
3. persistent-token revocation;
4. conditional-access enforcement.

The next source range expands these procedures.

## Identity and Access Management Containment

### Рисунок 80. Identity and Access Management Containment Steps

THIRD_PARTY_REVIEW_REQUIRED — visual asset not reproduced.

Если containment требует temporary accounts — например, чтобы сохранить admin access после bulk reset или работать с isolated system, — IRT должна document каждый account at creation:

- purpose;
- intended lifespan;
- owner.

Closure activities затем review accounts на retention/removal.

## Credential Revocation

Containment begins с invalidation compromised credentials wherever they exist.

Actions:

- reset user passwords through primary IdP;
- rotate service-account credentials;
- rotate application credentials;
- revoke API keys;
- revoke programmatic access tokens.

Если account synced между multiple identity systems, revoke/reset во всех relevant locations.

Example:

- on-prem Active Directory;
- Microsoft Entra ID.

Synchronization delay может создать brief window, где old credential ещё valid in one environment.

Также нужно revoke credentials в:

- federated partner directories;
- SaaS platforms with cached authentication;
- separate local identity stores.

### Order-of-Operations Problem in Isolated Environments

Credential revocation может зависеть от connectivity.

Если team сначала cuts internet/network access:

- cloud IdP не сможет push invalidation;
- isolated servers may retain local auth cache;
- stolen credentials могут continue working until cache expiry.

Source recommends:

- complete credential revocation before broad isolation;
- либо preserve trusted management path through isolation posture.

## Active Session Termination

Password reset alone недостаточен.

Existing authenticated sessions могут survive credential change.

После reset нужно terminate active sessions.

Modern IdPs often offer:

- revoke-all-sessions;
- token invalidation;
- session-cookie invalidation.

### Residual-Access Window

Interval between credential revocation and session termination — measurable attacker-access window.

Attacker with live VPN session may:

- initiate password reset;
- enroll new MFA factor;
- establish persistence.

Source recommends define in-incident SLA during Prepare:

- IRT → account-management handoff target;
- session termination target;
- exercise actual timing to verify achievable SLA.

### SaaS Session Persistence

IdP revocation affects applications only if they validate session state against IdP.

Some SaaS applications:

- cache session state;
- issue local session cookies;
- retain sessions after IdP revocation.

For privileged/high-risk accounts it may be necessary to contact SaaS provider support for:

- forced logout;
- application-level session invalidation.

### VPN / RDP / SSH Sessions

Containment must address active connections across all authentication mechanisms.

**VPN**

- find session by username/session ID;
- force disconnect in concentrator management interface.

**Windows RDP**

Use `qwinsta` and `rwinsta`.

### Listing 48. Windows RDP Server Session Query and Termination

~~~text
C:\> qwinsta /server:rdp-server01
 SESSIONNAME       USERNAME          ID  STATE   TYPE        DEVICE
 services                            0  Disc
>console           Administrator     1  Active  wdcon
 rdp-tcp#0         alice             2  Active  rdpwd
 rdp-tcp#1         admin             3  Active  rdpwd ①
 rdp-tcp#2         bob               4  Active  rdpwd

C:\> rwinsta 3 /server:rdp-server01
SUCCESS: The session was reset.
~~~

① Attacker RDP session.

**SSH**

Identify sessions with `who` or `w`, terminate target TTY/process.

### Listing 49. SSH Server Session Query and Termination

~~~text
$ who
admin    pts/0        2025-11-02 08:30 (192.168.1.140)
admin    pts/1        2025-11-01 02:53 (192.0.2.42) ①
alice    pts/2        2025-11-02 08:12 (192.0.2.10)
bob      pts/3        2025-11-02 08:20 (192.0.2.22)
$ sudo pkill -9 -t pts/1
$ who
admin    pts/0        2025-11-02 08:30 (192.168.1.140)
alice    pts/2        2025-11-02 08:12 (192.0.2.10)
bob      pts/3        2025-11-02 08:20 (192.0.2.22)
~~~

① Attacker SSH session.

## Enterprise Session Detection

Host commands do not scale.

A complementary method is SIEM correlation of:

- session-open event;
- without matching session-close event.

This applies to:

- RDP;
- SSH;
- RMM;
- cloud consoles.

For Windows RDP:

- Event ID 4624 / LogonType 10 = open;
- Event ID 4634 = close.

### Listing 50. Splunk SIEM Query for RDP Sessions Opened Without Close

~~~spl
index=wineventlog EventCode=4624 LogonType=10 ①
| fields _time, TargetUserName, TargetLogonId, IpAddress, Computer
| join type=left TargetLogonId ②
    [search index=wineventlog EventCode=4634
     | fields TargetLogonId, EventCode]
| where isnull(EventCode) ③
| table _time, TargetUserName, IpAddress, Computer
~~~

① Retrieve RDP logons.  
② Left join logoff events by TargetLogonId.  
③ Keep logons without matching close.

Equivalent logic can be adapted to other SIEM/session types.

## Refresh Token and Persistent Credential Revocation

Refresh tokens are persistence mechanisms.

They may remain valid for months and generate new access tokens after:

- password reset;
- active-session revocation.

Responders should revoke all refresh tokens for compromised account.

### Таблица 18. Token Types and Revocation Considerations

| Token type | Typical lifetime | Revocation method | Persistence risk |
|---|---|---|---|
| OAuth Access Token | Short, typically ~1 hour | Authorization-server API | Low |
| OAuth Refresh Token | Long, potentially months | IdP token management | High |
| OAuth Offline Access Token | Long / indefinite | IdP + possibly app-specific action | High |
| SAML Assertion | Minutes | Natural expiry + clear SP sessions | Medium |
| JWT | Variable | No native revocation; deny lists on resource servers | High |

For compromised service account in OAuth microservices environment:

- revoke access tokens;
- revoke refresh tokens;
- monitor token endpoint requests;
- verify no new tokens issued via old credentials.

Source recommends documenting token types/revocation capabilities during Prepare.

## Conditional Access Policy Implementation

After invalidating credentials/sessions, use temporary conditional-access controls to prevent re-authentication.

### Location-Based Restrictions

Block sign-ins from geographic regions tied to attacker infrastructure where legitimate business presence is absent.

This is layered control, not standalone defense.

### Device Compliance

Require authentication only from managed/compliant devices where possible.

This can block attacker use from unmanaged systems even when credentials are valid.

### Risk-Based Conditional Access

Integrate IdP risk signals and CTI.

### Рисунок 81. Risk-Based Conditional Access Policy Example

THIRD_PARTY_REVIEW_REQUIRED.

Policies may block sign-in when IdP detects:

- leaked credentials;
- impossible travel;
- suspicious IP infrastructure.

Sign-in-risk policies can require step-up phishing-resistant MFA for:

- unusual user agents;
- anomalous timing;
- unfamiliar device fingerprints.

## Multi-Application Containment Through SSO

SSO can centralize containment across connected SaaS applications.

Disabling account at IdP can block all apps that depend on central auth.

But responders must verify which apps actually use IdP.

Hybrid environments often include:

- SSO-connected SaaS;
- legacy apps with local credentials.

Example:

- Salesforce via Okta SSO;
- legacy ERP with same username in local auth store.

The latter requires separate disabling.

### MFA Enforcement

Where possible:

- enforce MFA at IdP;
- use phishing-resistant FIDO2 methods during containment;
- avoid relying only on SMS/TOTP for high-risk cases because they are more interceptable.

### Synchronization Delays

Some applications cache authentication state.

Track delay between IdP disable action and actual attacker activity cessation.

This informs future containment timing.

## Session Management Across Hybrid Environments

Users may have simultaneous sessions across:

- on-prem systems;
- cloud apps;
- VPN;
- browsers;
- mobile apps.

All may preserve access after primary credential action.

### Multi-Server RDP Enumeration

### Listing 51. Enumerate Active RDP Sessions Across Multiple Servers

~~~powershell
PS C:\> Invoke-Command -ComputerName server01,server02,server03 -ScriptBlock {qwinsta}

ComputerName : server01
SESSIONNAME       USERNAME        ID  STATE   TYPE        DEVICE
>console          administrator    1  Active
 rdp-tcp#12       jsmith           2  Active
 rdp-tcp#13       guest            3  Disc

ComputerName : server02
SESSIONNAME       USERNAME        ID  STATE   TYPE        DEVICE
>console          svc_backup       1  Active
 rdp-tcp#5        administrator    2  Active
 rdp-tcp#8        jdoe             3  Disc

ComputerName : server03
SESSIONNAME       USERNAME        ID  STATE   TYPE        DEVICE
>console          system           1  Active
 rdp-tcp#4        rwalker          2  Active
 rdp-tcp#6        analyst          3  Active
~~~

## Browser Session Management

SaaS sessions may survive via persistent cookies.

Some IdPs invalidate sessions by incrementing token/session version.

Source example: Microsoft Entra ID revoke-refresh-tokens behavior forces re-authentication on next request.

Containment should coordinate session termination across mechanisms simultaneously to reduce attacker reaction time.

Create an environment-specific session-termination checklist during Prepare:

- VPN;
- RDP;
- SSH;
- browser sessions;
- OAuth access tokens;
- refresh tokens;
- mobile app sessions.

## BACK-CHANNEL LOGOUT: A CRITICAL MISSING COMPONENT

Back-channel logout allows IdP to notify service providers when user logs out, terminating sessions ecosystem-wide.

Support remains limited.

Many integrations are proprietary, creating NxM integration problem:

- N service providers;
- M identity providers.

Source recommends making global session invalidation a procurement/RFP requirement.

It references emerging IETF Global Token Revocation work as a path toward standardized cross-application revocation.

## EVIDENCE COLLECTION DURING CONTAINMENT

Containment также используется для evidence collection, поддерживающего:

- further investigation;
- eradication;
- recovery;
- threat intelligence;
- timeline reconstruction.

После isolation affected systems analysts могут получить более reliable access к evidence без ongoing attacker interference.

### EVERY STEP IS FOR DATA COLLECTION

В PICERL и NIST SP 800-61 containment часто рассматривается как first moment, когда responders непосредственно получают control affected system и начинают volatile-data collection.

DAIR сохраняет эту логику, но расширяет её: **каждая activity incident response является opportunity for data collection**.

Collection goals by activity:

**Prepare**

Collect:

- baseline configurations;
- network topology;
- asset inventories;
- communication/escalation procedures.

**Identify / Detect**

Collect:

- initial logs;
- alerts;
- user reports;
- initial timeline markers;
- impact clues.

Network analysts prioritize:

- flow data;
- DNS.

Host analysts prioritize:

- process execution;
- local logging.

**Verify/Triage**

Collect:

- evidence supporting incident validity;
- risk classification data;
- decision-maker summaries;
- technical indicators.

**Scope**

Collect:

- lateral movement indicators;
- affected-system inventory;
- compromise timeline.

**Contain**

Collect:

- memory;
- active connections;
- processes;
- disk/system artifacts;
- logs;
- registry/configuration;
- attacker behavior.

**Eradicate**

Focus collection on:

- persistence;
- attacker tooling;
- remediation targets.

**Recover**

Collect:

- vulnerability-assessment results;
- patch deployment logs;
- control-validation results;
- root-cause evidence;
- remediation effectiveness.

DAIR iterative nature means data from one activity informs another:

- containment evidence may expand scope;
- eradication may expose Prepare gaps;
- recovery may drive detection improvements.

## Prioritized Collection

Collection should be prioritized by:

- volatility;
- investigative value;
- risk of evidence loss;
- operational/security cost of delay.

### Volatile Data Collection

Highest-priority volatile data includes:

- memory;
- active network connections;
- running processes;
- transient files/cache.

Memory can reveal:

- running malware;
- decrypted credentials;
- active C2;
- runtime configuration.

Tools mentioned:

- WinPMEM;
- Linux Memory Extractor (LiME).

Example: capture web-server memory before isolation/power cycle so web-shell in-memory configuration and active sessions are preserved.

### PRIORITIZED COLLECTION: ORGANIZATION-SPECIFIC APPROACH

DAIR generally advocates:

1. isolate;
2. collect.

Rationale:

- attacker may interfere with evidence before isolation;
- pre-containment collection may alert attacker;
- attacker may modify data;
- delay allows additional harm.

However, containment itself can destroy volatile evidence.

So organizations should explicitly balance:

- evidence loss from isolation;
- continued attacker-access risk.

Source example uses `Get-NetTCPConnection`.

### Listing 52. NetTCPConnection Output on Compromised Host

~~~text
PS C:\> Get-NetTCPConnection

LocalAddress     LocalPort RemoteAddress    RemotePort State
------------     --------- -------------    ---------- -----
::               445       ::               0          Listen
192.168.171.142  33318     151.101.118.172  80         TimeWait
192.168.171.142  33179     13.107.5.91      443        TimeWait
192.168.171.142  33174     172.183.7.192    443        Established
192.168.171.142  27288     192.168.1.140    4444       Established
192.168.171.142  1565      162.159.142.9    80         Established
~~~

Immediate isolation terminates those connections.

If external sources already preserve connection evidence, e.g.:

- NetFlow;
- Sysmon network events;
- NDR;

then isolation-first is safer.

If no alternative source exists, organization may decide collect-before-isolate.

## Persistent and Log-Based Evidence

Less volatile artifacts include:

- registry hives;
- event logs;
- temporary files;
- Prefetch;
- ShimCache;
- AmCache;
- browser cache/history.

These support execution-history and persistence analysis.

Network evidence:

- packet capture;
- NetFlow/VPC Flow Logs;
- firewall logs.

Application evidence:

- web-server logs;
- DB transaction logs;
- application audit logs.

These are important for:

- exfiltration analysis;
- impact assessment;
- notification scope;
- attacker-objective understanding.

# CLOUD CONTAINMENT

Cloud containment requires adaptation due:

- shared responsibility;
- control-plane attacks;
- multitenancy;
- misconfiguration;
- ephemeral resources.

## Cloud Security Demarcation

Cloud security demarcation = boundary between provider and customer security responsibilities.

### IaaS

Provider generally handles:

- physical hardware;
- hypervisor;
- provider network infrastructure.

Customer handles:

- IAM;
- OS;
- patching;
- applications;
- data protection;
- encryption/configuration.

### SaaS

Provider handles most infrastructure/application platform.

Customer typically handles:

- identity;
- access;
- data authorization;
- user controls.

### PaaS

Responsibility sits between IaaS and SaaS.

The exact line is product-specific.

### Рисунок 82. Cloud Security Demarcation Responsibility Summary

THIRD_PARTY_REVIEW_REQUIRED — visual not reproduced.

### CLOUD SERVICE AND RESPONSIBILITY DEFINITIONS

Broad IaaS/PaaS/SaaS labels are not enough to determine actual containment authority.

Source compares AWS EC2 vs AWS Lightsail.

**EC2**

Customer responsibility starts at OS/application level.

**Lightsail**

Although it can launch WordPress/Node.js/Drupal blueprints, customer may still own:

- OS patching;
- application security;
- service security;
- data protection.

Therefore responders should enumerate actual cloud products and review product-specific security responsibility documentation.

> Do not infer security responsibility solely from broad service category.

## Cloud Containment Objectives

Core goals remain:

- isolate compromised resource;
- preserve evidence;
- stop attacker;
- enable investigation/recovery.

Use cloud-native capabilities where appropriate:

- tags;
- snapshots;
- termination protection;
- deletion locks;
- IAM controls.

## Identity-First Containment

Cloud attacks often persist through identity rather than network position.

Critical credentials include:

- IAM access keys;
- service-account keys;
- OAuth tokens;
- refresh tokens;
- service principals.

Containment actions:

- disable access keys;
- terminate sessions;
- revoke tokens;
- rotate service-principal credentials.

Consider downstream automation dependencies.

Example: compromised service-account key used by critical pipeline requires:

- identify all consumers;
- update credentials everywhere;
- maintenance coordination;
- rollback plan.

Prepare should document privileged-identity dependencies in advance.

## Network Isolation Containment

In cloud IaaS:

- remove compromised instance from production auto-scaling/load balancing;
- keep instance running for forensics;
- modify security groups;
- modify NACLs;
- move to isolation VPC if supported;
- enable deletion/termination protection;
- create snapshots.

Storage cost should be weighed against forensic value during large incidents.

## Resource Tagging for Containment Visibility

Cloud tags help:

- mark resource status;
- link incident ticket;
- assign owner;
- record containment date;
- drive automated policy;
- support audit trail.

### Таблица 19. Incident Response Tagging Schemes

| Category | Purpose | Example |
|---|---|---|
| Status | Mark IR-controlled resource | Status:Quarantined |
| Case identifier | Link ticket | IR-Case:2026-001 |
| Containment date | Timeline/audit | ContainedDate:2025-10-27 |
| Analyst owner | Responsible responder | IR-Owner:jsmith@company.com |

### Таблица 20. Example Tag Set for a Contained EC2 Instance

| Tag | Purpose |
|---|---|
| Status:UnderInvestigation | Active IR |
| IR-Case:2026-001 | Ticket linkage |
| ContainedBy:security-team | Responsible team |
| ContainedDate:2025-10-27 | Timeline reconstruction |
| EvidencePreserved:Yes | Confirm snapshots |

Tags can apply across:

- EC2;
- volumes;
- NICs;
- load balancers;
- snapshots;
- security groups.

Temporary containment objects should also be tagged so they can be cleaned up after incident closure.

### Protecting Tag Integrity

Tags are meaningful only if attacker cannot remove/alter them.

Source recommends:

- define RACI for IR tag management;
- restrict tag write permissions via IAM;
- log tag changes to separate tamper-resistant destination.

This prevents attacker from removing `Status:UnderInvestigation` and disappearing from IR dashboards.

## IaaS Termination Protection

Termination protection prevents accidental or malicious deletion of contained cloud resources holding evidence.

Cloud admins and automation may routinely terminate instances, so a contained system can be destroyed by someone unaware of the investigation.

Protection introduces explicit additional step before deletion.

### AWS Example

### Listing 53. AWS CLI Command to Enable Termination Protection

~~~bash
$ aws ec2 modify-instance-attribute --instance-id i-1234567890abcdef0 --disable-api-termination
~~~

Replace instance ID with actual affected resource.

Azure and GCP provide equivalent protections.

### Таблица 21. Cloud Termination Protection Quick Reference

| Action | AWS | Azure | GCP |
|---|---|---|---|
| Enable protection | aws ec2 modify-instance-attribute --instance-id <instance-id> --disable-api-termination | az lock create --name IR-Preserve --lock-type CanNotDelete --resource-group <rg> --resource-name <vm> --resource-type Microsoft.Compute/virtualMachines | gcloud compute instances update <instance> --deletion-protection --zone <zone> |
| Verify status | aws ec2 describe-instance-attribute --instance-id <instance-id> --attribute disableApiTermination | az lock list --resource-group <rg> --resource-name <vm> --resource-type Microsoft.Compute/virtualMachines | gcloud compute instances describe <instance> --zone <zone> --format="value(deletionProtection)" |

Protection should extend where relevant to:

- EBS/persistent volumes;
- snapshots;
- databases;
- network configurations;
- other evidence-bearing resources.

Document protection state in incident tracking.

Remove protection only after:

- evidence preservation complete;
- legal hold requirements satisfied;
- authorized decision.

### Clone-Then-Terminate Pattern

If business insists compromised instance must be terminated before investigation completes:

1. clone/snapshot into isolated forensic account/subscription/project;
2. preserve attached storage;
3. restrict access to IRT;
4. collect RAM from original first if possible;
5. allow production termination.

Persistent artifacts survive clone; volatile memory/network process state does not.

Source gives equivalent patterns:

- AWS GuardDuty/Lambda → forensic AWS account;
- Azure Event Grid/Functions → forensic subscription;
- GCP Eventarc/Pub/Sub → separate project.

## SaaS Platform Containment

SaaS containment differs from IaaS because customer cannot access underlying infrastructure.

Responders are limited to provider-exposed:

- admin console;
- API;
- identity/session controls;
- provider support.

Primary priorities:

- reset password;
- set temporary random password if needed;
- revoke sessions;
- revoke refresh tokens;
- rotate API keys/client secrets/OAuth credentials;
- disable/freeze account.

Choose between disable and platform-specific freeze depending on investigation/data-access needs.

Source example for compromised Microsoft 365 administrator:

- reset password;
- revoke sessions;
- invalidate active auth tokens;
- disable sign-in;
- rotate service principals/app registrations created by compromised admin;
- timestamp actions.

## Third-Party Integration Containment

Compromised accounts may retain access through authorized integrations after human credential reset.

Containment includes reviewing/disabling:

- OAuth-connected applications;
- browser extensions;
- mobile apps;
- automation rules;
- outbound webhooks;
- CI/CD deployment keys;
- API tokens;
- bots/service identities.

After containment:

- replace secrets;
- re-authorize only verified integrations.

Example Slack administrator compromise:

- audit installed apps;
- disable unfamiliar OAuth apps;
- focus especially on broad permissions;
- remove unapproved external webhooks;
- revoke API tokens;
- review bot users.

## WHEN LEGITIMATE APPS LOOK LIKE COMPROMISE

Source recounts Microsoft 365 security assessment where team found application with broad permissions:

- read/send mail;
- access calendars;
- read SharePoint files.

Security team did not recognize it, initially resembling illicit consent-grant attack.[5]

Investigation showed it was CRM functionality enabled by Sales months earlier after salesperson approved OAuth consent.

Application was not necessarily malicious, but represented real security risk.

Lesson:

- broad permissions alone do not prove compromise;
- missing authorized-app baseline wastes investigation time;
- legitimate grants can hide malicious grants among noise.

### Рисунок 83. Entra ID Application Consent Grant

THIRD_PARTY_REVIEW_REQUIRED — product screenshot not reproduced.

Prepare should enumerate authorized applications in:

- Entra ID;
- Google Workspace;
- Okta;
- equivalent IdP.

### Рисунок 84. Entra ID Enterprise Application Configured Permissions

THIRD_PARTY_REVIEW_REQUIRED.

### Listing 54. Entra ID OAuth Consent Grant Enumeration

~~~powershell
Get-MgOauth2PermissionGrant -All | ForEach-Object {
    $sp = Get-MgServicePrincipal -ServicePrincipalId $_.ClientId
    [PSCustomObject]@{
        App=$sp.DisplayName;
        Scopes=$_.Scope;
        ConsentType=$_.ConsentType
    }
}
~~~

During containment compare current grants with baseline inventory.

## CONTAINMENT CHALLENGES

Modern environments create containment problems beyond traditional host isolation.

Source highlights:

- cloud/hybrid;
- encrypted communications;
- remote workers;
- non-host compromise.

## Cloud and Hybrid Environments

Cloud containment should leverage cloud-native controls and account for ephemeral infrastructure.

### API-Based Isolation

Provider APIs can modify:

- security groups;
- NACLs;
- IAM policies;
- firewall rules.

This allows rapid scalable containment.

Examples:

- AWS Security Groups;
- Azure NSGs;
- GCP firewall rules.

IaC such as Terraform/CloudFormation can version/control containment procedures.

### Listing 55. Azure CLI Example for Network Isolation

~~~bash
$ az vm show --name web-prod-01 -g rg-production-eastus2 --query   "networkProfile.networkInterfaces[0].id" -o tsv
/subscriptions/e7b3c1d9-a842-4f56-b6d1-8a3e5f902c4d/resourceGroups/rg-production-eastus2/providers/Microsoft.Network/networkInterfaces/web-prod-01-nic

$ az network nsg create --name IR-Quarantine-2025-042 -g rg-production-eastus2 -o none

$ az network nsg rule create --nsg-name IR-Quarantine-2025-042 -g rg-production-eastus2   --name AllowSSH-IR --priority 100 --direction Inbound --access Allow --protocol Tcp   --destination-port-ranges 22 --source-address-prefixes 198.51.100.10/32 -o none

$ az network nsg rule create --nsg-name IR-Quarantine-2025-042 -g rg-production-eastus2   --name DenyAllOutbound --priority 100 --direction Outbound --access Deny --protocol '*'   --destination-port-ranges '*' --source-address-prefixes '*'   --destination-address-prefixes '*' -o none

$ az network nic update --name web-prod-01-nic -g rg-production-eastus2   --network-security-group IR-Quarantine-2025-042 -o none
~~~

Purpose:

1. identify VM NIC;
2. create quarantine NSG;
3. allow SSH only from IR jump box;
4. deny outbound;
5. attach quarantine NSG.

## Serverless Containment

Serverless functions may have:

- no persistent host;
- no stable network presence;
- new runtime each invocation.

Traditional host isolation is ineffective.

Containment can:

- disable event triggers;
- preserve original code;
- replace function with deny-and-log implementation;
- revoke IAM/service permissions.

### Listing 56. AWS Lambda Deny-and-Log Function

~~~javascript
exports.handler = async (event) => {
    console.log('Lambda function invoked - logging request and rejecting');
    console.log('Event details:', JSON.stringify(event, null, 2));

    const response = {
        status: '403',
        statusDescription: 'Forbidden',
        headers: {
            'content-type': [{
                key: 'Content-Type',
                value: 'text/html'
            }]
        },
        body: 'Access Denied - Function in containment mode'
    };

    return response;
};
~~~

### Listing 57. Configure AWS Serverless Function

~~~bash
% head -4 index.js
exports.handler = async (event) ⇒ {
    // Log the entire event for analysis
    console.log('Lambda function invoked - logging request and rejecting');
    console.log('Event details:', JSON.stringify(event, null, 2));

% zip function.zip index.js
  adding: index.js (deflated 45%)

% aws --profile jwright lambda update-function-code   --function-name lambda-function-to-log-and-disable   --zip-file fileb://function.zip
~~~

Pattern also applies to:

- Azure Functions via deployment ZIP + Application Insights;
- GCP Functions via `gcloud functions deploy` + Cloud Logging.

## Multi-Cloud Coordination

Incidents spanning multiple providers require adaptation to different:

- isolation mechanisms;
- API interfaces;
- IAM models;
- security architectures.

AWS Security Groups, Azure NSGs and GCP firewall rules are not operationally identical.

Responders need provider-specific familiarity.

Hybrid/multi-cloud incidents may exceed standing IRT capacity both in:

- headcount;
- platform expertise.

Cloud administrators already possess:

- tooling access;
- IAM permissions;
- operational context.

Source recommends treating them as **co-opted IRT members**, not external ticket recipients.

Prepare activity should define:

- on-call pathway;
- authorization scope;
- communication channels;
- temporary IR role.

### Таблица 22. Multi-Cloud Containment Quick Reference

| Containment action | AWS | Azure | GCP |
|---|---|---|---|
| Network isolation | Security Groups, Network ACLs | Network Security Groups | VPC Firewall Rules |
| Identity containment | IAM policy changes, disable access keys | Entra ID disable, conditional access | Cloud IAM binding removal |
| Snapshot/evidence | EBS snapshots, AMI | Managed disk snapshots, VM capture | Persistent disk snapshots |
| Termination protection | EC2 termination protection | Resource deletion locks | Instance deletion protection |

## Encrypted Communications

Pervasive encryption reduces visibility of attacker traffic.

Encryption improves general security but may allow C2/exfiltration to evade traditional network inspection.

### TLS Interception

TLS interception proxies can:

1. decrypt;
2. inspect;
3. re-encrypt;

managed endpoint traffic.

Where deployed, egress policy can require TLS traffic to pass through inspection point.

Unexpected direct TLS connections bypassing proxy can be suspicious.

However implementation must consider:

- certificate pinning;
- application compatibility;
- privacy;
- legal authorization.

> Inspection policy should clearly define what traffic is inspected and be legally reviewed.

## Remote Worker Environments

Distributed work moves containment boundary into:

- home networks;
- personal devices;
- multiple geographies;
- SaaS accessed directly over Internet.

### Таблица 23. Remote Worker Containment Challenges

| Challenge | Impact | Recommended approach |
|---|---|---|
| Network visibility | No control over home network | Endpoint-focused EDR isolation |
| Personal-device contamination | Actions may affect personal data | MDM/MAM selective management |
| Home-network compromise | Pivot to family devices / liability | Legal review + employee notification policy |
| VPN isolation | Broad disable disrupts clean workers | Per-user/per-device VPN policy |
| Cloud-service dependencies | SaaS bypasses corporate network | Identity/conditional-access controls |
| Physical device recovery | Devices geographically distributed | Replacement shipping + secure return |

Each row should map to documented named-team procedure.

Details like:

- who ships replacement laptop;
- how MDM wipes corporate data;
- which VPN template applies;

must be worked out in Prepare, not during active incident.

### Network Visibility and Endpoint Controls

Home-network infrastructure is outside organization control.

Therefore containment shifts toward:

- EDR quarantine;
- retained IR management channel;
- endpoint policy;
- identity controls.

### Personal Device Contamination

BYOD requires separation of corporate and personal data.

Use:

- MDM;
- MAM;
- selective wipe;
- app-level isolation;
- conditional access.

Policies should define organization authority over personal devices before incident.

### Home Network Compromise

Attacker may pivot from corporate device to family/personal systems, but source emphasizes that this often reflects weak remote-device configuration.

A properly managed work device with:

- always-on VPN;
- strict firewall;
- no route to residential LAN;

should not freely scan household devices.

Where controls are weak, compromise may reach:

- personal PCs;
- NAS;
- smart-home devices;
- family systems.

This can create:

- liability;
- notification obligations.

Prepare should define:

- employee notifications;
- assistance to personal devices;
- household coordination;
- legal boundaries.

### Access and Recovery

VPN containment can be granular rather than disabling all remote access.

Example:

- restrict compromised user VPN session to email + help desk;
- block file shares/internal apps;
- preserve communication with responder.

For remote SaaS usage, rely on:

- conditional access;
- device compliance;
- forced re-authentication;
- per-user restrictions.

Document each critical SaaS application's containment capabilities.

### Physical Device Recovery

Remote compromised devices may need:

- secure return shipping;
- replacement laptop;
- on-site visit for high-severity cases;
- remote wipe if forensic value is lower than business continuity need.

Source example: ship preconfigured replacement overnight; instruct employee to power down compromised laptop and return it for analysis.

## Beyond Traditional Host Compromise

Modern incidents may not fit "attacker on a host."

Containment can instead focus on:

- service disruption;
- data-flow control;
- third-party coordination;
- identity.

### Рисунок 85. Traditional and Modern Containment Challenges

THIRD_PARTY_REVIEW_REQUIRED.

## Business Email Compromise

BEC uses legitimate email infrastructure for:

- fraud;
- wire-transfer requests;
- sensitive-data theft;
- redirection.

Initial access may come from:

- phishing;
- password reuse;
- session hijacking.

Containment includes:

- email flow rules;
- quarantine messages;
- conditional access;
- provider coordination;
- session/token revocation.

Challenge: distinguish legitimate communication from attacker-controlled messages without breaking business process.

Even if attacker actions occur in SaaS, endpoint investigation remains necessary.

Possible original compromise source:

- keylogger;
- infostealer;
- session-cookie theft.

Therefore BEC workflow should include:

- EDR review;
- endpoint evidence collection.

## Supply Chain Incidents

Supply chain incidents include:

1. upstream vendor software poisoned and deployed internally;
2. organization's own build pipeline compromised and malicious artifacts shipped to customers.

Containment can require:

- package-repository takedown;
- revoke code-signing certificates;
- secure build systems;
- customer notification;
- coordinate external maintainers/platforms.

If compromised CI/CD publishes malicious versions, containment must address both:

- internal breach;
- distributed artifacts already in customer environments.

## MODERN BREACH COMPLEXITY: THE MOVEIT SUPPLY CHAIN ATTACK

Source uses 2023 MOVEit incident to show breach chains crossing organizational boundaries.

First National Bank of Omaha (FNBO) reportedly had approximately **57,000 customer records** exposed, including:

- names;
- Social Security numbers;
- bank account numbers.

FNBO itself was not directly compromised.

Chain described:

FNBO → Pension Benefit Information (PBI) Research Services → MOVEit Transfer → Clop exploitation.

FNBO did not operate MOVEit itself.

This was both:

- supply-chain exposure;
- partner-ecosystem exposure.

Traditional containment assumptions break down because there may be:

- no internal compromised host;
- no local segment to quarantine;
- no process to kill;
- no patch under victim organization's control.

FNBO containment focused on external coordination:

- assess exposure with provider;
- customer notifications;
- credit-monitoring arrangements;
- regulatory reporting.

Source notes similar MOVEit exposure across many organizations including Deutsche Bank and ING.

Lesson: modern response planning must model data embedded in vendor ecosystems and SaaS, not only direct system compromise.

## Partner Ecosystem Breaches

Partner ecosystem breach compromises organization's data in third-party systems while local environment may be clean.

Examples:

- SaaS provider breach;
- MSP breach;
- business vendor exposure.

Containment focus shifts to **cutting data flows**:

- revoke API tokens;
- disable synchronization;
- remove integration permissions;
- audit shared data;
- coordinate provider IR.

Limitation: no direct control over compromised external systems.

Therefore containment occurs at own trust boundary.

Example SaaS CRM breach:

1. revoke provider API tokens;
2. stop automated feeds;
3. identify data shared;
4. contact provider security team;
5. align investigation/notification timeline.

These incidents depend heavily on:

- trust relationships;
- contracts;
- regulatory frameworks;
- external coordination.

## CONTAINMENT VALIDATION

Successful containment must be verified continuously.

Goal: confirm attacker activity has actually stopped and no alternative access path remains.

Validation should combine:

- network monitoring;
- process monitoring;
- log analysis;
- contained-host inspection;
- external telemetry.

### Таблица 24. Containment Validation Channels

| Channel | What to monitor | Key indicators |
|---|---|---|
| Network Monitoring | firewall logs, proxy logs, DNS, attacker infrastructure | resumed C2, new patterns, tunneling |
| Process Monitoring | process creation, services, parent-child relationships | respawned malware, new persistence, unusual paths |
| Log Analysis | authentication, application, security logs | failed logons, privilege escalation, unusual file access |

### Network Monitoring

Review:

- firewall logs;
- proxy logs;
- DNS queries;
- network appliances;
- external servers;
- live contained-system state.

Look for:

- resumed connections to attacker C2;
- new suspicious destinations;
- fallback infrastructure;
- protocol tunneling;
- changed communication patterns.

Containment should be treated as failed or incomplete if attacker simply shifts channels.

### Process Monitoring

Confirm malicious processes no longer run.

Monitor:

- process creation;
- service installations;
- executable paths;
- parent-child relationships;
- network-connected processes.

EDR can provide continuous monitoring.

Without EDR, source suggests:

- Sysinternals Process Explorer;
- `ps`;
- `top`/`htop`.

Establish expected process baseline and investigate deviations.

### Рисунок 86. Process Explorer Indicates Unusual Parent-Child Relationship for LSASS Process

THIRD_PARTY_REVIEW_REQUIRED — product screenshot not reproduced.

### Log Analysis

Monitor:

- authentication logs;
- application logs;
- security events;
- contained-host logs;
- external logging sources.

Look for:

- failed attempts after credential revocation;
- privilege escalation;
- suspicious file access;
- continued exfiltration;
- changed attacker techniques.

Compare pre-containment and post-containment behavior.

# CONTAIN ACTIVITY EXAMPLES

## The Multi-Tenant Credential Exposure

Sarah leads IRT for Kubernetes managed service provider.

Incident affects multiple AWS customers.

AWS GuardDuty alerts unusual API activity from unfamiliar IP.

Team traces credentials to internet-exposed read-only Kubernetes dashboard.

Dashboard service account had read access to cluster-wide secrets.

Kubernetes audit logs showed attacker listed secrets across three customer namespaces:

- TechFlow Solutions;
- Meridian Financial;
- Cascade Logistics.

CloudTrail confirmed attacker used only TechFlow credentials to launch two EC2 instances.

But because secrets for all three customers were viewed, Sarah obtained approval for simultaneous precautionary containment across all three AWS accounts.

Another team remediated dashboard exposure.

Sarah's responsibility: stop unauthorized customer-account access.

### Listing 58. Disable Compromised AWS Access Key for TechFlow Solutions

~~~bash
$ aws iam list-access-keys --user-name k8s-service-account --profile techflow-prod
{
    "AccessKeyMetadata": [
        {
            "UserName": "k8s-service-account",
            "AccessKeyId": "AKIATFSHNUL4J3QFDRFE",
            "Status": "Active",
            "CreateDate": "2025-11-09T14:22:31Z"
        }
    ]
}

$ aws iam update-access-key --user-name k8s-service-account   --access-key-id AKIATFSHNUL4J3QFDRFE   --status Inactive --profile techflow-prod

$ aws iam list-access-keys --user-name k8s-service-account --profile techflow-prod
{
    "AccessKeyMetadata": [
        {
            "UserName": "k8s-service-account",
            "AccessKeyId": "AKIATFSHNUL4J3QFDRFE",
            "Status": "Inactive",
            "CreateDate": "2025-11-09T14:22:31Z"
        }
    ]
}
~~~

Sarah repeated credential disable for Meridian and Cascade despite no confirmed CloudTrail abuse there.

This precaution prevented attacker from pivoting into exposed but unused credentials.

## TechFlow EC2 Isolation

Sarah then contained two attacker-created EC2 instances.

Actions:

- resource tags;
- termination protection;
- EBS snapshot;
- quarantine security group.

### Listing 59. Apply Tags and Termination Protection to Compromised TechFlow Instances

~~~bash
$ aws ec2 describe-instances   --filters "Name=tag:Customer,Values=TechFlow"   --query 'Reservations[].Instances[].InstanceId'   --output text --profile techflow-prod

i-a09727b1175f6b58e i-8d7f7414a5081787e

$ aws ec2 create-tags   --resources i-a09727b1175f6b58e i-8d7f7414a5081787e   --tags Key=Status,Value=UnderInvestigation          Key=IR-Case,Value=2025-042          Key=ContainedBy,Value=sarah-ir-team   --profile techflow-prod

$ aws ec2 modify-instance-attribute   --instance-id i-a09727b1175f6b58e   --disable-api-termination   --profile techflow-prod

$ aws ec2 modify-instance-attribute   --instance-id i-8d7f7414a5081787e   --disable-api-termination   --profile techflow-prod

$ aws ec2 create-snapshot   --volume-id vol-049df61146c4d7901   --description "IR-2025-042 TechFlow instance evidence"   --profile techflow-prod
{
    "SnapshotId": "snap-01234567890abcdef",
    "VolumeId": "vol-049df61146c4d7901",
    "State": "pending",
    "StartTime": "2025-11-02T15:42:18.000Z"
}
~~~

### Listing 60. Create Quarantine Security Group and Apply to Compromised Instances

~~~bash
$ aws ec2 create-security-group   --group-name IR-Quarantine-2025-042   --description "Quarantine SG for IR case 2025-042"   --vpc-id vpc-0a1b2c3d   --profile techflow-prod

{
    "GroupId": "sg-0123456789abcdef0"
}

$ aws ec2 authorize-security-group-ingress   --group-id sg-0123456789abcdef0   --protocol tcp --port 22   --cidr 198.51.100.10/32   --profile techflow-prod

$ aws ec2 revoke-security-group-egress   --group-id sg-0123456789abcdef0   --protocol all   --cidr 0.0.0.0/0   --profile techflow-prod

$ aws ec2 modify-instance-attribute   --instance-id i-a09727b1175f6b58e   --groups sg-0123456789abcdef0   --profile techflow-prod

$ aws ec2 modify-instance-attribute   --instance-id i-8d7f7414a5081787e   --groups sg-0123456789abcdef0   --profile techflow-prod
~~~

Ingress allows SSH only from IR jump box `198.51.100.10`.

Outbound is blocked.

## Kubernetes Service Account Containment

Rather than deleting overprivileged service account and destroying evidence, Sarah removed RBAC binding.

### Listing 61. Disable Kubernetes Service Account by Removing RBAC Bindings

~~~bash
$ kubectl get clusterrolebinding dashboard-secrets-reader -o yaml
apiVersion: rbac.authorization.k8s.io/v1
kind: ClusterRoleBinding
metadata:
  name: dashboard-secrets-reader
roleRef:
  apiGroup: rbac.authorization.k8s.io
  kind: ClusterRole
  name: cluster-secrets-reader
subjects:
- kind: ServiceAccount
  name: dashboard-viewer
  namespace: kubernetes-dashboard

$ kubectl delete clusterrolebinding dashboard-secrets-reader
clusterrolebinding.rbac.authorization.k8s.io "dashboard-secrets-reader" deleted

$ kubectl annotate serviceaccount dashboard-viewer -n kubernetes-dashboard   IR-Case=2025-042 Status=Disabled ContainedBy=sarah-ir-team

serviceaccount/dashboard-viewer annotated
~~~

## Validation

Sarah monitored:

- CloudTrail;
- K8s audit logs;
- quarantine SG behavior.

She configured CloudWatch alarms for:

- reactivated access keys;
- newly created keys on compromised service accounts.

Documented IOCs/containment:

**Account IOC**

- Kubernetes `dashboard-viewer`;
- AWS IAM `k8s-service-account` identities across TechFlow, Meridian, Cascade.

**Network IOC**

- source IP `185.220.101.42`.

**Cloud resource IOC**

- unauthorized EC2:
  - `i-a09727b1175f6b58e`;
  - `i-8d7f7414a5081787e`.

**Contained resources**

- 3 AWS IAM keys disabled;
- 2 EC2 instances quarantined;
- termination protection enabled;
- K8s RBAC removed;
- dashboard ingress removed.

**Customer impact**

- TechFlow: confirmed compromise;
- Meridian: precautionary credential rotation;
- Cascade: precautionary credential rotation.

Key lesson: multi-tenant exposure requires coordinated simultaneous containment of all potentially disclosed credentials, not only environments with confirmed abuse.

## The Ransomware Rapid Response

Marcus Chen is senior support-desk analyst at Vanguard Point Advisors, mid-sized financial-services firm.

Robert Dackinson from Accounting reports:

- spreadsheets corrupted;
- unusual extensions;
- `README_RANSOM.txt` on desktop.

Marcus recognizes ransomware indicators and escalates to Priority 1 according to playbook.

First action: immediate EDR isolation.

He opens CrowdStrike Falcon and finds:

`RD-LAPTOP-278`

### Рисунок 87. CrowdStrike Falcon EDR Workstation Search

THIRD_PARTY_REVIEW_REQUIRED.

Marcus initiates network containment.

### Рисунок 88. CrowdStrike Falcon EDR Workstation Containment

THIRD_PARTY_REVIEW_REQUIRED.

### Рисунок 89. CrowdStrike Falcon EDR Workstation Containment Confirmation

THIRD_PARTY_REVIEW_REQUIRED.

EDR isolation blocks all normal network communications while preserving encrypted management channel.

This prevents:

- network-share encryption;
- lateral movement;

while preserving remote forensic access.

After seconds, Marcus verifies containment status.

### Рисунок 90. CrowdStrike Falcon EDR Workstation Containment Validation

THIRD_PARTY_REVIEW_REQUIRED.

He records containment timestamp.

Next identity actions:

- disable Robert account in Okta;
- revoke active sessions;
- revoke refresh tokens.

### Таблица 25. Containment Actions Summary

| Time | Action |
|---|---|
| 11:47 AM | Report received: corruption/ransom note |
| 11:49 AM | P1 escalation + ransomware playbook |
| 11:51 AM | RD-LAPTOP-278 isolated via CrowdStrike |
| 11:52 AM | Network containment verified |
| 11:54 AM | robert.dackinson@vanguardpointadvisors.com disabled in Okta |
| 11:55 AM | Sessions + refresh tokens revoked |
| 11:57 AM | Escalated to IR for forensics/eradication planning |

Later analysis found ransomware encrypted **247 local files** but isolation occurred before access to critical network file shares.

Containment + identity actions completed in under **10 minutes** from initial report.

Case demonstrates value of:

- well-tested playbook;
- EDR isolation;
- identity containment;
- precise timestamping.

## CONTAIN: STEP-BY-STEP

Следующие steps дают condensed reference containment activities.

Guide организован вокруг задач:

- stop attacker activity;
- preserve evidence;
- prevent further harm;
- validate containment;
- prepare downstream response.

Source указывает, что guide доступен в PDF/Markdown на `dynamicincidentresponse.com`.

### Step 1. Assess Containment Urgency and Strategy

#### 1. Evaluate immediate-containment triggers

Urgent triggers include:

- active data destruction/encryption;
- ongoing exfiltration sensitive information;
- threat to critical/safety systems;
- regulatory timeframe requiring rapid action.

#### 2. Select containment approach

**Passive containment**

- monitor attacker;
- gather intelligence;
- limit damage.

**Active containment**

- stop attacker decisively;
- accept likelihood attacker notices response.

**Adaptive containment**

- combine passive/active measures;
- progressively increase restriction according to attacker behavior.

**Deceptive containment**

- honeypots/decoys;
- production-like controlled environments;
- intelligence gathering while protecting real assets.

#### 3. Balance competing priorities

Evaluate:

- evidence preservation vs operational continuity;
- intelligence value vs continued attacker access;
- business impact vs security benefit.

#### 4. Plan coordinated execution

- identify known compromised systems/accounts/services;
- coordinate network, endpoint, identity, application teams;
- prefer simultaneous actions over sequential isolation;
- sequence credential resets:
  1. most privileged;
  2. service accounts;
  3. standard users;
- prepare rollback for firewall/topology changes;
- establish communication channels.

### Step 2. Implement Identity and Access Containment

### 1. Invalidate known-compromised credentials

This step addresses known-compromised set.

Eradicate Step 4 later expands remediation to blast-radius accounts and deeper identity primitives such as KRBTGT/trust passwords.

Actions:

- reset user passwords via primary IdP;
- rotate service-account credentials;
- rotate API keys/programmatic tokens;
- coordinate synced on-prem/cloud identities;
- prioritize privileged/high-risk accounts.

### 2. Terminate active sessions

- revoke sessions/tokens through IdP;
- disconnect VPN;
- terminate RDP;
- terminate SSH;
- invalidate browser session versions where supported;
- request SaaS provider forced logout if necessary.

### 3. Revoke refresh/persistent tokens

- revoke OAuth refresh tokens;
- revoke offline-access tokens;
- implement deny lists for stateless JWTs where applicable;
- monitor token endpoint use indicating cached credentials.

### 4. Implement conditional access

- geographic restrictions;
- managed-device compliance;
- block suspicious IP/risk patterns;
- escalate MFA to phishing-resistant methods.

### 5. Coordinate SSO containment

- disable compromised account at central IdP;
- identify apps using local accounts separately;
- account for sync/cache delays;
- enforce MFA at IdP.

### 6. Disable third-party integrations

- revoke OAuth apps;
- disable automation;
- remove webhooks;
- disable CI/CD deployment keys;
- invalidate API tokens;
- review browser extensions with broad permissions.

### Step 3. Implement Network and Host Containment

### 1. Network isolation

- quarantine VLAN;
- firewall rules;
- DNS sinkholes;
- micro-segmentation;
- route manipulation when necessary.

### 2. Individual host isolation

- EDR quarantine while preserving forensic channel;
- local firewall restrictions;
- remove cloud instances from scaling groups/load balancers;
- process termination with watchdog caution;
- application-control:
  - AppLocker;
  - Gatekeeper;
  - AppArmor.

### 3. Application-level restrictions

- WAF rules;
- database access/query restrictions;
- disable AI-agent tools/MCP connections;
- revoke AI-system service principals/API keys;
- email quarantine rules;
- service disruption when necessary:
  - web service shutdown;
  - disable RDP/SSH;
  - stop compromised business application.

Coordinate disruptive actions with business owners.

### Step 4. Implement Cloud-Specific Containment

### 1. Verify security demarcation

- determine customer-controlled vs provider-controlled actions;
- do not rely solely on IaaS/PaaS/SaaS labels;
- check product-specific responsibility;
- engage provider security team for infrastructure outside customer control.

### 2. Prioritize cloud identity

- disable IAM access keys;
- rotate service principals;
- revoke OAuth/access/refresh tokens;
- document downstream automation impact.

### 3. Apply network isolation

- security groups;
- NACLs;
- isolation VPC;
- remove from load balancers while retaining running state.

### 4. Protect and track cloud resources

- IR tags;
- termination protection;
- deletion locks;
- snapshots.

### 5. Address SaaS limitations

- password reset/random password;
- freeze/disable account;
- revoke sessions;
- contact provider support when admin interface insufficient.

### 6. Contain serverless/ephemeral resources

- disable event triggers;
- replace function code with deny-and-log;
- revoke IAM/service permissions.

### Step 5. Address Remote Work and Modern Environment Challenges

### 1. Remote workers

- prefer EDR endpoint isolation;
- per-user/device VPN restrictions;
- conditional access for direct-to-SaaS;
- coordinate device recovery;
- balance forensics and continuity.

### 2. BYOD/personal devices

- MDM/MAM selective controls;
- device compliance;
- respect privacy/legal boundaries.

### 3. Encrypted communications

- TLS interception where authorized;
- require egress through inspection point;
- investigate bypass traffic;
- account for DoH;
- use host overrides/local DoH/browser policy;
- balance security with privacy/compatibility.

### 4. Non-traditional compromise

**BEC**

- email flow redirection;
- conditional access;
- endpoint review.

**Supply chain / partner ecosystem**

- external coordination;
- revoke API access;
- stop data synchronization;
- contain at trust boundary where no direct system control exists.

### Step 6. Collect and Preserve Evidence

This step preserves volatile evidence.

Eradicate Step 1 later interprets the captured artifacts during short-form investigation.

### 1. Decide timing

Weigh:

- evidence lost by isolation;
- risk of leaving attacker connected.

If organization has robust:

- network flow;
- host telemetry;
- NDR;

it can isolate first, then collect.

Without alternate volatile-network evidence, collect active connections before isolation where justified.

### 2. Volatile collection

- memory dump;
- active connections;
- running processes/services;
- parent-child relationships;
- temporary files/cache.

### 3. Persistent system artifacts

- registry hives;
- event logs;
- audit/auth logs;
- filesystem metadata;
- Prefetch;
- ShimCache;
- AmCache;
- browser history/cache.

### 4. Network/application evidence

- packet capture where practical;
- NetFlow/VPC Flow Logs;
- firewall logs;
- DNS logs;
- web-server logs;
- DB transaction logs;
- app audit logs;
- cloud audit logs before retention expiry.

### Step 7. Validate Containment Effectiveness

### 1. Network validation

- firewall/proxy/DNS review;
- known C2 monitoring;
- new C2/channel patterns;
- external telemetry when direct connection lost;
- combine appliance visibility + contained-host investigation;
- compare pre/post containment.

### 2. Process validation

- EDR/host telemetry;
- process creation;
- unusual parent-child chains;
- uncommon executable paths;
- new services/persistence;
- process-inspection utilities.

### 3. Log validation

- authentication failures;
- privilege escalation;
- suspicious file access;
- continued exfiltration;
- local + external logs.

### 4. Baseline comparison

- expected process activity;
- network difference;
- process difference;
- log difference;
- verify attacker stopped rather than changed technique/infrastructure.

### Step 8. Document Containment Actions and Communicate Status

### 1. Decision documentation

Record:

- passive/active/adaptive strategy rationale;
- timestamps;
- responsible personnel;
- affected systems/accounts/services;
- alternatives considered;
- chain of custody.

### 2. Operational impact

Document:

- business functions affected;
- user count affected;
- revenue/downtime impact;
- workarounds;
- business-unit feedback.

### 3. Stakeholder communication

Provide:

**Executives**

- business impact;
- risk reduction;
- resource needs.

**IT/security**

- technical implementation details.

**Affected users**

- disruption;
- workaround;
- expected timeline.

Coordinate with:

- legal;
- compliance;
- public relations.

### 4. Prepare downstream phases

- organize evidence for eradication/threat-intelligence analysis;
- create system inventory/prioritized recovery sequence;
- hand containment feedback on control gaps/playbook/tooling limitations to Debrief Step 8;
- identify additional scoping needs exposed by containment.

## Сноски и источники

[1] McMillan, Robert and Volz, Dustin, "Stryker Hit With Suspected Iran-Linked Cyberattack," The Wall Street Journal, March 2026, www.wsj.com/articles/stryker-hit-with-suspected-iran-linked-cyberattack-52f6615c

[2] U.S. Department of Health & Human Services, "Breach Notification Rule," www.hhs.gov/hipaa/for-professionals/breach-notification/breach-reporting/index.html

[3] PCI Security Standards Council, "Responding to a Cardholder Data Breach," listings.pcisecuritystandards.org/documents/Responding_to_a_Cardholder_Data_Breach.pdf

[4] General Data Protection Regulation (GDPR), "Article 33 - Notification of a personal data breach to the supervisory authority," gdpr-info.eu/art-33-gdpr/

[5] Microsoft, "Detect and Remediate Illicit Consent Grants," learn.microsoft.com/en-us/defender-office-365/detect-and-remediate-illicit-consent-grants
