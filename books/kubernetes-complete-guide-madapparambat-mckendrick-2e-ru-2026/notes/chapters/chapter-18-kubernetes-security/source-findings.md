# Source findings — Глава 18, Kubernetes security

**Source-only evidence:** RAG pp587–640, `p0587:c01`–`p0640:c01`. Classification: [Source contradiction], [Source code mismatch], [Source wording/code mismatch], [Source extraction issue], [Needs confirmation]. No external adjudication, silent repairs or executions.

## F-01 — [Source wording/code mismatch] — NetworkPolicy peer semantics
**p0633:** `allow-from-web1-netpol.yaml` declares two separate `ingress[].from` list elements, (1) `namespaceSelector.matchLabels.project: web1` and (2) `podSelector.matchLabels.app: nginx1`. **p0633–p0634 prose:** says only `nginx1` from `web1` may contact `nginx2`, all other traffic blocked. **Boundary:** separate peers are not the shown combined namespace+Pod constraint; source runs only one positive `curl` from nginx1. Conjunctive restriction not demonstrated. Exact permitted peers **[Needs confirmation]**. Do NOT use this manifest as validated least-privilege firewall policy.

## F-02 — [Source code mismatch] — NetworkPolicy metadata.name vs output
**p0633:** `metadata.name: allow-from-web1-netpol`. Immediately following `kubectl apply -f allow-from-web1-netpol.yaml` reports `networkpolicy.networking.k8s.io/nginx2-networkpolicy created`. **Boundary:** created object name mismatches YAML; no intermediate file edit in source; don't claim precise object state.

## F-03 — [Source wording/code mismatch] — logger echo namespace vs actual request
**p0616:** Pod shell loop emits `Querying Kubernetes API Server for Pods in default namespace...`, but its URL is `/api/v1/namespaces/rbac-demo-ns/pods` and Pod is created in `rbac-demo-ns`. **p0618:** observed log repeats default while output contains Pod from rbac-demo-ns. **Boundary:** human-readable message is inaccurate; the target namespace is determined by URI; not a demonstrated query of `default`.

## F-04 — [Source wording/code mismatch] — registry Secret encryption-at-rest
**p0638:** asserts that `kubectl create secret docker-registry` itself ensures security by **encrypting Secrets at rest**. **p0639:** command only supplies registry server/user/password/email, without any EncryptionConfiguration, KMS, etcd config or verification. **Boundary:** automatic encryption-at-rest cannot be inferred from creation command/source evidence. Actual encryption/RBAC **[Needs confirmation]**.

## F-05 — [Needs confirmation] — registry password exposed in process arguments
**p0639:** `--docker-password=your_password` placed directly on shell command line. **Boundary:** risk in history/process listing/automation logs; source placeholders not real credentials. Chapter does not demonstrate secure credential ingress, secret rotation or encrypted etcd [Needs confirmation]. Pod and Secret must share namespace (p0639 footnote).

## F-06 — [Needs confirmation] — JWT publication to third-party site
**p0598–p0599:** after `kubectl create token example-sa`, author suggests examining token on `https://jwt.io`. **Boundary:** chapter does not establish privacy or safe handling of an active bearer credential in an external website. Do not upload live JWT tokens as a study requirement; disclosure/revocation [Needs confirmation].

## F-07 — [Needs confirmation] — static authentication file and HA rollout
**p0593–p0595:** `--token-auth-file` CSV with all static tokens and restart required for changes/rotation, HA copies require sync. Authors explicitly discourage production use. **Boundary:** no secure lifecycle/rollback, and editing `/etc/kubernetes/manifests/kube-apiserver.yaml` is a control-plane change. Do not treat file as a production IdP.

## F-08 — [Needs confirmation] — SA TokenRequest history/Secret description
**p0592, p0595–p0597:** ServiceAccount tokens described as manually generated `Secret` or TokenRequest; since v1.22 projected short-lived tokens are contrasted with older static Secret tokens. **Boundary:** exact version and TokenRequest configuration of target cluster are not shown. No actual token lifetime/rotation or revocation test in book.

## F-09 — [Source extraction issue] — spacing in source command
**p0595:** `kubectl get pods/ <имя_пода> -o yaml` with whitespace after slash is printed as one suggested command. **Boundary:** source's spacing makes exact executability unclear, not silently repaired in commands list. Demonstrated `kubectl auth whoami` has v/version note (p0600).

## F-10 — [Needs confirmation] — exposure of kubeconfig credentials
**p0603:** `kubectl config view -o json | jq '.users[]'` shows a user token field `REDACTED` and file paths to client cert/key. **p0599/p0605:** `config set-credentials` writes token or private certificate paths. **Boundary:** don't archive/unredact real kubeconfig or tokens, and don't assume safe previous context restoration from output without noting it; key storage [Needs confirmation].

