---
book_id: dynamic-incident-response-joshua-wright-en-2026
chapter_number: 18
source_title: "Incident Response for Cloud Systems"
source_pdf_page_range: "584-612"
rag_chunk_range:
  first: "dynamic-incident-response-joshua-wright-en-2026:p0584:c01"
  last: "dynamic-incident-response-joshua-wright-en-2026:p0612:c01"
translation_status: "ACCEPTED"
license_notice: "Неофициальный русский перевод / unofficial Russian translation; original work CC BY 4.0. См. ../ATTRIBUTION.md."
third_party_review_policy: "Third-party figures, quoted report text, screenshots, and external materials remain fail-closed where marked."
translation_notes:
  - "Canonical English RAG is source of truth."
  - "Assembled from full-fidelity source-range segments."
  - "Commands, identifiers, metrics, and references are preserved where represented."
---

# Глава 18. Реагирование на инциденты в облачных системах

# ВВЕДЕНИЕ В ОБЛАЧНЫЕ СРЕДЫ

Облачные среды создают для реагирования на инциденты уникальные сложности, заметно отличающиеся от традиционных расследований в локальной инфраструктуре. Эта глава рассматривает cloud-specific considerations в рамках более широкой модели DAIR, представленной в Part 2: A Dynamic Approach to Incident Response. Организациям, реагирующим на инциденты в облаке, следует обращаться к соответствующим разделам Part 2 за полным описанием каждой активности реагирования, используя эту главу как дополнение с учетом особенностей облачной среды.

Сначала рассматриваются распространенные шаблоны атак на облако и их последствия, затем — вопросы подготовки, включая логирование и разрешения. После этого разбираются cloud-native средства обнаружения, а затем действия реагирования: определение масштаба компрометации, изоляция ресурсов и искоренение механизмов сохранения присутствия. В завершение рассматриваются облачные вопросы для разбора инцидента, использование самого облака для реагирования и особенности multi-cloud сред.

# Распространенные атаки на облачные среды

По мере переноса рабочих нагрузок в облако злоумышленники адаптировали свои техники. Тактики, применявшиеся в локальной инфраструктуре, не переносятся на облачные среды напрямую, поэтому потребовались новые подходы к первоначальному доступу, lateral movement и persistence.

В этом разделе рассматриваются наиболее распространенные шаблоны атак на облако: сначала векторы первоначального доступа, затем их последствия.

## Векторы первоначального доступа

Первый вопрос при анализе облачных атак — каким образом злоумышленники получают несанкционированный доступ. Согласно Google Threat Horizons Report за H1 и H2 2025 года, слабые или отсутствующие учетные данные, misconfiguration и компрометация API/UI обеспечили более 80% наблюдавшейся активности злоумышленников, связанной с первоначальным доступом.[1][2]

### Рисунок 185. Распределение векторов первоначального доступа к облаку

THIRD_PARTY_REVIEW_REQUIRED — диаграмма из внешнего источника не воспроизводится дословно.

### Слабые или отсутствующие учетные данные

Это стабильно один из наиболее часто атакуемых векторов первоначального доступа в облачных средах. В сочетании с отсутствием Multi-Factor Authentication (MFA) и слабым управлением разрешениями одна успешная атака социальной инженерии может дать злоумышленнику широкий доступ к среде и позволить реализовать поставленные цели.

### Ошибочные конфигурации

Многие организации перешли в облако, не располагая сопоставимой глубиной экспертизы по cloud security. Дефицит навыков, недостаточный change control и человеческие ошибки привели к многочисленным инцидентам, вызванным эксплуатацией cloud misconfiguration. Ошибка может раскрывать данные, которые должны быть ограничены, либо предоставлять избыточные привилегии, позволяющие lateral movement. Злоумышленники активно сканируют такие слабости и эксплуатируют их.

### Компрометация API/UI

Размещая cloud workloads в регионах по всему миру, организации получают лучшую доступность для конечных пользователей. Однако при отсутствии корректных access controls приложения могут быть открыты в интернет, формируя широкую поверхность атаки. В сочетании со слабыми учетными данными или уязвимым ПО это позволяет злоумышленнику закрепиться через открытые интерфейсы. После получения первоначального foothold разведка на хостах рабочих нагрузок может привести к lateral movement на другие хосты или, в худшем случае, к выходу в management plane.

# Последствия

После получения доступа к облачной среде проявляются несколько важных тенденций в целях атакующих. Mandiant M-Trends 2025 Report указывает, что кража данных наблюдалась почти в двух третях облачных компрометаций — 66%. Более трети случаев, 38%, были финансово мотивированы и включали extortion на основе кражи данных без ransomware encryption — 16%, Business Email Compromise (BEC) — 13%, ransomware — 9%, а также кражу криптовалюты и employment fraud.[3]

THIRD_PARTY_REVIEW_REQUIRED — quoted report text not reproduced verbatim.

Облачные среды содержат большие объемы ценных данных в storage services, базах данных и compute workloads. Orca Security 2025 State of Cloud Security Report приводит следующие результаты:

- 33% организаций с публично доступными storage buckets содержали в них sensitive data;
- 38% организаций с публично доступными базами данных имели в них sensitive data;
- 28% организаций с публично доступными cloud functions имели plaintext secrets в code packages и environment variables.[4]

В таких случаях атакующему нужны минимальные разрешения либо не нужны вовсе, чтобы получить доступ к чувствительным данным.

# SIDEBAR: ЧТО МОТИВИРУЕТ АТАКУЮЩИХ ОБЛАЧНЫЕ СРЕДЫ?

Злоумышленники, атакующие облачные среды, руководствуются теми же мотивами, что и при атаках на локальную инфраструктуру, однако облако дает новые возможности и более широкую поверхность атаки.

## Кража данных и вымогательство

Это остаются наиболее распространенными целями cloud-focused threat actors. Облачные среды хранят большие объемы sensitive data в storage services, базах данных и SaaS-платформах, нередко доступных через одну скомпрометированную identity. Получив доступ к привилегированной учетной записи, злоумышленник потенциально может получить доступ к данным всей организации, не взаимодействуя ни с одним endpoint. Это делает облако привлекательной целью для extortion campaigns, где украденные данные используются для давления на жертву, иногда вообще без развертывания ransomware.

## Ransomware

