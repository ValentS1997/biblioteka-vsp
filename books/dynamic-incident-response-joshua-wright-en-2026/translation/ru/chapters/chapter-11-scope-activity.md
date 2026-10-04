---
book_id: dynamic-incident-response-joshua-wright-en-2026
chapter_number: 11
source_title: "Scope Activity"
source_pdf_page_range: "224-243"
rag_chunk_range:
  first: "dynamic-incident-response-joshua-wright-en-2026:p0224:c01"
  last: "dynamic-incident-response-joshua-wright-en-2026:p0243:c01"
translation_status: "ACCEPTED"
license_notice: "Неофициальный русский перевод / unofficial Russian translation; original work CC BY 4.0. См. ../ATTRIBUTION.md."
third_party_review_policy: "Figures remain fail-closed; Siemens Figure 71 remains third-party credited material."
translation_notes:
  - "Canonical English RAG is source of truth."
  - "Assembled from full-fidelity source-range segments."
  - "Technical commands/listings are preserved."
---

# Глава 11. Определение масштаба

В модели DAIR вводится ещё одна activity, которая отдельно не выделяется в других популярных incident response models: **scope — определение масштаба**.

Этот step соединяет initial verification incident и effective containment, определяя extent compromise по organization.

Без proper scoping incident response teams рискуют устранить только visible symptoms и оставить значительную часть attack undetected и unaddressed.

### Рисунок 69. Scope Activity Waypoint

THIRD_PARTY_REVIEW_REQUIRED — visual asset не воспроизводится автоматически; сохраняются подпись и cross-reference.

## THE PURPOSE OF SCOPING

Scoping меняет understanding team с «у нас есть incident» на «мы знаем некоторую breadth и depth incident».

Activity берёт IOC, identified during detection/verification, и systematically searches их across environment, чтобы понять true extent breach.

Scoping essential для effective incident response.

Organizations, которые scope incidents недостаточно, часто сталкиваются с repeated compromise: malware eradicated с known-infected systems, но other compromised systems остаются untouched.

NovaFlow incident иллюстрирует failure: Jordan identified suspicious process ssupd на development system, но не searched те же IOC elsewhere в environment и пропустил broader compromise.

Scoping отвечает на фундаментальные вопросы, определяющие весь response effort:

- isolated ли incident одной system или attacker established widespread presence?
- какие systems compromised, а какие unaffected?
- какова timeline attack и как долго attacker maintained access?
- к каким data/resources attacker получил access или что exfiltrated?
- есть ли multiple attack vectors или persistence mechanisms across systems?

Scoping — essential step, заметно отсутствующий в traditional models.

Effective scoping даёт comprehensive understanding incident и позволяет targeted containment, eradication и recovery, addressing root cause, а не symptoms.

## INDICATORS OF COMPROMISE IN SCOPING

Effective scoping зависит от identification и использования IOC — artifacts, revealing malicious activity или attacker presence.

IOC бывают разными. Понимание variety помогает responders расширять search coverage.

Source делит IOC для scoping на две категории:

- technical indicators — concrete searchable artifacts;
- behavioral indicators — patterns attacker activity, не обязательно discrete artifacts.

### Technical IOCs

Technical indicators дают concrete artifacts, которые можно systematically hunt across environment.

**File-based Indicators**

Включают:

- malware hashes;
- suspicious filenames;
- specific file paths.

Если malicious executable найден на одной system, нужно search across systems:

- same hash;
- similar filenames;
- files in unusual locations.

**Network Indicators**

Network indicators broad, но особенно valuable, потому что позволяют быстро оценивать большое число systems.

Включают:

- IP addresses;
- domain names;
- URLs;
- network signatures;
- anomalies, часто characterized NDR platforms;
- unusual network activity patterns.

Если investigation выявил anomalous activity к attacker C2 server, scoping должен identify all systems, communicated with that infrastructure.

Это может раскрыть compromised systems без obvious symptoms.

**Process and Service Indicators**

Включают:

- suspicious process names;
- service names;
- scheduled task names;
- command-line arguments;
- другие process-launch configuration details.

Attackers часто используют consistent naming patterns across compromised systems, что делает их useful для scoping.

