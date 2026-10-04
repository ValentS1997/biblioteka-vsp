# Ответ к упражнению главы 10

Это RAG-grounded procedure, не официальный издательский answer key.

## Упражнение 1 — StatefulSet при аварийном отключении node

### Preconditions

Source requires:
- multi-node GKE;
- known worker node hosting target StatefulSet Pod;
- ability to recover/reset that node.

Do not perform this on production or on a node whose loss would remove your only management path.

### Step 1. Inject network failure

Connect to chosen worker:

~~~bash
gcloud compute ssh <node-name>
~~~

On worker:

~~~bash
sudo ifconfig eth0 down
~~~

Expected:
- SSH disconnects;
- Kubelet loses API-server connectivity.

### Step 2. Observe control-plane state

~~~bash
kubectl get node
kubectl get po
~~~

Expected source behavior:
- node becomes NotReady;
- affected Pod becomes Unknown.

Later:

~~~bash
kubectl describe po kubia-0
~~~

Expected:
- Terminating;
- Reason: NodeLost.

Important: this is control-plane view. Source explicitly states the actual container may still be running.

### Step 3. Try normal Pod deletion

~~~bash
kubectl delete po kubia-0
kubectl get po
~~~

Expected:
- kubectl reports deletion request;
- old Pod object remains visible/terminating;
- StatefulSet does not create replacement.

Reason:
Kubelet on isolated node cannot confirm container termination.

### Step 4. Decide whether force-delete is safe

Do not continue unless administrator knows:
- old node will not return in its current workload state;
- old kubia-0 is no longer actually running or is otherwise fenced;
- creating a replacement cannot result in two instances using same identity/storage.

If this is not verified: stop. State is [Unsafe to force-delete].

### Step 5. Force-delete only after fencing/confirmation

Source command:

~~~bash
kubectl delete po kubia-0 --force --grace-period 0
~~~

Expected:
- API object removed immediately;
- StatefulSet creates a new kubia-0 on an available node.

Verification:

~~~bash
kubectl get po
~~~

### Why StatefulSet waits

StatefulSet promises at-most-one instance for a stable identity.

If Kubernetes created a new kubia-0 while the isolated old kubia-0 was still running, both could operate under the same logical identity and potentially use the same storage. Source treats this as unacceptable.

### Step 6. Recover source lab node

~~~bash
gcloud compute instances reset <node-name>
~~~

This is source-supported recovery for the injected GCE node failure.

## Acceptance criteria

- node failure appears as NotReady;
- affected StatefulSet Pod becomes Unknown/Terminating;
- normal delete does not cause unsafe duplicate replacement;
- force-delete is performed only after old instance is known dead/fenced;
- replacement keeps ordinal identity kubia-0;
- lab node can be restored with source recovery command.

## Provenance

- p0378:c01–p0382:c01
