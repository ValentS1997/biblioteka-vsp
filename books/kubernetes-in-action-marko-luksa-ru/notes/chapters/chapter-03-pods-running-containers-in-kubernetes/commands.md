# Команды главы 3

Все команды ниже поддержаны RAG главы 3. Environment-specific names нормализуются placeholders только там, где это не меняет смысл. Source-era behavior не модернизируется.

## Read-only: Pod/API inspection

### Полный Pod YAML

~~~bash
kubectl get po <pod-name> -o yaml
~~~

Source example использует существующий Pod и показывает `apiVersion`, `kind`, `metadata`, `spec`, `status`.

### Полный Pod JSON

~~~bash
kubectl get po <pod-name> -o json
~~~

Read-only.

### Pods

~~~bash
kubectl get pods
~~~

Read-only.

### API help

~~~bash
kubectl explain pods
kubectl explain pod.spec
~~~

Read-only. Используется для исследования поддерживаемых полей API object.

## Source-confirmed Pod manifest structure

RAG listing 3.2 содержит:

~~~text
apiVersion: v1
kind: Pod
metadata:
  name: kubia-manual
spec:
  containers:
  – image: luksa/kubia
    name: kubia
    ports:
    – containerPort: 8080
      protocol: TCP
~~~

Важно: list marker в RAG извлечён как типографское `–`, а не ASCII `-`. Здесь он сохранён как источник; manifest не объявляется copy-paste validated.

Source note: `containerPort` в этом разделе описан как информационное поле; отсутствие записи само по себе не блокирует сетевое подключение к реально слушающему порту.

## State-changing: create

### Create from YAML/JSON

~~~bash
kubectl create -f kubia-manual.yaml
~~~

State-changing: создаёт resource из файла.

Verification:

~~~bash
kubectl get pods
kubectl get po kubia-manual -o yaml
~~~

Rollback:

~~~bash
kubectl delete po kubia-manual
~~~

С оговоркой: если Pod управляется controller, controller может создать replacement.

## Logs

### Docker-side logs

~~~bash
docker logs <container-id>
~~~

Read-only, но требует доступа к node/container runtime.

### Kubernetes logs

~~~bash
kubectl logs kubia-manual
~~~

Read-only.

Для multi-container Pod:

~~~bash
kubectl logs kubia-manual -c kubia
~~~

Source limitation: logs доступны только пока container/Pod существует; для сохранения после удаления нужен centralized logging, рассматриваемый позже в книге.

## Port forwarding

### Forward local port to Pod

~~~bash
kubectl port-forward kubia-manual 8888:8080
~~~

Workload-generating local proxy; процесс остаётся активным.

Source output:

~~~text
Forwarding from 127.0.0.1:8888 -> 8080
Forwarding from [::1]:8888 -> 8080
~~~

### HTTP request

RAG source в `p0108:c01` извлечён буквально как:

~~~text
$ curl localhost: 8888
~~~

Пробел после двоеточия выглядит подозрительно, но под RAG-only policy не исправляется молча. Семантика surrounding text: request должен идти через local port 8888 к Pod port 8080.

## Labels: read-only

~~~bash
kubectl get po --show-labels
kubectl get po -L creation_method,env
~~~

Read-only.

## Labels: modify

### Add label

~~~bash
kubectl label po kubia-manual creation_method=manual
~~~

State-changing metadata update.

### Overwrite label

~~~bash
kubectl label po kubia-manual-v2 env=debug --overwrite
~~~

State-changing metadata update.

Verification:

~~~bash
kubectl get po -L creation_method,env
~~~

Label removal syntax: `[Needs confirmation]`.

## Label selectors

### Equality

~~~bash
kubectl get po -l creation_method=manual
~~~

### Presence

~~~bash
kubectl get po -l env
~~~

### Absence

~~~bash
kubectl get po -l '!env'
~~~

Source note: single quotes вокруг `!env` нужны, чтобы bash не интерпретировал `!`.

Также source перечисляет selector forms:

~~~text
creation_method!=manual
env in (prod,devel)
env notin (prod,devel)
app=pc,rel=beta
~~~

