# Упражнения главы 6

В проверенной границе найдены два явно обозначенных упражнения.

## Упражнение 1 — Service вместо port-forward

Источник: p0219:c01.

Для Pod fortune вместо kubectl port-forward предоставить доступ через Kubernetes Service и проверить HTTP access к Nginx container, который читает content из shared emptyDir.

## Упражнение 2 — Git synchronization sidecar

Источник: p0222:c01–p0223:c01.

Расширить Pod из gitRepo example:

1. добавить второй sidecar container;
2. использовать существующий image, способный синхронизировать local directory с Git repository;
3. смонтировать тот же shared volume в sidecar;
4. настроить sidecar так, чтобы изменения repository появлялись в volume;
5. проверить, что Nginx начинает обслуживать обновлённые файлы без recreation Pod.

Source допускает отложить упражнение до chapter 18, где эта техника разбирается пошагово.

## Provenance

- Exercise 1: p0219:c01
- Exercise 2: p0222:c01–p0223:c01
- Source SHA-256: 0d50f167ed86088d0cc65d15e27f1ab397e7c0a0c8de4db3801b50439f24266f
