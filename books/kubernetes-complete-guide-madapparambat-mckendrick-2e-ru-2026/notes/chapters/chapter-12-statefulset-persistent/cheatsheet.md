# Cheatsheet — Глава 12. StatefulSet, stable identity, storage и rollout

**Source:** только RAG PDF **420–456**, chunks `p0420:c01`–`p0456:c01`. Примеры не исполнялись.

## Symptom / framing

Нужно обновлять или перемещать поды MySQL, сохраняя изменяемые данные и однозначную идентичность каждой реплики. Обычные Pod эфемерны, а одно PVC для нескольких replicas Deployment само по себе не синхронизирует независимые экземпляры БД (p0421–p0424). **StatefulSet** обеспечивает детерминированные имена, порядковый lifecycle и отдельную claim на Pod через `volumeClaimTemplates` (p0424–p0430), но **не обеспечивает синхронизацию самих данных, отказоустойчивость БД или внешние backup** (p0427).

## Baseline / context

- Cluster + `kubectl`, возможность выделения PVC; в примере minikube default StorageClass `standard`, provisioner `k8s.io/minikube-hostpath` (p0420, p0430–p0434). Реальные context, namespace, RWO backend, привилегии, совместимость образов и backup **[Needs confirmation]**.
- Namespace `mysql`, `StatefulSet: mysql-stateful`, `spec.serviceName: mysql-headless`, `replicas: 3`, Pod `mysql-stateful-0/1/2`, `image: mysql:8.2.0` (p0429).
- `mysql-headless` — `Service clusterIP: None`, selector `app=mysql,environment=test`, port 3306 (p0431). Stable DNS `mysql-stateful-0.mysql-headless.mysql.svc.cluster.local` в исходной логике, краткий lookup `mysql-stateful-0.mysql-headless` в одноимённом namespace (p0435–p0436); реальный cluster domain [Needs confirmation].
- `volumeClaimTemplates: name=mysql-data`, `ReadWriteOnce`, `requests.storage: 1Gi` → `mysql-data-mysql-stateful-0/1/2`, каждый отдельный PVC и PV (p0430, p0433–p0434).
- Secret `mysql-secret` нужен заранее; env `MYSQL_ROOT_PASSWORD`, `MYSQL_USER`, `MYSQL_PASSWORD` с `secretKeyRef` (p0429–p0431). **Не копировать пример plaintext credentials** в shell или Git.

## Read-only verification

```bash
kubectl describe statefulset mysql-stateful -n mysql
kubectl get sts -n mysql
kubectl get pod -n mysql
kubectl -n mysql describe pod mysql-stateful-0
kubectl -n mysql describe pod mysql-stateful-1
kubectl get pvc -n mysql
kubectl get pv
kubectl describe pod -n mysql -l app=mysql | egrep 'ClaimName|Name:'
kubectl describe sts -n mysql mysql-stateful
kubectl rollout status statefulset -n mysql
kubectl describe pod -n mysql mysql-stateful-0 | grep Image
kubectl describe pod -n mysql mysql-stateful-2 | grep Image
```

Книга: p0432–p0434, p0439–p0441, p0447–p0450. `rollout status` может долго ожидать (p0447), не принимать это за доказательство бесконечной работоспособности. `kubectl get pv` показывает cluster-scoped PV; `pvc` привязаны к namespace.

## Interpretation

- Pod name ordinal и соответствующий PVC **не меняются** при удалении/пересоздании Pod (p0437–p0439); IP в демонстрации поменялся, но фиксированность IP **не** является гарантией.
- `mysql-data-mysql-stateful-0` принадлежит Pod `mysql-stateful-0`, `-1` — Pod `-1` и т. д.; `Bound` подтверждает наличие заявки, **не** полноценный backup/replication (p0433–p0434).
- MySQL `ststest` создан в **одной** реплике и наблюдается после пересоздания той же реплики (p0437–p0438). В других Pod наличие `ststest` не показано.
- `OrderedReady`: создание 0→1→2, scale-down N-1→0; ожидание Ready предыдущих Pod (p0440). `Parallel` допускает параллельное масштабирование, но сам автор оговаривает, что оно **не меняет порядок RollingUpdate**.
- После scale 3→4→2 Pod `-3` и `-2` удаляются, а все 4 PVC в книге сохраняются (p0440–p0442) **при показанной политике хранения**.
- `persistentVolumeClaimRetentionPolicy.whenScaled: Delete` — отдельная версия поведения (p0442); нельзя переносить вывод «PVC всегда остаются» на любую политику.
- RollingUpdate Pod `-2→-1→-0`, `partition: 3` удерживает все 3, `partition: 2` обновляет только `-2`, `partition: 0` все оставшиеся (p0444–p0451).

