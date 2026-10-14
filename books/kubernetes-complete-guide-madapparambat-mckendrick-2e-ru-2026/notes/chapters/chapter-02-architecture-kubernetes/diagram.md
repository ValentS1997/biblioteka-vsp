# Архитектура Kubernetes — Mermaid

**Тип:** source-grounded conceptual flow (PDF 79–96, 103, 113). Это не сетевой трассировщик фактического кластера.

```mermaid
flowchart TD
  USER["Оператор / kubectl<br/>kubeconfig, context"]
  API["kube-apiserver<br/>REST API, authn/authz"]
  STORE[("etcd<br/>состояние кластера")]
  SCHED["kube-scheduler<br/>выбор узла, nodeName"]
  CTRL["kube-controller-manager<br/>reconciliation loops"]
  CCM["cloud-controller-manager<br/>облачные ресурсы, если применимо"]
  KLET["kubelet на назначенном узле<br/>спецификация Pod"]
  CRI["CRI / container runtime<br/>containerd, CRI-O"]
  POD["Запущенные контейнеры Pod"]
  PROXY["kube-proxy<br/>Service / сетевые механизмы"]
  USER -->|"kubectl / HTTP"| API
  API <-->|"read/write"| STORE
  SCHED <-->|"API: unscheduled Pod / binding"| API
  CTRL <-->|"API: наблюдение / согласование"| API
  CCM <-->|"API"| API
  API <-->|"Pod, assigned node"| KLET
  KLET -->|"Unix socket / CRI"| CRI
  CRI --> POD
  PROXY <-->|"API"| API
  PROXY -.->|"сетевая доступность"| POD
```

## Варианты отказоустойчивости

```mermaid
flowchart TD
  A["Топология кластера"]
  B["1 узел: обучение<br/>нет HA"]
  C["1 control plane + workers<br/>SPOF управляющего узла"]
  D["Несколько control plane + workers<br/>балансировка API, HA etcd"]
  E["Репликация etcd / Raft<br/>выбор лидера"]
  A --> B
  A --> C
  A --> D --> E
```

Source locators: control plane 74–89, workers/runtime 90–96, kubectl 99–107, HA 108–113. Элементы диаграмм — реконструкция **по тексту главы**, не перерисовка исходного иллюстративного PDF. Связи компонентов описывают логические взаимодействия, не маршруты и не проверенную конфигурацию узлов.
