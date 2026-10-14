# Commands — Глава 15: GCP / Google Kubernetes Engine

**RAG-only:** PDF 515–536, chunks `p0515:c01`–`p0536:c01`. Не выполнять учебные команды без authorization, approval бюджета и проверки текущего `gcloud` project/`kubectl` context. Все выводы в книге исторические; инструменты и URL не проверялись в сети.

## Client installation (local state changes)

| Команда из книги | Effect / risk | PDF |
|---|---|---:|
| `brew install --cask google-cloud-sdk` | устанавливает SDK в macOS; package integrity [Needs confirmation] | 520 |
| `brew info --cask google-cloud-sdk` | read-only package metadata | 520 |
| `choco install --ignore-checksum gcloudsdk` | **security risk:** локальная установка без проверки checksum | 521 |
| `curl https://sdk.cloud.google.com | bash` | **remote-code execution:** запускает загруженный сценарий в Linux; не исполнять без проверки | 521 |
| `exec -l $SHELL` | заменяет локальный shell session для PATH | 521 |
| `gcloud version` | read-only версия установленного клиента; также в Cloud Shell | 520–522 |

На p0521 приведён установщик Chocolatey через PowerShell, выполняющий скачанный скрипт; воспроизводить код удалённого bootstrap без проверки поставщика и контрольной суммы нецелесообразно. Все эти действия могут изменить локальную рабочую станцию. Rollback CLI установки в RAG не дан **[Needs confirmation]**.

## Account, project, authentication and Kubernetes context

```bash
gcloud init
gcloud config set project PROJECT_ID
```

p0522–p0523. `gcloud init` запускает авторизацию и выбор проекта; `config set project` меняет локальный активный project. **Effect:** cloud credentials/configuration and target of later GCP operations. **Risk:** создание платных ресурсов в ошибочном проекте, доступ к учётной записи. **Verification:** текст предлагает подтвердить выбранный уникальный Project ID в терминале (p0523), отдельной read-only команды показа проекта в source нет; **[Needs confirmation]**. **Rollback:** предыдущая конфигурация не приводится, [Needs confirmation]. Не подставлять придуманные Project ID.

```bash
gcloud services enable container.googleapis.com
gcloud components install gke-gcloud-auth-plugin
```

p0524. **Effect:** включение API GKE в активном проекте, установка auth plugin. **Risk:** разрешения/биллинг/API policy и изменение CLI. **Verification:** последующая попытка создания кластера и получение kubeconfig (p0524–p0526). **Rollback:** деактивация API / удаление плагина в источнике не предусмотрены — [Needs confirmation].

```bash
gcloud container clusters create myfirstgkecluster --num-nodes=2 --zone=us-central1-a
kubectl get nodes
```

p0524–p0526. **CLASS: BILLABLE, INFRASTRUCTURE STATE-CHANGING.** Создаёт кластер в одной зоне с 2 nodes; CLI сообщает о добавлении kubeconfig entry. **Risk:** ongoing cloud charges, wrong project/zone, IAM, GKE version defaults not specified, networking/storage costs, public endpoints depending defaults. **Verification:** `kubectl get nodes` выводит два node с префиксом `gke`. **Rollback:** source command `gcloud container clusters delete myfirstgkecluster --zone=us-central1-a` (p0533), destructive; no restore [Needs confirmation].

```bash
gcloud container clusters get-credentials myfirstgkecluster --zone=us-central1-a
kubectl config current-context
kubectl config get-contexts -o name
kubectl config use-context CONTEXT_NAME
```

p0526–p0527. **Class:** `get-credentials` mutates kubeconfig credentials/context; `current-context`/`get-contexts` read local config; `use-context` switches local target. **Risk:** accidental application of resources to wrong cluster and stored credentials; **verification:** current-context and `get nodes`. **Rollback:** old context must be known explicitly and is not given — [Needs confirmation].

## Guestbook — source URL manifest application

p0527 gives these **six** source manifest paths; the actual remote content is **not included** in chapter RAG and must be reviewed before application.

```bash
kubectl apply -f https://raw.githubusercontent.com/GoogleCloudPlatform/kubernetes-engine-samples/main/quickstarts/guestbook/redis-leader-deployment.yaml
kubectl apply -f https://raw.githubusercontent.com/GoogleCloudPlatform/kubernetes-engine-samples/main/quickstarts/guestbook/redis-leader-service.yaml
kubectl apply -f https://raw.githubusercontent.com/GoogleCloudPlatform/kubernetes-engine-samples/main/quickstarts/guestbook/redis-follower-deployment.yaml
kubectl apply -f https://raw.githubusercontent.com/GoogleCloudPlatform/kubernetes-engine-samples/main/quickstarts/guestbook/redis-follower-service.yaml
kubectl apply -f https://raw.githubusercontent.com/GoogleCloudPlatform/kubernetes-engine-samples/main/quickstarts/guestbook/frontend-deployment.yaml
kubectl apply -f https://raw.githubusercontent.com/GoogleCloudPlatform/kubernetes-engine-samples/main/quickstarts/guestbook/frontend-service.yaml
kubectl get service frontend
```

