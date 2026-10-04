# Шпаргалка: application lifecycle в Kubernetes

## 1. Design assumption

~~~text
Pod may disappear
Container may restart
Pod IP may change
Node may change
~~~

Therefore:
- do not depend on stable Pod IP;
- persist required state in volumes/external storage;
- handle restart and relocation.

## 2. Container writable layer

~~~text
container restart
→ new container
→ new writable layer
→ old files lost
~~~

Use volume when data must survive container restart inside same Pod.

## 3. CrashLoopBackOff nuance

ReplicaSet compares desired Pod count, not application health inside each Pod.

Source example:
3 Pods exist, all containers crash-loop → ReplicaSet still sees 3 current / 3 desired.

## 4. Startup ordering

Kubernetes stores submitted objects in order but does not guarantee application startup order.

Use init containers for prerequisite gating.

## 5. Init containers

~~~text
init #1
  ↓ success
init #2
  ↓ success
main containers start
~~~

Source example:
init container loops until Service fortune responds.

Inspect:

~~~bash
kubectl get po
kubectl logs fortune-client -c init
~~~

## 6. postStart

Runs after main process starts.

Important:
- runs concurrently with application initialization;
- container stays Waiting/ContainerCreating until hook completes;
- hook failure may terminate main container.

Failure diagnosis:
Pod events / kubectl describe.

## 7. preStop

Sequence:

~~~text
termination starts
  ↓
preStop hook
  ↓
SIGTERM to main process
  ↓
wait grace period
  ↓
SIGKILL if still running
~~~

preStop is per-container, not per-Pod.

## 8. Signal handling

Prefer:
- application handles SIGTERM;
- direct executable ENTRYPOINT/CMD;
- or shell explicitly forwards signal.

Source warns shell wrapper may swallow SIGTERM.

## 9. termination grace period

Source default:

~~~text
30 seconds
~~~

Can be overridden per Pod via:

~~~text
spec.terminationGracePeriodSeconds
~~~

Delete override:

~~~bash
kubectl delete po mypod --grace-period=5
~~~

## 10. Force delete

~~~bash
kubectl delete po mypod --grace-period=0 --force
~~~

CRITICAL.

API object may disappear before process stops.

StatefulSet risk:
old and replacement instances may run simultaneously.

## 11. Startup traffic safety

Without readiness probe:
Pod is considered ready immediately.

Correct model:

~~~text
application not ready
→ readiness fails
→ Pod absent from Service Endpoints

application ready
→ readiness succeeds
→ traffic allowed
~~~

## 12. Shutdown traffic race

~~~text
Pod deletion
├─ Kubelet → preStop/SIGTERM
└─ API/controller → Endpoints update
                  → kube-proxy/other routers update
~~~

These paths are asynchronous.

Therefore SIGTERM may arrive before all routers stop forwarding.

## 13. Source graceful request flow

~~~text
SIGTERM
  ↓
wait a few seconds
  ↓
stop accepting new connections
  ↓
close idle keep-alive connections
  ↓
finish active requests
  ↓
exit
~~~

Minimal source mitigation:

~~~text
preStop:
  exec:
    command:
    - sh
    - -c
    - "sleep 5"
~~~

## 14. Image practices

Prefer version tags over latest.

Problem with latest:
- replicas can run different image versions;
- rollback identity becomes ambiguous.

imagePullPolicy Always:
- checks registry on each new Pod start;
- startup depends on registry reachability.

## 15. Resource metadata

Labels:
- app/service;
- tier;
- environment;
- version;
- release type;
- tenant/client;
- shard.

Annotations:
- description;
- owner/contact;
- build/version metadata;
- tool metadata;
- dependency information.

## 16. Termination message

Default source path:

~~~text
/dev/termination-log
~~~

Custom:

~~~text
terminationMessagePath: /var/termination-reason
~~~

Kubelet exposes content through Pod status / kubectl describe.

## 17. Logging

Preferred:
application → stdout/stderr → kubectl logs / node log collector.

Source central logging:

~~~text
containers
  ↓
FluentD per node
  ↓
Elasticsearch
  ↓
Kibana
~~~

## 18. File transfer

~~~bash
kubectl cp foo-pod:/var/log/foo.log foo.log
kubectl cp localfile foo-pod:/etc/remotefile
~~~

State impact:
second command writes into container filesystem.

## 19. Local development

Source choices:
- run application directly in IDE/local OS;
- point local env vars to cluster/external services;
- access API through local kubectl proxy;
- use Minikube for Kubernetes-specific behavior.

Credential boundary:
local developer identity should have intended permissions.

## 20. Minikube image iteration

~~~bash
eval $(minikube docker-env)
~~~

Then local docker CLI builds into Minikube VM daemon.

Alternative source:

~~~bash
docker save <image> | (eval $(minikube docker-env) && docker load)
~~~

Ensure imagePullPolicy is not Always for copied local image.

## 21. Declarative delivery

~~~text
manifests in VCS
  ↓
review/audit/history
  ↓
kubectl apply
  ↓
desired cluster state
~~~

Source mentions kube-applier for automated apply.

## 22. Ksonnet / Jsonnet

Source-era pattern:
parameterized fragments → generated JSON manifest.

~~~bash
jsonnet kubia.ksonnet
~~~

## 23. CI/CD

Source pipeline goal:

~~~text
build application
→ build container image
→ build/version manifests
→ deploy to one or more Kubernetes clusters
~~~

## Acceptance model

Application:
- startup gated by readiness;
- SIGTERM tested;
- shutdown finishes active requests;
- grace period sufficient;
- state survives intended restart scenarios;
- logs and termination reason observable.

Delivery:
- image version identifiable;
- manifests version-controlled;
- labels/annotations present;
- deployment automated but auditable.
