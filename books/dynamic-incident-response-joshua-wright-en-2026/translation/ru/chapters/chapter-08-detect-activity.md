---
book_id: dynamic-incident-response-joshua-wright-en-2026
chapter_number: 8
source_title: "Detect Activity"
source_pdf_page_range: "166-189"
rag_chunk_range:
  first: "dynamic-incident-response-joshua-wright-en-2026:p0166:c01"
  last: "dynamic-incident-response-joshua-wright-en-2026:p0189:c01"
translation_status: "ACCEPTED"
license_notice: "Неофициальный русский перевод / unofficial Russian translation; original work CC BY 4.0. См. ../ATTRIBUTION.md."
third_party_review_policy: "Figures and direct third-party verbatim material remain fail-closed."
translation_notes:
  - "Canonical English RAG is source of truth."
  - "Assembled from full-fidelity source-range segments."
  - "Technical listings are preserved unless an explicit third-party boundary applies."
---

# Глава 8. Обнаружение

Действие **detect — обнаружение** является важной фазой модели, в ходе которой организации выявляют потенциальные incidents, используя различные information sources и analysis techniques. Как incident response analysts, мы проводим значительную часть времени в detection activities, ища признаки компрометации и потенциальные threats, требующие расследования.

### Рисунок 50. Опорная точка Detect Activity

`THIRD_PARTY_REVIEW_REQUIRED` — визуальный объект не воспроизводится автоматически; сохраняются подпись и cross-reference.

## МЕТОДОЛОГИИ ОБНАРУЖЕНИЯ

Современные detection programs используют несколько methodologies для выявления threats; у каждой есть собственные сильные стороны и ограничения. Понимание этих подходов помогает analysts выбирать подходящие techniques для разных threat scenarios. В этом разделе рассматриваются четыре methodologies: signature-based detection, behavioral detection, machine learning detection и hybrid approaches, объединяющие эти techniques.

### Signature-Based Detection

Signature-based detection использует известные patterns для выявления threats: file hashes, byte sequences, malicious domains, indicators network protocol/port number и другие признаки. Этот подход эффективно обнаруживает известные malware и attack patterns и обычно имеет низкий false-positive rate. Automated systems особенно эффективны при signature-based detection, быстро обрабатывая данные и выявляя matches.

Главное преимущество signature-based detection — эффективность и точность для известных threats. Signatures дают high-confidence indicators того, что атака произошла, и позволяют быстро выполнять automated response: quarantining files, blocking network connections или alerting analysts. Высокая скорость signature matching позволяет организациям обрабатывать большие объёмы data при множестве потенциальных threats.

Основное ограничение signature-based detection — reactive nature. Новые malware variants, zero-day exploits и novel attack techniques обходят signature detection до тех пор, пока researchers не проанализируют samples и не создадут matching patterns. Attackers, способные reverse-engineer detection signatures, могут изменить tools, чтобы избежать match, делая signature-based systems неэффективными против sophisticated adversaries.

> Организации, полагающиеся только на signature-based detection, с высокой вероятностью пропустят novel threats.

### Behavioral Detection

Behavioral detection отслеживает actions, а не static indicators, и выявляет threats по тому, **что они делают**, а не по тому, **как они выглядят**. Подход строит baselines normal activity и отмечает deviations, требующие investigation.

Behavioral detection особенно полезен для threats, которые пропускает signature-based approach:

- **Mass file encryption:** выявление patterns, характерных для ransomware.
- **Unusual access patterns:** off-hours authentication или atypical access к sensitive resources.
- **Living-off-the-land techniques:** legitimate tools, применяемые maliciously.
- **Insider threats:** misuse authorized access privileges.

Behavioral detection требует careful tuning, чтобы сбалансировать detection coverage и false-positive rate. Analysts должны совместно с team формировать accurate baselines, отражающие нормальную работу организации.

### SCOPING BASELINES TO BUSINESS UNITS

Для крупных networks единый organization-wide baseline часто слишком широк, чтобы обеспечивать meaningful anomaly detection. Разные business units работают в fundamentally different technical environments; усреднение между ними размывает именно те различия, которые делают anomalies заметными.

Рассмотрим крупного defense contractor с отдельными divisions для aeronautics, mission systems и corporate IT. Aeronautics division создаёт heavy CAD/CAM file transfers и взаимодействует со specialized supply-chain partners. Mission systems division работает с classified networks, strict access controls и minimal external connectivity. Corporate IT использует standard business applications с predictable Office 365 и SaaS traffic patterns. Baseline, построенный одновременно по всем трём divisions, определит «normal» настолько широко, что meaningful deviations растворятся в noise.

### Рисунок 51. Baseline defense contractor по business units

`THIRD_PARTY_REVIEW_REQUIRED` — визуальный объект не воспроизводится автоматически.

Healthcare organizations сталкиваются с похожими проблемами. Research laboratories генерируют large data transfers в cloud compute resources и обращаются к specialized databases, тогда как clinical operations создают predictable EHR access patterns с periodic spikes при смене shifts. Единый baseline по обеим groups либо будет считать routine research transfers anomalous, либо не сможет выявить unusual access в clinical environment.

Scoping baselines до business units или functional groups создаёт более узкие определения normal activity. Такие baselines делают genuine anomalies заметнее и уменьшают false-positive rate, позволяя analysts направлять investigative effort на events, действительно требующие внимания.

### Machine Learning Detection

