# Диаграммы главы 10 — репликация, failover и liveness

**Source:** PDF 366–383, RAG p0366:c01–p0383:c01. Схемы концептуальные, построены по тексту, не являются точной реконструкцией оригинальных рисунков.

## Контур согласования ReplicaSet

```mermaid
flowchart TD
  API["ReplicaSet: replicas=4, selector, template"]
  OBS["Наблюдаемые Pod с совпадающими метками"]
  DEC{"Количество совпадает с desired?"}
  CREATE["ReplicaSet создаёт Pod из template"]
  DELETE["ReplicaSet удаляет лишний Pod"]
  KEEP["Остаётся четыре управляемых Pod"]
  API --> DEC
  OBS --> DEC
  DEC -->|"Меньше четырёх"| CREATE --> OBS
  DEC -->|"Больше четырёх"| DELETE --> OBS
  DEC -->|"Да"| KEEP
```

RAG p0370, p0372–p0376. Bare Pod с подходящими `metadata.labels` может быть захвачен и удалён. Отсутствие пересечений селекторов и текущий namespace [Needs confirmation].

## Доступность приложения и восстановление узла

```mermaid
flowchart TD
  USER["Клиент"]
  SERVICE["Service nginx-service: порт 80"]
  P1["Pod на worker-1"]
  P2["Pod на worker-2"]
  P3["Pod на worker-3"]
  FAIL["Cordon / drain / delete worker-1: разрушительный тест"]
  RS["ReplicaSet: desired count"]
  USER --> SERVICE
  SERVICE --> P1
  SERVICE --> P2
  SERVICE --> P3
  FAIL --> P1
  FAIL --> RS
  RS -->|"Новые Pod на доступных узлах"| P2
  RS -->|"Новые Pod на доступных узлах"| P3
```

RAG p0377–p0378. В конкретном примере четыре реплики продолжают выполняться на двух узлах после отвода одного. **Не** доказывает отсутствие простоя, независимость от сети, storage или control plane. Выполнение действий только с разрешением в disposable кластере.

## ReplicaSet vs kubelet: разные циклы восстановления

```mermaid
flowchart TD
  A["Pod управляется ReplicaSet"]
  B{"Pod отсутствует?"}
  C["ReplicaSet создаёт замену Pod"]
  D["Существующий Pod: livenessProbe GET /"]
  E{"Liveness неуспешна?"}
  F["kubelet перезапускает контейнер"]
  G["Контейнер продолжает работу"]
  A --> B
  B -->|"Да"| C
  B -->|"Нет"| D --> E
  E -->|"Да"| F --> D
  E -->|"Нет"| G
```

RAG p0375, p0380–p0381. Source имитирует неуспешный HTTP 403 удалением HTML-файла; recovery файла/сервиса [Needs confirmation].

## Safety and rollback

Удаление ReplicaSet по умолчанию каскадно удаляет Pod; `--cascade=orphan` оставляет их, но не предотвращает последующее adoption другими контроллерами (p0382). Вывод worker из кластера и `exec rm` — не read-only процедуры. Практический откат и влияние на реальных пользователей [Needs confirmation].
