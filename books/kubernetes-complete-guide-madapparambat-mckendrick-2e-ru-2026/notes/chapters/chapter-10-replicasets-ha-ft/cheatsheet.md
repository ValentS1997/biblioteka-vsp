# Cheatsheet — Глава 10. HA/FT и ReplicaSet

**RAG:** `kubernetes-complete-guide-madapparambat-mckendrick-2e-ru-2026:p0366:c01`–`…:p0383:c01`; PDF/печатные стр. 366–383. Никакие примеры на реальном кластере не выполнялись.

## Symptom / problem framing

Единственный Pod становится точкой отказа: при его удалении или сбое узла приложение может перестать обслуживать запросы. Авторы связывают **High Availability** с долей времени, когда сервис доступен пользователю, **Fault Tolerance** — со способностью продолжать работу при сбоях компонентов. Для этого нужны репликация, failover, балансировка и контроль работоспособности (p0366–p0369). **ReplicaSet** поддерживает желаемое число Pod, согласуя наблюдаемое состояние с `spec.replicas` (p0370–p0374).

## Baseline / context

- Нужны кластер Kubernetes, настроенный `kubectl` и, для имитации отказа узла, многоузловой кластер, в источнике **kind v1.31.0 с тремя worker** (p0366, p0372). Реальный context, namespace, привилегии и topology **[Needs confirmation]**.
- Kubernetes Service распределяет запросы между доступными Pod; ReplicaSet обеспечивает **число реплик**, не управляет маршрутизацией (p0368–p0369).
- В авторском примере ReplicaSet `nginx-replicaset-example` в `rs-ns`: `replicas: 4`, `selector.matchLabels: app=nginx, environment=test`, такой же template labels, `nginx:1.17` (p0372–p0374).
- Для `selector.matchExpressions` пример `environment In [test,dev]` (p0374). Любые существующие bare Pod с совпадающими метками способны попасть под управление ReplicaSet (p0373–p0376).
- ReplicaSet и ReplicationController поддерживают заданное число копий; ReplicaSet поддерживает сложные set-based selectors, рекомендуемая надстройка для production — **Deployment** (p0370–p0372).
- В примере HA отказ узла проверяется через **cordon**, **drain** и **delete node** — это вмешательство в инфраструктуру, а не безопасный read-only эксперимент (p0377–p0378).
- **Liveness restart выполняет kubelet**, а не ReplicaSet: автор показывает `Unhealthy`, `Killing`, затем повторный `Started` контейнера (p0381).

## Read-only checks

```bash
kubectl get nodes
kubectl describe replicaset/nginx-replicaset-example -n rs-ns
kubectl get pods -n rs-ns
kubectl describe rs/nginx-replicaset-example -n rs-ns
kubectl get po -n rs-ns -o wide
kubectl get pods
kubectl describe pod/nginx-replicaset-livenessprobe-example-lgvqv
```

RAG p0372, p0374–p0378, p0381. Команда `kubectl describe pod <Id_пода>` упомянута в p0374 как шаблон с placeholder, а не готовое имя; нужно подставить действительный Pod и namespace. `kubectl get pods` в p0376 и p0381 **не имеет `-n rs-ns`**, что создаёт неоднозначность относительно текущего namespace — [Needs confirmation]. `watch -n 1 kubectl get pods -n rs-ns` (p0375) — повторное read-only наблюдение в терминале (вывод/доступность watch зависят от окружения).

## Interpretation

- `4 current / 4 desired` и `4 Running` в `describe rs` означает соблюдение желаемого числа в конкретном выводе (p0374), но не SLA и не доказательство равномерного распределения между узлами.
- Удаление одного управляемого Pod вызывает создание нового, `describe rs` показывает `SuccessfulCreate` (p0375). Старый Pod и новый Pod — **разные экземпляры**.
- Под с совпадающими метками (`nginx-pod-bare-example`) в книге попадает под управление/удаление; `SuccessfulDelete` показывается в событиях RS (p0375–p0376). **Не создавайте bare Pod с пересекающимися selector в общей среде**.
- После `cordon`/`drain`/`delete node` автор показывает четыре Pod на двух оставшихся узлах, но не доказывает универсальную live-HA при любой topology или потере control plane (p0377–p0378).
- Масштабирование `replicas: 4 → 5 → 2` требует изменение YAML и `apply`, либо `kubectl scale` для учебного сценария; source p0379.
- HTTP GET `/` каждые 2 секунды — ливнес probe автора; после `rm /usr/share/nginx/html/index.html` источник фиксирует `403`, `Unhealthy`, `Killing` и **restart контейнера** (p0380–p0381). Это не замена Pod самим ReplicaSet.

## Next action

