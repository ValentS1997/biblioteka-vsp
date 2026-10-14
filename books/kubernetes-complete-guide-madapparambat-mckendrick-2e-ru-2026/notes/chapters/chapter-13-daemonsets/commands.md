# Commands and manifests — глава 13 DaemonSet

**Source:** только RAG PDF 457–473, `p0457:c01`–`p0473:c01`. Демонстрационные команды не исполнялись. Классы: read-only observation; local/cluster state-changing; workload-generating; destructive; sensitive access. Все namespace и условия должны подтверждаться до выполнения.

## Read-only / diagnostics

| Команда в книге | Эффект и интерпретация | PDF |
|---|---|---:|
| `kubectl get nodes` | read-only: 3 узла учебного minikube | 461 |
| `kubectl get daemonsets -A` | read-only: DESIRED/CURRENT/READY, все namespace; calico-node и kube-proxy | 461 |
| `kubectl get po -n kube-system -o wide \| grep calico` | read-only: сопоставить Pod Calico и NODE | 461 |
| `kubectl describe daemonset fluentd-elasticsearch -n logging` | read-only: ожидаемый DaemonSet; **namespace не совпадает с YAML** | 465 |
| `kubectl get po -n logging -o wide` | read-only: Fluentd Pod и Node в примере, но namespace mismatch | 465 |
| `kubectl describe ds -n logging` | read-only: DaemonSet events, имя в команде не указано | 468 |
| `kubectl rollout status ds -n logging` | наблюдение обновления; проблема namespace по исходному манифесту | 468 |
| `kubectl describe ds -n kube-system kube-proxy` | read-only: пример системного DaemonSet | 470 |

Наблюдение `get`/ `describe` не создаёт Pod, однако может раскрыть системные IP, labels и события. `rollout status` может продолжительно ждать. Реальные имена Pod и IP автора нельзя переносить в чужой кластер.

## Local lab infrastructure — state-changing

p0460: многоузловой minikube с VirtualBox, Calico и containerd:
```bash
minikube start \
  --driver=virtualbox \
  --nodes=3 \
  --cni=calico \
  --cpus=2 \
  --memory=2g \
  --kubernetes-version=v1.31.0 \
  --container-runtime=containerd
```
**Effect:** creates/starts 3 local VMs and changes cluster context, CNI and resources. **Risk:** resource exhaustion, existing minikube profiles, incompatible driver/runtime and version. **Verification:** `kubectl get nodes`, `kubectl get daemonsets -A` (p0461). **Rollback:** chapter does not provide minikube shutdown/deletion steps; **[Needs confirmation]**. Do not run against a shared workstation profile without approval.

## Source manifest: Fluentd (contains an unresolved namespace conflict)

p0463 begins:
```yaml
# fluentd-daemonset.yaml, source excerpts combined p0463–p0465
apiVersion: v1
kind: Namespace
metadata:
  name: logging
---
apiVersion: apps/v1
kind: DaemonSet
metadata:
  name: fluentd-elasticsearch
  namespace: kube-system
  labels:
    k8s-app: fluentd-logging
spec:
  selector:
    matchLabels:
      name: fluentd-elasticsearch
  template:
    metadata:
      labels:
        name: fluentd-elasticsearch
    spec:
      containers:
        - name: fluentd-elasticsearch
          image: quay.io/fluentd_elasticsearch/fluentd:v4.7
          resources:
            limits:
              memory: 200Mi
            requests:
              cpu: 100m
              memory: 200Mi
          volumeMounts:
            - name: varlog
              mountPath: /var/log
          env:
            - name: FLUENT_ELASTICSEARCH_HOST
              value: "elasticsearch-logging"
            - name: FLUENT_ELASTICSEARCH_PORT
              value: "9200"
      terminationGracePeriodSeconds: 30
      volumes:
        - name: varlog
          hostPath:
            path: /var/log
```

**Important:** `metadata.namespace: kube-system` — буквальное значение source p0463, а p0465 затем выводит `kubectl describe ... -n logging` и три Pod `-n logging`. Нельзя считать этот YAML источником показанного вывода без объяснения отсутствующего изменения namespace. Файл представлен как **source excerpt, not authorized runnable configuration**. Root cause/repaired manifest [Needs confirmation].

```bash
kubectl apply -f fluentd-daemonset.yaml
kubectl describe daemonset fluentd-elasticsearch -n logging
kubectl get po -n logging -o wide
```
p0465. **Effect:** `apply` создаёт Namespace `logging` и DaemonSet в `kube-system` по YAML; `describe/get` инспектируют `logging`. **Risk:** непреднамеренное изменение системного namespace, дополнительная нагрузка на nodes, чтение хостовых журналов, публикация в непроверенный Elasticsearch и отсутствие видимости в ожидаемом namespace. **Verification:** не полагаться на выходные данные книги без согласования namespaces. **Rollback:** source uses deletion in `logging`, что **не** удалит DaemonSet `kube-system` по заявленному YAML; [Needs confirmation].

