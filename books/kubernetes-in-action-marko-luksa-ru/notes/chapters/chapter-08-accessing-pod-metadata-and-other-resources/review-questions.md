# Упражнения главы 8

В проверенной границе найдена одна явно предложенная самостоятельная практическая задача.

## Упражнение 1 — Swagger UI

Источник: p0314:c01.

Активировать source-era Swagger UI и использовать его для исследования Kubernetes REST API.

Source Minikube example:

~~~text
minikube start --extra-config=apiserver.Features.EnableSwaggerUI=true
~~~

После включения открыть:

~~~text
http(s)://<api-server>:<port>/swagger-ui
~~~

Проверить, что UI позволяет просматривать API operations.

## Risk boundary

Source отдельно говорит, что Swagger UI позволяет не только читать API, но и:
- отправлять resource manifests;
- patch resources;
- delete resources.

Поэтому acceptance для упражнения — read-only exploration. State-changing operations не требуются для подтверждения результата.

## Provenance

- Exercise: p0314:c01
- Source SHA-256: 0d50f167ed86088d0cc65d15e27f1ab397e7c0a0c8de4db3801b50439f24266f
