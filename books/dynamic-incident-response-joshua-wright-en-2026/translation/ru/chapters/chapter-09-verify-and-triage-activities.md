---
book_id: dynamic-incident-response-joshua-wright-en-2026
chapter_number: 9
source_title: "Verify and Triage Activities"
source_pdf_page_range: "190-212"
rag_chunk_range:
  first: "dynamic-incident-response-joshua-wright-en-2026:p0190:c01"
  last: "dynamic-incident-response-joshua-wright-en-2026:p0212:c01"
translation_status: "DRAFT_FOR_QA"
license_notice: "Неофициальный русский перевод / unofficial Russian translation; original work CC BY 4.0. См. ../ATTRIBUTION.md."
third_party_review_policy: "Figures and direct third-party verbatim material remain fail-closed."
translation_notes:
  - "Canonical English RAG is source of truth."
  - "Assembled from full-fidelity source-range segments."
  - "Technical commands/log listings are preserved unless an explicit safety/license boundary applies."
---

# Глава 9. Проверка и триаж

В модели DAIR вводится activity, которая отдельно не выделяется в других популярных incident response models: **verify and triage — проверка и триаж**. Этот step часто подразумевается внутри detection phase в PICERL или NIST SP 800-61 (*Computer Security Incident Handling Guide*), однако автор считает важным обозначить его явно.

### Рисунок 57. Опорная точка Verify/Triage Activity

`THIRD_PARTY_REVIEW_REQUIRED` — visual asset не воспроизводится автоматически; сохраняются подпись и cross-reference.

В verify and triage analysts выполняют два важных действия:

- **Verify the incident — проверить incident:** использовать information, собранную в detect activity, чтобы оценить validity incident и назначить initial risk impact classification для подключения broader incident response team.
- **Triage the incident — выполнить triage:** совместно с decision makers определить appropriate response actions на основе risk impact classification и доступной incident information, включая allocation resources для investigation.

На этой activity analysts начинают более активно координироваться с decision makers — людьми, обладающими authority принимать решения по incident response process. Обычно это managers или executives, способные предоставить необходимые resources, но сюда также могут входить data owners, legal counsel, business-unit leaders и другие stakeholders, заинтересованные в outcome incident response process.

## ВАЖНОСТЬ ПРОВЕРКИ

Во время verification information из detect activity используется для определения, является ли incident реальным или false positive. Verification предотвращает расход resources incident response team на несуществующий incident и позволяет команде заниматься другими responsibilities. Она также укрепляет confidence decision makers, показывая, что response соответствует risk, известному на начальном этапе response effort.

Иногда verification очевидна: defaced website, например, является ясным indication compromise. В других случаях IOC менее определённы, и IRT приходится потратить время на verification до перехода к response effort.

На этом этапе visibility incident часто ограничена, поэтому initial assessment строится на data из detect phase. Также необходимо принимать возможность того, что verification не выявит evidence compromise, даже если unexplained behavior выглядит suspicious.

### VERIFICATION AS A GATING FUNCTION

Canonical source приводит вопрос студента о том, почему verify and triage стоит перед response actions loop, а не повторяется внутри цикла вместе со scope, contain, eradicate и recover.

`THIRD_PARTY_REVIEW_REQUIRED` — direct student quotation не воспроизводится verbatim; сохраняется смысл вопроса.

Краткий ответ автора: verification является **gating function**, не позволяющей broader response team тратить resources на incident, которого может не существовать. Verification до подключения broader team, company stakeholders и decision makers помогает убедиться, что response effort соответствует risk, известному на старте.

При прямом переходе от detection к response action есть риск потратить resources на incidents, которые не реальны или не оправдывают рассматриваемый уровень response. Это ведёт к wasted effort, упущенной возможности заниматься другими critical responsibilities и снижению confidence decision makers в incident response process.

Это не исключает того, что последующая повторная verification или resource reallocation может происходить внутри response actions loop. Смысл initial verification — установить gate перед первоначальным подключением broader team.

## VERIFICATION RESPONSE ACTIONS

Во время verification IRT review information, collected в detect activity, чтобы определить validity incident. В зависимости от доступных data возможны три outcomes:

- **Continue the incident response process:** если IRT считает incident реальным, она escalates и initiates incident response process, подключая broader IRT, company stakeholders и decision makers.
- **Stop the incident response process:** если incident не реален, он закрывается, а findings документируются для future reference.
- **Defer verification:** если validity нельзя определить по доступной information, decision откладывается до получения additional information от reporting party или других sources.

Decision **continue / stop / defer** позволяет analyst выполнить initial assessment reported incident до подключения broader response team, stakeholders и decision makers.

### Рисунок 58. Verification Process

`THIRD_PARTY_REVIEW_REQUIRED` — visual asset не воспроизводится автоматически.

## DOCUMENTATION

