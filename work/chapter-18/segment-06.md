# Chapter 18 — Segment 06

Source RAG: `p0609:c01`–`p0612:c01`

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
