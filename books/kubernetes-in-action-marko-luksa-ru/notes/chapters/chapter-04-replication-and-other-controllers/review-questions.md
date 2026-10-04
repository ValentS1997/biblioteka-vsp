# Упражнения главы 4

В проверенной границе найдены три явно обозначенных упражнения.

## Упражнение 1 — отказ worker node

Источник: `p0142:c01`–`p0143:c01`.

В GKE-кластере с несколькими nodes:

1. выбрать node, на котором работает хотя бы один managed Pod;
2. отключить network interface node;
3. наблюдать изменение статуса node и Pods;
4. проверить, создаёт ли ReplicationController replacement Pod;
5. вернуть node в рабочее состояние.

Source restriction: упражнение неприменимо к Minikube-сценарию главы, потому что там один node совмещает роли.

## Упражнение 2 — изменение selector ReplicationController

Источник: `p0146:c01`.

Вопрос по смыслу источника:

Что произойдёт, если изменить не labels Pod, а label selector самого ReplicationController так, чтобы текущие Pods перестали ему соответствовать?

## Упражнение 3 — изменение Pod template

Источник: `p0147:c01`.

1. выполнить `kubectl edit rc kubia`;
2. добавить новую label в metadata Pod template;
3. проверить labels уже существующих Pods;
4. удалить managed Pods и дождаться replacements;
5. сравнить labels replacement Pods с предыдущими.

## Provenance

- Exercise 1: `p0142:c01`–`p0143:c01`
- Exercise 2: `p0146:c01`
- Exercise 3: `p0147:c01`
- Source SHA-256: `0d50f167ed86088d0cc65d15e27f1ab397e7c0a0c8de4db3801b50439f24266f`
