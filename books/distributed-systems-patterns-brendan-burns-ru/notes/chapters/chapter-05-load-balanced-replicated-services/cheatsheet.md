# Шпаргалка: глава 5 — Реплицированные сервисы с распределением нагрузки

## Symptom / problem framing

Нужно:
- выдерживать отказ/обновление instance;
- обслуживать растущую нагрузку;
- дать clients стабильный endpoint;
- не слать traffic в not-ready replicas.

Pattern:

~~~text
replicated stateless instances
+ load balancer
+ readiness
→ availability + horizontal scale
~~~

## Baseline / context

Basic topology:

~~~text
client
→ Service / load balancer
→ replica 1
→ replica 2
→ replica N
~~~

Extended chapter topology:

~~~text
HTTPS client
→ nginx replicated SSL tier
→ Varnish replicated cache tier
→ replicated application tier
~~~

## Read-only checks

1. Service действительно stateless для данного request path?
2. Сколько replicas нужно для redundancy/capacity?
3. Есть ли readiness endpoint?
4. Чем readiness отличается от simple process health?
5. Есть ли session affinity?
6. Не скрывает ли proxy/cache real client identity?
7. Cache и application должны масштабироваться одинаково или независимо?
8. Какой layer владеет TLS termination?
9. Есть ли rate-limit behavior/HTTP 429 semantics?
10. Как проверить external Service address?

Source does not provide universal SLO/capacity formula beyond illustrative examples.

## Interpretation

### One instance

~~~text
single replica
→ update/failure can consume availability budget
~~~

### Multiple instances

~~~text
replicas + load balancer
→ one instance can update/fail
→ others continue serving
~~~

### Healthy but not ready

~~~text
process alive
+ initialization incomplete
→ do not route user traffic
~~~

### Sticky sessions

~~~text
user
→ affinity function
→ same replica
~~~

Use when cache locality/state between requests matters.

### Cache tier

~~~text
few larger cache replicas
→ higher aggregate cache utility
→ independently scaled from many app replicas
~~~

### SSL bridge

~~~text
nginx
→ terminate HTTPS
→ forward HTTP to Varnish
→ Varnish forwards to app
~~~

## Next action

1. Identify stateless request-serving component.
2. Add replication.
3. Add readiness contract.
4. Expose stable load-balanced endpoint.
5. Verify traffic reaches only ready replicas.
6. Decide whether affinity is needed.
7. Add independent cache layer if repeated HTTP work benefits from it.
8. Add rate policy/SSL edge layer where required.
9. Remeasure availability, latency and capacity.

Steps 5 and 9 require environment-specific measurements not supplied by chapter.

## Modifying action

Source-supported modifying commands are listed in `commands.md`.

They create:
- local Docker workload;
- Kubernetes Deployment/Service resources;
- Varnish ConfigMap/Deployment/Service;
- TLS Secret;
- nginx ConfigMap/Deployment/Service.

Risk:
- changes cluster/runtime state;
- TLS Secret handles private-key material;
- old Kubernetes manifest schemas may not match current clusters: `[Needs confirmation]`.

## Verification / acceptance checks

### dictionary-server
- replicas exist after Deployment creation;
- Service gives stable endpoint;
- `/ready` controls readiness;
- local test responds on port 8080.

### cache tier
- Varnish routes to `dictionary-server-service:8080`;
- cache replicas are independently deployed;
- `varnish-service` exposes cache layer.

### SSL tier
- TLS Secret exists;
- nginx config points to `varnish-service:80`;
- nginx replicas expose 443;
- LoadBalancer Service gets external address where cluster supports it.

Exact functional test commands are partly absent: `[Needs confirmation]`.

## Rollback

Chapter gives no complete rollback sequence.

- dictionary Deployment/Service: `[Needs confirmation]`;
- Varnish resources: `[Needs confirmation]`;
- TLS Secret/nginx resources: `[Needs confirmation]`.

Do not invent delete/rollback commands.

## Sticky-session warning

~~~text
IP affinity + cache/proxy
→ backend sees proxy IP
→ affinity can collapse onto few replicas
~~~

For external users chapter prefers application-level affinity such as cookies; HTTP headers are also mentioned for preserving useful routing context.

## Operational layering rule

Scale by responsibility:

| Layer | Chapter tendency |
|---|---|
| application | many smaller replicas |
| cache | fewer larger-memory replicas |
| SSL bridge | independently replicated edge layer |

Exact counts are workload-dependent.
