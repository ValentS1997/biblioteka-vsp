# Шпаргалка: первый end-to-end workflow Docker → Kubernetes

Цель: пройти путь от локального приложения до доступного и масштабируемого workload, используя только операции, явно поддержанные главой 2.

## Symptom / problem framing

Практическая задача главы:

- упаковать приложение так, чтобы его можно было запускать одинаково на разных машинах;
- сделать image доступным рабочим узлам;
- получить работающий Kubernetes cluster;
- развернуть приложение без ручного выбора узла;
- открыть приложение для клиентов;
- масштабировать количество экземпляров;
- проверить, где работают Pod и как Service распределяет запросы.

## Baseline / context

~~~text
Node.js source
    ↓ Dockerfile
Docker image
    ↓ tag / push
Image registry
    ↓ image reference
kubectl → Kubernetes API
    ↓
ReplicationController
    ↓ desired replicas
Pods
    ↓
Service
    ↓
Clients
~~~

В source-era workflow главы `kubectl run` создаёт ReplicationController, а не Deployment.

## Read-only checks

| Что проверить | Команда из главы | Ожидаемое наблюдение |
|---|---|---|
| Локальные Docker images | `docker images` | image присутствует локально |
| Запущенные containers | `docker ps` | `kubia-container` запущен |
| Детали container | `docker inspect kubia-container` | JSON с low-level данными |
| Процессы внутри container | `ps aux` после `docker exec` | application process виден внутри |
| Процесс на host | `ps aux \| grep app.js` | тот же application process виден с host PID |
| Cluster endpoint | `kubectl cluster-info` | API cluster доступен |
| Nodes | `kubectl get nodes` | nodes в состоянии Ready в примере |
| Node details | `kubectl describe node <node-name>` | подробные сведения об узле |
| Pods | `kubectl get pods` | Pod переходит к Running |
| Pod placement | `kubectl get pods -o wide` | колонка NODE показывает назначение |
| Pod details | `kubectl describe pod <pod-name>` | node и другие детали Pod |
| Services | `kubectl get services` / `kubectl get svc` | Service и адреса |
| ReplicationControllers | `kubectl get replicationcontrollers` / `kubectl get rc` | DESIRED/CURRENT/READY |
| HTTP response | `curl <external-ip>:8080` | ответ приложения содержит hostname/Pod identity |

## Interpretation

### Image работает локально, но Pod завис в ожидании

Глава предлагает проверить доступность image для worker nodes. Для собственного image он должен быть доступен в registry; как troubleshooting step предлагается вручную проверить `docker pull` на другой машине.

### Container работает, но нужно увидеть его фактическое окружение

Использовать:

~~~text
docker exec -it kubia-container bash
ps aux
ls /
~~~

Это показывает процессы и файловую систему с точки зрения container.

### Cluster доступен, но неизвестно, где выполняется Pod

Использовать `kubectl get pods -o wide` или `kubectl describe pod <pod-name>`.

### Service существует, но внешний адрес ещё не готов

Повторно проверить `kubectl get svc`. В примере GKE внешний IP сначала может находиться в состоянии pending. Для Minikube глава отдельно указывает, что LoadBalancer не получает внешний IP, и предлагает `minikube service kubia-http`.

### После scaling запросы попадают в разные Pod

Это ожидаемое поведение главы: Service распределяет запросы между несколькими Pod, управляемыми одним ReplicationController.

## Next action

~~~text
1. build image
2. run locally
3. verify HTTP
4. inspect container if needed
5. tag + login + push
6. verify cluster
7. kubectl run
8. verify Pod
9. expose Service
10. verify service access
11. scale replicas
12. verify RC + Pods + repeated HTTP requests
~~~

## Modifying action

### Docker build

`docker build -t kubia .`

Effect: создаёт локальный image.

Risk: использует содержимое build directory и может получить base image из registry.

Verification: `docker images`.

Rollback: `[Needs confirmation]` — удаление image в главе не показано.

### Docker run

`docker run --name kubia-container -p 8080:8080 -d kubia`

Effect: запускает container и публикует порт.

Verification: `docker ps`, затем `curl localhost:8080`.

Rollback, поддержанный главой:

~~~text
docker stop kubia-container
docker rm kubia-container
~~~

### Docker push

`docker push <dockerhub-id>/kubia`

Effect: публикует image в удалённом registry.

Prerequisite: `docker login`.

Verification: запуск опубликованного image на другой машине описан в главе.

Rollback: `[Needs confirmation]`.

### Start local Kubernetes

`minikube start`

Effect: запускает локальный одноузловой cluster через VM.

Verification: `kubectl cluster-info`.

Rollback: `[Needs confirmation]`.

### Create GKE cluster

`gcloud container clusters create kubia --num-nodes 3 --machine-type f1-micro`

Effect: создаёт многоузловой managed cluster в примере главы.

Verification: `kubectl get nodes`.

Rollback: `[Needs confirmation]`.

### Run application in Kubernetes

`kubectl run kubia --image=<dockerhub-id>/kubia --port=8080 --generator=run/v1`

Effect: в source-era workflow создаёт ReplicationController, который приводит к запуску Pod.

Verification: `kubectl get pods`, `kubectl get rc`.

Rollback: `[Needs confirmation]`.

### Expose application

`kubectl expose rc kubia --type=LoadBalancer --name kubia-http`

Effect: создаёт Service для ReplicationController.

Verification: `kubectl get svc`, затем HTTP request к external IP.

Rollback: `[Needs confirmation]`.

### Scale

`kubectl scale rc kubia --replicas=<count>`

Effect: изменяет desired replica count.

Verification: `kubectl get rc` и `kubectl get pods`.

Rollback: вернуть pre-change replica count той же командой.

## Verification / acceptance checks

Workflow главы подтверждён, если:

- image виден в `docker images`;
- локальный container отвечает по опубликованному порту;
- image опубликован в registry и может быть запущен на другой машине;
- `kubectl cluster-info` отвечает;
- nodes доступны;
- Pod переходит к Running;
- Service получает доступный endpoint в поддерживаемой среде;
- HTTP запрос достигает приложения;
- после scaling DESIRED/CURRENT отражают новое число replicas;
- несколько HTTP-запросов могут попадать в разные Pod.

## Rollback

Поддержано источником:

- container: `docker stop` → `docker rm`;
- replica count: повторный `kubectl scale rc ... --replicas=<previous-count>`.

Не поддержано явными командами в главе:

- удаление Docker image;
- удаление remote image;
- остановка/удаление Minikube cluster;
- удаление GKE cluster;
- удаление ReplicationController;
- удаление Service.

Для этих действий: `[Needs confirmation]`.
