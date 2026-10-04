# Резюме главы 8

Источник: явный раздел 8.3 Резюме, RAG chunk p0315:c01.

После главы читатель должен понимать:

- как передавать Pod name, namespace и другие metadata через environment variables или downwardAPI volume files;
- как передавать CPU/memory requests/limits в требуемых единицах;
- как downwardAPI volume предоставляет актуализируемые labels/annotations;
- как исследовать Kubernetes REST API через kubectl proxy;
- как Pod находит API server через Service environment/DNS;
- как приложение проверяет API server certificate и authenticates itself;
- как ambassador sidecar упрощает in-Pod API access;
- как Kubernetes client libraries упрощают работу с API.

## Центральная модель

~~~text
Own metadata
  → Downward API
  → env / files

Cluster resources
  → Kubernetes REST API
  → TLS verification + authentication + authorization

Complex client logic
  → ambassador or client library
~~~

## Security conclusion

Authentication не равна authorization.

ServiceAccount token подтверждает identity, но RBAC определяет разрешённые действия.

Source lab command, выдающая cluster-admin всем ServiceAccounts, является deliberate security bypass и прямо запрещается source для production.

## Provenance

- Chapter chunks: p0288:c01–p0315:c01
- Summary chunk: p0315:c01
- PDF page: 315
- Printed page: 314
- Source SHA-256: 0d50f167ed86088d0cc65d15e27f1ab397e7c0a0c8de4db3801b50439f24266f