Machine learning усиливает behavioral detection, выполняя scoring events и correlation patterns at scale. Unsupervised learning algorithms автоматически формируют baselines, а supervised models классифицируют events как malicious или benign на основе training data. Эти capabilities особенно полезны для high-volume telemetry analysis и обнаружения subtle patterns в distributed systems.

> Supervised models учатся на labeled examples, где analysts уже определили events как malicious или benign. Они хорошо обнаруживают известные attack patterns, но могут плохо работать с novel techniques, отсутствующими в training data. Unsupervised models учатся normal behavior без labeled examples; это помогает находить unknown threats, но создаёт больше false positives, когда legitimate activity отклоняется от baseline.

Организации, внедряющие ML-based detection, должны понимать ограничения этих systems, включая model drift, проблемы training data quality и evasion techniques.

**Model drift** возникает по мере эволюции attacker techniques и organizational environments и постепенно ухудшает detection accuracy. Model, обученная на прошлогодних attack patterns, может не распознать техники текущего года, особенно если adversaries адаптируют methods для evasion. Environmental drift также вносит вклад: adoption новых technologies, изменение business processes или workforce patterns сдвигают baseline «normal».

Training data quality напрямую влияет на detection accuracy и на то, что ML-based detection вообще способна сделать. Models, trained на incomplete datasets, не смогут характеризовать attack techniques, отсутствующие в training data. Contaminated training data с mislabeled examples обучает models неправильным classifications. Supervised models испытывают трудности с attack patterns, которых они никогда не встречали.

При **model evasion attacks** adversaries формируют inputs, рассчитанные на обход ML classification. Attackers, понимающие принцип работы models, могут менять techniques так, чтобы оставаться чуть ниже detection thresholds, или exploit deficiencies model training. Model evasion применялся против malware detection, spam filtering и image recognition classifiers.

**Human-in-the-loop (HITL)** approaches уменьшают эти ограничения, объединяя machine efficiency и human judgment. Вместо восприятия ML outputs как definitive determinations эффективные detection programs используют ML для выделения high-priority signals, которые затем проверяет человек. Analysts добавляют context, которого нет у models: recent organizational changes, ongoing projects, способные объяснить unusual activity, и intuition, сформированную расследованием похожих alerts.

HITL workflows также создают feedback loops, улучшающие model performance: decisions analysts по flagged events дают labeled data для retraining. Где возможно, detection workflows следует проектировать так, чтобы ML выполнял initial triage/prioritization, но final classification и response actions оставались под human decision authority. Такой подход позволяет human expertise участвовать в continuous improvement models/classifiers.

### Hybrid Detection Approaches

Эффективные detection programs объединяют несколько methodologies, используя их complementary strengths. Signature-based, behavioral и machine-learning techniques вместе позволяют строить robust detection capabilities, уменьшая false positives и false negatives. Многие современные threat detection tools интегрируют signature matching, behavioral analysis и ML в одной platform.

Detection logic всё чаще maps attacker Tactics, Techniques, and Procedures к frameworks вроде MITRE ATT&CK.[1] Если фокусироваться на adversary behaviors, а не specific indicators, detection rules остаются effective даже при изменении attacker tools. В результате конкретный detection method — signature, ML или behavioral — становится менее важен, чем underlying technique. Использование нескольких methods для одной threat повышает detection confidence и уменьшает вероятность false positive.

Layered approach даёт defense-in-depth для detection: signatures эффективно ловят known threats, behavioral analysis выявляет novel techniques, ML поднимает subtle patterns, которые могут уйти от rule-based detection.

## ACTIVE VS. PASSIVE DETECTION

Detection activities делятся на две основные categories: passive и active detection.

**Passive detection** происходит, когда организация узнаёт об incident через reports: internal staff замечает unusual activity, external partners передают threat intelligence или automated alerting systems создают notifications. Этот reactive approach необходим, но часто приводит к более длинному detection time и потенциально большему impact.

**Active detection**, также называемый threat hunting, означает proactive search Events of Interest (EOI) в environment. Threat hunting analysts анализируют logs, network traffic, system behavior patterns и другие data sources, чтобы выявлять compromises, которые могли обойти automated detection systems. Такой подход способен существенно снизить Mean Time to Detect (MTTD) — время между началом incident и его обнаружением организацией.

> Снижение MTTD остаётся постоянным приоритетом incident response teams, поскольку более быстрое detection обычно коррелирует с меньшим incident impact.

### THE TYRANNY OF INFINITE CHOICE

Incident response и threat hunting имеют fundamentally different starting points, как отмечает security researcher Faan Rossouw.[2] При response analyst начинает с defined indicator: сработал alert, user сообщил suspicious activity, third party уведомила организацию о compromise. Starting point уже задан, и investigation развивается от этого anchor.

Threat hunters сталкиваются с другой проблемой: искать unknown threats без predefined indicators. Alert не сработал. Ни одна system не отметила что-либо suspicious. Hunter смотрит на миллионы log entries, тысячи systems и сотни possible threat vectors, когда ничего не выглядит явно wrong. Rossouw называет это **tyranny of infinite choice**: hunter должен решить не только *что* расследовать, но и *с чего начать*, *как prioritise* и *почему одна hunting hypothesis важнее бесчисленных alternatives*.

### Рисунок 52. Pyramid of Pain

`THIRD_PARTY_REVIEW_REQUIRED` — визуальный объект не воспроизводится автоматически.

Pyramid of Pain, созданная David Bianco в 2013 году, даёт mental model, помогающий threat hunters выйти из paralysis.[3] Pyramid размещает adversary artifacts по тому, сколько «pain» их изменение причиняет attacker. Внизу — hash values и IP addresses, которые adversaries меняют легко. Наверху — TTPs, operational methods, на которые adversaries опираются и которые трудно быстро заменить.

