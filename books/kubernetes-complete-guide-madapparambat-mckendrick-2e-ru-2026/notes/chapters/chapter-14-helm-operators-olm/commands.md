# Commands and manifests — Chapter 14: Helm, Operators and OLM

**Strict source:** RAG PDF **474–514**, chunks `p0474:c01`–`p0514:c01`. Commands are textual evidence, **not executed**. Classify: observation, local configuration, cluster-mutating, destructive, privileged, remote-code execution, secret disclosure. Do not assume source URLs still deliver the same content.

## Helm installation and package discovery

| Book command | Class / effect | PDF |
|---|---|---:|
| `sudo dnf repolist | grep fedora` | local observation of Fedora repository | 477 |
| `sudo dnf install helm` | privileged local package installation | 478 |
| `choco install kubernetes-helm` | local software installation on Windows | 478 |
| `brew install helm` | local package installation on macOS | 478 |
| `helm version` | read-only version observation | 478–479 |
| `wget https://get.helm.sh/helm-v3.15.1-linux-amd64.tar.gz` | network download of historical binary | 479 |
| `tar -zxvf helm-v3.15.1-linux-amd64.tar.gz` | extracts files locally | 479 |
| `sudo mv linux-amd64/helm /usr/local/bin/helm` | privileged install/overwrite binary | 479 |
| `helm repo add stable https://charts.helm.sh/stable` | modifies local Helm repo config; book calls old stable deprecated | 479 |
| `helm search repo stable | grep -i deprecated | head` | reads repo metadata, terminal pipeline | 480 |
| `helm search hub wordpress` | remote package discovery | 480 |
| `helm repo add bitnami https://charts.bitnami.com/bitnami` | local repo configuration, trust required | 482 |

Book versions differ by installation platform (3.11, 3.15 release-candidate, 3.16.2); they are **historical outputs**, not current recommendations. **Verification:** `helm version`; trust of downloaded binary not established [Needs confirmation]. No universally safe rollback of installed CLI given.

## WordPress: Helm release and manifest values

```bash
kubectl create ns wordpress
helm install wp-demo bitnami/wordpress -n wordpress --values wp-values.yaml
helm install wp-demo bitnami/wordpress --dry-run --debug
helm install my-wordpress bitnami/wordpress --version 22.4.2
helm list -n wordpress
kubectl get po -n wordpress
kubectl get statefulsets.apps -n wordpress
kubectl get svc -n wordpress
minikube service --url wp-demo-wordpress -n wordpress
```

Source p0482–p0486. **State effects:** `create ns` changes cluster, `helm install` creates Service/Deploy/StatefulSet/PVC/Secrets for WordPress+MariaDB and can expose NodePort, `dry-run --debug` reads/renders manifests and can expose sensitive values to logs; `helm list/get` observe. **Verification:** source `wp-demo` release status deployed, WordPress and MariaDB Pod Running, MariaDB StatefulSet 1/1, NodePort returned. **Risk:** vulnerable chart, external exposure and database persistence, resource cost, historical repository paths/versions. **Rollback:** `helm uninstall wp-demo -n wordpress` explicitly shown (p0487), but PVC/PV retention and data restoration **[Needs confirmation]**.

Source `wp-values.yaml` includes `wordpressUsername`, `wordpressPassword`, `wordpressEmail`, names and `service.type: NodePort`, `volumePermissions.enabled: true` (p0482). **Do not copy the source's demo password into Git or a shell command.** Minimal non-secret structural illustration only:
```yaml
service:
  type: NodePort
volumePermissions:
  enabled: true
```

`helm install ... --set wordpressUsername=wpadmin` appears p0482. `--set` can pass secrets in process args if misused; the source uses it for username only. `helm install --dry-run --debug` on p0484 omits `-n wordpress` and `--values wp-values.yaml`, so it does **not** render the identical desired configuration as the actual install: flagged in findings.

`helm uninstall wp-demo -n wordpress` (p0487): **destructive**, can make website/database unavailable, PVC/PV may remain. Do not delete remaining volumes until backup/reclaim verified; source does not provide recovery.

## Helm chart structure (source conceptual, not a CLI recipe)

```text
wordpress/
  Chart.yaml
  values.yaml
  values.schema.json    # optional
  charts/               # optional dependencies
  crds/                 # optional CRDs
  templates/
    deployment.yaml     # Go templating: {{ .Values.replicaCount }}
    NOTES.txt           # optional post-install instructions
  README.md
  LICENSE               # optional
```

p0487–p0489. Source `Chart.yaml` depends on `mariadb` and optionally `memcached`, `mariadb.enabled: true` by default (p0488). `helm upgrade` is introduced in the book but no complete WordPress upgrade+rollback command sequence is shown; don't invent a fully supported migration.

## Dashboard: high-privilege exercise, not production instructions

Source p0489:
```bash
helm repo add kubernetes-dashboard https://kubernetes-retired.github.io/dashboard/
helm upgrade --install kubernetes-dashboard kubernetes-dashboard/kubernetes-dashboard --create-namespace --namespace kubernetes-dashboard
kubectl get pod -n kubernetes-dashboard
```

**Effect:** local Helm repo config and cluster-wide app installation; may create Services/Ingress and RBAC. URL is *exact source* and its current operation has not been checked. p0490–p0491 show ServiceAccount `admin-user` in `kubernetes-dashboard` and **ClusterRoleBinding `roleRef.name: cluster-admin`**. Source then:
```bash
kubectl apply -f dashboard-sa.yaml
kubectl apply -f dashboard-rbac.yml
kubectl -n kubernetes-dashboard create token admin-user
kubectl -n kubernetes-dashboard port-forward svc/kubernetes-dashboard-kong-proxy 8443:443
```

