# Source-confirmed commands — Глава 5

**Scope:** RAG PDF 181–217. Команды в этой таблице/блоках взяты из главы 5, без текущей внешней проверки или исполнения. Цель, контекст, namespace, RBAC, версии и права реального кластера **[Needs confirmation]**.

## Read-only / observation

| Команда из книги | Эффект | Страница |
|---|---|---:|
| `kubectl get pods` / `kubectl get pod` | статус Pod | 185–188 |
| `kubectl describe pod failed-multi-container-pod` | Events/ErrImagePull/ImagePullBackOff | 186–187 |
| `kubectl describe pods/multi-container-pod` | список контейнеров и подробности | 190 |
| `kubectl get pod/multi-container-pod -o jsonpath="{.spec.containers[*].name}"` | имена из спецификации Pod | 190 |
| `kubectl logs multi-container-pod -c debian-container` | stdout/stderr Debian | 185 |
| `kubectl logs multi-container-pod -c nginx-container` | stdout/stderr Nginx | 185 |
| `kubectl logs -f pods/multi-container-pod --container nginx-container` | follow журнала контейнера | 198 |
| `kubectl logs --since=2h pods/multi-container-pod --container nginx-container` | журнал за последние 2 часа | 198 |
| `kubectl logs --tail=30 pods/multi-container-pod --container nginx-container` | 30 последних строк | 198 |
| `kubectl get po -w` | watch состояния Pod и initContainers | 194, 196–197 |
| `kubectl get po` | статус Pod после emptyDir манифеста | 202 |

Логи могут содержать информацию приложения. При отсутствии `--container/-c` автор p0192 описывает неявный выбор контейнера, поэтому при множестве контейнеров имя следует задавать явно (p0198).

## Workload-generating: два контейнера в одном Pod

```yaml
# multi-container-pod.yaml; RAG p0184
apiVersion: v1
kind: Pod
metadata:
  name: multi-container-pod
spec:
  restartPolicy: Never
  containers:
    - name: nginx-container
      image: nginx:latest
    - name: debian-container
      image: debian
      command: ["/bin/sh"]
      args: ["-c", "while true; do date; echo debian-container; sleep 5; done"]
```

```bash
kubectl apply -f multi-container-pod.yaml
kubectl get pods
```

**Effect:** создаёт Pod с двумя контейнерами (p0184–p0185). **Risk:** использование вычислительных ресурсов и незакреплённых тегов образов; **verification:** `2/2 Running` по образцу p0185, затем адресные логи. **Rollback:** `kubectl delete -f multi-container-pod.yaml` или `kubectl delete pods/multi-container-pod` из p0188 удалит Pod/контейнеры, но не вернёт уничтоженное состояние [Needs confirmation].

## Failure exercise: демонстрационный конфликт имени

В p0186 дан манифест `failed-multi-container-pod.yaml` с `image: nginx:i-do-not-exist`, но **`metadata.name: multi-container-pod`**, а пример результата `kubectl apply -f failed-multi-container-pod.yaml` сообщает **`pod/failed-multi-container-pod created`**. Следующие `get`/`describe` тоже указывают имя `failed-multi-container-pod`. Поэтому **этот манифест не воспроизводить как целостную процедуру** без явного разрешения [Source code mismatch]; сохранено в [source-findings.md](source-findings.md). В книге `describe` показывает `ErrImagePull`/ `ImagePullBackOff` (p0187).

## State-changing: normal deletion and force deletion

```bash
kubectl delete -f multi-container-pod.yaml
kubectl delete pods/multi-container-pod
kubectl delete pods multi-container-pod
kubectl delete -f failed-multi-container-pod.yaml
kubectl delete pod failed-multi-container-pod --grace-period=0 --force
```

p0188–p0189. **Effect:** удаление Pod, включая контейнеры. **Risk:** нарушает доступность; **force** освобождает имя, но Kubernetes может ещё выполнять прежний ресурс, о чём книга прямо предупреждает. **Verification:** `kubectl get pod`, однако для force фактическое прекращение без доп. наблюдений [Needs confirmation]. **Rollback:** [Needs confirmation]. Force применять только в особой ситуации, не как обычный cleanup.

## Executing processes in containers: permission-sensitive access

```bash
kubectl exec -it multi-container-pod --container nginx-container -- /bin/bash
kubectl exec pods/multi-container-pod -c nginx-container -- ls
kubectl exec multi-container-with-emptydir-pod -c debian-container -- ls /var
kubectl exec multi-container-with-emptydir-pod -c nginx-container -- ls /var
```

p0190–p0192, p0202–p0203. Первые операции дают запуск процесса внутри контейнера; `ls` — read-only *команда внутри контейнера*, `bash` — интерактивный процесс, который способен изменить состояние. **Risk:** права контейнера и исполнение произвольных инструкций. **Verification:** исходник показывает `hostname`, `ls /var`, ожидаемый каталог. **Rollback:** выход из shell не отменяет изменений внутри; [Needs confirmation].

Команда p0203 **изменяет общий том**:
```bash
kubectl exec multi-container-with-emptydir-pod -c debian-container -- /bin/sh -c "echo 'hello world' >> /var/i-am-empty-dir-volume/hello-world.txt"
```
Проверочные **read-only exec**:
```bash
kubectl exec multi-container-with-emptydir-pod -c nginx-container -- cat /var/i-am-empty-dir-volume/hello-world.txt
kubectl exec multi-container-with-emptydir-pod -c debian-container -- cat /var/i-am-empty-dir-volume/hello-world.txt
```

