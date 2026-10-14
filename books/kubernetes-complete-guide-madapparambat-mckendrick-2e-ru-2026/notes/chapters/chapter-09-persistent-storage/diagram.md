# Диаграммы главы 9 — постоянное хранилище

**Source:** RAG PDF 326–365, `p0326:c01`–`p0365:c01`. Mermaid-схемы реконструированы из текста, не являются точной копией иллюстраций PDF.

## Статическое выделение тома

```mermaid
flowchart TD
  ADMIN["Администратор: подготовить backend"]
  PV["PersistentVolume: cluster-scoped"]
  DEV["Разработчик: потребность приложения"]
  PVC["PersistentVolumeClaim: namespace-scoped"]
  POD["Pod: тот же namespace, что PVC"]
  STORE["Внешнее или узловое хранилище"]
  ADMIN --> STORE
  ADMIN --> PV
  PV <-->|"Matching: capacity, modes, class, selector"| PVC
  DEV --> PVC
  DEV --> POD
  POD -->|"volumes.persistentVolumeClaim"| PVC
  PV --> STORE
```

p0341–p0347: PV определён администратором, PVC заявлен разработчиком, Pod подключает **имя PVC**, а не PV. Статический пример hostPath ограничен узлом.

## Динамическое выделение PV

```mermaid
flowchart TD
  PVC["Создан PVC со storageClassName"]
  SC["StorageClass: provisioner / reclaim"]
  CSI["CSI / provisioner"]
  STORAGE["Система хранения: выделить том"]
  PV["Автоматически создан PV"]
  POD["Pod: volumeMount + claimName"]
  PVC --> SC --> CSI --> STORAGE
  CSI --> PV
  PV -->|"Bound"| PVC
  PVC --> POD
```

p0352–p0360: minikube `standard` — *только учебный пример*. Для clone/snapshot/expansion нужна поддержка драйвера и других объектов; не считать универсальной.

## Проверка состояния без разрушительных действий

```mermaid
flowchart TD
  A["kubectl get sc / pv / pvc"]
  B{"PVC Bound?"}
  C["Сверить capacity, class, modes, selector"]
  D["kubectl get pvc,pod -n namespace"]
  E{"Pod Running?"}
  F["Проверить конфигурацию PVC / Pod mount"]
  G["Контролируемое изменение только с backup"]
  A --> B
  B -->|"Нет"| C --> G --> A
  B -->|"Да"| D --> E
  E -->|"Нет"| F --> G
  E -->|"Да"| H["В источнике дополнительно не доказана сохранность данных"]
```

Предметная причина Pending, события и команда диагностики при конкретной ошибке в RAG **[Needs confirmation]**. Следует избегать придуманных CLI steps, которых нет в главе.

## Lifecycle / reclaim risk

```mermaid
flowchart TD
  PV["PV Available"] --> BOUND["PV Bound к PVC"]
  BOUND -->|"Удалён PVC"| RELEASED["PV Released при Retain"]
  BOUND -->|"Удалён PVC"| DELETE["Delete: возможное удаление тома"]
  RELEASED -->|"patch policy Delete; учебный пример"| DELETE
  RELEASED --> REVIEW["Отдельный ручной план сохранения/возврата данных"]
```

p0349–p0351, p0360–p0361. **Не выполнять** patch/delete на ресурсах с нужными данными. Возможность восстановить байты из RAG не следует: backup/restore [Needs confirmation].
