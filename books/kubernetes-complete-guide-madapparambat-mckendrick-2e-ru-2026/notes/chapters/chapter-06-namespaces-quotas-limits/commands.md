# Source-confirmed commands — Глава 6: namespaces, quotas, limits

**Source:** RAG PDF/printed p0218–p0247. Это каталог примеров, **не разрешение на изменение существующего кластера**. В описании action указаны effect, risk, verification и rollback; недостающие данные помечены [Needs confirmation].

## Read-only — Kubernetes API

| Команда из источника | Результат / граница | PDF |
|---|---|---|
| `kubectl get namespaces` / `kubectl get ns` | namespaces, состояние | 220–223 |
| `kubectl describe namespaces default` | свойства Namespace, квоты/LimitRange | 223 |
| `kubectl get ns custom-ns` | подтвердить Active | 224 |
| `kubectl get pods -n custom-ns` | Pod в конкретном namespace | 227 |
| `kubectl get pods` | Pod в текущем namespace; зависит от контекста | 227–230 |
| `kubectl get cm` / `kubectl get cm -n custom-ns` | ConfigMap в выбранной области | 227 |
| `kubectl config view --minify --output 'jsonpath={..namespace}'` | текущий namespace kubeconfig | 228–229 |
| `kubectl get all -n custom-ns` | типы объектов, покрываемые `get all`; область неполная [Needs confirmation] | 229 |
| `kubectl get pods --namespace custom-ns` | полная форма `-n` | 230 |
| `kubectl api-resources --namespaced=false` | ресурсы уровня кластера | 230 |
| `kubectl api-resources --namespaced=true` | ресурсы уровня namespace | 231 |
| `kubectl get po -n kube-system \| grep metrics` | наблюдение Pod metrics-server, pipe read-only | 237 |
| `kubectl top node` | метрики узлов при установленном metrics-server | 237 |
| `kubectl get pod -n quota-ns` | статус Pod | 238 |
| `kubectl describe po nginx-with-request-and-limit-1 -n quota-ns` | FailedScheduling/Insufficient memory | 239 |
| `kubectl get po -n quota-ns` | Ready/Pending | 240, 242 |
| `kubectl get quota -n quota-ns` | Used/Hard ResourceQuota | 242 |
| `kubectl top pod -n quota-ns` | фактическое потребление, метрики необходимы | 242 |
| `kubectl get resourcequotas -n quota-ns` | список объектов ResourceQuota | 244 |
| `kubectl get limitranges -n quota-ns` | список LimitRange | 246 |
| `kubectl describe limitranges my-limitrange -n quota-ns` | defaultRequest/default, min/max | 246 |

Read-only `get namespaces default -o yaml` с перенаправлением `> default-ns.yaml` в p0223 **меняет локальный файл**, см. ниже. Вывод API может содержать чувствительные сведения о конфигурации. Без указания `-n` namespace берется из локального контекста, а не всегда `default` (по последовательности p0228–p0229).

## State-changing local — запись файлов и выбор контекста

```bash
kubectl get namespaces default -o yaml > default-ns.yaml
kubectl config set-context --current --namespace=custom-ns
kubectl config set-context --current --namespace=default
```

p0223, p0228–p0229. Первый вызов **читает кластер и записывает/перезаписывает файл**, риск потери прежнего файла; verification — наличие сохранённого YAML, rollback [Needs confirmation]. `set-context` изменяет `~/.kube/config` (книгой подтверждено), изменяя target namespace последующих команд; verification — `kubectl config view --minify --output 'jsonpath={..namespace}'`. Книга возвращает `default`, но не знает первоначального контекста пользователя; rollback — [Needs confirmation].

p0228–p0229 содержит пример shell alias `alias kubens='kubectl config set-context --current --namespace'`, который задаётся в `~/.bashrc`. Это изменение **локальной конфигурации оболочки**, не состояние кластера; безопасное применение, проверка и rollback [Needs confirmation].

## Workload-generating / state-changing — Namespace

```bash
kubectl create ns custom-ns
kubectl apply -f custom-ns-2.yaml
kubectl get ns custom-ns
```

