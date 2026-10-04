# Резюме главы 4

Источник: явный раздел `4.7 Резюме`, RAG chunks `p0166:c01`–`p0167:c01`.

После главы читатель должен понимать следующие механизмы:

- liveness probe позволяет Kubernetes перезапускать container, когда приложение больше не считается здоровым;
- Pods не следует создавать напрямую для устойчивых workloads, потому что такой Pod не будет автоматически восстановлен после удаления, node failure или eviction;
- ReplicationController поддерживает требуемое число matching Pod replicas;
- horizontal scaling выполняется изменением desired replica count;
- Pods могут входить и выходить из области controller в зависимости от label selector;
- Pod template используется только для новых Pods и не изменяет уже существующие;
- ReplicationController в модели главы следует заменять ReplicaSet/Deployment;
- ReplicaSet даёт ту же базовую reconciliation-функцию, но с более мощными selectors;
- DaemonSet гарантирует один daemon Pod на каждом подходящем node;
- finite batch work следует запускать через Job;
- будущие/периодические Jobs создаются через CronJob.

## Иерархия ответственности

~~~text
livenessProbe
└─ restart unhealthy container

ReplicaSet / ReplicationController
└─ maintain N Pods

DaemonSet
└─ maintain one Pod per matching node

Job
└─ reach successful completion count

CronJob
└─ create Jobs by schedule
~~~

## Provenance

- Chapter chunks: `p0127:c01`–`p0167:c01`
- Summary chunks: `p0166:c01`–`p0167:c01`
- PDF pages: 166–167
- Printed pages: 165–166
- Source SHA-256: `0d50f167ed86088d0cc65d15e27f1ab397e7c0a0c8de4db3801b50439f24266f`
