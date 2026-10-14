# Commands and YAML — Глава 18: Kubernetes Security

**Strict provenance:** chapter PDF 587–640, RAG chunks `p0587:c01`–`p0640:c01`. **Source examples only; not executed.** Classifications: read-only observation, cluster-state-changing, local-secret-changing, workload-generating, control-plane disruptive, privileged. No invented fixes.

## API authentication / static token

p0593–p0595: **not recommended for production**, kube-apiserver static Pod manifest `/etc/kubernetes/manifests/kube-apiserver.yaml` includes `--token-auth-file=/etc/kubernetes/user-tokens.csv`, example CSV `token,user,uid,"group1,group2,group3"`, API header `Authorization: Bearer <токен>`. **Classification:** editing API server/token file is privileged, control-plane-state-changing; leaked CSV compromises all static users, rotation needs API-server restart in source. **Verification:** authenticated identity via client; **Rollback:** not provided [Needs confirmation]; don't change kube-apiserver in a shared cluster.

```bash
kubectl config set-credentials <контекстный_пользователь> --token=<токен>
```

p0594. **Local-sensitive change:** inserts a credential in kubeconfig; risks shell history, local persistence and future cluster impersonation. Source says create/use context afterward, no safe secret cleanup procedure [Needs confirmation].

## ServiceAccount demo: namespace and minimum RBAC

p0597–p0598 source defines:
```yaml
# 01_serviceaccount/example-sa-ns.yaml
apiVersion: v1
kind: Namespace
metadata:
  name: example-ns
---
apiVersion: v1
kind: ServiceAccount
metadata:
  name: example-sa
  namespace: example-ns
---
# In a separate file: pod-reader-role.yaml
apiVersion: rbac.authorization.k8s.io/v1
kind: Role
metadata:
  namespace: example-ns
  name: pod-reader
rules:
  - apiGroups: [""]
    resources: ["pods"]
    verbs: ["get", "watch", "list"]
---
# In a separate file: read-pods-rolebinding.yaml
apiVersion: rbac.authorization.k8s.io/v1
kind: RoleBinding
metadata:
  name: read-pods
  namespace: example-ns
subjects:
  - kind: ServiceAccount
    name: example-sa
    namespace: example-ns
roleRef:
  kind: Role
  name: pod-reader
  apiGroup: rbac.authorization.k8s.io
```

The documents above represent **separate source manifests** logically combined for reading; they are not an actual combined source file. Actions:
```bash
kubectl apply -f 01_serviceaccount/
kubectl create token example-sa -n example-ns
kubectl config set-credentials example-sa --token=<ваш_токен>
kubectl config set-context example-sa-context --user=example-sa --cluster=minikube
kubectl config current-context
kubectl config use-context example-sa-context
kubectl auth whoami
kubectl get po -n example-ns
kubectl get pods -n kube-system
kubectl get svc -n example-ns
```

