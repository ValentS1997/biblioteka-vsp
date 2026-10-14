# Cheatsheet — Глава 9. PersistentVolume, PVC, StorageClass

**Source only:** RAG PDF 326–365, `kubernetes-complete-guide-madapparambat-mckendrick-2e-ru-2026:p0326:c01`–`…:p0365:c01`. Никакие примеры не выполнялись.

## Symptom / problem framing

Под пересоздан и потерял локальные данные, рабочую нагрузку перенесли на другой узел или приложению нужен долговременный том. Прямые `emptyDir` / `hostPath` ограничены жизненным циклом/местом хранения, поэтому глава вводит независимый ресурс `PersistentVolume` (PV) и заявку `PersistentVolumeClaim` (PVC), связывающую его с Pod (p0327–p0335, p0341–p0347). Нужны одновременно **доступ, сохранность и жизненный цикл данных**, а не только успешный `Running`.

## Baseline / context

- Доступный кластер и `kubectl` (p0326); идентификатор кластера, namespace, CSI/backend, права, размер хранилища и backup **[Needs confirmation]**.
- PV — cluster-scoped объект, «указатель» на физическое или сетевое хранилище, **не сам диск** (p0333); PVC и Pod — namespace-scoped, PVC должен находиться в namespace Pod (p0342–p0344).
- `accessModes`: `ReadWriteOnce` (один узел RW), `ReadOnlyMany` (многие узлы RO), `ReadWriteMany` (многие узлы RW), `ReadWriteOncePod` (один Pod RW); поддержка зависит от драйвера (p0336–p0337).
- `volumeMode`: `Filesystem` для файлов, `Block` для блочного доступа в примере FC (p0339–p0340).
- `persistentVolumeReclaimPolicy`: `Retain`, `Delete`, `Recycle` (**deprecated по книге**, p0349–p0350); выбор влияет на судьбу тома и данных **при удалении PVC**.
- **Static provisioning**: подготовить backend → создать PV → PVC → Pod. **Dynamic**: StorageClass с provisioner/CSI → PVC → PV/backend создаётся автоматически → Pod (p0352–p0360).
- Пример minikube `standard`/ `k8s.io/minikube-hostpath` относится только к учебной среде, не гарантирован во всех кластерах (p0356, p0358).

## Read-only checks

```bash
kubectl get persistentvolume
kubectl get pv
kubectl get persistentvolumeclaims
kubectl get pvc
kubectl get pv
kubectl get pvc -n pv-ns
kubectl get pvc,pod -n pv-ns
kubectl api-resources --namespaced=false | grep -i volume
kubectl get pod,pvc -n pv-ns
kubectl get sc
kubectl get storageclasses standard -o yaml
kubectl get pod,pvc,pv -n dynamicstorage
```

RAG p0332, p0341, p0345–p0348, p0350–p0351, p0356, p0358–p0360. `kubectl get pv` показывает кластерные PV даже при `-n`; `get pvc -n` ограничен namespace. Наблюдать `CAPACITY`, `ACCESS MODES`, `STORAGECLASS`, `RECLAIM POLICY`, `STATUS`, `CLAIM`. Не считать пустой вывод безопасным подтверждением отсутствия физических дисков.

## Interpretation

- `PV Available`: не привязан; `PVC Bound` / `PV Bound`: связывание состоялось; `PV Released`: запрос удалён, том ещё существует, **не обязательно вновь Available** (p0345–p0351).
- `PVC Pending`: конкретная причина не устанавливается из одного `get`; проверить размер, режим доступа, StorageClass, метки/selector, поддержку provisioner. Команда детальной диагностики PVC с событиями **не приводится в главе** — [Needs confirmation].
- Reclaim `Delete` может удалить PV и базовое хранилище после удаления PVC; `Retain` оставляет Released и требует работы администратора (p0349–p0351). Избегать автоматического «очищения» Released PV.
- Под с `volumes[].persistentVolumeClaim.claimName` монтирует PVC, не PV напрямую. Условие: claim и Pod в одном namespace (p0342, p0347).
- В динамическом примере PVC создан в `dynamicstorage` при `storageClassName: standard`; если `standard` не существует или несовместим, демонстрационный workflow не применим (p0358–p0360).
- `hostPath` из p0338 и p0345 — лабораторный вариант; автор прямо запрещает считать его подходящим для критичных production-данных (p0338). `NFS` требует рабочий экспорт (p0339).

