# Концептуальная схема главы 3 — выбор и запуск учебного кластера

Это **RAG-grounded концептуальный workflow**, а не автоматизированный сценарий установки. Источник: PDF 115–142.

```mermaid
flowchart TD
    A["Нужен Kubernetes для практики<br/>PDF 115"]
    B["Baseline: kubectl, CPU/RAM/disk,<br/>container engine или hypervisor<br/>PDF 116"]
    C{"Выбрать учебную среду"}
    M["minikube<br/>VM или Docker/Podman<br/>PDF 116–129"]
    K["kind<br/>контейнерные узлы и YAML<br/>PDF 129–135"]
    L["Killercoda<br/>временный браузерный кластер<br/>PDF 135"]
    MS["minikube start<br/>создание и kubeconfig"]
    KS["kind create cluster<br/>создание и kubeconfig"]
    VC["kubectl config current-context<br/>проверить выбранный кластер"]
    V["minikube status / kubectl get nodes<br/>kubectl cluster-info / readyz<br/>PDF 122–125, 133–134"]
    D{"Кластер и нужные узлы готовы?"}
    E["Проверить драйвер, ресурсы,<br/>конфигурацию, повторно проверить<br/>не менять production"]
    F["Использовать учебный кластер<br/>в следующих главах"]
    S["Остановить: minikube stop<br/>или pause / unpause"]
    X["Удалить: minikube delete<br/>или kind delete cluster<br/>ПОТЕРЯ СОСТОЯНИЯ"]
    A --> B --> C
    C --> M --> MS --> VC
    C --> K --> KS --> VC
    C --> L --> V
    VC --> V --> D
    D -->|"Нет"| E
    E --> V
    D -->|"Да"| F
    F --> S
    F --> X
```

## Вне учебного сценария

```mermaid
flowchart TD
    A["Production Kubernetes<br/>PDF 136–141"]
    B["Managed cloud:<br/>GKE / AKS / EKS"]
    C["On-prem/self-managed:<br/>kubeadm, kops, Kubespray"]
    D["Управление инфраструктурой и HA:<br/>сеть, storage, upgrades, security,<br/>monitoring, IaC"]
    A --> B --> D
    A --> C --> D
```

**Ограничения схем:** команды нельзя исполнять из блок-схемы без контекста и прав; `minikube delete` и `kind delete cluster` необратимы по описанию главы (стр. 127, 134). `kind stop` из источника помечен [Needs confirmation], не используется как достоверный rollback.
