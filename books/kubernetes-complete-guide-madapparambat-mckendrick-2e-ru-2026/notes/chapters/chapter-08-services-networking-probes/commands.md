# Команды и манифесты — Глава 8: Service и probes

**Source policy:** только RAG PDF 281–325. Учебные команды ниже не исполнялись. Classifications: read-only, network diagnostic, workload-generating, state-changing / destructive. Если команда модифицирует кластер, перед применением обязательны подтверждённый context, namespace, RBAC и разрешение [Needs confirmation].

## Read-only observation and network diagnosis

| Команда из книги | Класс / смысл | PDF |
|---|---|---:|
| `kubectl get po new-nginx-pod -o wide` | read-only; Pod IP и Node | 285–286 |
| `kubectl get po,svc nginx` | read-only; Pod и Service | 292 |
| `kubectl get po nginx --show-labels` | read-only; label `run=nginx` | 293 |
| `kubectl describe svc nginx` | read-only; selector/endpoints | 293 |
| `kubectl get po k8sutils` | read-only; debug Pod status | 295 |
| `kubectl exec -it k8sutils -- nslookup nginx.default.svc.cluster.local` | network diagnostic from Pod | 295 |
| `kubectl get svc kube-dns -n kube-system -o wide` | read-only; DNS Service | 296 |
| `kubectl get svc nginx -o wide` | read-only; Service IP | 296 |
| `kubectl exec -it k8sutils -- curl nginx.default.svc.cluster.local` | outbound HTTP request from debug Pod | 296 |
| `kubectl get pods --show-labels` | read-only; selectors for whoami | 300 |
| `kubectl get service nodeport-whoami` | read-only; NodePort value | 300 |
| `kubectl describe service nodeport-whoami` | read-only; Endpoints, IP, ports | 304 |
| `minikube ip` | read-only; lab node IP | 302 |
| `minikube service --url nodeport-whoami` | environment dependent; obtain URL, may have local driver effects | 302 |
| `kubectl get service`, `kubectl get svc` | read-only; service inventory | 303, 308 |
| `kubectl describe svc/nginx-clusterip` | read-only; ClusterIP/selector | 309 |
| `kubectl get pods/nginx-clusterip --show-labels` | read-only | 309 |
| `kubectl exec k8sutils -- curl nginx-clusterip.default.svc.cluster.local` | network diagnostic | 309–310 |

`nslookup`, `curl` and `kubectl exec` launch a process in the target Pod; do not call them harmless in a sensitive runtime. Reading `describe` may expose internal infrastructure details. `cluster.local` is the suffix in the book, not confirmed universally.

## Workload-generating: temporary Pod and Service

```yaml
# new-nginx-pod.yaml (p0285)
apiVersion: v1
kind: Pod
metadata:
  name: new-nginx-pod
spec:
  containers:
    - image: nginx:1.17
      name: new-nginx-container
      ports:
        - containerPort: 80
```

```bash
kubectl apply -f new-nginx-pod.yaml
kubectl get po new-nginx-pod -o wide
kubectl delete -f new-nginx-pod.yaml
kubectl apply -f new-nginx-pod.yaml
```

p0285–p0286. **Effect:** Pod lifecycle, dynamic IP, ephemeral application. **Risk:** interruption, loss of Pod contents, image version historical. **Verification:** second `get` after recreate may show changed IP (book demo .109 → .110), not guarantee a specific value or uniqueness after all lifecycle transitions. **Rollback:** deletion is destructive; full restoration [Needs confirmation].

```bash
kubectl run nginx --image nginx --expose=true --port=80
kubectl get po,svc nginx
kubectl port-forward service/nginx 8080:80
curl 127.0.0.1:8080
```

p0292–p0294. **Effect:** `run` creates Pod + Service `nginx` ClusterIP; `port-forward` opens local socket; `curl` reads web response. **Risk:** resource collision, exposing local port, uncontrolled image. **Verification:** labels `run=nginx`, selector `run=nginx`, `Endpoints` in `describe svc`. **Rollback:** Ctrl+C stops forwarding; reversing created resources not provided as a complete tested sequence [Needs confirmation].

Source debug Pod `k8sutils.yaml`, p0295:
```yaml
apiVersion: v1
kind: Pod
metadata:
  name: k8sutils
  namespace: default
spec:
  containers:
    - name: k8sutils
      image: quay.io/iamgini/k8sutils:debian12
      command:
        - sleep
        - "infinity"
  restartPolicy: Always
```

`kubectl apply -f k8sutils.yaml` creates a long-running Pod; **risk:** resource use, image provenance/permissions; **verification:** `kubectl get po k8sutils`, then DNS and curl inside. Cleanup procedure not specified in this section [Needs confirmation].

## Workload-generating: NodePort

```bash
kubectl run whoami1 --image=containous/whoami --port 80 --labels="app=whoami"
kubectl run whoami2 --image=containous/whoami --port 80 --labels="app=whoami"
kubectl apply -f nodeport-whoami.yaml
kubectl get service nodeport-whoami
```

p0299–p0300. Service YAML:
```yaml
apiVersion: v1
kind: Service
metadata:
  name: nodeport-whoami
spec:
  type: NodePort
  selector:
    app: whoami
  ports:
    - nodePort: 30001
      port: 80
      targetPort: 80
```

