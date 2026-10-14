# Mermaid-схемы главы 5 (RAG-only)

**Source:** PDF 181–217; RAG p0181–p0217. Диаграммы являются концептуальным представлением извлечённого текста, не точными копиями иллюстраций PDF.

## Размещение и общий том

```mermaid
flowchart TD
  A["Pod на одном узле"] --> B["nginx-container"]
  A --> C["debian-container"]
  A --> D["Общая сеть: localhost"]
  A --> E["Общий том emptyDir"]
  B <-->|"Файлы / каталог"| E
  C <-->|"Файлы / каталог"| E
```

Книга: совместное размещение p0182–p0185, работа с файлами `emptyDir` p0201–p0203. После удаления Pod данные `emptyDir` теряются. `hostPath` — том, основанный на каталоге узла, с риском привязки Pod к узлу (p0204–p0206).

## Init, обычный Sidecar и Adapter

```mermaid
flowchart TD
  INIT["initContainers: последовательная подготовка"] -->|"После успеха"| APP["Основной контейнер приложения"]
  APP --> LOG["Общий том: файлы / журналы"]
  LOG --> SIDECAR["Sidecar: отправка логов"]
  LOG --> ADAPTER["Adapter: преобразование записей"]
  APP --> AMBASSADOR["Ambassador: исходящий прокси"]
  AMBASSADOR --> EXT["Внешняя БД / API"]
```

RAG: init p0194–p0197; Ambassador p0207–p0209; Sidecar p0209–p0212; Adapter p0212–p0215. Native sidecar отдельно представлен через `initContainers` с `restartPolicy: Always` на p0216, совместимость с фактическим кластером **[Needs confirmation]**.

## Учебная диагностика Pod

```mermaid
flowchart TD
  A["Применён YAML многоконтейнерного Pod"] --> B["kubectl get pods"]
  B --> C{"2/2 Ready?"}
  C -->|"Да"| D["kubectl logs -c / exec -c"]
  C -->|"Нет"| E["kubectl describe: Events"]
  E --> F{"ImagePullBackOff?"}
  F -->|"Да"| G["Проверить имя образа и доступность реестра"]
  F -->|"Не установлено"| H["Причина требует дополнительных данных"]
  G --> I["Контролируемое изменение YAML"]
  I --> B
```

RAG: p0184–p0187, p0190–p0198. Применение/удаление YAML — **state-changing**; диагностика через `get`, `describe`, `logs` — read-only. Для force-delete p0189 отдельно предупреждает об отсутствии гарантии реального завершения. Реальные показатели и rollback **[Needs confirmation]**.
