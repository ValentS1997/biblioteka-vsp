# Source findings — Глава 9: постоянное хранилище

**Policy:** `rag_only`. Evidence: `kubernetes-complete-guide-madapparambat-mckendrick-2e-ru-2026:p0326:c01`–`…:p0365:c01`. Это журнал **исходных противоречий, неопределённостей и версионных ограничений**; он не исправляет книгу по памяти модели или внешним источникам. Реальное поведение кластера — **[Needs confirmation]**.

## F-01 — [Source contradiction]: reclaim trigger, Pod vs PVC

- **p0335:** автор прямо пишет, что при `Delete` том и данные удаляются «при удалении пода».
- **p0349–p0350:** reclaim policy определена как реакция на **удаление PVC**; источник последовательно удаляет Pod, затем PVC, после чего PV `Released` при `Retain`.
- **p0360–p0361:** динамический PV исчезает после удаления PVC при `Delete`.
- **Boundary:** не утверждать по p0335, что любое удаление Pod автоматически удаляет PV/том. При принятии операционного решения проверять конкретную связь PVC, reclaim policy и драйвер. **[Needs confirmation]**.

## F-02 — [Source contradiction]: hostPath / emptyDir lifecycle и гарантия PV

- **p0333:** emptyDir и hostPath названы «оба привязаны к жизненному циклу пода» с уничтожением данных при его удалении.
- **p0335, p0338, p0345–p0347:** тот же источник создаёт PV, ссылающийся на hostPath, и описывает его сохранение за пределами Pod, но признаёт узловую привязку и ограничения.
- **Boundary:** не сводить объект `hostPath` (прямое подключение), hostPath backend в PV и долговечность базовых файлов к одной гарантии. Реальный драйвер, путь, отказ узла и сохранность [Needs confirmation].

## F-03 — [Source contradiction]: Released как доступный для нового PVC

- **p0351:** статус `Released` описан словами «отвязан, но остается доступным для будущих PVC».
- **p0350:** пример `kubectl get pv` показывает `Released`, после чего прямо сказано, что PV **ещё не** `Available` для другого PVC.
- **Boundary:** освобождение тома не является доказательством безопасного повторного использования. Процедура reclaim/manual recovery **[Needs confirmation]**.

## F-04 — [Source/version limitation]: устаревший Recycle в рабочем YAML

- **p0339:** `pv-nfs.yaml` использует `persistentVolumeReclaimPolicy: Recycle`.
- **p0350:** `Recycle` прямо объявлен устаревшим, далее рекомендуется динамическое provision.
- **Boundary:** сохранять как исторический код книги, но не объявлять production-ready. Совместимость текущего API [Needs confirmation].

## F-05 — [Needs confirmation]: dynamic PVC selector и успешный Bound

- **p0359:** `pvc-dynamic.yaml` для `storageClassName: standard` одновременно задаёт `selector.matchLabels.type: hostpath` и `env: prod`.
- **p0359–p0360:** source показывает созданный динамический PV со статусом `Bound`; при этом явно не подтверждён набор меток автоматически созданного PV и их согласование с selector.
- **Boundary:** не выдавать манифест за универсальный воспроизводимый способ динамического provisioning на любом provisioner. Совместимость заданного selector, способность драйвера и фактический outcome **[Needs confirmation]**.

## F-06 — [Source/version limitation]: миграция in-tree volume plugins и StorageClass

- **p0334:** приводится перечень типов, «удалённых или устаревших с момента Kubernetes 1.29» (awsElasticBlockStore, azureDisk, azureFile, portworxVolume, flexVolume, vsphereVolume, cephfs, cinder) без раздельной таблицы точных дат/статусов.
- **p0357:** далее дан пример `provisioner: kubernetes.io/gce-pd` в `gce-pd-sc.yaml`.
- **Boundary:** статья книги не подтверждает актуальную поддержку каждого конкретного in-tree провиженера в текущем кластере. Требуется отдельная проверка конкретного API/CSI миграции. **[Needs confirmation]**.

## F-07 — [Source overgeneralization]: access modes для block/file

- **p0336:** таблица допускает `ReadOnlyMany` для FC и iSCSI, а CSI режимы ставит в зависимость от драйвера.
- **p0337:** затем сказано, что блочное хранилище «поддерживает только режим RWO», тогда как сетевое файловое якобы всегда предназначено для многопользовательского доступа.
- **Boundary:** источник сам показывает различные сочетания. Не заменять таблицу жёстким универсальным ограничением без указания backend. **[Needs confirmation]**.

## F-08 — [Needs confirmation]: PV как гарантия сохранности и доступа на любом узле