Cloud-based ransomware отличается от on-premises ransomware. Вместо шифрования локальных дисков злоумышленники могут удалять snapshots и backups, изменять storage lifecycle policies для уничтожения данных или блокировать доступ администраторов через манипуляции с IAM. Последствия могут быть столь же тяжелыми, особенно если у организации нет offline backups облачных данных.

## Cryptomining

Это распространенный результат компрометации учетных записей с правами на создание compute resources. Создание GPU-enabled virtual machines сразу в нескольких регионах может генерировать большие расходы для жертвы и одновременно приносить криптовалюту атакующему. Некоторые организации обнаруживают компрометацию только после получения неожиданно большого счета за облачные ресурсы.

Особую опасность облачных атак создает возможность эскалации от скомпрометированной workload к management plane. Виртуальная машина в облаке имеет доступ к metadata service, который может предоставлять учетные данные service accounts или roles. Если эти учетные данные обладают широкими правами, компрометация одного хоста может позволить атакующему перейти к контролю всей облачной среды.

# ПОДГОТОВКА

Подготовка к облачным инцидентам требует внимания к возможностям, отсутствующим в традиционных локальных средах. Shared responsibility model означает, что значительная часть visibility и доступа, необходимых для эффективного реагирования, должна быть настроена самой организацией. Общая подготовка к реагированию была рассмотрена в Prepare Activity; здесь внимание сосредоточено на двух cloud-specific областях с наибольшим влиянием на эффективность реагирования: logging и permissions.

# Логирование

Cloud logging возлагает существенную ответственность на заказчика: необходимо убедиться, что ожидаемые журналы включены и собираются. В облаке есть две категории журналов:

- management plane, или control plane logs;
- data plane logs.

Как общее правило, management plane logs включены по умолчанию, а data plane logs — выключены. Проверка корректной конфигурации логирования — один из важнейших шагов подготовки к cloud incident response. Немногие ошибки подготовки обходятся так дорого, как начало расследования с последующим обнаружением, что нужных журналов просто нет.

Если cloud logs не были включены, их нельзя восстановить задним числом. В отличие от локальных систем, где несобранные логи иногда сохраняются на диске, никогда не включенные облачные журналы не существуют.

При выборе журналов необходимо учитывать баланс стоимости и ценности. В идеале следовало бы включить все возможные источники, но большинство организаций не может игнорировать их стоимость. Среди важных data plane logs:

- network flow logs;
- storage access logs;
- operating system logs.

Из-за объема данных следует определить критические системы и ресурсы и включить расширенное логирование там, где оно будет наиболее полезно при расследовании. Например, access logging для bucket с общедоступными статическими файлами сайта может быть неоправданным, тогда как для чувствительного bucket с конфиденциальными записями стоимость audit trail оправданна.

Следует приоритизировать data-plane logging на системах, которые хранят sensitive data или наиболее вероятно станут целью. Стоимость логирования значительно ниже стоимости расследования без достаточной visibility.

Дополнительные параметры — lag time и retention time.

Lag time критичен, когда злоумышленник активен в среде прямо во время расследования. Если записи в конкретном источнике появляются с задержкой 24 часа, responders не могут уверенно исключить соответствующую активность, пока не пройдет полный lag period.

Retention time определяет способность расследовать инциденты с длительным dwell time. Например, Azure Entra ID audit и sign-in logs сохраняются только 30 дней при premium license и 7 дней на free tier. Listing 141 показывает, как проверить retention period для Entra ID logs. Если extended storage не был настроен, при расследовании события, произошедшего даже за семь дней до обнаружения, часть доказательств уже может отсутствовать.

## Листинг 141. Проверка срока хранения журналов Entra ID через Azure CLI

```text
$ az rest --method get --url
"https://management.azure.com/providers/Microsoft.aadiam/diagnosticSettings?api-version=2017-04-01"

{
  "value": [
    {
      "id": "/providers/Microsoft.aadiam/diagnosticSettings/EntraID-to-LogAnalytics",
      "name": "EntraID-to-LogAnalytics",
      "properties": {
        "logs": [
          {
            "category": "SignInLogs",
            "enabled": true,
            "retentionPolicy": { "days": 0, "enabled": false }
          },
          {
            "category": "AuditLogs",
            "enabled": true,
            "retentionPolicy": { "days": 0, "enabled": false }
          }
        ],
        "workspaceId": "/subscriptions/a1b2c3d4-…/resourceGroups/rg-security/providers/Microsoft.OperationalInsights/workspaces/secops-workspace"
      }
    }
  ]
}

$ az monitor log-analytics workspace show --resource-group rg-security --workspace-name secops-workspace --query "retentionInDays"

30
```

1. Первый запрос получает Entra ID diagnostic settings через Azure REST API.
2. Значение `retentionPolicy.days: 0` означает, что logs не сохраняются сверх default retention period.
3. `workspaceId` указывает Log Analytics workspace и resource group.
4. Последняя команда показывает фактический retention period workspace.

Оптимальный вариант — заранее настроить SIEM или другую централизованную logging platform, например Log Analytics workspace или storage account, которая получает cloud platform logs и хранит их с увеличенным retention period с учетом угроз с длительным dwell time. Централизация упрощает расследование, уменьшая необходимость переключаться между несколькими приложениями и источниками логов.

# Разрешения

Еще одна важная область подготовки для облачных сред — permissions. Во время активного инцидента responders не должны тратить критически важное время на запросы доступа, необходимого для расследования. Координация с другими командами для назначения прав замедляет расследование и может дать злоумышленнику дополнительное время для действий. Необходимые для расследования и реагирования привилегии должны быть определены и подготовлены заранее.

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

### Рисунок 188. Идентификация Azure Subscription и Resource Group

THIRD_PARTY_REVIEW_REQUIRED — внешний screenshot не воспроизводится.

### Рисунок 189. Azure Subscription показывает доступ Owner и Contributor

THIRD_PARTY_REVIEW_REQUIRED — внешний screenshot не воспроизводится.

### Рисунок 190. Azure Resource Group показывает дополнительный Contributor access

THIRD_PARTY_REVIEW_REQUIRED — внешний screenshot не воспроизводится.

## Листинг 142. Список Azure CLI Role Assignment для пользователя

```json
$ az role assignment list --all --assignee hydra@pymtechlabs.com --output json
[
  {
    "principalId": "ddaca639-d9c8-4d65-9f30-c0dcc58f9574",
    "principalName": "Hydra@pymtechlabs.com",
    "principalType": "User",
    "roleDefinitionName": "Contributor",
    "scope": "/subscriptions/a1b2c3d4-…/resourceGroups/rg-prod-eastus"
  },
  {
    "principalId": "ddaca639-d9c8-4d65-9f30-c0dcc58f9574",
    "principalName": "Hydra@pymtechlabs.com",
    "principalType": "User",
    "roleDefinitionName": "Owner",
    "scope": "/subscriptions/a1b2c3d4-…"
  }
]
```

