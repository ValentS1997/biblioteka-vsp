# Cheatsheet — Глава 4: Pod, labels, Job и CronJob

**RAG-only:** PDF 143–180; `kubernetes-complete-guide-madapparambat-mckendrick-2e-ru-2026:p0143:c01`–`…:p0180:c01`.

## Symptom / problem framing

Как превратить контейнерный образ в управляемый Kubernetes Pod, проверить его, открыть локальный доступ, добавить метаданные, а затем перейти к конечным и плановым заданиям? Глава отвечает через Pod → Job → CronJob (p0143–p0144, p0165–p0178).

## Baseline / context

- Нужны правильно настроенные Kubernetes и `kubectl`, хотя бы один узел `Ready` (p0144).
- **Pod**: 1+ контейнеров на **одном** узле, общее сетевое пространство имен и порты, подключаемые общие тома (p0144–p0147).
- Сеть CNI назначает Pod IP; авторы не рекомендуют использовать прямой Pod IP как основной путь доступа приложения (p0147–p0150).
- Pod должен быть пригоден для уничтожения/пересоздания; долговременное состояние выносится вовне. Авторы отделяют WordPress от MySQL/MariaDB на уровне Pod (p0149).
- **Labels** — идентификация/селекция; **annotations** — контекстные сведения, иногда используемые внешними системами (p0159–p0165).
- **Job** создает/контролирует один или несколько Pod для конечной задачи; **CronJob** создает Job по cron-расписанию (p0165–p0178).

## Read-only checks

```bash
kubectl get pods
kubectl get po -w
kubectl describe pod nginx-pod
kubectl get pods -o wide
kubectl get pods --show-labels
kubectl get pods -l "environment=production"
kubectl get jobs
kubectl logs jobs/hello-world-job
kubectl get cronjobs
```

Команды буквально присутствуют в p0151–p0156, p0159–p0162, p0167–p0168, p0178. `get`, `describe`, `logs` — наблюдение, `-w` — непрерывное наблюдение. Реальный контекст/namespace, секреты в аннотациях и логах, уровень доступа — **[Needs confirmation]**.

## Interpretation

- `kubectl get pods`: авторский пример `nginx-pod 1/1 Running` (p0151). `describe` показывает контейнеры, Conditions, Events, IP (p0154).
- `-o wide` сообщает узел и Pod IP (p0156). `port-forward` + браузер подтверждают работу Nginx в авторском эксперименте (p0156–p0157).
- `kubectl get pods --show-labels` и `-l` позволяют сравнить фактические метки и выборку (p0159–p0164). Изменение labels может изменить работу объектов, использующих селекторы (p0163).
- `kubectl get jobs` c `COMPLETIONS 1/1` и `kubectl logs jobs/hello-world-job` → `Hello world` — пример успешного Job (p0167–p0168).
- `backoffLimit: 3`, `completions: 10`, `parallelism: 5`, `activeDeadlineSeconds: 60`, `ttlSecondsAfterFinished: 30` показаны в **разных** Job-примерах (p0168–p0172), их нельзя автоматически объединять.
- `schedule: "*/1 * * * *"`, `startingDeadlineSeconds: 30`, `successfulJobsHistoryLimit: 5` — пример CronJob (p0177). Результат наблюдается через `get cronjobs/jobs/pods` (p0178).

## Next action

Практиковаться только в авторизованном учебном кластере: установить целевой Kubernetes context/namespace **[Needs confirmation]**, запустить один Pod, прочитать его состояние, при необходимости выполнить кратковременный `port-forward`, затем изучить метки, Job и CronJob. Для production deployment/backup/security требуется отдельный план: глава его не дает.

## Modifying action

Учебные действия, **меняющие кластер**:

```bash
kubectl run nginx-pod --image=nginx:latest
kubectl apply -f nginx-pod.yaml
kubectl label pod nginx-pod stack=blue
kubectl label pod nginx-pod stack=green --overwrite
kubectl apply -f hello-world-job.yaml
kubectl apply -f hello-world-cronjob.yaml
```

`run/apply` создают или обновляют ресурсы и могут вызывать выполнение контейнеров; `label` меняет селектируемые метаданные; `CronJob` создает периодические Job (p0151–p0153, p0161–p0167, p0177). Риски: потребление ресурсов, нарушение связей по label, повторные задачи и доступ к данным. Не выполнять на рабочей инфраструктуре автоматически.

`kubectl port-forward pod/nginx-pod 8080:80` — изменяет локальную сетевую доступность на время работы процесса; `kubectl exec -it nginx-pod -- bash` — открывает интерактивную оболочку, действия внутри могут изменить контейнер (p0156–p0158). Источник призывает придерживаться наименьших привилегий.

## Verification / acceptance checks

1. После Pod: `kubectl get pods`, `kubectl describe pod nginx-pod`, `kubectl get pods -o wide`.
2. Для forwarding: `http://localhost:8080` в браузере; остановить `Ctrl+C` (p0157).
3. После labels: `kubectl get pods nginx-pod --show-labels` (p0163–p0164).
4. Для Job: `kubectl get jobs` и `kubectl logs jobs/hello-world-job` (p0167–p0168).
5. Для CronJob: `kubectl get cronjobs`, `kubectl get jobs`, `kubectl get pods` (p0178).
6. Универсальные acceptance thresholds production **[Needs confirmation]**.

## Rollback

- Удаление Pod через `kubectl delete pods nginx-pod` или `kubectl delete -f nginx-pod.yaml` удаляет контейнеры; не гарантирует восстановления данных (p0158–p0159).
- `kubectl label pod nginx-pod stack-` удаляет метку, но может изменить селекторы. Возврат исходного значения требует заранее его знать (p0163–p0164).
- `kubectl delete jobs hello-world-job` удаляет Job и управляемые Pod; вариант `--cascade=false` по тексту книги сохраняет Pod (p0172).
- `kubectl delete -f hello-world-cronjob.yaml` прекращает будущие расписания удалением ресурса; обратное восстановление эффектов уже созданных Job **[Needs confirmation]** (p0178).
- `Ctrl+C` прекращает port-forward; `exit` закрывает интерактивный shell, но не отменяет действий в контейнере.
- Общий rollback `apply`, `replace`, файлового вывода и job side effects: **[Needs confirmation]**.

## Source caveats

В p0153, p0168, p0170–p0173 есть утверждения о `apply`, Job retries, параллелизме и cascade, которые требуют отдельной проверки; сохраняются как исходные варианты в [source-findings.md](source-findings.md), а не правятся без источника.