Определить желаемое количество реплик, права, требуемые узлы и доступность Service; прочитать текущие selectors/labels, состояние Pod и события до любых изменений. Для production выбрать управление ReplicaSet через Deployment (рекомендация главы), план распределения по узлам/данным/сетям и SLO — **[Needs confirmation]**. Деструктивные тесты допускаются только в disposable учебном кластере, с отдельным разрешением.

## Modifying action

```bash
kind create cluster --config Chapter03/kind_cluster --image kindest/node:v1.31.0
kubectl create -f ns-rs.yaml
kubectl apply -f nginx-replicaset-example.yaml
kubectl apply -f nginx-service.yaml
kubectl port-forward svc/nginx-service 8080:80 -n rs-ns
```

p0372, p0374, p0377. **Effect:** kind создаёт отдельный кластер, `create` Namespace, `apply` — ReplicaSet/Service, `port-forward` локальный сокет. **Risk:** расход ресурсов, изменение kubeconfig, выбор неправильного контекста и локальная экспозиция порта; служебные селекторы/namespace требуют проверки. **Verification:** `kubectl get nodes`, `describe rs`, `get pods`, `curl localhost:8080` (p0377). **Rollback:** Ctrl+C останавливает `port-forward`; удаление тестового кластера/возврат контекста в RAG не показаны — [Needs confirmation].

**Destructive, never production exercise without explicit approval:**
```bash
kubectl delete po nginx-replicaset-example-6qc9p -n rs-ns
kubectl apply -f nginx-pod-bare.yaml
kubectl cordon kind-worker
kubectl drain kind-worker --ignore-daemonsets
kubectl delete node kind-worker
```

p0375–p0378. **Effect:** удаляет Pod/вводит bare Pod с пересекающимися labels/выводит узел из обслуживания/удаляет объект Node. **Risk:** потеря доступности, eviction, побочные эффекты на другие workloads; bare Pod может быть удалён контроллером. **Verification:** `describe rs`, `get po -n rs-ns -o wide`, `curl localhost:8080`. **Rollback:** нет подтверждённого восстановления узла, чужих Pod или сетевого состояния — [Needs confirmation].

**Scaling and probe:**
```bash
kubectl apply -f ./nginx-replicaset-example.yaml
kubectl scale rs/nginx-replicaset-example --replicas=5
kubectl apply -f ./nginx-replicaset-livenessprobe.yaml
kubectl exec -it nginx-replicaset-livenessprobe-example-lgvqv -- rm /usr/share/nginx/html/index.html
```

p0379–p0381. `apply` after changing `spec.replicas` (to 5 or 2) меняет число Pod; `scale` — императивно меняет число; `apply liveness` создаёт отдельный ReplicaSet с тремя Pod; `exec rm` **уничтожает файл внутри контейнера и может инициировать цикл рестартов**. **Verification:** `kubectl describe rs`, `kubectl get pods`, `kubectl describe pod`, `Unhealthy`/ `Killing`. **Rollback:** восстановление удалённого файла и исходной доступности не документировано — [Needs confirmation]. Предостережение о пересечении селекторов относится ко всем связанным примерам.

## Verification / acceptance checks

- `kubectl describe rs/nginx-replicaset-example -n rs-ns`: desired/current/ready (p0374).
- После удаления **тестового** Pod: событие `SuccessfulCreate`, восстановление числа реплик (p0375).
- После отвода **тестового** узла: `kubectl get po -n rs-ns -o wide`, 4 Running на доступных узлах в примере (p0378).
- После scaling: `kubectl get pods -n rs-ns` и `describe rs` показывают 5/2 реплики (p0379).
- После liveness failure: `kubectl describe pod` показывает `Unhealthy` → `Killing` → `Started` (p0381).
- Фактический end-to-end HA/SLA, возврат после control-plane failure, геораспределение и восстановление состояния данных не проверены — [Needs confirmation].

## Rollback

- `kubectl delete rs/nginx-replicaset-livenessprobe-example` удаляет контроллер **вместе с управляемыми Pod**; `kubectl delete rs/nginx-replicaset-livenessprobe-example --cascade=orphan` удаляет контроллер **и оставляет Pod**, которые другой RS может впоследствии принять (p0382). Это **альтернативы**, не выполнять подряд.
- Масштабирование обратно требует знания прежнего desired count; source демонстрирует изменение `spec.replicas` и `apply`, но не общее восстановление рабочего состояния (p0378–p0379).
- После `kubectl drain`/ `kubectl delete node` вернуться к прежней topology без отдельного плана нельзя; [Needs confirmation].
- `kubectl exec -- rm` удаляет файл внутри контейнера; повторный старт может восстановить файлы из образа, но source не содержит полного rollback/DR — [Needs confirmation].
