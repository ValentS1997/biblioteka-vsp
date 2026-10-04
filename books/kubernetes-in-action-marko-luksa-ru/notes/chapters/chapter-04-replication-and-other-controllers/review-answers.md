# Ответы к упражнениям главы 4

Это RAG-grounded ответы по материалу главы, не официальный издательский answer key.

## Упражнение 1 — отказ worker node

### Risk

Упражнение намеренно нарушает network connectivity worker node.

Не выполнять на production или на единственном control/worker node.

### Source procedure

Выбрать node, на котором работает test Pod. Source указывает использовать wide Pod listing для определения placement.

Подключиться:

~~~bash
gcloud compute ssh <node-name>
~~~

На node отключить interface:

~~~bash
sudo ifconfig eth0 down
~~~

SSH перестанет отвечать.

Из отдельного terminal:

~~~bash
kubectl get node
~~~

Expected source observation: выбранный node становится `NotReady`.

После ожидания:

~~~bash
kubectl get pods
~~~

Expected:
- Pod на недоступном node переходит в `Unknown`;
- ReplicationController видит недостаток available/matching replicas;
- создаётся новый replacement Pod;
- снова существует требуемое число работающих replicas.

Recovery:

~~~bash
gcloud compute instances reset <node-name>
~~~

Acceptance:
- node после boot возвращается в `Ready`;
- source говорит, что старый `Unknown` Pod удаляется.

## Упражнение 2 — изменение RC selector

Ответ в самой главе дан явно.

Если selector ReplicationController изменить так, что текущие три Pods больше ему не соответствуют:

1. все текущие Pods выпадут из scope controller;
2. controller посчитает matching replica count равным нулю;
3. desired replicas остаётся 3;
4. controller создаст три новых Pods, которые соответствуют новому selector/template relation.

Старые Pods не уничтожаются только потому, что перестали соответствовать selector; они просто перестают контролироваться этим RC.

## Упражнение 3 — изменение Pod template

Открыть RC:

~~~bash
kubectl edit rc kubia
~~~

Добавить новую label в `spec.template.metadata.labels`.

После save:

- ReplicationController обновлён;
- existing Pods остаются без новой label;
- изменение template не мутирует уже созданные Pods.

Проверить labels существующих Pods:

~~~bash
kubectl get pods --show-labels
~~~

Затем удалить managed Pod по имени, используя source-supported delete form:

~~~bash
kubectl delete pod <pod-name>
~~~

Controller создаст replacement из нового template.

Проверить:

~~~bash
kubectl get pods --show-labels
~~~

Acceptance: replacement Pod содержит новую template label, а первоначальные Pods до их замены её не имели.

## Provenance

- Node failure procedure/result: `p0142:c01`–`p0143:c01`
- Selector thought exercise/result: `p0146:c01`
- Template edit exercise/result: `p0147:c01`
