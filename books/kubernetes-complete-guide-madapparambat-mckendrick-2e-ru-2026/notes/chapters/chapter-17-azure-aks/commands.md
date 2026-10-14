# Commands — Глава 17, Microsoft Azure / AKS

**Source:** only chapter RAG PDF pp561–586, `p0561:c01`–`p0586:c01`. No commands were executed. Preserve source operation, classify risk, avoid invented runbooks.

## Azure CLI setup: local changes and read-only

| Source CLI | Classification / operational effect | PDF |
|---|---|---:|
| `brew install azure-cli` | local state-changing, macOS package installation; trust/current support [Needs confirmation] | 565 |
| `az --version` | read-only local version check | 565–569 |
| `curl -L https://aka.ms/InstallAzureCli \| bash` | **remote code execution** for Linux; integrity and rollback [Needs confirmation] | 566 |
| `source ~/.profile` | current-shell environment change (reload profile), not a cloud resource | 566 |
| `choco install azure-cli` | privileged local Windows software install | 566 |
| `az login` | interactive browser authentication, writes a local CLI session | 567 |
| `az login --use-device-code` | authentication with device code; credential handling needed | 567 |
| `az account show` | read-only signed-in account/subscription summary; may disclose IDs | 567 |

Windows p566 also gives a PowerShell downloader of `AzureCLI.msi` with `Invoke-WebRequest`, `Start-Process msiexec.exe`, `Remove-Item`: **local file writes, privileged installer execution and cleanup**. It is not reproduced as a one-click recommendation. Script/download hash/supplier metadata unknown [Needs confirmation]. Azure Cloud Shell is an alternative to local install (p567–p569).

Cloud Shell p567–p569: Portal → Cloud Shell → `Mount storage account` → select subscription → `We will create a storage account for you`. **GUI state-changing and potentially billable**: creates/attaches storage to retain files/kubeconfig. Source says `az login` is unnecessary inside Cloud Shell, as it authenticates on shell startup. Access controls, storage charges, credential protection [Needs confirmation].

## Cluster creation: Azure resources and kubeconfig

```bash
az group create --name rg-myfirstakscluster-eus --location eastus -o table
```

p0569. **Class:** Azure resource state-changing; creates a resource group in `eastus`. **Risk:** accidental wrong subscription, naming collisions and inherited permissions/locks. **Verification:** source table output confirms group; target subscription must be checked separately (`az account show`, p567). **Rollback:** `az group delete --name rg-myfirstakscluster-eus` (p582) is **destructive for all group resources**, not safe for a shared group; prior inventory/backup [Needs confirmation].

```bash
az aks create --resource-group rg-myfirstakscluster-eus \
  --name aksmyfirstakscluster-eus --node-count 2 \
  --enable-addons monitoring --generate-sshkeys -o yaml
```

p0570. **Class:** billable, workload-generating/cloud state-changing. **Effect:** AKS cluster with two worker VMs, Azure monitoring addon, generated SSH keys and YAML output; in source location inherited from RG `eastus`, VM default `Standard_DS2_v2` (historical, 2 vCPU, 7 GiB). **Risk:** VM/network/log analytics charges, credentials/SSH private key creation, subscription and portal access, no tested production admission or network policy. **Verification:** successful source output p0571, `kubectl get nodes`; Azure Portal Kubernetes services list (p0573). **Rollback:** `az aks delete` p0582 removes cluster but not RG; no app data restore and actual cloud teardown [Needs confirmation].

Optional alternative source p0583:
```bash
az aks create --resource-group rg-myfirstakscluster-eus \
  --name aksmyfirstakscluster-eus --node-count 2 \
  --enable-addons monitoring --generate-sshkeys \
  --node-vm-size standard_ds3_v2 -o yaml
```

**Class:** alternative billable cluster creation, **not sequentially after the first `az aks create` with identical name**. **Effect:** source estimates two 4-vCPU/16GiB VM at lower historical rate in non-production tier; **risk:** current SKU availability and actual charges unverified, [Needs confirmation]. **Verification/rollback:** analogous, with explicit cleanup and no backup in source.

```bash
az aks get-credentials --resource-group rg-myfirstakscluster-eus \
  --name aksmyfirstakscluster-eus
kubectl get nodes
```

p0571. **Class:** `get-credentials` changes **local kubeconfig and active cluster configuration**, `get nodes` read-only API. **Risk:** inadvertently targeting wrong cloud cluster, leaked auth material. **Verification:** 2 nodes from source; prior kubeconfig context and safe restoration [Needs confirmation].

## Guestbook via unpinned remote YAML

