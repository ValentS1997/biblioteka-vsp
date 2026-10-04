# Резюме главы 15

Источник: явный раздел 15.4 Резюме, RAG chunks p0551:c01–p0552:c01.

Основные выводы главы:

- HorizontalPodAutoscaler создаётся как отдельный API resource и указывает на масштабируемый Deployment, ReplicaSet или ReplicationController; source chapter также рассматривает Scale subresource и StatefulSet target support;
- HPA может масштабировать workload по CPU utilization;
- HPA также может использовать custom application metrics и metrics других cluster objects;
- source-era vertical autoscaling running Pod ещё невозможно;
- на поддерживаемом cloud provider можно автоматически масштабировать cluster nodes;
- kubectl run с -it и --rm source показывает как удобный способ выполнять одноразовые in-cluster processes с автоматическим удалением временного Pod.

## Центральная модель

~~~text
metrics
  → HPA
  → desired replicas
  → workload controller
  → Pods

unschedulable Pods
  → Cluster Autoscaler
  → more nodes

voluntary node removal
  → PDB
  → availability constraint
~~~

## Autoscaling conclusion

Pod autoscaling и node autoscaling решают связанные, но разные задачи.

HPA отвечает на load signal и увеличивает desired replicas.

Scheduler пытается разместить новые Pods.

Если capacity nodes недостаточно, Cluster Autoscaler увеличивает node group.

При обратном процессе Cluster Autoscaler уменьшает node count только когда workloads можно безопасно перенести, а PDB ограничивает допустимые voluntary disruptions.

## Provenance

- Chapter chunks: p0529:c01–p0552:c01
- Summary chunks: p0551:c01–p0552:c01
- PDF pages: 551–552
- Printed pages: 550–551
- Source SHA-256: 0d50f167ed86088d0cc65d15e27f1ab397e7c0a0c8de4db3801b50439f24266f
