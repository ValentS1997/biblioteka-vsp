# Commands — глава 9. PersistentVolume / PVC / CSI / StorageClass

**Source:** исключительно RAG PDF 326–365. Все действия показаны как примеры главы, **не выполнялись**. Обозначение [Needs confirmation] означает отсутствие достаточной опоры в источнике для безопасной эксплуатации. Внешнее backend, namespace, доступы, резервирование и сохранность данных не проверены.

## Read-only — inventory, status and storage classes

| Подтверждённая RAG команда | Класс / данные | PDF |
|---|---|---:|
| `kubectl get persistentvolume` | read-only; список кластерных PV | 332 |
| `kubectl get persistentvolumes` | read-only; эквивалентная форма | 332 |
| `kubectl get pv` | read-only; Available / Bound / Released, reclaim | 332, 345, 350–351 |
| `kubectl get persistentvolumeclaims` | read-only; PVC текущего namespace | 341 |
| `kubectl get pvc` | read-only; сокращение | 341 |
| `kubectl get pvc -n pv-ns` | read-only; PVC в заданном namespace | 346 |
| `kubectl get pvc,pod -n pv-ns` | read-only; Bound и Running | 347 |
| `kubectl get pod,pvc -n pv-ns` | read-only; состояние перед удалением | 350 |
| `kubectl api-resources --namespaced=false \| grep -i volume` | read-only; PV cluster-scoped | 348 |
| `kubectl get sc` | read-only; StorageClass, provisioner, reclaim | 356, 358 |
| `kubectl get storageclass` / `kubectl get storageclasses` | read-only; те же классы | 356 |
| `kubectl get storageclasses standard -o yaml` | read-only; параметры default minikube StorageClass | 356 |
| `kubectl get pod,pvc,pv -n dynamicstorage` | read-only; динамические ресурсы, binding, cleanup | 359–361 |

**Interpretation:** `Bound` фиксирует привязку PV/PVC; `Available` — ресурс для нового сопоставления; `Released` — освобождён после PVC, но **не** автоматически `Available` (p0345–p0351). `get pv -n` всё равно показывает PV cluster-scoped; в образцах p0359–p0360 используется составной `get pod,pvc,pv -n`. Реальные номера дисков, пути, провайдеры, права и статусы текущей среды [Needs confirmation].

## Workload-generating: конфигурация в томе

```bash
kubectl apply -f nginx-configmap.yaml
kubectl apply -f nginx-pod.yaml
kubectl get pod,cm
kubectl exec -t pod/nginx-hello -- ls -al /usr/share/nginx/html/hello/
kubectl port-forward nginx-hello 8080:80
curl 127.0.0.1:8080/hello/hello1.html
curl 127.0.0.1:8080/hello/hello2.html
```

Source p0327–p0329. `nginx-configmap.yaml` создаёт `nginx-hello` ConfigMap с `hello1.html` / `hello2.html`, `nginx-pod.yaml` создаёт Pod `nginx-hello`, монтирующий эти файлы в `/usr/share/nginx/html/hello`; образ `nginx:1.14.2`. **Effect:** `apply` создаёт Pod и ConfigMap; `exec -- ls` читает содержимое, `port-forward` открывает локальный TCP endpoint, `curl` генерирует HTTP трафик. **Risk:** локальный доступ, неизвестный origin образа и публикация данных. **Verification:** два URL возвращают тестовые HTML-фрагменты. **Rollback:** Ctrl+C останавливает `port-forward`; последовательность полного удаления/восстановления в источнике не описана [Needs confirmation]. Этот ConfigMap **не замена** долговременному пользовательскому хранилищу.

## PV static provisioning — state-changing

```yaml
# pv-hostpath.yaml (p0338) — только для демонстрации
apiVersion: v1
kind: PersistentVolume
metadata:
  name: pv-hostpath
  labels:
    type: local
spec:
  storageClassName: manual
  capacity:
    storage: 1Gi
  accessModes:
    - ReadWriteOnce
  hostPath:
    path: "/mnt/data"
```
```bash
kubectl apply -f pv-hostpath.yaml
```

