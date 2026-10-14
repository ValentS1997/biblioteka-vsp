# Commands — Глава 12: StatefulSet, PVC, DNS, scaling, rollout

**Source:** только RAG PDF **420–456**, `p0420:c01`–`p0456:c01`. Ничего не исполнялось. Не добавлять отсутствующие в source команды. Для действий с базой данных и хранилищем считать полное восстановление **[Needs confirmation]**.

## Read-only observation (Kubernetes)

| Источник | Команда | Результат/ограничение |
|---|---|---|
| p0432 | `kubectl describe statefulset mysql-stateful -n mysql` | объект StatefulSet |
| p0432 | `kubectl get sts -n mysql` | READY 3/3 в книге |
| p0432 | `kubectl get pod -n mysql` | ordinal names 0/1/2 |
| p0432–p0433 | `kubectl -n mysql describe pod mysql-stateful-0` | `ClaimName: mysql-data-mysql-stateful-0` |
| p0433 | `kubectl -n mysql describe pod mysql-stateful-1` | claim с ordinal 1 |
| p0433, p0441 | `kubectl get pvc -n mysql` | отдельные `Bound` PVC |
| p0434 | `kubectl get pv` | cluster-scoped PV; source reclaim = `Delete` |
| p0437, p0439, p0440 | `kubectl get po -n mysql` / `kubectl get pod -n mysql` | пересоздание и число реплик |
| p0439 | `kubectl describe pod -n mysql -l app=mysql \| egrep 'ClaimName\|Name:'` | соответствие Pod/PVC |
| p0441, p0447 | `kubectl describe sts -n mysql mysql-stateful` | события контроллера и порядок |
| p0447, p0450, p0451 | `kubectl rollout status statefulset -n mysql` | прогресс; возможное ожидание Ready |
| p0448–p0450 | `kubectl describe pod -n mysql mysql-stateful-0 \| grep Image`, `kubectl describe pod -n mysql mysql-stateful-2 \| grep Image` | текущие версии image |

В `rollout status statefulset -n mysql` source не называет конкретный StatefulSet; в неизвестном namespace нужно сначала установить scope. `rollout status` может ожидать завершения, не является операцией восстановления.

## Create resources (workload-generating / state-changing)

Тестовая топология: namespace `mysql`, headless Service, Secret, StatefulSet, вспомогательный Pod `k8sutils`. Source p0428–p0434.

```yaml
# mysql-statefulset.yaml (объединено из непрерывных фрагментов p0428–p0430)
apiVersion: apps/v1
kind: StatefulSet
metadata:
  name: mysql-stateful
  labels:
    app: mysql
  namespace: mysql
spec:
  serviceName: mysql-headless
  replicas: 3
  selector:
    matchLabels:
      app: mysql
      environment: test
  template:
    metadata:
      labels:
        app: mysql
        environment: test
    spec:
      containers:
        - name: mysql
          image: mysql:8.2.0
          ports:
            - containerPort: 3306
          volumeMounts:
            - name: mysql-data
              mountPath: /var/lib/mysql
          env:
            - name: MYSQL_ROOT_PASSWORD
              valueFrom:
                secretKeyRef:
                  name: mysql-secret
                  key: MYSQL_ROOT_PASSWORD
            - name: MYSQL_USER
              valueFrom:
                secretKeyRef:
                  name: mysql-secret
                  key: MYSQL_USER
            - name: MYSQL_PASSWORD
              valueFrom:
                secretKeyRef:
                  name: mysql-secret
                  key: MYSQL_PASSWORD
  volumeClaimTemplates:
    - metadata:
        name: mysql-data
      spec:
        accessModes: ["ReadWriteOnce"]
        resources:
          requests:
            storage: 1Gi
```

```yaml
# mysql-headless-service.yaml, p0431
apiVersion: v1
kind: Service
metadata:
  name: mysql-headless
  namespace: mysql
spec:
  selector:
    app: mysql
    environment: test
  clusterIP: None
  ports:
    - port: 3306
```

Source confirms:
```bash
kubectl apply -f mysql-ns.yaml
kubectl apply -f mysql-headless-service.yaml
kubectl apply -f mysql-statefulset.yaml
kubectl apply -f k8sutils.yaml -n mysql
```

**Effect:** creates namespace, Service, 3 MySQL Pod and one PVC/PV per Pod (when provisioner works), and debug Pod. **Risk:** MySQL data integrity, missing default StorageClass, storage charges and security; Pod `mysql:8.2.0` historical. **Verification:** `get sts/pod/pvc/pv`, `describe pod`, `Bound`. **Rollback:** none safe or complete; source only shows disruptive delete and warns about data retention; **[Needs confirmation]**.

### Secret creation — sensitive command

p0431 source uses `kubectl create secret generic mysql-secret --from-literal=MYSQL_ROOT_PASSWORD=... --from-literal=MYSQL_USER=... --from-literal=MYSQL_PASSWORD=... -n mysql`. **Это state-changing и может оставить пароль в history, списках процессов, логах.** Исходные демонстрационные парольные значения не воспроизводятся в файлах артефактов. В p0432 упомянут альтернативный YAML `mysql-secret.yaml` с base64; plaintext и Base64 не дают гарантию шифрования. Safe secret ingress, RBAC, KMS/backup **[Needs confirmation]**. **Verification:** source показывает `secret/mysql-secret created`; не печатать значение.

Debug image p0434:
```yaml
# k8sutils.yaml
apiVersion: v1
kind: Pod
metadata:
  name: k8sutils
spec:
  containers:
    - name: k8sutils
      image: quay.io/iamgini/k8sutils:debian12-1.1
      command: ["sleep", "infinity"]
  restartPolicy: Always
```