Model предлагает hunters направлять ограниченное время туда, где изменение действительно болезненно для adversary. Search known malicious hashes/IP имеет мало value для human hunters, поскольку automated systems делают это быстрее. Лучше подниматься вверх к behavioral indicators: beaconing patterns, указывающим на C2 communications; suspicious process-creation chains, где legitimate tools неожиданно запускают друг друга; lateral movement techniques, раскрывающим adversary procedures.

Pyramid также показывает tradeoff. Lower-level indicators вроде hashes дают high-confidence detection с minimal false positives, но adversary легко их меняет. Higher-level indicators вроде TTPs требуют значительной expertise для reliable detection, зато выявляют tradecraft, сохраняющийся между campaigns.

Skilled threat hunters понимают эти tradeoffs и выбирают focus исходя из strategic impact, а не tactical convenience.

## DETECTION DATA SOURCES

Эффективное detection использует technical и human data sources. Technical sources дают данные для выявления malicious activity; human sources добавляют institutional knowledge, context и observations, которые automated systems могут пропустить.

Далее рассматриваются technical platforms, создающие detection telemetry, human observations и specialized considerations cloud-native environments.

### Technical Detection Sources

Detection зависит от technical infrastructure, развёрнутой во время preparation. В Prepare Activity подробно рассматривались deployment/configuration detection infrastructure; здесь focus — как analysts используют эти capabilities.

**Endpoint Detection and Response (EDR)** даёт host-level visibility, необходимую для многих attacker TTPs с минимальным network traffic. EDR telemetry включает event information, раскрывающую complex attack patterns: process injection, credential dumping, persistence deployment, suspicious parent-child process relationships и другие indicators. Analysts могут query EDR для hunting indicators по managed endpoints и поиска threats. Та же telemetry используется для scoping, выявляя другие compromises по известному IOC.

EDR systems существенно улучшили endpoint security и являются essential component современных security programs. Помимо visibility, platforms объединяют alerting и hunting в едином dashboard, как в SentinelOne example на Figure 53. Они часто интегрируются с SIEM/SOAR и другими detection/reporting/orchestration tools.

### Рисунок 53. SentinelOne EDR Dashboard

`THIRD_PARTY_REVIEW_REQUIRED` — product screenshot не воспроизводится автоматически.

Ни один EDR не даёт perfect protection, но такие platforms создают valuable data для detection/investigation.

Если endpoint visibility фокусируется на отдельных hosts, **Network Detection and Response (NDR)** и flow data дают широкую visibility по environment через анализ traffic attributes и communication patterns. Use cases: C2 beaconing через timing analysis, lateral movement через unusual internal traffic, potential data exfiltration через anomalous outbound volumes.

> Network-based detection дополняет endpoint visibility, показывая attacker activity, проходящую через несколько systems.

**SIEM** platforms позволяют simple search и complex correlation-based detection по diverse log sources. Rules могут находить attack patterns между systems: authentication failures followed by success, privilege-escalation sequences, coordinated access to sensitive resources. Splunk, Elastic Security и Microsoft Sentinel дают analysts мощные search capabilities для alerting и threat hunting.

**SOAR** platforms уменьшают MTTR и risk, автоматизируя response high-confidence alerts. При clear threats они могут quarantine endpoints, block malicious IPs, disable compromised accounts и capture forensic data. Automation уменьшает attacker dwell time и освобождает analysts для сложных investigations. SOAR case management помогает track detection events, link related alerts и document findings.

### OPENOBSERVE: OPEN SOURCE LOG ANALYSIS

OpenObserve — open-source observability platform, объединяющая log search, metrics collection и trace analysis в одном binary. Для IRT это lightweight alternative commercial SIEM для centralized log aggregation/analysis.

OpenObserve принимает logs от common collection agents и предоставляет SQL-based query interface для поиска по diverse sources. Низкий resource footprint по сравнению с traditional indexing platforms делает его practical для организаций, которым нужен search без infrastructure overhead full SIEM.

### Рисунок 54. OpenObserve Dashboard for AWS Event Analysis

`THIRD_PARTY_REVIEW_REQUIRED` — product screenshot не воспроизводится автоматически.

OpenObserve не заменяет full SIEM с correlation rules/automated alerting, но его легко развернуть и использовать, если team нужно быстро query logs во время investigation.

Это не exhaustive list. Email gateways, web proxies, cloud-native logging, Cloud Workload Protection Platforms (CWPP) и другие specialized monitoring tools также дают detection data. Организация должна выбирать platforms, обеспечивающие лучшую visibility именно для её environment.

## RITA: OPEN SOURCE NETWORK THREAT ANALYSIS

Real Intelligence Threat Analytics (RITA) — free open-source tool, применяющий statistical anomaly analysis к network activity для выявления command-and-control communications, которые signature-based detection может пропустить.[4] RITA не ищет signatures конкретных C2 frameworks. Вместо этого tool выявляет behavioral characteristics, общие для большинства C2 tools: long connection durations, beaconing intervals, consistent packet sizes, unusual subdomain patterns и другие anomalies, отличающие attacker activity от normal network traffic.

Такой approach позволяет RITA обнаруживать novel C2 frameworks, ранее не наблюдавшиеся, поскольку новые tools демонстрируют те же behavioral characteristics, что и established ones. Organizations могут использовать RITA как дополнение к commercial detection tools и получать statistical-analysis capabilities, которых некоторые NDR platforms вообще не имеют.