p0203. **Effect:** запись локального файла `hello-world.txt` в `emptyDir`, затем чтение из обоих контейнеров. **Risk:** удаление Pod безвозвратно удаляет данные `emptyDir`. **Verification:** строка `hello world` в обоих выводах. **Rollback:** [Needs confirmation].

## Workload-generating: initContainers

`nginx-with-init-container.yaml` из p0195–p0196 задаёт `emptyDir` с `name: website-volume`, `initContainers[0].name: download-website`, `image: busybox`; init-контейнер с помощью `wget` и `unzip` загружает демонстрационный сайт из GitHub и размещает его в смонтированном каталоге `/usr/share/nginx/html`. Основной `nginx-container` монтирует тот же том. **Команды из главы**:

```bash
kubectl apply -f nginx-with-init-container.yaml
kubectl get po -w
kubectl expose pod nginx-with-init-container --port=80 --type=NodePort
kubectl port-forward pod/nginx-with-init-container 8080:80
```

p0196–p0197. **Effect:** `apply` создаёт Pod и инициирует внешний download; `expose` создаёт Service типа NodePort, меняет сетевую доступность; `port-forward` создаёт временное локальное соединение. **Risk:** внешние загрузки, сеть/NodePort, открытый порт 8080 и источник контента; **verification:** `Init:0/1 → Running`, затем браузер по `http://localhost:8080`; **rollback:** `Ctrl+C` для port-forward (p0197), ресурсы и скачанное содержимое — [Needs confirmation].

## Config and args override

p0193 Dockerfile:
```dockerfile
FROM busybox:latest
ENTRYPOINT ["sleep"]
CMD ["30"]
```

p0194 YAML `nginx-debian-with-custom-command-and-args.yaml` содержит `command: ["sleep"]` и `args: ["60"]` для Debian; в тексте описана пара `command ↔ ENTRYPOINT`, `args ↔ CMD`.
```bash
kubectl apply -f nginx-debian-with-custom-command-and-args.yaml
kubectl get po -w
```
**Effect:** создаёт Pod с переопределенной программой контейнера; по примеру он переходит в `NotReady` после завершения `sleep`. **Risk:** рабочая нагрузка может завершиться раньше ожидаемого; **verification:** watch, **rollback:** [Needs confirmation].

## Workload-generating: emptyDir / hostPath

```bash
kubectl apply -f multi-container-with-emptydir-pod.yaml
kubectl apply -f multi-container-with-hostpath.yaml
kubectl get pod
```

p0201–p0206. **Effect:** создаёт Pod с общим `emptyDir`, либо Pod с `hostPath: /tmp`, `type: Directory` и `mountPath: /foo`. **Risk:** `hostPath` монтирует реальные файлы узла; привязка к узлу, права, SELinux и переносимость (p0204). **Verification:** `get`, `exec ... cat /foo/hello-world.txt` (p0206). **Rollback:** удаление Pod не восстанавливает состояние файлов host, [Needs confirmation].

Для подготовки hostPath автор приводит **state-changing local/node**:
```bash
minikube ssh
echo "Hello World" > /tmp/hello-world.txt
```
p0205: `echo` выполняется **внутри minikube VM**, не обязательно на физической рабочей станции. Также p0206 показывает `sudo podman exec -it minikube /bin/bash` как вариант доступа; не использовать на произвольном узле без подтверждения.

## Ambassador, Sidecar, Adapter: source limits

- **Ambassador** p0208: YAML `nginx-with-ambassador.yaml` с контейнерами `mysql-proxy-ambassador-container` (`mysql-proxy:latest`, `DB_HOST=...`, port 3306) и `nginx-container`. Авторы прямо отмечают, что для реального теста нужен доступный AWS RDS и надлежащее приложение; полный работающий способ подключения **[Needs confirmation]**. Никакие credentials не включены.
- **Sidecar** p0211–p0212: `nginx-with-fluentd-sidecar.yaml` содержит Nginx и Fluentd `fluent/fluentd:v1.17` с общим `emptyDir` по `/var/log/nginx`. Рядом дан ConfigMap Fluentd, но в показанном Pod нет явно связанного mount этой конфигурации: **[Needs confirmation]**. Доступность Elasticsearch не подтверждена.
- **Adapter** p0214–p0215: манифест `alpine-with-adapter.yaml` имеет `alpine-writer`, `log-adapter`, `emptyDir`, преобразование через `sed`. На p0215 автор применяет **другое** имя:
```bash
kubectl apply -f nginx-with-adapter.yaml
kubectl exec -it pod-with-adapter -c alpine-writer -- head -5 /var/log/app/app.log
kubectl exec -it pod-with-adapter -c log-adapter -- head -5 /logs/processed_app.log
```
`apply` — **workload-generating**, `head` в контейнере — **read-only**; риск циклического логирования и файловых изменений. **Verification:** записи с суффиксом `PROCESSED`; **rollback:** [Needs confirmation]. Имя `alpine-with-adapter.yaml` / `nginx-with-adapter.yaml` — [Source code mismatch], не выбирать за пользователя.

**Native sidecar** p0216: фрагмент YAML, а не полный Deployment, с `initContainers`/`restartPolicy: Always`. Нет законченной команды запуска и верифицированного текущего Kubernetes-версии — **[Needs confirmation]**.