## Network diagnostics and SQL

p0435–p0438 inside debug Pod:
```bash
kubectl exec -it -n mysql k8sutils -- /bin/bash
```
Within shell:
```bash
nslookup mysql-headless
mysql -u root -p -h mysql-headless.mysql.svc.cluster.local
mysql -u root -p -h mysql-stateful-0.mysql-headless
```
Within MySQL shell:
```sql
SHOW DATABASES;
CREATE DATABASE ststest;
```

**Classification:** `exec` creates an interactive process, `nslookup` and MySQL client open connections; `SHOW DATABASES` is observational but access-controlled, `CREATE DATABASE` **mutates persistent state**. **Risk:** connecting headless service can reach any matching Pod, with distinct unsynchronised databases; do not log passwords or create test DB in production. **Verification:** on **mysql-stateful-0** after deleting/recreating that Pod, `SHOW DATABASES` still lists `ststest` (p0437–p0438). **Rollback for CREATE DATABASE:** not provided [Needs confirmation]; **do not invent DROP**.

## Destructive Pod tests

```bash
kubectl delete po -n mysql mysql-stateful-0
kubectl delete po -n mysql mysql-stateful-0 mysql-stateful-1 mysql-stateful-2
```

p0437–p0439. **Effect:** forcibly removes Pod, controller recreates same ordinal name and attaches same PVC. **Risk:** downtime, database sessions interrupted; depending on backend may require safe detach/re-attach. **Verification:** `kubectl get pod -n mysql`, `describe pod … ClaimName`, `SHOW DATABASES` shows `ststest` in the example. **Rollback:** re-creation is automatic for Pod, not a universal data restore; [Needs confirmation].

## Scaling and persistence

p0440–p0441:
```bash
kubectl scale statefulset -n mysql mysql-stateful --replicas=4
kubectl get pod -n mysql
kubectl describe sts -n mysql mysql-stateful
kubectl scale statefulset -n mysql mysql-stateful --replicas=2
kubectl get pvc -n mysql
```

**Effect:** Pod `-3` created, then `-3` and `-2` removed in reverse order, all four PVC remained `Bound` in source. **Risk:** no automatic replication of MySQL state, capacity and cost, availability during scale changes. **Verification:** ordinal pods and 4 PVC retained. **Rollback:** returning replicas number not equivalent to reversing database writes; [Needs confirmation].

## Removal: mutually exclusive and dangerous

```bash
kubectl delete sts -n mysql mysql-stateful
kubectl delete sts -n mysql mysql-stateful --cascade=orphan
```

p0442–p0443. **Not sequential.** Default delete removes workload Pod and StatefulSet (not guaranteed ordered); orphan leaves Pod. `persistentVolumeClaimRetentionPolicy` may change PVC retention from default behaviour:
```yaml
# Source fragment, p0442
spec:
  persistentVolumeClaimRetentionPolicy:
    whenDeleted: Retain
    whenScaled: Delete
```
**Effect:** potential PVC removal on scale-down; actual running policy, PV reclaim and finalizers must be inspected before action, [Needs confirmation]. **Verification:** get Pod/PVC/PV. **Rollback:** not provided.

**Destructive storage delete, p0443:**
```bash
kubectl delete -n mysql pvc mysql-data-mysql-stateful-0 mysql-data-mysql-stateful-1 mysql-data-mysql-stateful-2 mysql-data-mysql-stateful-3
```
**Never routine rollback.** In example PV `reclaimPolicy: Delete` (p0434), deleting PVC can delete backing volume and database bytes. No verified recovery; [Needs confirmation].

## Rollout / staged upgrade

p0445–p0451:
```bash
cp mysql-statefulset.yaml mysql-statefulset-rolling-update.yaml
kubectl apply -f mysql-statefulset-rolling-update.yaml
kubectl rollout status statefulset -n mysql
kubectl describe sts -n mysql mysql-stateful
kubectl describe pod -n mysql mysql-stateful-0 | grep Image
kubectl describe pod -n mysql mysql-stateful-2 | grep Image
```

**Source:** file `mysql-statefulset-rolling-update.yaml` is shown only as snippets, with `...<фрагмент опущен>`; no executable full manifest in chapter RAG. Configure `spec.updateStrategy.type: RollingUpdate`, `rollingUpdate.partition: 0`, `podManagementPolicy: OrderedReady`, start MySQL 8.2.0, update to 8.3.0, then canary 8.4.0:
- `partition: 3`: staged, no Pod upgraded
- `partition: 2`: only `mysql-stateful-2` upgraded to 8.4.0
- `partition: 0`: complete 8.4.0 rollout (p0449–p0451)

`kubectl -n mysql set image sts mysql-stateful mysql=mysql:8.3.0` (p0449) and `kubectl patch sts mysql-stateful -p '{"spec":{"updateStrategy":{"type":"RollingUpdate","rollingUpdate":{"partition":3}}}}' -n mysql` (p0451) are **state-changing, not recommended for production by authors**. Full update/rollback and data compatibility require separate review. **Verification:** `rollout status`, image in per-Pod `describe`, SQL `stsrolling` persists on mysql-stateful-0 (p0448–p0449). **Risk:** MySQL schema changes and stalled readiness may make undo unsafe.

`CREATE DATABASE stsrolling;` is a mutating SQL step on p0446. No source-supported cleanup; [Needs confirmation].

## Rollback boundary

p0452 suggests reverting a Git commit and reapplying YAML or `kubectl rollout undo`, but **requires reverse schema migration** if an image update changed DB format. No validated restore procedure, RPO/RTO or backup test in the source. State change is not reversible by simply restoring a Pod object. **[Needs confirmation]**.
