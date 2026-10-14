# Cheatsheet — Глава 5. Многоконтейнерные Pod

**Source:** RAG PDF 181–217, `kubernetes-complete-guide-madapparambat-mckendrick-2e-ru-2026:p0181:c01`–`…:p0217:c01`. Примеры — учебные, живой кластер не проверялся.

## Symptom / problem framing

Как совместно запустить контейнер приложения и помощника, выбрать нужный контейнер для `exec`/логов, диагностировать `ImagePullBackOff`, обмениваться файлами и изолировать вспомогательную логику с помощью Ambassador/Sidecar/Adapter? Глава показывает многоконтейнерный Pod с Nginx и Debian, init-контейнеры и тома (p0182–p0216).

## Baseline / context

- Нужны `kubectl` и локальный/облачный кластер (p0182). Точный контекст, namespace, RBAC и ресурсы **[Needs confirmation]**.
- Контейнеры одного Pod планируются на **один узел** и могут разделять сеть/том; управляются одним жизненным циклом Pod (p0182–p0185).
- Контейнеры из демонстрационного `multi-container-pod.yaml`: `nginx-container` (`nginx:latest`) и `debian-container` с циклом `date; echo; sleep 5`, `restartPolicy: Never` (p0184).
- **initContainers** выполняются последовательно до основных контейнеров; отсутствие успешной инициализации препятствует запуску основных (p0194–p0197).
- **emptyDir** — общий пустой каталог на время жизни Pod, данные теряются при удалении Pod; **hostPath** — монтирование файловой системы узла с рисками безопасности и переносимости (p0199–p0205).
- **Ambassador** — прокси для исходящего доступа к внешним системам (p0207–p0209); **Sidecar** — добавочные функции вроде пересылки логов (p0209–p0212); **Adapter** — преобразование данных (p0212–p0215).
- Авторы отдельно обсуждают **нативный sidecar** в разделе `initContainers` с `restartPolicy: Always` (p0215–p0216); указанная автором версия не проверена на текущем окружении.

## Read-only checks

```bash
kubectl get pods
kubectl get pod
kubectl describe pods/multi-container-pod
kubectl get pod/multi-container-pod -o jsonpath="{.spec.containers[*].name}"
kubectl logs multi-container-pod -c debian-container
kubectl logs multi-container-pod -c nginx-container
kubectl logs -f pods/multi-container-pod --container nginx-container
kubectl logs --since=2h pods/multi-container-pod --container nginx-container
kubectl logs --tail=30 pods/multi-container-pod --container nginx-container
```

Все приведены в p0185–p0190, p0197–p0198. Команды `get`, `describe` и `logs` не меняют состояние кластера, но могут выводить чувствительные сведения. `-f` — длительное чтение потока. Для выборки контейнера использовать имя из `.spec.containers[*].name`.

## Interpretation

- `READY 2/2` в примере p0185 означает оба контейнера готовы; `1/2 ImagePullBackOff` p0186 — один контейнер не может скачать образ, другой может работать.
- Диагностика: `kubectl describe pod failed-multi-container-pod` отображает `ErrImagePull`, `ImagePullBackOff` и события загрузки несуществующего `nginx:i-do-not-exist` (p0186–p0187). **Имя metadata в YAML не совпадает с результатом** — запись в `source-findings.md`.
- Для `kubectl exec` и `kubectl logs` в многоконтейнерном Pod рекомендуется явно `-c`/`--container` (p0190–p0192, p0198). Книга p0192 также описывает выбор первого контейнера при отсутствии флага — не полагаться на неявный выбор.
- `Init:0/1` в watch означает незавершённый init-контейнер; после завершения появляется обычный `Running` (p0196–p0197).
- Общий `emptyDir` проверяется записью в Debian и чтением из Nginx (p0202–p0203), что **меняет содержимое тома**.
- `hostPath` по p0204 непереносим между узлами; использовать как общее постоянное хранилище нельзя без отдельной оценки.
- Нативные sidecar-поведния по книге зависят от версии, [Needs confirmation].

## Next action

Уточнить действительный контекст Kubernetes и допуск учебных изменений. Создать тестовый Pod из YAML, проверить `READY` и события, адресно получить `logs -c`. Затем независимо испытать initContainers, emptyDir и один из паттернов. **Не воспроизводить ошибочный пример YAML без учёта несоответствия имени**. Для доступа к внешним сервисам и реальным журналам подтверждать сеть/секреты отдельно.

## Modifying action

```bash
kubectl apply -f multi-container-pod.yaml
kubectl apply -f nginx-with-init-container.yaml
kubectl apply -f multi-container-with-emptydir-pod.yaml
kubectl apply -f multi-container-with-hostpath.yaml
kubectl delete pods/multi-container-pod
```

Примеры p0184, p0188, p0196, p0202, p0206. **Эффект:** создают или удаляют Pod и связанные контейнеры/тома. **Риск:** нагрузка, сетевой доступ, повреждение/утрата данных, ограничения hostPath. **Verification:** `kubectl get pods`, `describe`, `logs -c` и проверки монтирования. **Rollback:** после уничтожения данных emptyDir невозможно восстановить их из описанной главы; для hostPath и side effects [Needs confirmation].

**Не нормальный способ cleanup:** `kubectl delete pod failed-multi-container-pod --grace-period=0 --force`. Авторы прямо предупреждают, что имя может освободиться до фактической остановки Pod (p0189). Не применять без отдельного решения.

## Verification / acceptance checks

- Pod: `kubectl get pods` показывает `2/2 Running` в сценарии книги; `describe` и `logs -c` позволяют локализовать сбой (p0185–p0187).
- Init: `kubectl get po -w` показывает переход `Init:0/1 → PodInitializing → 1/1 Running` (p0196–p0197).
- emptyDir: `kubectl exec` читает один и тот же `hello-world.txt` в двух контейнерах (p0203).
- Adapter: p0215 показывает в журнале исходную строку и вариант с `PROCESSED`; **имя файла при apply расходится с именем манифеста**.
- Sidecar/амбассадор в книге показаны концептуально; успешное подключение к настоящей внешней БД/сервису и Fluentd получателем не демонстрируется: **[Needs confirmation]**.

## Rollback

- Обычное удаление `kubectl delete -f multi-container-pod.yaml` или по имени приводит к прекращению Pod (p0188). Полное восстановление файлов/сервисов [Needs confirmation].
- `emptyDir`: при удалении Pod данные уничтожаются, rollback файлов невозможен по книге (p0203).
- `hostPath`: удаление Pod не является инструкцией по восстановлению файлов узла; [Needs confirmation] (p0204–p0206).
- `kubectl port-forward` завершается Ctrl+C (p0197); `kubectl exec -it` даёт возможность менять контейнер, выход из shell не отменяет изменений.
- Принудительное удаление не гарантирует остановку процесса: **не считать rollback** (p0189).