RITA анализирует Zeek log files, но это не означает, что organization нужен full Zeek sensor deployment. Analyst может capture network traffic в network edge location — желательно **24 hours или дольше** — а затем convert packet capture в Zeek logs через command-line tool `zeek`, как показано в Listing 29.

### Listing 29. Zeek Log Generation and RITA Import

```
$ zeek -Cr capture.pcap
$ /opt/rita/rita.sh import -l ~/zeek-logs -d InvestigationDB
…
Finished Analysis! analysis_began=1723660142 analysis_finished=1723660142
Finished Import! elapsed_time=4.8s
$ /opt/rita/rita.sh view InvestigationDB
```

Flag `-C` указывает Zeek обрабатывать packets даже с invalid checksums, что часто встречается в truncated captures. RITA импортирует полученные logs и применяет analysis algorithms, scoring connections по beacon consistency, connection duration, subdomain patterns и другим threat indicators.

### Рисунок 55. RITA Threat Analysis Results

`THIRD_PARTY_REVIEW_REQUIRED` — visual output не воспроизводится автоматически.

Terminal interface RITA показывает найденные threats, ranked по severity: critical, high, medium, low или none. Для каждой threat RITA сообщает source/destination addresses, beacon score — показатель interval consistency, — connection duration, prevalence среди internal hosts и protocol details. High beacon score означает consistent communication intervals между двумя hosts и является сильным indicator automated C2 communication.

Как free tool RITA даёт powerful network threat-detection capabilities без licensing costs. Tradeoff — deployment effort: RITA работает на Linux и требует analyst expertise для правильной интерпретации results.

## HUMAN DETECTION SOURCES

Human observations остаются важным detection source и часто выявляют проблемы, которые пропускают automated systems. В Prepare Activity рассматривались security awareness training programs, развивающие эту capability и позволяющие использовать employee observations как источник incident detection.

Employees часто являются first line of defense: сообщают suspicious emails, unusual system behavior или social-engineering attempts. Effective training и culture, поощряющая reporting suspicious events, помогают staff распознавать IOC и понимать reporting procedures. Source отмечает, что pop-culture references могут повышать engagement; Figure 56 показывает Dall-E-generated poster, призывающий employees сообщать suspicious activity.

### Рисунок 56. The Danger Things Dall-E Poster

`THIRD_PARTY_REVIEW_REQUIRED` — visual asset не воспроизводится автоматически.

> Когда employees сообщают suspected incidents, даже false alarms, organization получает detection coverage, которую technical systems дать не могут. Culture of vigilance повышает вероятность reporting и улучшает overall detection capabilities.

System administrators и help desk personnel часто замечают anomalies при routine operations: server постоянно crashes, unexpected network traffic patterns, unauthorized changes в managed systems. При proper escalation такие observations могут раскрыть ongoing compromise. Clear escalation paths, созданные во время preparation, обеспечивают своевременную передачу этих observations incident response team.

То, как SOC analysts и help desk staff отвечают employee reports, не менее важно, чем сам факт reporting. Dismissive response, slow acknowledgment или confusing intake process discourages future reporting и разрушает culture of vigilance, от которой зависит detection program. Organizations следует разработать professional supportive communication templates для acknowledgment reports, status updates и closing loop после investigation. Даже если report оказался false alarm, краткая благодарность reinforces желаемое поведение.

> Timely supportive communication подтверждает ценность employee reports и помогает staff чувствовать себя участниками detection effort.

Third-party notifications от customers, partners или security researchers иногда становятся первым признаком breach. Это неideal по detection timeline, но остаётся важным detection source. Published `security.txt` file по RFC 9116 даёт standard channel, через который researchers могут напрямую reach security team. Organizations должны иметь procedures для receiving/validating external notifications как часть preparation.

## CLOUD-NATIVE DETECTION SOURCES

Cloud-native detection — specialized subset technical detection, заслуживающий отдельного рассмотрения из-за особенностей cloud: ephemeral workloads, API-driven infrastructure, shared-responsibility models и distributed architectures. EDR, NDR и SIEM по-прежнему применимы, но cloud environments добавляют новые data sources и detection patterns. Specialized solutions различаются по architecture: containerized, serverless или hybrid.

> Chapter *Incident Response for Cloud Systems* рассматривает cloud detection подробнее, включая provider-specific tooling и cross-cloud correlation.

### Container and Kubernetes Detection

Container/Kubernetes detection использует несколько approaches.

Kernel-level monitoring через **eBPF** позволяет наблюдать system calls containerized workloads и выявлять unexpected processes, file-system modifications и anomalous network connections.

Container runtime socket monitoring наблюдает Docker/containerd API и lifecycle events, image operations и configuration changes, которые могут указывать на compromise или policy violation.

Logging systems, включая Kubernetes audit events, дают visibility API-server activity и позволяют выявлять unauthorized pod creation, privilege-escalation attempts и access sensitive secrets.

Service mesh architectures дают дополнительную network-level visibility между services и фиксируют traffic patterns, которые kernel/runtime monitoring могут пропустить. Для traffic, входящего/выходящего cluster, NDR tools на ingress points дополняют mesh-level monitoring.

> Container environments создают уникальные detection challenges из-за ephemeral nature. Когда container terminates, evidence compromise может исчезнуть до investigation. Нужны centralized log collection и runtime detection tools, способные capture forensic artifacts real-time для high-sensitivity workloads.

### Serverless and Microservices Detection

