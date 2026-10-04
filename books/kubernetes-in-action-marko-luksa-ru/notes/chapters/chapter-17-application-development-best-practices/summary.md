# Резюме главы 17

Источник: явный раздел 17.6 Резюме, RAG chunks p0609:c01–p0610:c01.

Глава закрепляет следующие положения:

- Kubernetes resources типичного приложения образуют связанную систему, а не набор независимых объектов;
- applications в Pods должны ожидать более частого relocation/recreation, чем applications на традиционных VMs;
- multi-component applications не должны зависеть от строгого порядка startup;
- init containers позволяют выполнять initialization и ждать prerequisites;
- lifecycle hooks расширяют startup/shutdown behavior containers;
- distributed nature Kubernetes приводит к eventual/asynchronous propagation during shutdown;
- application должно корректно завершать работу и не прерывать client connections;
- manageable container images, labels, annotations и termination reasons упрощают operations;
- application logs должны быть удобны для collection/analysis;
- applications можно разрабатывать локально или в Minikube до deployment в настоящий multi-node cluster.

## Центральная модель

~~~text
robust application
  = restart/relocation tolerance
  + readiness
  + init prerequisites
  + graceful termination
  + observability
  + versioned/declarative delivery
~~~

## Operational conclusion

Kubernetes может автоматизировать scheduling, restart и reconciliation, но correctness application lifecycle остаётся обязанностью приложения и его manifests.

Kubernetes не может автоматически:
- понять, когда application действительно готово обслуживать requests без readiness signal;
- гарантировать мгновенное прекращение traffic при Pod deletion;
- завершить application-specific active requests;
- сохранить данные, записанные только в container writable layer;
- объяснить termination reason, если application не пишет полезные logs/status.

## Provenance

- Chapter chunks: p0575:c01–p0610:c01
- Summary chunks: p0609:c01–p0610:c01
- PDF pages: 609–610
- Printed pages: 608–609
- Source SHA-256: 0d50f167ed86088d0cc65d15e27f1ab397e7c0a0c8de4db3801b50439f24266f