Документирование incident по мере развития создаёт более accurate record, чем попытка написать documentation после завершения response. Под давлением active response analysts естественным образом откладывают notes, однако specific commands, timestamps и decisions быстро забываются. Поздняя reconstruction часто получается incomplete или misleading.

IRT должна воспринимать documentation как continuous practice, начинающуюся на verification и накапливающуюся на протяжении response actions loop, а не как task, отложенную на конец incident.

> Документирование по ходу incident создаёт более качественный record и разбивает tedious documentation task на меньшие, manageable части.

Используя incident-tracking platform, созданную во время preparation, analyst должен начать capture incident information. Этот information-collection process продолжается весь lifecycle incident.

Во время verification source рекомендует фиксировать:

- **Incident identifier:** unique ID incident, часто generated tracking platform.
- **Incident title:** descriptive title, обычно основанный на report source или incident classification; служит quick intuitive reference.
- **Handler ID:** identifier analyst, responsible за assessment incident.
- **Incident summary:** краткое описание incident, source report, date/time report и relevant information.
- **Incident classification:** initial classification по доступным data; examples: unauthorized access, phishing, malicious code, sensitive data disclosure, account compromise, public-facing exploit и др.
- **Evidence references:** ссылки на evidence, собранные в detect activity.

Documentation, начатая на verification, обычно используется далее для tracking incident, записи response actions и future reference. Она также помогает IRT предоставлять updates decision makers/stakeholders. Позднее она может стать основой final incident report или частью cyber insurance claim.

На этом этапе часто возникает urgency двигаться быстро. Однако incident необходимо документировать accurately и достаточно подробно для subsequent activities. Source формулирует современную практическую мысль: если analyst работает настолько быстро, что не успевает делать notes, вероятно, работа идёт слишком быстро. Documentation также помогает умерить investigation pace и не пропустить details.

### THE NEED FOR PRISTINE DOCUMENTATION

Analysts должны поддерживать integrity incident documentation на протяжении response process. Contamination может снизить validity documentation как evidence в legal proceedings.

Автор ссылается на наставления Ed Skoudis, который рекомендовал использовать отдельный unused notebook для incident response documentation. Рекомендация основана на его опыте expert witness, где opposing attorneys неоднократно ставили под сомнение integrity notes.

Canonical source пересказывает courtroom example: lead investigator представил notebooks как evidence; cross-examination сосредоточился на том, что из notebook отсутствовали несколько sheets, что позволило attorney поставить вопрос о возможном уничтожении evidence.

`THIRD_PARTY_REVIEW_REQUIRED` — direct courtroom dialogue не воспроизводится и не переводится verbatim.

Modern investigations используют digital documentation platforms, но lesson остаётся тем же: opposing counsel будет искать основания сомневаться в integrity notes. Не следует загрязнять incident documentation unrelated information; notes должны относиться к incident at hand. Нужно учитывать, как записи могут выглядеть для outside party, и сохранять их clear, accurate и concise.

## INITIAL RISK ASSESSMENT

Documentation section зафиксировал необходимость вести incident record, но initial risk assessment ещё не добавлен.

Перед presentation incident details decision maker для resource-allocation decisions analyst должен дать initial risk assessment. Существуют разные подходы к classification/impact assessment. Source перечисляет:

- **Vocabulary for Event Recording and Incident Sharing (VERIS):** используется Verizon DBIR и incident-sharing communities для quantification incident impact.
- **Factor Analysis of Information Risk (FAIR):** framework количественного анализа/manage information risk.
- **NIST SP 800-30:** US government risk-assessment framework для identification, assessment и response risks information systems.

Для многих organizations initial risk assessment проще: classification incident по perceived impact. Учитываются financial, operational, reputational loss и potential regulatory impact. Хотя оценка может отличаться даже между analysts одной organization, broad categories помогают communicate incident details decision makers.

Common four-level model:

- **Low:** minor security anomalies с minimal impact.
- **Medium:** potential security concerns, требующие investigation, но не disrupting operations.
- **High:** confirmed incidents, impacting business operations или data integrity.
- **Critical:** major security incidents, требующие executive escalation и immediate containment.

Initial risk assessment в incident documentation помогает decision makers понять potential impact, исходя из assessment analyst.

## VERIFICATION AND CYBER THREAT INTELLIGENCE

Cyber Threat Intelligence (CTI) добавляет context во время verification, помогая отличать genuine threats от false positives и уточнять risk assessment, который затем влияет на triage decisions. Интеграция CTI позволяет быстрее и точнее выбирать continue, stop или defer.

Source выделяет три способа, которыми CTI усиливает verification:

1. enrich Events of Interest для validation suspicious indicators;
2. inform initial risk classification через attribution и threat-actor context;
3. pivot from single indicator к related IOC, расширяя verification scope.