Source pp598–601. **Effect:** `apply` creates namespace, SA, Role and RoleBinding; `create token` mints **bearer credential** (don't print/log/submit to third-party JWT site), `config` writes local credentials and switches active context. `auth whoami`/`get` are observational. **Verification:** user `system:serviceaccount:example-ns:example-sa`; Pod list allowed in example-ns; denied (403) listing kube-system Pods and example-ns Services. **Rollback:** `kubectl config use-context <имя_контекста>` (p601); no comprehensive token revocation or manifest cleanup given [Needs confirmation].

Source p0597 describes `automountServiceAccountToken: false` (SA or Pod spec, Pod setting wins), but no actual mutate command is tested for this option.

p0600 additional source:
```bash
cp references/sa-demo-nginx-pod.yaml 01_serviceaccount/nginx-pod.yaml
kubectl apply -f 01_serviceaccount/nginx-pod.yaml
kubectl get po -n example-ns
```
**Effect:** local file copy and nginx Pod creation; complete nginx YAML is a separate repository file, not reproduced in RAG. **Risk:** resource scheduling, mutable source file provenance; **Verification:** nginx Pod Running. **Rollback:** absent [Needs confirmation].

## X.509 CSR exercise — sensitive identity and admin approval

p0603–p0605:
```bash
kubectl config view -o json | jq '.users[]'
openssl genrsa -out iamgini.key 2048
openssl req -new -key iamgini.key -out iamgini.csr -subj "/CN=iamgini/O=web1/O=frontend"
cat iamgini.csr | base64 -w 0
kubectl apply -f csr.yaml
kubectl get csr
kubectl certificate approve iamgini
kubectl get csr iamgini -o json | jq -r '.status.certificate' | base64 --decode > iamgini.crt
ls iamgini.*
kubectl config set-credentials iamgini --client-key=/full-path/iamgini.key --client-certificate=/full-path/iamgini.crt
kubectl config set-context iamgini --cluster=minikube --user=iamgini
kubectl config use-context iamgini
kubectl auth whoami
```

p0604 CSR manifest:
```yaml
apiVersion: certificates.k8s.io/v1
kind: CertificateSigningRequest
metadata:
  name: iamgini
spec:
  request: <CSR in base64 from source step 3>
  signerName: kubernetes.io/kube-apiserver-client
  usages:
    - client auth
```

**Classification:** `config view`, `get csr`, `ls`, `whoami` are observational but `config view` **may reveal sensitive auth data**; `openssl genrsa` writes **private key**; `apply` submits CSR; `certificate approve` is admin-approved sensitive **identity issuance**; `config set-credentials`/context mutate local kubeconfig. **Verification:** `get csr` Pending then Approved and `whoami` Username `iamgini`, groups `web1` and `frontend` (p605). **Risks:** inadvertently sharing private keys, grants more identity than intended, signing an unaudited CSR, cert expiration/rotation. **Rollback:** revocation and certificate cleanup [Needs confirmation]; not provided.

## RBAC before/after RoleBinding

p0614–p0619:
```bash
kubectl apply -f 02_rbac/rbac-demo-ns.yaml
kubectl apply -f 02_rbac/nginx-pod.yaml
kubectl apply -f 02_rbac/pod-logger-serviceaccount.yaml
kubectl apply -f 02_rbac/pod-reader-role.yaml
kubectl apply -f 02_rbac/pod-logger-app.yaml
kubectl get po -n rbac-demo-ns
kubectl exec -it -n rbac-demo-ns pod-logger-app -- bash
kubectl logs -n rbac-demo-ns pod-logger-app -f
kubectl apply -f 02_rbac/read-pods-rolebinding.yaml
kubectl logs -n rbac-demo-ns pod-logger-app -f
kubectl delete rolebinding read-pods -n rbac-demo-ns
```

**Effect:** first five create namespace, 2 Pod, SA, namespaced Role. `exec` starts shell inside Pod (sensitive, not read-only API), `logs -f` only observes stream. `apply` binding grants SA Pods get/list/watch; `delete rolebinding` **revokes** it. **Verification:** before binding logs HTTP **403**, after binding `PodList`, after delete logs 403 (pp617–619). **Rollback:** deletion of binding as source; cleanup of demo namespace mentioned but no explicit command, [Needs confirmation]. **Risk:** deployed pod queries Kubernetes API every 10 seconds and logs output.

p0616 source pod `pod-logger-app` has `serviceAccountName: pod-logger`, `image: quay.io/iamgini/k8sutils:debian12`, shell loop reading `/var/run/secrets/kubernetes.io/serviceaccount/token` and `ca.crt`, sends `curl --cacert ... --header "Authorization: Bearer $TOKEN" -X GET https://kubernetes.default.svc.cluster.local/api/v1/namespaces/rbac-demo-ns/pods`. **Never print token or attach unredacted shell logs.** Source echoes “Pods in default namespace” while URL and output actually target `rbac-demo-ns`, see findings.

## Admission controller settings (control-plane high risk)

p0622 source read-only (requires minikube VM privileges):
```bash
minikube ssh 'sudo grep -- "--enable-admission-plugins" /etc/kubernetes/manifests/kube-apiserver.yaml'
```

Source shows `--enable-admission-plugins=NamespaceLifecycle,LimitRanger,ServiceAccount,DefaultStorageClass,DefaultTolerationSeconds,NodeRestriction,MutatingAdmissionWebhook,ValidatingAdmissionWebhook,ResourceQuota`. Author additionally illustrates a `kube-apiserver --disable-admission-plugins=PodNodeSelector,AlwaysDeny ...` startup flag. **Classification:** inspection itself read-only; editing static Pod manifest or running altered API server flags is **critical disruptive control-plane change** (kubelet restarts API Pod). **Risk:** loss of API availability, skipped policies; **Rollback:** no verified restore path or admission checklist in source [Needs confirmation]. Do not perform in a shared cluster.

## SecurityContext: non-root and rootfs tests

p0627 source:
```yaml
# pod-with-security-context.yaml
apiVersion: v1
kind: Pod
metadata:
  name: security-context-demo
spec:
  containers:
    - name: app-container
      image: nginx:latest
      securityContext:
        runAsUser: 1000
        runAsGroup: 1000
        readOnlyRootFilesystem: true
      volumeMounts:
        - name: html-volume
          mountPath: /usr/share/nginx/html
  volumes:
    - name: html-volume
      emptyDir: {}
```

```bash
kubectl apply -f pod-with-security-context.yaml
kubectl exec -it security-context-demo -- /bin/sh
id
touch /testfile
```

**Effect:** `apply` creates Pod, `exec` interactive shell and `touch` attempts to mutate container rootfs (expected failure). **Verification:** `uid=1000 gid=1000`, `touch: /testfile: Read-only file system` in source p628. **Risk:** source image `nginx:latest` mutable; Pod readiness and full hardening not demonstrated. **Rollback:** no pod delete in source [Needs confirmation].

p0625 also presents `capabilities.add: [CAP_NET_ADMIN]` and `privileged: true` for a `privileged-container` Pod. These **grant elevated privileges** and are not endorsed as production security controls. Avoid deploying them; runtime and least privilege impact [Needs confirmation].

## NetworkPolicy: deny and allow (source has a critical mismatch)

p0629 requires CNI supporting policy, source Calico:
```bash
minikube start --network-plugin=cni --cni=calico --container-runtime=containerd
kubectl apply -f web-app1.yaml
kubectl apply -f web-app2.yaml
kubectl get po -o wide -n web1
kubectl get po -o wide -n web2
kubectl -n web1 exec nginx1 -- curl 10.244.120.72
```

**Effect:** cluster creation/configuration (potential existing profile impact), Namespaces `web1`/`web2` and nginx Pod creation, remote exec launches curl traffic. **Verification:** initial HTTP 200/sample nginx HTML (pp631–632). **Rollback:** not supplied.

p0632 `default-deny-ingress.yaml` (source has no `metadata.namespace`, apply uses `-n web2`):
```yaml
apiVersion: networking.k8s.io/v1
kind: NetworkPolicy
metadata:
  name: default-deny-ingress
spec:
  podSelector: {}
  policyTypes:
    - Ingress
  ingress: []
```
```bash
kubectl apply -f default-deny-ingress.yaml -n web2
kubectl -n web1 exec nginx1 -- curl 10.244.120.72
```
**Effect:** disrupts *all incoming traffic to selected Pods in web2*; source curl times out (135435 ms) p633. **Risk:** outage, DNS/monitoring impact for real workloads. **Verification:** example timeout, not a measured security guarantee. **Rollback:** not supplied [Needs confirmation].

p0633 `allow-from-web1-netpol.yaml` source:
```yaml
apiVersion: networking.k8s.io/v1
kind: NetworkPolicy
metadata:
  name: allow-from-web1-netpol
  namespace: web2
spec:
  podSelector:
    matchLabels:
      app: nginx2
  policyTypes:
    - Ingress
  ingress:
    - from:
        - namespaceSelector:
            matchLabels:
              project: web1
        - podSelector:
            matchLabels:
              app: nginx1
      ports:
        - protocol: TCP
          port: 80
```

```bash
kubectl apply -f allow-from-web1-netpol.yaml
kubectl -n web1 exec nginx1 -- curl 10.244.120.72
```

**CRITICAL SOURCE DISCREPANCIES:** Source prose claims only Pod `nginx1` *in* `web1` can access `nginx2`, but YAML uses **two separate `from` peer entries** (`namespaceSelector` and `podSelector`) rather than demonstrating their conjunction. p0633 output after apply names `nginx2-networkpolicy`, not manifest `allow-from-web1-netpol`. Source success test p634 only checks nginx1, **not non-matching peers**. **Do not treat as verified narrow policy or reuse unreviewed.** Corrected YAML would be external adjudication, not part of RAG-only artifact. Actual enforceability and rollback **[Needs confirmation]**.

## TLS, RuntimeClass and registry Secrets

p0634–p0638 describe mTLS links and runtime sandboxes but provide **no executable TLS or gVisor/Kata installation**. Source RuntimeClass sample:
```yaml
apiVersion: v1
kind: Pod
metadata:
  name: secure-pod
spec:
  runtimeClassName: kata-containers
  containers:
    - name: my-app
      image: my-secure-image
```
**Effect if applied:** schedules through configured RuntimeClass handler; existence/config/compatibility of handler not shown [Needs confirmation]. No source apply command.

p0639 registry:
```bash
kubectl create secret docker-registry my-registry-secret \
  --docker-server=your-registry.com \
  --docker-username=your_username \
  --docker-password=your_password \
  --docker-email=your-email@example.com
```
```yaml
apiVersion: v1
kind: Pod
metadata:
  name: my-pod
spec:
  containers:
    - name: my-container
      image: your-registry.com/your-image:tag
  imagePullSecrets:
    - name: my-registry-secret
```
**State-changing and sensitive:** creates namespaced Secret containing registry credential and source Pod would use it. **Risk:** `--docker-password` leaks into shell history/process lists/logs, Base64/Secret alone does not prove at-rest encryption (despite broad claim p638). Source footnote says Pod and Secret must be **in same namespace** (p639). **Verification:** only source conceptual image pull, no actual live pod or successful pull shown. **Rollback/rotation:** [Needs confirmation].
