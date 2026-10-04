# Резюме главы 2

Источник: явный раздел `2.4 Резюме`, RAG chunk `p0094:c01`.

После этой практической главы читатель должен уметь:

- получать и запускать общедоступный container image;
- упаковывать собственное приложение в image и публиковать его в remote image registry;
- входить в работающий container и исследовать его окружение;
- настраивать многоузловой Kubernetes cluster в Google Kubernetes Engine;
- настраивать alias и completion для `kubectl`;
- выводить и исследовать nodes, Pods, Services и ReplicationControllers;
- запускать containerized application в Kubernetes;
- предоставлять приложению доступ извне через Service;
- понимать базовую связь между Pod, ReplicationController и Service;
- горизонтально масштабировать приложение изменением replica count;
- получать доступ к Kubernetes Dashboard в Minikube и GKE.

## Главная связка главы

~~~text
Docker image
   ↓ registry
kubectl run
   ↓
ReplicationController
   ↓
Pods
   ↑
Service
   ↑
client
~~~

## Provenance

- Chapter chunks: `p0062:c01`–`p0094:c01`
- Summary chunk: `p0094:c01`
- PDF page: 94
- Printed page: 93
- Source SHA-256: `0d50f167ed86088d0cc65d15e27f1ab397e7c0a0c8de4db3801b50439f24266f`
