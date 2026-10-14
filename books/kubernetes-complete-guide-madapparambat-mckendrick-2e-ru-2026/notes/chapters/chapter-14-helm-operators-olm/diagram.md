# Диаграммы главы 14 — Helm, OLM и операторы

**Источник:** RAG PDF p0474–p0514. Диаграммы синтезированы из текстовых chunks; иллюстрации PDF напрямую не просмотрены.

## Helm: chart → release

```mermaid
flowchart TD
  REPO["Repository / Artifact Hub"]
  CHART["Chart: Chart.yaml, values.yaml, templates, dependencies"]
  VALUES["Custom values / --values"]
  HELM["Helm: render and install"]
  REL["Release wp-demo"]
  WP["WordPress Deployment and Service"]
  DB["MariaDB StatefulSet and PVC"]
  REPO --> CHART --> HELM
  VALUES --> HELM --> REL
  REL --> WP
  REL --> DB
```

RAG p0475–p0489. Установка чарта создаёт ресурсы, включая базу данных и PVC; не следует считать uninstall полным удалением всех данных.

## Operator control loop

```mermaid
flowchart TD
  CRD["CRD defines custom resource kind"]
  CR["Custom resource: desired state"]
  OP["Operator reconciliation loop"]
  ACT["Actual Deployment, StatefulSet, PVC, Service"]
  CRD --> CR --> OP
  ACT -->|"Observe"| OP
  OP -->|"Create/update/recover"| ACT
```

p0495–p0499. CRD определяет тип, custom resource хранит параметры конкретного экземпляра. Результат зависит от прикладной логики оператора.

## OLM lifecycle

```mermaid
flowchart TD
  CAT["OperatorHub catalog / CatalogSource"]
  SUB["Subscription"]
  CSV["ClusterServiceVersion: metadata, version, RBAC"]
  OP["Installed operator and CRDs"]
  CAT --> SUB --> CSV --> OP
```

p0500–p0504. Из успеха одного CSV нельзя выводить Ready всех operator/catalog Pods.

## Monitoring pipeline

```mermaid
flowchart TD
  OLM["OLM manages Prometheus and Grafana Operators"]
  PCR["Prometheus CR replicas=2"]
  GCR["Grafana CR"]
  DS["Node Exporter DaemonSet"]
  SVC["Node Exporter Service"]
  MON["ServiceMonitor"]
  PROM["Prometheus StatefulSet and Service"]
  GRAF["Grafana service and dashboard"]
  OLM --> PCR --> PROM
  OLM --> GCR --> GRAF
  DS --> SVC --> MON --> PROM
  PROM -->|"Metrics datasource"| GRAF
```

p0505–p0513. `servicemonitor-instance.yaml` not fully printed in chapter RAG; actual match labels and scrape coverage [Needs confirmation].

## Risk gate

```mermaid
flowchart TD
  A["Plan install/upgrade"]
  B{"Source and package reviewed?"}
  C{"RBAC and credentials safe?"}
  D{"Retention/backup approved?"}
  E["Authorized test deployment"]
  STOP["Stop: Needs confirmation"]
  A --> B
  B -->|"No"| STOP
  B -->|"Yes"| C
  C -->|"No"| STOP
  C -->|"Yes"| D
  D -->|"No"| STOP
  D -->|"Yes"| E
```

p0479, p0482, p0487, p0490–p0494, p0502, p0506. Исторические учебные инструкции не равны актуальному production runbook.
