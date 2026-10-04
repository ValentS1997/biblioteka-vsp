# Упражнение главы 15

В проверенной границе найдено одно явно обозначенное упражнение: p0541:c01.

## Упражнение 1 — Изменить target CPU существующего HPA

Исходное состояние source example:

~~~text
HorizontalPodAutoscaler kubia
target CPU utilization: 30%
min replicas: 1
max replicas: 5
~~~

Задача:

1. открыть HPA kubia для редактирования;
2. изменить targetAverageUtilization с 30 на 60;
3. сохранить ресурс;
4. проверить новый target;
5. убедиться, что HPA controller продолжает управлять Deployment kubia с новым target.

Source command:

~~~bash
kubectl edit hpa kubia
~~~

Source field change:

~~~text
targetAverageUtilization: 30
→
targetAverageUtilization: 60
~~~

## Acceptance criteria

- HPA resource сохранён успешно;
- target CPU отображается как 60%;
- min/max replicas не изменены случайно;
- scaleTargetRef по-прежнему указывает на kubia;
- дальнейшие scaling decisions используют target 60%.

## Risk

Это изменение production scaling policy.

При более высоком target workload будет дольше работать с большей CPU utilization до scale-out.

Выполнять только в контролируемом lab либо после понимания capacity/headroom.

## Provenance

- Explicit exercise: p0541:c01
- Source SHA-256: 0d50f167ed86088d0cc65d15e27f1ab397e7c0a0c8de4db3801b50439f24266f