1. Флаг `--all` возвращает role assignments по всем scopes, а не только для текущего subscription default.
2. `Contributor` на уровне resource group соответствует portal view из Figure 190.
3. `Owner` на уровне subscription означает, что compromised identity имеет широкий доступ ко всем resources в subscription.

Direct role assignments — не единственный механизм, определяющий реальный scope компрометации identity.

Например, в AWS compromised identity может выглядеть так, будто умеет управлять users, но конечное действие может быть запрещено:

- permission boundary;
- Service Control Policy (SCP);
- session policy;
- resource-based policy.

Для точного scoping важно понимать полный policy evaluation chain.

В AWS evaluation logic работает по определенному порядку. Explicit deny в любой применимой policy имеет приоритет. Далее учитываются:

- organization SCP;
- resource-based policies;
- identity-based policies;
- IAM permission boundaries;
- session policies.

На каждом уровне explicit deny отменяет allow. Поэтому identity с `AdministratorAccess` может все равно не иметь возможности выполнить определенное действие, если его блокирует SCP или permission boundary. Когда apparent permissions не совпадают с наблюдаемым поведением, responders должны учитывать полный IAM evaluation chain.

После compromised identities нужно определить affected resources. Это помогает установить действия атакующего и понять, вносились ли unauthorized changes.

Для:

- storage accounts;
- buckets;
- других data stores

необходимо выяснить, были ли раскрыты данные.

Некоторые ресурсы также могут облегчать lateral movement. Cloud virtual machines часто имеют Instance Metadata Service, через который можно получить access tokens для service accounts или roles, а затем использовать их для privilege escalation.

Наконец, следует проверить cloud network architecture и возможные пути lateral movement. Если compromised cloud environment напрямую связан:

- с другими cloud organizations у того же provider;
- с on-premises environment;
- с другим cloud provider;

нужно собрать и проанализировать дополнительные logs, чтобы проверить, не распространилась ли компрометация на связанные среды.

# SIDEBAR: CIRCLECI — КОГДА УКРАДЕННЫЙ SESSION TOKEN КОМПРОМЕТИРУЕТ SUPPLY CHAIN

В январе 2023 года CircleCI, платформа continuous integration, сообщила, что злоумышленник скомпрометировал laptop инженера malware и украл действующий SSO session token.[6]

Поскольку token уже прошел MFA, атакующий полностью обошел multi-factor controls и использовал session для доступа к внутренним системам CircleCI.

Используя один session token, злоумышленник:

- получил доступ к production environment;
- exfiltrated customer secrets;
- получил environment variables;
- получил API tokens;
- получил encryption keys, хранившиеся на платформе.

Масштаб был значительным: CircleCI рекомендовала всем клиентам ротировать каждый secret, хранившийся в их средах. Это затронуло тысячи организаций, использовавших платформу для CI/CD pipelines. Украденные credentials потенциально давали доступ к downstream integrations клиентов, включая cloud platforms, code repositories и SaaS applications.

Практическая ценность этого кейса для cloud responders — в attack chain:

- украденный session token дал доступ без срабатывания credential-based detections;
- blast radius распространился на downstream customers, чьи secrets находились на платформе;
- расследование требовало анализа session logs, internal access patterns и data-plane activity, а не только host-based forensics.

Два основных вывода:

1. MFA сама по себе не предотвращает token-based access; session token theft нужно учитывать при scoping.
2. Если cloud platform скомпрометирована, incident может распространяться на каждого customer и integration, которые доверили платформе credentials.

# Источники журналов

В ходе подготовки уже была отмечена важность включения и централизации logs до инцидента. Здесь рассматриваются control-plane и data-plane logs, содержащиеся в них данные и их значение для IR.

Management/control plane logs фиксируют:

- Identity and Access Management (IAM) events;
- administrative events;
- resource management events.

Как отмечалось ранее, они обычно включены по умолчанию.

IAM events — одна из наиболее ценных категорий при расследовании. Для initial access они помогают установить:

- кто вошел;
- когда;
- откуда;
- каким способом.

Контекст вроде success/failure status и login method позволяет точнее реконструировать intrusion.

Listing 143 показывает Azure sign-in log, где пользователь успешно прошел password authentication, но обе MFA attempts завершились неуспешно. Это может означать, что password уже украден, но MFA пока предотвращает compromise.

## Листинг 143. Детали аутентификации Azure Sign-In Log

```json
[
  {
    "authenticationStepDateTime": "2025-05-25T01:54:30.9375542+00:00",
    "authenticationMethod": "Password",
    "authenticationMethodDetail": "Password in the cloud",
    "succeeded": true,
    "authenticationStepResultDetail": "Authentication in progress"
  },
  {
    "authenticationStepDateTime": "2025-05-25T01:54:30.9375542+00:00",
    "authenticationMethod": "Mobile app notification",
    "succeeded": false,
    "authenticationStepResultDetail": "MFA denied; user did not select the correct number"
  },
  {
    "authenticationStepDateTime": "2025-05-25T01:54:30.9375542+00:00",
    "authenticationMethod": "Text message",
    "succeeded": false,
    "authenticationStepResultDetail": "MFA denied; invalid verification code"
  }
]
```

После получения доступа IAM logs помогают выявлять persistence и privilege escalation, например:

- создание новых users;
- назначение дополнительных roles compromised accounts.

В зависимости от TTP могут встречаться organization-level management events, например изменения logging configuration или domain settings.

Resource management events включают:

- создание resources;
- удаление resources;
- запуск resources;
- остановку resources.

Они дают важную информацию о намерениях атакующего. Попытки destructive actions через удаление критических resources будут видны в этих logs, как и создание GPU-enabled virtual machines, что может указывать на cryptomining.

Listing 144 показывает CloudTrail event `RunInstances`, запускающий GPU instance типа `p3.2xlarge`. При анализе особенно важны:

- instance type;
- region — атакующие часто используют регионы, в которых организация обычно не работает;
- identity, инициировавшая request.

## Листинг 144. CloudTrail Event: создание GPU Instance