## Next action

1. Согласовать с владельцем данных требования к retention, downtime, backup и restore; подтвердить реальный namespace, StorageClass, accessModes/volumeMode, provisioner/CSI и физическую технологию (внешние исходные данные [Needs confirmation]).
2. Для тестов — источник предлагает статический `hostPath` или динамический `minikube standard`. Это разные сценарии, **не объединять все YAML в один кластер без проверки уникальных имён**.
3. Сначала наблюдать PV/PVC/StorageClass и их политики, затем создавать тестовые ресурсы только с одобренным retention.
4. Перед удалением PVC и особенно изменением reclaim на `Delete` — убедиться в наличии восстановимой копии данных. Глава **не содержит работающую backup/restore процедуру**.

## Modifying action

**Статический путь (p0345–p0347):**
```bash
kubectl apply -f pv.yaml
kubectl apply -f pv-ns.yaml
kubectl apply -f pvc.yaml
kubectl apply -f pod.yaml
```
Эффект: кластерный PV `my-hostpath-pv` → namespace `pv-ns` → PVC `my-hostpath-pvc` (`Bound`) → Pod `nginx`, mount `/var/www/html`. **Риск:** hostPath привязан к узлу, использует локальный путь `/tmp/test`; без резервирования/контроля нельзя полагаться на сохранность. Verification: `kubectl get pv`, `kubectl get pvc,pod -n pv-ns`. Rollback отсутствует в безопасном виде — [Needs confirmation].

**Динамический путь (p0358–p0360):**
```bash
kubectl create ns dynamicstorage
kubectl get sc
kubectl apply -f pvc-dynamic.yaml -n dynamicstorage
kubectl apply -f pod-with-dynamic-pvc.yaml -n dynamicstorage
```
Эффект: при наличии `standard` provisioner создаёт PV/том и привязывает PVC, Pod монтирует claim. **Риск:** storage consumption и провайдерская стоимость, reclaim `Delete`, непроверенный selector `matchLabels` в динамическом PVC. Verification: `kubectl get pod,pvc,pv -n dynamicstorage` с `Bound`, `Running` (в книге). При нехватке возможностей backend — [Needs confirmation].

## Verification / acceptance checks

- Статика: `kubectl get pv` → `my-hostpath-pv` сначала `Available`, `kubectl get pvc -n pv-ns` → `my-hostpath-pvc Bound`, `kubectl get pvc,pod -n pv-ns` → Pod `1/1 Running` (p0345–p0347).
- Динамика: `kubectl get sc` → `standard` в minikube, затем `get pod,pvc,pv -n dynamicstorage` → PVC/PV `Bound` и Pod `Running` (p0358–p0360). Данные о фактическом throughput, persistence across host failure или корректности backup не представлены.
- Изменение reclaim: пример p0350–p0351 показывает `Released` после удаления PVC при `Retain`. Перевод на `Delete` приводит к удалению PV из API в примере. Это **отрицательное последствие**, не безопасный acceptance тест.
- CSI clones / snapshots / expansion описаны преимущественно концептуально; выполнение не показано. Условия драйвера, capacity, доступность CRD и успешное восстановление: [Needs confirmation].

## Rollback

- **НЕ** использовать удаление PVC как универсальный откат. `kubectl delete pvc my-hostpath-pvc -n pv-ns` по книге с `Retain` оставляет `Released`; при `Delete` возможно удаление backing storage (p0349–p0351).
- `kubectl patch pv/my-hostpath-pv -p '{"spec":{"persistentVolumeReclaimPolicy":"Delete"}}'` для `Released` PV — **в примере приводит к немедленному удалению** (p0351), потенциально необратимо.
- `kubectl delete po nginx-dynamic-storage -n dynamicstorage` и `kubectl delete pvc my-dynamic-hostpath-pvc -n dynamicstorage` приводят к удалению динамического PV в демонстрации (p0360–p0361). Не выполнять с данными, которые нужно сохранить.
- Обратное развертывание YAML не восстанавливает уничтоженные байты. Надёжный план backup/restore и retention вне источника — **[Needs confirmation]**.

## Source caveats

У источника есть противоречия в описании reclaim на удалении Pod vs PVC, статусе Released и динамическом selector PVC, а также устаревший пример `Recycle`. Они сохранены в [source-findings.md](source-findings.md), без исправлений из внешней документации. Для актуального Kubernetes API и конкретного storage backend нужна отдельная проверка.
