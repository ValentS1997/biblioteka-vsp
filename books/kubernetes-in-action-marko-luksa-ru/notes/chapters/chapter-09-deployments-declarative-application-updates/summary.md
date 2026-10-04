# Резюме главы 9

Источник: явный раздел 9.4 Резюме, RAG chunk p0349:c01.

После главы читатель должен уметь:

- выполнять rolling update Pods, управляемых ReplicationController;
- создавать Deployment вместо более низкоуровневого ReplicationController/ReplicaSet;
- обновлять Pods через изменение Pod template Deployment;
- rollback Deployment к предыдущей или выбранной revision;
- abort rollout в процессе;
- pause rollout для проверки ограниченного числа новых instances;
- управлять rollout speed через maxSurge и maxUnavailable;
- использовать minReadySeconds и readiness probe для блокировки rollout дефектной версии.

Дополнительно source отмечает:

- YAML может содержать несколько resources, разделённых тремя дефисами;
- verbose kubectl logging помогает видеть взаимодействие client с API server.

## Центральная модель

~~~text
Deployment
  ↓ desired Pod template
ReplicaSet per revision
  ↓
Pods

Template change
  → new revision
  → rolling convergence

Readiness + minReadySeconds
  → availability gate
  → bad rollout stops before replacing all healthy Pods
~~~

## Provenance

- Chapter chunks: p0316:c01–p0349:c01
- Summary chunk: p0349:c01
- PDF page: 349
- Printed page: 348
- Source SHA-256: 0d50f167ed86088d0cc65d15e27f1ab397e7c0a0c8de4db3801b50439f24266f
