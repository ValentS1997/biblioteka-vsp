# Шпаргалка: metadata и Kubernetes API из приложения

## 1. Downward API

### Через environment variables

fieldRef:
- metadata.name
- metadata.namespace
- status.podIP
- spec.nodeName
- spec.serviceAccountName

resourceFieldRef:
- requests.cpu
- limits.memory
- divisor задаёт единицу результата.

Verification:

~~~bash
kubectl exec downward env
~~~

### Через downwardAPI volume

Дополнительно доступны:
- metadata.labels
- metadata.annotations

Read-only:

~~~bash
kubectl exec downward -- ls -lL /etc/downward
kubectl exec downward -- cat /etc/downward/labels
kubectl exec downward -- cat /etc/downward/annotations
~~~

Source behavior:
- labels/annotations могут обновляться;
- files volume получают новые значения;
- env variables после запуска process не обновляются.

## 2. fieldRef vs resourceFieldRef

~~~text
Pod metadata/status/spec field
  → fieldRef

Container CPU/memory request/limit
  → resourceFieldRef
  → divisor
~~~

В downwardAPI volume resourceFieldRef требует containerName.

## 3. Когда Downward API недостаточно

Если нужны:
- другие Pods;
- Jobs;
- другие resources;
- latest cluster state;

нужен API server.

## 4. Local REST exploration

~~~bash
kubectl cluster-info
kubectl proxy
curl http://localhost:8001
curl http://localhost:8001/apis/batch
curl http://localhost:8001/apis/batch/v1
curl http://localhost:8001/apis/batch/v1/jobs
curl http://localhost:8001/apis/batch/v1/namespaces/default/jobs/my-job
~~~

Compare with:

~~~bash
kubectl get job my-job -o json
~~~

kubectl proxy handles authentication and server verification.

## 5. Direct API access from Pod

Discover API service:

~~~bash
kubectl get svc
~~~

Inside Pod:

~~~bash
env | grep KUBERNETES_SERVICE
curl https://kubernetes
~~~

First direct curl fails certificate verification in source demo.

Service-account volume contains:

~~~text
ca.crt
namespace
token
~~~

## 6. Verify API server certificate

Source pattern:

~~~bash
curl --cacert /var/run/secrets/kubernetes.io/serviceaccount/ca.crt https://kubernetes
~~~

Or source sets:

~~~bash
export CURL_CA_BUNDLE=/var/run/secrets/kubernetes.io/serviceaccount/ca.crt
~~~

Then:

~~~bash
curl https://kubernetes
~~~

At this point certificate verification works, but authentication is still required.

## 7. Authenticate with bearer token

Source pattern:

~~~bash
TOKEN=$(cat /var/run/secrets/kubernetes.io/serviceaccount/token)
curl -H "Authorization: Bearer $TOKEN" https://kubernetes
~~~

Security:
- TOKEN is credential material;
- do not echo/log/share it.

Namespace:

~~~bash
NS=$(cat /var/run/secrets/kubernetes.io/serviceaccount/namespace)
~~~

Namespace-scoped Pod list:

~~~bash
curl -H "Authorization: Bearer $TOKEN"   https://kubernetes/api/v1/namespaces/$NS/pods
~~~

## 8. Dangerous source RBAC bypass

Source lab command:

~~~bash
kubectl create clusterrolebinding permissive-binding   --clusterrole=cluster-admin   --group=system:serviceaccounts
~~~

CRITICAL RISK:
- grants cluster-admin to all ServiceAccounts;
- source explicitly says never do this in production;
- acceptable only as historical/lab example in this chapter.

Rollback command: [Needs confirmation] — chapter excerpt does not provide it.

## 9. Ambassador pattern

~~~text
main container
  ↓ HTTP localhost:8001
ambassador: kubectl proxy
  ↓ HTTPS + auth + CA verification
Kubernetes API server
~~~

Test:

~~~bash
kubectl exec -it curl-with-ambassador -c main bash
curl localhost:8001
~~~

Advantage:
- app does not handle certificate/token logic.

Cost:
- extra sidecar process/resources.

## 10. Client libraries

Use when API interaction is more complex than a few HTTP calls.

Source lists multiple language clients and shows Fabric8 Java DSL.

## 11. Swagger/OpenAPI

Source endpoints:
- /swaggerapi
- /swagger.json
- /swagger-ui

Minikube source-era enable example:

~~~text
minikube start --extra-config=apiserver.Features.EnableSwaggerUI=true
~~~

Risk: interactive UI can create/patch/delete resources.

## Acceptance model

Application should know:
- whether it only needs own metadata or cluster-wide state;
- which fields come from Downward API;
- whether metadata must update during Pod lifetime;
- how API server identity is verified;
- which credential authenticates request;
- exact namespace scope;
- RBAC permissions;
- whether direct API client, ambassador, or client library is appropriate.
