# Chapter 18 — Segment 03

Source RAG: `p0594:c01`–`p0598:c01`

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