В agentless environments, включая serverless functions/microservices, traditional endpoint agents не могут работать, поэтому требуются alternative approaches.

Primary sources — cloud-provider logs, function telemetry и event anomaly analysis. Analysts должны искать:

- abnormal invocation patterns;
- unexpected outbound connection attempts;
- unusual access к secrets/environment variables;
- deviations baseline execution: timeouts, throttling, unusual memory/CPU consumption.

Ephemeral nature делает real-time detection особенно важным: evidence существует короткое время.

### Hybrid Cloud

Detection across distributed infrastructure — hybrid/multi-cloud — требует unified telemetry и detection logic между on-premises systems и несколькими cloud providers.

Organizations используют mix agentless approaches — API access, snapshot-based analysis — и agent-based runtime monitoring там, где workloads это поддерживают. Cloud-aware network detection и control-plane analytics дают visibility cross-environment activity, которую traditional tools могут пропустить.

Native provider tools — **AWS GuardDuty, Azure Defender и Google Cloud Security Command Center** — дают built-in detections для своих platforms. Это обеспечивает native visibility cloud events, но cross-environment correlation обычно слабее, чем у third-party SIEM/EDR. Organizations с несколькими clouds следует рассмотреть detection solutions, объединяющие telemetry/analysis across environments.

## CHALLENGES IN DETECTION

Задача detection teams сложна: огромные volumes data, encrypted traffic, adversaries, активно уклоняющиеся от detection, и skills gaps внутри security teams затрудняют effective threat identification. Понимание этих challenges помогает выработать strategies обхода limitations и постепенного улучшения detection capability.

### Data Volume and Velocity

Современные environments генерируют такое количество и скорость security data, что analysis capacity может быть перегружена. Large networks легко создают terabytes logs daily с endpoints, network devices, cloud services и applications. Даже sophisticated tools/automation не гарантируют comprehensive analysis.

Data из multiple disparate sources требует prioritization/filtering. Даже SIEM и ML models могут генерировать alert volume выше capacity analysts, вызывая alert fatigue и missed detections. Retention costs заставляют выбирать, какие данные хранить long-term, а какие удалять быстрее.

Source предлагает **detection-driven collection**: каждый retained event должен поддерживать конкретный detection use case. Если data source не связан с use case, value retention ограничена. Default меняется с «collect everything and hope» на «define threats and collect required data».

Практические strategies:

- **Start from use cases:** сначала определить attack detection scenarios, затем required sources; не поддерживающие objective sources filter/discard.
- **Tiered data retention:** hot/warm/cold tiers — recent high-fidelity data доступна быстро, older data архивируется cost-effectively.
- **Filtering at the source:** удалять known-good noise до ingestion — routine successful service-account authentications, expected traffic patterns.
- **Intentional data disposal:** не деградировать quality aggregation/sampling при ingestion; хранить full-fidelity столько, сколько нужно для useful detection/investigation, затем deliberately purge.
- **Correlation-based alerting:** несколько low-confidence signals превращать в один high-confidence analyst-facing alert.
- **Constant tuning:** регулярно adjust detection rules, thresholds и sources по мере изменений environment/threats; сохранять test environments для validation изменений до production.

Цель — не «collect less», а collect useful data и эффективно processing, чтобы analysts занимались relevant signals.

### DETECTION-DRIVEN COLLECTION: AZURE STORAGE LOGGING

Azure Blob Storage diagnostic logging иллюстрирует principle. Moderately active storage account может генерировать миллионы `StorageBlobLogs` entries daily, большинство — routine read requests public content. Ingest всего массива в Log Analytics workspace создаёт storage cost и analyst burden без proportional detection value.

Organizations могут использовать **Data Collection Rules (DCR)** с ingest-time transformations, filtering storage logs до workspace. Сначала определить threats: unauthorized access attempts, data exfiltration, suspicious deletion. Затем DCR transformation с Kusto Query Language (KQL) проверяет каждый log entry по detection criteria.

### Listing 30. DCR Transformation for Storage Log Filtering

```
source
| where StatusCode >= 400 ①
    or OperationType in ("DeleteBlob", "PutBlob",
                         "PutBlock", "CopyBlob") ②
    or (CallerIpAddress !startswith "10."
        and CallerIpAddress !startswith "192.168.") ③
| project TimeGenerated, OperationType, StatusCode,
    CallerIpAddress, AccountName, ObjectKey, UserAgentHeader ④
```

① Сохранять failed requests — 4xx/5xx.  
② Сохранять write/delete operations независимо от status.  
③ Сохранять requests от IP вне expected internal ranges.  
④ Оставлять только нужные columns для дальнейшего уменьшения ingestion volume.

Такой approach существенно снижает log volume, сохраняя events, реально поддерживающие threat detection. Transformation выполняется at ingestion в DCR pipeline, поэтому filtered events не используют workspace storage/processing.

### Encrypted Traffic

Encryption уменьшает network-based visibility communications content. По мере роста TLS web traffic, encrypted DNS и VPN connections monitoring tools больше полагаются на metadata analysis вместо deep packet inspection. Encryption важна для privacy/security, но уменьшает visibility threat hunting и позволяет скрывать C2/data-exfiltration activity.

#### ENCRYPTED TRAFFIC DETECTION TECHNIQUES

Когда payload inspection ограничен, detection сосредоточен на metadata/behavioral analysis.

Flow-based analysis, включая **Encrypted Traffic Analysis (ETA)**, использует packet sizes, timing, directionality и TLS handshake attributes для anomaly detection без decryption. ML models могут классифицировать suspicious encrypted flows по этим characteristics.