Randomly named processes/services также valuable, потому что отклоняются от normal system behavior.

**Registry and Configuration Indicators**

Включают:

- specific registry keys/values;
- configuration changes;
- PowerShell scripts stored in registry;
- WMI event subscriptions;
- modified system settings.

На non-Windows systems аналогичные indicators могут находиться в configuration files, включая ASCII/encoded data и macOS property list files.

**Account-based Indicators**

Включают:

- unauthorized user accounts;
- suspicious usage patterns;
- privilege escalations.

Attacker-created account на одной system требует immediate investigation похожих accounts across organization.

### Behavioral IOCs

Behavioral patterns могут раскрывать attacker activity, которую static IOC не capture.

Они часто требуют более sophisticated analysis, но способны выявлять widespread compromise.

**Temporal Patterns**

Patterns в logs, SIEM trend analysis или aggregate network investigations могут указывать на coordinated activity across systems.

Examples:

- simultaneous logons;
- synchronized file modifications;
- regular beacon intervals.

Отдельные events могут выглядеть benign, но cross-environment timing reveals broader compromise.

Attackers могут работать по consistent schedules, создавая predictable patterns.

**Data Movement Patterns**

Unusual data flows between systems или external destinations могут указывать на data staging/exfiltration.

Large transfers, особенно off-hours, требуют investigation.

Systems, которые обычно не communicate, но внезапно transfer large volumes, также suspicious.

**Lateral Movement Indicators**

Включают authentication, remote access и service-usage patterns, показывающие attacker movement between systems.

Examples:

- pass-the-hash;
- Remote Desktop sessions;
- WMI remote execution.

Эти techniques оставляют distinctive patterns, differing from normal administration.

Multiple authentication attempts across many systems in short timeframe могут reveal automated lateral-movement tooling.

## SCOPING METHODOLOGIES

Analysts могут применять systematic approaches для comprehensive coverage при resource constraints.

Source рассматривает две complementary methodologies:

- enterprise-wide hunting;
- progressive scoping.

### Enterprise-Wide Hunting

После identification IOC analysts должны search matching evidence across organization.

Начинать полезно с centralized log analysis:

- SIEM;
- log aggregation systems;
- другие centralized data resources.

Это обычно даёт быстрые initial results, если organization уже имеет comprehensive log collection.

EDR platforms особенно полезны для IOC searches across managed endpoints.

Modern EDR позволяет query:

- files;
- processes;
- network connections;
- registry modifications;

across thousands systems.

Если EDR отсутствует, можно использовать:

- inventory-management tools;
- active scanning;
- network scans для services/open ports;
- authenticated scans для file presence;
- specialized compromise-assessment tools;
- custom PowerShell или shell scripts.

Для comprehensive scoping желательно использовать threat-hunting platforms, объединяющие endpoint, network и logging data.

Overlapping data-source coverage уменьшает chance пропустить compromised system.

### Progressive Scoping

Из-за resource limitations scoping часто выполняется phases, а не одновременно across entire environment.

**Critical Asset Prioritization**

Initial scoping focuses high-value systems:

- domain controllers;
- file servers;
- databases;
- systems with sensitive data.

Они требуют immediate attention независимо от initial IOC location.

Source отмечает, что этот approach иногда называют pivoting.

**Lateral Expansion**

Scoping расширяется на systems directly connected known-compromised hosts:

- same network segment;
- recent authentication from compromised accounts;
- shared administrative credentials.

Approach следует likely attacker movement paths.

**Environmental Sweep**

Позднее search расширяется на all systems environment, чтобы не оставить undiscovered compromised hosts.

В large organizations sweep может занять days или weeks.

## TIMELINE RECONSTRUCTION

Important output scoping — attack timeline:

- когда compromised разные systems;
- как attack progressed;
- как attacker moved through environment.

Timeline даёт critical context для containment/eradication decisions.

> Timeline reconstruction — iterative activity. Каждый pass Response Actions Loop может раскрыть artifacts, extending timeline earlier или revealing additional attacker activity.

Analysts должны стремиться определить:

- initial compromise;
- patient zero system — first compromised system;
- initial compromise vector.

Early iterations могут завершаться без confirmation этих facts.

