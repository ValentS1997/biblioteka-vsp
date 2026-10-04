# Шпаргалка: внутреннее устройство Kubernetes

## 1. Control plane vs worker node

Control plane:
- etcd;
- API server;
- scheduler;
- controller manager.

Worker:
- Kubelet;
- container runtime;
- kube-proxy;
- networking plugin.

Add-ons:
- DNS;
- Ingress controller;
- dashboard;
- network agents.

## 2. etcd

~~~text
all persistent cluster state
        ↓
      etcd
        ↑
API server only
~~~

Source rule:
- Kubernetes components read/write etcd indirectly through API server.

RAFT/quorum:
- state change requires majority;
- 3 members tolerate 1 failure;
- 5 tolerate 2;
- 7 tolerate 3.

## 3. API request pipeline

~~~text
HTTP request
  ↓
Authentication
  ↓
Authorization
  ↓
Admission control
  ↓
Resource validation
  ↓
etcd persistence
~~~

Source note:
read-only requests bypass admission control.

## 4. Watch mechanism

~~~bash
kubectl get pods --watch
kubectl get pods -o yaml --watch
~~~

Model:

~~~text
client opens watch
API object changes
API server streams updated object
controllers react
~~~

## 5. Scheduler

Scheduler does not start containers.

~~~text
unscheduled Pod
  ↓ watch
scheduler
  ↓ filter nodes
  ↓ prioritize nodes
  ↓ update Pod.spec.nodeName
API server
  ↓ watch
Kubelet on selected node
~~~

## 6. Controllers

Independent reconciliation loops.

Example chain:

~~~text
Deployment
  ↓ Deployment controller
ReplicaSet
  ↓ ReplicaSet controller
Pod
  ↓ Scheduler
assigned Pod
  ↓ Kubelet
containers
~~~

## 7. Events

~~~bash
kubectl get events --watch
~~~

Useful to observe controller actions and scheduling/container lifecycle events.

## 8. Kubelet and static Pods

Kubelet:
- watches Pods assigned to its node;
- ensures containers are running;
- reports Pod/node status;
- may also read local manifest directory.

Source framing:
Kubelet itself runs as normal system component.

## 9. Running Pod internals

Source Docker-era model:

~~~text
Pod
├─ pause / infrastructure container
├─ app container A
└─ app container B
~~~

pause container holds shared Linux namespaces.

If app container restarts, it rejoins same Pod namespaces.

## 10. Pod networking

Requirements:
- each Pod gets unique cluster-wide IP;
- Pods communicate directly;
- no address translation should be required between Pods;
- Pod sees same IP peers see.

Same node:
~~~text
container eth0 ↔ veth ↔ bridge ↔ veth ↔ peer
~~~

Cross-node:
- non-overlapping Pod CIDRs;
- routing, overlay or underlay connects node bridges.

## 11. CNI

Source lists:
- Calico;
- Flannel;
- Romana;
- Weave Net.

CNI standardizes network-plugin integration.

## 12. Service implementation

Source-era iptables model:

~~~text
client packet to ClusterIP:port
  ↓
iptables rules programmed by kube-proxy
  ↓ random backend Endpoint
  ↓ DNAT/forward
Pod IP:targetPort
~~~

kube-proxy watches:
- Service objects;
- Endpoints objects.

## 13. High availability

Applications:
- multiple replicas;
- distribute replicas across nodes.

Control plane:
- replicated etcd;
- multiple API servers;
- multiple scheduler/controller-manager instances;
- one active leader for scheduler/controller-manager.

## 14. Leader election

Source-era model:

~~~text
scheduler instances
  ↓ compete to update
Endpoints kube-scheduler
  ↓ annotation holderIdentity
one leader
~~~

Winner renews resource periodically; if renewals stop, standbys compete again.

## Acceptance model

When reasoning about Kubernetes internals, separate:

- persisted desired state: etcd;
- API/security/validation boundary: API server;
- placement decision: scheduler;
- reconciliation: controllers;
- node execution: Kubelet;
- Service routing: kube-proxy/kernel;
- Pod networking: CNI/network implementation;
- HA coordination: quorum + leader election.
