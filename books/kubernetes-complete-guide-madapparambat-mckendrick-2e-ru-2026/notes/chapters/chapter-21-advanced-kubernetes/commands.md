# Commands — Глава 21: Ingress, day-2, troubleshooting

**Provenance:** PDF 705–749; RAG `p0705:c01`–`p0749:c01`. Source examples only. **No commands executed.** Mutating commands have effect/risk/verification/rollback.

## Ingress controller and application (pp711–715)

```bash
minikube start --cni calico --nodes 3 --kubernetes-version=v1.31.0
minikube addons enable ingress
kubectl get pods -n ingress-nginx
kubectl apply -f ingress/
kubectl get po,svc,ingress -n ingress-demo
minikube ip
kubectl get IngressClass -o yaml
```

`minikube start`: **local cluster state-changing**, allocates nodes/CNI; could affect existing profile; rollback [Needs confirmation]. `addons enable`: **cluster state-changing**, installs ingress-nginx components (Controller, admission Jobs); risks privileges/version compatibility and network exposure. `apply -f ingress/`: **workload-generating**, creates Namespace, ConfigMaps, 3 Deployments, 3 ClusterIP Services and `portal-ingress`. Source p714 verifies 3 Running Pod + 3 Services and Ingress CLASS nginx, HOSTS `k8sbible.local`. **Rollback:** no complete source cleanup [Needs confirmation]. `get` and `minikube ip` are read-only.

Cloud controller examples p711:
```bash
kubectl apply -f https://raw.githubusercontent.com/kubernetes/ingress-nginx/controller-v1.11.2/deploy/static/provider/cloud/deploy.yaml
kubectl apply -f https://raw.githubusercontent.com/kubernetes/ingress-nginx/controller-v1.11.2/deploy/static/provider/aws/deploy.yaml
```
**Cluster-state-changing external manifest execution:** source URL is not independently fetched or integrity verified; may create cluster-wide roles, namespace, controller and paid load balancer. This is **not** an instruction to run against production. **Verification:** controller Pods/IngressClass/Service. **Rollback:** not supplied [Needs confirmation]. Source p710 discusses a differently named Nginx controller product and an ingress-nginx retirement footnote; distinction unresolved.

Source `portal-ingress` p708:
```yaml
apiVersion: networking.k8s.io/v1
kind: Ingress
metadata:
  name: portal-ingress
  namespace: ingress-demo
  annotations:
    nginx.ingress.kubernetes.io/rewrite-target: /
spec:
  rules:
    - host: k8sbible.local
      http:
        paths:
          - path: /video
            pathType: Prefix
            backend:
              service:
                name: video-service
                port:
                  number: 8080
          - path: /shopping
            pathType: Prefix
            backend:
              service:
                name: shopping-service
                port:
                  number: 8080
```
p713 separately adds path `/` to `blog-service:8080`, but source fragment shows `port:number` misindentation. **Do not use p713 as verified complete YAML.** p708 sets a host; p709 prose incorrectly says it is unused. Source p714 modifies `/etc/hosts` (local state-changing) to map `192.168.39.18 k8sbible.local`, after `minikube ip`; IP is environment-specific, **not a stable value**. Browser `http://k8sbible.local` and paths remain unencrypted (p715). Cleanup of host file [Needs confirmation].

## AKS AGIC (pp717–720)

Source creates an AKS cluster in an Azure resource group using `az aks create` with managed identity, ingress-appgw add-on, AppGateway name and subnet; later calls `az aks get-credentials` and `kubectl apply -f aks_agic/`. **Do not execute the literal sequence:** the prose identifies group/cluster `k8sforbeginners-rg/k8sforbeginners-aks-agic`, but create uses `myResourceGroup/myAKSCluster`, while credentials use prose names (p719). Gateway name also differs (`MyAppGateway` vs `AksApplicationGateway`). `get-credentials` mutates kubeconfig; `apply` creates workloads. **Risk:** billable cloud infrastructure, exposed HTTP and wrong cluster context. **Verification:** `kubectl get ingress` p720, but source output references `example-ingress`, not `portal-ingress`, and command omits `-n agic-demo`. **Rollback:** source gives no AGIC deletion command [Needs confirmation].

## Gateway API (pp720–722)

