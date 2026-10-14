# Глава 7 — Mermaid diagrams (RAG-only)

**Source:** PDF 248–280; текстовые чанки p0248–p0280. Концептуальные схемы реконструированы по тексту RAG, не по оригинальным иллюстрациям книги.

## Один образ, разные конфигурации

```mermaid
flowchart TD
  IMG["Один образ приложения"]
  DEV["Pod в dev"]
  PROD["Pod в prod"]
  CMDEV["ConfigMap dev: не-чувствительные данные"]
  CMPROD["ConfigMap prod: не-чувствительные данные"]
  SECDEV["Secret dev: чувствительные значения"]
  SECPROD["Secret prod: чувствительные значения"]
  IMG --> DEV
  IMG --> PROD
  CMDEV --> DEV
  CMPROD --> PROD
  SECDEV --> DEV
  SECPROD --> PROD
```

Основание: переносимость контейнера, разделение приложения и конфигурации, p0249–p0252.

## Два способа получения значений

```mermaid
flowchart TD
  SOURCE["ConfigMap / Secret"]
  ENV["env: KeyRef для одного ключа"]
  ALL["envFrom: весь набор ключей"]
  VOL["volumes: configMap или secret"]
  CONTAINER["Контейнер в Pod"]
  MOUNT["volumeMounts: каталог и файлы"]
  SOURCE --> ENV --> CONTAINER
  SOURCE --> ALL --> CONTAINER
  SOURCE --> VOL --> MOUNT --> CONTAINER
```

Основание: p0252–p0253, p0262–p0265, p0275–p0278. Вариант `env` с реальным Secret может раскрывать значение в окружении процесса. В книге для чувствительных данных предпочтён том (p0253); p0275 также показывает env, что не равнозначно security-одобрению.

## Диагностика ошибочной зависимости

```mermaid
flowchart TD
  A["Создание Pod из YAML"]
  B["kubectl get pod"]
  C{"Pod Running?"}
  D["Проверить kubectl describe pod"]
  E{"FailedMount / configmap not found?"}
  F["Проверить существование источника и namespace"]
  G["Контролируемо восстановить зависимость"]
  H["Состояние нужно исследовать дополнительно"]
  A --> B --> C
  C -->|"Нет"| D --> E
  E -->|"Да"| F --> G --> B
  E -->|"Нет"| H
```

Книга p0266–p0267 показывает `my-sixth-configmap` удалённым и `FailedMount` для Pod, ожидающего его том. Подстановка/возврат исходного содержимого Secret/ConfigMap в реальной среде **[Needs confirmation]**. Команды `kubectl delete` — деструктивны для конфигурационной зависимости. Пример `kubectl get secret -o yaml` может раскрыть Base64, а `exec -- env` — plaintext; не печатать реальные значения.
