# Резюме главы 16

Источник: явный раздел 16.4 Резюме, RAG chunk p0574:c01.

Основные выводы главы:

- taint на node предотвращает scheduling Pods, которые не имеют соответствующего toleration;
- NoSchedule запрещает новое placement;
- PreferNoSchedule выражает soft avoidance;
- NoExecute также может вытеснять уже работающие Pods;
- NoExecute toleration может задавать, сколько control plane ждёт при notReady/unreachable node;
- node affinity определяет, к каким nodes Pod должен или предпочитает быть назначен;
- pod affinity размещает Pods рядом с matching Pods;
- topologyKey задаёт topology scope co-location: node/rack/zone/region/custom domain;
- pod anti-affinity удерживает matching workloads подальше друг от друга;
- node affinity, pod affinity и pod anti-affinity могут выражать hard requirements либо preferences.

## Центральная модель

~~~text
Node exclusion:
taint
  + Pod toleration

Node attraction:
node labels
  + nodeAffinity

Workload co-location:
Pod labels
  + podAffinity
  + topologyKey

Workload separation:
Pod labels
  + podAntiAffinity
  + topologyKey
~~~

## Operational conclusion

Жёсткие scheduling rules улучшают предсказуемость placement, но уменьшают число допустимых решений scheduler.

Поэтому source distinction между required и preferred принципиален:

- required подходит для настоящего invariant;
- preferred подходит, когда placement желателен, но availability важнее идеального topology match.

## Provenance

- Chapter chunks: p0553:c01–p0574:c01
- Summary chunk: p0574:c01
- PDF page: 574
- Printed page: 573
- Source SHA-256: 0d50f167ed86088d0cc65d15e27f1ab397e7c0a0c8de4db3801b50439f24266f