Analysis требует review:

- logs;
- file timestamps;
- process-creation times;
- oldest incident-related artifacts.

Examples:

- first malicious file execution;
- first network connection attacker infrastructure;
- earliest authentication anomaly.

Следующий step — map lateral movement:

- authentication logs;
- remote-access records;
- file movement patterns.

Особое внимание:

- privilege-escalation events;
- authentication high-value systems;
- domain controllers;
- database servers.

Также нужно определить timeline persistence deployment.

Common persistence:

- scheduled tasks;
- registry modifications;
- service installations;
- account creations.

Timestamped artifacts помогают определить oldest/deepest persistence.

Наконец, определить, когда sensitive data accessed/removed:

- file-access logs;
- database-query logs;
- network traffic patterns.

Это critical для breach notifications и understanding full impact.

Многие regulatory frameworks требуют report timeline data access/exfiltration.

Source приводит Figure 70, где multiple first-contact events по systems показывают attacker progression.

Используются обозначения:

- LOLC — attacker domain lolcats[dot]org;
- W1GA — attacker domain www1-google-analytics[dot]com.

Timeline reconstructed from network logs в CSV и визуализирован short Python script.

### Рисунок 70. Sample Network Activity Timeline

THIRD_PARTY_REVIEW_REQUIRED — visual asset не воспроизводится автоматически.

### Listing 41. Network Activity Data Summary CSV

~~~text
"2025-03-19 16:46:11",172.16.42.103→W1GA
"2025-03-19 14:46:22",172.16.42.103→LOLC
"2025-03-19 16:48:39",172.16.42.105→W1GA
"2025-03-19 15:16:13",172.16.42.105→LOLC
"2025-03-19 16:50:23",172.16.42.107→W1GA
"2025-03-19 16:55:19",172.16.42.108→W1GA
"2025-03-19 16:57:04",172.16.42.109→W1GA
"2025-03-19 16:10:48",172.16.42.2→W1GA
"2025-03-19 16:38:15",172.16.42.3→W1GA
~~~

Timeline reconstruction часто показывает, что incident ongoing weeks/months before detection.

Это подчёркивает необходимость comprehensive scoping, а не focus только recent symptoms.

Full timeline помогает identify systems, compromised early but not yet discovered by IOC search.

## SCOPING CHALLENGES

Scoping across entire organization создаёт significant challenges.

Source выделяет три obstacles:

- visibility gaps;
- anti-forensic techniques;
- scale and complexity.

### Visibility Gaps

Organizations редко имеют complete visibility across environment.

Blind spots включают:

- unmanaged systems;
- BYOD endpoints;
- shadow IT;
- legacy systems.

Они могут быть compromised и escape standard scoping tools.

Часто такие systems отсутствуют asset inventory, а analysts не имеют credentials/management tooling.

Limited logging — другая visibility problem.

Особенно это касается:

- legacy systems;
- embedded devices;
- ICS platforms;
- network devices;
- printers;
- IoT.

Такие systems могут генерировать minimal logs или хранить их temporarily.

Alternative evidence sources:

- network flow;
- authentication logs connected systems;
- physical evidence unauthorized access.

Source приводит Siemens S7-1200 PLC.

Он widely deployed в:

- manufacturing;
- water treatment;
- building automation;
- other ICS environments.

Несмотря на Ethernet, TCP/IP stack и web interface diagnostics, S7-1200 не имеет centralized logging уровня modern IT systems.

PLC содержит internal diagnostics, connection tables и error counters через web UI, но:

- не генерирует syslog;
- не forwards logs в SIEM;
- не имеет historical audit trails, нужных responders для timeline reconstruction.

Поэтому network flow часто становится primary evidence, был ли ICS device accessed/manipulated.

### Рисунок 71. Siemens S7-1200 [1]

THIRD_PARTY_REVIEW_REQUIRED — image credited to Siemens; visual asset не воспроизводится.

Network flow тоже имеет limitations.

Enterprise switches часто export sampled flow — ratios 1:1000 или higher.

Это может пропустить:

- short-lived connections;
- low-volume C2 beaconing.

Analysts должны verify configured sampling rate и, where feasible, request unsampled export на high-value traffic paths.

