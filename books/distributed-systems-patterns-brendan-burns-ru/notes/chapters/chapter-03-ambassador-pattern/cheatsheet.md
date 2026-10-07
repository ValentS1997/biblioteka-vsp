# Шпаргалка: глава 3 — Паттерн Ambassador

## Symptom / problem framing

Application должно взаимодействовать с external service, но external side содержит сложность:
- sharding;
- environment-specific discovery;
- request splitting / experiments.

Если эту логику встроить непосредственно в application, оно становится жестче связано с topology и policy.

Chapter pattern:

~~~text
application
→ stable local endpoint
→ Ambassador
→ changing / complex external world
~~~

## Baseline / context

Ambassador:
- colocated с application;
- работает на том же узле;
- является посредником между application и external services;
- инкапсулирует networking/routing/discovery policy;
- может быть reused рядом с разными applications.

## Read-only checks

Перед использованием Ambassador проверить:

1. Какая external complexity скрывается?
2. Действительно ли application нужен стабильный local interface?
3. Кто владеет routing/discovery/experiment logic?
4. Будет ли client-side deployment проще organizationally, чем central service?
5. Какие external services должны существовать до запуска Ambassador?
6. Какая configuration определяет routing?
7. Нужна ли user/session consistency при traffic splitting?
8. Есть ли observable way проверить destination/result?
9. Не содержит ли source example known ambiguity из `source-findings.md`?

Quantitative SLO/failure thresholds глава не задает: `[Needs confirmation]`.

## Interpretation

### Sharded storage

~~~text
application expects one store
→ Ambassador presents localhost store
→ routes by shard logic
→ several Redis shards
~~~

### Service broker

~~~text
same application
→ different environment
→ Ambassador discovers/provisions target dependency
→ application keeps same local-facing contract
~~~

### Experiment / request splitting

~~~text
application
→ Ambassador
→ 90% production
→ 10% experiment
~~~

Source nginx example adds `ip_hash` so a user remains consistently associated with one backend behavior.

## Next action

Source-grounded sequence:

1. Define stable interface expected by application.
2. Identify external variability to hide.
3. Decide client-side Ambassador vs separate shared service.
4. Configure routing/discovery/splitting policy.
5. Ensure external targets exist where source requires them.
6. Deploy Ambassador beside application.
7. Verify application can use local endpoint.
8. Verify traffic reaches intended external target(s).

## Modifying action

### Redis practical example

Source commands include:

~~~bash
kubectl create -f redis-shards.yaml
kubectl get pods
kubectl create configmap twem-config --from-file=./nutcracker.yaml
~~~

Effects:
- create Kubernetes resources from manifest;
- list pods;
- create ConfigMap for twemproxy configuration.

Rollback commands are not provided: `[Needs confirmation]`.

### Experiment practical example

Source RAG contains:

~~~text
kubectl create configmaps --from-file=nginx.conf
~~~

Do not use as verified copy/paste command. It is internally inconsistent with the later Pod reference to `experiment-config`; see `source-findings.md`.

## Verification / acceptance checks

### Redis sharding example

Source-supported observations:
- three Redis pods are expected;
- DNS names such as `sharded-redis-0.redis` are expected;
- twemproxy local endpoint is `127.0.0.1:6379`;
- application talks to Ambassador as if to one local Redis service.

Exact command for DNS/Redis functional verification: `[Needs confirmation]`.

### Service broker

Verify conceptually:
- application uses local service endpoint;
- broker resolves/provisions environment-specific target.

Exact operational verification command: `[Needs confirmation]`.

### Experiment

Source assumptions:
- `web` service exists;
- `experiment` service exists;
- nginx Ambassador starts only when proxy targets can be found;
- traffic policy uses weights 9:1;
- IP hashing maintains per-user consistency.

Exact measurement procedure for 90/10 distribution: `[Needs confirmation]`.

## Rollback

No complete rollback procedure is supplied in chapter 3.

- Redis StatefulSet/Service rollback: `[Needs confirmation]`;
- twemproxy ConfigMap rollback: `[Needs confirmation]`;
- service-broker rollback: `[Needs confirmation]`;
- experiment ConfigMap/Pod rollback: `[Needs confirmation]`.

Do not infer `kubectl delete` commands from model knowledge.

## Decision frame

~~~text
external interaction complexity?
        |
        +-- reusable + client-local → Ambassador candidate
        |
        +-- architecture-wide / permanent → consider separate service
~~~

Chapter does not define a universal threshold between the two.