**Effect:** creates two Pods with `app=whoami` and external service using node port 30001; default range 30000–32767 in source p0301. **Risk:** external network exposure, firewall conflicts, service access from other users, image trust. **Verification:** `kubectl get pods --show-labels`, `kubectl describe service nodeport-whoami` for `Endpoints`; `minikube ip`, `minikube service --url nodeport-whoami` are book's local examples. **Rollback:** `kubectl delete svc/nodeport-whoami` (p0305) removes Service but leaves Pods; resources and application data recovery [Needs confirmation].

Ports are distinct: **nodePort** on nodes, **port** on Service and **targetPort** for endpoints (p0301). Do not confuse these, and do not assume both IP examples from p0302 point to the same interface; flagged in source-findings.

## Workload-generating: ClusterIP and headless

```bash
kubectl run nginx-clusterip --image nginx --expose=true --port=80
kubectl describe svc/nginx-clusterip
kubectl get pods/nginx-clusterip --show-labels
kubectl exec k8sutils -- curl nginx-clusterip.default.svc.cluster.local
```

p0308–p0310. `run` creates Pod + ClusterIP Service. Declarative manifest p0310:
```yaml
apiVersion: v1
kind: Service
metadata:
  name: nginx-clusterip
spec:
  type: ClusterIP
  ports:
    - port: 80
      protocol: TCP
      targetPort: 80
  selector:
    run: nginx-clusterip
```

**Effect:** internal stable VIP/DNS and endpoint routing. **Risk:** mismatch selector, duplicate name, misrouted traffic; **verification:** `describe svc`, labels, request from debug Pod. **Rollback:** `kubectl delete svc nginx-clusterip` (p0311), leaves Pod running; service IP/availability restoration [Needs confirmation].

Headless variant p0311 (source presents as example, no full create command):
```yaml
apiVersion: v1
kind: Service
metadata:
  name: nginx-clusterip-headless
spec:
  clusterIP: None
  type: ClusterIP
  ports:
    - port: 80
      protocol: TCP
      targetPort: 80
  selector:
    run: nginx-clusterip
```
**Effect:** discovery of Pod endpoints without VIP load balancing; **risk:** client has to handle multiple addresses; **verification and rollback** [Needs confirmation] because no executed example is shown in chapter.

## LoadBalancer / ExternalName — declarative examples and boundaries

p0312–p0314: `type: LoadBalancer`, optional `loadBalancerClass`; cloud resource provisioning **asynchronous** and may incur provider charges. Chapter supplies conceptual explanation, **no complete runnable LoadBalancer YAML**; don't invent one. **Verification/rollback/cost:** [Needs confirmation].

p0315:
```yaml
# externalname-service.yaml
apiVersion: v1
kind: Service
metadata:
  name: mysql-db
  namespace: prod
spec:
  type: ExternalName
  externalName: app-db.database.example.com
```
**Effect if created:** DNS alias for external resource, not a proxy to Pod; `prod` namespace/example.com not confirmed to exist. **Risk:** outbound access, DNS trust, endpoint mismatch. **Verification:** source gives no executed DNS check; [Needs confirmation]. Do not treat example hostname as a live database.

## Probes — modifying Pod specification

Source p0317–p0324. These YAML fragments belong under `spec.containers[*]` **in Pod**, not inside Service. They are source snippets, not production defaults.

```yaml
# nginx-pod-with-readiness-http.yaml, p0317–p0318
readinessProbe:
  initialDelaySeconds: 5
  periodSeconds: 5
  httpGet:
    path: /ready
    port: 80
```

```yaml
# nginx-pod-with-liveness-http.yaml, p0320–p0321
livenessProbe:
  initialDelaySeconds: 5
  periodSeconds: 5
  httpGet:
    path: /healthcheck
    port: 80
    httpHeaders:
      - name: My-Custom-Header
        value: My-Custom-Header-Value
```

```yaml
# nginx-pod-with-liveness-command.yaml, p0321
livenessProbe:
  initialDelaySeconds: 5
  periodSeconds: 5
  exec:
    command: ["cat", "/hello/world"]
```

```yaml
# nginx-pod-with-liveness-tcp.yaml, p0322
livenessProbe:
  initialDelaySeconds: 5
  periodSeconds: 5
  tcpSocket:
    port: 80
```

```yaml
# nginx-pod-with-startupprobe.yaml, p0323
startupProbe:
  httpGet:
    path: /healthz
    port: liveness-port
  failureThreshold: 30
  periodSeconds: 10
```

**Effect:** readiness gates endpoint availability; failing liveness initiates container restart; startup probe controls slow initialization (p0317–p0324). **Risk:** source says Nginx often has no `/healthcheck`, so HTTP 404 makes Liveness fail (p0321). `/ready`, `/healthz`, and named port 8080 may also be unverified for unmodified Nginx. **Verification:** determine real app endpoints and status codes; no full tested acceptance or CLI probe-specific status check appears here [Needs confirmation]. **Rollback:** revert to verified manifest, but real rollout/instance state restoration [Needs confirmation]. `hostPort: 8080` used in p0322–p0323 may introduce host port conflicts.

## Operational boundary

Do not execute `run/apply/delete` or expose `NodePort/LoadBalancer` in production without authorization and verification. The chapter does not prove any live cluster, external LB or health endpoint exists, nor does it provide a complete safe rollback for network changes. CNI, DNS suffix, balancing strategy, IPv4 addresses and service readiness are environment-dependent; discrepancies recorded in [source-findings.md](source-findings.md).
