# Команды и инструменты главы 3

Only commands/configuration explicitly supported by RAG `p0050:c01–p0063:c01`.

## Command inventory

| Command | Type | Source purpose | Verification | Rollback |
|---|---|---|---|---|
| `kubectl create -f redis-shards.yaml` | state-changing | создать resource(s) из Redis manifest | `kubectl get pods` for pod visibility | `[Needs confirmation]` |
| `kubectl get pods` | read-only | показать pods | expected Redis pod names visible | Not applicable |
| `kubectl create configmap twem-config --from-file=./nutcracker.yaml` | state-changing | создать ConfigMap twemproxy | Ambassador consumes config in Pod manifest | `[Needs confirmation]` |
| `kubectl create configmaps --from-file=nginx.conf` | state-changing, source-defective | intended creation of nginx experiment config | later Pod expects `experiment-config` | `[Needs confirmation]` |

## Redis StatefulSet deployment

Source introduces a StatefulSet named `sharded-redis` with `replicas: 3`, Redis container and port `6379`.

Source command:

~~~bash
kubectl create -f redis-shards.yaml
~~~

Effect:
- creates Kubernetes object(s) described by the file.

Verification:

~~~bash
kubectl get pods
~~~

Source-expected pod pattern:

~~~text
sharded-redis-[0,1,2]
~~~

Rollback:
- `[Needs confirmation]`.

## Redis Service / DNS

Source then shows a headless Service:
- name `redis`;
- port `6379`;
- `clusterIP: None`;
- selector `app: redis`.

The source again says to save this code as `redis-shards.yaml` and run the same create command. This creates an operational ambiguity because the same filename/command was already used for the StatefulSet. See `source-findings.md`.

Source expects DNS names:
- `sharded-redis-0.redis`;
- `sharded-redis-1.redis`;
- `sharded-redis-2.redis`.

Exact DNS verification command: `[Needs confirmation]`.

## twemproxy configuration

Source configuration includes:

~~~yaml
redis:
  listen: 127.0.0.1:6379
  hash: fnv1a_64
  distribution: ketama
  auto_eject_hosts: true
  redis: true
  timeout: 400
  server_retry_timeout: 2000
  server_failure_limit: 1
  servers:
    - sharded-redis-0.redis:6379:1
    - sharded-redis-1.redis:6379:1
    - sharded-redis-2.redis:6379:1
~~~

Create ConfigMap:

~~~bash
kubectl create configmap twem-config --from-file=./nutcracker.yaml
~~~

Rollback: `[Needs confirmation]`.

## Ambassador Pod for twemproxy

Source Pod uses:
- image `ganomede/twemproxy`;
- command `nutcracker`;
- config path `/etc/config/nutcracker.yaml`;
- ConfigMap volume `twem-config`.

RAG indentation in this YAML should not be silently normalized into a copy/paste production manifest; use it as chapter structure unless separately verified.

## nginx 10% experiment configuration

Source nginx fragment:

~~~nginx
upstream backend {
  ip_hash;
  server web weight=9;
  server experiment;
}

server {
  listen localhost:80;
  location / {
    proxy_pass http://backend;
  }
}
~~~

Source interpretation:
- production/backend `web`: weight 9;
- `experiment`: remaining share;
- `ip_hash`: keeps user consistently routed.

Source command:

~~~text
kubectl create configmaps --from-file=nginx.conf
~~~

Classification:
- state-changing;
- `[Source code mismatch]`.

Later Ambassador Pod references ConfigMap `experiment-config`, but this source command does not provide that name. Exact executable replacement: `[Needs confirmation]`.

## Service prerequisites for experiment

Source requires services:
- `experiment`;
- `web`.

It states nginx will not start correctly if it cannot find proxy targets.

The chapter supplies Service YAML but no dedicated creation command for those specific files in the retrieved range.

## Safety boundary

Do not add from model memory:
- alternative deployment commands;
- rollback/delete commands;
- service DNS diagnostic commands;
- Redis CLI commands;
- corrected ConfigMap command;
- updated Kubernetes API versions.

Those are outside chapter RAG.
