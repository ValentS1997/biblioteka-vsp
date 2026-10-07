# Команды и инструменты главы 6

Only commands/configuration explicitly supported by RAG `p0102:c01–p0121:c01`.

## Command inventory

| Command / action | Type | Source purpose | Verification | Rollback |
|---|---|---|---|---|
| `kubectl create -f memcached-shards.yaml` | state-changing | создать memcached StatefulSet | three memcached containers expected | `[Needs confirmation]` |
| source Service creation instruction | state-changing, source-mismatched | создать headless Service | DNS names `memcache-N.memcache` expected | `[Needs confirmation]` |
| source twemproxy ConfigMap instruction | state-changing | создать ConfigMap from `nutcracker.yaml` | Pod references `twem-config` | `[Needs confirmation]` |
| `kubectl create -f memcached-ambassador-pod.yaml` | state-changing | deploy local Ambassador/twemproxy Pod | local proxy path available | `[Needs confirmation]` |
| source shared twemproxy ConfigMap instruction | state-changing | create ConfigMap for shared router | Deployment references `shared-twem-config` | `[Needs confirmation]` |
| `kubectl create -f shared-twemproxy-deploy.yaml` | state-changing | deploy replicated shared router | router replicas expected | `[Needs confirmation]` |
| `kubectl create -f shard-router-service.yaml` | state-changing | expose shared router via Service | named service exists | `[Needs confirmation]` |

## memcached StatefulSet

Source filename:
- `memcached-shards.yaml`.

Source command is split by PDF line wrapping but semantically reads:

~~~text
kubectl create -f memcached-shards.yaml
~~~

Effect:
- creates 3 memcached replicas in a StatefulSet.

Source details:
- image `memcached`;
- port `11211`;
- StatefulSet name `sharded-memcache`.

Rollback:
- `[Needs confirmation]`.

## Headless Service

Source file name:
- `memcached-service.yaml`.

However, the following prose tells the reader to deploy using `memcached-shards.yaml` again.

Classification:
- `[Source code mismatch]`.

Do not silently replace the command. See `source-findings.md`.

Source expected DNS names:
- `memcache-0.memcache`;
- `memcache-1.memcache`;
- additional ordinal instances accordingly.

## twemproxy ConfigMap

Source renders:

~~~text
kubectl create configmap --from-file=nutcracker.yaml twem-config
~~~

Classification:
- state-changing;
- exact copy/paste validity: `[Needs confirmation]`.

Purpose:
- provide twemproxy configuration to Ambassador Pod.

Do not reorder arguments from model knowledge.

## Ambassador Pod

Source command:

~~~bash
kubectl create -f memcached-ambassador-pod.yaml
~~~

Source Pod contains:
- `ganomede/twemproxy`;
- `nutcracker`;
- config path `/etc/config/nutcracker.yaml`;
- ConfigMap `twem-config`.

Extracted YAML formatting is not treated as production-copy-safe.

## Shared router ConfigMap

Source renders:

~~~text
kubectl create configmap --from-file=shared-nutcracker.yaml
shared-twem-config
~~~

Classification:
- state-changing;
- PDF line wrapping/exact syntax: `[Needs confirmation]`.

Purpose:
- configure shared twemproxy to listen on `0.0.0.0:11211`.

## Shared router Deployment

Source:

~~~bash
kubectl create -f shared-twemproxy-deploy.yaml
~~~

Effect:
- deploys 3 twemproxy replicas.

## Shared router Service

Source:

~~~bash
kubectl create -f shard-router-service.yaml
~~~

Effect:
- creates Service on port `11211` targeting shared twemproxy replicas.

## nginx consistent-sharding configuration

Source fragment:

~~~nginx
upstream backend {
  hash $request_uri consistent
  server web-shard-1.web;
  server web-shard-2.web;
  server web-shard-3.web;
}

server {
  listen localhost:80;
  location / {
    proxy_pass http://backend;
  }
}
~~~

Important:
- extracted line `hash $request_uri consistent` appears without a visible semicolon;
- do not silently normalize;
- exact executable nginx configuration: `[Needs confirmation]`.

## Workload-generating guidance

Chapter explicitly recommends load testing:
- with cache;
- without cache.

No concrete load-generator command is supplied.

## Safety boundary

Do not add from model memory:
- `kubectl delete/apply`;
- corrected Service filename command;
- reordered ConfigMap command;
- current Kubernetes API versions;
- memcache client commands;
- production resharding commands;
- autoscaler manifests.

Unsupported details remain `[Needs confirmation]`.