```yaml
apiVersion: gateway.networking.k8s.io/v1
kind: GatewayClass
metadata:
  name: dev-cluster-gateway
spec:
  controllerName: example.net/gateway-controller
---
apiVersion: gateway.networking.k8s.io/v1
kind: Gateway
metadata:
  name: dev-gateway
  namespace: gateway-api-demo
spec:
  gatewayClassName: dev-cluster-gateway
  listeners:
    - name: http
      protocol: HTTP
      port: 80
---
apiVersion: gateway.networking.k8s.io/v1
kind: HTTPRoute
metadata:
  name: dev-httproute
  namespace: gateway-api-demo
spec:
  parentRefs:
    - name: dev-gateway
      kind: Gateway
      namespace: gateway-api-demo
  hostnames: [k8sbible.local]
  rules:
    - matches:
        - path: {type: PathPrefix, value: /video}
      backendRefs:
        - name: video-service
          port: 80
```
**Illustrative source YAML; not applied**. `controllerName` is a placeholder-style example, no real matching Controller/CRD installation or routed request verified. Source path `gateway-api/gateway_api/gateway.yaml` has extra nested directory; filenames in repo [Needs confirmation]. `video-service` port 80 here versus Ingress 8080 p708, without demonstrated service port change. Running any unverified creation would mutate Gateway CRDs and requires provider support; rollback [Needs confirmation].

## Etcd snapshot and recovery (pp727–729)

Source describes a TLS-authenticated local `etcdctl snapshot save /tmp/snapshot-pre-patch.db` using CA/client certificate/private key parameters, followed by:
```bash
etcdutl --write-out=table snapshot status snapshot.db
etcdutl --data-dir <каталог_с_данными> snapshot restore snapshot.db
```
**Critical:** snapshot creation and subsequent status/restore refer to different filenames, with no source file renaming. **Classification:** `snapshot save` creates a highly sensitive file with cluster state, `status` read-only status of specified file, `restore` **destructive/high-impact etcd data restoration**. No live execution recommended. **Risk:** cluster outage, secrets exposure, inconsistent multi-node state and wrong snapshot. **Verification:** source suggests status output hash, revision and key count; no successful restore test. **Rollback:** no source-backed verified DR procedure [Needs confirmation]. Source p729 instructs stopping API servers and reconnecting endpoints before resuming.

## Upgrades / node operations (pp730–732)

```bash
kubectl drain <освобождаемые_узлы> --ignore-daemonsets
kubectl get nodes
kubectl uncordon <имя-узла>
```
**Effects:** `drain` cordons/evicts workloads, **potential outage/data loss**; `get` is observation; `uncordon` reopens scheduling. **Verification:** source requires node Ready, controller health and etcd monitoring. **Rollback:** `uncordon` is *not* version rollback; source provides no exact kubeadm/package versions or reproducible downgrade [Needs confirmation]. All cloud upgrade details depend on provider and version.

## Troubleshooting observations (pp739–747)

```bash
kubectl get pods
kubectl describe pod todo-app
kubectl get deployments
kubectl describe deployment webapp
kubectl get events
kubectl get events --field-selector involvedObject.name=todo-pod
kubectl logs todo-app
kubectl logs todo-app -c app-container
kubectl logs -f todo-app
kubectl logs todo-app --previous
kubectl explain pod
kubectl explain pod.spec
kubectl get nodes
kubectl get pv
kubectl get pvc
kubectl get quota
kubectl top nodes
kubectl top pods
kubectl auth can-i <глагол> <ресурс>
kubectl describe ingress <имя_ingress>
```
**Read-only API**, caveat: logs and describe can reveal secrets/environment; `-f` stays open. `kubectl get pods -l todo -o json | jq -r '.items[] | .metadata.name' | xargs -I {} kubectl logs {}` p741 retrieves multiple logs, but exact label choice [Needs confirmation].

## In-container diagnostics (pp742–745)

```bash
kubectl get po -n trouble-ns
kubectl exec -it blog-675df44d5-gkrt2 -n trouble-ns -- /bin/bash
kubectl cp troubles/test.txt blog-675df44d5-gkrt2:/app/test.txt -n trouble-ns
kubectl cp blog-675df44d5-gkrt2:/app/app.py /tmp/app.py -n trouble-ns
kubectl debug -it pod/video-7d945d8c9f-wkxc5 --image=quay.io/iamgini/k8sutils:debian12 -c k8sutils -n ingress-demo
```
**Classes:** `get` read-only; `exec` starts processes inside Pod (can be state-changing); `cp` reads or writes Pod/local filesystem, potentially sensitive; `debug` **adds ephemeral container** and starts processes (Pod-state-changing). Source p742 earlier shows `kubectl exec blog-... -- env` *without namespace* despite `trouble-ns`: cannot assume it works as printed. **Verification:** source `whoami; hostname; uptime`, copied file listing and debug `nslookup video-service` / `curl http://video-service:8080`. **Rollback:** no proven cleanup of ephemeral containers or copied files [Needs confirmation]. Never archive raw environment variables without secret handling.

## Source constraints

Knative, OpenFaaS, Kubeflow, KubeVirt, Rancher, Lens, Azure Arc, etc. are **conceptual only**. They supply no source-confirmed installation commands or production compatibility tests. No current external versions/prices verified.
