# Шпаргалка: Kubernetes storage lifecycle

## Какой storage нужен

### Временный shared storage внутри Pod

Использовать модель emptyDir.

Свойства:
- shared между containers одного Pod;
- переживает restart container;
- удаляется вместе с Pod;
- может быть disk-backed либо Memory-backed.

### Файлы worker node

hostPath.

Использовать только когда workload должен читать/писать node filesystem.

Риск:
- данные привязаны к node;
- rescheduled Pod на другом node увидит другой hostPath.

### Данные должны пережить Pod

Нужен external persistent storage или PV/PVC abstraction.

## emptyDir pattern

~~~text
Pod
├─ html-generator
│  └─ mount /var/htdocs
├─ web-server
│  └─ mount /usr/share/nginx/html readOnly
└─ volume: emptyDir
~~~

Source verification:

~~~bash
kubectl port-forward fortune 8080:80
curl http://localhost:8080
~~~

## gitRepo pattern

~~~text
Pod creation
  ↓
emptyDir created
  ↓
Git repository cloned once
  ↓
container reads files
~~~

Subsequent Git commits не синхронизируются автоматически.

Для continuous sync source предлагает sidecar container.

## hostPath

~~~text
Node filesystem
    ↓
hostPath volume
    ↓
system Pod
~~~

Source use cases:
- node logs;
- /var/lib/docker/containers;
- node devices/system files.

Не использовать как обычное application storage, которое должно follow Pod across nodes.

## Persistent storage direct attachment

Source model:

~~~text
Pod → gcePersistentDisk → GCE Persistent Disk
~~~

Verification concept:
1. записать данные;
2. удалить Pod;
3. создать Pod снова с тем же disk;
4. проверить сохранённые данные.

Риск: Pod manifest зависит от конкретного infrastructure backend.

## PV/PVC abstraction

~~~text
Cluster admin
  ↓
PersistentVolume
  ↓ binding
PersistentVolumeClaim
  ↓ claimName
Pod volume
~~~

PV:
- cluster-scoped;
- capacity;
- accessModes;
- reclaim policy;
- actual storage backend.

PVC:
- namespaced;
- requested capacity;
- requested accessModes;
- optional storageClassName.

## Access modes

| Mode | Source meaning |
|---|---|
| RWO | ReadWriteOnce — read/write from one node |
| ROX | ReadOnlyMany — read-only from many nodes |
| RWX | ReadWriteMany — read/write from many nodes |

Это про nodes, не про количество Pods.

## PV/PVC states

~~~text
PV Available
   ↓ compatible PVC
PV Bound
   ↓ PVC deleted
PV Released
~~~

При Retain Released PV не должен автоматически выдаваться другому claim с потенциально чужими данными.

## Reclaim policies

### Retain

Сохраняет PV/storage/data после удаления PVC. Требуется ручное решение для повторного использования.

### Recycle

Очищает storage и делает PV Available, если backend поддерживает.

### Delete

Удаляет underlying storage.

HIGH RISK: data-destructive lifecycle.

## Dynamic provisioning

~~~text
PVC
 ↓ storageClassName
StorageClass
 ↓ provisioner + parameters
Provisioner
 ↓
PV + actual storage
~~~

Если storageClassName не указан, default StorageClass может использоваться автоматически.

Если нужен предварительно созданный PV, source использует storageClassName: "".

## Read-only checks

~~~bash
kubectl get pv
kubectl get pvc
kubectl get sc
kubectl get sc standard -o yaml
gcloud compute disks list
~~~

## Risky actions

### Create infrastructure disk

~~~bash
gcloud compute disks create --size=1GiB --zone=<zone> mongodb
~~~

State-changing cloud infrastructure action.

### Delete PVC

~~~bash
kubectl delete pvc mongodb-pvc
~~~

State-changing storage lifecycle action.

До удаления проверить reclaim policy соответствующего PV.

### Delete Pod

~~~bash
kubectl delete pod mongodb
~~~

Pod destructive, но persistent data may survive depending on volume backend.

## Acceptance

Перед storage change должно быть известно:

- volume type;
- node affinity/portability;
- requested access mode;
- PV/PVC binding state;
- reclaim policy;
- StorageClass/default-class behavior;
- ожидается ли сохранение или удаление underlying data.