Certificate/handshake inspection использует certificate attributes, Server Name Indication (SNI), TLS versions, cipher suites и handshake fingerprints. **Encrypted Client Hello (ECH)** — successor ESNI — уменьшает доступную information. Fingerprinting techniques вроде **JA4+** дают insight на основе TLS handshake parameters и помогают identify malicious clients даже при encryption.[5]

Source показывает extraction JA4 fingerprints из TLS Client Hello через TShark и lookup local JA4 JSON database. Fingerprint `t13i3110as_e8f1e7e78f70_1f22a2ca17c4` соответствует **AnyDesk v9.6.1**.

### Listing 31. TLS JA4 Fingerprint Analysis

```
$ tshark -r netedge-20260105.pcapng -Y "tls.handshake.type == 1" -T fields -e
tls.handshake.ja4 | sort -u
t13i3110as_e8f1e7e78f70_1f22a2ca17c4
$ jq '.[] | select(.ja4_fingerprint == "t13i3110as_e8f1e7e78f70_1f22a2ca17c4")'
~/ja4db.json
{
  "application": "AnyDesk",
  "library": null,
  "device": null,
  "os": null,
  "user_agent_string": "",
  "certificate_authority": null,
  "verified": false,
  "notes": "AnyDesk v9.6.1",
  "ja4_fingerprint": "t13i3110as_e8f1e7e78f70_1f22a2ca17c4",
  "ja4_fingerprint_string": "",
  "ja4s_fingerprint": "",
  "ja4h_fingerprint": null,
  "ja4x_fingerprint": null,
  "ja4t_fingerprint": null,
  "ja4ts_fingerprint": null,
  "ja4tscan_fingerprint": null
}
```

JA4 fingerprinting даёт context для encrypted traffic analysis и позволяет identify applications/clients, даже если payload inaccessible и дополнительные privacy controls скрывают client/server details.

Behavioral context analysis добавляет insight: unusual outbound volumes, connections к unusual destinations, новые encrypted channels от systems, которые обычно их не создают.

Organizations должны сосредоточить network detection на connection metadata: destination addresses, timing/duration, data volumes, certificate information, остающейся visible. TLS inspection internal systems, где policy permits, даёт valuable data для threat hunting/investigation. Metadata + behavioral approaches позволяют поддерживать meaningful coverage при росте encryption.

### Adversary Evasion

Sophisticated attackers активно работают над evasion и воспринимают security tools как obstacles, которые можно overcome. Понимание common techniques помогает analysts заметить попытки hiding activity.

Attackers target logging infrastructure: clear Windows Event Logs, disable audit policies, timestomp files для сокрытия timelines. Analysts должны monitor gaps в logs и unexpected logging configuration changes как potential IOC. Scope chapter рассматривает anti-forensic techniques подробнее.

Вместо custom malware attackers всё чаще используют legitimate tools: PowerShell, WMI, PsExec и другие built-ins. Это смешивается с normal administration и делает behavioral detection essential.

Attackers, знающие thresholds, могут работать just below them: exfiltration множеством малых transfers, authentication attempts с интервалами для bypass lockout, lateral movement в normal business hours.

### THE PRE-ATTACK LAB

Canonical source описывает practice disciplined attackers: laboratory environments, имитирующие enterprise security stacks, где malware/procedures test against EDR/SIEM/network monitoring.

В качестве example source ссылается на **2022 Conti ransomware leaks**.[6] Internal chats показывали budget several thousand dollars monthly на purchase security/AV tools для continuous testing и инвестицию **$60,000** для acquisition legitimate Cobalt Strike license через intermediary company.

`THIRD_PARTY_REVIEW_REQUIRED` — direct quotation Conti manager Reshaev из third-party leaked chat не переводится и не воспроизводится без separate rights review.

Смысл author text: detection capability должна continuously evolve. Rules, работавшие против прошлых incidents, могут fail против adapted attackers. Organizations должны исходить из того, что determined adversary со временем сможет bypass отдельный detection method, поэтому нужны layered strategies и continuous improvement.

Layered detection strategies и continuous improvement остаются необходимыми.

По мере адаптации attacker techniques detection teams не могут полагаться только на endpoint signatures или static rules. Threat intelligence по emerging evasion techniques, regular updates detection rules и purple-team exercises для проверки coverage помогают сохранять effective detection capabilities.

**Purple teaming** особенно полезен для уменьшения gap между detection capability и attacker tradecraft. В purple-team exercise red team демонстрирует specific attack techniques, а blue team наблюдает resulting telemetry и почти real-time создаёт или уточняет detections. Такой collaborative approach развивает detection-engineering skills, которые трудно получить только из alerts. Он также служит practical litmus test: если SOC не способен track internal red team, работающую с known machine внутри собственной network, обнаружить sophisticated external adversary будет значительно сложнее.

### Skills Gap

Skills gap в security operations означает, что многим organizations трудно эффективно использовать detection tools и интерпретировать alerts. Недостаток experienced analysts, способных tune detection systems, investigate alerts, perform threat hunting и develop new rules, ограничивает detection effectiveness по всей industry.

Entry-level analysts часто не хватает deep technical knowledge для distinction sophisticated attacks от benign anomalies, а experienced analysts находятся в high demand и трудно удерживаются. Organizations должны инвестировать в training programs, развивающие detection skills, использовать Managed Security Service Providers (MSSPs) для supplementation internal capabilities и внедрять knowledge-management systems для capture detection expertise.

