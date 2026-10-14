# Cheatsheet — Глава 15: Google Cloud / GKE

**Provenance:** RAG PDF 515–536, `kubernetes-complete-guide-madapparambat-mckendrick-2e-ru-2026:p0515:c01`–`…:p0536:c01`. Никакие команды не выполнялись; актуальность облачных тарифов/API не проверена.

## Symptom / problem framing

Нужно получить управляемый Kubernetes-кластер в GCP, настроить `gcloud` и `kubectl`, развернуть Guestbook, проверить трафик через frontend Service и **полностью учесть расходуемые платные ресурсы**. GKE предоставляет кластер, но deployment, Service, контекст kubectl, контролируемая география и cleanup остаются ответственностью оператора (p0515–p0517, p0524–p0535).

## Baseline / context

- **Требования источника:** аккаунт GCP и способ оплаты; выделенный project ID; установленный `gcloud` либо Cloud Shell; Kubernetes context; права для включения API, кластеров, сетевых ресурсов (p0515, p0518–p0523). Фактические IAM, billing budget, квоты, region/zone — **[Needs confirmation]**.
- **Историческая акция:** $300 credits на 90 дней на момент написания книги (p0518), **не** обещание сегодняшнего бесплатного доступа.
- **Зональная лаборатория:** `myfirstgkecluster`, `--num-nodes=2`, `--zone=us-central1-a`, включён `container.googleapis.com`, установлен `gke-gcloud-auth-plugin` (p0524).
- **Контексты:** `gcloud container clusters create` в примере пишет kubeconfig; `get-credentials` нужен при другом `kubectl` (p0525–p0527). `kubectl config current-context` перед любыми действиями.
- **Гостевая книга:** 3 Deployment и 3 Service (redis-leader, redis-follower, frontend); фронтенд с публичным балансировщиком HTTP:80, Redis только ClusterIP (p0527–p0531).
- **Региональная topology:** `--num-nodes=2 --region=us-central1` в источнике даёт **6 узлов** по 2 на 3 зоны; конфигурация 4 зон даёт **8 узлов** (p0534–p0536).

## Read-only checks

```bash
gcloud version
kubectl config current-context
kubectl config get-contexts -o name
kubectl get nodes
kubectl get service frontend
```

RAG p0520–p0522, p0525–p0527. `gcloud version` — local read-only; `kubectl config` показывает текущую цель и может раскрыть названия кластеров; `get nodes` и `get service` читают API. Консоль: Workloads (Pod/Deployment/Events/Logs), Services (External LoadBalancer vs ClusterIP), Storage, Backup for GKE (p0528–p0532). Консольный вывод иллюстративен, не текущий снимок.

## Interpretation

- Два `gke-...` узла после создания доказывают наличие двух объектов Node в выбранном кластере (p0525–p0526), но не доступность Guestbook и не наличие достаточных прав на ресурсы.
- `kubectl get service frontend`: публичный EXTERNAL-IP появляется **после** provision балансировщика; в книге используют `http://EXTERNAL-IP` на 80, не HTTPS (p0527–p0528). Это небезопасный публичный транспорт для секретных/боевых данных.
- `frontend` имеет внешний Service, `redis-leader`/`redis-follower` внутренние (p0530–p0531). Внешний LoadBalancer создаёт платный облачный ресурс — cleanup необходим.
- `--num-nodes=2` для regional означает **per-zone в демонстрации**, а не два узла всего: 2 × 3 = 6 (p0534). Четыре `--node-locations` при 2 на зону → 8 (p0534–p0536). Не путать с текущими стандартами провайдера: они не проверены.
- Оценки **$55/месяц и $347/месяц** относятся к моменту написания и указанным профилям (p0535); нынешние тарифы, сетевые/дисковые расходы и кредиты не подтверждены.

## Next action

До создания определить проект, billing account, бюджет/лимиты, регион, число зон, IAM, размер узлов, expected LoadBalancer cost, процедуру завершения. Проверить и зафиксировать kubeconfig context, одобрить источник внешних manifests. После lab заранее запланировать удаление и проверить остаточные ресурсы в консоли (p0515, p0533).

## Modifying action (source-supported; DO NOT execute in production without approval)

```bash
gcloud init
gcloud config set project PROJECT_ID
gcloud services enable container.googleapis.com
gcloud components install gke-gcloud-auth-plugin
gcloud container clusters create myfirstgkecluster --num-nodes=2 --zone=us-central1-a
gcloud container clusters get-credentials myfirstgkecluster --zone=us-central1-a
kubectl config use-context CONTEXT_NAME
```

p0522–p0527. **Effects:** local login/project/context changed, API enabled, client plugin installed, billable GKE cluster + nodes created, kubeconfig credentials changed. **Risks:** не тот project/context, IAM scope, billable resources, overwrite kubeconfig assumptions. **Verification:** `kubectl config current-context`, `kubectl get nodes`, Google Cloud Console (p0525–p0526). **Rollback:** source shows deletion of **zonal** cluster, but cannot guarantee recovery of local context or cost refunds — **[Needs confirmation]**.

Guestbook (p0527): source uses six `kubectl apply -f https://raw.githubusercontent.com/GoogleCloudPlatform/kubernetes-engine-samples/main/quickstarts/guestbook/...` for deployment+service of redis-leader, redis-follower, frontend. **Effect:** create workloads and public external Service. **Risk:** mutable `main` manifests unreviewed; cloud billing, public HTTP; current SHA/content unknown. **Verification:** `kubectl get service frontend`, browser `http://EXTERNAL-IP` as source (p0528). **Rollback:** source deletes `service frontend` then cluster; complete manifest and storage/dependency cleanup **[Needs confirmation]**.

## Verification / acceptance checks

- `gcloud version` shows CLI; `kubectl config current-context` targets **intended** GKE cluster (p0522–p0527).
- `kubectl get nodes` shows two gke-named nodes in zonal lab (p0526).
- Guestbook deployments Redis leader/follower/frontend visible in console Workloads; three Services, frontend external with public IP (p0529–p0531).
- Guestbook HTTP loads and accepts test entries in the book (p0528); not proof of HTTPS, public security, data persistence or SLO.
- After teardown confirm expected cluster gone and orphan resources absent in console (p0533). Real AWS/GCP pricing and API state not verified.

## Rollback / cleanup

```bash
kubectl delete service frontend
gcloud container clusters delete myfirstgkecluster --zone=us-central1-a
```

p0533. **Destructive**: removes the public load balancer resource (subject to reconciliation), then deletes the zonal cluster/workloads. Region-based sample uses `gcloud container clusters delete myfirstgkecluster --region=us-central1` (p0535) — **alternative, not sequential with zonal deletion**. **Risk:** permanent workload/data loss, orphaned resources, ongoing charges; source recommends cloud-console audit (p0533). No validated data backup or guarantee of cleanup of every billable asset — **[Needs confirmation]**. Do not infer current resource state from textbook output.

## Boundaries

Unattended execution of `curl ... | bash` or `choco install --ignore-checksum` is not advised: package/download content not validated in source RAG (p0521). Accounts, project ID, credentials and tokens are not available and must not be fabricated. No state changes in Git except chapter artifacts.
