# Резюме главы 7

Источник: явный раздел 7.6 Резюме, RAG chunks p0286:c01–p0287:c01.

После главы читатель должен уметь:

- переопределять default command container в Pod definition;
- передавать command-line arguments главному process container;
- задавать environment variables;
- отделять non-sensitive configuration от Pod spec через ConfigMap;
- хранить sensitive data в Secret и передавать её containers;
- создавать docker-registry Secret и использовать его для private registry image pulls.

## Дополнительные ключевые выводы главы

- ConfigMap может передаваться через env variables или files.
- ConfigMap volume files могут обновляться после изменения ConfigMap.
- Application должен самостоятельно reload configuration.
- Single-file/subPath mount в source-era behavior не получает update.
- Secret data in YAML Base64-encoded, но Base64 не является encryption.
- Secret volume предоставляет decoded values.
- Source recommends Secret volume rather than env for sensitive data.
- imagePullSecrets связывает Pod с registry credential Secret.

## Центральная модель

~~~text
Non-sensitive:
ConfigMap → env / args / files

Sensitive:
Secret → preferably files in secret volume

Registry:
docker-registry Secret → imagePullSecrets
~~~

## Provenance

- Chapter chunks: p0249:c01–p0287:c01
- Summary chunks: p0286:c01–p0287:c01
- PDF pages: 286–287
- Printed pages: 285–286
- Source SHA-256: 0d50f167ed86088d0cc65d15e27f1ab397e7c0a0c8de4db3801b50439f24266f