Automation и AI-assisted detection могут частично закрывать skill gap, добавляя context/recommendations — см. Accelerating Incident Response with AI. Однако они требуют oversight experienced personnel, иначе возможны missed threats или excessive false positives.

## DETECT ACTIVITY EXAMPLES

Следующие examples показывают, где detection является важной частью incident response process.

### The External Breach Hunter

Yoshihiro, tier-1 SOC analyst on duty, во вторник утром открыл email с subject “Security Issue - Exposed Administrative Systems.” Message пришло через security disclosure address, опубликованный в organization security.txt, и попало прямо security team вместо general support queue.

Sender — Tom Liston — сообщил об exposed administrative portals и suspicious accounts в patient management system.

### Listing 32. Excerpt from Liston’s Disclosure Email

THIRD_PARTY_REVIEW_REQUIRED — canonical source воспроизводит прямое third-party correspondence от Tom Liston. Его verbatim text не переводится и не воспроизводится без отдельной проверки прав.

Авторский surrounding text фиксирует ключевые claims сообщения:

- admin interface https://admin.genusight.com/login публично reachable;
- researcher считает, что system использовала default/weak credentials и уже была exploited;
- suspicious accounts: admin_backup, created 2026-03-02, и svc_temp, created 2026-03-05;
- имена не соответствуют convention adm_firstname.lastname;
- оба accounts, по report, authenticated from Eastern Europe IP addresses в течение последних **45 days**;
- authentication logs приложены;
- sender указывает, что external notification сама по себе означает возможный gap internal detection.

Yoshihiro узнал имя sender: Tom Liston — longtime handler SANS Internet Storm Center, известный тем, что как hobby выявляет compromised systems. Однако узнаваемость sender не заменяет verification.

Yoshihiro отнёсся к report со healthy skepticism. Он видел false alarms от well-meaning researchers и social-engineering attempts, замаскированные под security notifications. Вместо reliance на single indicator он прошёл structured verification process до решения об escalation.

Сначала он подтвердил, что URLs ведут на actual organizational infrastructure, а не lookalike domains social engineer. Затем cross-referenced suspicious account names с standard adm_firstname.lastname convention и подтвердил, что admin_backup и svc_temp действительно существуют и нарушают policy-defined provisioning pattern.

После этого он review attached authentication logs, geolocated source IPs и подтвердил отсутствие business presence/remote workers organization в указанных regions. Наконец, Yoshihiro оценил quality report: specific technical details, reproducible evidence и clear disclosure timeline больше соответствовали legitimate researcher, чем attacker, пытающемуся social-engineer incident response.

Yoshihiro escalated report tier-2 SOC analysts с summary validated findings. Detection event переходит к **verify and triage**, где team будет отдельно проверять claims и определять appropriate response. Published disclosure channel, structured triage и multi-factor validation превратили message, которое могло застрять в help-desk queue, в actionable threat intelligence.

### The SIEM Wizard

Active threat hunting позволяет proactively находить threats, которые automated alerting может пропустить, особенно при поиске suspicious patterns вместо известных malicious indicators.

Mature detection teams ведут threat hunting как documented program, а не ad hoc effort: track hunt hypotheses, target data sources, cadence и last-run dates в table, поддерживающей coverage reviews и regulator inquiries. Prepare chapter описывает design/documentation такой program.

Lucía, threat hunter SOC team, выполняла recurring hunt beaconing behavior в outbound traffic — common indicator C2 communications, где compromised systems регулярно check in attacker infrastructure.

Beaconing suspicious потому, что legitimate applications редко общаются с external servers с идеально consistent intervals, тогда как malware часто использует regular callback schedule для commands/exfiltration.

Lucía открыла Kibana и создала Elasticsearch aggregation query, чтобы найти URLs с consistent access patterns за последние seven days. Query grouped proxy requests по destination URL и анализировал distribution over time, ища scheduled automated communication вместо human browsing.

### Listing 33. Elasticsearch Query for Beaconing Detection

~~~json
{
  "size": 0, ①
  "query": {
    "range": {
      "@timestamp": {
        "gte": "now-7d", ②
        "lte": "now"
      }
    }
  },
  "aggs": {
    "by_url": {
      "terms": {
        "field": "url.keyword", ③
        "size": 500
      },
      "aggs": {
        "over_time": {
          "auto_date_histogram": {
            "field": "@timestamp", ④
            "buckets": 50
          }
        },
        "request_count": {
          "value_count": { ⑤
            "field": "@timestamp"
          }
        }
      }
    }
  }
}
~~~

① Не возвращать individual documents, только aggregation results.  
② Искать только последние seven days proxy logs.  
③ Group requests по destination URL.  
④ Создать histogram времени requests для каждого URL.  
⑤ Count total requests для каждого URL.

Query вернул hundreds URLs с разными patterns. Lucía review time-distribution histograms. Большинство демонстрировало irregular human-access patterns: bursts during business hours, lunch gaps, quiet overnight. Другие имели consistent legitimate automated patterns — software update checkers и monitoring tools, знакомые по previous hunts.

Один URL выделился: api.cloudserv-cdn.com показал ровно **2,016 requests** за seven days и perfectly spaced intervals. Calculation дал ровно **five minutes между requests**. Такая precision была unusual и alarming.

Lucía углубила analysis: follow-up query определил client systems и timestamps. Все requests пришли с одной finance workstation; timestamps подтверждали pattern — :05, :10 и далее каждые five minutes без variation.

Threat intelligence добавила context: domain был зарегистрирован всего **three weeks ago** через registrar, часто abused threat actors, а hosting provider связывался с malicious infrastructure.

