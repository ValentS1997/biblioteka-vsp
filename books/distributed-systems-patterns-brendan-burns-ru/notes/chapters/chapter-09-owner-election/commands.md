# Команды и инструменты главы 9

Only commands explicitly supported by RAG `p0151:c01–p0170:c01`.

## Command inventory

| Command | Type | Source purpose | Verification | Rollback |
|---|---|---|---|---|
| `helm init` | state-changing | initialize Helm in source-era workflow | operator install can proceed | `[Needs confirmation]` |
| `helm install stable/etcd-operator` | state-changing | install etcd operator | operator resource appears implicitly | `[Needs confirmation]` |
| `kubectl create -f etcd-cluster.yaml` | state-changing | create 3-node etcd cluster | `kubectl get pods` | `[Needs confirmation]` |
| `kubectl get pods` | read-only | list etcd pods | 3 replicas expected | Not applicable |
| extracted `export ETCD_ENDPOINTS=...` | shell state change, source-defective | prepare endpoint list | later etcdctl uses variable | Not applicable |
| `kubectl exec ... etcdctl ... set foo bar` | state-changing | test write into etcd | command success | `[Needs confirmation]` |
| etcdctl lock acquire/release examples | state-changing | demonstrate mutex semantics | Bob CAS fails while Alice owns | source-specific |
| etcdctl TTL lease create/renew examples | state-changing | demonstrate renewable ownership | key persists while renewed | source-specific |

## Helm / etcd operator

Source:

~~~bash
helm init
helm install stable/etcd-operator
~~~

Classification:
- state-changing;
- historical/book-era toolchain.

Current Helm/operator compatibility:
- `[Needs confirmation]`.

Rollback:
- not supplied by chapter.

## etcd cluster creation

Source manifest:
- kind `Cluster`;
- name `my-etcd-cluster`;
- size `3`;
- version `3.1.0`.

Create:

~~~bash
kubectl create -f etcd-cluster.yaml
~~~

Verify:

~~~bash
kubectl get pods
~~~

Expected source result:
- three etcd replicas.

## Endpoint discovery

RAG extraction renders:

~~~text
export ETCD_ENDPOINTS=kubectl get endpoints example-etcd-cluster
"-o=jsonpath={.subsets[*].addresses[*].ip}:2379,"
~~~

Classification:
- `[Source extraction issue]`;
- `[Source code mismatch]`.

Reasons:
- shell command substitution syntax is not preserved clearly;
- cluster name `example-etcd-cluster` conflicts with earlier `my-etcd-cluster`.

Do not copy/paste as verified shell. See `source-findings.md`.

## Test write

Source renders:

~~~text
kubectl exec my-etcd-cluster-0000 -- sh -c "ETCD_API=3 etcdctl
--endpoints=${ETCD_ENDPOINTS} set foo bar"
~~~

Purpose:
- write key `foo` with value `bar`.

Exact line wrapping and current etcdctl/API behavior:
- `[Needs confirmation]`.

## Mutex initialization

Source:

~~~text
kubectl exec my-etcd-cluster-0000 -- sh -c   "ETCD_API=3 etcdctl --endpoints=${ETCD_ENDPOINTS} set
   my-lock unlocked"
~~~

Effect:
- create lock key with initial value `unlocked`.

## Alice acquires

Source:

~~~text
kubectl exec my-etcd-cluster-0000 -- sh -c   "ETCD_API=3 etcdctl --endpoints=${ETCD_ENDPOINTS}     set --swap-with-value unlocked my-lock alice"
~~~

Expected behavior:
- succeeds only if current value is `unlocked`.

## Bob contends

Source:

~~~text
kubectl exec my-etcd-cluster-0000 -- sh -c   "ETCD_API=3 etcdctl --endpoints=${ETCD_ENDPOINTS}     set --swap-with-value unlocked my-lock bob"
~~~

Source-observed result:
- compare fails because current owner is Alice.

## Alice releases

Source:

~~~text
kubectl exec my-etcd-cluster-0000 -- sh -c   "ETCD_API=3 etcdctl --endpoints=${ETCD_ENDPOINTS}     set --swap-with-value alice my-lock unlocked"
~~~

Purpose:
- release only if Alice still owns lock.

## Create 10-second lease

Source:

~~~text
kubectl exec my-etcd-cluster-0000 --   sh -c "ETCD_API=3 etcdctl --endpoints=${ETCD_ENDPOINTS}     --ttl=10 mk my-lock alice"
~~~

Effect:
- creates lock key only if absent;
- key expires after 10 seconds if not renewed.

## Renew lease

Source:

~~~text
kubectl exec my-etcd-cluster-0000 --   sh -c "ETCD_API=3 etcdctl --endpoints=${ETCD_ENDPOINTS}     set --ttl=10 --swap-with-value alice my-lock alice"
~~~

Effect:
- refreshes Alice's lease conditionally.

## Safety boundary

Do not add from model memory:
- modern Helm install procedure;
- current etcd operator manifests;
- current etcdctl v3 syntax;
- corrected endpoint export;
- delete/uninstall commands;
- production quorum/backup procedures;
- production lease/fencing libraries.

The chapter's commands are preserved as historical source evidence. Current executable replacements remain `[Needs confirmation]`.
