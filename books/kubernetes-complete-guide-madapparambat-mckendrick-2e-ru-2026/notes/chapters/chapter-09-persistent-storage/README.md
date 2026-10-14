# Глава 9. Постоянное хранилище в Kubernetes

**Книга:** «Kubernetes. Полное руководство по развертыванию и управлению Kubernetes в облачных и локальных средах. 2-е изд.»  
**Inventory:** `0033` · **Book ID:** `kubernetes-complete-guide-madapparambat-mckendrick-2e-ru-2026` · **Chapter:** 09  
**Контракт:** BIBLIOTEKA-VSP-CHAPTER-ARTIFACT-COLLECTION v1.7 · **source policy:** `rag_only`.

## Scope / provenance

- **Chapter boundaries VERIFIED:** PDF/печатные страницы **326–365** включительно, глава 10 начинается на **366**. Оглавление p0013–p0014, заголовок p0326, «Резюме» p0364, источники p0365, следующий заголовок p0366.
- **Addressable chapter RAG:** `kubernetes-complete-guide-madapparambat-mckendrick-2e-ru-2026:p0326:c01` … `kubernetes-complete-guide-madapparambat-mckendrick-2e-ru-2026:p0365:c01` (40 source-page chunks); координаты PDF/printed 326–365; EPUB spine: Not applicable.
- **Canonical source:** `source/book.pdf`; SHA256 `380ccbfc9e0a65cb2e5aa67a671528c15b9ce6eac63ad9aab80b90f91b1e6e65`.
- **RAG acceptance:** `ACCEPTED`, `failed_checks: []`; corpus generation `9fa19b3d399c47de2b9feaf303a9b1895b354beaacda6cd44d100908d3c41842`; index `0a62c809aeded557e1ed8c79d306a4770a3fbf55f4f7436a47865879c1d84a44`.
- **Readiness:** canonical source, RAG acceptance and collection template v1.7 checked on `main`; previous book-readiness workflow `38394894818` PASS. Новый запуск readiness CLI не заявляется.
- **Evidence:** только RAG главы; нет прямого обращения к PDF, внешних источников или исправлений с помощью памяти модели.

## Карта главы

| Раздел | PDF | Ключевые темы |
|---|---:|---|
| Назначение хранения и тома | 326–332 | Внешнее состояние, ConfigMap/Secret volume, emptyDir/hostPath/local, FC и NFS |
| PersistentVolume | 332–335 | Кластерный объект-указатель на базовое хранилище, технологии и ограничения |
| AccessModes | 336–337 | ReadWriteOnce, ReadOnlyMany, ReadWriteMany, ReadWriteOncePod |
| Создание PV | 338–340 | hostPath demo, NFS и FC, `volumeMode: Block`; динамическое provision |
| PVC и подключение к Pod | 341–347 | Разделение ролей администратора и разработчика, PV/PVC binding, namespace и `volumeMounts` |
| Lifecycle, reclaim policy | 348–351 | Available, Bound, Released, Failed; Retain/Delete/устаревший Recycle; опасность patch/delete |
| Static vs dynamic provisioning | 352–360 | CSI, StorageClass, provisioner, PVC, minikube `standard` |
| Продвинутые операции | 361–364 | ephemeral volumes, clone через PVC dataSource, VolumeSnapshot, expansion `allowVolumeExpansion` |
| Резюме и источники | 364–365 | Итоги и переход к контроллерам Kubernetes |

## Основная архитектура

```text
Приложение: Pod (namespace pv-ns)
   └── volumes[*].persistentVolumeClaim.claimName: my-hostpath-pvc
           └── PersistentVolumeClaim (namespace pv-ns)
                   └── Bound → PersistentVolume (cluster-scoped)
                                   └── хранилище: hostPath / NFS / CSI / FC / ...
```

При **статическом** выделении администратор заранее подготавливает хранилище и PV; затем PVC выбирает подходящий PV и Pod подключается к PVC (p0341–p0347). При **динамическом** выделении `StorageClass` и provisioner/CSI создают подходящий PV и физический том после запроса PVC (p0352–p0360).

**Критическая граница:** PV — объект Kubernetes с метаданными, а **не** сам диск (p0333). Сохранность зависит от reclaim policy, драйвера и системы хранения, а не от самого факта существования PV (p0335, p0349–p0351).

## Артефакты

- [cheatsheet.md](cheatsheet.md) — symptom, baseline, диагностика, interpretation, change, verification и rollback.
- [commands.md](commands.md) — команды и YAML только из главы, с классификацией и рисками.
- [diagram.md](diagram.md) — Mermaid-схемы статического/динамического provision и reclaim.
- [visual-cheatsheet.svg](visual-cheatsheet.svg) — компактная визуальная памятка.
- [visual-cheatsheet-detailed.svg](visual-cheatsheet-detailed.svg) — подробная визуальная памятка.
- [summary.md](summary.md) — сохранённый раздел «Резюме» книги p0364.
- [source-findings.md](source-findings.md) — спорные и устаревшие утверждения с точными локаторами.

**Review questions/answers:** [Not applicable] — самостоятельного блока контрольных вопросов или упражнений между p0326–p0365 нет.

## Evidence links

- [Mount ConfigMap, p0328](../../../rag/chunks/p0301-p0400/p0328-c01.md)
- [Local vs network storage, p0330](../../../rag/chunks/p0301-p0400/p0330-c01.md)
- [PV as pointer, p0333](../../../rag/chunks/p0301-p0400/p0333-c01.md)
- [PV access modes, p0336](../../../rag/chunks/p0301-p0400/p0336-c01.md)
- [hostPath example, p0338](../../../rag/chunks/p0301-p0400/p0338-c01.md)
- [NFS example, p0339](../../../rag/chunks/p0301-p0400/p0339-c01.md)
- [PVC and namespace, p0342](../../../rag/chunks/p0301-p0400/p0342-c01.md)
- [PV/PVC binding, p0346](../../../rag/chunks/p0301-p0400/p0346-c01.md)
- [Reclaim policy, p0349](../../../rag/chunks/p0301-p0400/p0349-c01.md)
- [Dangerous patch, p0351](../../../rag/chunks/p0301-p0400/p0351-c01.md)
- [CSI, p0353](../../../rag/chunks/p0301-p0400/p0353-c01.md)
- [StorageClass, p0356](../../../rag/chunks/p0301-p0400/p0356-c01.md)
- [Dynamic PVC, p0359](../../../rag/chunks/p0301-p0400/p0359-c01.md)
- [Clone, p0362](../../../rag/chunks/p0301-p0400/p0362-c01.md)
- [Expansion and summary, p0364](../../../rag/chunks/p0301-p0400/p0364-c01.md)

## Safety

Ни одна команда Kubernetes не выполнялась против реального кластера. Примеры `hostPath`, `fc`, `Recycle`, `kubernetes.io/gce-pd` и PVC selector в динамическом сценарии содержат ограничения/версионные вопросы; см. [source-findings.md](source-findings.md). **Удаление PVC при Delete может привести к потере тома и данных**; смена policy у Released PV может сработать как разрушительное изменение (p0350–p0351). Для production необходимы контекст, RBAC, backup, backend/CSI compatibility и rollback [Needs confirmation]. Исходный PDF, RAG, registry и статус/прогресс чтения не меняются.
