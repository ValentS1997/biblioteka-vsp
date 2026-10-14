# Commands — Глава 11: Deployment, rollout, rollback, canary

**Source:** RAG PDF **384–419**. Ниже — только команды, явно содержащиеся в chapter RAG (нормализованы однозначные PDF-переносы). Не исполнялись. Target Kubernetes context, namespace, RBAC, exposed ports и recovery **[Needs confirmation]**. Любая `apply`/`scale`/`set image`/`rollout undo`/`delete` — **state-changing**.

## Read-only / observational

| Source command | Purpose / risk | PDF |
|---|---|---:|
| `kubectl create deployment my-deployment --replicas=1 --image=my-image:latest --dry-run=client --port=80 -o yaml` | dry-run: генерирует YAML локально, без создания Deployment; исторический dummy image | 388 |
| `kubectl rollout status deployment nginx-deployment-example` | наблюдает rollout, ожидает завершения | 391 |
| `kubectl get deploy nginx-deployment-example` | READY/UP-TO-DATE/AVAILABLE | 391 |
| `kubectl get rs` | дочерние ReplicaSet и история | 391, 408 |
| `kubectl get pods` / `kubectl get po` | текущий namespace; конкретная область [Needs confirmation] | 391, 402, 407–408 |
| `kubectl describe service nginx-service-example` | selector, Endpoints, external exposure | 395, 400 |
| `kubectl describe svc nginx-service-example | grep Endpoint` | список готовых backend в примере | 401 |
| `kubectl describe pod nginx-deployment-readiness-69dd4cfdd9-4pkwr` | Unhealthy/HTTP 404 | 401 |
| `kubectl get po -w` | follow, Running != Ready | 401 |
| `kubectl describe deployments.apps nginx-deployment-readiness` | события ScalingReplicaSet | 403 |
| `kubectl describe deploy nginx-deployment-rollingupdate` | события rollout RS | 408 |
| `kubectl rollout status deployment.apps/nginx-deployment-rollingupdate` | проверка успеха обновления | 407, 410 |
| `kubectl describe pod nginx-deployment-rollingupdate-5479f5d87f-2k7d6 | grep 'Image:'` | версия `nginx:1.18` | 409 |
| `kubectl rollout history deployment.apps/nginx-deployment-rollingupdate` | доступные ревизии | 410–411 |
| `kubectl rollout history deploy nginx-deployment-rollingupdate --revision=2` | шаблон конкретной ревизии | 410 |

При `get pods` без `-n` scope определяется kubeconfig; реальные имена Pod с суффиксами источника не следует использовать вслепую. `kubectl exec … curl` генерирует сетевой запрос внутри контейнера, это **network diagnostic**, не read-only API.

## Generate locally / local state change

```bash
kubectl create deployment my-deployment --replicas=1 --image=my-image:latest --dry-run=client --port=80 -o yaml > my-deployment.yaml
cp nginx-deployment-readinessprobe.yaml nginx-deployment-rollingupdate.yaml
```

RAG p0388, p0406. **Effect:** writes/overwrites local manifest files (no Kubernetes object in `dry-run=client`). **Risk:** overwrite existing file, dummy image `my-image:latest`. **Verification:** inspect resulting YAML before apply; complete tested rollback of overwritten source file **[Needs confirmation]**.

## Workload-generating — initial Deployment

p0388–p0389 source manifest `nginx-deployment.yaml`:
```yaml
apiVersion: apps/v1
kind: Deployment
metadata:
  name: nginx-deployment-example
spec:
  replicas: 3
  selector:
    matchLabels:
      app: nginx
      environment: test
  minReadySeconds: 10
  strategy:
    type: RollingUpdate
    rollingUpdate:
      maxUnavailable: 1
      maxSurge: 1
  template:
    metadata:
      labels:
        app: nginx
        environment: test
    spec:
      containers:
        - name: nginx
          image: nginx:1.17
          ports:
            - containerPort: 80
```

```bash
kubectl apply -f ./nginx-deployment.yaml
kubectl rollout status deployment nginx-deployment-example
kubectl get deploy nginx-deployment-example
kubectl get rs
kubectl get pods
```

**Effect:** creates Deployment, ReplicaSet and three nginx Pod. **Risk:** selectors overlap, historical nginx image, CPU/memory requirements absent. **Verification:** source p0391 demonstrates READY `3/3` and rollout success, observes RS with `pod-template-hash`. **Rollback:** no source-confirmed restoration of prior app/data; [Needs confirmation].