Манифест из p0224:
```yaml
apiVersion: v1
kind: Namespace
metadata:
  name: custom-ns-2
```

- `create`/ `apply` создают cluster-scoped namespaces (p0224–p0225), **меняют состояние кластера**.
- Risk: конфликт имен/полномочий; размещение рабочих ресурсов требует уточнения. Не использовать системный префикс `kube-` для пользовательских namespaces (p0224).
- Verification: `kubectl get ns custom-ns` и состояние `Active` (p0224).
- Rollback: автор показывает удаление Namespace, **которое также уничтожает находящиеся в нём ресурсы**. Оно допустимо лишь для пустой disposable среды; восстановление [Needs confirmation].
- **Source wording/code mismatch:** p0224 говорит `kubectl create` для декларативного файла, а непосредственно следующий исполняемый пример p0225 — `kubectl apply -f custom-ns-2.yaml`. Не скрывать различие.

## Destructive state-changing — Namespace deletion

```bash
kubectl delete namespaces custom-ns
kubectl delete -f custom-ns-2.yaml
```

p0225. **Effect:** перевод Namespace в `Terminating`, удаление Namespace и его содержимого. **Risk:** необратимое уничтожение объектов по явному предупреждению автора. **Verification:** автор описывает переход Active→Terminating→удалено; конкретный проверочный CLI после удаления в этом подразделе не дан — [Needs confirmation]. **Rollback:** нет подтверждённого восстановления, заранее сохранить YAML, данные/секреты/PVC [Needs confirmation]. Никогда не удалять namespace по одному его названию без проверки содержимого/владельца.

## Workload-generating — объекты внутри namespace

```bash
kubectl create ns custom-ns
kubectl run nginx --image nginx:latest -n custom-ns
kubectl create configmap configmap-custom-ns --from-literal=Lorem=Ipsum -n custom-ns
kubectl apply -f pod-in-namespace.yaml
```

p0225–p0226. **Effect:** Namespace, Pod и ConfigMap, потребление ресурсов. **Risk:** ошибочный target namespace, неприкрепленный image `latest`; **verification:** `kubectl get pods -n custom-ns`, `kubectl get cm -n custom-ns` (p0227); **rollback:** удаление ресурсов [Needs confirmation], не подменять удалением всего namespace.

Манифест p0226:
```yaml
apiVersion: v1
kind: Pod
metadata:
  name: nginx2
  namespace: custom-ns
spec:
  containers:
    - name: nginx
      image: nginx:latest
```

`kubectl run nginx --image nginx:latest` p0230 дважды в одном namespace — **негативный тест**: первый Pod создаётся, второй `AlreadyExists`. Книга показывает возможность одинакового имени в другом namespace. Не выполнять этот тест на рабочих объектах.

В p0230 сказано, что `kubectl apply -n` переопределяет `metadata.namespace` манифеста: точная интерпретация без версии и live проверок [Needs confirmation], сохранена в [source-findings.md](source-findings.md). **Не считать безопасной миграцией объекта между пространствами.**

## Workload-generating — requests / limits

Пример p0235:
```yaml
apiVersion: v1
kind: Pod
metadata:
  name: nginx-with-request
  namespace: custom-ns
spec:
  containers:
    - name: nginx
      image: nginx:latest
      resources:
        requests:
          memory: "512Mi"
          cpu: "250m"
```

Пример p0237:
```yaml
apiVersion: v1
kind: Pod
metadata:
  name: nginx-with-request-and-limit
  namespace: quota-ns
spec:
  containers:
    - name: nginx
      image: nginx:latest
      resources:
        requests:
          memory: "512Mi"
          cpu: "250m"
        limits:
          memory: "1Gi"
          cpu: "1000m"
```

**Effect:** scheduler учитывает requests; limits ограничивают потребление (p0235–p0237). **Risk:** запросы могут оставить Pod в Pending, memory limit может привести к завершению процесса, CPU limit — снизить производительность. Verification: `kubectl get po -n quota-ns`, `kubectl describe`, `kubectl top`; rollback ресурсного изменения [Needs confirmation]. Упомянута `kubectl set resource` без полного исполняемого примера — **не дописывать команду**.

## State-changing — метрики и test Pending

