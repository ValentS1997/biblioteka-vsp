# Cheatsheet — Глава 17: Microsoft Azure / AKS

**Source:** RAG-only PDF pp561–586, `p0561:c01`–`p0586:c01`. No Azure/cloud/Kubernetes commands executed; current prices and package support [Needs confirmation].

## Symptom / problem framing

Нужны управляемый кластер AKS и инструменты Azure CLI/Cloud Shell, чтобы применить переносимые Kubernetes-манифесты Guestbook, инспектировать приложение в Azure Portal и полностью прекратить расходы после лабораторного занятия. Источник подчёркивает, что облачные ресурсы тарифицируются (p0561) и все действия должны быть направлены на верную подписку, группу ресурсов и Kubernetes context.

## Baseline / context

- Azure account **с платёжным способом**; subscription ID, IAM/RBAC, лимиты, бюджет, доступный VM size и текущая цена **[Needs confirmation]** (p0561, p0564–p0565).
- Source free-trial $200 credit and 12 months (p0564) — **исторический маркетинговый пример, не текущая гарантия**.
- Azure CLI: macOS `brew install azure-cli`, Linux installer `curl -L https://aka.ms/InstallAzureCli | bash`, Windows .msi, PowerShell или `choco install azure-cli`; доверие к installer binary не проверялось (p0565–p0567).
- Authentication: `az login` or `az login --use-device-code`, inspect `az account show`. Cloud Shell starts authenticated but may **create a storage account** to persist configuration between sessions, with potential cost and data impact (p0567–p0569).
- Lab resource group: `rg-myfirstakscluster-eus`, location `eastus`; AKS cluster: **`aksmyfirstakscluster-eus`**, 2 nodes; monitoring addon; `--generate-sshkeys` (p0569–p0571).
- **Source name mismatch:** p0573 says portal cluster `aks-myfirstakscluster-eus` (extra hyphen) versus CLI `aksmyfirstakscluster-eus` on p0570–p0571. Do not silently substitute or claim both resolve (see findings).

## Read-only checks

```bash
az --version
az account show
kubectl get nodes
kubectl get service frontend
```

p0565–p0569, p0571–p0573. `az --version` local observation, `az account show` identifies signed-in Azure account/subscription and can reveal subscription metadata, Kubernetes `get` reads cluster objects. Source does not give `kubectl config current-context` as a chapter command; verify target kubeconfig through the `az aks get-credentials` output and independent approval. Adding a familiar command as source evidence would violate RAG-only.

Azure Portal read-only *when viewing*: Kubernetes services → cluster, Namespaces (p0574), Workloads and Live logs (pp575–577), Services and ingresses (p0577), Storage/Configuration/Custom resources/Events (p0578), Nodes/Node pools (p0579), Insights (pp581–582). **Run command** in Portal (p0578) is *capable of writing cluster state*, not intrinsically read-only.

## Interpretation

- A resource group is a *logical grouping*, not the cluster itself; policies/locks/RBAC can be associated at group scope (p0569–p0570). **Deleting the group later can delete unrelated resources**.
- `az aks create` with `--node-count 2` produces 2 workers in this lab; book's default VM size `Standard_DS2_v2` (2 vCPU, 7 GiB per VM) and pricing are historical, not verified available now (p0570, p0583).
- `--enable-addons monitoring` sends cluster metrics/logs to Azure Log Analytics/Insights in this source (p0581); **not** proof that logs are retained for a given period, backups exist or Azure Monitor alerts are configured.
- `az aks get-credentials` mutates local `kubeconfig` and therefore future `kubectl` target. `kubectl get nodes` confirms the currently configured access to a cluster (p0571).
- Guestbook Deployment/Service resources applied from unpinned `raw.githubusercontent.com/.../main` URLs (p0572); frontend receives **external IP, public HTTP**, no SSL certificate (p0573). Redis Services internal, but the full manifest source is outside chapter RAG. Do not assume TLS/proper credential policy.
- Source says its default workload namespace is `default`, storage unused, and system ConfigMap/Secret resources should **not** be changed (pp574,578).
- Version upgrade described as **control plane before node pools** (p0579–p0580), and "3-release backward compatibility" is an unverified book claim, not an unconditional policy for all versions.

