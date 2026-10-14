# Commands — глава 4 (только RAG, PDF 143–180)

Ни одна из команд не выполнялась. `nginx-pod`, `hello-world-job` и `hello-world-cronjob` — демонстрационные имена книги. Перед любым изменением кластерного ресурса проверить контекст, namespace, права и наличие объекта: **[Needs confirmation]**.

## Read-only / observation

| Команда | Назначение | RAG |
|---|---|---|
| `kubectl api-resources` | типы и сокращенные имена | p0151 |
| `kubectl get pods` / `kubectl get po -w` | Pod и динамика | p0151 |
| `kubectl describe pod nginx-pod` | Conditions, Events и детали | p0154 |
| `kubectl get pods --output=yaml` | вывести YAML | p0155 |
| `kubectl get pods --output=json` | вывести JSON | p0155 |
| `kubectl get pods <ИМЯ_ПОДА> -o yaml` | YAML одного объекта; placeholder | p0155 |
| `kubectl get pods <ИМЯ_ПОДА> -o json` | JSON одного объекта; placeholder | p0155 |
| `kubectl get pods -o wide` | IP, назначенный узел | p0156 |
| `kubectl get pods --selector "environment=production"` | выборка по метке | p0159 |
| `kubectl get pods -l "environment=production"` | короткая форма выборки | p0160 |
| `kubectl get pod -l environment=prod` | другая исходная выборка | p0162 |
| `kubectl get pods --show-labels` | отображение меток | p0162 |
| `kubectl get pods nginx-pod --show-labels` | метки одного Pod | p0163 |
| `kubectl get pod nginx-pod -o json \| jq '.metadata.annotations'` | извлечение аннотаций; требуется jq | p0165 |
| `kubectl get jobs` / `kubectl get jobs -w` | задания и watch | p0167, p0170 |
| `kubectl logs jobs/hello-world-job` | логи Job | p0168 |
| `kubectl logs pods/hello-world-job-2qh4d` | логи образцового Pod | p0168 |
| `kubectl get pods --watch` / `kubectl get pods -w` | наблюдение за Pod | p0170–p0171 |
| `kubectl get cronjobs` | CronJob и расписание | p0178 |
| `podman manifest inspect nginx:latest` | сведения об образе, а не Kubernetes | p0152 |
| `diff nginx-pod.yaml nginx-pod-output.yaml` | сравнение файлов | p0155 |

Read-only запрос может выводить чувствительные сведения из метаданных, образов и логов; публиковать после проверки.

## State-changing local: экспорт

```bash
kubectl get pods/nginx-pod -o yaml > nginx-pod-output.yaml
```

p0155. Чтение из Kubernetes API + **создание/перезапись локального файла**. Риск: утрата прежнего содержимого, возможная публикация приватных метаданных. Verification: `diff` из книги; rollback прежней версии файла: **[Needs confirmation]**.

## Workload-generating: одиночный Pod

```bash
kubectl run nginx-pod --image=nginx:latest
kubectl apply -f nginx-pod.yaml
```

Manifest p0153:

```yaml
apiVersion: v1
kind: Pod
metadata:
  name: nginx-pod
spec:
  containers:
    - name: nginx-container
      image: nginx:latest
```

Эффект: создание/применение Pod, возможный запуск Nginx. Риски: ресурсы кластера, пересечение имен, изменяемый тег `latest`. Проверить `kubectl get pods`, `kubectl describe pod nginx-pod`. Rollback: `kubectl delete pod nginx-pod` (p0152), но восстановление состояния приложения не гарантируется: **[Needs confirmation]**. p0153 утверждает ошибку `apply` для существующего Pod; универсальность этой формулировки **[Needs confirmation]**.

Авторский пример image digest p0152: `nginx@sha256:1445eb9c6dc5e9619346c836ef6fbd6a95092e4663f27dcfce116f051cdbd232`. Не подтверждена текущая действительность этого реестрового объекта.

## Workload-generating: Pod с метками

```bash
kubectl run nginx-pod --image nginx --labels "tier=frontend"
kubectl run nginx-pod --image nginx --labels="app=myapp,env=dev,tier=frontend"
kubectl apply -f ~/labeled_pod.yaml
```

p0161–p0162; пример метаданных YAML:

```yaml
apiVersion: v1
kind: Pod
metadata:
  name: nginx-pod
  labels:
    environment: prod
    tier: frontend
spec:
  containers:
    - name: nginx-container
      image: nginx:latest
```

Эффект/риск: создаёт Pod и селектируемые метаданные. Verification: `kubectl get pods --show-labels`. Rollback ресурса/селекторов: **[Needs confirmation]**.

## State-changing: labels / annotations / replace

