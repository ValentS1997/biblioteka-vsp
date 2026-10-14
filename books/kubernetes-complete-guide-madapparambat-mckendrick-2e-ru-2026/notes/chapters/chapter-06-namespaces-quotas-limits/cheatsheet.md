# Cheatsheet — Глава 6. Namespace, ResourceQuota и LimitRange

**Source:** RAG PDF/printed p0218–p0247; `kubernetes-complete-guide-madapparambat-mckendrick-2e-ru-2026:p0218:c01`–`…:p0247:c01`. Примеры не выполнялись на реальном кластере.

## Symptom / problem framing

В общем Kubernetes-кластере ресурсы разных приложений/команд смешиваются, имена конфликтуют, а один Pod может создать ресурсное давление на остальных. Глава показывает логическую организацию объектов по namespace, CPU/RAM `requests` и `limits`, ограничения на совокупные ресурсы через `ResourceQuota` и default/min/max через `LimitRange` (p0218–p0246).

## Baseline / context

- Требуются работающий Kubernetes-кластер (локальный или облачный) и настроенная `kubectl` (p0218); права, контекст, namespace и размер кластера **[Needs confirmation]**.
- Типичные namespaces: `default`, `kube-system`, `kube-public`, `kube-node-lease`; набор может зависеть от дистрибутива (p0220–p0222).
- Изоляция Namespace **логическая**, а не самостоятельная сетевая изоляция: cross-namespace обращение возможно через FQDN `<сервис>.<namespace>.svc.cluster.local`, защитные границы дополняются RBAC и сетевыми политиками (p0221, p0231–p0233).
- `Node`, `Namespace`, `PersistentVolume` — примеры cluster-scoped ресурсов; `Pod` и `ConfigMap` namespace-scoped (p0230–p0231).
- Контейнерный `requests.cpu: "250m"` — четверть ядра, `requests.memory: "512Mi"` — 512 Mi; `limits.cpu: "1000m"` и `limits.memory: "1Gi"` — примеры верхних пределов (p0235–p0237).
- `ResourceQuota`: budget на namespace (requests/limits, число объектов, storage); `LimitRange`: per-container `default`, `defaultRequest`, `min`, `max` (p0240–p0246).

## Read-only checks

Только source-confirmed:
```bash
kubectl get namespaces
kubectl describe namespaces default
kubectl get ns custom-ns
kubectl get pods -n custom-ns
kubectl get all -n custom-ns
kubectl api-resources --namespaced=false
kubectl api-resources --namespaced=true
kubectl config view --minify --output 'jsonpath={..namespace}'
kubectl get quota -n quota-ns
kubectl get resourcequotas -n quota-ns
kubectl get limitranges -n quota-ns
kubectl describe limitranges my-limitrange -n quota-ns
kubectl describe po nginx-with-request-and-limit-1 -n quota-ns
kubectl top pod -n quota-ns
```

RAG p0220–p0231, p0239, p0242, p0244–p0246. `kubectl get all -n` не проверяет буквально все namespace-scoped ресурсы — это спорная source-формулировка, сохраненная в [source-findings.md](source-findings.md). `top` зависит от metrics-server (p0237–p0238). `kubectl config view` использует локальный kubeconfig и может раскрывать конфигурационные сведения.

## Interpretation

- Namespace `Active`: допускает новые объекты; `Terminating`: удаляется и не принимает новые (p0223).
- Имя `nginx` можно использовать в `default` и `custom-ns`, но два Pod с ним в одном namespace конфликтуют `AlreadyExists` (p0230).
- После `kubectl config set-context --current --namespace=custom-ns` команда `kubectl get pods` будет обращаться к `custom-ns`, если явно не указано иное; команда меняет `~/.kube/config` (p0228–p0229).
- Если Pod с `requests.memory: "100Gi"` не помещается, `kubectl describe` показывает `Pending`, `FailedScheduling: Insufficient memory` (p0238–p0239).
- В авторском примере `ResourceQuota` отклоняет Pod с `requests.memory: 3Gi`, `limits.memory: 4Gi`: `Forbidden: exceeded quota` (p0241–p0243).
- `LimitRange` задаёт default/границы на CPU/memory контейнера; команды `get` и `describe` показывают вступившие ограничения (p0245–p0246).
- При достижении CPU limit авторы описывают снижение производительности; при превышении memory limit — возможное завершение процесса (p0236–p0237).