### EOI Validation and Enrichment

Когда analyst сталкивается с suspicious EOI, CTI platforms могут показать, связаны ли indicators с known threats. Reputation databases, threat-intelligence feeds и community-sourced information помогают отличить malicious activity от benign behavior. Это особенно важно на verification, где задача — быстро assess validity без unnecessary resource expenditure.

Analysts могут query CTI по IP addresses, domain names, URLs или file hashes. Database может показать associations с malware distribution, phishing campaigns, C2 infrastructure или другой malicious activity. VirusTotal, AlienVault OTX, Shodan и commercial feeds могут давать разные perspectives на один indicator; cross-reference multiple sources повышает confidence.

Source приводит incident example: IP address `147.45.44.131` наблюдался как source PowerShell script downloads в web-proxy logs. Само по себе это suspicious, но не definitive. Cross-reference через VirusTotal и AlienVault OTX добавил context malicious patterns.

### Рисунок 59. CTI Insight for IP Address IOC from VirusTotal

`THIRD_PARTY_REVIEW_REQUIRED` — third-party platform visual не воспроизводится.

### Рисунок 60. CTI Insight for IP Address IOC from AlienVault OTX

`THIRD_PARTY_REVIEW_REQUIRED` — third-party platform visual не воспроизводится.

CTI enrichment также помогает отсеять false positives до расхода investigation resources. Legitimate services иногда выглядят suspicious: CDN с unusual traffic, cloud infrastructure с dynamic IP allocation или security tools, выполняющие authorized scanning. Threat-intelligence platforms часто содержат known-good infrastructure.

Например, regularly timed outbound connections к unfamiliar IP могут выглядеть как C2, но enrichment может показать, что IP принадлежит Microsoft Windows Notification Service (WNS), быстро закрывая verification loop.

### Рисунок 61. VirusTotal CTI for IPv6 Address Reveals Microsoft ASN

`THIRD_PARTY_REVIEW_REQUIRED` — third-party platform visual не воспроизводится.

### Рисунок 62. VirusTotal CTI for IPv6 Address Reveals Server Identity

`THIRD_PARTY_REVIEW_REQUIRED` — third-party platform visual не воспроизводится.

Source рекомендует вести **local knowledge base false-positive sources**, специфичных для environment organization. Когда CTI подтверждает benign indicator, вызвавший alert, finding нужно document для future reference. Со временем organizational memory сокращает verification time recurring false positives.

## Informing Initial Risk Classification

Один и тот же IOC может означать совершенно разные risk levels в зависимости от того, что CTI сообщает о его origin, associated threat actors и typical attack patterns. Используя CTI context, analysts могут точнее calibrate initial risk classification во время verification assessment.

Например, phishing email с credential-harvesting link может получить **medium** classification, если threat intelligence связывает его с mass-distributed commodity campaign, targeting broad populations. Тот же indicator может быть escalated до **high** или **critical**, если CTI связывает его с threat actor, известным targeting similar organizations и последующим ransomware deployment.

> Technical indicator остаётся тем же, но threat context принципиально меняет appropriate response.

Не все CTI signals имеют одинаковый вес при communication risk decision makers. Source размещает indicators на spectrum от circumstantial до behavioral:

- **Circumstantial indicators:** infrastructure observations, характерные и legitimate, и malicious activity. Examples: domain registration через low-cost registrars (Namecheap, Porkbun), free-tier hosting/CDN (Cloudflare free tier, GitHub Pages), short-validity certificates automated CAs (Let’s Encrypt). Такие indicators легко reproduce любому actor и часто встречаются benignly; они повышают suspicion, но редко подтверждают intent.
- **Behavioral indicators (TTPs):** patterns, отражающие documented operational habits threat actor. Examples: specific domain naming conventions вроде `secure-[vendor]-portal.com` для impersonation, tooling artifacts, action sequencing из CISA advisories/vendor reporting. Такие indicators сложнее случайно воспроизвести unrelated actor и они дают stronger attribution confidence.

При briefing executives/decision makers эти classes нужно различать явно. Finding, supported несколькими TTP-level matches, требует другой language, чем finding, основанный преимущественно на circumstantial infrastructure.

### SAME DOMAIN, TWO RISK ASSESSMENTS

Scenario: во время routine log review analyst IT services provider замечает connections в employee web-proxy logs к unfamiliar domain `secure-sendwise-portal.com`. WHOIS показывает регистрацию domain всего **36 hours** назад, что вызывает suspicion.

### Listing 34. Proxy Log Entries Showing Connections to Newly Registered Domain

