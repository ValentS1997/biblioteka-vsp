# Ответ к упражнению главы 15

Это RAG-grounded walkthrough, не официальный издательский answer key.

## 1. Открыть HPA

~~~bash
kubectl edit hpa kubia
~~~

STATE-CHANGING scaling-policy edit.

## 2. Изменить target

В source fragment:

~~~text
spec:
  maxReplicas: 5
  metrics:
  - resource:
      name: cpu
      targetAverageUtilization: 60
    type: Resource
~~~

Нужно изменить только target CPU:

~~~text
30 → 60
~~~

Не менять случайно:
- maxReplicas;
- minReplicas;
- scaleTargetRef;
- metric resource name.

## 3. Проверить результат

Read-only:

~~~bash
kubectl get hpa
kubectl describe hpa
~~~

Expected:
- target показывает 60%;
- HPA продолжает ссылаться на Deployment kubia;
- controller events появляются при последующих rescale operations.

## 4. Интерпретация

CPU utilization source определяется относительно CPU request.

При target 60% HPA допускает более высокую среднюю CPU utilization до необходимости scale-out, чем при target 30%.

Следовательно, при одинаковой нагрузке desired replica count в общем случае может быть ниже, чем при target 30%.

## 5. Rollback

Source-supported rollback по смыслу exercise:
снова отредактировать тот же HPA и вернуть targetAverageUtilization к 30.

~~~bash
kubectl edit hpa kubia
~~~

После возврата проверить:

~~~bash
kubectl get hpa
kubectl describe hpa
~~~

## Acceptance

- target 60% подтверждён;
- HPA не удалён;
- Deployment remains scaling target;
- min/max bounds сохранены;
- rollback path понятен.

## Provenance

- p0541:c01
