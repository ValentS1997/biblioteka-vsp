# Диаграммы: логика главы 1

## 1. Почему появляется Kubernetes

```mermaid
flowchart LR
    M["Монолит"] --> MS["Микросервисы"]
    MS --> C["Больше независимо развертываемых компонентов"]
    C --> P["Сложнее размещение, конфигурация, связи и восстановление"]
    P --> CT["Контейнеры: изоляция и консистентное окружение"]
    CT --> K["Kubernetes: автоматизированное размещение и управление"]
```

Глава связывает Kubernetes с ростом операционной сложности: микросервисы дают независимость компонентам, но требуют автоматизации размещения и сопровождения.

## 2. Контейнерная граница

```mermaid
flowchart TB
    A["Application process"] --> N["Linux namespaces"]
    A --> G["cgroups"]
    N --> H["Host kernel"]
    G --> H
    H --> HW["Hardware"]
```

Namespaces определяют, какие системные ресурсы видит процесс. cgroups ограничивают объём ресурсов, который процесс может потреблять.

## 3. Базовая архитектура Kubernetes

```mermaid
flowchart LR
    U["Разработчик / описание приложения"] --> API["API server"]

    subgraph CP["Control plane"]
      API
      SCH["Scheduler"]
      CM["Controller Manager"]
      ETCD["etcd"]
    end

    API --> SCH
    API --> CM
    API --> ETCD

    SCH --> KL["Kubelet"]
    API --> KL

    subgraph W["Worker node"]
      KL
      RT["Container runtime"]
      KP["kube-proxy"]
      APP["Containers / application"]
    end

    KL --> RT
    RT --> APP
    KP --> APP
```

Control plane хранит и управляет состоянием кластера; worker nodes выполняют контейнеризированные приложения.

## 4. Путь приложения

```mermaid
flowchart LR
    S["Исходное приложение"] --> I["Container image"]
    I --> R["Image registry"]
    D["Описание приложения"] --> API["Kubernetes API server"]
    API --> SC["Scheduler"]
    SC --> K["Kubelet выбранного узла"]
    R --> CR["Container runtime"]
    K --> CR
    CR --> C["Running containers"]
```

Описание приложения задаёт требуемое состояние, а Kubernetes выбирает узлы и инициирует запуск.

## 5. Поддержание состояния

```mermaid
flowchart LR
    DES["Desired state"] --> OBS["Kubernetes observes actual state"]
    OBS --> Q{"Actual = desired?"}
    Q -- "да" --> OBS
    Q -- "нет" --> ACT["Перезапуск / новый узел / изменение числа реплик"]
    ACT --> OBS
```

Диаграмма отражает описанный в главе принцип постоянного поддержания количества и состояния экземпляров.