```
1734955847.284    127 172.16.42.108 TCP_MISS/200 0 CONNECT 198.51.100.47:443 -
ORIGINAL_DST/198.51.100.47 -
1734955847.412     94 172.16.42.108 TCP_MISS/200 4891 GET https://secure-sendwise-
portal.com/api/v2/status - ORIGINAL_DST/198.51.100.47 application/json ①
1734955848.156    203 172.16.42.108 TCP_MISS/200 12847 GET https://secure-sendwise-
portal.com/assets/notify.js - ORIGINAL_DST/198.51.100.47 application/javascript
1734955912.891    142 172.16.42.108 TCP_MISS/200 2156 POST https://secure-sendwise-
portal.com/api/v2/register - ORIGINAL_DST/198.51.100.47 application/json ②
1734956147.445     87 172.16.42.108 TCP_MISS/200 891 GET https://secure-sendwise-
portal.com/api/v2/status - ORIGINAL_DST/198.51.100.47 application/json
```

① Initial API call to newly registered domain.  
② POST request, suggesting data submission to external site.

Traffic показывает workstation, connecting domain, loading JavaScript и выполняющий periodic API calls. Без additional context analyst должен решить, требует ли это escalation.

#### Interpretation 1: Assessment Without CTI Enrichment

Analyst использует доступный context. WHOIS показывает registration 36 hours ago, но newly registered domains обычны для SaaS vendors, создающих customer-specific infrastructure. Domain name выглядит consistent с legitimate secure document-transfer service.

Asset inventory показывает, что `172.16.42.108` — workstation accounting department. Accounting staff регулярно используют secure-document portals, electronic-signature platforms и vendor-payment systems. Traffic pattern — API calls, JavaScript loading, form submission — соответствует web application workflow.

Analyst делает defensible conclusion: вероятно, это новый vendor tool Accounting. При отсутствии evidence malicious behavior analyst documents finding и closes ticket.

**Risk Classification: Low — legitimate business activity, no further action.**

#### Interpretation 2: Assessment With CTI Enrichment

Второй analyst review тот же finding, но перед closure query CTI. Картина меняется.

Registrar — Namecheap, nameserver configuration — Cloudflare free tier, certificate — Let’s Encrypt; pattern совпадает с infrastructure fingerprints, documented recent CISA advisories for Scattered Spider operations. Domain naming convention `secure-[vendor]-portal.com` соответствует pattern, used threat actor для impersonation legitimate vendor login pages.

Дополнительная investigation показывает, что Scattered Spider в предыдущие **30 days** targeting technology companies через fake vendor portals для harvesting credentials и MFA tokens.

**Risk Classification: High — immediate containment affected workstation, user credential reset, expanded scoping, investigation whether credentials/sensitive data were submitted.**

Оба analysts смотрели на одни и те же proxy logs и применяли reasonable judgment. Первый conclusion был defensible при доступном context: domain выглядел legitimate, а user role объяснял traffic pattern. Без CTI indicators оставались ambiguous.

CTI query второго analyst превратил ambiguous finding в confirmed threat, показав infrastructure fingerprints, matching known adversary patterns. CTI не изменил technical evidence — он дал context, необходимый для правильной interpretation.

Threat intelligence также помогает risk classification через knowledge attacker capabilities и typical impact. CTI sources могут документировать outcomes previous campaigns: average dwell times, exfiltration volumes, recovery costs victims. Historical context позволяет calibrate risk по real-world consequences, а не theoretical harm.

При интеграции CTI в risk classification source рекомендует учитывать:

- **Attribution confidence:** насколько надёжно source links indicator specific actor/campaign?
- **Relevance to organization:** targeting ли actor industry, geography или size organization?
- **Attacker capability:** sophisticated persistent attacks или opportunistic take-what-they-can operations?
- **Typical impact:** какие outcomes наблюдались у previous victims?

> Absence threat intelligence не означает absence threat. Novel attacks, zero-days и emerging actors не появятся в CTI feeds до первых victims и последующего sharing intelligence. CTI — один input verification, а не sole proof.

## Pivoting to Related Indicators

Threat-intelligence platforms часто показывают relationships между indicators. Один suspicious indicator может быть связан с additional domains, IP addresses, hashes или behavioral patterns того же campaign/actor.

Когда CTI раскрывает related indicators, analysts могут spot-check дополнительные IOC в environment, чтобы понять, initial finding isolated или отражает broader compromise. Pivoting превращает single-indicator assessment в более comprehensive evaluation threat presence.

Например, domain hosting ransomware message может через CTI оказаться связанным с другими domains того же threat actor. Search proxy logs/DNS records по related domains может выявить additional affected users/systems, пропущенных initial detection. Это влияет и на verification decision continue/stop, и на последующий scope.

### Рисунок 63. CTI Enrichment Reveals Related Indicators

`THIRD_PARTY_REVIEW_REQUIRED` — visual asset не воспроизводится автоматически.

CTI pivoting также помогает anticipate, что искать после confirmation incident. Threat intelligence часто описывает TTPs actor/campaign. Если indicator относится к actor, известному specific persistence mechanisms или lateral-movement techniques, analysts могут proactively искать эти TTPs во время scope.