Change annotation `kubectl annotate deployment/nginx-deployment-example kubernetes.io/change-cause='Updated image to 1.2.3'` (p0391) — **state-changing** metadata, may affect audit; verification via revision history, no source explicit rollback. `--record` described as deprecated (p0390).

## Service and network access

Source p0394–p0395:
```yaml
# nginx-service.yaml
apiVersion: v1
kind: Service
metadata:
  name: nginx-service-example
spec:
  selector:
    app: nginx
    environment: test
  type: LoadBalancer
  ports:
    - port: 80
      protocol: TCP
      targetPort: 80
```

```bash
kubectl apply -f nginx-service.yaml
kubectl describe service nginx-service-example
kubectl apply -f ../Chapter07/k8sutils.yaml
kubectl exec -it k8sutils -- curl nginx-service-example.default.svc.cluster.local | grep Welcome -A2
kubectl expose deployment --type=LoadBalancer nginx-deployment-example
```

**Effect:** `apply` Service provisions external LoadBalancer when supported, `apply k8sutils` creates a debug Pod; `expose` creates *another* Service named after Deployment (p0396). **Risk:** public exposure, cloud cost, duplicate resources, unmatched selectors, untrusted debug image; `exec curl` creates network traffic. **Verification:** `describe service` Endpoints/selector and expected nginx HTML. **Rollback:** source does not describe a safe end-to-end removal procedure; [Needs confirmation]. For environments lacking LoadBalancer, book permits NodePort/ClusterIP and discusses `minikube service` without full substituted manifest (p0395). Do not invent a working cloud external address.

## Readiness exercise — deliberate disruption, controlled re-enable

p0397–p0399 describes `nginx-deployment-readinessprobe.yaml`, assembled from multiple source fragments:
```yaml
apiVersion: apps/v1
kind: Deployment
metadata:
  name: nginx-deployment-readiness
spec:
  replicas: 3
  selector:
    matchLabels:
      app: nginx
      environment: test
  minReadySeconds: 10
  strategy:
    type: RollingUpdate
    rollingUpdate:
      maxUnavailable: 1
      maxSurge: 1
  template:
    metadata:
      labels:
        app: nginx
        environment: test
    spec:
      containers:
        - name: nginx
          image: nginx:1.25.4
          ports:
            - containerPort: 80
          command:
            - /bin/sh
            - -c
            - |
              touch /usr/share/nginx/html/ready
              echo "You have been served by Pod with IP address: $(hostname -i)" > /usr/share/nginx/html/index.html
              nginx -g "daemon off;"
          readinessProbe:
            httpGet:
              path: /ready
              port: 80
            initialDelaySeconds: 5
            periodSeconds: 2
            timeoutSeconds: 10
            successThreshold: 1
            failureThreshold: 2
```

**Note:** Source combines split YAML across p0397–p0398, with a PDF-extracted line-break inside the shell echo string; the one-line `echo` above is an unambiguous formatting normalization according to the explanatory text p0399, *not* independently executed. Exact compatibility and successful build **[Needs confirmation]**.

```bash
kubectl delete deployment nginx-deployment-example
kubectl apply -f ./nginx-deployment-readinessprobe.yaml
kubectl describe svc nginx-service-example
kubectl exec -it k8sutils -- curl nginx-service-example.default.svc.cluster.local
kubectl exec -it nginx-deployment-readiness-69dd4cfdd9-4pkwr -- rm /usr/share/nginx/html/ready
kubectl describe svc nginx-service-example | grep Endpoint
kubectl describe pod nginx-deployment-readiness-69dd4cfdd9-4pkwr
kubectl get po -w
kubectl exec -it nginx-deployment-readiness-69dd4cfdd9-4pkwr -- touch /usr/share/nginx/html/ready
```

p0397, p0400–p0402. **Effect:** `delete` stops existing Deployment, `apply` creates new, `rm` disrupts readiness, `touch` restores readiness condition in educational image. **Risk:** application unavailability; the book deletes `ready` on **all three** Pod on p0401 so no backend remains. **Verification:** Endpoints drop from 3 to 2 to 0, Pod `Running` but `0/1 Ready`, HTTP 404 for probe and `curl` connection failure. **Rollback:** `touch` shown for one Pod; full recovery of arbitrary application and Deployment [Needs confirmation]. The other two source `exec rm` commands target Pod suffixes `7n2kz` and `t7rp2` (p0401); **not safe to reuse** on unknown workload.

## Scaling — workload-generating

