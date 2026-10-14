# Cheatsheet — Глава 14. Helm и Kubernetes Operators

**Source:** RAG-only PDF **474–514**, `kubernetes-complete-guide-madapparambat-mckendrick-2e-ru-2026:p0474:c01`–`…:p0514:c01`. Commands not executed. No external source validation.

## Problem / symptom

Многокомпонентные приложения требуют согласованного развёртывания, конфигурации и зависимостей. Kubernetes YAML по отдельности неудобны для переиспользования; Helm объединяет шаблоны в charts. Сложные stateful workflows требуют непрерывной прикладной reconciliation — это задача operators (p0474–p0477, p0495–p0498).

## Baseline

- Рабочий `kubectl`, Kubernetes cluster (в книге для minikube рекомендованы 4 vCPU и 8 GiB), локальный Helm CLI; target kubeconfig/namespace, RBAC, storage class, internet access **[Needs confirmation]** (p0474–p0475).
- Термины: **chart** = пакет YAML/Go templates; **repository** = источник chart; **release** = установленный экземпляр; **values.yaml** = значения по умолчанию, overridden `--values`/`--set` (p0476, p0482, p0487).
- **Helm 3** по книге не требует кластерного Tiller (p0477). Версии Helm 3.11, 3.15, 3.16.2 в примерах — разные исторические платформы, не проверенная current support (p0478–p0479).
- Example WordPress release `wp-demo`, namespace `wordpress`, chart `bitnami/wordpress`, WordPress + MariaDB, Service NodePort (p0482–p0486).
- **Helm security gate:** не добавлять/не устанавливать непроверенный chart; проверять dependency tree, manifests, RBAC, image/version, secrets, PV retention (p0479, p0484, p0494).
- **Operator model:** custom resource via CRD → app-specific controller reconciliation → Deployments/StatefulSets/PVC/Services; OLM CatalogSource/Subscription/CSV manages operator lifecycle (p0495–p0504).

## Read-only and offline first

```bash
helm version
helm search hub wordpress
helm search hub | head
helm search repo stable | grep -i deprecated | head
helm list -n wordpress
kubectl get po -n wordpress
kubectl get statefulsets.apps -n wordpress
kubectl get svc -n wordpress
kubectl get pod -n kubernetes-dashboard
kubectl get pods -n olm
kubectl get csv -n olm
kubectl get packagemanifests | grep prometheus
kubectl get csv -n operators
kubectl get pods -n operators
kubectl get crd
kubectl get pod,svc,sts -n monitoring
```

RAG p0478–p0480, p0484, p0486, p0490, p0503–p0506. `helm search hub` queries remote catalog, `helm search repo` uses configured repository metadata; `kubectl get` reads API. No guarantee named repo/operator exists in target environment. `helm install ... --dry-run --debug` is proposed on p0484, **but output can contain Secrets**; avoid logs/artifacts leaking sensitive generated resources.

## Interpretation

- `helm list -n wordpress` shows release `wp-demo`, status deployed and revision 1 in source. Deployment/StatefulSet/Service belong to release, but Pod readiness and successful web login need separate check (p0483–p0486).
- `helm uninstall wp-demo -n wordpress` (p0487) is **destructive**, yet source warns PV/PVC may remain. Do not equate uninstall with full cleanup or safe retention of data.
- Dashboard Pod Running (p0490) does not authorize access; source demonstrates `admin-user` SA and `cluster-admin` ClusterRoleBinding (p0491), unsafe for production. Local port-forward `8443:443` (p0491) and bearer token constitute sensitive access. Source suggests browser certificate warning bypass (p0492), **not** security verification.
- OLM `kubectl get csv -n olm` `Succeeded` for packageserver (p0503) vs Prometheus Operator CSV in `operators` (p0504) distinguishes OLM itself from operator readiness. Source shows a `0/1 Running` catalog Pod (p0503), so not every component proven Ready.
- Prometheus CR has `replicas: 2` and `serviceMonitorSelector.app.kubernetes.io/name: node-exporter`, Grafana CR uses custom `kind: Grafana` (p0505–p0506). Matching of ServiceMonitor labels is not visible because files live outside chapter RAG — **[Needs confirmation]**.
- Successful `get pod,svc,sts` and `/targets` view (p0506–p0508) show demo resources/metrics, **not** verified HA/SLO, backup, retention or cluster-wide coverage.