> CTI pivoting мощный, но не должен быть sole means verification. Threat actors adapt, а new indicators могут отсутствовать в intelligence. CTI не заменяет thorough investigation.

## VERIFICATION ACTIVITY EXAMPLES

### The Unresponsive WordPress Site

Повторяющийся help-desk ticket привлёк внимание IRT. WordPress server, используемый для customer documentation software product, регулярно становился down/unresponsive. Sysadmins несколько раз reboot server; после reboot problem temporarily исчезала, Engineering закрывал ticket, но system снова становилась unresponsive через hours/days.

Savvy help-desk analyst предположил, что issue шире, чем считает engineering. Для verification IRT collected Apache web-server logs. Review показал множество requests к specific PHP file в WordPress `wp-includes`, как в Listing 35.

### Listing 35. Apache Web Server Log Activity

```
42.105.168.75 - - [30/Jun/2024:00:36:29 -0400] "GET /wp-includes/FkhDUPZ.php HTTP/1.1" 200
65046892 "" "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko)
Chrome/126.0.0.0 Safari/537.36"
42.105.168.75 - - [30/Jun/2024:00:36:29 -0400] "GET /wp-includes/FkhDUPZ.php HTTP/1.1" 200
65046886 "" "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko)
Chrome/126.0.0.0 Safari/537.36"
42.105.168.75 - - [30/Jun/2024:00:36:29 -0400] "GET /wp-includes/FkhDUPZ.php HTTP/1.1" 200
65046884 "" "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko)
Chrome/126.0.0.0 Safari/537.36"
42.105.168.75 - - [30/Jun/2024:00:36:29 -0400] "GET /wp-includes/FkhDUPZ.php HTTP/1.1" 200
65046886 "" "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko)
Chrome/126.0.0.0 Safari/537.36" ①
```

① Multiple requests к `FkhDUPZ.php` возвращают unusually large HTTP responses.

Само по себе это ещё не подтверждало incident, хотя engineering не мог объяснить purpose oddly named file `FkhDUPZ.php` в `wp-includes`. IRT inspected file contents.

### Listing 36. Contents of Suspicious PHP File

Canonical source содержит obfuscated PHP source code и явно помечает его как truncated. Код сохраняется в canonical English RAG как technical evidence.

`THIRD_PARTY_REVIEW_REQUIRED` — обфусцированный malicious/unknown PHP payload не дублируется в производный reader-facing перевод; сохраняются filename, purpose listing и факт obfuscation. Canonical English RAG остаётся source of truth для byte-level/verbatim analysis.

Obfuscated code само по себе не доказывает malicious intent. Legitimate WordPress plugins/themes иногда obfuscate source для licensing/IP protection, поэтому IRT рассматривает obfuscation как reason for review, не как confirmation.

IRT computed SHA-256 `FkhDUPZ.php` и submitted CTI sources, которые returned matches known PHP webshell families. Дополнительно team проверила official WordPress release manifest для installed version: `FkhDUPZ.php` отсутствовал, значит файл был добавлен вне legitimate update process.

CTI match + file-integrity discrepancy вместе подтвердили incident. IRT escalated event, подключив broader incident response team, stakeholders и decision makers.

> Undesirable activity — high CPU, unexpected storage consumption, unexplained instability — не всегда IOC, но требует root-cause investigation. Здесь verification строилась на Apache anomalies, frequent requests к `FkhDUPZ.php`, unusually large responses и analysis suspicious file.

### The Unpaid Toll

Accounts payable clerk forwarded suspicious SMS в IRT. Message представлялось уведомлением Rhode Island Turnpike and Bridge Authority (RITBA), требуя payment unpaid toll.

### Рисунок 64. Suspicious Text Message

`THIRD_PARTY_REVIEW_REQUIRED` — third-party/suspicious-message visual и verbatim message не воспроизводятся; сохраняется авторское описание.

Initial investigation показала redirect с SMS URL на `rhodeislandturnpike.com`, а затем на longer URL.

### Рисунок 65. Unpaid Toll Redirect to “Rhode Island Turnpike” Website

`THIRD_PARTY_REVIEW_REQUIRED` — website visual не воспроизводится автоматически.

Site выглядел semi-professional и визуально напоминал Rhode Island government websites, но IRT suspected phishing. Threat-intelligence resources показали, что domain был зарегистрирован **в тот же день**.

### Listing 37. Domain Registration Creation Date

```
$ date -u
Sun Feb 16 20:11:32 UTC 2025
$ whois -i rhodeislandturnpike.com | grep -i 'creation date'
   Creation Date: 2025-02-16T06:37:27Z ①
```

① Domain registration создан менее чем **14 hours** назад.

