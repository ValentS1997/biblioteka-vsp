# Команды главы 11

Source policy: RAG-only. Это в основном inspection commands; source-era internal/debug commands отдельно маркированы.

## List Kubernetes system components

Source:

~~~bash
kubectl get po -o custom-columns=POD:metadata.name,NODE:spec.nodeName   --sort-by spec.nodeName -n kube-system
~~~

Read-only.

Purpose:
- map control-plane/add-on Pods to nodes.

## Inspect etcd internals — source-era / privileged

Source v2-style:

~~~bash
etcdctl ls /registry
etcdctl ls /registry/pods
etcdctl ls /registry/pods/default
etcdctl get /registry/pods/default/<pod-name>
~~~

Source note for v3 API:

~~~bash
etcdctl get /registry --prefix=true
~~~

READ-ONLY but HIGH-SENSITIVITY internal datastore access.

Risks:
- etcd contains authoritative cluster state;
- source explicitly notes direct etcd access exposes Secrets;
- applications/components should use API server, not etcd.

Do not use write/delete etcd commands as operational shortcuts.

## Watch Pods

~~~bash
kubectl get pods --watch
kubectl get pods -o yaml --watch
~~~

Read-only watch streams.

## Observe cluster events

~~~bash
kubectl get events --watch
~~~

Read-only.

Useful to see:
- Deployment controller scaling ReplicaSet;
- ReplicaSet controller creating Pods;
- scheduler assignment;
- Kubelet pull/create/start events.

## Create Nginx example Pod/Deployment

Source-era command:

~~~bash
kubectl run nginx --image=nginx
~~~

STATE-CHANGING.

Source output labels it Deployment creation in that version.

Purpose:
- inspect underlying runtime containers.

Rollback command not provided in retrieved excerpt: [Needs confirmation].

## Enter worker node

Source Minikube:

~~~text
minikube ssh
~~~

Source GKE:

~~~bash
gcloud compute ssh <node-name>
~~~

Interactive privileged node access.

## Inspect runtime containers

On source Docker-based node:

~~~bash
docker ps
~~~

Read-only runtime inspection.

Expected source observation:
- application container;
- pause/infrastructure container.

## Inspect add-ons

Source:

~~~bash
kubectl get rc -n kube-system
~~~

Read-only.

Used to inspect source-era Ingress/dashboard ReplicationControllers.

## Inspect leader-election resource

Source:

~~~bash
kubectl get endpoints kube-scheduler -n kube-system -o yaml
~~~

Read-only.

Source-era behavior:
- annotation control-plane.alpha.kubernetes.io/leader;
- holderIdentity indicates current leader.

This is historical implementation detail, not generalized as current contract.

## Network inspection concepts

Source discusses node-side tools such as ifconfig while explaining veth/bridge structure, but no canonical complete troubleshooting command set is provided in the verified chunks.

Operational command reconstruction from memory: not performed.

## Service implementation

Chapter explanation is architectural: kube-proxy watches Services/Endpoints and installs iptables rules.

Exact iptables inspection command is not confirmed in retrieved chapter excerpts: [Needs confirmation].

Do not invent an iptables command line.

## Risk matrix

| Operation | Class |
|---|---|
| kubectl get / --watch | read-only |
| kubectl get events --watch | read-only |
| kubectl get endpoints ... -o yaml | read-only |
| etcdctl get/ls | privileged internal read |
| kubectl run nginx --image=nginx | state-changing |
| minikube ssh / gcloud compute ssh | privileged interactive access |
| docker ps | node-local read-only |