**Effect:** создаётся cluster-scoped PV, указывающий на узловую директорию. **Risk:** hostPath не переносит файлы между узлами; автор прямо не рекомендует для production (p0338). **Verification:** `kubectl get pv` (p0332). **Rollback:** source не описывает безопасной процедуры для произвольных данных [Needs confirmation].

Отдельные PV examples, **зависят от реально настроенного внешнего хранилища**:
```yaml
# pv-nfs.yaml, p0339
apiVersion: v1
kind: PersistentVolume
metadata:
  name: pv-nfs
spec:
  capacity:
    storage: 5Gi
  volumeMode: Filesystem
  accessModes:
    - ReadWriteOnce
  persistentVolumeReclaimPolicy: Recycle
  storageClassName: slow
  mountOptions:
    - hard
    - nfsvers=4.1
  nfs:
    path: /appshare
    server: nfs.example.com
```

**Warning:** `Recycle` прямо признан deprecated на p0350. Это *source literal*, **не применять** как текущий production API без отдельной проверки. `nfs.example.com` — placeholder, не реальный экспорт. **Risk:** удаление данных по reclaim, ошибки подключения; verification/rollback [Needs confirmation].

```yaml
# pv-block.yaml, p0340
apiVersion: v1
kind: PersistentVolume
metadata:
  name: pv-block
spec:
  capacity:
    storage: 100Gi
  accessModes:
    - ReadWriteOnce
  volumeMode: Block
  persistentVolumeReclaimPolicy: Retain
  fc:
    targetWWNs: ["50060e801049cfd1"]
    lun: 0
    readOnly: false
```

Source example, **не выполнять** на storage fabric, WWN / LUN и доступ не подтверждены. Работающая CSI-замена [Needs confirmation].

## PV → PVC → Pod — статический связанный пример

PV из p0345:
```yaml
# pv.yaml
apiVersion: v1
kind: PersistentVolume
metadata:
  name: my-hostpath-pv
  labels:
    type: hostpath
    env: prod
spec:
  capacity:
    storage: 1Gi
  accessModes:
    - ReadWriteOnce
  hostPath:
    path: "/tmp/test"
  storageClassName: slow
```

PVC из p0346:
```yaml
# pvc.yaml
apiVersion: v1
kind: PersistentVolumeClaim
metadata:
  name: my-hostpath-pvc
  namespace: pv-ns
spec:
  resources:
    requests:
      storage: 1Gi
  accessModes:
    - ReadWriteOnce
  selector:
    matchLabels:
      type: hostpath
      env: prod
  storageClassName: slow
```

Pod из p0346–p0347:
```yaml
# pod.yaml
apiVersion: v1
kind: Pod
metadata:
  name: nginx
  namespace: pv-ns
spec:
  containers:
    - image: nginx
      name: nginx
      volumeMounts:
        - mountPath: "/var/www/html"
          name: mypersistentvolume
  volumes:
    - name: mypersistentvolume
      persistentVolumeClaim:
        claimName: my-hostpath-pvc
```

```bash
kubectl apply -f pv.yaml
kubectl get pv
kubectl apply -f pv-ns.yaml
kubectl apply -f pvc.yaml
kubectl get pvc -n pv-ns
kubectl apply -f pod.yaml
kubectl get pvc,pod -n pv-ns
```

p0345–p0347. **Effect:** PV cluster-scoped, namespace `pv-ns`, PVC `my-hostpath-pvc` and Pod `nginx`. **Risk:** `hostPath: /tmp/test` local to node; applying can consume existing data; namespace isolation is not a backup. **Verification:** `PV Available`, `PVC Bound`, Pod `Running`. **Rollback:** automatic deletion or recreation **not safe** for persistent data; [Needs confirmation]. Содержимое `pv-ns.yaml` в RAG p0346 не показано полностью; не конструировать неизвестные поля.

## Reclaim policy lifecycle — destructive

```bash
kubectl get pod,pvc -n pv-ns
kubectl delete pod nginx -n pv-ns
kubectl delete pvc my-hostpath-pvc -n pv-ns
kubectl get pv
kubectl patch pv/my-hostpath-pv -p '{"spec":{"persistentVolumeReclaimPolicy":"Delete"}}'
kubectl get pv
```

