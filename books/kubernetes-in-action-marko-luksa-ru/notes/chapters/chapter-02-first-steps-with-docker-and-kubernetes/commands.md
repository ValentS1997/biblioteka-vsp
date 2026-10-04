# Команды главы 2

Все команды ниже происходят из RAG главы 2. Environment-specific идентификаторы нормализованы в placeholders. Команды установки и cluster creation отражают контекст издания и не проверялись на актуальность.

## Docker: read-only / inspection

### Список локальных images

~~~bash
docker images
~~~

Read-only. Используется после build.

### Список запущенных containers

~~~bash
docker ps
~~~

Read-only.

Для запущенных и остановленных containers глава также явно указывает:

~~~bash
docker ps -a
~~~

Read-only.

### Детали container

~~~bash
docker inspect kubia-container
~~~

Read-only. Возвращает low-level JSON.

### Процессы внутри container

После входа в container:

~~~bash
ps aux
~~~

Read-only.

### Процесс container с точки зрения host

~~~bash
ps aux | grep app.js
~~~

Read-only.

### Файловая система внутри container

~~~bash
ls /
~~~

Read-only.

## Docker: workload-generating / state-changing

### Запуск готового BusyBox

~~~bash
docker run busybox echo "Hello world"
~~~

Workload-generating. Если image отсутствует локально, Docker получает его из registry, затем запускает container.

### Общая форма запуска image

~~~bash
docker run <image>
docker run <image>:<tag>
~~~

Workload-generating.

### Dockerfile из главы

~~~dockerfile
FROM node:7
ADD app.js /app.js
ENTRYPOINT ["node", "app.js"]
~~~

Source-confirmed build definition.

### Build image

~~~bash
docker build -t kubia .
~~~

State-changing: создаёт локальный image `kubia`.

Verification:

~~~bash
docker images
~~~

Rollback: `[Needs confirmation]`.

### Запуск приложения с port mapping

~~~bash
docker run --name kubia-container -p 8080:8080 -d kubia
~~~

Workload-generating/state-changing: создаёт и запускает container, host port 8080 сопоставляется с container port 8080.

Verification:

~~~bash
docker ps
curl localhost:8080
~~~

Rollback:

~~~bash
docker stop kubia-container
docker rm kubia-container
~~~

### Вход в работающий container

~~~bash
docker exec -it kubia-container bash
~~~

Workload-generating: запускает дополнительный `bash` process в namespaces container.

Source explanation:
- `-i` держит STDIN открытым;
- `-t` выделяет pseudo-TTY.

Выход:

~~~bash
exit
~~~

### Остановка container

~~~bash
docker stop kubia-container
~~~

State-changing. Останавливает главный process container.

Verification:

~~~bash
docker ps -a
~~~

### Удаление container

~~~bash
docker rm kubia-container
~~~

State-changing/destructive для container: его содержимое удаляется, и этот container нельзя запустить снова.

Rollback: `[Needs confirmation]`.

### Дополнительный tag для image

Source example нормализован:

~~~bash
docker tag kubia <dockerhub-id>/kubia
~~~

State-changing: добавляет дополнительный tag к тому же image.

Verification:

~~~bash
docker images | head
~~~

### Authentication to Docker Hub

~~~bash
docker login
~~~

Authentication state change. Глава требует login перед push.

Security: credentials не должны помещаться в артефакты или командную историю сверх поведения самого клиента.

### Push image

~~~bash
docker push <dockerhub-id>/kubia
~~~

State-changing remote action.

Rollback remote image: `[Needs confirmation]`.

### Запуск опубликованного image на другой машине

~~~bash
docker run -p 8080:8080 -d <dockerhub-id>/kubia
~~~

Workload-generating.

### Troubleshooting image pull

Глава явно предлагает проверить, что image может быть получен на другой машине:

~~~bash
docker pull <image>
~~~

State-changing cache/download operation; используется как проверка registry accessibility.

## Minikube

### Source-specific install example for macOS

~~~bash
curl -Lo minikube https://storage.googleapis.com/minikube/releases/v0.23.0/minikube-darwin-amd64 && chmod +x minikube && sudo mv minikube /usr/local/bin/
~~~

State-changing host installation.

Risk: скачивание binary + изменение executable bit + privileged move.

Verification: `[Needs confirmation]` — глава сразу переходит к запуску.

Rollback: `[Needs confirmation]`.

### Start cluster

~~~bash
minikube start
~~~

State-changing: запускает локальный одноузловой cluster в VM.

Verification:

~~~bash
kubectl cluster-info
~~~

Rollback: `[Needs confirmation]`.

### SSH в Minikube VM

~~~bash
minikube ssh
~~~

Interactive/read-only intent in главе: исследовать процессы внутри VM. Сам shell позволяет изменения; соблюдать read-only discipline.

### Получить адрес Service в Minikube

~~~bash
minikube service kubia-http
~~~

