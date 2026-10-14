# Cheatsheet — Глава 11: Deployment для stateless workload

**Source:** RAG PDF 384–419; `kubernetes-complete-guide-madapparambat-mckendrick-2e-ru-2026:p0384:c01`–`…:p0419:c01`. Никакие Kubernetes-команды не выполнялись.

## Symptom / problem framing

Нужно выпускать новую версию stateless-приложения, поддерживать число Pod, исключать неготовые реплики из трафика и быстро возвращаться к прежнему образу. `Deployment` задаёт desired state для дочерних `ReplicaSet`; `Service` обнаруживает Pod по меткам и обеспечивает стабильную точку входа; `readinessProbe` определяет готовность каждого endpoint (p0384–p0389, p0392–p0402).

## Baseline

- Кластер Kubernetes и настроенный `kubectl`; многоузловой рекомендуется автором (p0384). **Context, namespace, RBAC, тип Service, образ, ресурсы и SLO [Needs confirmation].**
- Демонстрационный `nginx-deployment-example`: `replicas: 3`, `app: nginx`, `environment: test`, `nginx:1.17`, `minReadySeconds: 10`, `RollingUpdate`, `maxUnavailable: 1`, `maxSurge: 1` (p0388–p0389). При rollout допускаются до 4 Pod, минимум 2 считаются доступными в авторском расчёте (p0406–p0407).
- Селектор Deployment после создания не меняют; шаблонные labels должны ему соответствовать (p0389–p0390). Пересечение labels с чужими объектами может приводить к конфликтам (p0415).
- `Service` выбирает Pod с `app=nginx,environment=test`; в книге `nginx-service-example` — `LoadBalancer` с port/targetPort 80 (p0394–p0395). Для локального кластера возможен только NodePort/ClusterIP.
- `nginx-deployment-readinessprobe.yaml`: `replicas: 3`, `nginx:1.25.4`, `touch /usr/share/nginx/html/ready`, `readinessProbe: httpGet /ready`, period 2 sec, failureThreshold 2 (p0397–p0399).
- `RollingUpdate` создаёт новый RS и постепенно меняет число Pod; `Recreate` сначала прекращает старые Pod и может вызвать downtime (p0405). Для дальнейших примеров версионирования p0406–p0411 книга использует образы `nginx:1.17 → 1.18 → 1.19`.

## Read-only checks / observation

```bash
kubectl get deploy nginx-deployment-example
kubectl get rs
kubectl get pods
kubectl rollout status deployment nginx-deployment-example
kubectl describe service nginx-service-example
kubectl describe svc nginx-service-example | grep Endpoint
kubectl describe pod nginx-deployment-readiness-69dd4cfdd9-4pkwr
kubectl get po -w
kubectl describe deployments.apps nginx-deployment-readiness
kubectl describe deploy nginx-deployment-rollingupdate
kubectl rollout status deployment.apps/nginx-deployment-rollingupdate
kubectl rollout history deployment.apps/nginx-deployment-rollingupdate
kubectl rollout history deploy nginx-deployment-rollingupdate --revision=2
```

RAG p0391, p0395, p0400–p0403, p0407–p0411. `rollout status` отслеживает процесс; `-w` — поток наблюдения. В `kubectl get pods` отсутствует явное указание namespace: прежде чем полагаться на вывод, проверить текущий контекст — [Needs confirmation]. Имена Pod и IP в книге **учебные**.

## Interpretation