**CRITICAL:** This issues a credential with **cluster-admin** privileges. The actual bearer token is not reproduced. Binding can grant full administrative rights; URL/local port-forward can expose privileged UI to local users. Source suggests ignoring self-signed certificate warnings (p0492), which is **not** a validated TLS trust mechanism. **Verification:** Pod Running, local https://localhost:8443 and login in source. **Rollback:** no complete cleanup/credential revocation sequence presented; **[Needs confirmation]**. Do not execute without explicit security review.

## OLM installation / subscription (remote-code and cluster-wide effects)

p0502 source:
```bash
curl -sL https://github.com/operator-framework/operator-lifecycle-manager/releases/download/v0.28.0/install.sh | bash -s v0.28.0
```
**REMOTE-CODE EXECUTION**. Avoid executing uninspected remote code; target URL, checksum, privileges, script behavior, admission policies and teardown [Needs confirmation]. This exact command is **reference only**, not an endorsed action.

```bash
kubectl get pods -n olm
kubectl get csv -n olm
kubectl get packagemanifests | grep prometheus
kubectl create -f https://operatorhub.io/install/prometheus.yaml
kubectl get csv -n operators
kubectl get pods -n operators
kubectl create -f https://operatorhub.io/install/grafana-operator.yaml
kubectl get crd
```

p0503–p0504. `get` operations are observational. **Both `kubectl create -f https://...` commands mutate the cluster from uninspected remote manifests, create Subscriptions/operators/CRDs and RBAC, potentially with cluster-wide effects**. Need source/review/signature/namespace admission controls; complete cancellation/rollback [Needs confirmation]. Book OLM check: packageserver CSV `Succeeded` in namespace `olm`; Prometheus Operator CSV shown in `operators`, versions source-specific. One `operatorhubio-catalog` Pod `0/1 Running` in source: do not interpret all components as Ready.

## Prometheus/Grafana CR instances, monitoring

```yaml
# prometheus-instance.yaml, p0505
apiVersion: monitoring.coreos.com/v1
kind: Prometheus
metadata:
  name: example-prometheus
  namespace: monitoring
spec:
  replicas: 2
  serviceAccountName: prometheus
  serviceMonitorSelector:
    matchLabels:
      app.kubernetes.io/name: node-exporter
```

```yaml
# grafana-instance.yaml, p0505–p0506, sensitive fields REDACTED
apiVersion: grafana.integreatly.org/v1beta1
kind: Grafana
metadata:
  name: grafana-a
  namespace: monitoring
  labels:
    dashboards: grafana-a
    folders: grafana-a
spec:
  config:
    auth:
      disable_login_form: 'false'
    log:
      mode: console
    security:
      admin_user: "[Needs confirmation]"
      admin_password: "[Needs confirmation]"
```

Source p0506 embeds demo admin credentials **plaintext**; the snippet above is intentionally **redacted** and thus **not runnable**. Production requires a secret-management design [Needs confirmation].

```bash
kubectl apply -f monitoring-ns.yaml
kubectl apply -f monitoring-sa.yaml
kubectl apply -f prometheus-instance.yaml
kubectl apply -f grafana-instance.yaml
kubectl get pod,svc,sts -n monitoring
kubectl apply -f node-exporter-daemonset.yaml
kubectl apply -f node-exporter-svc.yaml
kubectl apply -f servicemonitor-instance.yaml
```

p0505–p0507. **Effect:** creates namespace, RBAC, custom Prometheus/Grafana resources, node-exporter DaemonSet/Service, ServiceMonitor. **Risk:** cluster-wide CRDs and monitoring access, missing example files from RAG, demo credentials, privileges/capacity. **Verification:** Pod/Service/StatefulSet outputs on p0506; source screenshot p0508 shows targets. **Rollback:** no complete tested uninstall/cleanup, PVC retention and data recovery [Needs confirmation]. The ServiceMonitor full YAML isn't present in chapter source, so label compatibility unverified.

## Local port-forwards and Grafana UI

```bash
kubectl port-forward -n monitoring svc/prometheus-operated 9091:9090
kubectl port-forward -n monitoring service/grafana-a-service 3000:3000
```

p0508. These open **local listeners** (not public ingress), terminate with Ctrl+C. Browser routes: `http://localhost:9091/targets`, `http://localhost:3000` (p0508–p0509). Grafana datasource source URL `http://prometheus-operated.monitoring.svc.cluster.local:9090` (p0510); import `Node Exporter Full` from Grafana dashboard library (p0510–p0513). **Risk:** Grafana credential exposure and incorrectly configured datasource, image/compatibility and dashboard third-party trust [Needs confirmation].

## Verification and rollback boundary

Successful source outcome: Helm release visible; WordPress/MariaDB running; OLM packageserver CSV Succeeded; Prometheus operator CSV/POD present; Prometheus (2 pods, StatefulSet), Grafana Pod, node-exporter and ServiceMonitor; browser charts. But data durability, true alerting, disaster recovery, SLO, current install URL safety, least privilege, removal of subscriptions/CRDs and persistence **not demonstrated**. `helm uninstall` is **not** a guaranteed cleanup of PVC/PV; service account token + cluster-admin binding requires an approved credential revocation mechanism not supplied in source.
