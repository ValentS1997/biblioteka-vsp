# Ответ к упражнению главы 9

Это RAG-grounded procedure, не официальный издательский answer key.

## Упражнение 1 — Наблюдение RollingUpdate

### Шаг 1. Замедлить rollout

~~~bash
kubectl patch deployment kubia -p '{"spec": {"minReadySeconds": 10}}'
~~~

Expected:
- Deployment spec изменён;
- существующие Pods не заменяются только из-за изменения minReadySeconds;
- Pod template не изменён.

### Шаг 2. Наблюдать Service traffic

Source pattern:

~~~bash
while true; do curl http://<service-external-ip>; done
~~~

<service-external-ip> должен быть взят из текущего environment.

### Шаг 3. Изменить Pod template

~~~bash
kubectl set image deployment kubia nodejs=luksa/kubia:v2
~~~

Expected:
- template image изменяется v1 → v2;
- Deployment создаёт новый ReplicaSet;
- начинается RollingUpdate.

### Шаг 4. Проверить постепенную замену

Read-only:

~~~bash
kubectl rollout status deployment kubia
kubectl get rs
kubectl get po
~~~

Expected source behavior:
- сначала traffic идёт только в v1;
- затем появляются v2 responses;
- число v2 Pods растёт, v1 уменьшается;
- после завершения traffic идёт только в v2.

## Acceptance criteria

- rollout завершается успешно;
- desired replicas доступны;
- active Pods используют v2;
- старый ReplicaSet остаётся как revision history согласно source behavior;
- Service traffic не требует полного stop/start приложения.

## Rollback

Если exercise нужно отменить:

~~~bash
kubectl rollout undo deployment kubia
~~~

Это state-changing rollback и должно выполняться только если возврат к предыдущей revision действительно требуется.

## Provenance

- minReadySeconds patch: p0334:c01
- set image update: p0334:c01
- rollout mechanics: p0334:c01–p0336:c01