p0350–p0351. **Effect:** удаляет Pod и PVC; с `Retain` PV переходит в `Released`; patch затем устанавливает `Delete`, а в книге PV сразу исчезает из API. **HIGH RISK:** возможная необратимая потеря backend данных; не считать этот учебный паттерн безопасным cleanup. **Verification:** `get pv` сначала `Released`, затем `No resources found`; recovery/restore [Needs confirmation]. Не запускать для существующих PV/PVC без согласованного backup.

## StorageClass and dynamic provisioning

В RAG p0356–p0358 minikube default `standard` имеет `provisioner: k8s.io/minikube-hostpath`, `reclaimPolicy: Delete`, `volumeBindingMode: Immediate`, `allowVolumeExpansion: false`. Это **свойства среды примера**, не универсальная норма.

Source показывает StorageClass `gce-pd-sc.yaml` с `provisioner: kubernetes.io/gce-pd` (p0357). Современная совместимость этого in-tree provider не проверена. Запуск вне Google Cloud без backend бессмысленен и опасен; **[Needs confirmation]**.

PVC для динамического сценария, p0359:
```yaml
# pvc-dynamic.yaml
apiVersion: v1
kind: PersistentVolumeClaim
metadata:
  name: my-dynamic-hostpath-pvc
spec:
  accessModes:
    - ReadWriteOnce
  storageClassName: standard
  resources:
    requests:
      storage: 1Gi
  selector:
    matchLabels:
      type: hostpath
      env: prod
```

```bash
kubectl create ns dynamicstorage
kubectl get sc
kubectl apply -f pvc-dynamic.yaml -n dynamicstorage
kubectl get pod,pvc,pv -n dynamicstorage
kubectl apply -f pod-with-dynamic-pvc.yaml -n dynamicstorage
kubectl get pod,pvc,pv -n dynamicstorage
```

Pod from p0359–p0360: `metadata.name: nginx-dynamic-storage`, `volumeMounts.mountPath: /var/www/html`, `volumes[].persistentVolumeClaim.claimName: my-dynamic-hostpath-pvc`. **Effect:** StorageClass/provisioner expected to allocate backend and PV on demand; **risk:** cost, reclaim `Delete`, PVC selector can affect dynamic provisioning; compatibility [Needs confirmation]. **Verification:** book reports `Bound` for PVC/PV and Pod `Running`, but other clusters may differ.

**Explicit destructive teardown (p0360–p0361):**
```bash
kubectl delete po nginx-dynamic-storage -n dynamicstorage
kubectl delete pvc my-dynamic-hostpath-pvc -n dynamicstorage
kubectl get pod,pvc,pv -n dynamicstorage
```
Source output: `No resources found` after `Delete` reclaim. **Not a safe rollback** for application data. Verification of physical backend deletion and restoration [Needs confirmation].

## Advanced feature manifests (not fully executable recipes)

CSI clone `pv-cloning.yaml` (p0362):
```yaml
apiVersion: v1
kind: PersistentVolumeClaim
metadata:
  name: cloned-pvc
  namespace: mynamespace
spec:
  accessModes:
    - ReadWriteOnce
  storageClassName: custom-storage-class
  resources:
    requests:
      storage: 5Gi
  dataSource:
    kind: PersistentVolumeClaim
    name: original-pvc
```

**Effect if applied:** attempts clone of PVC with CSI support; **risk:** data duplication, capacity/cost, missing source PVC/class. Chapter provides **no executed command, verified clone output or restore procedure** — [Needs confirmation].

CSI snapshots: `VolumeSnapshot`, `VolumeSnapshotContent`, `VolumeSnapshotClass` described p0363, but no full manifest or executed steps. Availability of CSI driver/CRDs/snapshot-controller [Needs confirmation]. Do not assume snapshot equals application-consistent backup.

Expansion: p0364 shows *incomplete* `storageclass-expandable.yaml` with `allowVolumeExpansion: true` and redacted provisioner, then discusses increasing `PVC.spec.resources.requests.storage`; no full CLI or output shown. **Effect:** potentially allocate larger volume; **risk:** cost and driver support, shrinking/rollback not demonstrated. [Needs confirmation].

## Operational boundary

This chapter includes deprecated and infrastructure-specific historical examples. No real cluster, storage backend, retention and backup state were verified. For any destructive operation, rollback must be a separate approved restore procedure, not `kubectl delete` or a speculative `apply`.
