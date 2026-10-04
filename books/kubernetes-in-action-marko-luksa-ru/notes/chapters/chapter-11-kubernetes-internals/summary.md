# Резюме главы 11

Источник: явный раздел 11.7 Резюме, RAG chunk p0424:c01.

Глава показывает:

- какие components образуют Kubernetes cluster и за что каждый отвечает;
- как API server, scheduler, controllers и Kubelet совместно приводят Pod к running state;
- как infrastructure/pause container связывает containers одного Pod через shared namespaces;
- как Pods на одном node общаются через bridge и как node networks соединяются для cross-node traffic;
- как kube-proxy реализует Service load balancing через iptables rules;
- как multiple control-plane component instances делают cluster highly available.

## Центральная модель

~~~text
cluster state
    ↓
   etcd
    ↑
API server
  ├─ scheduler watches/assigns
  ├─ controllers watch/reconcile
  ├─ Kubelet watches/executes
  └─ kube-proxy watches/programs service routing
~~~

## Architectural conclusion

Большая часть Kubernetes coordination происходит не через прямые вызовы одного component к другому, а через shared API objects и watches.

Это объясняет:
- weak coupling components;
- declarative behavior;
- independent reconciliation;
- restartability components;
- возможность HA через replicated API/control-plane instances.

## Provenance

- Chapter chunks: p0383:c01–p0424:c01
- Summary chunk: p0424:c01
- PDF page: 424
- Printed page: 423
- Source SHA-256: 0d50f167ed86088d0cc65d15e27f1ab397e7c0a0c8de4db3801b50439f24266f