Server certificate также был создан в тот же день.

### Listing 38. Website Server Certificate Start Date

```
$ date -u
Sun Feb 16 20:13:31 UTC 2025
$ curl -svX HEAD https://rhodeislandturnpike.com/ 2>&1 | grep -A6 "Server certificate"
* Server certificate:
*  subject: CN=rhodeislandturnpike.com
*  start date: Feb 16 06:01:28 2025 GMT ①
*  expire date: May 17 06:01:27 2025 GMT
*  subjectAltName: host "rhodeislandturnpike.com" matched cert’s "rhodeislandturnpike.com"
*  issuer: C=US; O=Let’s Encrypt; CN=E5
*  SSL certificate verify ok.
```

① TLS certificate создан примерно **14 hours** назад.

Clerk сообщил, что не открывал SMS link и не посещал website. Browser history подтвердил это. Analyst также не нашёл web activity к domain в company web-proxy logs.

После consultation с другим IRT analyst event классифицирован как **Indicator of Attack (IOA)**, но **не EOI**, требующий further investigation. Domain и server IP добавлены в threat-intelligence platform для monitoring, incident closed.

> Indicator of attack не всегда становится event of interest. Verification позволяет ограничить число incidents, требующих дальнейшего investigation, и сосредоточиться на наиболее significant для organization.

## The Simple, Secure Storage Bucket

Analyst incident response team получил report о disclosure vulnerable Amazon Simple Storage Service (S3) bucket. Report пришёл от unknown source — self-identified bug bounty hunter, который заявил о high-risk vulnerability в bucket `ssptmsdata` и спросил о policy organization по reward bug bounty hunters.

Company analyst проверила report и подтвердила, что `ssptmsdata` действительно используется одним из AWS accounts organization. Через AWS Command Line Interface она review security settings bucket.

### Listing 39. AWS S3 Bucket Policy

```json
$ aws s3api get-bucket-policy --bucket ssptmsdata | jq '.Policy | fromjson'
{
  "Version": "2012-10-17",
  "Id": "ssptmsdata-Policy",
  "Statement": [
    {
      "Sid": "AllowPublicRead",
      "Effect": "Allow",
      "Principal": {
        "AWS": "*"
      },
      "Action": [
        "s3:Get*", ①
        "s3:List*" ②
      ],
      "Resource": [
        "arn:aws:s3:::ssptmsdata",
        "arn:aws:s3:::ssptmsdata/*"
      ]
    }
  ]
}
```

① Bucket policy позволяет любому AWS principal выполнять S3 get actions, включая `GetObject`, `GetBucketLocation`, `GetBucketPolicy` и другие.  
② Bucket policy позволяет любому AWS principal выполнять S3 list actions, включая `ListObjects`, `ListBucketAnalyticsConfigurations` и другие.

Review policy подтвердил: любой AWS principal из любой organization мог list bucket files и retrieve contents любого file.

Однако analyst знала, что bucket используется для public data sharing: company website resources, images, CSS, fonts, JavaScript и related data.

Чтобы определить, требуется ли IRT action, analyst review bucket contents.

### Listing 40. AWS S3 Bucket Contents

```
$ aws s3 ls s3://ssptmsdata
                           PRE css/
                           PRE dist/
                           PRE fonts/
                           PRE images/
                           PRE js-lib/
                           PRE js/
                           PRE pdf/
                           PRE uat/
$ aws s3 ls s3://ssptmsdata/uat/
2025-02-14 14:56:41     112537 acceptance_summary.pdf
2024-05-12 11:03:12       2520 config.json
2025-02-05 11:20:15      19264 cross_browser_test.xlsx
2024-11-15 09:12:45       5515 database_seed.sql
2025-01-03 14:22:01       6472 error_log.log
2024-10-12 12:01:42      15036 feature_toggle.yaml
2024-12-15 08:45:33      22491 integration_test.py
2025-01-25 10:05:35      17055 mobile_test_cases.docx
2025-02-10 12:40:03      14491 performance_metrics.csv
2024-11-23 17:05:19      12848 performance_report.txt
2024-09-20 11:45:50      30059 sample_api_response.json
2024-12-01 10:03:58      40927 sample_users.csv
2025-01-15 13:35:22      24037 security_audit.txt
2024-10-05 15:27:35      19957 test_case.docx
2024-06-17 14:22:10      17103 test_script.sh
2024-11-03 16:30:11       1987 uat.env
2024-09-01 10:10:31      10295 uat_deploy.sh
2024-09-15 08:33:25       9087 uat_log.txt
2025-01-20 09:50:38      26982 ui_mockup.png
2024-07-20 09:15:05      41033 user_data_sample.csv
```

Bucket содержал folders, выглядящие как public website resources, а также `pdf` и `uat` (User Acceptance Testing). В `pdf` находилась public documentation; `uat` содержал documentation, test data и sample configuration data нескольких products.