## Next action — safe workflow

Identify trust and package versions; inspect chart templates and values, especially any embedded credentials, privileged workloads and retention. Confirm namespaces, RBAC, storage provisions, resource requests and expected services. For operators inspect CRDs/CSV, desired resource schema, managed namespaces, cluster-scoped API mutations, update channel, reconciliation logic. Only then approve deployment in isolated test cluster. Current compatibility and policy **[Needs confirmation]**.

## Modifying actions and side effects

```bash
helm repo add bitnami https://charts.bitnami.com/bitnami
kubectl create ns wordpress
helm install wp-demo bitnami/wordpress -n wordpress --values wp-values.yaml
helm upgrade --install kubernetes-dashboard kubernetes-dashboard/kubernetes-dashboard --create-namespace --namespace kubernetes-dashboard
kubectl apply -f monitoring-ns.yaml
kubectl apply -f monitoring-sa.yaml
kubectl apply -f prometheus-instance.yaml
kubectl apply -f grafana-instance.yaml
kubectl apply -f node-exporter-daemonset.yaml
kubectl apply -f node-exporter-svc.yaml
kubectl apply -f servicemonitor-instance.yaml
```

Source p0482–p0483, p0489, p0505–p0507. **Effect:** local repo configuration, namespaces and cluster resources; dashboard and operator-related deployments can require broad permissions, chart dependencies create database/PVC. **Risks:** password exposure, external NodePort, storage cost, cluster-admin access, CRDs cluster-wide, provider compatibility. **Verification:** `helm list`, `get pod/svc/sts`, CSV status, Prometheus `/targets` and Grafana datasource `Save & test`. **Rollback:** `helm uninstall` demonstrated only for WordPress; no complete rollback for CRDs/operators/PVC or monitoring stack — [Needs confirmation].

**Prohibited as automatic execution:** source p0502 `curl -sL .../install.sh | bash -s v0.28.0` downloads and executes arbitrary network content with system/cluster effects; source p0503–p0504 `kubectl create -f https://operatorhub.io/install/prometheus.yaml` and Grafana counterpart apply remote manifests. All require independent source verification, review and authorization; none performed.

**High-privilege:** source Dashboard `ClusterRoleBinding` binds `admin-user` to `cluster-admin`; token creation is credential issuance. Do not copy/administer bearer tokens casually, print them to logs or enable a production Dashboard with these example permissions.

## Verification / acceptance

1. WordPress: namespace resources created, MariaDB StatefulSet `1/1`, WordPress Pod `1/1`, NodePort reachable only after confirmed network access (p0483–p0486). Historical node IP/port in source is not target address.
2. Helm: `helm list` release `deployed`; `Chart.yaml` dependencies (MariaDB) and template `{{ .Values.replicaCount }}` observed in source (p0487–p0489).
3. OLM: packageserver CSV `Succeeded`, operators available in `operators` namespace and CRDs registered (p0503–p0504).
4. Monitoring: two Prometheus pods (StatefulSet), Grafana, node-exporter and ServiceMonitor, targets visible in Prometheus `http://localhost:9091/targets`, datasource `http://prometheus-operated.monitoring.svc.cluster.local:9090`, dashboard import (p0506–p0513).
5. Production acceptance: RBAC, supply-chain signatures, encrypted secrets, storage/reclaim, complete rollout/DR and current API-version tests **[Needs confirmation]**.

## Rollback / stop

- Stop port-forwards with Ctrl+C (p0508); do not mistake this for deletion of exposed components or bearer tokens.
- `helm uninstall wp-demo -n wordpress` deletes managed release resources but source says PVC/PV not automatically removed; actual resource retention must be inventoried before action (p0487).
- No safe undo for the OLM installer, remote Subscription, CRDs, `cluster-admin` binding, grafana admin password, persistent database or dashboards supplied in RAG. **[Needs confirmation]**, do not improvise `kubectl delete` on cluster-scoped resources.