## Next action

Confirm target account/subscription and names, quota, zone/location, cluster auth and activity, resource group dedicated ownership, monthly cost ceiling, monitoring/Log Analytics billing, generated SSH keys and backup scope. For the Guestbook demo, review pinned manifests before application, avoid production data on unauthenticated public HTTP and confirm cleanup coverage. Current Azure defaults and safety **[Needs confirmation]**.

## Modifying action — source workflow only

```bash
az login
az group create --name rg-myfirstakscluster-eus --location eastus -o table
az aks create --resource-group rg-myfirstakscluster-eus \
  --name aksmyfirstakscluster-eus --node-count 2 \
  --enable-addons monitoring --generate-sshkeys -o yaml
az aks get-credentials --resource-group rg-myfirstakscluster-eus \
  --name aksmyfirstakscluster-eus
```

pp0567, 0569–0571. **Effect:** credentials/session; billable Azure group, AKS/VMs/monitoring and possibly generated SSH private key; kubeconfig changes. **Risk:** wrong subscription, data exposure, resource charges, collisions, future kubectl targeting wrong cluster. **Verification:** `az account show`, `kubectl get nodes`, Azure Portal. **Rollback:** source deletes AKS cluster then resource group; destructive and safe only in verified disposable group (p0582).

Guestbook is applied using six source URLs for redis-leader, redis-follower, frontend, each Deployment and Service (p0572); full URLs and classification in [commands.md](commands.md). All are **cluster-state-changing**; do not apply unreviewed mutable remote YAML as an unattended workflow. **Verification:** `kubectl get service frontend`, portal Workloads/Services, HTTP browser (p0573). **Rollback:** source provides only deletion of entire AKS/group, not independently tested Guestbook-only removal [Needs confirmation].

## Verification / acceptance checks

- Azure CLI returns version, `az account show` shows intended subscription (pp0565–0569).
- Azure Resource Group `rg-myfirstakscluster-eus` and AKS `aksmyfirstakscluster-eus` show created state, `kubectl get nodes` returns two nodes (pp0569–0572).
- Guestbook accessible at source example's public `http://EXTERNAL-IP` (p0573); this does **not** prove TLS, authentication, SLA, persistent data or disaster recovery.
- Azure Portal `Live logs` and `Insights` show data in the author's demo (pp0576,0581–0582), not proof of functioning future alert rules.
- After tear-down inspect AKS resource deletion and whether group/children are removed; source **does not supply a CLI/portal receipt for zero remaining charges**, [Needs confirmation].

## Rollback / destructive cleanup

```bash
az aks delete --resource-group rg-myfirstakscluster-eus \
  --name aksmyfirstakscluster-eus
az group delete --name rg-myfirstakscluster-eus
```

p0582; both prompt for `yes`. **Mutually different scopes, not equivalent operations.** First deletes AKS cluster, **not the group**. Second deletes the **entire resource group** (potentially every service/resources within). **Risk:** irreversible workloads, monitoring/storage artifacts and unrelated assets. **Verification:** source instructs cleanup to avoid bills, but does not demonstrate verified backup/restore or post-delete inventory. **Rollback:** no recovery instructions [Needs confirmation]. Don't run on non-disposable group.

**Costs:** source p0583 estimates ~$213/month for two `Standard_DS2_v2`, ~$286/month with a standard paid management tier, alternative ~$140/month for two `standard_ds3_v2` in non-production. These are **historical illustrative figures** and the source's product/pricing claims aren't externally validated. Third-party/public CloudFront etc not inferred.
