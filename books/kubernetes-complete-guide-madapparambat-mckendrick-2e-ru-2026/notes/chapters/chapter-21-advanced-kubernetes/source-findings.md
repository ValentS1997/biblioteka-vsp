# Source findings — Глава 21. Продвинутые возможности Kubernetes

**Policy:** RAG-only p0705:c01–p0749:c01; original PDF 705–749. Classification: [Source contradiction], [Source code mismatch], [Source wording/code mismatch], [Source extraction issue], [Needs confirmation]. Never silently rewrite source variants or use external/model-memory corrections.

## F-01 — [Source contradiction] — Ingress host specified vs described as absent
**p0708:** Ingress YAML explicitly sets `spec.rules[0].host: k8sbible.local`; **p0709:** prose says "В нашем примере оно не используется" and rule applies to all incoming traffic. **Boundary:** explicit host is not absence of host. Host-matching behavior as claimed in prose does not follow from given manifest. Source's own p0713 again uses `k8sbible.local`.

## F-02 — [Source wording/code mismatch] — Ingress API fields old vs v1
**p0708:** networking.k8s.io/v1 backend uses `service.name` and `service.port.number`; **p0710:** text refers to `serviceName` / `servicePort`. **Boundary:** two source representations cannot be called the same YAML API schema. Do not make source command "working" by editing without verified spec.

## F-03 — [Source extraction issue] — malformed blog backend indentation
**p0713:** path `/` has `port:` followed by `number: 8080` at the same/incorrect indentation level. **p0708:** /video and /shopping backend correctly nest `number`. **Boundary:** the printed blog fragment is not a verified valid YAML object. Separate repo manifest bytes [Needs confirmation].

## F-04 — [Needs confirmation] — ingress-nginx versus NGINX Inc Controller
**p0710:** source names F5 Nginx Ingress Controller with f5.com URL; **p0711:** instructions and specific YAML reference community `kubernetes/ingress-nginx` `controller-v1.11.2`. **Boundary:** sources describe potentially distinct distributions/projects under similar names without clarifying equivalence. Runtime support, current maintenance and migration [Needs confirmation].

## F-05 — [Needs confirmation] — historical ingress-nginx retirement note
**p0710 footnote:** cites a plan to close a project in 2026 and migrate to Gateway API, with 2025/11/11 blog URL. **Boundary:** this is the book's historical editorial note; we have **not** checked the current project lifecycle or replacement support. Do not claim present-day status solely from this URL.

## F-06 — [Needs confirmation] — mutable/external controller manifests
**p0711:** `kubectl apply -f https://raw.githubusercontent.com/kubernetes/ingress-nginx/controller-v1.11.2/.../deploy.yaml` for cloud and aws, capable of creating namespace/RBAC/LoadBalancer. **Boundary:** URLs not fetched, image integrity/version and current behavior unverified; cloud billing/RBAC blast radius [Needs confirmation]. Not a production endorsement.

## F-07 — [Source code mismatch] — AGIC resource names
**p0719 prose:** new AKS `k8sforbeginners-aks-agic` in Resource Group `k8sforbeginners-rg`; **p0719 create CLI:** `--resource-group myResourceGroup --name myAKSCluster`; **p0719 get-credentials:** `--resource-group k8sforbeginners-rg --name k8sforbeginners-aks-agic` claims merged kubeconfig for the latter. **Boundary:** an uninterrupted transcript with no intervening rename cannot support the stated outcome. Extremely important: wrong cluster/context and billable cloud resources.

## F-08 — [Source code mismatch] — AGIC gateway name and source directory
**p0719 create CLI:** `--appgw-name MyAppGateway`; **p0719 prose:** created `AksApplicationGateway`. **p0719 prose:** copied directory `aks_agic` but YAML heading `aks-agic/portal-ingress.yaml`; apply command uses `aks_agic/`. **Boundary:** gateway/resource/working-directory values differ and are not reconciled.

## F-09 — [Source code mismatch] — AGIC Ingress result from wrong namespace
**p0719:** AGIC source Ingress `portal-ingress` and namespace `agic-demo`; **p0720:** `kubectl get ingress` without `-n agic-demo` displays `example-ingress` CLASS `<none>`, HOSTS `*`, instead of named `portal-ingress` with class `azure-application-gateway`. **Boundary:** this is not verification that the just-applied `portal-ingress` is functioning.

## F-10 — [Needs confirmation] — GatewayClass without controller implementation
**p0721:** `spec.controllerName: example.net/gateway-controller`, **p0722:** `dev-gateway` and `dev-httproute` refer to it. **Boundary:** no matching controller is installed/configured; CRDs, reconciler, readiness and endpoint routing [Needs confirmation]. Treat YAML as conceptual, not a working Gateway.