Последний пример показывает AND semantics для нескольких условий.

## Node labels / scheduling

### Label node

Source command с environment-specific node name:

~~~bash
kubectl label node <node-name> gpu=true
~~~

State-changing metadata update.

### Find matching nodes

~~~bash
kubectl get nodes -l gpu=true
kubectl get nodes -L gpu
~~~

Read-only.

### Pod nodeSelector

RAG listing 3.4 содержит ключевой fragment:

~~~text
spec:
  nodeSelector:
    gpu: "true"
~~~

Semantics: scheduler выбирает только nodes с matching label.

Source recommendation: не привязывать workload к отдельному node hostname без необходимости; описывать логические требования к node.

## Annotations

### Read annotations / object details

~~~bash
kubectl get po <pod-name> -o yaml
kubectl describe pod <pod-name>
~~~

Read-only.

### Add annotation

~~~bash
kubectl annotate pod kubia-manual mycompany.com/someannotation="foo bar"
~~~

State-changing metadata update.

Verification:

~~~bash
kubectl describe pod kubia-manual
~~~

Annotation selector отсутствует по модели главы.

Annotation removal: `[Needs confirmation]`.

## Namespaces: read-only

~~~bash
kubectl get ns
kubectl get po --namespace kube-system
~~~

`-n` source указывает как short form для `--namespace`.

## Namespace manifest

RAG listing 3.6:

~~~yaml
apiVersion: v1
kind: Namespace
metadata:
  name: custom-namespace
~~~

## Namespaces: create

~~~bash
kubectl create -f custom-namespace.yaml
~~~

или:

~~~bash
kubectl create namespace custom-namespace
~~~

State-changing.

Verification:

~~~bash
kubectl get ns
~~~

## Create resource in another namespace

~~~bash
kubectl create -f kubia-manual.yaml -n custom-namespace
~~~

State-changing.

Verification:

~~~bash
kubectl get po --namespace custom-namespace
~~~

Source также описывает возможность указать `namespace: custom-namespace` в `metadata`.

## Namespace context helper

Source приводит shell alias:

~~~bash
alias kcd='kubectl config set-context $(kubectl config currentcontext) --namespace '
~~~

и затем форму:

~~~text
kcd some-namespace
~~~

Это изменяет namespace текущего kubectl context. Точное поведение/современная совместимость не проверяются.

## Delete operations — destructive

### Delete Pod by name

~~~bash
kubectl delete po kubia-gpu
~~~

Destructive.

Source termination semantics:
1. Kubernetes sends SIGTERM.
2. Ждёт grace period, по умолчанию 30 seconds.
3. Если process не завершился — SIGKILL.

### Delete several named Pods

Source приводит общую форму:

~~~bash
kubectl delete po pod1 pod2
~~~

Destructive.

### Delete Pods by selector

~~~bash
kubectl delete po -l creation_method=manual
kubectl delete po -l rel=canary
~~~

Destructive/multi-resource.

### Delete namespace

~~~bash
kubectl delete ns custom-namespace
~~~

High impact: namespace-scoped resources удаляются вместе с namespace.

### Delete all Pods in current namespace

~~~bash
kubectl delete po --all
~~~

High impact.

Critical interpretation: если Pods создаются ReplicationController, удаление Pods не меняет controller desired state, поэтому replacements появляются снова.

### Delete almost all resources in current namespace

~~~bash
kubectl delete all --all
~~~

Very high impact.

Source output показывает удаление Pod, ReplicationController и Services.

Source caveats:
- keyword `all` не охватывает абсолютно все resource types;
- некоторые resources, например Secrets, сохраняются;
- в source example удаляется Service `kubernetes`, который затем должен автоматически воссоздаться.

Rollback для массового delete: `[Needs confirmation]`; explicit restore workflow глава не предоставляет.

## Safety boundary

Read-only commands отделены от state-changing/destructive operations.

Перед выполнением selector-based или `--all` deletion нужно сначала проверить target set соответствующим `kubectl get ... -l <selector>` или scoped `kubectl get`. Это operational safety framing данного артефакта; сама глава показывает selectors и delete semantics, но отдельный preflight workflow не формулирует.
