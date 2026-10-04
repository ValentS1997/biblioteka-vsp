# Шпаргалка: StatefulSet identity, storage и failure handling

## 1. ReplicaSet vs StatefulSet

ReplicaSet:
- replicas interchangeable;
- random Pod suffixes;
- one shared Pod template;
- no stable individual identity.

StatefulSet:
- stable ordinal;
- stable hostname;
- stable per-Pod PVC;
- ordered create/delete.

## 2. Stable identity

~~~text
StatefulSet kubia
  ├─ kubia-0
  ├─ kubia-1
  └─ kubia-2
~~~

Replacement of kubia-0 remains kubia-0.

It may move to another node while keeping:
- Pod name;
- hostname;
- associated PVC/storage.

## 3. Headless governing Service

Source pattern:

~~~text
spec:
  clusterIP: None
  selector:
    app: kubia
~~~

StatefulSet:

~~~text
serviceName: kubia
~~~

Purpose:
- stable DNS identity;
- peer discovery;
- no single virtual ClusterIP endpoint.

## 4. Per-Pod storage

~~~text
volumeClaimTemplates:
  name: data
      ↓
data-kubia-0 → PV
data-kubia-1 → PV
data-kubia-2 → PV
~~~

Pod template mounts volume named data; StatefulSet injects a per-Pod PVC-backed volume.

## 5. Scale semantics

Scale up:
- create lowest missing ordinal;
- wait until Pod ready;
- then create next Pod.

Scale down:
- delete highest ordinal first;
- wait for full termination;
- then continue.

PVC:
- remains after scale-down;
- reused if ordinal later returns.

## 6. Peer discovery

DNS SRV query:

~~~bash
kubectl run -it srvlookup --image=tutum/dnsutils --rm   --restart=Never -- dig SRV kubia.default.svc.cluster.local
~~~

Expected source model:
- SRV records point to Pod hostnames;
- additional A records provide Pod IPs;
- result order is not guaranteed.

Application example:
~~~text
dns.resolveSrv("kubia.default.svc.cluster.local", ...)
~~~

## 7. Client access vs peer discovery

Client traffic:
~~~text
client → ordinary ClusterIP Service → random StatefulSet Pod
~~~

Peer discovery:
~~~text
Pod → headless Service DNS/SRV → all peer hostnames
~~~

## 8. StatefulSet update source-era behavior

Source demo:

~~~bash
kubectl edit statefulset kubia
~~~

Changes:
- replicas 2 → 3;
- image → kubia-pet-peers.

In source-era initial behavior:
- new kubia-2 uses new template;
- existing kubia-0/kubia-1 remain old;
- source manually deletes old Pods to recreate them.

Source note:
Kubernetes 1.7+ introduced StatefulSet updateStrategy.

No modernization beyond this source statement.

## 9. Failure semantics

Node network lost:

~~~text
node → NotReady
Pod → Unknown / Terminating
old process may still be running
~~~

StatefulSet does not safely create replacement because old Pod may still own identity/storage.

## 10. Force-delete boundary

Source command:

~~~bash
kubectl delete po kubia-0 --force --grace-period 0
~~~

CRITICAL RISK.

This removes API object without confirmation that old process stopped.

Only acceptable when administrator knows old node/Pod is permanently unavailable.

Potential failure:
~~~text
old kubia-0 still alive
+
new kubia-0 created
=
duplicate identity / shared-storage conflict
~~~

## 11. Source recovery for failure injection

~~~bash
gcloud compute instances reset <node-name>
~~~

Used to restore disabled GCE node after lab.

## Acceptance model

Healthy StatefulSet:
- expected ordinals Running/Ready;
- each Pod has distinct PVC;
- replacement retains same PVC;
- headless DNS exposes peers;
- ordinary Service can distribute client requests;
- no duplicate ordinal identity exists.

Before force deletion:
- exact failed node identified;
- old workload confirmed irrecoverably stopped/unreachable;
- storage attachment implications understood;
- recovery/rollback path available.
