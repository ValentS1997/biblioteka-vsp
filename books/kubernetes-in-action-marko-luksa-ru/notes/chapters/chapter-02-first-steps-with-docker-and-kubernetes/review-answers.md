# Решение упражнения главы 2

Это RAG-grounded решение упражнения из главы; не официальный издательский answer key.

## Ненумерованное упражнение — решение

Исходное состояние в тексте: ReplicationController `kubia` имеет три реплики.

### 1. Увеличить replica count

Глава уже показала синтаксис:

~~~bash
kubectl scale rc kubia --replicas=<higher-count>
~~~

Где `<higher-count>` — значение больше 3.

Точное значение упражнение не задаёт.

### 2. Проверить состояние ReplicationController

~~~bash
kubectl get rc
~~~

Ожидаемое по модели главы: DESIRED отражает новое число реплик, а CURRENT/READY сходятся к нему по мере создания Pod.

### 3. Проверить дополнительные Pod

~~~bash
kubectl get pods
~~~

При необходимости увидеть placement:

~~~bash
kubectl get pods -o wide
~~~

### 4. Проверить Service

Если Service `kubia-http` уже создан и имеет доступный адрес:

~~~bash
curl <external-ip>:8080
~~~

Повторные запросы могут возвращать разные container/Pod hostnames, поскольку Service распределяет запросы между Pod.

### 5. Масштабировать обратно

Поскольку перед упражнением было три реплики:

~~~bash
kubectl scale rc kubia --replicas=3
~~~

### 6. Acceptance check

~~~bash
kubectl get rc
kubectl get pods
~~~

Результат считается соответствующим упражнению, когда desired replica count снова равен 3 и количество работающих Pod возвращается к исходному состоянию.

## Ограничения

- Упражнение не задаёт конкретное максимальное число реплик.
- Время convergence не задано.
- Cleanup Service/ReplicationController в этой главе не приведён.

## Provenance

- Exercise: `p0090:c01`
- Scaling command: глава 2, раздел 2.3.4
- Verification commands: разделы 2.3.1, 2.3.4 и 2.3.5
- Source SHA-256: `0d50f167ed86088d0cc65d15e27f1ab397e7c0a0c8de4db3801b50439f24266f`
