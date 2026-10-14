# Cheatsheet — Глава 8. Service, сети и probes

**Источник:** PDF 281–325, RAG `kubernetes-complete-guide-madapparambat-mckendrick-2e-ru-2026:p0281:c01`–`…:p0325:c01`. Только источник, без исполнения команд.

## Symptom / problem framing

IP пода может меняться при пересоздании (p0285–p0287). Привязка клиентского кода к Pod IP ненадёжна. **Service** даёт имя и точку доступа к целому набору Pod, связанному `spec.selector` ↔ `metadata.labels`; доступность endpoints зависит от готовности приложений (p0288–p0297, p0316–p0324).

## Baseline / context

- Доступный учебный Kubernetes и настроенный `kubectl`; реальный context, namespace, RBAC, CNI, kube-proxy mode, возможность внешней публикации неизвестны — **[Needs confirmation]** (p0281).
- Pod имеет IP сети кластера, не гарантированно постоянный (p0285–p0287); Service DNS в книге имеет вид `nginx.default.svc.cluster.local` (p0291–p0296). Суффикс `cluster.local` назван типичным, не проверен в конкретном кластере.
- В author demo `nginx` с `run=nginx` соответствует Service `selector: run=nginx`, `Endpoints` в `kubectl describe svc` показывают IP:port (p0292–p0293).
- Типы: **ClusterIP** для внутренних клиентов (p0306–p0310), **NodePort** через порт узла (p0299–p0305), **LoadBalancer** через интеграцию с облаком (p0312–p0314), **ExternalName** для DNS внешнего адреса (p0314–p0316). **Headless**: `clusterIP: None`, нет единого Service IP и встроенного VIP-балансирования (p0311–p0312).
- `readinessProbe` влияет на допуск в обслуживаемый сервисом пул (p0316–p0318), `livenessProbe` на восстановление неработоспособного контейнера (p0319–p0322), `startupProbe` на ожидание медленного старта (p0323).

## Read-only checks

```bash
kubectl get po new-nginx-pod -o wide
kubectl get po,svc nginx
kubectl get po nginx --show-labels
kubectl describe svc nginx
kubectl get po k8sutils
kubectl exec -it k8sutils -- nslookup nginx.default.svc.cluster.local
kubectl exec -it k8sutils -- curl nginx.default.svc.cluster.local
kubectl get service nodeport-whoami
kubectl describe service nodeport-whoami
kubectl get svc
kubectl describe svc/nginx-clusterip
kubectl get pods/nginx-clusterip --show-labels
```

RAG p0285, p0292–p0296, p0300, p0304, p0308–p0309. `kubectl exec` запускает процесс внутри отладочного контейнера: в приведённых вызовах `nslookup/curl` служат сетевой диагностике, но имеют outbound network effect, не считать чисто локальным чтением; для неизвестной среды требуется разрешение. Для получения контекста и namespace книга здесь не даёт отдельной проверенной команды: **[Needs confirmation]**.

## Interpretation

- **Service без подходящего selector/endpoints**: `kubectl describe svc` следует проверять вместе с Pod labels, `Endpoints` и readiness (p0293, p0297, p0317); наличие ClusterIP и DNS **не доказывает**, что есть готовый backend.
- `kubectl exec k8sutils -- nslookup ...`: имя должно разрешиться в Service IP по примеру p0295; `curl ...` проверяет прикладной ответ Nginx по p0296. Значения IP в книге демонстрационные.
- **NodePort** `30001`: порт узла `nodePort`, внутри Service `port: 80`, в Pod `targetPort: 80`; типичный диапазон `30000–32767` указан для стандартной настройки (p0300–p0302).
- **LoadBalancer**: provisioning асинхронный, status выставляет провайдер, возможны дополнительные затраты; доступность зависит от платформы (p0312–p0314). Проверенный CLI polling конкретного провайдера не дан.
- **Headless** возвращает endpoint-информацию через DNS вместо единого VIP (p0311–p0312); какое DNS поведение в целевом кластере — [Needs confirmation].
- **Readiness**: endpoint не получает трафик, пока контейнер не готов. Пример `httpGet.path: /ready` требует существования реального handler в приложении (p0317–p0318).
- **Liveness**: пример Nginx `/healthcheck` намеренно показывает вероятный HTTP 404 и неуспех (p0321). Он **не является здоровым production-манифестом**.
- **Startup**: `failureThreshold: 30` × `periodSeconds: 10` — увеличенное окно запуска в книге (p0323), но `/healthz` в показанном Nginx не подтверждён.

