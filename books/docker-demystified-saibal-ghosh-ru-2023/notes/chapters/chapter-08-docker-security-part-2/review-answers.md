# Ответы к контрольным материалам — глава 8

## Контрольный тест: ключ из источника

| № | Ответ |
|---:|:---:|
| 1 | D |
| 2 | C |
| 3 | B |
| 4 | C |
| 5 | A |
| 6 | C |
| 7 | C |
| 8 | D |
| 9 | A |
| 10 | A |

Ключ `1-D, 2-C, 3-B, 4-C, 5-A, 6-C, 7-C, 8-D, 9-A, 10-A` прямо приведён в `p0212:c01`.

## Ответы на открытые вопросы

### 1. Из каких компонентов состоит Docker Enterprise Edition?

По source: Docker Engine Enterprise, Universal Control Plane и Docker Trusted Registry.

### 2. Каковы основные функции UCP?

UCP обеспечивает centralized management of clusters/applications, управляет source-era Swarm/Kubernetes environment и предоставляет authentication/authorization/RBAC model.

### 3. Каковы основные функции DTR?

DTR — enterprise image registry. В chapter он хранит repositories/images и выполняет vulnerability scanning against CVE database.

### 4. Для чего нужен Client Bundle?

Чтобы авторизованный client мог обращаться к UCP по certificate-based TLS. Bundle содержит client key/certificate material и scripts/configuration для Docker CLI and Kubectl.

### 5. Какие environment variables обновляет Client Bundle?

- `DOCKER_HOST`
- `DOCKER_CERT_PATH`
- `DOCKER_TLS_VERIFY`

### 6. Что такое CVE?

В chapter CVE database — регулярно обновляемая база известных vulnerabilities, которую DTR использует при image scanning.

### 7. Что такое RBAC?

Role Based Access Control — модель, в которой определённый subject получает role с набором permissions для определённого resource set/collection.

```text
subject + role + collection → grant
```

### 8. Что означают users, organizations и teams?

User — конкретный UCP user.  
Organization — grouping users with common permission/privilege context.  
Team — group of users, typically inside organization; source показывает organization containing teams and user membership through team.

### 9. Что такое role?

Role — набор permissions/privileges that defines which operations subject may perform. Source includes predefined roles and custom roles.

### 10. Что такое collection?

Collection — resource set to which permissions apply. Source examples include development/test/production-style separation conceptually and built-in UCP collection paths.

## Operational map

```text
control plane:
Client Bundle → UCP → RBAC / cluster management

image supply:
docker push → DTR → CVE scan → findings

authorization:
subject + role + collection → grant
```

## Provenance

Ответы сформированы только по chapter RAG `p0185:c01`–`p0212:c01`. External sources и model-memory не использовались.
