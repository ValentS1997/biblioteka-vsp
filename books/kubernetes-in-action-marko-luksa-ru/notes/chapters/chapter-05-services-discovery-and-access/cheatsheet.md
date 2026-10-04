# Шпаргалка: Service, Endpoints, discovery и external access

## 1. Базовая модель

~~~text
Client
  ↓
Service: stable IP + port
  ↓
Endpoints: Pod IP:targetPort
  ↓
ready matching Pods
~~~

Service selector не пересылает traffic напрямую. Он помогает сформировать Endpoints.

## 2. Read-only troubleshooting path

| Проверка | Команда/действие из главы | Интерпретация |
|---|---|---|
| Service exists | kubectl get svc | ClusterIP/ports/type |
| Service details | kubectl describe svc <service> | selector + endpoints |
| Endpoints | kubectl get endpoints <service> | реальные backends |
| Test inside cluster | kubectl exec <pod> -- curl -s http://<service-ip> | ClusterIP connectivity |
| Service env vars | kubectl exec <pod> env | discovery variables |
| DNS inside Pod | shell + curl http://<service> | DNS discovery |
| Pod status/readiness | kubectl get po | READY column |
| Direct Pod test | source checklist | отделяет Service problem от app listener |
| Headless DNS | kubectl exec dnsutils nslookup <headless-service> | Pod IP A-records |

Не использовать ping <service> как test Service reachability: source объясняет, что ClusterIP — virtual IP и ping не работает.

## 3. Internal discovery

### Environment variables

При запуске Pod Kubernetes создаёт, например:

~~~text
KUBIA_SERVICE_HOST=<cluster-ip>
KUBIA_SERVICE_PORT=80
~~~

Ограничение: Service должен существовать до запуска client Pod.

### DNS

~~~text
service.namespace.svc.cluster.local
service.namespace
service
~~~

Short name работает внутри того же namespace согласно source example.

## 4. Service types

### ClusterIP

Default. Внутрикластерный stable IP.

### NodePort

~~~text
external client
  ↓ nodeIP:nodePort
node
  ↓
Service
  ↓
Pod
~~~

Один и тот же node port открыт на каждом node.

### LoadBalancer

~~~text
external LB public IP
  ↓
NodePort
  ↓
Service
  ↓
Pod
~~~

Source: LoadBalancer является расширением NodePort.

### ExternalName

DNS CNAME alias к внешнему FQDN. ClusterIP не создаётся.

## 5. Ingress

~~~text
HTTP client
   ↓ host/path
Ingress controller
   ↓
Service
   ↓ Endpoints
Pod
~~~

Преимущество source framing: много HTTP Services через один внешний IP.

TLS может завершаться на Ingress controller; backend остаётся HTTP.

## 6. Readiness

~~~text
Pod labels match Service
        +
readinessProbe succeeds
        ↓
Pod included in Endpoints
        ↓
receives Service traffic
~~~

Readiness failure:
- container не restart;
- Pod удаляется из Endpoints;
- traffic к нему не направляется.

## 7. Headless Service

~~~text
clusterIP: None
~~~

DNS возвращает Pod IPs, а не Service ClusterIP.

Используется, когда клиенту нужно обнаружить individual Pods.

## 8. Troubleshooting checklist

В порядке главы:

1. ClusterIP тестируется изнутри cluster.
2. Не использовать ping Service IP.
3. Проверить readiness.
4. Проверить kubectl get endpoints.
5. Если DNS name не работает — попробовать ClusterIP.
6. Проверить Service port, а не путать его с targetPort.
7. Проверить прямое подключение к Pod IP.
8. Если Pod IP не отвечает — проверить, слушает ли приложение не только localhost.

## 9. State-changing / risk actions

### Recreate Pods for service environment variables

~~~bash
kubectl delete po --all
~~~

Destructive. В source scenario ReplicationController должен создать replacements.

### Firewall for NodePort

~~~bash
gcloud compute firewall-rules create kubia-svc-rule --allow=tcp:30123
~~~

State-changing infrastructure action.

Source output показывает SRC_RANGES=0.0.0.0/0.

Risk: публичное открытие node port.

Rollback command: [Needs confirmation] — chapter не приводит delete firewall rule.

### Enable Minikube Ingress addon

~~~bash
minikube addons enable ingress
~~~

State-changing local cluster addon.

Verification:

~~~bash
kubectl get po --all-namespaces
~~~

### TLS Secret

~~~bash
kubectl create secret tls tls-secret --cert=tls.cert --key=tls.key
~~~

State-changing; Secret содержит private key material.

Не публиковать tls.key.

## 10. Acceptance model

Service path считается работоспособным, когда:

- selector выбирает ожидаемые Pods;
- ready Pods присутствуют в Endpoints;
- Service port соответствует ожидаемому client port;
- targetPort ведёт на слушающий application port;
- DNS/ClusterIP разрешаются в правильном scope;
- external exposure имеет ожидаемый NodePort/LB/Ingress endpoint;
- readiness исключает неготовые Pods.
