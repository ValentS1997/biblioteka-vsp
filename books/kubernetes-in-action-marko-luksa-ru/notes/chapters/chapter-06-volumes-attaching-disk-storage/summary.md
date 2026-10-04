# Резюме главы 6

Источник: явный раздел 6.7 Резюме, RAG chunks p0247:c01–p0248:c01.

В главе показано, как Kubernetes Volumes предоставляют containers временное или постоянное storage.

После главы читатель должен понимать, как:

- создавать multi-container Pod и давать containers доступ к одним файлам через общий Volume;
- использовать emptyDir для temporary data;
- использовать gitRepo для initial population directory содержимым Git repository;
- использовать hostPath для доступа к filesystem worker node;
- монтировать external persistent storage, переживающий Pod replacement;
- отделять application Pod от concrete storage technology через PersistentVolume и PersistentVolumeClaim;
- запрашивать storage нужного или default StorageClass;
- динамически provision PersistentVolume для PVC;
- предотвращать default dynamic provisioning, когда PVC должна bind к заранее provisioned PV.

## Центральная модель

~~~text
Container filesystem
    ↓ not durable across replacement

Pod Volume
    ├─ emptyDir / gitRepo / hostPath
    └─ persistent backend

Application abstraction:
Pod → PVC → PV → storage

Dynamic:
PVC → StorageClass → provisioner → PV + storage
~~~

## Provenance

- Chapter chunks: p0212:c01–p0248:c01
- Summary chunks: p0247:c01–p0248:c01
- PDF pages: 247–248
- Printed pages: 246–247
- Source SHA-256: 0d50f167ed86088d0cc65d15e27f1ab397e7c0a0c8de4db3801b50439f24266f