Неясным оставалось главное: соответствует ли bucket configuration и data business needs organization? Было ли намерение share data publicly или это misconfiguration? Есть ли sensitive files или всё предназначено для public use?

Analyst связалась с AWS account holder bucket `ssptmsdata`, чтобы подтвердить purpose/contents. Она попросила responsible team review каждый file на sensitive disclosure, обозначила urgency и запросила analysis до end of day. После этого можно было решить, требуют ли bucket configuration и information disclosure дальнейшего IRT investigation.

> Во время verification analysts используют available information, threat/risk insight, organizational policies/procedures и knowledge из preparation, чтобы выбрать appropriate response. Иногда information недостаточно — тогда verification decision нужно defer до получения additional data.

### A TEMPERAMENTAL SERVER

Customer обратился за investigation Windows server с erratic behavior. System administrator наблюдал unexpectedly high CPU utilization across multiple processes, crashed services и unexplained password changes. Это продолжалось weeks, пока administrator не столкнулся с Blue Screen of Death (BSOD). Customer нанял team для определения source предполагаемой compromise.

System была virtual machine, поэтому snapshot и offline analysis были straightforward. Несколько days ушло на investigation processes, services, scheduled tasks, WMI queries и других system elements. Были review system logs, network activity, memory dumps и forensic artifacts.

IOC обнаружены не были.

Customer настаивал, что system compromised: unexpected behavior казалось ему evidence adversary control, а investigators якобы что-то missed. Team сохранила позицию, что после sufficient investigation assessment customer является false positive.

Some incidents дают clear IOC; другие не подтверждаются, несмотря на persistent unexplained behavior. Нужно принимать, что verification иногда не выявит compromise even when behavior suggests otherwise.

Для этого customer team потратила дополнительное время на demonstration collected evidence и explanation, почему system considered uncompromised. В итоге customer rebuilt system from scratch, после чего unexpected behavior прекратилось.

Example показывает recurring challenge — **proving a negative**. Для confirmation compromise достаточно одного credible IOA/EOI. Для confidence в no-compromise нужно показать coverage relevant attack surface: running processes, persistence mechanisms, scheduled tasks, file-system changes, network activity, authentication logs.

Stakeholders редко принимают “we found nothing” с той же уверенностью, что “we found something”, поэтому analysts могут столкнуться с pressure продолжать investigation после reasonable scope.

Defensible response — explicitly document investigation scope:

- что examined;
- какие tools used;
- какие time windows covered;
- какие evidence sources были unavailable/out of reach.

С таким record clean verdict защищается выполненной работой, а не просто absence findings.

## TRIAGE ACTIVITY

Во время triage analysts работают с decision makers и определяют appropriate response actions на основе risk impact classification и available incident information. Actions могут включать allocation resources для investigation, engagement legal counsel или notification law enforcement в зависимости от severity.

Немногие organizations могут сказать, что incident response function имеет excess resources. Для большинства IR — cost center, consuming money, а не profit center, generating revenue. Поэтому consumed resources неизбежно scrutinized.

Во время triage analyst даёт decision makers достаточный insight для выбора response actions на основе risk classification и information после verify activity.

В medicine triage определяет priority treatment по severity condition. Broadly, high-severity patients идут раньше lower-severity. В incident response аналогично: threats prioritised по organizational policies, часто через potential negative impact.

### Presenting the Incident

Technical analysts должны помочь decision makers понять incident и potential impact. Insights verification и initial risk assessment существенно влияют на triage и response actions.

При presentation source рекомендует:

- **Be clear and concise:** plain language для incident и potential impact.
- **Provide context:** связать incident с policies/procedures и operational impact.
- **Offer recommendations:** предложить response actions по risk classification и available information.
- **Be prepared to answer questions:** decision makers могут спросить об incident, impact и recommended actions.

Decision maker должен учитывать impacted service, potential organizational impact, regulatory exposure и resources available. Analyst даёт incident insight, но ultimate responsibility за appropriate response actions/resource allocation остаётся у decision maker, который учитывает overall organizational needs.

Open communication между IRT и decision makers формируется ещё в preparation activity.

## TRIAGE EXAMPLE: THE THIRD-PARTY VENDOR BREACH

Third-party SaaS vendor, используемый для Customer Relationship Management, уведомил organization о data breach. Vendor заявил, что affected customer contact information — names, email addresses, phone numbers — примерно **45,000 customers**.

До escalation decision makers IRT собрала independent evidence, не полагаясь только на vendor account:

- API gateway logs и egress traffic records: какие data fields vendor integration accessed в указанный window;
- Single Sign-On authentication events: какие internal users имели active sessions;
- Cloud Access Security Broker (CASB) telemetry: anomalous session behavior или bulk transfers.