## Next action

Возможности StorageClass, backup/restore, репликации/схемы БД и реальные endpoints нужно подтвердить отдельно. Перед обновлением проверить `pvc Bound`, версии/схему данных, DNS, мониторинг, retention policy, `Ready` всех реплик и вариант безопасной остановки. В production авторы предпочитают Git/IaC и декларативный `apply` (p0452–p0453). Тесты удаления — только disposable cluster.

## Controlled modifying steps (source)

```bash
kubectl apply -f mysql-ns.yaml
kubectl apply -f mysql-headless-service.yaml
kubectl apply -f mysql-statefulset.yaml
kubectl apply -f k8sutils.yaml -n mysql
kubectl scale statefulset -n mysql mysql-stateful --replicas=4
kubectl scale statefulset -n mysql mysql-stateful --replicas=2
kubectl apply -f mysql-statefulset-rolling-update.yaml
```

**Effect:** namespace, headless service, Pod/PVC/PV creation, debug Pod, scale, rollout. **Risk:** hostPath portability, separate MySQL datasets, compute/storage charges, disruption and schema incompatibility. **Verification:** `get sts/pod/pvc/pv`, `describe sts`, `rollout status`, `describe pod | grep Image`; `show databases;` внутри MySQL относится к одному выбранному Pod (p0435–p0438, p0447–p0451). **Rollback:** безопасного общего rollback не дано; p0452 требует обратной миграции схемы, если формат изменён — **[Needs confirmation]**.

## Destructive and recovery steps

```bash
kubectl delete po -n mysql mysql-stateful-0
kubectl delete po -n mysql mysql-stateful-0 mysql-stateful-1 mysql-stateful-2
kubectl delete sts -n mysql mysql-stateful
kubectl delete sts -n mysql mysql-stateful --cascade=orphan
```

Эти команды **разрушают Pod/контроллер**. Последние две — **взаимоисключающие варианты**, не последовательность. В p0437–p0439 демонстрация сохраняет данные `ststest` за счёт PVC. Но при удалении StatefulSet p0442–p0443 **не гарантирован порядок завершения Pod** — сначала scale to zero рекомендован для безопасного завершения. `--cascade=orphan` оставляет Pod без контроллера и не доказывает безопасность их дальнейшего управления. Verification: `get pod`, `get pvc`, SQL `show databases;`. Rollback полностью **[Needs confirmation]**.

**Особо опасно:**
```bash
kubectl delete -n mysql pvc mysql-data-mysql-stateful-0 mysql-data-mysql-stateful-1 mysql-data-mysql-stateful-2 mysql-data-mysql-stateful-3
```
p0443. При показанном minikube PV с `Delete` это может **уничтожить тома и БД**. **Не выполнять как cleanup или rollback до backup/restore и письменного допуска.** Успешное воссоздание YAML не восстанавливает данные.

## Acceptance / rollback boundary

- Наблюдать 3 Pod `Running`, 3 PVC `Bound`, свои claim names (p0432–p0434).
- `nslookup mysql-headless` из k8sutils показывает 3 адреса, `mysql -u root -p -h mysql-stateful-0.mysql-headless` соединяется с конкретной репликой (p0435–p0436). Эти команды создают процессы/сетевые соединения, имеют риск disclosure паролей.
- После удаления Pod `-0` `ststest` остаётся при прежнем PVC (p0437–p0438).
- После rolling update 8.2.0→8.3.0 и частичного 8.3.0→8.4.0 `describe pod ... | grep Image` подтверждает разные версии по ordinal (p0448–p0450).
- База данных `stsrolling` сохраняется при обновлении конкретного PVC (p0448–p0449). Межрепликовая репликация, RPO/RTO, отказ узла и disaster recovery в RAG не доказаны: **[Needs confirmation]**.
- Возврат к предыдущему образу требует проверки сохранённых данных и **обратной миграции**, если изменилась схема (p0452–p0454). Подмена image tag или `rollout undo` сама по себе не является восстановлением.

## Caveats

Не трактовать предложение p0455 о «переключении на другой исправный под с тем же состоянием» как реализованную отказоустойчивость БД: p0427 явно отвергает автоматическую репликацию StatefulSet. Версии StorageClass/CSI и retention behaviour зависят от реальной среды. См. [source-findings.md](source-findings.md).
