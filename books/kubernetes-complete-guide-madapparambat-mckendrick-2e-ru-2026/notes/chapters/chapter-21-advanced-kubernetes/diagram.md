# Mermaid — Глава 21. Продвинутые механизмы Kubernetes

**RAG-only:** pages 705–749. Diagrams synthesize textual source evidence; original PDF figures were not reproduced. No runtime state verified.

## Shared L7 entry with Ingress

```mermaid
flowchart TD
  U["Browser: k8sbible.local"]
  D["DNS or /etc/hosts"]
  C["Nginx Ingress Controller"]
  I["Ingress portal-ingress, Prefix routing"]
  V["/video → video-service:8080"]
  S["/shopping → shopping-service:8080"]
  B["/ → blog-service:8080"]
  U --> D --> C --> I
  I --> V
  I --> S
  I --> B
```

pp708–715. Source lab uses HTTP without TLS; Ingress alone does not process packets. Host setting discrepancy p708 vs p709 must be resolved before any actual deployment.

## AKS Application Gateway and Gateway API

```mermaid
flowchart TD
  AZ["Azure Application Gateway / AGIC"]
  POD["Private AKS Pod IPs"]
  NAMES["Create/get-credentials cluster names mismatch"]
  GC["GatewayClass: dev-cluster-gateway"]
  GW["Gateway dev-gateway listener HTTP:80"]
  ROUTE["HTTPRoute /video → video-service:80"]
  PLACE["example.net/gateway-controller not installed"]
  AZ --> POD
  AZ --> NAMES
  GC --> GW --> ROUTE
  GC --> PLACE
```

pp717–722. AGIC and Gateway API are distinct conceptual paths. Gateway lacks verified controller and deploy/test sequence.

## Backup and restore gate

```mermaid
flowchart TD
  ETCD["Self-managed etcd state"]
  SNAP["etcdctl snapshot save /tmp/snapshot-pre-patch.db"]
  STATUS["etcdutl status snapshot.db"]
  MISMATCH{"Filename and metadata independently verified?"}
  STOP["STOP: No validated restore"]
  BACKUP["Coordinated outage, backup, approved plan"]
  RESTORE["etcdutl snapshot restore snapshot.db"]
  CHECK["Reconnect control plane and validate cluster"]
  ETCD --> SNAP --> STATUS --> MISMATCH
  MISMATCH -->|"No"| STOP
  MISMATCH -->|"Yes"| BACKUP --> RESTORE --> CHECK
```

pp727–729. The filename discrepancy belongs to the source, not a tested command. Snapshots may contain credentials and restore can replace cluster state.

## Day-2 upgrade and configuration

```mermaid
flowchart TD
  START["Check version compatibility and backups"]
  DRAIN["drain and evacuate nodes"]
  CONTROL["Upgrade control plane and kubeadm"]
  WORKER["Upgrade workers, kubelet, CNI as needed"]
  REOPEN["uncordon nodes"]
  TEST["Ready and etcd health checks"]
  ROLLBACK["Rollback plan before start"]
  START --> DRAIN --> CONTROL --> WORKER --> REOPEN --> TEST
  ROLLBACK --> START
```

pp730–732. Upgrade/downgrade not executed. `drain` may disrupt running applications; `uncordon` does not reverse a version upgrade.

## Troubleshooting workflow

```mermaid
flowchart TD
  SYM["Pending / CrashLoop / Ingress / PVC / API failure"]
  GET["kubectl get + describe"]
  EV["get events / logs --previous"]
  YAML["kubectl explain: API schema"]
  DECIDE{"Live Pod intervention required?"}
  OBS["Read-only diagnosis"]
  EXEC["Approved exec or cp"]
  DEBUG["Approved kubectl debug ephemeral container"]
  VERIFY["Re-measure and report result"]
  SYM --> GET --> EV --> YAML --> DECIDE
  DECIDE -->|"No"| OBS --> VERIFY
  DECIDE -->|"Yes"| EXEC --> DEBUG --> VERIFY
```

pp739–747. Observation and modification are separate. `exec`, `cp` and `debug` cannot be claimed read-only.

## Broader chapter map

```mermaid
flowchart TD
  TOP["Advanced Kubernetes operations"]
  NET["Ingress / Gateway / EndpointSlice"]
  ECO["Knative, OpenFaaS, Kubeflow, KubeVirt"]
  DAY["Backups, upgrades, multi-cluster"]
  SEC["TLS, kubelet, RBAC, audit, Secrets"]
  TRI["Events, logs, exec, debug, troubleshooting"]
  TOP --> NET
  TOP --> ECO
  TOP --> DAY
  TOP --> SEC
  TOP --> TRI
```

pp705–749. Ecosystem projects described conceptually, not installed.