Cross-reference этой telemetry с customer records в собственном system of record дал affected record count ниже vendor figure. Analyst classified incident как **high-risk** из-за possible notification requirements GDPR/state privacy laws и отметил scope discrepancy как open item для reconciliation vendor.

IRT presented verified incident **VP of Customer Experience** — accountable decision maker, owning customer relationship/business process. **VP of Legal** участвовал advisory, интерпретируя regulatory obligations и coordinating external counsel.

Presentation включала:

- independent evidence records in scope + discrepancy vendor figure;
- possible regulatory notification timelines — **72 hours для GDPR-covered residents**;
- legal obligation notify customers, contingent on confirming exposed fields;
- coordination dependencies между Customer Experience, Legal, Marketing и IRT.

VP Customer Experience authorized IRT resources для продолжения vendor coordination на следующую week и обязала team reconcile affected count с organization system of record.

VP Legal engaged external privacy counsel для notification drafting после scope confirmation, allocated budget и set drafting timeline.

Совместно они установили **daily 30-minute status call** с Marketing и executive leadership.

Role IRT analyst сместилась от technical investigation к coordination/documentation support. Analyst продолжил independent reconciliation вместе с Customer Experience и Legal, чтобы выполнить regulatory obligations и не отправить notifications шире confirmed scope.

> При third-party incidents analysts должны объяснять decision makers, как external dependencies влияют на resource allocation и response timelines. Role analyst может переходить от technical investigation к coordination, особенно когда response определяется regulatory/legal context. Decision makers должны понимать не только technical details, но и organizational/legal context.

## VERIFY AND TRIAGE: STEP-BY-STEP

Следующие steps дают condensed reference для verification/triage: validation potential incident, risk assessment и совместное с decision makers определение priorities. Verification выступает gating function перед engagement broader team и предотвращает expenditure resources на incidents, которые не реальны.

Source указывает, что guide доступен в PDF/Markdown на `dynamicincidentresponse.com`.

### Step 1. Document the Incident Details

Использовать incident-tracking platform, established during preparation. Representative fields:

- Incident identifier;
- Title;
- Handler ID;
- Summary;
- Classification;
- Evidence references.

Maintain documentation integrity: notes focused на incident at hand; не допускать contamination, снижающую validity evidence in legal proceedings.

### Step 2. Enrich Events of Interest with Cyber Threat Intelligence

Representative activities:

- query CTI по IP addresses, domains, URLs, hashes observed in environment;
- cross-reference multiple CTI sources;
- check indicators against local knowledge base known false positives;
- pivot related indicators и spot-check environment только в объёме, необходимом для verification decision. Enterprise-wide hunting full IOC set относится к **scope** после verification.

### Step 3. Perform an Initial Risk Assessment

Classify incident как low/medium/high/critical или иной organizational scheme.

Consider:

- attribution confidence;
- relevance to organization;
- attacker capability;
- typical impact из CTI.

Не считать absence CTI evidence доказательством absence threat.

### Step 4. Verify the Incident

Использовать detect information + CTI enrichment и выбрать один outcome:

- **Continue:** incident real; escalate broader IRT/stakeholders.
- **Stop:** incident not real. Closing unusual-but-benign finding требует strong documentation:
  - document trigger, evidence ruling out compromise, covered time window/data sources;
  - add benign source local false-positive knowledge base;
  - notify original reporter/downstream stakeholders;
  - close in tracking platform с clear classification: false positive, authorized activity, duplicate или other.
- **Defer:** information insufficient; запросить additional information before determination.

### Step 5. Triage by Presenting to Decision-Makers

Present verified incident managers/executives/data owners/legal/business-unit leaders с authority.

Representative activities:

- plain language;
- context через policies/procedures/operations;
- recommendations по risk classification и available information;
- готовность отвечать на вопросы по impact/actions.

### Step 6. Work with Decision-Makers on Response Actions and Resource Allocation

Decision makers должны учитывать:

- impacted service;
- potential organizational impact;
- regulatory exposure;
- resources available.

Response actions могут включать investigation resources, legal counsel или law-enforcement notification.

Analyst role может shift в coordination support, особенно при legal/regulatory-driven response.

### Step 7. Review and Improve the Verification and Triage Process

Representative activities:

- track false-positive rate at triage как quality indicator; drift может означать необходимость upstream detection tuning;
- track incidents initially stopped/deferred; если later reopened as real, diagnose misses и update criteria;
- periodically rerun prior incidents through current verification workflow, проверяя risk assessment, CTI enrichment и decision-maker presentation;
- capture recurring blockers: ambiguous alerts, missing enrichment sources, unclear escalation paths; feed improvements в Prepare/Detect;
- solicit decision-maker feedback: помогла ли presentation принять informed decision; recurring follow-up questions могут указывать на gaps framing incident.
