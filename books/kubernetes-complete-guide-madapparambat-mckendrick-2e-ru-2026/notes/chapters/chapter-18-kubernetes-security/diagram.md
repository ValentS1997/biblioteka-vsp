# Диаграммы главы 18 — многоуровневая безопасность Kubernetes

**Source:** chapter RAG PDF pp587–640, `p0587:c01`–`p0640:c01`. Mermaid-схемы синтезированы по тексту, не являются копиями рисунков PDF и не вводят внешних фактов.

## API request: identity → authorization → admission → audit

```mermaid
flowchart TD
  Q["Запрос к Kubernetes API"]
  AUTH{"Аутентификация успешна?"}
  DENY401["401 Unauthorized или anonymous при разрешении"]
  IDENT["username, groups, extra"]
  RBAC{"Авторизация (RBAC / Node / Webhook...)?"}
  DENY403["403 Forbidden"]
  WRITE{"Изменяющий запрос?"}
  MUTATE["Mutating admission"]
  VALIDATE{"Validating admission"}
  REJECT["Отклонить запрос"]
  APPLY["API выполняет запрос"]
  AUDIT["Аудит действий и событий"]
  Q --> AUTH
  AUTH -->|"Нет"| DENY401
  AUTH -->|"Да"| IDENT --> RBAC
  RBAC -->|"Нет"| DENY403
  RBAC -->|"Да"| WRITE
  WRITE -->|"Да"| MUTATE --> VALIDATE
  VALIDATE -->|"Нет"| REJECT
  VALIDATE -->|"Да"| APPLY
  WRITE -->|"Нет: get/list/watch"| APPLY
  APPLY --> AUDIT
```

pp589–592, p612, pp619–622. Source states admission does not reject pure reads; audit is discussed as logging cluster actions, not a source-tested policy.

## ServiceAccount and RBAC negative/positive test

```mermaid
flowchart TD
  POD["Pod pod-logger-app, SA pod-logger"]
  REQUEST["GET /api/v1/namespaces/rbac-demo-ns/pods"]
  RULE["Role pod-reader: get/watch/list pods"]
  BIND{"RoleBinding read-pods exists?"}
  FORBIDDEN["403 Forbidden"]
  OK["PodList from API"]
  REMOVE["kubectl delete rolebinding read-pods"]
  POD --> REQUEST --> BIND
  RULE --> BIND
  BIND -->|"Нет"| FORBIDDEN
  BIND -->|"Да"| OK --> REMOVE --> FORBIDDEN
```

pp614–619. ServiceAccount identity does **not** itself grant Pods-listing rights. Source shell echo says "default namespace" but API URI and Resource are `rbac-demo-ns` (see findings).

## Authentication methods

```mermaid
flowchart TD
  API["kube-apiserver authentication"]
  STATIC["Static token file (discouraged)"]
  SA["ServiceAccount / TokenRequest"]
  CERT["Client X.509 with CA / CSR"]
  OIDC["OIDC external IdP (SSO)"]
  EXTRA["Authenticating proxy / webhook / bootstrap"]
  API --> STATIC
  API --> SA
  API --> CERT
  API --> OIDC
  API --> EXTRA
```

pp591–611. `kubectl create token` is sensitive; CSR approval grants credentials; identity issuance is not a mere observation.

## Admission controllers and securityContext

```mermaid
flowchart TD
  POD["Pod spec"]
  SEC["securityContext"]
  UID["runAsUser/runAsGroup = 1000"]
  ROOT["readOnlyRootFilesystem = true"]
  ELEVATE["CAP_NET_ADMIN or privileged = true (risk)"]
  RESULT["id = UID/GID 1000; touch /testfile denied"]
  POD --> SEC
  SEC --> UID --> RESULT
  SEC --> ROOT --> RESULT
  SEC --> ELEVATE
```

pp624–628. Elevated settings are **not** recommended defaults. The source uses writable `emptyDir` at /usr/share/nginx/html alongside read-only rootfs.

## NetworkPolicy source experiment and discrepancy

```mermaid
flowchart TD
  A["web1: nginx1"]
  B["web2: nginx2"]
  NONE["Before policy: HTTP response"]
  DENY["web2 default-deny-ingress: curl timeout"]
  ALLOW["web2 allow-from-web1-netpol applied"]
  SUCCEED["nginx1 curl returns HTML"]
  CLAIM["Source claims only nginx1 from web1 can access"]
  UNKNOWN["Other peers untested; source YAML uses separate from entries"]
  A --> NONE --> DENY --> ALLOW --> SUCCEED
  B --> DENY
  SUCCEED --> CLAIM --> UNKNOWN
```

pp630–634. The last test proves **a connection from nginx1**, not exclusion of every other source; the YAML has separate namespaceSelector and podSelector entries rather than a shown conjunctive peer. The printed resource name after apply is also inconsistent.

## TLS / runtime and registry image access

```mermaid
flowchart TD
  SEC["Workload protection layers"]
  MTLS["TLS / mTLS for component links"]
  RUNTIME["gVisor (user-space kernel) / Kata (lightweight VM)"]
  IMAGE["Private registry access"]
  SECRET["docker-registry Secret + imagePullSecrets"]
  SEC --> MTLS
  SEC --> RUNTIME
  SEC --> IMAGE --> SECRET
```

pp634–639. No end-to-end TLS, RuntimeClass deployment or private image pull executed in chapter RAG; encryption-at-rest for Secrets and availability of runtime handler **[Needs confirmation]**.
