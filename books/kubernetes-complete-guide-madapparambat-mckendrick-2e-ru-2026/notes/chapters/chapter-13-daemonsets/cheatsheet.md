# Cheatsheet — Глава 13. DaemonSet: один Pod на подходящий узел

**RAG:** `kubernetes-complete-guide-madapparambat-mckendrick-2e-ru-2026:p0457:c01`–`…:p0473:c01`, PDF 457–473. Ни один кластер не изменялся. При нехватке source evidence — **[Needs confirmation]**.

## Symptom / problem framing

Нужен агент мониторинга, CNI, сборщик логов или exporter на **каждом подходящем узле** и автоматическое расширение при появлении новых nodes. `DaemonSet` поддерживает соответствие между eligible nodes и Pod, без `spec.replicas`. Особые требования к узлу задаются `nodeSelector`, `nodeAffinity`, `tolerations`; управляемые Pod имеют selector и template (p0457–p0464).

## Baseline / prerequisites

- Доступный Kubernetes, настроенный `kubectl`, многоузловой кластер для наглядного опыта (p0457). Учебная конфигурация: `minikube`, VirtualBox, Calico, 3 узла, Kubernetes v1.31.0 (p0460). Текущий context/RBAC, ресурсы, CNI и сеть **[Needs confirmation]**.
- В книге Calico и kube-proxy показаны как DaemonSet `kube-system`; по одному Pod на три узла (p0461–p0462). **Не изменять CNI или kube-proxy** ради практики.
- Демонстрация Fluentd: `fluentd-elasticsearch`, historical image `quay.io/fluentd_elasticsearch/fluentd:v4.7`, `hostPath: /var/log`, CPU request 100m, memory request/limit 200Mi, отправка в `elasticsearch-logging:9200` (p0463–p0465). Рабочий Elasticsearch endpoint **не** создаётся в главе.
- **Блокирующая несогласованность источника:** DaemonSet задан в `kube-system`, но CLI/ожидаемые Pod — в `logging` (p0463 vs p0465). Не утверждать, что source manifest воспроизводит показанный результат; дальнейшее применение **[Needs confirmation]**.

## Read-only checks

```bash
kubectl get nodes
kubectl get daemonsets -A
kubectl get po -n kube-system -o wide | grep calico
kubectl get po -n logging -o wide
kubectl describe daemonset fluentd-elasticsearch -n logging
kubectl describe ds -n logging
kubectl describe ds -n kube-system kube-proxy
```

p0461, p0465, p0468, p0470. `kubectl describe daemonset ... -n logging` из главы не проверен против исходного DaemonSet namespace; не считать `NotFound` доказательством отсутствия Pod. Перед диагностикой подтвердить namespace/selector на **фактическом** кластере [Needs confirmation].

В примере `kubectl get daemonsets -A` содержит `DESIRED/CURRENT/READY/UP-TO-DATE/AVAILABLE` для `calico-node` и `kube-proxy`; `-A` объединяет namespace. `get po ... -o wide` позволяет сравнить Pod → node (p0461–p0462).

## Interpretation

- `desired=3/current=3/ready=3` в трёхузловой конфигурации Calico означает 3 соответствующих Pod, **не** измеренную доступность сети (p0461).
- **Scope:** one Pod **per eligible node**, а не безусловно на абсолютно всех узлах. Узлы могут не подходить по labels/affinity/taints или ресурсам (p0459–p0460, p0464).
- DaemonSet `fluentd` читает `/var/log` хоста через `hostPath`; это доступ к чувствительным узловым логам, требует доверенного образа/минимальных прав. Конкретные security controls source не предоставляет — [Needs confirmation] (p0464–p0465).
- Сетевые варианты: hostPort, агент, сам отправляющий данные другому сервису, headless Service или обычный Service (p0459–p0460). Выбор определяется задачей, прямое общение с агентами часто не требуется.
- При обновлении шаблона Pod стратегия `RollingUpdate` последовательно заменяет Pod, `OnDelete` ждёт ручного удаления; пример `v4.7 → v4.7.5` и status `2/3 → 3/3` на p0467–p0468.
- Если daemon имеет высокий priority, другие workload могут пострадать от конкуренции за ресурсы/вытеснения; в тексте `system-node-critical` описан как абсолютная защита, но реальный результат при ошибках/сбое узла не проверен (p0466–p0467).

