# Команды главы 16

Source policy: RAG-only. Read-only inspection and scheduling-policy changes are separated.

## Inspect node taints

~~~bash
kubectl describe node master.k8s
~~~

Read-only.

Source output includes:

~~~text
Taints: node-role.kubernetes.io/master:NoSchedule
~~~

## Inspect Pod tolerations

~~~bash
kubectl describe po kube-proxy-80wqm -n kube-system
~~~

Read-only.

Source shows tolerations including:
- master NoSchedule;
- notReady NoExecute;
- unreachable NoExecute.

## Add taint

~~~bash
kubectl taint node node1.k8s node-type=production:NoSchedule
~~~

STATE-CHANGING SCHEDULING POLICY.

Effect:
new Pods without matching toleration cannot schedule onto node1.

Verification:

~~~bash
kubectl get po -o wide
~~~

## Deploy source test workload

~~~bash
kubectl run test --image busybox --replicas 5 -- sleep 99999
~~~

STATE-CHANGING workload creation.

Source purpose:
show that ordinary Pods avoid tainted production node.

## Inspect default NoExecute tolerations

~~~bash
kubectl get po prod-350605-1ph5h -o yaml
~~~

Read-only.

Source fields include tolerationSeconds: 300 for notReady/unreachable.

## Taint rollback

Exact taint-removal command is not shown in verified source excerpts.

Command: [Needs confirmation].

Do not reconstruct from memory.

## Label nodes for affinity

~~~bash
kubectl label node node1.k8s availability-zone=zone1
kubectl label node node1.k8s share-type=dedicated
kubectl label node node2.k8s availability-zone=zone2
kubectl label node node2.k8s share-type=shared
~~~

STATE-CHANGING SCHEDULING METADATA.

Inspect:

~~~bash
kubectl get node -L availability-zone -L share-type
~~~

Read-only.

Changing/removing these labels can alter future placement of Pods using nodeAffinity.

## Inspect preferred node-affinity placement

~~~bash
kubectl get po -o wide
~~~

Read-only.

Source shows most Pods on preferred node but not necessarily all, because other scheduler priority functions also contribute.

## Scale-to-20 demonstration

Source says the reader may try scaling preferred-deployment to 20 or more Pods.

Exact scale command is not shown in verified source excerpt.

Command: [Needs confirmation].

## Create backend workload for podAffinity example

~~~bash
kubectl run backend -l app=backend --image busybox -- sleep 999999
~~~

STATE-CHANGING workload creation.

Source-era kubectl run semantics preserved.

## Inspect backend placement

~~~bash
kubectl get po -o wide
~~~

Read-only.

## Create frontend pod-affinity deployment

~~~bash
kubectl create -f frontend-podaffinity-host.yaml
~~~

STATE-CHANGING.

Hard rule:
frontend Pods require same hostname topology domain as Pod app=backend.

Verify:

~~~bash
kubectl get po -o wide
~~~

Expected source example:
frontend Pods land on same node as backend.

## Anti-affinity verification

Source deployment manifest:
frontend-podantiaffinity-host.yaml.

The exact create command is not shown in the verified excerpt.

Command: [Needs confirmation].

Read-only verification:

~~~bash
kubectl get po -l app=frontend -o wide
~~~

Source result on two-node cluster with five replicas:
- one frontend Pod per node Running;
- remaining replicas Pending due to hard hostname anti-affinity.

## Risk matrix

| Operation | Class |
|---|---|
| kubectl describe/get | read-only |
| kubectl taint node | scheduling-policy change |
| kubectl label node | scheduling-metadata change |
| kubectl run/create workload | workload creation |
| NoSchedule taint | future placement restriction |
| PreferNoSchedule | soft placement preference |
| NoExecute taint | high-impact: may evict running Pods |
| required node/pod affinity | hard scheduling constraint |
| required pod anti-affinity | hard separation; can cause Pending Pods |