OT constraints могут быть ещё сильнее:

- industrial switches могут не уметь flow export;
- sampled output может miss low-volume ICS protocol traffic.

Purpose-built OT monitoring tools дают passive protocol-aware visibility без extra load control network.

Они могут parse:

- Modbus;
- DNP3;
- S7comm.

И формировать:

- asset inventories;
- communication baselines.

Source приводит:

- Dragos — commercial platform;
- Malcolm from Idaho National Laboratory — open source;
- Zeek + ICS Network Protocol Parsers (ICSNPP) — open-source approach.

Chapter 19 рассматривает OT scoping подробнее.

### Cloud and Hybrid Environments

Cloud/hybrid require different scoping approaches from traditional on-premises.

Serverless functions, containers, cloud-native services могут быть invisible traditional Windows-endpoint tools.

Scoping strategy должна включать:

- cloud-provider APIs;
- container-runtime security tools;
- cloud-native logging.

Ephemeral resources могут исчезнуть вместе с evidence после deallocation, поэтому timely scoping critical.

### Anti-Forensic Techniques

Sophisticated attackers intentionally impede scoping через anti-forensics.

Responders должны recognize techniques, develop counter-strategies и избегать conclusions from manipulated evidence.

## Anti-Forensic Techniques

Sophisticated attackers могут удалять или модифицировать logs, скрывать timestamps, encrypt/obfuscate payloads и использовать legitimate tools, чтобы затруднить scoping.

### Log Deletion and Modification

Log deletion удаляет evidence attacker activity, создаёт gaps timeline reconstruction и мешает identify all compromised systems.

Attackers могут:

- удалить specific log entries;
- clear entire log files.

Counter-strategies:

- искать gaps in log timestamps;
- unusual log file sizes;
- security events indicating log clearing.

### Рисунок 72. Windows Event Log Indicating Log Deletion

THIRD_PARTY_REVIEW_REQUIRED — visual asset не воспроизводится автоматически.

Multiple independent log sources помогают reconstruct activity, даже если часть logs удалена.

Если multiple sources unavailable, иногда можно infer deleted events через correlation network logs или other system events.

На Windows каждому event назначается sequential Event Record ID.

Gaps в sequence могут указывать на deleted records.

### Рисунок 73. Windows Event Viewer Event Record ID Field

THIRD_PARTY_REVIEW_REQUIRED — visual asset не воспроизводится автоматически.

Attackers могут manipulate logs без удаления.

**Log replay и flooding** загрязняют event stream:

- replay legitimate events, чтобы attacker session выглядел normal;
- flood SIEM, causing dropped events;
- spacing detectable events below alert thresholds.

Countermeasures:

- baseline expected log volumes;
- alerting on sudden surges;
- alerting on unusual quiet periods;
- correlation across independent sources, которые трудно manipulate simultaneously.

### Timestomping

Timestomping modifies file timestamps, чтобы скрыть installation time malware или смешать malicious files с legitimate ones.

Attackers могут сделать new malware file выглядящим так, будто он существует since system installation.

Alternative timestamp sources:

- filesystem metadata;
- $MFT entries on Windows;
- backup-system records;
- network-detection timestamps for downloads.

### Encryption and Obfuscation

Encryption/obfuscation скрывают indicators от automated scanning.

Examples:

- encrypted malware payloads;
- obfuscated PowerShell commands;
- packed executables;
- encrypted C2 traffic.

В таких случаях behavioral analysis и memory forensics часто effective than signature matching.

### Living off the Land

Attackers используют legitimate system tools:

- PowerShell;
- WMI tooling, включая wmic.exe и mofcomp.exe;
- .NET Framework tools, включая csc.exe, installutil.exe и другие.

Это позволяет blend into normal administrative operations.

Для detection malicious use нужно analyze:

- command-line arguments;
- execution context;
- temporal patterns.

Baseline normal admin activity помогает identify anomalies.

Behavioral detections + machine learning могут surface deviations, которые static rules пропускают.

## Scale and Complexity

Large environments создают practical scoping problems даже для well-resourced teams.

IOC search across thousands systems генерирует large volumes:

- log data;
- file listings;
- process information.