- `READY: 3/3` и `rollout successfully rolled out` — наблюдение конкретного Deploy, не доказательство application SLO, сетевого доступа и отсутствия пользовательского простоя (p0391).
- При `rm /usr/share/nginx/html/ready` HTTP readiness возвращает **404**, `Unhealthy`; endpoint исчезает из `Endpoints` Service, но Pod остаётся **Running** (p0400–p0401). Если все три не готовы, `curl` к Service падает (p0401). Воссоздание `ready` восстанавливает готовность (p0402).
- Scale `replicas: 3 → 10 → 2` через `apply` приводит к `ScalingReplicaSet` (p0402–p0403). Аналоги `kubectl scale` — императивное изменение, обычно учебное.
- `RollingUpdate` на `nginx:1.18` создаёт новый RS; старый остаётся с нулём реплик для истории; `revisionHistoryLimit` по книге по умолчанию 10 (p0407–p0409).
- Ревизии `1/2/3`, после `rollout undo` показаны `1/3/4` (p0410–p0411): **номер ревизии не идентичен неизменному номеру версии образа**.
- Canary: stable `frontend-app:1.0` (3 replicas) и canary `frontend-app:2.0` (1 replica), общий Service выбирает `app=myapp,tier=frontend`; точная доля трафика не измерена в исходнике (p0412–p0413).

## Next action

Прочитать текущие Deploy/RS/Pod, labels, endpoints, историю и readiness; согласовать SLO, допустимое `maxUnavailable`/`maxSurge`, квоты, rollout/change gate. В production управлять манифестом из Git/IaC и запускать проверяемый pipeline, что рекомендует книга (p0409, p0414). Версия кластера и безопасность `apps/v1`/probes/публикации — [Needs confirmation].

## State-changing actions

```bash
kubectl apply -f ./nginx-deployment.yaml
kubectl apply -f nginx-service.yaml
kubectl apply -f ./nginx-deployment-readinessprobe.yaml
kubectl apply -f nginx-deployment-rollingupdate.yaml
kubectl scale deploy nginx-deployment-readiness --replicas=10
kubectl rollout undo deploy nginx-deployment-rollingupdate
```

**Effect:** создаются или меняются Deployment/RS/Pod/Service, число реплик либо ревизия. **Risks:** сбой трафика при ошибочной readiness, масштабирование расходует ресурсы, LoadBalancer — внешняя экспозиция/стоимость, императивный rollback может расходиться с Git. **Verification:** `kubectl rollout status`, `get deploy/rs/pods`, `describe svc` и приложение по Service (p0391–p0411). **Rollback:** source описывает `kubectl rollout undo` и восстановление Git-манифеста, но точные rollback manifest, SLO, rollback data [Needs confirmation].

**Негативный тест, только одноразовый кластер (p0400–p0402):**
```bash
kubectl exec -it nginx-deployment-readiness-69dd4cfdd9-4pkwr -- rm /usr/share/nginx/html/ready
kubectl exec -it nginx-deployment-readiness-69dd4cfdd9-4pkwr -- touch /usr/share/nginx/html/ready
```
**Effect:** `rm` нарушает готовность, `touch` создаёт файл, возвращая соответствие пробе. **Risk:** кратковременная/полная недоступность Service. **Verification:** Endpoints, `describe pod` `Unhealthy`, HTTP-запрос из debug Pod. **Rollback:** source показывает `touch`, но восстановление самого файла и готовности не универсально, другие Pod/образы [Needs confirmation].

**Деструктивно (p0397, p0404):** `kubectl delete deployment nginx-deployment-example`, `kubectl delete deploy nginx-deployment-readiness`; `--cascade=orphan` оставляет Pod в источнике, но не гарантирует управляемость. Не применять как обычную процедуру отката.

## Verification / acceptance

`rollout status` успешно завершён; `get deploy` показывает желаемые ready/available Pod; `describe svc` показывает только готовые endpoints; версия образа подтверждена `describe pod … | grep 'Image:'`; история показывает ожидаемую ревизию (p0391, p0401–p0411). Реальные измерения доли canary, HTTP SLO, состояние после rollback, права и storage **[Needs confirmation]**.

## Rollback и безопасность

При ошибочном rollout книга предлагает **вернуть предыдущий Git commit и повторно применить манифест** либо `kubectl rollout undo` в учебном сценарии (p0409–p0411). `pause/resume` лишь меняет ход развертывания, не заменяет восстановление исправной конфигурации. `delete`/ `Recreate`/неверные liveness probes могут вызвать downtime. Данные в работающих контейнерах, секреты и внешние зависимости не покрыты экспериментом. См. [source-findings.md](source-findings.md).
