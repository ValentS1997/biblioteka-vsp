# Команды и инструменты главы 5

Only commands/configuration explicitly supported by RAG `p0082:c01–p0101:c01`.

## Command inventory

| Command | Type | Source purpose | Verification | Rollback |
|---|---|---|---|---|
| `docker run -p 8080:8080 brendanburns/dictionary-server` | state-changing | локально запустить dictionary-server | open `http://localhost:8080/dog` | `[Needs confirmation]` |
| `kubectl create -f dictionary-deploy.yaml` | state-changing | создать replicated Deployment | readiness/replicas implied by manifest | `[Needs confirmation]` |
| `kubectl create -f dictionary-service.yaml` | state-changing | создать Service/load-balancer abstraction | stable service endpoint | `[Needs confirmation]` |
| Varnish ConfigMap creation fragment | state-changing | создать ConfigMap из `default.vcl` | Deployment consumes `varnish-config` | `[Needs confirmation]` |
| `kubectl create -f varnish-deploy.yaml` | state-changing | создать replicated Varnish cache tier | replicas become available | `[Needs confirmation]` |
| `kubectl create -f varnish-service.yaml` | state-changing | expose Varnish tier | `varnish-service` routes to cache | `[Needs confirmation]` |
| `kubectl create secret tls ssl --cert=server.crt --key=server.key` | state-changing / security-sensitive | загрузить TLS cert/key как Secret | nginx references Secret `ssl` | `[Needs confirmation]` |
| `kubectl create configmap nginx-conf --from-file=nginx.conf` | state-changing | создать nginx ConfigMap | Deployment references `nginx-conf` | `[Needs confirmation]` |
| `kubectl create -f nginx-deploy.yaml` | state-changing | создать replicated nginx SSL tier | replicas expose 443 | `[Needs confirmation]` |
| `kubectl create -f nginx-service.yaml` | state-changing | создать external LoadBalancer Service | `kubectl get services` | `[Needs confirmation]` |
| `kubectl get services` | read-only | получить Service/external address | address shown when supported | Not applicable |

## Local dictionary-server

Source:

~~~bash
docker run -p 8080:8080 brendanburns/dictionary-server
~~~

Effect:
- starts local dictionary service on port 8080.

Source verification:
- browse/request `http://localhost:8080/dog`.

Risk:
- starts a local runtime container and binds host port 8080.

Rollback:
- exact source-supported stop/remove command: `[Needs confirmation]`.

## Kubernetes application tier

Source Deployment:
- `replicas: 3`;
- image `brendanburns/dictionary-server`;
- container port `8080`;
- readiness path `/ready`;
- `initialDelaySeconds: 5`;
- `periodSeconds: 5`.

Create:

~~~bash
kubectl create -f dictionary-deploy.yaml
~~~

Load-balancing Service:

~~~bash
kubectl create -f dictionary-service.yaml
~~~

Rollback:
- `[Needs confirmation]`.

## Varnish ConfigMap

RAG-extracted source is line-wrapped as:

~~~text
kubectl create configmap varnish-config
--from-file=default.vcl
~~~

Classification:
- state-changing;
- `[Source extraction issue]`.

The semantic intent is to create `varnish-config` from `default.vcl`, but this artifact does not silently normalize the wrapped text into a guaranteed copy/paste-safe shell line.

Exact executable formatting:
- `[Needs confirmation]`.

## Varnish replicated cache

Source commands:

~~~bash
kubectl create -f varnish-deploy.yaml
kubectl create -f varnish-service.yaml
~~~

Source architecture:
- 2 Varnish replicas;
- backend `dictionary-server-service:8080`;
- cache listener `0.0.0.0:8080`;
- Service port `80` → targetPort `8080`.

The source example associates approximately 2 GiB requested memory with `malloc,2G` cache allocation.

Exact current resource semantics/API compatibility:
- `[Needs confirmation]`.

## TLS Secret

Source:

~~~bash
kubectl create secret tls ssl --cert=server.crt --key=server.key
~~~

Classification:
- state-changing;
- security-sensitive.

Effect:
- stores certificate/private-key material in a Kubernetes Secret named `ssl`.

Risk:
- private key is sensitive material;
- chapter does not define secret rotation/access-control procedure.

Verification:
- nginx Deployment later references `secretName: ssl`.

Rollback:
- `[Needs confirmation]`.

## nginx SSL tier

Create config:

~~~bash
kubectl create configmap nginx-conf --from-file=nginx.conf
~~~

Create replicated tier:

~~~bash
kubectl create -f nginx-deploy.yaml
~~~

Expose it:

~~~bash
kubectl create -f nginx-service.yaml
~~~

Read-only check:

~~~bash
kubectl get services
~~~

Source expectation:
- if the Kubernetes cluster supports external load balancers, the Service gets an external address.

## Rate limiting

Chapter discusses:
- Varnish throttle-like rate limiting;
- HTTP `429` after limit exceeded;
- remaining-quota header such as `X-RateLimit-Remaining`.

No exact source command/config snippet for throttle is provided.

## Safety boundary

Do not add from model memory:
- current replacement APIs;
- delete/rollback commands;
- current TLS/cert-manager procedures;
- Varnish throttle configuration;
- readiness diagnostic commands;
- deployment rollout/status commands.

Unsupported details remain `[Needs confirmation]`.