Source p0402–p0403: edit `spec.replicas: 10`, then `2`, apply same manifest:
```bash
kubectl apply -f ./nginx-deployment-readinessprobe.yaml
kubectl describe deployments.apps nginx-deployment-readiness
kubectl scale deploy nginx-deployment-readiness --replicas=10
kubectl scale deploy nginx-deployment-readiness --replicas=2
kubectl describe deploy nginx-deployment-readiness
```

**Effect:** increases/decreases Pod count and capacity. **Risk:** CPU/memory cost, transient availability, mismatch with Git. **Verification:** events `ScalingReplicaSet … 10 from 3` and `… 2 from 10` (p0403). **Rollback:** apply previously versioned manifest; source lacks full checked recovery [Needs confirmation].

## Rollout, history and rollback

Source p0406–p0409 `nginx-deployment-rollingupdate.yaml` is a **partial snippet**, not a complete tested manifest. It changes `metadata.name: nginx-deployment-rollingupdate`, sets `replicas: 3`, `maxUnavailable: 1`, `maxSurge: 1`, `minReadySeconds: 10`, initial `image: nginx:1.17`; then `nginx:1.18`. Source refers to a `readinessProbe` but omits parts of full YAML here — [Needs confirmation].

```bash
kubectl apply -f nginx-deployment-rollingupdate.yaml
kubectl rollout status deployment.apps/nginx-deployment-rollingupdate
kubectl describe deploy nginx-deployment-rollingupdate
kubectl get rs
kubectl get po
kubectl set image deployment nginx-deployment-rollingupdate nginx=nginx:1.19
kubectl rollout history deployment.apps/nginx-deployment-rollingupdate
kubectl rollout history deploy nginx-deployment-rollingupdate --revision=2
kubectl rollout undo deploy nginx-deployment-rollingupdate
kubectl rollout undo deploy nginx-deployment-rollingupdate --to-revision=2
kubectl rollout status deploy nginx-deployment-rollingupdate
kubectl rollout pause deployment nginx-deployment-example
kubectl rollout resume deployment nginx-deployment-example
```

p0407–p0411. **Effect:** applying new image creates new RS/revision; `set image` changes deployment imperatively; `undo` changes desired template to prior revision, `pause`/`resume` control rollout. **Risk:** inadvertent new version, mismatch of paused **`nginx-deployment-example`** vs rolled-back **`nginx-deployment-rollingupdate`**, Git drift, downtime. **Verification:** `rollout status`, `get rs` (old RS scaled zero), `get po`, `describe pod … | grep 'Image:'`, `rollout history`. **Rollback:** previous Git manifest and verified rollout; no complete recovery of dependencies/data provided [Needs confirmation]. Do not execute both `undo` variants as a fixed sequence without checking revision history.

## Destructive deletion / orphan

```bash
kubectl delete deploy nginx-deployment-readiness
kubectl delete deploy nginx-deployment-readiness --cascade=orphan
```
p0404. **These are mutually exclusive alternatives**, not sequential steps. Default delete removes associated Pods, orphan leaves them without Deployment control. **Risk:** outage, unexpected other-controller adoption. Verification of resulting resources not fully supplied in source; rollback [Needs confirmation]. Source text mistakenly calls orphaned Pod those belonging to `nginx-deployment-example`, instead of command target `nginx-deployment-readiness` (see findings).

## Canary — conceptual, incomplete manifests

p0412–p0413 describes stable `frontend-stable` (3 replicas, `frontend-app:1.0`) and `frontend-canary` (1 replica, `frontend-app:2.0`), both `app=myapp,tier=frontend`, differing `version` labels, with one Service:
```yaml
apiVersion: v1
kind: Service
metadata:
  name: frontend-service
spec:
  selector:
    app: myapp
    tier: frontend
  ports:
    - protocol: TCP
      port: 80
      targetPort: 8080
```
The two Deployment snippets use ellipses; **not complete runnable YAML**. The chapter provides no confirmed Helm/Ingress implementation or live 10% routing measurement. **Risk:** number of replicas `3+1` is not a reliable traffic-percentage control; traffic policy/SLO [Needs confirmation]. Verification: source advises error rate, latency and user feedback, but supplies no executable command. Rollback [Needs confirmation].

## Operational safety

Use this catalog as source-grounded evidence, not a production procedure. `LoadBalancer` may create public exposure and charges. `Recreate` has downtime, readiness disruption can remove every endpoint, and labels may collide. Historical nginx image tags are not evidence of current support.
