# Глава 15. Запуск кластера на платформе Google Cloud Platform (GCP) с помощью Google Kubernetes Engine (GKE)

**Inventory:** `0033` · **book_id:** `kubernetes-complete-guide-madapparambat-mckendrick-2e-ru-2026` · **Edition:** второе, русское (2026) · **Chapter:** 15  
**Contract:** `BIBLIOTEKA-VSP-CHAPTER-ARTIFACT-COLLECTION v1.7` · **Source policy:** `rag_only`.

## Scope and provenance

- **Boundary VERIFIED:** PDF/печатные страницы **515–536**; заголовок p0515, «Резюме» и дополнительные источники p0536; глава 16 начинается с p0537. Оглавление RAG p0017:c01–p0018:c01.
- **Chapter RAG:** `kubernetes-complete-guide-madapparambat-mckendrick-2e-ru-2026:p0515:c01`–`kubernetes-complete-guide-madapparambat-mckendrick-2e-ru-2026:p0536:c01`; **22 адресных страницы** в `rag/chunks/p0501-p0600/p####-c01.md`. Source format PDF, EPUB spine Not applicable.
- **Canonical PDF:** `source/book.pdf`, SHA256 `380ccbfc9e0a65cb2e5aa67a671528c15b9ce6eac63ad9aab80b90f91b1e6e65`.
- **RAG:** `ACCEPTED`, `failed_checks: []`; corpus generation `9fa19b3d399c47de2b9feaf303a9b1895b354beaacda6cd44d100908d3c41842`, index generation `0a62c809aeded557e1ed8c79d306a4770a3fbf55f4f7436a47865879c1d84a44`.
- **Readiness:** prior book readiness CI `38394894818` PASS; current `main` acceptance and v1.7 contract checked. No new execution of readiness CLI claimed.
- **Evidence:** only chapter RAG. No direct PDF, external search/API validation, model-memory filling or live cloud resources. Unsupported facts **[Needs confirmation]**.

## Карта главы

| Тема | Страницы | Что рассматривается |
|---|---:|---|
| Введение и требования | 515–517 | GCP, GKE, история, облачный billing и предостережения по расходам |
| Учетная запись и проект | 517–519 | Trial credits из источника, Google Cloud Console, Project ID |
| Установка и инициализация gcloud | 519–523 | macOS, Windows, Linux, Cloud Shell, `gcloud init`, выбор проекта |
| Создание зонального кластера GKE | 524–526 | `container.googleapis.com`, auth plugin, `myfirstgkecluster`, 2 node в `us-central1-a` |
| Кубернетес-контекст | 525–527 | `get-credentials`, kubeconfig, `kubectl get nodes`, `use-context` |
| Guestbook PHP/Redis | 527–528 | Redis leader/follower и frontend: 3 Deployment, 3 Service; публичный LoadBalancer HTTP:80 |
| Google Cloud Console | 528–532 | Workloads, Events, Logs, YAML, Services/Ingress, Storage, Backup for GKE и Enterprise |
| Удаление / зоны и регионы | 533–535 | Remove Service/cluster, проверить «осиротевшие» ресурсы; zonal vs regional, `--node-locations` |
| Резюме / ссылки | 536 | Итоги и переход к Amazon EKS |

## Главный принцип

**GKE запускает и управляет кластером Kubernetes на ресурсах Google Cloud; клиент `gcloud` управляет GCP/GKE, `kubectl` — объектами внутри кластера** (p0516–p0527). В примере включается API GKE, устанавливается плагин аутентификации, создаётся кластер `myfirstgkecluster` с двумя узлами в одной зоне `us-central1-a`. `get-credentials` загружает параметры доступа в kubeconfig. Текущий контекст необходимо подтвердить перед применением Kubernetes-ресурсов.

**Guestbook** использует Redis leader/follower и PHP frontend. Три пары Deployment/Service создаются из URL `raw.githubusercontent.com`; в source внешний `frontend` Service создаёт балансировщик и публичный IP, тогда как Redis Service — внутренние `ClusterIP` (p0527–p0531). Содержимое удалённых манифестов вне chapter RAG, их безопасность/состояние сейчас **[Needs confirmation]**.

**География влияет на число узлов и стоимость.** `--num-nodes=2 --zone=us-central1-a` даёт **2 узла**; `--num-nodes=2 --region=us-central1` в учебном выводе разворачивает **2 узла на каждую из 3 зон = 6 узлов**; `--node-locations` с четырьмя зонами — **8 узлов** (p0533–p0535). Цены источника $55/$347 в месяц — исторические оценки, не актуальные тарифы. Multi-zone не доказывает измеренный SLO или automatic cross-zone state replication.

## Артефакты

- [cheatsheet.md](cheatsheet.md) — baseline, наблюдение, действие, проверка, удаление и rollback boundary.
- [commands.md](commands.md) — только исходные CLI и manifest URLs, эффекты/риски.
- [diagram.md](diagram.md) — GKE lifecycle, Guestbook, региональная topology, billing/cleanup.
- [visual-cheatsheet.svg](visual-cheatsheet.svg) — компактная визуальная карта.
- [visual-cheatsheet-detailed.svg](visual-cheatsheet-detailed.svg) — подробная визуальная карта.
- [summary.md](summary.md) — пересказ раздела «Резюме», p0536, сохранено значение источника.
- [source-findings.md](source-findings.md) — противоречия и ограничение воспроизводимости книги.

**Review questions/answers:** [Not applicable], отдельный раздел контрольных вопросов/упражнений отсутствует на pp515–536.

## Evidence index

- [GCP и GKE, p0516](../../../rag/chunks/p0501-p0600/p0516-c01.md)
- [Требования, платежи, p0515](../../../rag/chunks/p0501-p0600/p0515-c01.md)
- [Trial и аккаунт, p0518](../../../rag/chunks/p0501-p0600/p0518-c01.md)
- [Linux and Windows CLI, p0521](../../../rag/chunks/p0501-p0600/p0521-c01.md)
- [gcloud init, p0523](../../../rag/chunks/p0501-p0600/p0523-c01.md)
- [GKE API and cluster, p0524](../../../rag/chunks/p0501-p0600/p0524-c01.md)
- [Get credentials, p0526](../../../rag/chunks/p0501-p0600/p0526-c01.md)
- [Guestbook manifests, p0527](../../../rag/chunks/p0501-p0600/p0527-c01.md)
- [Frontend endpoint, p0528](../../../rag/chunks/p0501-p0600/p0528-c01.md)
- [Console Services, p0530](../../../rag/chunks/p0501-p0600/p0530-c01.md)
- [GKE services, p0532](../../../rag/chunks/p0501-p0600/p0532-c01.md)
- [Cleanup, p0533](../../../rag/chunks/p0501-p0600/p0533-c01.md)
- [Regional node counts, p0534](../../../rag/chunks/p0501-p0600/p0534-c01.md)
- [Costs and multi-zone, p0535](../../../rag/chunks/p0501-p0600/p0535-c01.md)
- [Summary, p0536](../../../rag/chunks/p0501-p0600/p0536-c01.md)

## Operational safety

Source requires a billing-enabled GCP account and cautions about charges (p0515). Source shows `curl | bash` and `choco install --ignore-checksum` as installation methods; not audited. Cloud project/zone/context, IAM, APIs, public HTTP endpoint, cleanup and cost controls **[Needs confirmation]**. `gcloud container clusters delete` is **destructive**; pre-delete backup, finalizer and resource inventory not supplied. No cloud resources or Kubernetes commands were executed. Do not modify PDF/LFS, RAG, registry, reading status/dates/progress.