- **p0333–p0335:** заявлены независимость PV от Pod и доступность из любого узла.
- **p0335:** прямо оговорено, что `hostPath` ограничен узлом и три перечисленных «преимущества» не всегда верны.
- **p0349–p0351:** reclaim `Delete` может уничтожать данные.
- **Boundary:** PV — *указатель* на backend, не избыточное защищённое хранилище. Резервное копирование, отказоустойчивость, доступ из другого узла **[Needs confirmation]**.

## F-09 — [Source wording/code mismatch]: путь ConfigMap тома

- **p0328:** `nginx-pod.yaml` задаёт `mountPath: "/usr/share/nginx/html/hello"`.
- **p0329:** текст сначала описывает `/usr/share/nginx/hello`, а `kubectl exec -- ls` затем использует `/usr/share/nginx/html/hello/`.
- **Boundary:** при исполнении ориентироваться на актуальный YAML и не смешивать пути.

## F-10 — [Needs confirmation]: ограничение размера ConfigMap/etcd

- **p0329:** заявлен предел «1,5 Мбайт» из ограничений etcd для рассматриваемых объектов конфигурации.
- **Boundary:** максимальный размер конкретного Kubernetes API объекта и лимит backend etcd не тождественны; chapter RAG не проверяет реальный лимит target cluster и версию. Не применять число для quota/SLA без проверки. **[Needs confirmation]**.

## F-11 — [Needs confirmation]: reclaim Delete после patch Released PV

- **p0350–p0351:** `kubectl patch pv/my-hostpath-pv ... Delete` выполняется для Released PV и `get pv` показывает отсутствие объектов.
- **Boundary:** p0351 доказывает исход одного учебного кластера, а не одинаковый эффект для всех backend. Нет подтверждения уничтожения **фактических данных** на каждом провайдере и возможности восстановления. **[Needs confirmation]**.

## F-12 — [Source wording/code mismatch]: CSI ephemeral volume lifecycle

- **p0355:** универсальный ephemeral том в контексте CSI описан как временный, «не сохраняемый при перезапуске пода».
- **p0361–p0362:** общий эффект эфемерных томов связан с завершением жизни Pod.
- **Boundary:** термины «перезапуск контейнера» и «пересоздание/удаление Pod» различаются, но в источнике не раскрыты по отдельности. Не заявлять автоматическую потерю данных при любом рестарте контейнера. **[Needs confirmation]**.

## F-13 — [Needs confirmation]: VolumeSnapshot как полная backup гарантия

- **p0363:** VolumeSnapshot представлен как «точная копия данных на конкретный момент» и средство для backup/restore; упоминаются snapshot CRD/controller/CSI.
- **Boundary:** глава не демонстрирует успешный snapshot/restore, согласование данных работающего приложения, ретенцию и изоляцию backup. Снимок не доказан полноценным application-consistent backup. **[Needs confirmation]**.

## F-14 — [Needs confirmation]: клонирование как средство репликации и восстановление

- **p0362:** `pv-cloning.yaml` использует `dataSource: kind: PersistentVolumeClaim`, `original-pvc`, `storageClassName: custom-storage-class` и новый `cloned-pvc`.
- **p0363:** текст объявляет клоны «идентичными копиями PV», однако рабочее состояние, допустимость source PVC, namespace и фактическая точность копирования не показаны.
- **Boundary:** не путать клон PVC/данных с HA-репликацией или программой резервного копирования. **[Needs confirmation]**.

## F-15 — [Needs confirmation]: expansion only CSI и сокращённый StorageClass

- **p0363–p0364:** утверждается, что расширение PVC доступно «только» томам CSI; пример `storageclass-expandable.yaml` содержит placeholder `vendor-name.example/magicstorage` и явный пропуск полей.
- **Boundary:** это **не полный рабочий манифест** и не доказательство доступности/отсутствия expansion для всех драйверов в текущем кластере. Нужна проверка `allowVolumeExpansion`, PVC/storage backend и план расширения. Уменьшение тома и откат в RAG не описаны.

## F-16 — [Operational limitation]: удаление PVC и облачная стоимость

- **p0360–p0361:** в демонстрации динамического `standard` PVC с Delete удаляется вместе с PV; p0364 предупреждает о стоимости большого числа оставленных томов.
- **Boundary:** удаление объекта в Kubernetes не доказывает удаление billing resource у каждого провайдера и не гарантирует отсутствие остаточных данных. Финансовая, security и DR-проверка **[Needs confirmation]**.

**Не менялись:** исходный PDF/LFS, канонический RAG и статус чтения. Эти source findings не являются результатом текущей проверки Kubernetes API.