Analysts должны использовать progressive scoping:

1. known-compromised systems/high-value targets;
2. connected/lateral systems;
3. broader environment.

Automation помогает processing, но findings требуют analyst validation.

False positives consume resources.

Examples:

- malware filename совпадает с legitimate software;
- network IOC search finds legitimate VPN connection.

Known false-positive sources следует document для future scoping.

### Dynamic / Cloud Environments

Auto-scaling и containerized environments создают additional challenges:

- systems continuously created/destroyed;
- compromised instances могут disappear before investigation;
- tainted images могут create new compromised systems.

Scoping должен включать:

- system images;
- container registries;
- infrastructure-as-code templates;
- running workloads.

Logging должен persist evidence after resource destruction.

### Таблица 14. Cloud Audit Log Quick Reference

| Objective | AWS | Azure | GCP |
|---|---|---|---|
| Query audit logs | aws cloudtrail lookup-events | az monitor activity-log list | gcloud logging read |
| Filter by resource | aws cloudtrail lookup-events --lookup-attributes AttributeKey=ResourceName,AttributeValue=<name> | az monitor activity-log list --resource-id <resource-id> | gcloud logging read 'resource.type="<type>"' |
| Filter by user/principal | aws cloudtrail lookup-events --lookup-attributes AttributeKey=Username,AttributeValue=<user> | az monitor activity-log list --caller <object-id> | gcloud logging read 'protoPayload.authenticationInfo.principalEmail="<email>"' |
| Filter by time range | aws cloudtrail lookup-events --start-time <time> --end-time <time> | az monitor activity-log list --start-time <time> --end-time <time> | gcloud logging read 'timestamp>="<time>"' |

Эти commands дают starting point для cross-platform audit-log analysis during scoping.

## INTEGRATION WITH RESPONSE ACTIVITIES

Scoping тесно связан с containment, eradication и recovery.

Information from scoping feeds directly into downstream decisions.

New findings during containment/eradication/recovery могут trigger additional scoping.

Possible execution patterns:

- scope → contain → eradicate → recover;
- scope parallel with other activities;
- scope → recovery directly, если no new compromised systems found, but additional context changes root-cause analysis.

Scoping transforms incident response from reactive firefighting to strategic remediation.

Systematic identification affected systems помогает:

- eliminate threats comprehensively;
- address root cause;
- avoid incomplete remediation;
- reduce reinfection.

## SCOPE ACTIVITY EXAMPLES

### The LinkedIn Attachment

Renee — incident response analyst mid-sized SaaS company.

Product manager reported suspicious activity after opening document, received through LinkedIn direct message from person claiming to be industry analyst.

Document promised leaked competitive analysis of closest rival.

Renee должна определить, malicious ли document.

Initial analysis выполнялась на dedicated workstation isolated from corporate network.

Она начала с file size, hash и file type.

### Listing 42. Unsolicited Document File Command Output

~~~text
$ ls -l malware
-rw-r—r--@ 1 renee staff   1.6M Oct 21 16:29 malware
$ sha256sum malware
9484272e48f908e816a68f295a105d885b9d0ba52d8255d95c9bf237f71eae6b  malware
$ file malware
malware: PDF document, version 1.4
~~~

File looked like standard PDF, но Renee ещё не открывала его в viewer.

Она extracted PDF structural summary с pdfid.py.

### Listing 43. Unsolicited Document Pdfinfo Command Output

~~~text
$ pdfid.py malware
PDFiD 0.2.10 malware
 PDF Header: %PDF-1.4
 obj                   27
 endobj                27
 stream                 5
 endstream              5
 xref                   4
 trailer                4
 startxref              4
 /Page                  1
 /Encrypt               0
 /ObjStm                0
 /JS                    0
 /JavaScript            0
 /AA                    0
 /OpenAction            0
 /AcroForm              0
 /JBIG2Decode           0
 /RichMedia             0
 /Launch                0
 /EmbeddedFile          0
 /XFA                   0
 /URI                   6
 /Colors > 2^24         0
~~~

pdfid.py показывает:

- one-page PDF;
- six embedded URIs;
- no JavaScript/OpenAction/Launch markers.

Renee extracted URIs через pdf-parser.py.

