# Chapter 18 — Segment 02

Source RAG: `p0589:c01`–`p0593:c01`

На уровне организации все incident responders должны иметь глобальный read-only доступ. Это позволяет:

- читать журналы;
- просматривать пользователей, роли и policies;
- определять масштаб инцидента;
- исследовать подозрительные ресурсы.

У каждого cloud provider есть встроенные роли, подходящие для этой задачи:

- AWS — managed policy `SecurityAudit`;
- Azure — роль `Security Reader`;
- Google Cloud — роль `Security Reviewer`.

Эти роли обеспечивают достаточную visibility для расследования, но не позволяют изменять ресурсы.

Если forensics выполняется в облаке, следует выделить отдельный project, account или subscription, где можно разворачивать forensic VMs и другие инструменты, а investigators должны иметь достаточные права на управление ресурсами именно в этой forensic-среде. Отделение forensic infrastructure от production environments снижает риск загрязнения доказательств и мешает злоумышленнику вмешиваться в расследование. Заранее подготовленные forensic accounts с повышенными правами внутри forensic project, но только read-only правами в остальных средах, позволяют начать анализ немедленно, без ожидания согласования доступа.

Процедуры реагирования могут требовать глобальных write actions, например:

- изменить network resources для изоляции скомпрометированных hosts;
- отозвать credentials;
- создать snapshots volumes.

Постоянный write access по всей среде противоречит least-privilege, но запрос доступа во время активного инцидента отнимает время. Таблица 55 показывает варианты, позволяющие сбалансировать безопасность и скорость реагирования.

## Таблица 55. Подходы к предоставлению write access для IR

| Подход | Описание |
|---|---|
| Automated service accounts | Service account с ограниченным набором write permissions выполняет containment и isolation actions от имени responders через заранее подготовленную automation. Это позволяет не выдавать людям широкие права напрямую. |
| Just-in-time elevation | Responders активируют заранее одобренные elevated roles по запросу, с автоматическим истечением срока действия. Такой подход поддерживают Azure Privileged Identity Management (PIM), AWS IAM Identity Center с temporary permission sets и Google Cloud IAM Conditions с time-based access. |
| Break-glass accounts | Emergency credentials хранятся в защищенном виде, например в hardware safe или secrets vault с audit logging, и дают доступ, когда остальные механизмы недоступны. Использование break-glass account должно вызывать alert и обязательный post-incident review. |

У каждого подхода свои компромиссы по operational complexity, audit coverage и скорости доступа. Организации должны выбрать и протестировать подход заранее, до того как активный инцидент вынудит решать этот вопрос в реальном времени.

# ОБНАРУЖЕНИЕ

Обнаружение в облачных средах опирается на другие инструменты и источники данных, чем традиционный on-premises monitoring. Общие рекомендации рассматриваются в Detect Activity. Здесь представлены cloud-native detection services крупных cloud providers как отправная точка для понимания встроенных возможностей.

# Cloud-Native Detection Tooling

Cloud providers разработали встроенные detection services, которые отслеживают среду на предмет угроз без необходимости использовать third-party tools. Эти сервисы анализируют:

- control-plane logs;
- network traffic;
- resource behavior.

Цель — выявлять suspicious activity, включая compromised credentials и cryptomining.

Source отмечает, что атакующие все чаще ориентируются не на традиционные инфраструктурные уязвимости, а на сам cloud fabric, используя misconfiguration, слабости identity и over-permissioned access как основные точки входа.

THIRD_PARTY_REVIEW_REQUIRED — quoted report text not reproduced verbatim.

Оптимальный вариант — SIEM с detection capabilities, который анализирует cloud data sources. Если SIEM нет, cloud providers предлагают native detection services.

## Detection Tooling for AWS

Amazon GuardDuty — managed threat detection service, который непрерывно отслеживает AWS accounts и workloads на предмет malicious activity и unauthorized behavior. Он использует:

- machine learning;
- anomaly detection;
- integrated threat intelligence.

GuardDuty выявляет потенциальные угрозы, включая:

- cryptomining;
- compromised credentials;
- связь с известными command-and-control servers.

### Рисунок 186. Детали finding в AWS GuardDuty: проверка threat detection

THIRD_PARTY_REVIEW_REQUIRED — внешний screenshot не воспроизводится.

В интерфейсе GuardDuty analysts могут просматривать findings по ресурсам среды. Детальный finding показывает identities, resources и indicators и служит отправной точкой для дальнейшего расследования.

GuardDuty также поддерживает agentless malware scanning для EC2 instances и container workloads через Malware Protection. Когда GuardDuty создает finding, указывающий на возможный malware, сервис может автоматически инициировать scan, создавая snapshots EBS volumes, подключенных к затронутому instance. Поскольку анализ выполняется по snapshots, а не по live volumes, running workloads не испытывают performance impact.

Responders также могут запускать on-demand scan вручную, указывая ARN EC2 instance. Это полезно для hosts, по которым automated finding еще не сработал. При обнаружении malware EBS snapshots сохраняются как forensic evidence для дальнейшего анализа. Сочетание автоматического detection и evidence preservation делает GuardDuty полезной первой ступенью AWS cloud incident response workflow.

## Detection Tooling for Azure

Azure detection capabilities можно добавить, включив Microsoft Defender for Cloud. Defender for Cloud отслеживает:

- resources в среде;
- Microsoft 365 logs;
- Azure audit logs.

### Рисунок 187. Детали alert в Azure Defender for Cloud: атака SQL Injection

THIRD_PARTY_REVIEW_REQUIRED — внешний screenshot не воспроизводится.

В примере показан alert SQL injection против Azure SQL database. Как и GuardDuty, alert предоставляет контекст по затронутым resources и indicators, необходимый для начала расследования.

С точки зрения incident response, интерфейс Defender for Cloud включает вкладку `Take action`, откуда responders могут:

- просмотреть activity logs ресурса;
- изучить manual remediation steps, относящиеся к конкретному alert type;
- запустить automated response через Azure Logic App.

Где применимо, alerts сопоставляются с MITRE ATT&CK kill chain stages, что помогает analysts понимать продвижение атакующего по среде. Для организаций, использующих Microsoft Sentinel или другой SIEM, alerts Defender for Cloud можно передавать напрямую в SIEM для централизованного расследования вместе с другими log sources.

## Detection Tooling for Google Cloud

Google Cloud предоставляет native threat detection через Security Command Center (SCC). SCC включает несколько detection services:

- Event Threat Detection анализирует Cloud Audit Logs и VPC Flow Logs на suspicious patterns: brute-force login attempts, cryptomining activity и outbound connections к известной malicious infrastructure;
- VM Threat Detection работает на hypervisor level и выявляет malware и kernel-level rootkits на Compute Engine instances без установки agent;
- Container Threat Detection отслеживает GKE container workloads и выявляет runtime attacks, включая reverse shells, suspicious binaries и unexpected script execution.

Каждый сервис формирует findings, которые responders могут:

- просматривать;
- аннотировать;
- приоритизировать по severity.

Findings содержат affected resource, detection source и recommended remediation steps. Интерфейс SCC аналогично GuardDuty и Defender for Cloud предоставляет консолидированный обзор findings с drill-down до отдельных alerts.

Для расследования findings можно:

- экспортировать в BigQuery для deeper analysis;
- публиковать в Pub/Sub для интеграции с external SIEM и ticketing systems;
- передавать в Google Security Operations, ранее Chronicle, для корреляции с другими log sources.

SCC также поддерживает automated playbooks for remediation, позволяя выполнять response actions при появлении определенных типов findings.

# Что пропускают Cloud-Native Detection Services

Cloud-native detection services полезны, но имеют ограничения.