```json
{
  "eventTime": "2025-08-14T03:22:17Z",
  "eventSource": "ec2.amazonaws.com",
  "eventName": "RunInstances",
  "awsRegion": "ap-southeast-1",
  "sourceIPAddress": "198.51.100.47",
  "userIdentity": {
    "type": "AssumedRole",
    "arn": "arn:aws:sts::471903287148:assumed-role/LambdaExecRole/i-0e83f91a7c42d1b05"
  },
  "requestParameters": {
    "instanceType": "p3.2xlarge",
    "instancesSet": { "items": [{ "imageId": "ami-0c7ea5497c02abcf5" }] },
    "minCount": 4,
    "maxCount": 4
  }
}
```

Data plane logs, также называемые resource logs, содержат resource-level operations.

Data plane logs по умолчанию отключены, но без них responders часто не видят полную картину инцидента.

## Таблица 56. Control Plane и Data Plane Logging

| Resource | Control plane — по умолчанию включен | Data plane — по умолчанию выключен |
|---|---|---|
| Storage — S3/Blob/GCS | Создание и удаление bucket, изменения policy | Чтение, запись и удаление отдельных objects |
| Virtual machines | Создание и termination instance, изменения security group | OS-level logs, network flow logs, process execution |
| Databases | Provisioning instance, configuration changes, backup operations | Отдельные queries, data access, row-level operations |
| IAM | Создание users, role assignments, изменения policies | Authentication attempts, token issuance, session activity |

Рассмотрим incident, где атакующий получает доступ к sensitive files в S3 bucket. Control plane logs CloudTrail покажут изменение bucket policy, но только S3 server access logs или CloudTrail data events покажут, какие именно objects были скачаны.

Аналогично, если initial access получен через compromise публичной virtual machine, только OS logs на endpoint или network flow logs в VPC покажут evidence первоначального вектора доступа.

Без data plane logs responders могут подтвердить compromise resource, но не всегда понять, что именно атакующий сделал с ним. Этот gap напрямую влияет на способность оценить data exposure и выполнить breach notification requirements.

Если доступен только факт изменения policy, но нет данных о том, какие objects были затем скачаны, организация может быть вынуждена исходить из worst-case exposure и уведомлять всех потенциально затронутых parties.

Control-plane и data-plane logs вместе позволяют проследить путь атакующего через cloud environment. Понимание доступных log sources и их содержимого необходимо для построения полной timeline attacker activity.

# Изоляция скомпрометированных ресурсов

Когда resources открыты наружу или скомпрометированы, нужно быстро устранить условия, позволяющие атакующему продолжать операцию или позволяющие новому threat actor войти в среду.

Подход зависит от сервиса. Здесь рассматриваются два часто атакуемых public-facing resource:

- virtual machines;
- storage accounts/buckets.

## Изоляция Virtual Machine

После compromise VM может показаться, что единственный вариант — выключить host. Более полезный подход позволяет сохранить host для deeper analysis и наблюдения за intent злоумышленника.

С помощью virtual network controls VM можно изолировать так, чтобы:

- заблокировать inbound traffic;
- заблокировать outbound traffic;
- оставить доступ только designated forensic networks.

В сочетании с flow logs на isolated subnet или compromised host это позволяет наблюдать, что пытается делать active threat actor или malware.

Listing 145 показывает создание Azure Network Security Group (NSG), которая запрещает весь трафик, кроме designated forensics subnet. VM остается включенной для наблюдения, но доступ злоумышленника отсекается.

## Листинг 145. Изоляция скомпрометированной VM через Azure NSG

```text
$ az network nsg create --resource-group rg-prod-eastus --name nsg-isolation

$ az network nsg rule create --resource-group rg-prod-eastus --nsg-name nsg-isolation --name AllowForensicsSubnet --priority 100 --direction Inbound --access Allow --source-address-prefixes 192.168.200.0/24 --destination-port-ranges '*' --protocol '*'

$ az network nsg rule create --resource-group rg-prod-eastus --nsg-name nsg-isolation --name DenyAllInbound --priority 4096 --direction Inbound --access Deny --source-address-prefixes '*' --destination-port-ranges '*' --protocol '*'

$ az network nsg rule create --resource-group rg-prod-eastus --nsg-name nsg-isolation --name DenyAllOutbound --priority 4096 --direction Outbound --access Deny --source-address-prefixes '*' --destination-port-ranges '*' --protocol '*'

$ az network nic update --resource-group rg-prod-eastus --name compromised-vm-nic --network-security-group nsg-isolation
```

1. Создается dedicated isolation NSG в той же resource group, где находится compromised VM.
2. Inbound разрешается только с forensics subnet `192.168.200.0/24` с более высоким priority.
3. Весь остальной inbound traffic запрещается.
4. Весь outbound traffic запрещается, чтобы compromised VM не могла взаимодействовать наружу.
5. Isolation NSG применяется к network interface compromised VM.

# Remediation Storage Account и Bucket

Data exfiltration — одно из основных последствий cloud compromise, а часть наиболее ценных данных хранится в storage accounts и buckets. Даже простая misconfiguration storage resource с sensitive data может привести к exposure, а threat actors постоянно используют automated scanners для поиска таких buckets.

Google Threat Horizons Report H1 2025 отмечает, что weak или absent authentication обеспечивали почти половину initial access, а во многих средах использовались overprivileged service accounts с high-privilege default credentials.[7]

THIRD_PARTY_REVIEW_REQUIRED — quoted report text not reproduced verbatim.

Если bucket скомпрометирован, misconfiguration нужно устранить как можно быстрее, чтобы прекратить дальнейший data exposure.

## AWS

Для S3 buckets используются:

- Block Public Access;
- IAM policies;
- resource-based policies;
- в legacy configurations — ACLs.

Block Public Access перекрывает настройки policies и ACLs, поэтому обычно является наиболее эффективным первым шагом для прекращения публичного exposure.

ACLs важно проверить во время расследования, поскольку атакующие могут ими злоупотреблять, но их не следует применять для новых access-control configurations.

## Листинг 146. Ограничение Public Access к Cloud Storage

```text
$ aws s3api put-public-access-block --bucket <bucket-name> --public-access-block-configuration BlockPublicAcls=true,IgnorePublicAcls=true,BlockPublicPolicy=true,RestrictPublicBuckets=true

$ aws s3api get-public-access-block --bucket <bucket-name>

$ az storage account update --name <account-name> --resource-group <rg-name> --allow-blob-public-access false

$ gcloud storage buckets update gs://<bucket-name> --public-access-prevention=enforced
$ gsutil iam ch -d allUsers gs://<bucket-name>
$ gsutil iam ch -d allAuthenticatedUsers gs://<bucket-name>
```