## F-11 — [Needs confirmation] — certificate signing/revocation
**p0604–p0605:** `openssl genrsa`, `openssl req`, CSR to `kubernetes.io/kube-apiserver-client`, `kubectl certificate approve`, signed cert file. **p0606:** certificate revocation is listed as a benefit. **Boundary:** no actual revocation, rotation or certificate lifetime control is demonstrated; admin approval and key secrecy remain necessary. **[Needs confirmation]**.

## F-12 — [Needs confirmation] — OIDC issuer trust/certificate requirement
**p0608–p0610:** external OIDC provider required, discovery/TLS/CA and flags; **p0609** describes CA TRUE flag even for IdP's certificate as broadly required. **Boundary:** no IdP certificate inspection or live API server issuer integration, so the exact operational trust condition and current support **[Needs confirmation]**.

## F-13 — [Needs confirmation] — admission plugin listing and obsolete entries
**p0622–p0623:** sample uses `--enable-admission-plugins` for specific minikube and lists older names `PodSecurityPolicy`, `DenyEscalatingExec`, `SecurityContextDeny`, `AlwaysAdmit`, `AlwaysDeny`. Some are labelled deprecated by source, others not. **Boundary:** cannot assume all names available/enabled for source's or current cluster version. Source does not test disabling or upgrading these flags; control-plane recovery **[Needs confirmation]**.

## F-14 — [Needs confirmation] — API-server admission change automatically restarts it
**p0622:** editing static `kube-apiserver.yaml` triggers kubelet to recreate API Pod. **Boundary:** this is a high-impact instruction; no HA failover, backup of flags, admission audit or safe undo documented. Control plane availability after arbitrary edits **[Needs confirmation]**.

## F-15 — [Source wording/code mismatch] — privileged containers in hardening subsection
**p0624–p0625:** least privilege advocated, then `CAP_NET_ADMIN` and `privileged: true` showcased under Pod protection. **Boundary:** these examples **increase** privileges and should not be copied as default hardening; source warns about risks for privileged mode, without giving compensating safeguards.

## F-16 — [Needs confirmation] — nginx non-root/read-only Pod readiness
**p0627–p0628:** Pod `security-context-demo` uses `nginx:latest`, UID/GID 1000, rootfs read-only, with writable `emptyDir`. **p0628:** `id` and failed `touch /testfile` shown. **Boundary:** confirms specific process identity and blocked root write; it does not prove nginx readiness, image tag immutability or total filesystem immutability. **[Needs confirmation]**.

## F-17 — [Needs confirmation] — CNI support and existing minikube
**p0629:** `minikube start --network-plugin=cni --cni=calico --container-runtime=containerd` provided to enable policies, but no negative test of CNI policy enforcement without plugin, no cluster teardown. **Boundary:** starting/recreating minikube may alter an existing profile; compatibility/rollback for target environment **[Needs confirmation]**.

## F-18 — [Source wording/code mismatch] — illustration caption misaligned
**p0629:** NetworkPolicy explanation shows traffic isolation between Pod. **p0630** caption for Fig. 18.8 says a Pod is down but Service keeps forwarding traffic to it. **Boundary:** source text and figure caption do not establish the same claim; cannot infer network-policy behavior from that caption alone.

## F-19 — [Needs confirmation] — TLS/mTLS full-link guarantees
**p0634–p0636:** mTLS example covers API server↔etcd, Ingress↔Service, service mesh and load balancers; some passages describe full-path encryption in a configured architecture. **Boundary:** no TLS configuration, certificate testing, Ingress backend, trust rotation, IPSec or end-to-end packet verification is performed. Actual full-path guarantee **[Needs confirmation]**.

## F-20 — [Needs confirmation] — gVisor/Kata isolation/performance claim
**p0636–p0638:** strong isolation claims and minimal Kata performance penalty; only example `runtimeClassName: kata-containers`. **Boundary:** handler installation, RuntimeClass API object, sandbox compatibility, benchmark and workload readiness **not demonstrated**; don't promise escape-proof isolation or no overhead.

## F-21 — [Needs confirmation] — NetworkPolicy default-deny scope
**p0632:** `default-deny-ingress.yaml` has `podSelector: {}`, no namespace metadata, and applied using `-n web2`. **p0633:** blocked `curl` from source nginx1. **Boundary:** applies to all selected Pods in **web2**, not an entire cluster. No proof of deny egress, host traffic, DNS or other namespaces. A timed-out curl isn't comprehensive security acceptance.

## F-22 — [Source wording/code mismatch] — Role and namespace of Kubernetes users
**p0592:** ordinary users are global while ServiceAccounts are namespaced; **p0614:** Role/ClusterRole and bindings differ in scope. **Boundary:** existence of a namespaced SA does not prevent other ClusterRoleBindings from granting broader rights; the tested limited rights apply only to the example's RBAC configuration. No inventory of other bindings in the target cluster **[Needs confirmation]**.

**No source adjudication or environment mutation:** no cluster commands executed. Canonical PDF, RAG, registry, metadata and reading status unchanged.
