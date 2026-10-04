# Упражнения главы 5

В проверенной границе найдены два явно обозначенных упражнения.

## Упражнение 1 — Session affinity ClientIP

Источник: p0174:c01.

Создать дополнительный Service с:

~~~text
sessionAffinity: ClientIP
~~~

и отправить к нему несколько запросов от одного и того же client IP, чтобы проверить, направляются ли они в один и тот же Pod.

## Упражнение 2 — Multi-port Pod и Service

Источник: p0175:c01.

Создать:
- Pod, предоставляющий два ports;
- один Service с двумя named ports;
- mappings 80 → 8080 и 443 → 8443.

Проверить принцип multi-port Service.

## Provenance

- Exercise 1: p0174:c01
- Exercise 2: p0175:c01
- Source SHA-256: 0d50f167ed86088d0cc65d15e27f1ab397e7c0a0c8de4db3801b50439f24266f