1. AWS: Block Public Access перекрывает policies или ACLs, разрешающие public access.
2. AWS: второй вызов проверяет текущую настройку public access.
3. Azure: отключается anonymous access для storage account.
4. Google Cloud: включается public access prevention и удаляются bindings `allUsers` и `allAuthenticatedUsers`.

Для оценки exposure в AWS следует анализировать S3 server access logs или CloudTrail data events, чтобы определить, какие objects были доступны и кем. Инструмент `s3logparse` может упростить анализ S3 server access logs.

## Azure

Anonymous read access для Azure storage resource может быть настроен:

- на container level;
- на blob level.

Container-level settings имеют приоритет над blob-level settings. Пользователь с permissions на `AllowBlobAnonymousAccess` должен отключить anonymous access для containers, которые не должны быть публичными.

## Google Cloud

Permissions на Google Cloud buckets контролируются через:

- IAM policies;
- ACLs.

Для remediation exposed bucket следует использовать IAM policies, выдавая только необходимые права только нужным users.

Как и в AWS, ACLs — legacy mechanism. Их нужно проверять во время compromise investigation, но не использовать как основной механизм remediation.

Если одновременно действуют IAM permissions и ACLs, достаточно allow в одном из механизмов, чтобы доступ был разрешен. Поэтому проверки только IAM недостаточно.

Время критично. Automated scanners постоянно ищут misconfigured buckets, и public exposure может быть обнаружен и использован в течение нескольких часов после ошибочной настройки.

После исправления access controls responders должны проверить remediation, попытавшись обратиться к resource из unauthenticated context и подтвердив, что public access больше невозможен.

При exposed storage сначала следует ограничить доступ, а уже затем проводить полное исследование того, что было прочитано. Чем больше задержка между discovery и remediation, тем больше потенциальный объем exposure.

# Искоренение Cloud Persistence

Cloud environments дают злоумышленнику множество способов закрепиться в зависимости от полученного уровня доступа. Полный каталог persistence techniques выходит за рамки главы; здесь рассматриваются ключевые области для eradication.

# Identity and Access Management

IAM — одна из важнейших служб облачной среды и одновременно одно из наиболее удобных мест для persistence при наличии соответствующих permissions.

Помимо IAM logs, responders должны напрямую проверить IAM resources на недавно созданные или измененные объекты:

- service accounts, созданные атакующим;
- access keys для существующих или новых accounts;
- role assignments или policy changes, выдающие elevated privileges;
- OAuth application consent grants, позволяющие API access без user credentials;
- изменения MFA configuration, включая отключение MFA или регистрацию attacker-controlled devices.

## Листинг 147. Выявление IAM Persistence Mechanisms

```text
$ aws iam list-users --query 'Users[*].UserName' --output text | xargs -I{} aws iam list-access-keys --user-name {}

$ az ad app list --query "[].{Name:displayName,AppId:appId,Created:createdDateTime}" -o table

$ gcloud iam service-accounts list --format="table(email)" | xargs -I{} gcloud iam service-accounts keys list --iam-account={} --managed-by=user
```

1. AWS: перечислить IAM users и их access keys с creation dates.
2. Azure: перечислить OAuth applications и creation timestamps для поиска недавно зарегистрированных apps.
3. Google Cloud: перечислить user-managed service account keys для поиска keys, созданных злоумышленником.

Простого credential rotation недостаточно, если active sessions остаются валидными. Cloud provider tokens обычно действуют до expiration даже после rotation underlying credential.

Responders должны одновременно выполнять rotation credentials и revoke active sessions:

- AWS — применить inline policy, запрещающую действия до определенного времени;
- Azure — revoke user sessions через Entra ID;
- Google Cloud — invalidate OAuth tokens затронутых service accounts.

IAM persistence mechanisms следует проверять при любом cloud compromise: это наиболее распространенные способы восстановить доступ после первоначального реагирования.

Mandiant M-Trends 2025 называет identity-based persistence ведущим способом сохранения доступа в cloud environments.[8] Поэтому IAM review должен быть первым приоритетом eradication до работы с compute или network persistence.

# Compute и Workloads

Для compute services следует учитывать:

- virtual machines;
- containers;
- serverless functions.

Каждый из этих типов workloads может быть backdoored.

Для virtual machines распространены:

- backdoored machine images, используемые для новых instances;
- malware на running hosts;
- malicious user data или startup scripts, выполняемые при boot.

Startup scripts особенно важны, потому что запускаются при каждой загрузке и могут переживать reboot и redeployment из того же image.

Нужно проверять не только running instances, но также machine images и launch templates, из которых они создаются. Compromised image повторно внесет backdoor при каждом новом deployment.

Для containers атакующий может отравить container registry, чтобы новые instances уже содержали backdoor. Responders должны сравнивать running container images с known-good digests и проверять недавно pushed images на unauthorized modifications.

Serverless functions — часто упускаемый persistence vector. При достаточных permissions атакующий может создать Lambda function, Azure Function или Cloud Function, которая по расписанию или trigger:

- создает новые access keys;
- exfiltrates data.

Поскольку serverless functions не имеют persistent host, traditional endpoint monitoring их не обнаруживает.

Responders должны перечислить functions во всех регионах и проверить:

- triggers;
- code;
- execution history.

Listing 148 показывает пример enumeration Lambda functions по регионам.

## Листинг 148. Перечисление Lambda Functions во всех регионах

```text
$ for region in $(aws ec2 describe-regions --query 'Regions[*].RegionName' --output text); do
  echo "=== $region ===" && aws lambda list-functions --region $region --query 'Functions[*].{Name:FunctionName,Modified:LastModified,Runtime:Runtime}' --output table
done

=== ap-south-1 ===
=== eu-north-1 ===
=== eu-west-3 ===
=== eu-west-2 ===
=== eu-west-1 ===
=== ap-northeast-3 ===
=== ap-northeast-2 ===
=== ap-northeast-1 ===
=== ca-central-1 ===
=== sa-east-1 ===
=== ap-southeast-1 ===
=== ap-southeast-2 ===
=== eu-central-1 ===
=== us-east-1 ===
-------------------------------------------------------------------------
|                              ListFunctions                            |
+-------------------------------+-------------------------+-------------+
|           Modified            |         Name            |   Runtime   |
+-------------------------------+-------------------------+-------------+
|  2022-05-26T17:00:49.000+0000 |  secheaders-cloudfront  |  nodejs14.x |
|  2025-11-05T12:00:13.000+0000 |  erk-requireauth        |  nodejs22.x |
|  2016-02-12T02:09:49.179+0000 |  blackFriday            |  python2.7  |
|  2022-03-01T21:59:46.000+0000 |  testKMSAccess          |  nodejs14.x |
+-------------------------------+-------------------------+-------------+
=== us-east-2 ===
=== us-west-1 ===
=== us-west-2 ===
```

