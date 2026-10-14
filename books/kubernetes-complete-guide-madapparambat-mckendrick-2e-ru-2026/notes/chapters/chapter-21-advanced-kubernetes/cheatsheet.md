# Cheatsheet — Глава 21: продвинутые возможности Kubernetes

**Source:** RAG-only PDF 705–749, `p0705:c01`–`p0749:c01`. Никаких Kubernetes, Azure, etcd или cloud операций не выполнялось.

## Symptom / problem framing
Требуется маршрутизировать HTTP-запросы по host/path, затем сопровождать кластер: создавать надёжные резервные копии, планировать обновления, проверять доступы и диагностировать неисправности (pp705–749).

## Baseline / context
- Multi-node Kubernetes + kubectl; для AGIC нужен AKS; для локального Ingress возможен minikube addon (p706).
- `Ingress` — API-правила L7, обработка требует контроллера. Source lab: `k8sbible.local` с `/video`, `/shopping` и `/` на 3 ClusterIP Services, **без TLS** (pp708–715). `IngressClass` выбирает контроллер.
- AGIC в AKS использует Azure Application Gateway, но создание и kubeconfig в книге указывают **разные имена кластеров** (p719).
- Gateway API использует `GatewayClass`, `Gateway`, `HTTPRoute`; примерный `controllerName` не обеспечен установленным контроллером (pp720–722).
- Day-2: etcd snapshots/restore, безопасное обновление управляющего слоя и узлов, IaC/CaC, multi-cluster, RBAC, audit, secrets encryption, troubleshooting (pp727–747).

## Read-only checks
```bash
kubectl get pods -n ingress-nginx
kubectl get po,svc,ingress -n ingress-demo
kubectl get IngressClass -o yaml
kubectl get nodes
kubectl get deployments
kubectl describe deployment webapp
kubectl get events
kubectl get events --field-selector involvedObject.name=todo-pod
kubectl logs todo-app
kubectl logs todo-app --previous
kubectl explain pod.spec
kubectl get pv
kubectl get pvc
kubectl top nodes
kubectl auth can-i <глагол> <ресурс>
```
Source pp712–717, 739–747. Это запросы чтения API, но вывод logs/events/config может раскрывать внутренние данные. Работающие права и назначение namespace [Needs confirmation].

## Interpretation
**Ingress troubleshooting:** controller Running → Service существует → IngressClass разрешает контроллеру обрабатывать правила → DNS/host совпадает → нужный backend/service port (pp712–716). В p708 YAML host указан, а p709 текст говорит, что host не используется. Без исправления рассогласования нельзя считать правила универсальными.

**Gateway:** класс, слушатель и HTTPRoute определены как схема, но Gateway Controller не установлен в главе. EndpointSlice уменьшает объём обновлений адресов Pod (pp720–724).

**etcd:** p728 записывает `/tmp/snapshot-pre-patch.db`, а `etcdutl snapshot status` и `snapshot restore` обращаются к `snapshot.db` (pp728–729). Это **разные имена без переименования**, так что восстановление не проверено. Snapshots содержат чувствительное состояние, требуют защиты.

**Upgrade:** подготовка, проверка совместимости, snapshot, `drain`, control plane first, workers/CNI, `uncordon`, post-upgrade checks. Возможен простой и потери, rollback требует репетиции (pp730–732).

**Troubleshooting:** Pending → events/node requests; CrashLoop → logs/previous; Service/Ingress → ports, selectors и endpoint; PVC Pending → PV, PVC, StorageClass; API outage → смотреть состояние управляющего слоя на узле (pp739–747).

## Next action
Сначала уточнить context, namespace, контроллеры, DNS, TLS и SLO; для etcd/upgrade — backup/restore план, владельцев, RPO/RTO, согласование и проверку в staging. Исходные команды AGIC и etcd нельзя запускать как единую подтверждённую последовательность.

## Modifying action
```bash
minikube start --cni calico --nodes 3 --kubernetes-version=v1.31.0
minikube addons enable ingress
kubectl apply -f ingress/
kubectl drain <освобождаемые_узлы> --ignore-daemonsets
kubectl uncordon <имя-узла>
kubectl debug -it pod/video-7d945d8c9f-wkxc5 --image=quay.io/iamgini/k8sutils:debian12 -c k8sutils -n ingress-demo
```
pp712–714, 731, 744. **State-changing:** создание Pod/Ingress, возможно выселение рабочих Pod, запуск эфемерного debug-контейнера в Pod. **Risk:** disruption, небезопасное HTTP, доверие к образу, не тот namespace. **Verification:** `get pods/ingress/nodes`, запросы к 3 путям, debug nslookup/curl. **Rollback:** chapter не даёт безопасного полного undo для этих операций [Needs confirmation].

**etcd snapshot/restore:** p728–729 описывает `etcdctl snapshot save` и `etcdutl snapshot status/restore`, но имена файлов **расходятся**, так что нельзя воспроизводить как готовый runbook. Restore меняет каталог данных etcd и требует согласованного управления API серверами; резервная копия, шифрование и проверка целостности обязательны.

## Verification / acceptance checks
Источник показывает nginx controller Running, 3 Pod/Services и Ingress, пути `/video`, `/shopping`, `/`; пример эфемерного debug контейнера успешно обращается к video-service (pp712–715,744–745). Gateway controller, TLS, backup restore, upgrade, security audit и cloud teardown живыми тестами не подтверждены.

## Rollback
`kubectl uncordon` разрешает размещение после операции drain, **не возвращает предыдущую версию Kubernetes**. Для Ingress/AGIC, etcd restore, ephemeral containers, облачных ресурсов и upgrade восстановление/удаление **[Needs confirmation]**. Никакой команды не исполнялось.
