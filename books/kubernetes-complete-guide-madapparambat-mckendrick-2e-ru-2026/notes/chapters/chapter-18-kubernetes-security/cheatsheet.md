# Cheatsheet — Глава 18: Безопасность Kubernetes

**Source:** RAG-only PDF **587–640**, `p0587:c01`–`p0640:c01`. Kubernetes не вызывался; source URL/параметры не сверялись с внешней документацией. Unknown: **[Needs confirmation]**.

## Symptom / problem framing

Нужна защита доступа к Kubernetes API, процессов внутри Pod, сетевых потоков и приватных образов. Неправильные ServiceAccount, RoleBinding, NetworkPolicy или `securityContext` могут как открыть ненужные полномочия, так и заблокировать приложение. Ключевой контур: **authenticate → authorize → mutate/validate (admission) → audit** (pp589–592), с независимыми runtime/TLS/Secret слоями.

## Baseline / context

- Развёрнутый Kubernetes и настроенный `kubectl`; многозвенный/облачный кластер желателен (p588). Реальные cluster, context, namespace, API flags, версии CNI, права на CSR и реальные secret policies **[Needs confirmation]**.
- **Пользователь** идентифицируется вне Kubernetes; **ServiceAccount** — namespaced API-object для процессов. Subject SA: `system:serviceaccount:<namespace>:<name>` (p592). Стандартный `default` SA в каждом namespace и автоматический токен; параметр `automountServiceAccountToken: false` позволяет отказаться от монтирования (pp595–597).
- **Аутентификация** (сертификаты, SA/статический токен, OIDC, webhook/proxy, bootstrap) определяет личность. Неудача → 401 или `system:anonymous` при включённом anonymous. **Авторизация** (RBAC и другие режимы) запрещает недостаточные права → 403 (pp590–594, p612).
- **RBAC:** `Role` namespaced; `ClusterRole` global; `RoleBinding` namespaced связывает Role **или** ClusterRole; `ClusterRoleBinding` global связывает ClusterRole (p614).
- **Admission** не применяется к `get/list/watch`: сначала mutating, потом validating; его настройки в статическом манифесте API server являются критичной control-plane операцией (pp619–622).
- `securityContext` задаёт UID, GID, Linux capabilities, root filesystem, privileged и др. (pp624–628). Добавление `CAP_NET_ADMIN`/privileged — *усиление полномочий*, а не безопасный вариант по умолчанию.
- `NetworkPolicy` требует CNI с поддержкой — источник использует Calico на minikube. Без политик Pod не изолированы; с правилом default-deny ingress — блокировка входа к выбранным Pod (pp628–633).

## Read-only checks

```bash
kubectl config current-context
kubectl auth whoami
kubectl get po -n example-ns
kubectl get pods -n kube-system
kubectl get svc -n example-ns
kubectl get po -n rbac-demo-ns
kubectl logs -n rbac-demo-ns pod-logger-app -f
kubectl get csr
kubectl get po -o wide -n web1
kubectl get po -o wide -n web2
```

Evidence pp600–605, 616–618, 631. **Read-only** in API terms; logs and `kubectl auth whoami` may reveal identity, resources, identities and token metadata; `logs -f` keeps a stream open. `kubectl config view -o json | jq '.users[]'` (p603) may expose auth material, so **do not print or archive unredacted kubeconfig**. `minikube ssh 'sudo grep -- "--enable-admission-plugins" /etc/kubernetes/manifests/kube-apiserver.yaml'` (p622) reads control-plane file but requires elevated host access. SSH access itself requires change control.

## Interpretation

**RBAC positive/negative test.** `example-ns` SA `example-sa` bound to Role `pod-reader` can `list` pods in example-ns but `get pods -n kube-system` and `get svc -n example-ns` yield 403 (pp597–601). A separate `rbac-demo-ns` `pod-logger-app` initially gets 403, after RoleBinding gets `PodList`, and after deleting RoleBinding gets 403 (pp614–619). Permission change is effective without changing identity. Token used by external kubectl is **not recommended production user auth** (p602).

**X.509:** CSR `iamgini`, `CN=iamgini`, organization fields map to groups; only after approval and signed certificate can kubeconfig identity authenticate (pp602–606). Key `iamgini.key` and `iamgini.crt` are **sensitive**, not safe repository outputs. Source does not show cert expiry/rotation/revocation recovery.

**OIDC:** external IdP, issuer, client ID, username/group claim mapping, discovery and trust (pp606–610). Source mentions Dex, Keycloak, OpenUnison and UAA. Exact cloud provider IdP and issuer settings **[Needs confirmation]**.