Во-первых, они обычно ориентированы на known patterns. Novel techniques или living-off-the-land подходы, использующие legitimate cloud APIs необычным образом, могут не вызывать alerts. Атакующего, который использует только уже назначенные скомпрометированной identity разрешения, сложно отличить от normal operations.

Во-вторых, большинство cloud-native detection services фокусируются на control plane. Data plane activity часто остается без наблюдения, если дополнительные функции не включены. Например, скачивание sensitive files из storage bucket не вызовет detection, если data plane logging и соответствующие detection rules не настроены.

В-третьих, сервисы не знают организационного контекста. Они не понимают, что:

- конкретный service account работает только в business hours;
- определенный пользователь никогда раньше не обращался к конкретному ресурсу.

Без organization-specific baselines anomalous behavior, очевидное analyst, может не вызвать alert.

Cloud-native detection services следует рассматривать как foundation, а не как complete solution. SIEM, который умеет применять custom detection rules, cross-correlate events и учитывать organizational baselines, значительно расширяет detection coverage.

# SIDEBAR: КОГДА ПЕРВЫМ ALERT СТАНОВИТСЯ СЧЕТ ЗА ОБЛАКО

Один из повторяющихся detection patterns — неожиданный billing alert как первый indicator of compromise. Finance team замечает, что cloud bill вырос в три-четыре раза, а расследование выявляет сотни GPU-enabled instances, выполняющих cryptomining в регионах, которыми организация раньше не пользовалась.

Google Threat Horizons стабильно относит cryptomining к наиболее распространенным post-compromise действиям в облаке.[5] Причина проста: скомпрометированный cloud account дает мгновенный доступ к compute resources, которые можно монетизировать без lateral movement и data exfiltration.

Отсюда следует важный вывод для detection strategy: billing alerts и budget thresholds — полноценные detection mechanisms для облачных сред. Следует настраивать alerts на неожиданные всплески расходов, особенно в регионах, где организация обычно не работает. Billing anomaly может быть не самым сложным detection signal, но может сработать первым.

# ДЕЙСТВИЯ РЕАГИРОВАНИЯ

Cloud incident response включает те же core activities, что и другие типы инцидентов, но техники и инструменты заметно отличаются. Identity-based access models, distributed resources и cloud-specific persistence mechanisms требуют адаптированных процедур.

Здесь рассматриваются:

- определение масштаба cloud compromise;
- понимание cloud log sources;
- изоляция скомпрометированных resources;
- искоренение persistence;
- применение automation.

# Определение масштаба облачного инцидента

## Вопросы для определения масштаба

Один из важнейших этапов cloud incident response — определить масштаб compromise. Облачные среды часто требуют учета большего числа access controls и связей, чем традиционная локальная инфраструктура.

Начинать следует с определения compromised identity или identities. Это могут быть:

- users;
- access keys;
- service accounts;
- в AWS — даже role.

После идентификации compromised identities нужно определить назначенные им permissions, чтобы понять, к чему атакующий потенциально имел доступ.

Это не всегда сводится к просмотру списка прав конкретной identity.

В Azure permissions назначаются через role assignments, связывающие:

- identity;
- role;
- resource.

Figures 188–190 показывают назначения прав на уровне subscription и resource group и влияние этих уровней на scope compromise. Аналогичную информацию можно получить через Azure CLI: Listing 142 перечисляет role assignments пользователя по всей subscription.

Google Cloud использует сходную концепцию bindings, где IAM policy связывает member — user, service account или group — с role на определенном resource. Bindings применяются на разных уровнях resource hierarchy:

- organization;
- folder;
- project;
- individual resource.

Permissions наследуются вниз.

Responders могут использовать `gcloud projects get-iam-policy`, чтобы перечислить bindings project и определить effective permissions compromised identity.

В Azure и Google Cloud унаследованные permissions с более высоких уровней resource hierarchy могут расширять scope compromise за пределы того, что видно на уровне отдельного resource.
