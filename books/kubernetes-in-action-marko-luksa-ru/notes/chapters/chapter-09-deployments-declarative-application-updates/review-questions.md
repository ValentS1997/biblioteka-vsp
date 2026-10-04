# Упражнения главы 9

В проверенной границе найдено одно явно обозначенное упражнение.

## Упражнение 1 — Наблюдение RollingUpdate

Источник: p0333:c01–p0334:c01.

1. Замедлить rollout, установив minReadySeconds равным 10.
2. Запустить цикл запросов к Service.
3. Изменить image Deployment с v1 на v2 через kubectl set image.
4. Наблюдать постепенный переход traffic от старых Pods к новым.

Source commands:

~~~bash
kubectl patch deployment kubia -p '{"spec": {"minReadySeconds": 10}}'
kubectl set image deployment kubia nodejs=luksa/kubia:v2
~~~

Service endpoint в source example должен быть заменён фактическим адресом текущего lab environment.

## Provenance

- Exercise: p0333:c01–p0334:c01
- Source SHA-256: 0d50f167ed86088d0cc65d15e27f1ab397e7c0a0c8de4db3801b50439f24266f