## Next action

Сначала подтвердить namespace, права, CNI и допустимую сетевую экспозицию. Затем проверить `Service selector`, метки, endpoints, DNS внутри кластера, HTTP-ответы, готовность. **Не публиковать NodePort/LoadBalancer** без оценки доступности извне, firewall и стоимости. Для медленного старта подобрать health endpoints и время по реальному приложению — точные значения [Needs confirmation].

## Modifying action

Source exercise commands (p0285, p0292, p0295, p0299–p0300, p0308, p0311):
```bash
kubectl apply -f new-nginx-pod.yaml
kubectl run nginx --image nginx --expose=true --port=80
kubectl apply -f k8sutils.yaml
kubectl run whoami1 --image=containous/whoami --port 80 --labels="app=whoami"
kubectl run whoami2 --image=containous/whoami --port 80 --labels="app=whoami"
kubectl apply -f nodeport-whoami.yaml
kubectl run nginx-clusterip --image nginx --expose=true --port=80
```

**Эффект:** создание Pod/Service, запуск образов, изменение адресации/сетевого доступа. `NodePort` может открывать порт на узлах. **Риски:** выставление приложения наружу, ресурсная нагрузка, подмена target selector, устаревшие демонстрационные образы, влияние на соседние сервисы. **Verification:** `kubectl get svc`, `kubectl describe service`, `get pods --show-labels`, `curl/nslookup` из учебного debug Pod. **Rollback:** создание/удаление сервисов раздельно; восстановление точной доступности [Needs confirmation].

`kubectl port-forward service/nginx 8080:80` (p0294) открывает локальный сокет; остановка Ctrl+C, **не считать production Service**.

**Destructive operations** p0286, p0305, p0311:
```bash
kubectl delete -f new-nginx-pod.yaml
kubectl delete svc/nodeport-whoami
kubectl delete svc nginx-clusterip
```
Pod deletion прекращает экземпляр и может сменить IP; Service deletion разрушает точку входа, но не удаляет Pod. Для удаления production объектов полный rollback [Needs confirmation].

## Verification / acceptance

1. Pod `Running` и IP из `kubectl get po ... -o wide` (p0285–p0286).
2. Мета `run=nginx` ↔ `Selector: run=nginx`; `Endpoints: <ip>:80` в `describe svc` (p0293).
3. DNS разрешается из k8sutils, `curl` даёт ожидаемый Nginx HTML (p0295–p0296).
4. Для NodePort `get service nodeport-whoami` демонстрирует `80:30001/TCP`, `describe` показывает два endpoints (p0300, p0304).
5. Для ClusterIP `kubectl exec k8sutils -- curl nginx-clusterip.default.svc.cluster.local` получает страницу Nginx (p0309–p0310).
6. Если настроены probes, принять endpoint в трафик **только после Readiness**, контролировать события отказов и риск restart loop от Liveness (p0317–p0323). Нет source-confirmed полного production check-list и SLO — [Needs confirmation].

## Rollback / source boundary

Прекратить `port-forward` через Ctrl+C (p0294); удаление Service исключает сетевую точку доступа, не удаляя backend Pod (p0305, p0311). Повторное создание Service может изменить ClusterIP и внешний VIP; универсальный безболезненный rollback в главе не доказан. Delete Pod и ошибочные Liveness настройки могут вызвать нарушение работы. Не экстраполировать рисунки и проценты равномерного round-robin на каждый CNI/kube-proxy mode: автор p0290 сам перечисляет режимы с другим распределением. См. [source-findings.md](source-findings.md).
