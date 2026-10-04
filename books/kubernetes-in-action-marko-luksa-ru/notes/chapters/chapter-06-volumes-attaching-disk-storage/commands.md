# Команды главы 6

Source policy: только RAG главы 6. Команды разделены на read-only, state-changing и destructive/data-sensitive.

## Docker image for fortune container

~~~bash
docker build -t luksa/fortune .
docker push luksa/fortune
~~~

State-changing:
- build создаёт local image;
- push публикует image в registry.

Rollback: [Needs confirmation].

## emptyDir demo

~~~bash
kubectl port-forward fortune 8080:80
~~~

Workload-generating local forwarding process.

Verification:

~~~bash
curl http://localhost:8080
~~~

Повторные requests должны показывать меняющийся content, записываемый generator container в shared volume.

Source предлагает вместо port-forward предоставить Pod через Service.

Exact Service manifest/command в chapter 6 не дан: [Needs confirmation].

## Inspect hostPath use in system Pods

Source-confirmed describe:

~~~bash
kubectl describe po <system-pod> --namespace kube-system
~~~

Read-only.

Source example показывает hostPath paths:
- /var/log;
- /var/lib/docker/containers.

Строка списка Pods в p0224 имеет RAG extraction artifact и не реконструируется молча.

## GCE persistent disk

Определить cluster/zone context:

~~~bash
gcloud container clusters list
~~~

Read-only.

Создать disk:

~~~bash
gcloud compute disks create --size=1GiB --zone=<zone> mongodb
~~~

STATE-CHANGING cloud infrastructure action.

Verification:

~~~bash
gcloud compute disks list
~~~

Rollback/delete disk command отсутствует в chapter: [Needs confirmation].

## MongoDB persistent-data verification

Interactive shell:

~~~bash
kubectl exec -it mongodb mongo
~~~

Source operations:

~~~text
use mystore
db.foo.insert({name:'foo'})
db.foo.find()
~~~

Insert изменяет application data.

### Delete and recreate Pod

~~~bash
kubectl delete pod mongodb
kubectl create -f mongodb-pod-gcepd.yaml
~~~

Первое destructive для Pod; второе state-changing.

После recreation:

~~~bash
kubectl exec -it mongodb mongo
~~~

и:

~~~text
use mystore
db.foo.find()
~~~

Expected: ранее записанный document остаётся на persistent disk.

## Pod placement

~~~bash
kubectl get po -o wide
~~~

Read-only. Source использует wide output для проверки node placement.

## PersistentVolume

После generic kubectl create для PV:

~~~bash
kubectl get pv
~~~

Read-only.

Expected before claim: Available.

Exact create command line для PV file не присутствует в retrieved RAG и не реконструируется.

## PersistentVolumeClaim

После generic kubectl create для PVC:

~~~bash
kubectl get pvc
~~~

Read-only.

Expected compatible claim state: Bound.

Access modes:
- RWO;
- ROX;
- RWX.

## Verify PV binding

~~~bash
kubectl get pv
~~~

Expected: Bound и CLAIM вида namespace/claim-name.

## Pod using PVC

Source manifest relation:

~~~text
persistentVolumeClaim:
  claimName: mongodb-pvc
~~~

Data verification:

~~~bash
kubectl exec -it mongodb mongo
~~~

## PVC deletion — storage lifecycle boundary

Source experiment:

~~~bash
kubectl delete pod mongodb
kubectl delete pvc mongodb-pvc
~~~

DESTRUCTIVE/state-changing.

Перед выполнением критично знать PV reclaim policy.

При source policy Retain:
- PV становится Released;
- underlying data сохраняются;
- новый PVC не bind автоматически к Released PV.

Read-only checks:

~~~bash
kubectl get pvc
kubectl get pv
~~~

Expected:
- recreated PVC Pending;
- old PV Released.

## Reclaim policy semantics

Source policies:

~~~text
Retain
Recycle
Delete
~~~

Retain:
- сохранить storage/data;
- administrative cleanup/reuse required.

Recycle:
- erase contents;
- make PV Available again;
- backend support varies.

Delete:
- delete underlying storage.

Delete — HIGH RISK data-destruction boundary.

Exact command to change reclaim policy is not provided in retrieved chapter commands.

## StorageClass inspection

~~~bash
kubectl get sc
kubectl get sc standard -o yaml
~~~

Read-only.

Source default StorageClass is identified by source-era annotation in GKE example.

## Dynamic PVC with explicit StorageClass

Source manifest concept:

~~~text
storageClassName: fast
resources:
  requests:
    storage: 100Mi
accessModes:
- ReadWriteOnce
~~~

Verification:

~~~bash
kubectl get pvc mongodb-pvc
kubectl get pv
gcloud compute disks list
~~~

Expected:
- PVC Bound;
- dynamically provisioned PV;
- reclaim policy Delete in source example;
- actual infrastructure disk exists.

## PVC without storageClassName

Source checks:

~~~bash
kubectl get pvc mongodb-pvc2
kubectl get pv <pv-name>
gcloud compute disks list
~~~

Expected source behavior on GKE:
- default StorageClass used;
- dynamically provisioned disk created.

## Force use of pre-provisioned PV

Source fragment:

~~~text
storageClassName: ""
~~~

Meaning:
- prevent default dynamic provisioner from creating a new PV;
- allow matching pre-provisioned PV to bind.

## Data-safety checklist

Before deleting PVC:

1. kubectl get pvc
2. kubectl get pv
3. identify bound PV
4. verify reclaim policy
5. decide whether data should be retained, wiped or infrastructure-deleted
6. only then perform delete

Пункты 3–5 are operational safety framing derived from source lifecycle model; chapter does not package them as a literal command sequence.