**Class:** first six state-changing (Deployment/Service creation); last read-only. **Effects:** Redis Leader/Follower and PHP frontend; frontend Service gets EXTERNAL-IP through provisioned cloud LoadBalancer; internal Redis Services use ClusterIP (p0529–p0531). **Risks:** unpinned mutable `main` URLs, supply-chain drift, internet-exposed endpoint over **HTTP not HTTPS**, compute/load-balancer fees and unreviewed permissions. **Verification:** external address, `http://EXTERNAL-IP`, Guestbook messages shown in source (p0528); console Workloads shows three deployments and Services lists public frontend + internal Redis (p0529–p0531). **Rollback:** only source's frontend Service deletion and full cluster removal, not a granular 6-manifest reversal, [Needs confirmation]. Current accessibility not asserted.

## Console checks (manual, non-CLI)

p0528–p0532: Google Cloud Console → Kubernetes Engine → Workloads (Overview, Details, Observability, Revision History, Events, Logs, App Errors, YAML); Gateways, Services and Ingress (Services tab); Secrets and ConfigMaps; Storage, Object Browser, Backup for GKE and Marketplace. Some panes can show sensitive data, and Backup for GKE is described as **separate service**, not an automatically enabled safety net.

## Zonal vs regional examples — billable

```bash
gcloud container clusters create myfirstgkecluster --num-nodes=2 --region=us-central1
kubectl get nodes
```

p0534. Source output: **2 nodes per zone × default 3 zones = 6 nodes**. **Effect:** creates regional cluster, billable and potentially higher cost; **risk:** p0524 sample already used same cluster name in a zone; source does not show guaranteed removal before trying same name, preflight [Needs confirmation]. **Verification:** `kubectl get nodes`, six nodes in book. **Rollback:** `gcloud container clusters delete myfirstgkecluster --region=us-central1`, destructive (p0535).

```bash
gcloud container clusters create myfirstgkecluster \
  --num-nodes=2 \
  --region=us-central1 \
  --node-locations us-central1-a,us-central1-b,us-central1-c,us-central1-f
```

p0534. **Effect:** creates a new regional cluster using 4 specified zones, 2 nodes/zone → 8 total in source. **Risk:** expenses, quota, zone availability, network/storage charges; rollback delete regional (p0535), no data restore.

```bash
gcloud container clusters update myfirstgkecluster \
  --min-nodes=2 \
  --region=us-central1 \
  --node-locations us-central1-a,us-central1-b,us-central1-c,us-central1-f
```

p0535. **Effect:** alters an existing regional cluster's node locations / node settings, potentially changes node footprint. **Risk:** source uses `--min-nodes=2` whereas earlier `create` uses `--num-nodes=2`, semantics not explained; cannot assert exact scaling from field alone, **[Needs confirmation]**. **Verification:** `kubectl get nodes` after operation, source figure shows nodes spread across four zones. **Rollback:** reverting node locations not provided, [Needs confirmation].

**Historical price estimates:** source p0535 states approximately **$55/month** for 2-node zonal cluster and **$347/month** for 8-node example. Those are not up-to-date quotes; billing includes other resources and varies by conditions [Needs confirmation].

## Destructive cleanup — essential cloud cost control

```bash
kubectl delete service frontend
gcloud container clusters delete myfirstgkecluster --zone=us-central1-a
```

p0533. **Class: destructive / billable infrastructure teardown.** `delete service` removes external frontend exposure/cloud LoadBalancer subject to reconciliation; `delete cluster` destroys zonal cluster, Node/workloads and possibly stored state. **Risk:** irreversible data deletion; some chargeable resources may remain. **Verification:** source explicitly recommends inspect Google Cloud Console for **orphaned services/resources** after removal. **Rollback:** no restore/backup procedure, [Needs confirmation]. Do not run on real project without resource inventory and approval.

```bash
gcloud container clusters delete myfirstgkecluster --region=us-central1
```

p0535: alternative for regional cluster, **not** to be run after zonal command as one recipe. **Risk/verification/rollback:** as above, with correct region and project required.

## Unsupported claims

Chapter does not show current GKE version availability, active billing costs/free credits, GitHub `main` manifest integrity, real account IAM, data durability, SLA measurements, cross-zone Redis replication, backup restores or security policy. Preserve **[Needs confirmation]**. No live testing was performed.