Source-described access helper для Minikube, где LoadBalancer Service не получает внешний IP.

### Dashboard

~~~bash
minikube dashboard
~~~

Открывает Kubernetes Dashboard в браузере.

## kubectl installation / shell setup

### Source-specific install example for macOS

~~~bash
curl -LO https://storage.googleapis.com/kubernetes-release/release/$(curl -s https://storage.googleapis.com/kubernetes-release/release/stable.txt)/bin/darwin/amd64/kubectl && chmod +x kubectl && sudo mv kubectl /usr/local/bin/
~~~

State-changing host installation. Для Linux/Windows source указывает менять `darwin` в URL.

Rollback: `[Needs confirmation]`.

### Alias

~~~bash
alias k=kubectl
~~~

Session/shell state change. Для постоянного использования source предлагает добавить в shell startup file.

### Bash completion

~~~bash
source <(kubectl completion bash)
~~~

Изменяет текущую shell session.

Для alias `k` source приводит:

~~~bash
source <(kubectl completion bash | sed s/kubectl/k/g)
~~~

## Cluster: read-only checks

### Cluster info

~~~bash
kubectl cluster-info
~~~

Read-only.

### Nodes

~~~bash
kubectl get nodes
~~~

Read-only.

### Node details

~~~bash
kubectl describe node <node-name>
~~~

Read-only.

Source также указывает, что без имени node команда может вывести detailed descriptions всех nodes:

~~~bash
kubectl describe node
~~~

### Pods

~~~bash
kubectl get pods
~~~

Read-only.

### Pods with node placement

~~~bash
kubectl get pods -o wide
~~~

Read-only.

### Pod details

~~~bash
kubectl describe pod <pod-name>
~~~

Read-only.

### Services

~~~bash
kubectl get services
kubectl get svc
~~~

Read-only.

### ReplicationControllers

~~~bash
kubectl get replicationcontrollers
kubectl get rc
~~~

Read-only.

### Общий get

Source описывает:

~~~bash
kubectl get
~~~

как способ получить список возможных object types в контексте версии книги.

### Dashboard URL in GKE

~~~bash
kubectl cluster-info | grep dashboard
~~~

Read-only.

## Google Kubernetes Engine / gcloud

### Install kubectl component through gcloud

~~~bash
gcloud components install kubectl
~~~

State-changing local installation.

Rollback: `[Needs confirmation]`.

### Create managed cluster

~~~bash
gcloud container clusters create kubia --num-nodes 3 --machine-type f1-micro
~~~

State-changing remote infrastructure action.

Effect: создаёт cluster `kubia` с тремя nodes в примере главы.

Verification:

~~~bash
kubectl get nodes
~~~

Rollback: `[Needs confirmation]` — delete command в главе не приведена.

### SSH to worker node

~~~bash
gcloud compute ssh <node-name>
~~~

Interactive access. Source uses it for inspection; shell itself permits modifications.

### Credential-exposing cluster description

Source приводит команду:

~~~bash
gcloud container clusters describe kubia | grep -E "(username|password):"
~~~

Read-only, но security-sensitive: она выводит cluster credentials в source-era example.

В этом артефакте реальные значения намеренно не воспроизводятся:

~~~text
username: <redacted>
password: <redacted>
~~~

Не использовать вывод в shared logs.

## Kubernetes workload: state-changing

### Run first application

Source command normalized only by replacing Docker Hub ID:

~~~bash
kubectl run kubia --image=<dockerhub-id>/kubia --port=8080 --generator=run/v1
~~~

State-changing.

Source-era effect: создаёт ReplicationController `kubia`, который приводит к созданию Pod.

Verification:

~~~bash
kubectl get pods
kubectl get rc
~~~

Rollback: `[Needs confirmation]`.

### Expose ReplicationController

~~~bash
kubectl expose rc kubia --type=LoadBalancer --name kubia-http
~~~

State-changing: создаёт Service `kubia-http`.

Verification:

~~~bash
kubectl get svc
curl <external-ip>:8080
~~~

Rollback: `[Needs confirmation]`.

### Scale application

~~~bash
kubectl scale rc kubia --replicas=3
~~~

State-changing: меняет desired replica count.

Verification:

~~~bash
kubectl get rc
kubectl get pods
~~~

Rollback: выполнить `kubectl scale rc kubia --replicas=<previous-count>`.

## HTTP verification / workload generation

### Local container

~~~bash
curl localhost:8080
~~~

Workload-generating HTTP request.

### Kubernetes Service

~~~bash
curl <external-ip>:8080
~~~

Workload-generating HTTP request.

Повторные вызовы в главе показывают ответы от разных Pod после scaling.

## Source-era boundary

Не добавлены из памяти:

- команды удаления ReplicationController/Service;
- команды удаления GKE cluster;
- команды остановки/удаления Minikube cluster;
- команды удаления local/remote image;
- современные замены source-era `kubectl run --generator=run/v1`.

Для них: `[Needs confirmation]`.
