# Chapter 18 — Segment 04

Source RAG: `p0599:c01`–`p0603:c01`

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