Книга пишет, что для production конфигурация Fluentd и Elasticsearch требует дополнительных настроек, в том числе целевого endpoint (p0464). Тест `Running` не подтверждает доставку логов.

## Sensitive access / diagnostic processes

p0465:
```bash
kubectl exec -n logging -it fluentd-elasticsearch-cs4hm -- /bin/bash
# inside container
ls -l /var/log/
```

**Effect:** запускает interactive shell внутри Pod, перечисляет каталоги смонтированного hostPath. **Risk:** раскрытие путей системных журналов, shell access с чувствительными правами; имя Pod из демонстрации и namespace не подтверждены. **Verification:** source показывает `calico`, `containers`, `journal`, `pods`. **Rollback:** exit from shell; никакой модификации в sample `ls` не предполагается, но эффект shell depends on operator actions.

## PriorityClass — cluster-scoped, state-changing

p0466:
```yaml
# priorityclass.yaml
apiVersion: scheduling.k8s.io/v1
kind: PriorityClass
metadata:
  name: fluentd-priority
value: 100000
globalDefault: false
description: "Fluentd Daemonset priority class"
```
Связь в шаблоне:
```yaml
spec:
  template:
    spec:
      priorityClassName: fluentd-priority
```

В разделе показан manifest и логика, но отдельная source команда `kubectl apply -f priorityclass.yaml` **не приведена** — не обозначать её как выполненный рецепт. **Effect if applied:** приоритет Pod может изменить scheduling/preemption других рабочих нагрузок во всём кластере. **Risk:** вытеснение приложений, деградация ресурсоёмких workload, конфликт с системными приоритетами. **Verification/rollback:** в главе нет отдельного исполняемого теста — [Needs confirmation].

## Update strategy and rollout — state-changing

p0467–p0468 source: заменить `image: quay.io/fluentd_elasticsearch/fluentd:v4.7` на `...:v4.7.5` в шаблоне. `RollingUpdate` — по умолчанию, `maxUnavailable` по книге default 1, `minReadySeconds` default 0. `OnDelete` требует ручного удаления Pod для применения нового шаблона.

```bash
kubectl apply -f fluentd-daemonset.yaml
kubectl rollout status ds -n logging
kubectl describe ds -n logging
```
**Effect:** rollout across eligible nodes, source output 2/3→3/3 updated. **Risk:** частичная потеря логирования или узлового агента, namespace mismatch, историческая версия образа, отсутствие проверенной готовности Elasticsearch. **Verification:** source `rollout status` success, `describe ds` events `SuccessfulDelete`/`SuccessfulCreate` (p0468). **Rollback:** `kubectl rollout undo daemonset fluentd-elasticsearch -n logging` (p0469); если объект создан в другом namespace, команда не адресует его. Restoration of logs/availability [Needs confirmation].

Императивный вариант обновления изображения `kubectl set image ds ...` в p0468 показан с разрывом строки внутри image repo; автор не рекомендует для production. Не преобразовывать обрезанный фрагмент в объявленно воспроизводимый production script.

## Deletion and drain caveat — destructive

p0469:
```bash
kubectl rollout undo daemonset fluentd-elasticsearch -n logging
kubectl delete ds fluentd-elasticsearch -n logging
kubectl delete ds fluentd-elasticsearch -n logging --cascade=orphan
```
**Classification:** first changes workload revision; second **deletes controller and its Pods**, third **deletes controller but leaves Pod orphaned**. Second/third are **mutually exclusive alternatives**, not sequential steps. **Risks:** cluster service disruption/log gaps and unmanaged Pod; in presence of namespace mismatch may delete the wrong object or return NotFound. **Verification:** inspect DaemonSet/Pod status in **correct verified namespace**. **Rollback:** no exact safe recreation/cleanup sequence in source.

p0469 notes `--ignore-daemonsets` requirement for `kubectl drain` involving DaemonSet Pod, but does **not** provide a full drain command/restore scenario; do not invent one.

## Monitoring exporter and alternatives — conceptual only

p0462 mentions a working `node-exporter.yaml` in external repository with `node-exporter` headless Service and `/metrics` at port 9100; the chapter RAG does **not** include the full manifest/CLI. Other examples include Calico/kube-proxy (p0461, p0470), Flannel/Ceph/ingress (p0470), Fluentd/Prometheus node-exporter (p0471). External repo content not consulted. **No execution claims**.

p0472–p0473 alternatives: sidecar, CronJob, operating-system daemon, static Pod; no complete commands in source.

## Operational boundary

Before running any action, verify `metadata.namespace`, Pod labels, eligible nodes, PriorityClass scope, image provenance, node log permissions, Service/Elasticsearch endpoint and actual rollout settings. Stage first; never change CNI/kube-proxy or shared DaemonSets for a learning exercise. Full test/rollback [Needs confirmation].