## Next action

1. Подтвердить, какие nodes должны обслуживаться, их labels, taints/tolerations и ОС.
2. Разделить системный DaemonSet (kube-system) и учебный logging workload; исправление несогласованного namespace **только после** отдельного утверждения манифеста — [Needs confirmation].
3. Проверить requests/limits и security access к hostPath `/var/log`, изоляцию namespace, выходной Elasticsearch endpoint и образ.
4. Согласовать допустимое число временно недоступных Pod и rollback при отказе сетевого/логирующего агента. Для критичных DaemonSet необходим staging.
5. До любого удаления/rollout убедиться, что это не CNI/kube-proxy и не production logging pipeline.

## Source modifying actions

```bash
minikube start --driver=virtualbox --nodes=3 --cni=calico --cpus=2 --memory=2g --kubernetes-version=v1.31.0 --container-runtime=containerd
kubectl apply -f fluentd-daemonset.yaml
kubectl rollout status ds -n logging
kubectl rollout undo daemonset fluentd-elasticsearch -n logging
```

p0460, p0465, p0468–p0469. **Effect:** создание учебного кластера или DaemonSet, изменение Pod на каждом узле, откат image/template; `rollout status` только наблюдает. **Risk:** поломка сетевой основы, ресурсы, чтение узловых логов, namespace mismatch, отсутствие Fluentd→Elasticsearch. **Verification:** `get daemonsets -A`, `get po -n <ns> -o wide`, `describe ds`, `rollout status`. **Rollback:** `rollout undo` описан, но полное восстановление logs/network не показано — [Needs confirmation]. При изначально несовпадающем namespace команда undo может вообще не найти объект.

## Destructive and sensitive operations

```bash
kubectl delete ds fluentd-elasticsearch -n logging
kubectl delete ds fluentd-elasticsearch -n logging --cascade=orphan
```

p0469. **Взаимоисключающие альтернативы, не последовательность.** Первая удаляет DaemonSet и Pod, вторая оставляет Pod без контроллера. Ни одна не удаляет показанный в YAML DaemonSet `kube-system` без дополнительного изменения/верификации namespace. Восстановление и безопасное прекращение записи логов **[Needs confirmation]**.

`kubectl exec -n logging -it fluentd-elasticsearch-cs4hm -- /bin/bash` и `ls -l /var/log/` (p0465) открывают процесс внутри Pod и могут раскрыть структуру системных журналов. Для диагностики это не чистое read-only API; не выводить реальные логи в CI.

`kubectl drain` c `--ignore-daemonsets` упомянут как особый случай (p0469), но **полного безопасного runbook обслуживания узла в главе нет**. Удаление Node или drain здесь не выполнялось.

## Verification / acceptance

В учебной среде: сравнить число подходящих nodes с DESIRED/READY DaemonSet, проверить `Pod NODE` раздельно, статус rollout, ожидаемые `SuccessfulDelete` и `SuccessfulCreate` при обновлении (p0461, p0465, p0468). Доказательства доставки логов до Elasticsearch, high availability, восстановления CNI и security posture не представлены — [Needs confirmation].

## Rollback

Source `kubectl rollout undo daemonset fluentd-elasticsearch -n logging` возвращает revision **при наличии корректного объекта и истории** (p0469). Для GitOps предпочтительнее вернуть предыдущий YAML и применить его, но конкретная команда восстановительного apply в этом подразделе не дана. Каскадное удаление и orphan — **не** безопасные rollback сетевых/логирующих сервисов. Контекст, права, служебные зависимости и данные [Needs confirmation].
