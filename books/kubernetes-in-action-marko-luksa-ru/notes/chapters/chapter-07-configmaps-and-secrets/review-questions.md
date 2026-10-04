# Упражнения главы 7

В проверенной границе найдены две явно сформулированные практические задачи.

## Упражнение 1 — Pod с переопределёнными args

Источник: p0255:c01.

Создать Pod из manifest, где container args переопределяют default arguments image, и проверить, что указанные значения передаются главному process container.

## Упражнение 2 — Private image через imagePullSecrets

Источник: p0286:c01.

Самостоятельно проверить запуск Pod, использующего image из private registry:

1. создать docker-registry Secret;
2. указать его в spec.imagePullSecrets;
3. использовать private image;
4. проверить, что Kubernetes способен выполнить image pull и запустить Pod.

## Provenance

- Exercise 1: p0255:c01
- Exercise 2: p0286:c01
- Source SHA-256: 0d50f167ed86088d0cc65d15e27f1ab397e7c0a0c8de4db3801b50439f24266f