## F-11 — [Source wording/code mismatch] — Gateway vs Ingress backend ports and folder
**p0708/713:** video Service backend at port `8080`; **p0722:** HTTPRoute to `video-service` at port `80`. Also `gateway-api/gateway_api/gateway.yaml` versus `gateway-api/httproute.yaml`/GatewayClass example. **Boundary:** source does not show changing video Service port or clarifying nested folder. Cross-example reference is not an operable one-to-one migration without validation.

## F-12 — [Source code mismatch] — etcd backup file names differ
**p0728:** `etcdctl ... snapshot save /tmp/snapshot-pre-patch.db`; **p0728:** `etcdutl --write-out=table snapshot status snapshot.db`; **p0729:** `etcdutl --data-dir <...> snapshot restore snapshot.db`. **Boundary:** save/inspect/restore use different names and source contains no rename/copy. Production recovery **MUST NOT** follow this transcript uncritically. Restore correctness [Needs confirmation].

## F-13 — [Needs confirmation] — etcd snapshot zero-performance-impact claim
**p0728:** author states taking live snapshot has no impact on etcd performance. **p0727–729:** discusses copying sensitive entire cluster state but gives no benchmark. **Boundary:** no measured performance, storage throughput, snapshot latency, disk-space, consistency with PVs, or restore drill [Needs confirmation]. Treat assertion as source viewpoint only.

## F-14 — [Needs confirmation] — restore / multi-control-plane coordination
**p0729:** stop **all** API servers, restore etcd data, update `--etcd-servers`/load balancer, restart control plane components. **Boundary:** no evidence of executed multi-node recovery or consistent data restoration; fatal if applied to wrong etcd member/cluster. Source recommends encryption but no verified backup encryption/storage/rotation.

## F-15 — [Needs confirmation] — upgrade plan without actual run
**p0731–732:** backup, `kubectl drain ... --ignore-daemonsets`, apt/yum, kubeadm and kubelet update, `uncordon` and CNI check; **p0732:** admits etcd/API changes can make downgrade difficult. **Boundary:** no concrete version pins, PDB evaluation, canary test, completed upgrade or rollback command. Do not call it a fully validated zero-downtime runbook.

## F-16 — [Source wording/code mismatch] — exec namespace omitted
**p0742:** `kubectl get po -n trouble-ns` locates Pod `blog-675df44d5-gkrt2` in `trouble-ns`, but `kubectl exec blog-675df44d5-gkrt2 -- env` omits namespace. **p0743:** later `exec ... -n trouble-ns` is explicit. **Boundary:** p742 command may act on default namespace; not the demonstrated workload unless context's namespace matches [Needs confirmation].

## F-17 — [Source wording/code mismatch] — ephemeral debugging said to not change configuration
**p0744:** `kubectl debug -it pod/video-... --image=... -c k8sutils -n ingress-demo` adds an ephemeral container via special API. **p0745:** says no change to existing configuration. **Boundary:** the Pod's `ephemeralContainers` subresource is changed, so this is **state-changing debugging**, not a read-only query. Cleanup not demonstrated.

## F-18 — [Needs confirmation] — unencrypted HTTP examples and security advice
**p0715:** Ingress endpoints shown over HTTP with no TLS certificate in demo; **p0735/738:** security recommends TLS. **Boundary:** chapter explicitly warns production requires certificates; no HTTPS certificate issuance or successful TLS test. Do not call sample production-secure.

## F-19 — [Needs confirmation] — audit policy concept vs working cluster config
**p0740:** calls audit logs Policy type and describes API-request history; **p0737:** illustrates `--audit-log-path` and `--audit-policy-file` flags in kube-apiserver, without actual valid policy file or rollout. **Boundary:** audit-log security and retention cannot be assumed enabled. Setting static API server flags risks control-plane disruption [Needs confirmation].

## F-20 — [Needs confirmation] — Secret encryption at rest is configuration-dependent
**p0737:** recommends EncryptionConfig in kube-apiserver to protect secrets in etcd. **Boundary:** no EncryptionConfig YAML, KMS key security, re-encryption of old records, or audit/verification. This is a recommended control, not evidence that the target cluster already encrypts Secrets.

## F-21 — [Source wording/code mismatch] — mis-scoped troubleshooting action
**p0745–746:** network problem section suggests `kubectl describe pod` and `kubectl get svc` to diagnose NetworkPolicy; these commands can illuminate symptoms, but they do not themselves verify effective CNI policy/rule evaluation. **Boundary:** proposed read-only checks do not prove a NetworkPolicy is correct; external traffic and actual enforcer behavior [Needs confirmation].

## F-22 — [Needs confirmation] — terminal "no current state" boundary
**p0748–749:** chapter ends with further reading and publisher/book recommendations; p0751 onward advertises other books. **Boundary:** source chapters conclude on p749; external URLs and afterword/ads are not evidence of a current Kubernetes release, installed tooling, prices or live status. No new chapter 22.

**Non-interference:** no direct PDF, outside research, executable cloud/cluster/etcd actions, source/registry mutations or reading status updates.