```bash
minikube addons enable metrics-server
kubectl create ns quota-ns
kubectl apply -f pod-with-request-and-limit-1.yaml
kubectl get pod -n quota-ns
kubectl describe po nginx-with-request-and-limit-1 -n quota-ns
kubectl apply -f pod-with-request-and-limit-2.yaml
```

p0237–p0240. **Effect:** включает addon, создаёт namespace, Pod c `requests.memory: 100Gi` (негативный тест) и отдельно Pod c `requests.memory: 1Gi`. **Risk:** изменение metrics-server и admission/ресурсных требований, тестовый Pending Pod остаётся в namespace. **Verification:** `FailedScheduling: Insufficient memory` и Ready/Running для второго примера. **Rollback:** [Needs confirmation]. Книга использует название `minikube start --profile cluster2-vb --driver=virtualbox` как вариант создания нового локального кластера (p0238), но автоматическое выполнение не предполагается.

## State-changing — ResourceQuota

Манифест p0241:
```yaml
apiVersion: v1
kind: ResourceQuota
metadata:
  name: resourcequota
  namespace: quota-ns
spec:
  hard:
    requests.cpu: "1000m"
    requests.memory: "1Gi"
    limits.cpu: "2000m"
    limits.memory: "2Gi"
```

```bash
kubectl apply -f resourcequota.yaml
kubectl get quota -n quota-ns
kubectl top pod -n quota-ns
kubectl apply -f pod-with-request-and-limit-3.yaml
```

p0241–p0242. **Effect:** квота requests CPU 1 core/memory 1Gi; limits CPU 2 cores/memory 2Gi на весь `quota-ns`; третий Pod с запросом 3Gi/лимитом 4Gi **отклоняется** в авторском примере. **Risk:** ограничение поступления новых Pod при admission, влияние на приложения. **Verification:** `kubectl get quota -n quota-ns` Used/Hard, `Forbidden: exceeded quota` (p0242). **Rollback:** для исходного `resourcequota.yaml` конкретная отдельная процедура отсутствует — [Needs confirmation].

Пример `resourcequota-with-object-count.yaml` p0243 добавляет `configmaps: "10"` и `services: "5"` с `metadata.name: my-resourcequota`:
```bash
kubectl apply -f resourcequota-with-object-count.yaml
kubectl get resourcequotas -n quota-ns
kubectl delete -f resourcequota-with-object-count.yaml
```

**Effect:** создаёт/удаляет ResourceQuota с object count; **risk:** меняет бюджет объектов и условия допуска, может разрешить неограниченные новые ресурсы после удаления; **verification:** `get resourcequotas`; **rollback:** [Needs confirmation]. Квоты PVC, StorageClass и ephemeral storage описаны концептуально (p0244), без конкретного YAML — не реконструировать.

## State-changing — LimitRange

Манифест p0245:
```yaml
apiVersion: v1
kind: LimitRange
metadata:
  name: my-limitrange
  namespace: quota-ns
spec:
  limits:
    - default:
        cpu: 500m
        memory: 256Mi
      defaultRequest:
        cpu: 500m
        memory: 128Mi
      max:
        cpu: "1"
        memory: 1000Mi
      min:
        cpu: 100m
        memory: 128Mi
      type: Container
```

```bash
kubectl apply -f limitrange.yaml
kubectl get limitranges -n quota-ns
kubectl describe limitranges my-limitrange -n quota-ns
kubectl delete limitranges my-limitrange -n quota-ns
```

p0245–p0246. **Effect:** admission/default requests and limits контейнеров в `quota-ns`; удаление снимает политику. **Risk:** могут не допускаться Pod вне диапазонов либо без соответствующих значений; **verification:** `get` и `describe`; **rollback:** [Needs confirmation] — нужно сохранять прежнюю политику. Авторские формулировки про fallback `max/min` и per-container defaults требуют проверки на конкретной версии.

## Source / version limitations

RAG не подтверждает текущий Kubernetes context, права доступа, runtime, расход ресурсов, совместимость версии и отсутствие других объектов в target namespace. Не менять `kube-system`/другие системные Namespace и не выполнять `delete namespace` как рядовой учебный rollback.