## Next action

Сначала подтвердить **имя кластера, текущий контекст, namespace и полномочия**. Затем только в разрешённой тестовой среде создать `custom-ns` либо `quota-ns`, провести source-confirmed наблюдение, отдельно проверить admission/scheduling до и после ResourceQuota/LimitRange. Для production нужны разграничение RBAC, NetworkPolicy, наблюдаемость, backup и план rollback: **[Needs confirmation]**.

## Modifying action

```bash
kubectl create ns custom-ns
kubectl run nginx --image nginx:latest -n custom-ns
kubectl config set-context --current --namespace=custom-ns
kubectl create ns quota-ns
kubectl apply -f resourcequota.yaml
kubectl apply -f limitrange.yaml
```

- `create ns` создаёт cluster-scoped Namespace; `run` Pod размещается в целевом namespace (p0224–p0226).
- `set-context` **state-changing local kubeconfig**, не меняет удалённый namespace, но меняет область последующих команд (p0228).
- `apply` ResourceQuota/LimitRange меняет admission и ресурсы, доступные приложениям, может блокировать следующие Pod (p0241–p0246).
- Преднамеренно неприменимый Pod с запросом 100Gi (p0238–p0239) — **учебный негативный тест**, его нельзя использовать как нормальный workload.
- `minikube addons enable metrics-server` меняет локальный кластер; нужен только в выбранной среде (p0237).

## Verification / acceptance checks

| Объект/действие | Проверка из книги | Что следует увидеть |
|---|---|---|
| Namespace создан | `kubectl get ns custom-ns` | `Active`, p0224 |
| Pod в заданном Namespace | `kubectl get pods -n custom-ns` | имя Pod, p0227 |
| Текущий контекст | `kubectl config view --minify --output 'jsonpath={..namespace}'` | название целевого namespace, p0228 |
| Завышенный request | `kubectl describe po nginx-with-request-and-limit-1 -n quota-ns` | `FailedScheduling`, p0239 |
| ResourceQuota | `kubectl get quota -n quota-ns` | `Used/Hard` и превышение → `Forbidden`, p0242 |
| LimitRange | `kubectl describe limitranges my-limitrange -n quota-ns` | значения Min, Max, Default, p0246 |

Проверка приложения как production-сервиса, задержки метрик и реальные quotas **[Needs confirmation]**.

## Rollback

- `kubectl delete namespaces custom-ns` / `kubectl delete -f custom-ns-2.yaml` **разрушительно удаляет всё содержимое namespace** (p0225); это не безусловный rollback. Полное восстановление объектов, секретов и хранилища **[Needs confirmation]**.
- Для изменения текущего namespace источник показывает `kubectl config set-context --current --namespace=default`, но исходный namespace конкретного пользователя **не установлен**; восстановить ранее сохранённую настройку нужно отдельно (p0229).
- `kubectl delete -f resourcequota-with-object-count.yaml` снимает соответствующую квоту, что способно допустить новое потребление ресурсов (p0244); для исходного `resourcequota.yaml` точный безопасный rollback [Needs confirmation].
- `kubectl delete limitranges my-limitrange -n quota-ns` удаляет ограничения; возврат прежней admission-политики требует заранее сохранённых значений (p0246).
- Для Pod/ConfigMap/изменений системных namespaces и эффекта на работающие приложения: **[Needs confirmation]**.

## Risk note

Главу нельзя интерпретировать как доказательство полной безопасности Namespace: cross-namespace networking не блокируется самим фактом разных имён (p0221, p0233). Спорные исходные формулировки об `apply -n`, `get all` и пределах `LimitRange` не исправлены молча.
