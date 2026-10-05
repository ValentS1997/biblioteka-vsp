# Ответы к контрольным материалам — глава 5

## Контрольный тест: ключ из источника

| № | Ответ |
|---:|:---:|
| 1 | C |
| 2 | D |
| 3 | B |
| 4 | C |
| 5 | C |
| 6 | A |
| 7 | A |
| 8 | C |

Ключ `1-C, 2-D, 3-B, 4-C, 5-C, 6-A, 7-A, 8-C` прямо приведён в `p0112:c01`.

## Ответы на открытые вопросы

### 1. Что такое Docker Swarm?

В формулировке главы Docker Swarm — встроенный в Docker механизм кластеризации/orchestration, позволяющий управлять несколькими Docker Engine hosts и container workloads как единым cluster.

### 2. Что такое service? Чем service отличается от task/replica?

Service описывает desired state: image, command, network, ports, resources, mode/replica count. Manager scheduler создаёт tasks, чтобы реализовать это состояние. Task — конкретная единица выполнения service, сопоставленная с container. В практических примерах глава также использует термин replica для task instance.

### 3. Что такое routing mesh и как она работает?

Routing mesh — встроенный механизм Swarm для распределения входящих requests к tasks service. Клиенту не нужно знать, на каком именно node выполняется выбранная task: request маршрутизируется внутри cluster к подходящему worker/task.

### 4. Как lock/unlock Docker Swarm?

Source sequence:

```bash
docker swarm update --autolock=true
systemctl restart docker
docker swarm unlock
```

После enable autolock Docker выдаёт unlock key. Его нужно хранить безопасно. После restart manager требует этот key для unlock.

### 5. Что такое consensus?

Consensus — согласование cluster state между managers. Источник указывает Raft, рекомендует нечётное число managers и объясняет quorum. При потере majority существующие tasks могут продолжать работу, но scheduler не может надёжно менять cluster state/reconcile failures.

### 6. Replicated vs global mode

Replicated service имеет заданное пользователем количество replicas, которые scheduler распределяет по nodes.

Global service имеет одну task на каждом eligible node. Когда новый node добавляется, global task появляется на нём автоматически.

### 7. Что такое overlay networks в Swarm?

Overlay network связывает service tasks across multiple hosts. Swarm автоматически создаёт `ingress`; можно создать custom overlay network. Source также описывает `docker_gwbridge` для external connectivity и перечисляет ports 2377/TCP, 7946/TCP+UDP и 4789/UDP для cluster/overlay communications.

### 8. Как публиковать custom ports/protocols?

Короткая форма source:

```bash
docker service create --name myserv_ingress -p 8081:80 nginx
```

Полная форма:

```bash
docker service create --name myservice_ingress --publish published=8080,target=80 nginx
```

Для protocol source показывает параметры `protocol=udp` и `protocol=tcp` в publish specification.

## Operational map

```text
cluster
├─ managers → leader / consensus / scheduling
└─ workers → tasks

service desired state
      ↓
scheduler
      ↓
replicas/tasks
      ↓
reconcile on failure / scale / drain
```

## Provenance

Ответы сформированы только по chapter RAG `p0088:c01`–`p0113:c01` (+ `p0096:c02`). External sources и model-memory не использовались.