**NetworkPolicy result:** nginx1 `web1` → nginx2 `web2` succeeds without policy (p632), times out after default-deny ingress in web2 (p633), then succeeds after allow policy (p634). **CRITICAL:** p633 YAML has two separate `from` peers: a `namespaceSelector project:web1` and a `podSelector app:nginx1`. Source text says it allows **only nginx1 in web1**, but manifest's peers are separate, so the named restrictive requirement is **not demonstrated**. Also `metadata.name: allow-from-web1-netpol` but printed apply output says `nginx2-networkpolicy created`. Do not reuse as an audited least-privilege rule.

**securityContext result:** p628 `id` → uid/gid 1000 and `touch /testfile` → `Read-only file system`. This shows specific rootfs restriction, not a universal hardened Pod; source `nginx:latest` compatibility [Needs confirmation].

**TLS and sandbox:** mTLS protects both ends of connections; examples API server↔etcd, Ingress↔backends, service mesh, node encryption (pp634–636). gVisor isolates via user-space kernel interception, Kata via lightweight VMs, `runtimeClassName: kata-containers` requires installed handler (pp636–638). No actual mTLS or runtime deployment in source.

**Secrets:** `kubectl create secret docker-registry` + `imagePullSecrets` (pp638–639), requires same namespace. **Do not assume command itself enables encryption at rest** despite statement p638; encryption config/RBAC/secret lifecycle not shown [Needs confirmation].

## Next action

Verify actual context, target namespace, CNI policy support, running control plane settings, existing RBAC bindings and available RuntimeClasses **without changing them**. For authentication use organization-approved identity and rotation; scope permissions to exactly needed verbs/resources/namespace. For network policy isolate a disposable namespace, confirm both deny and allow paths from multiple sources, especially unintended peers. For secrets use approved credential ingress and encryption-at-rest validation. Do not test API-server static token flags or privileged containers on production clusters.

## Modifying action (source lab steps, NOT EXECUTED)

```bash
kubectl apply -f 01_serviceaccount/
kubectl create token example-sa -n example-ns
kubectl config set-credentials example-sa --token=<ваш_токен>
kubectl config set-context example-sa-context --user=example-sa --cluster=minikube
kubectl config use-context example-sa-context
kubectl apply -f 02_rbac/rbac-demo-ns.yaml
kubectl apply -f 02_rbac/pod-logger-serviceaccount.yaml
kubectl apply -f 02_rbac/pod-reader-role.yaml
kubectl apply -f 02_rbac/pod-logger-app.yaml
kubectl apply -f 02_rbac/read-pods-rolebinding.yaml
kubectl delete rolebinding read-pods -n rbac-demo-ns
```

pp598–601, 614–619. **Effect:** namespaces/SA/Role/RoleBinding/workload created; `create token` issues sensitive credential; `config` updates local kubeconfig; binding grants/revokes API read permissions. **Risk:** token leak, accidentally replacing active context, scheduling Pod with SA access. **Verification:** `auth whoami`, restricted `get po`, log `403 → PodList → 403`. **Rollback:** switching to previously noted context in source (p601), deleting binding and demo namespace (p619); exact namespace cleanup CLI not supplied and existing data/security controls must be checked.

For network experiment (pp629–634) `minikube start --network-plugin=cni --cni=calico --container-runtime=containerd` changes/creates local cluster. `kubectl apply -f web-app1.yaml` / `web-app2.yaml` and `kubectl apply -f default-deny-ingress.yaml -n web2` modify workloads/network access; source's `allow-from-web1-netpol.yaml` **does not encode the stated single-pod restriction**. **Do not apply as security runbook**. `kubectl -n web1 exec nginx1 -- curl 10.244.120.72` opens process/network connection; source IP is demo-only.

The source also shows creating CSR with `openssl`, approving it using `kubectl certificate approve iamgini`, and local certificate/credential setup (pp604–605). These are **high-sensitivity identity changes** requiring admin approval and protected private key handling; details in commands.md. No rollback or revocation workflow provided.

## Verification / acceptance checks

Expected tests *as book examples*, not executed here: SA identity, allowed namespace read and forbidden other resource; CSR `Approved` and `whoami iamgini`; RBAC `403 → PodList → 403`; Pod `id` 1000/1000 and rootfs write denied; before-policy curl success / after-deny timeout / after-allow source curl success. **Do not infer policy is least-privileged**, verify extra non-matching traffic sources separately. Source does not verify mTLS, encrypted etcd, Kata runtime, registry pull, cert revoke or network fail-open conditions.

## Rollback

Source-supported: `kubectl delete rolebinding read-pods -n rbac-demo-ns` revokes lab permission (p619); `kubectl config use-context <имя_контекста>` restores previous saved context (p601); disposable `rbac-demo-ns` deletion proposed but not shown as command. For `NetworkPolicy`, CSR, kube-apiserver flags, registry Secret, cloud environments or runtime handler source does **not** provide validated backup/rollback. All **[Needs confirmation]**. Changing API server admission flags risks restarting/losing cluster control plane (p622); explicit approval and verified recovery plan are prerequisites.