p0572 has six `kubectl apply -f` invocations (PDF line wrapping unambiguously normalized):
```bash
kubectl apply -f https://raw.githubusercontent.com/GoogleCloudPlatform/kubernetes-engine-samples/main/quickstarts/guestbook/redis-leader-deployment.yaml
kubectl apply -f https://raw.githubusercontent.com/GoogleCloudPlatform/kubernetes-engine-samples/main/quickstarts/guestbook/redis-leader-service.yaml
kubectl apply -f https://raw.githubusercontent.com/GoogleCloudPlatform/kubernetes-engine-samples/main/quickstarts/guestbook/redis-follower-deployment.yaml
kubectl apply -f https://raw.githubusercontent.com/GoogleCloudPlatform/kubernetes-engine-samples/main/quickstarts/guestbook/redis-follower-service.yaml
kubectl apply -f https://raw.githubusercontent.com/GoogleCloudPlatform/kubernetes-engine-samples/main/quickstarts/guestbook/frontend-deployment.yaml
kubectl apply -f https://raw.githubusercontent.com/GoogleCloudPlatform/kubernetes-engine-samples/main/quickstarts/guestbook/frontend-service.yaml
kubectl get service frontend
```

**Class:** six state-changing calls creating three Deployment + Service pairs; last is read-only. **Effect:** Redis Leader/Follower and PHP frontend, public Azure frontend LoadBalancer/external IP in author's output. **Risks:** mutable `main` branch, external manifest contents not in RAG and not reviewed, public **HTTP without certificate** (p0573), billable IP/LB, wrong kubeconfig context and unclear data retention. **Verification:** `kubectl get service frontend` and browser `http://EXTERNAL-IP` (p0573), Portal Workloads/Services/Events/Live logs (pp574–578). **Rollback:** no source-tested separate `kubectl delete` for these six resources; cluster deletion is available but destructive and cannot serve as universal app rollback, [Needs confirmation].

## Azure Portal operations

p0573–p0582 describes **observational** portal pages: Kubernetes services; AKS Overview; Namespaces, Workloads (Deployments/Pods/ReplicaSets/StatefulSets/DaemonSets/Jobs/CronJobs), Services/ingresses, Storage, Configuration (ConfigMap/Secret), Custom resources, Events, Insights (Cluster/Reports/Nodes/Controllers/Containers). `Live logs` opens Pod logs; `Run command` executes `kubectl` server-side from portal, potentially **state-changing**. `Node pools` permits scaling/upgrading, `Cluster configuration` permits control plane upgrades, `Application scaling` KEDA sources; merely viewing tabs is read-only, initiating changes is not. Full corresponding CLI/YAML **not provided** in chapter — don't fabricate.

p0580 states update control plane before node pools and a general 3-release compatibility window; no upgrade was carried out in source and actual current AKS support matrix [Needs confirmation].

Monitoring enabled with `--enable-addons monitoring`, data visible through Azure Log Analytics / Azure Monitor Insights (p0581–p0582). Logging, retention, alert delivery, actual storage charges and backup restore [Needs confirmation].

## Destructive cleanup — different scopes

```bash
az aks delete --resource-group rg-myfirstakscluster-eus --name aksmyfirstakscluster-eus
az group delete --name rg-myfirstakscluster-eus
```

p0582. **Class:** destructive Azure control plane + node/workload teardown, then deletion of entire resource group with **all contained resources**. Source prompts `yes` twice. **Risk:** permanent app/data loss, wrong subscription, removal of shared resources, orphaned external costs, failure to recover destroyed cluster, no backup; **both actual targets must be inventoried**. **Verification:** command confirmation in source; it does not include post-delete resource inventory, price ledger or restore tests. **Rollback:** [Needs confirmation]. Do not treat `az group delete` as an innocuous substitute for `az aks delete`.

## Historical pricing and cloud comparison

p0583: two source `Standard_DS2_v2` nodes approximately **$213/month**, paid management tier total ~$286/month, alternative two `standard_ds3_v2` estimated ~$140/month in non-production. p0584 table compares GKE/EKS/AKS (version adoption, auto upgrades, ease, security, integrations, cost, multi-zone/private/serverless). These are **source-dated estimates and author assessments**, not fresh prices or universal platform capability claims. The claim in p0584 of a free GKE control plane is also distinct from chapter 15's specific historical GKE cost figures; differences in cluster tier/free allowance [Needs confirmation].

## Boundary

No local package installation, Azure login, Cloud Shell storage creation, Azure API, SSH generation, Kubernetes manifests or destructive commands executed. Read-only source checks are examples, **not live verification**; current provider pricing, version availability and security practices [Needs confirmation].