Проблема многих cloud persistence techniques в том, что они либо не отражаются в logs, либо log entries не содержат достаточного контекста.

Для virtual machines:

- control-plane logs показывают instance creation;
- фиксируют изменения startup scripts;
- но не сохраняют содержимое самих scripts.

Для serverless functions:

- control plane фиксирует creation и updates;
- function code и execution output требуют отдельных log sources, например CloudWatch Logs для Lambda.

Поэтому investigation часто требует host forensics либо manual review ресурсов в cloud console.

# Networking

Network resources — критически важные security controls. Небольшое изменение может открыть доступ как исходному threat actor, так и новым атакующим.

Примеры:

- изменение Network Security Group;
- изменение ACL;
- создание persistent VPN tunnel;
- изменение DNS settings для перенаправления traffic.

Это распространенные persistence techniques, но не полный список. Во время eradication responders должны проверять network configuration и, где возможно, сравнивать текущее состояние с known-good baselines.

Общая особенность cloud persistence: зачастую достаточно API-level access, а host-level compromise не требуется. Поэтому закрепление может выполняться быстрее и быть менее заметным для traditional endpoint monitoring.

# SIDEBAR: РАСПРОСТРАНЕННЫЕ ОШИБКИ CLOUD IR

Несколько ошибок регулярно повторяются при cloud incident response.

## 1. Выключение compromised instance до его фиксации

После termination instance volatile data теряются безвозвратно:

- memory;
- running processes;
- network connections.

Перед containment action следует сначала сохранить snapshot.

## 2. Rotation credentials без revoke active sessions

Новый password или access key не делает существующие tokens недействительными. Если у атакующего есть valid session token, он может продолжать работу после rotation credentials.

Нужно явно revoke sessions дополнительно к credential rotation.

## 3. Предположение, что control plane logs показывают всю картину

Investigation только по CloudTrail или Activity Log может пропустить:

- lateral movement;
- data access;
- события, видимые лишь в data plane logs;
- VPC flow logs;
- host-level telemetry.

Control plane logs показывают, что было сконфигурировано, но не обязательно что произошло после изменения configuration.

## 4. Проверка только одного региона

Cloud providers работают в десятках regions. Атакующие нередко создают persistence resources в регионах, которыми организация обычно не пользуется.

Access key из `us-east-1` может использоваться для создания Lambda function в `ap-southeast-1`, которую команда не проверяет.

Во время eradication нужно перечислять resources во всех regions.

Все эти ошибки возникают из-за переноса on-premises assumptions в облачную среду. Cloud-specific checklists в response runbooks и регулярные tabletop exercises снижают риск таких ошибок под давлением реального инцидента.

# Automated Response Capabilities

Одно из преимуществ облака — native tooling для automated incident response.

Реализация зависит от provider и response process, но общий принцип одинаков. Пример для AWS:[9]

Trigger: GuardDuty alert указывает на возможную compromise EC2 instance. Lambda function выполняет:

1. перемещает EC2 instance в private subnet без internet access;
2. включает flow logs на subnet, VPC или network interface;
3. создает snapshot EC2 instance и сохраняет его в S3 bucket.

Те же AWS CLI команды из Listing 149 можно выполнять вручную, если automation еще не внедрена.

## Листинг 149. Automated EC2 Isolation and Snapshot

```text
$ aws ec2 modify-instance-attribute --instance-id i-0a1b2c3d4e5f67890 --groups <isolation-security-group-id>

$ aws ec2 create-flow-logs --resource-type NetworkInterface --resource-ids eni-0a1b2c3d4e5f67890 --traffic-type ALL --log-destination-type s3 --log-destination arn:aws:s3:::forensics-flow-logs

$ aws ec2 create-snapshot --volume-id vol-0a1b2c3d4e5f67890 --description "Forensic snapshot - GuardDuty finding 2025-08-14" --tag-specifications 'ResourceType=snapshot,Tags=[{Key=Case,Value=IR-2025-042}]'
```

1. Security groups instance заменяются isolation group, запрещающей inbound и outbound traffic.
2. На network interface включаются flow logs для capture попыток коммуникации.
3. Создается tagged snapshot EBS volume для forensic analysis.

При такой automation responders могут быть уверены, что host изолирован последовательно и без ручных изменений, а snapshot готов к host-level forensics.

Это лишь базовый пример. Большинство manual steps активного response можно превратить в scripts и actions, которые:

- автоматически запускаются alert;
- либо инициируются responder вручную.

Даже без fully automated pipeline полезно обернуть CLI-команды в простые scripts. Скрипт, который последовательно изолирует instance, включает flow logs и создает snapshot, уменьшает риск пропущенных шагов и опечаток.

# РАЗБОР ИНЦИДЕНТА

Cloud incidents часто выявляют gaps в:

- configuration;
- visibility;
- access management.

Debrief — возможность превратить эти gaps в конкретные улучшения cloud security posture. Общие правила, включая After-Action Review (AAR), documentation requirements и implementation tracking, описаны в Debrief Activity. Здесь рассматриваются cloud-specific вопросы и способы использовать cloud capabilities для повышения качества будущего incident response.

# Cloud-Specific Debrief Questions

Кроме стандартных AAR вопросов, следует отдельно проверить:

## Identity and access

- Какие identities были compromised?
- Какие permissions получил threat actor?
- Соответствовали ли identities принципу least privilege?
- Какие identity controls нужны для уменьшения blast radius?

## Resources

- Какие resources были compromised?
- Действительно ли identities, через которые был получен доступ, должны были иметь права на эти resources?
- Нужно ли применить более restrictive policies?

## Networking

- Обошел ли threat actor network controls?
- Были ли network rules слишком permissive или misconfigured?
- Какие дополнительные network controls предотвратят unauthorized access без нарушения functionality?

## Data exfiltration

