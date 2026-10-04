# Ответ к упражнению главы 8

Это RAG-grounded procedure, не официальный издательский answer key.

## Упражнение 1 — Swagger UI

Source-era enablement for Minikube:

~~~text
minikube start --extra-config=apiserver.Features.EnableSwaggerUI=true
~~~

После запуска source предлагает открыть:

~~~text
http(s)://<api-server>:<port>/swagger-ui
~~~

Expected result:
- Swagger UI загружается;
- доступны Kubernetes API definitions/operations;
- пользователь может исследовать endpoints без ручного перебора curl paths.

Source также указывает:
- Swagger definitions доступны через /swaggerapi;
- OpenAPI specification доступна через /swagger.json.

## Safety

Swagger UI является privileged interactive API surface.

Для acceptance достаточно:
1. открыть UI;
2. найти/read endpoint metadata;
3. не отправлять create/patch/delete requests.

Source говорит, что UI способен изменять и удалять resources, поэтому любые такие действия должны считаться отдельными state-changing operations.

## Current compatibility

[Unverified] — source-era Swagger UI enablement сохранён буквально из книги. Современная совместимость не проверялась, поскольку source policy главы — rag_only.

## Provenance

- Swagger/OpenAPI and UI: p0314:c01