Lucía documented beaconing pattern, recently registered domain, five-minute interval и affected workstation и escalated detection event incident response team для verify and triage. Следующая phase должна определить, действительно ли workstation compromised, или у highly regular communication есть legitimate explanation.

## DETECT: STEP-BY-STEP

Следующие steps дают condensed reference detection activities. Они организованы для использования при establishing detection sources, hunting threats и refining detection capabilities.

Source указывает, что guide доступен для download в PDF/Markdown на dynamicincidentresponse.com.

### Step 1. Select and Combine Detection Methodologies

Representative activities:

- использовать signature-based detection для efficient high-confidence identification known threats;
- применять behavioral detection для threats, evading signatures: mass file encryption, unusual access patterns, living-off-the-land, insider misuse;
- scope behavioral baselines до business units/functional groups;
- layer ML-based detection для scoring/correlation at scale с HITL, сохраняя analyst judgment final classification;
- map detection logic к MITRE ATT&CK techniques вместо specific indicators, чтобы rules переживали changes attacker tools.

### Step 2. Operate Detection Data Sources

Representative activities:

- review EDR telemetry для process injection, credential dumping, persistence, suspicious parent-child chains;
- analyze network monitoring для C2 beaconing, lateral movement, anomalous volumes;
- query SIEM attack patterns across sources;
- применять SOAR automation к high-confidence alerts;
- monitor health log sources, подтверждая delivery critical feeds.

### Step 3. Adapt Detection to Cloud-Native Environments

Representative activities:

- query cloud-provider flow logs, control-plane events и Kubernetes audit logs;
- использовать eBPF monitoring и container runtime socket telemetry;
- service-mesh telemetry для east-west visibility;
- для serverless/microservices collect function telemetry и искать abnormal invocations, unexpected outbound connections, unusual secret/env access и deviations baseline execution;
- unify telemetry across on-premises, hybrid и multi-cloud для cross-environment correlation.

### Step 4. Implement Data Reduction and Prioritization Strategies

Representative activities:

- detection-driven collection: use cases first, sources second;
- filter high-volume low-value logs before SIEM ingestion;
- tiered hot/warm/cold retention;
- intentionally dispose data, которое больше не поддерживает detection/forensics, вместо degradation aggregation/sampling;
- correlate multiple low-confidence signals в high-confidence alerts;
- statistical analysis для anomalous patterns вроде periodic beaconing.

### Step 5. Conduct Active Threat Hunting

Threat hunting в detect — standing program, distinct от IOC-driven enterprise sweep, выполняемого scope после verified incident.

Representative activities:

- documented program с rotating hypotheses, tracked cadence, auditable last-run dates;
- prioritise TTPs/behavioral indicators over hashes/IP — Pyramid of Pain;
- search beaconing, lateral movement, data staging, living-off-the-land;
- standing IOC sweeps against current/recent telemetry по threat-intelligence feeds; incident-specific IOC sweeps относятся к scope после verification;
- analyze encrypted metadata: TLS client fingerprints, connection patterns, certificate attributes;
- deploy TLS inspection internal systems where policy permits;
- document findings и new IOC.

### Step 6. Monitor Passive Detection Sources

Representative activities:

- review automated security-tool alerts;
- monitor employee suspicious-activity reports;
- promptly/supportively acknowledge employee reports, даже false alarms;
- track observations sysadmins/help desk;
- validate third-party notifications по multiple factors: infrastructure legitimacy, IOC cross-reference, report quality — не только source reputation.

### Step 7. Respond to Detection Events

Representative activities:

- apply false-positive prefilter через local knowledge base до escalation, исключая alerts, matching documented benign sources;
- document EOI для handoff: alert source, timestamps, affected assets, indicators;
- escalate documented EOI в verify and triage; verification, CTI enrichment и decision continue/stop/defer принадлежат следующей phase;
- для external researcher reports acknowledge report и establish channel для ongoing updates.

### Step 8. Continuously Improve Detection Capabilities

Этот step фиксирует phase-specific feedback; broader organizational changes относятся к debrief Step 8.

Representative activities:

- track MTTD, alert volume, false-positive rate;
- purple-team exercises для adversary-evasion coverage;
- update rules по new threats/TTPs;
- address detection gaps, найденные incident response;
- monitor log tampering, disabled audit policies и data gaps;
- retrain/recalibrate ML models для model drift, validate training data quality и avoid mislabeled contamination;
- сохранять test environments для validation detection logic;
- capture detection expertise в knowledge systems;
- review threat intelligence по attacker tooling/evasion;
- staffing/sourcing decisions — training investment, MSSP supplementation — передавать в debrief Step 8, а не решать внутри detect activity.

## Сноски и источники

[1] MITRE ATT&CK, attack.mitre.org/

[2] Rossouw, Faan, "Hunt What Hurts: The Pyramid of Pain," Active Countermeasures, November 2025, www.activecountermeasures.com/hunt-what-hurts-the-pyramid-of-pain/

[3] Bianco, David, "The Pyramid of Pain," 2013, detect-respond.blogspot.com/2013/03/the-pyramid-of-pain.html

[4] RITA (Real Intelligence Threat Analytics), github.com/activecm/rita

[5] FoxIO, "JA4+ Network Fingerprinting," github.com/FoxIO-LLC/ja4

[6] Krebs, Brian, "Conti Ransomware Group Diaries, Part III: Weaponry," Krebs on Security, March 2022, krebsonsecurity.com/2022/03/conti-ransomware-group-diaries-part-iii-weaponry/