### Listing 44. Unsolicited Document Pdf-parser Command Output

~~~text
$ pdf-parser.py -s /URI malware

obj 9 0
 Type: /Annot
 Referencing:

  <<
    /Type /Annot
    /Subtype /Link
    /Rect [51.7500000  191.750000  542.250000  827.750000 ]
    /Border [0 0 0]
    /A
      <<
        /Type /Action
        /S /URI
        /URI (hxxp://host███████private.duckdns[.]org/eubp/example.zip) ①
      >>
  >>

obj 19 0
 Type: /Action
 Referencing:

  <<
    /URI (hxxps://stc████████lik[.]com/Update/UpdatePDF.exe) ②
    /S /URI
    /Type /Action
  >>

obj 25 0
 Type: /Action
 Referencing:

  <<
    /URI (hxxps://stc████████lik[.]com/Update/UpdatePDF.zip) ③
    /S /URI
    /Type /Action
  >>
~~~

① Suspicious URL at DuckDNS serving example.zip.  
② Suspicious URL hosting UpdatePDF.exe.  
③ Suspicious URL hosting UpdatePDF.zip.

Renee обнаружила three suspicious URLs across six references.

Indicators для дальнейшего scoping:

- PDF SHA-256 hash;
- three embedded URLs;
- filenames UpdatePDF.exe и UpdatePDF.zip.

Она documented indicators и продолжила analysis PDF while searching for impacted systems across organization.

## The Cloud Storage Exfiltration

Priya — cloud security analyst financial-services company, использующей Azure для production applications и data storage.

Microsoft Defender for Cloud создал automated alert: в storage account `stcorpdata01` появился новый Blob Storage container `backup-data-archive-2025`, созданный three days earlier.

Priya проверила Teams и не нашла associated change order.

Container name соответствовал internal naming conventions, но creation timestamp был **11:47 PM Saturday**, outside normal business hours.

Она начала investigation как possible IOC.

### Listing 45. Cloud Exfiltration Container Contents

~~~text
$ az storage blob list --container-name backup-data-archive-2025 --account-name stcorpdata01   --query "[].{Name:name, Size:properties.contentLength, Modified:properties.lastModified}"   --output table

Name                                                Size       Modified
--------------------------------------------------  ---------  --------------------------------
HR/Payroll_2025_Q1.xlsx                             49492787   2025-10-19T23:52:14+00:00
Finance/Budget_Projections_2026.xlsx                134637158  2025-10-19T23:52:18+00:00
CustomerData/client_list_full.csv                   935418906  2025-10-19T23:52:23+00:00
Engineering/Product_Roadmap_Confidential.pptx       67947725   2025-10-19T23:52:31+00:00
Legal/Contracts_Archive_2024.zip                    225770509  2025-10-19T23:52:38+00:00
HR/Employee_Records_Complete.xlsx                   103494067  2025-10-19T23:52:45+00:00
CustomerData/transaction_history_2024.csv           462638387  2025-10-19T23:52:52+00:00
Finance/Audit_Reports_2024.pdf                      164481254  2025-10-19T23:53:01+00:00
Engineering/Source_Code_Archive.zip                 77070336   2025-10-19T23:53:08+00:00
CustomerData/customer_pii_database.csv              340331930  2025-10-19T23:53:15+00:00
[...]
~~~

Container содержал **47 blobs**, total approximately **8.2 GiB**.

Filenames указывали на highly sensitive data:

- payroll;
- customer data;
- intellectual property;
- legal contracts.

Directory structure:

- HR/;
- Finance/;
- CustomerData/;
- Engineering/;
- Legal/.

Она точно соответствовала internal file-server layout.

Все blobs имели upload timestamps внутри approximately twenty-minute window того же Saturday night.

Priya выяснила, кто создал container, через Azure Activity Log.

### Listing 46. Cloud Exfiltration Container Creation Event

~~~json
$ az monitor activity-log list --offset 7d --query "[?contains(resourceId, 'backup-data-archive-2025')] | [0]"
{
  "authorization": {
    "action": "Microsoft.Storage/storageAccounts/blobServices/containers/write",
    "scope": "/subscriptions/e7b3c1d9-a842-4f56-b6d1-8a3e5f902c4d/resourceGroups/rg-production-eastus2/providers/Microsoft.Storage/storageAccounts/stcorpdata01/blobServices/default/containers/backup-data-archive-2025"
  },
  "caller": "c7e2a091-4b38-4d65-9f12-b8a3e6d50c71", ①
  "claims": {
    "appid": "e4f2d1b8-6a93-4c57-8e1f-9d0b2a3c5e7f",
    "http://schemas.microsoft.com/identity/claims/objectidentifier": "c7e2a091-4b38-4d65-9f12-b8a3e6d50c71"
  },
  "eventTimestamp": "2025-10-19T23:47:32.381Z",
  "httpRequest": {
    "clientIpAddress": "203.0.113.88", ②
    "method": "PUT"
  },
  "operationName": {
    "localizedValue": "Create or Update Container",
    "value": "Microsoft.Storage/storageAccounts/blobServices/containers/write"
  },
  "resourceGroupName": "rg-production-eastus2",
  "status": {
    "localizedValue": "Succeeded",
    "value": "Succeeded"
  }
}
~~~

① Entra ID service-principal object ID, создавший container.  
② External IP address source request.

Priya cross-referenced caller object ID в Entra ID.

Это был legitimate `svc-automation` service principal, used automated processes across organization.

Но source IP `203.0.113.88` не был internal system или known Azure resource.

Это стало possible indicator compromise service-principal credentials.

Далее Priya расширила activity search по principal.

### Listing 47. Cloud Exfiltration Compromised Service Principal Activity

~~~text
$ az monitor activity-log list --caller c7e2a091-4b38-4d65-9f12-b8a3e6d50c71 --offset 7d   --query "[].{Time:eventTimestamp, Operation:operationName.localizedValue, Provider:resourceProviderName.localizedValue}"   --output table

Time                       Operation                         Provider
-------------------------  --------------------------------  -------------------------
2025-10-15T14:23:18+00:00  Read Role Assignment              Microsoft.Authorization
2025-10-15T14:28:42+00:00  Read Virtual Machine              Microsoft.Compute
2025-10-16T03:15:27+00:00  List Storage Account Keys         Microsoft.Storage
2025-10-16T08:44:19+00:00  Create Role Assignment            Microsoft.Authorization
2025-10-17T11:32:54+00:00  Create or Update Security Rule    Microsoft.Network
2025-10-17T16:19:08+00:00  Create or Update Virtual Machine  Microsoft.Compute ①
2025-10-19T23:47:32+00:00  Create or Update Container        Microsoft.Storage ②
~~~

① Attacker launched a virtual machine using compromised service principal.  
② Creation unauthorized Blob Storage container.

Activity showed extensive unauthorized actions over **five days**:

- enumerate role assignments;
- reconnaissance existing virtual machines;
- obtain storage-account keys;
- grant additional permissions through new role assignment;
- modify network security-group rules;
- launch virtual machine;
- create unauthorized container.

Storage diagnostic logs revealed **47 blob uploads** on October 19 corresponding files in container.

Additional queries showed:

- container creation originated from external IP `203.0.113.88`;
- uploads originated from VM at internal IP `10.0.50.15`;
- this matched VM created October 17.

This indicated attacker had established infrastructure inside Azure environment to facilitate exfiltration from internal resources.

Priya documented IOC categories:

**Account-based indicators**

- compromised Entra ID service principal `svc-automation`;
- object ID `c7e2a091-4b38-4d65-9f12-b8a3e6d50c71`.

**Network indicators**

- external IP `203.0.113.88`.

**Cloud resource indicators**

- unauthorized container `backup-data-archive-2025`;
- storage account `stcorpdata01`;
- attacker-created VM at `10.0.50.15`.

**File-based indicators**

- 47 specific filenames;
- payroll/customer PII/intellectual property.

**Behavioral indicators**

- bulk blob upload in twenty-minute window;
- Azure management API activity external IP;
- service-principal usage outside normal automation patterns.

После IOC identification Priya started enterprise-wide scoping.

### Таблица 15. Cloud Exfiltration Scoping Commands

| Scoping objective | Command |
|---|---|
| Extend activity search to 90 days | az monitor activity-log list --caller c7e2a091-4b38-4d65-9f12-b8a3e6d50c71 --offset 90d |
| Enumerate all role assignments for compromised principal | az role assignment list --assignee c7e2a091-4b38-4d65-9f12-b8a3e6d50c71 --all |
| Identify recently created/modified storage containers | az storage container list --account-name stcorpdata01 --query "[?properties.lastModified >= '2025-10-15']" --output table |

Extended search showed service principal accessed from external IP as early as **October 8**, more than a week before first management actions initially identified.

Role-assignment query showed attacker granted compromised principal **Contributor** access to second resource group:

- `rg-analytics-eastus2`.

This expanded potential scope beyond production environment.

Priya compiled scoping summary for incident commander:

- confirmed attacker timeline;
- compromised resources across both resource groups;
- volume/sensitivity exfiltrated data;
- recommended next containment steps.

Summary gave leadership context for:

- notification obligations;
- containment priorities;
- resource allocation.

## SCOPE: STEP-BY-STEP

Следующие steps дают condensed reference scoping activities.

Source указывает, что guide доступен в PDF/Markdown на `dynamicincidentresponse.com`.

### Step 1. Identify Indicators of Compromise from Detection and Verification

Categorize IOC handed off from verify/triage в canonical inventory.

Representative categories:

- file-based: hashes, filenames, paths;
- network: IP, domains, URLs, signatures;
- process/service: process names, command-line arguments;
- registry/configuration: keys, configuration changes;
- account-based: unauthorized accounts, suspicious usage;
- behavioral: temporal patterns, data movement, lateral movement.

### Step 2. Conduct Enterprise-Wide Hunting for Identified IOCs

Это IOC-driven sweep during verified incident, distinct from standing hypothesis-driven hunting program owned by detect.

Representative activities:

- search SIEM/log aggregation;
- leverage EDR across managed endpoints;
- если EDR unavailable — inventory tools, active scans, network scans, custom scripts;
- use threat-hunting platforms, combining endpoint/network/logging data.

### Step 3. Apply Progressive Scoping Methodology

Representative activities:

- prioritize critical assets:
  - domain controllers;
  - file servers;
  - databases;
  - sensitive-data systems;
- expand laterally to systems connected known-compromised hosts;
- conduct environmental sweep across all systems.

### Step 4. Reconstruct the Attack Timeline

Scope owns canonical attack-progression timeline.

Later activities annotate it:

- eradicate adds eradication-sequencing markers;
- debrief consolidates final narrative.

Representative activities:

- identify initial compromise and patient zero;
- map lateral movement via authentication/file-access patterns;
- identify persistence deployment timeline;
- determine when sensitive data accessed/exfiltrated.

### Step 5. Document Scoping Findings

Representative activities:

- list compromised systems;
- record new IOC;
- create attack-progression timeline visualization;
- note visibility gaps and systems requiring more investigation.

### Step 6. Address Scoping Challenges

Representative activities:

- identify/document visibility gaps:
  - unmanaged systems;
  - limited logging;
  - IoT;
  - ICS;
- use alternative evidence for low-logging systems:
  - network flow;
  - authentication logs connected systems;
- for ICS/industrial devices without centralized logging, rely on network flow as primary evidence source;
- watch anti-forensic techniques:
  - log deletion;
  - timestomping;
  - encryption/obfuscation;
  - living off the land;
- use counter-strategies:
  - log-manipulation detection;
  - alternative timestamp sources;
  - behavioral analysis;
  - command-line review;
- apply cloud-specific tooling:
  - provider audit logs;
  - container-runtime security;
- scope cloud quickly because ephemeral resources may disappear with evidence;
- manage scale through prioritization/automation;
- document false positives.

### Step 7. Prepare Scoping Results for Containment, Eradication, and Recovery

Hand off downstream:

- scoped system list;
- canonical IOC inventory from Step 1;
- attack-progression timeline from Step 4.

Цель — чтобы containment/eradication/recovery строились на settled artifacts и не re-derive scoping results.

## Сноски и источники

[1] Siemens S7-1200 G2 PLC, image used courtesy of Siemens.
