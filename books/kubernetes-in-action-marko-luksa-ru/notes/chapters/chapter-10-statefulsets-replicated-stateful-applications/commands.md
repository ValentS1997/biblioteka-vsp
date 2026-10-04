# Команды главы 10

Source policy: RAG-only. Read-only, state-changing, infrastructure-changing and critical failure-injection commands are separated.

## Create GCE persistent disks

Source example:

~~~bash
gcloud compute disks create --size=1GiB --zone=<zone> pv-a
gcloud compute disks create --size=1GiB --zone=<zone> pv-b
gcloud compute disks create --size=1GiB --zone=<zone> pv-c
~~~

STATE-CHANGING cloud infrastructure.

Source requirement:
- disks must be in same zone as nodes.

Rollback/delete disk command: [Needs confirmation] — not provided in chapter excerpt.

## Create StatefulSet

Source:

~~~bash
kubectl create -f kubia-statefulset.yaml
~~~

STATE-CHANGING.

Read-only observation:

~~~bash
kubectl get po
kubectl get po kubia-0 -o yaml
kubectl get pvc
~~~

Expected:
- Pods appear sequentially;
- first Pod must become Ready before next is created;
- PVC names include claim template + Pod name.

## API proxy to Pod

Start local proxy:

~~~bash
kubectl proxy
~~~

Local process/network listener.

Read-only GET:

~~~bash
curl localhost:8001/api/v1/namespaces/default/pods/kubia-0/proxy/
~~~

Source note:
trailing slash matters unless curl follows redirects.

## Write Pod-local state

Source pattern:

~~~bash
curl -X POST -d "Hey there! This greeting was submitted to kubia-0."   localhost:8001/api/v1/namespaces/default/pods/kubia-0/proxy/
~~~

APPLICATION DATA CHANGE.

Verify:

~~~bash
curl localhost:8001/api/v1/namespaces/default/pods/kubia-0/proxy/
curl localhost:8001/api/v1/namespaces/default/pods/kubia-1/proxy/
~~~

Expected:
- kubia-0 returns stored data;
- kubia-1 has separate state.

## Delete/recreate Pod to verify stable identity/storage

~~~bash
kubectl delete po kubia-0
~~~

STATE-CHANGING but normal graceful deletion.

Observe:

~~~bash
kubectl get po
~~~

After StatefulSet replacement:

~~~bash
curl localhost:8001/api/v1/namespaces/default/pods/kubia-0/proxy/
~~~

Expected:
- same Pod name;
- same hostname;
- same stored data;
- possibly different worker node.

## StatefulSet scale behavior

Source explicitly invites trying scale-down/up but exact scale command is not present in retrieved excerpt.

Command: [Needs confirmation].

Expected source behavior:
- highest ordinal removed first;
- PVC remains;
- later scale-up reuses existing PVC.

No kubectl scale line is reconstructed from memory.

## Access via ordinary Service through API proxy

Source path:

~~~bash
curl localhost:8001/api/v1/namespaces/default/services/kubia-public/proxy/
~~~

Read-only/workload-generating GET.

## DNS SRV peer discovery

Source-era command:

~~~bash
kubectl run -it srvlookup --image=tutum/dnsutils --rm   --restart=Never -- dig SRV kubia.default.svc.cluster.local
~~~

STATE-CHANGING temporary Pod creation, automatically deleted by --rm after completion.

Expected:
- SRV records for each StatefulSet Pod;
- A records for Pod IPs.

## Update StatefulSet template

~~~bash
kubectl edit statefulset kubia
~~~

STATE-CHANGING interactive edit.

Source changes:
- spec.replicas to 3;
- image to luksa/kubia-pet-peers.

Observe:

~~~bash
kubectl get po
~~~

Source-era result:
- new kubia-2 uses new template;
- existing kubia-0 and kubia-1 remain old.

Source manual replacement:

~~~bash
kubectl delete po kubia-0 kubia-1
~~~

DESTRUCTIVE to Pods but StatefulSet recreates them.

Source note:
Kubernetes 1.7+ supports StatefulSet rolling updates via spec.updateStrategy.

## Clustered-storage demo

Write through Service proxy:

~~~bash
curl -X POST -d "The sun is shining"   localhost:8001/api/v1/namespaces/default/services/kubia-public/proxy/

curl -X POST -d "The weather is sweet"   localhost:8001/api/v1/namespaces/default/services/kubia-public/proxy/
~~~

APPLICATION DATA CHANGE.

Read cluster view:

~~~bash
curl localhost:8001/api/v1/namespaces/default/services/kubia-public/proxy/
~~~

Expected:
- receiving Pod discovers peers via SRV;
- queries /data on peers;
- returns collected values.

## Failure injection — HIGH RISK

Source requires multi-node GKE.

SSH to chosen worker:

~~~bash
gcloud compute ssh <node-name>
~~~

Then:

~~~bash
sudo ifconfig eth0 down
~~~

CRITICAL NETWORK FAILURE INJECTION.

Effects:
- SSH session drops;
- node eventually becomes NotReady;
- Pod on node becomes Unknown/Terminating;
- workload process may still be running even though control plane cannot confirm it.

Do not run on production/control-plane/only reachable node.

## Observe failed node and Pod

Read-only:

~~~bash
kubectl get node
kubectl get po
kubectl describe po kubia-0
~~~

Source observations:
- Node NotReady;
- Pod Unknown then Terminating;
- Reason NodeLost.

## Ordinary Pod deletion during lost-node condition

~~~bash
kubectl delete po kubia-0
~~~

STATE-CHANGING.

Source result:
- API reports deleted;
- Pod remains visible because termination cannot be confirmed by unreachable Kubelet;
- StatefulSet does not create replacement yet.

## Force-delete stateful Pod — CRITICAL RISK

~~~bash
kubectl delete po kubia-0 --force --grace-period 0
~~~

CRITICAL / potential split-brain and data corruption.

Source warning:
immediate deletion does not wait for confirmation that running resource terminated.

Precondition:
only when administrator knows old node/Pod is no longer running and will remain unavailable.

After force-delete:

~~~bash
kubectl get po
~~~

Expected:
- new kubia-0 starts on healthy node.

## Recover failure-injected node

Source-supported recovery:

~~~bash
gcloud compute instances reset <node-name>
~~~

STATE-CHANGING infrastructure recovery.

Important:
if old stateful workload could still be running, restore/reconnect decisions must account for duplicate identity/storage risk.

## Risk matrix

| Operation | Class |
|---|---|
| kubectl get/describe | read-only |
| kubectl proxy | local proxy process |
| curl GET | workload-generating/read-only application request |
| curl POST | application data change |
| create/edit StatefulSet | cluster state change |
| delete normal StatefulSet Pod | workload state change |
| create GCE disks | cloud infrastructure state change |
| ifconfig eth0 down | critical network failure injection |
| force delete stateful Pod | critical split-brain/data risk |
| gcloud reset node | infrastructure recovery |