- Есть ли внутри blast radius resources с sensitive data: buckets, VMs, databases и т.д.?
- Получал ли threat actor доступ к ним?
- Есть ли evidence массовой exfiltration?

Такие вопросы позволяют выявить cloud-specific lessons, которые могут быть упущены при generic incident review.

# Использование Cloud для Incident Response

Serverless functions для automated response pipeline — лишь один пример.

Облачную инфраструктуру можно использовать для:

- forensic analysis;
- evidence storage;
- automated response.

Часто это дешевле, чем содержать отдельную on-premises forensic infrastructure.

# Cloud Infrastructure for Forensic Workstations

Cloud compute и infrastructure-as-code templates позволяют готовить forensic workstations современным способом.

Вместо физических workstations можно разворачивать заранее сконфигурированные VMs с необходимыми:

- CPU;
- memory;
- forensic tooling.

Такие images можно поддерживать в актуальном состоянии и запускать on demand.

Infrastructure-as-code инструменты, включая:

- AWS CloudFormation;
- Azure Resource Manager templates;
- Terraform;

позволяют создавать и уничтожать forensic environment одной командой.

Это делает практичным подход, при котором для каждого расследования создается fresh workstation, а после закрытия case он уничтожается.

# Secure, Read-Only Log Storage

Если важна forensic integrity, cloud storage упрощает хранение evidence с chain of custody.

Преимущества:

- практически неограниченная емкость;
- низкая стоимость;
- встроенный audit trail;
- access controls;
- retention policies.

Можно сделать evidence read-only для authorized personnel и автоматически архивировать либо удалять его в соответствии с organizational policy.

Cloud providers также поддерживают immutable storage, предотвращающий modification и deletion evidence даже администраторами.

Listing 150 показывает AWS S3 Object Lock с write-once-read-many (WORM).

## Листинг 150. Настройка Immutable Forensic Storage в S3

```text
$ aws s3api create-bucket --bucket forensic-evidence-ir2025 --region us-east-1 --object-lock-enabled-for-bucket

$ aws s3api put-object-lock-configuration --bucket forensic-evidence-ir2025 --object-lock-configuration '{"ObjectLockEnabled": "Enabled", "Rule": {"DefaultRetention": {"Mode": "COMPLIANCE", "Days": 365}}}'
```

1. Создается S3 bucket с включенным Object Lock сразу при создании.
2. Применяется default retention policy в compliance mode, запрещающая любому user, включая root, удалять или перезаписывать objects в течение 365 дней.

Azure Blob Storage предоставляет аналогичную возможность через immutable storage policies, а Google Cloud Storage — retention policies с bucket lock.

Принцип одинаков: forensic evidence должно храниться так, чтобы исключить tampering и обеспечить verifiable chain of custody.

# Network Logging with VPC Flow Logs

VPC flow logs фиксируют metadata сетевого traffic через cloud network interfaces без специального packet-capture hardware.

Flow logs не содержат packet payloads, но дают важный контекст для расследований:

- network-based attacks;
- lateral movement;
- data exfiltration.

Каждая запись включает:

- source IP;
- destination IP;
- ports;
- protocol;
- transferred bytes;
- action accept/reject.

Этого достаточно, чтобы:

- выявлять communication patterns;
- оценивать data exfiltration volumes;
- проверять, работают ли network isolation controls.

Flow log data можно направлять в cloud storage или log analytics services для long-term retention и analysis.

Поскольку flow logs работают на network layer, они дополняют control plane logs и показывают traffic, не отражающийся в management APIs, например:

- lateral movement между instances внутри одного VPC;
- outbound connections к attacker-controlled infrastructure.

# Containers and Serverless for Forensic Tooling

Даже без fully automated pipeline containers и serverless services могут ускорить triage и response.

Forensic scripts можно:

- containerize;
- deploy как serverless functions.

Это позволяет собирать и анализировать evidence с минимальным operational overhead.

Velociraptor — open-source endpoint monitoring и digital forensics tool с lightweight agent. Он умеет собирать:

- file system metadata;
- running processes;
- event logs;
- memory.

Также поддерживает real-time hunting queries по крупным fleets через VQL.

Например, containerized Velociraptor server можно развернуть за минуты для сбора endpoint telemetry с compromised hosts.

Через Amazon ECS, Azure Container Instances или Google Cloud Run можно:

- запустить prebuilt Velociraptor server image;
- подключить agents к target hosts;
- начать сбор artifacts без отдельного dedicated server.

После расследования container можно остановить, а collected data сохранить в cloud storage.

Listing 151 показывает deployment Velociraptor server в Amazon ECS через AWS CLI. Создается Fargate task, который запускает frontend Velociraptor, открывает GUI и client communication ports и сохраняет artifacts в EFS volume.

## Листинг 151. Развертывание Velociraptor Server в Amazon ECS

```text
$ aws ecs create-cluster --cluster-name forensics-cluster

$ aws ecs register-task-definition --family velociraptor-server --network-mode awsvpc --requires-compatibilities FARGATE --cpu 2048 --memory 4096 --container-definitions '[{"name": "velociraptor", "image": "wlambert/velociraptor:latest", "portMappings": [{"containerPort": 8000, "protocol": "tcp"}, {"containerPort": 8001, "protocol": "tcp"}], "mountPoints": [{"sourceVolume": "velociraptor-data", "containerPath": "/velociraptor"}]}]' --volumes '[{"name": "velociraptor-data", "efsVolumeConfiguration": {"fileSystemId": "fs-0a1b2c3d4"}}]'

$ aws ecs create-service --cluster forensics-cluster --service-name velociraptor --task-definition velociraptor-server --desired-count 1 --launch-type FARGATE --network-configuration '{"awsvpcConfiguration": {"subnets": ["subnet-forensics"], "securityGroups": ["sg-velociraptor"], "assignPublicIp": "DISABLED"}}'
```

1. Создается dedicated ECS cluster для forensic tooling.
2. Регистрируется task definition с Velociraptor container image, портами 8000 для GUI и 8001 для client communication и EFS volume для persistent artifact storage.
3. Service разворачивается в private subnet с security group, ограничивающей доступ authorized forensic networks.

Azure Container Instances и Google Cloud Run поддерживают аналогичный pattern с использованием своих CLI:

- container image;
- port mapping;
- persistent storage configuration.

# ЗАКЛЮЧИТЕЛЬНЫЕ СООБРАЖЕНИЯ

Cloud incident response быстро развивается под влиянием:

- изменений cloud architecture;
- новых attacker techniques;
- новых инструментов.

Два сквозных вопроса для всего response lifecycle:

- multi-cloud environments;
- дальнейшее развитие cloud incident response.

# Multi-Cloud Environments

Одна из наиболее серьезных сложностей возникает в multi-cloud architecture.

Организация может распределять resources и users между:

- AWS;
- Azure;
- Google Cloud.

Это усложняет investigation и scoping в двух отношениях.

## 1. Централизация logs становится критически важной

Централизация в SIEM полезна при любой cloud architecture, но при нескольких cloud providers становится практически обязательной.

Investigation существенно замедляется, если responders вынуждены постоянно переключаться между provider consoles.

Cross-cloud correlation также усложняется из-за различий:

- field names;
- log formats;
- provider-specific semantics.

## 2. Cloud architecture влияет на scope

Если cloud environments полностью изолированы друг от друга, scope incident относительно понятен.

Если между clouds есть связи через:

- shared identity provider;
- federated authentication;
- direct network communication;

появляется возможность lateral movement через cloud boundaries.

Для корректного scoping нужно понимать:

- как clouds связаны;
- какие trust relationships существуют;
- входят ли связанные environments в incident scope.

Cross-cloud identity federation следует рассматривать как автоматическое расширение scope. Если единый identity provider, например Entra ID или Okta, используется в нескольких cloud environments, compromised identity в одном cloud следует считать потенциально имеющей доступ ко всем federated environments, пока не доказано обратное.

# Эволюция Cloud Incident Response

Cloud incident response меняется вместе с использованием cloud services и способами атак на них.

Несколько тенденций особенно важны.

## Multi-cloud visibility

Когда workloads распределены между несколькими providers, получить единое представление security posture становится сложнее.

Cloud Security Posture Management (CSPM) инструменты дают centralized visibility по:

- misconfigurations;
- policy violations;
- security risks;

в AWS, Azure, Google Cloud и SaaS platforms.

Для incident responders CSPM может ускорить scoping, быстро показывая:

- какие resources exposed;
- где permissions слишком широки;
- какие misconfigurations могли обеспечить attack path.

Организациям с multi-cloud следует рассматривать CSPM не только как preventive security control, но и как часть incident response preparation.

## AI-driven SOC operations

AI в security operations выходит за рамки простой alert correlation.

Как рассмотрено в Chapter 16, AI-driven tooling начинает выполнять investigation и response actions, которые раньше требовали human analysts.

В API-driven cloud infrastructure AI agents потенциально могут:

- triage alerts;
- собирать context из нескольких log sources;
- выполнять containment actions с минимальным human oversight.

Cloud-native detection services также интегрируют AI для:

- снижения false positives;
- повышения confidence findings.

Эти capabilities продолжают развиваться. Организациям следует отслеживать их зрелость и оценивать, где AI-assisted investigation может дополнять cloud response workflows.

## Runtime visibility для Serverless и Containers

Traditional host-based forensics предполагает наличие:

- persistent filesystem;
- memory;
- process list.

Serverless functions и ephemeral containers нарушают это предположение.

Lambda function или Cloud Run service могут работать секунды и не оставить persistent state. Container workload может быть автоматически уничтожен и заменен до того, как responders успеют собрать evidence.

Поэтому runtime security tooling, отслеживающий:

- function execution;
- container behavior;
- API calls;

становится важной частью cloud visibility.

Без runtime visibility единственным evidence могут остаться control-plane logs, показывающие только факт execution или start, но не:

- какой code выполнялся;
- какие data были доступны;
- какие network connections устанавливались.

Для serverless и ephemeral containers runtime monitoring фактически является единственным источником информации о том, что происходило внутри workload.

## Token-based attacks

В cloud и SaaS environments растет доля token-based attacks относительно классического password compromise.

Вместо кражи password и обычного login атакующие нацеливаются на:

- session tokens;
- OAuth tokens;
- API keys.

Они могут полностью обходить authentication controls.

Украденный session token может дать доступ:

- без MFA challenge;
- без появления нового login event.

Это делает attack сложнее для traditional authentication monitoring.

Следует отслеживать anomalous token usage:

- token используется с неожиданного IP;
- token используется из необычной geographic location;
- unusually long token lifetime;
- token refresh patterns не соответствуют нормальному user behavior.

Conditional access policies, привязывающие tokens к устройствам или network ranges, уменьшают ценность украденного token. Short token lifetime сокращает exposure window.

## Cloud-native forensics

Организации все чаще используют cloud infrastructure для:

- forensic analysis;
- evidence storage;
- automated response.

Тренд будет усиливаться по мере развития cloud-native tooling.

Облако хорошо подходит для IR благодаря:

- scalability;
- accessibility;
- auditability.

Возможность:

- развернуть forensic workstation on demand;
- хранить evidence в immutable storage с automatic chain-of-custody logging;
- запускать automated collection scripts как serverless functions;

снижает overhead отдельной dedicated forensic infrastructure.

Для организаций, чья production environment уже находится в cloud, использование cloud services для incident response является естественным продолжением существующей архитектуры.

# Ссылки

[1] Google Cloud, "Threat Horizons Report H1 2025," services.google.com/fh/files/misc/threat_horizons_report_h1_2025.pdf

[2] Google Cloud, "Threat Horizons Report H2 2025," services.google.com/fh/files/misc/cloud_threat_horizons_report_h22025.pdf

[3] Mandiant, "M-Trends 2025," services.google.com/fh/files/misc/m-trends-2025-en.pdf

[4] Orca Security, "2025 State of Cloud Security Report," orca.security/wp-content/uploads/2025/06/2025-State-of-Cloud-Security-Report-v2.pdf

[5] Google Cloud, "Threat Horizons Report H1 2025," services.google.com/fh/files/misc/threat_horizons_report_h1_2025.pdf

[6] CircleCI, "CircleCI incident report for January 4, 2023 security incident," January 2023, circleci.com/blog/jan-4-2023-incident-report/

[7] Google Cloud, "Threat Horizons Report H1 2025," services.google.com/fh/files/misc/threat_horizons_report_h1_2025.pdf

[8] Mandiant, "M-Trends 2025," services.google.com/fh/files/misc/m-trends-2025-en.pdf

[9] AWS Prescriptive Guidance, "Automate incident response and forensics," docs.aws.amazon.com/prescriptive-guidance/latest/patterns/automate-incident-response-and-forensics.html
