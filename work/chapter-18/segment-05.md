# Chapter 18 — Segment 05

Source RAG: `p0604:c01`–`p0608:c01`

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