```bash
kubectl label pod nginx-pod stack=blue
kubectl label pod nginx-pod stack=green --overwrite
kubectl label pod nginx-pod stack-
```

p0162–p0164. Добавление, изменение и удаление label. **Риск:** другие объекты используют labels для связей; можно нарушить работу селекторов. **Verification:** `kubectl get pods nginx-pod --show-labels`. **Rollback:** возможен только при сохраненном прежнем значении, полноценное восстановление **[Needs confirmation]**.

p0164–p0165: пример `annotated_pod.yaml` задаёт `metadata.annotations.tier: webserver`. Текст упоминает `kubectl replace -f` как замену конфигурации, но **не даёт полного filename-аргумента**; не выдавать частичную запись за готовую безопасную команду. Риск replacement, верификация и rollback **[Needs confirmation]**.

## Access actions

```bash
kubectl port-forward pod/nginx-pod 8080:80
kubectl port-forward pod/nginx-pod :80
kubectl exec -it nginx-pod -- bash
kubectl exec -it nginx-pod -- /bin/bash
```

p0156–p0158. **Port-forward**: state-changing local connectivity, порт 8080 → 80, проверка `http://localhost:8080` в браузере; прекращение `Ctrl+C`. **Exec**: интерактивный доступ, в книге внутри показаны `hostname` (read-only) и `exit` (закрыть shell). Внутренние команды могут изменить контейнер; особенно учитывать исходное предупреждение не использовать root. Выход не откатывает изменения.

## State-changing: удаление Pod

```bash
kubectl delete pod nginx-pod
kubectl delete pods nginx-pod
kubectl delete pods/nginx-pod
kubectl delete -f nginx-pod.yaml
```

p0152, p0158–p0159. Удаляет Pod и контейнеры в нём. **Риск:** простой и потеря эфемерных данных. **Verification:** `kubectl get pods`. **Rollback:** пересоздание из YAML лишь если есть корректный манифест; сохранность состояния **[Needs confirmation]**.

## Workload-generating: Job

```bash
kubectl apply -f hello-world-job.yaml
```

Манифест из p0166–p0167:

```yaml
apiVersion: batch/v1
kind: Job
metadata:
  name: hello-world-job
spec:
  template:
    metadata:
      name: hello-world-job
    spec:
      restartPolicy: OnFailure
      containers:
        - name: hello-world-container
          image: busybox
          command: ["/bin/sh", "-c"]
          args: ["echo 'Hello world'"]
```

Вариации отдельных манифестов p0168–p0172: `backoffLimit: 3`, `completions: 10`, `parallelism: 5`, `activeDeadlineSeconds: 60`, `ttlSecondsAfterFinished: 30`. Эффект: создание/повторы/параллелизм Pod, время жизни/автоочистка Job. **Риски:** выполнение задач с побочными эффектами и нагрузкой. **Verification:** `kubectl get jobs` и `kubectl logs jobs/hello-world-job`. **Rollback:** побочные эффекты Job **[Needs confirmation]**.

```bash
kubectl delete jobs hello-world-job
kubectl delete jobs hello-world-job --cascade=false
```

p0172. Первый вариант удаляет Job и управляемые Pod по книге; второй приведён как способ сохранить созданные Pod. Риск удаления или оставления бесхозных Pod; verification `kubectl get jobs`, `kubectl get pods`, rollback **[Needs confirmation]**. Описание p0173 неоднозначно — см. findings.

## Workload-generating: CronJob

Манифест p0177:

```yaml
apiVersion: batch/v1
kind: CronJob
metadata:
  name: hello-world-cronjob
spec:
  schedule: "*/1 * * * *"
  successfulJobsHistoryLimit: 5
  startingDeadlineSeconds: 30
  jobTemplate:
    spec:
      template:
        metadata:
          name: hello-world-cronjob
        spec:
          restartPolicy: OnFailure
          containers:
            - name: hello-world-container
              image: busybox
              imagePullPolicy: IfNotPresent
              command: ["/bin/sh", "-c"]
              args: ["echo 'Hello world'"]
```

```bash
kubectl apply -f hello-world-cronjob.yaml
kubectl get cronjobs
kubectl get jobs
kubectl get pods
kubectl delete -f hello-world-cronjob.yaml
```

Эффект: создание периодического CronJob → Job → Pod каждую минуту. Риск непрерывного запуска задач, нагрузки и очистки истории; проверка `get cronjobs/jobs/pods` (p0178). Удаление CronJob останавливает будущие запуски по книге; rollback эффектов созданных задач **[Needs confirmation]**.

**Boundary:** все версии, имена и выводы — книжные примеры; никакой production-среды или права на выполнение не подтверждено.
