# Команды главы 8

Source policy: RAG-only. Read-only, local proxy, credential-sensitive and privileged operations are separated.

## Downward API — read-only verification

Environment:

~~~bash
kubectl exec downward env
~~~

Volume files:

~~~bash
kubectl exec downward -- ls -lL /etc/downward
kubectl exec downward -- cat /etc/downward/labels
kubectl exec downward -- cat /etc/downward/annotations
~~~

Read-only inside container.

## Local API discovery

~~~bash
kubectl cluster-info
~~~

Read-only. Source uses output to find API server URL.

Direct source test:

~~~bash
curl https://<api-server>:<port> -k
~~~

UNSAFE VERIFICATION PATH:
- -k disables TLS certificate verification;
- source demonstrates it before introducing kubectl proxy;
- do not treat as secure production pattern.

## kubectl proxy

~~~bash
kubectl proxy
~~~

Starts local proxy process, source default endpoint localhost:8001.

Requests:

~~~bash
curl http://localhost:8001
curl http://localhost:8001/apis/batch
curl http://localhost:8001/apis/batch/v1
curl http://localhost:8001/apis/batch/v1/jobs
curl http://localhost:8001/apis/batch/v1/namespaces/default/jobs/my-job
~~~

Compare:

~~~bash
kubectl get job my-job -o json
~~~

## Enter API test Pod

~~~bash
kubectl exec -it curl bash
~~~

Interactive shell surface.

Read Service discovery:

~~~bash
kubectl get svc
~~~

Inside Pod:

~~~bash
env | grep KUBERNETES_SERVICE
curl https://kubernetes
~~~

Expected source result: certificate verification failure before CA is supplied.

## ServiceAccount volume — sensitive read surface

List filenames:

~~~bash
ls /var/run/secrets/kubernetes.io/serviceaccount/
~~~

Expected source filenames:
- ca.crt
- namespace
- token

Do not print token content to logs.

## Verify server using CA

~~~bash
curl --cacert /var/run/secrets/kubernetes.io/serviceaccount/ca.crt https://kubernetes
~~~

Source also configures:

~~~bash
export CURL_CA_BUNDLE=/var/run/secrets/kubernetes.io/serviceaccount/ca.crt
curl https://kubernetes
~~~

export changes shell process environment only.

## Authenticate with ServiceAccount token

~~~bash
TOKEN=$(cat /var/run/secrets/kubernetes.io/serviceaccount/token)
curl -H "Authorization: Bearer $TOKEN" https://kubernetes
~~~

CREDENTIAL-SENSITIVE:
- TOKEN is authentication credential;
- avoid echo, history expansion, logs and screenshots containing token value.

## Namespace-scoped API request

~~~bash
NS=$(cat /var/run/secrets/kubernetes.io/serviceaccount/namespace)
curl -H "Authorization: Bearer $TOKEN"   https://kubernetes/api/v1/namespaces/$NS/pods
~~~

Read-only API request if identity has permission.

## Dangerous lab-only RBAC bypass

Source command:

~~~bash
kubectl create clusterrolebinding permissive-binding   --clusterrole=cluster-admin   --group=system:serviceaccounts
~~~

CRITICAL PRIVILEGE ESCALATION.

Source effect:
- all ServiceAccounts receive cluster-admin;
- effectively all Pods can act as cluster admin through their ServiceAccount.

Source warning:
- dangerous;
- never use in production;
- shown only to bypass RBAC for chapter testing.

Rollback: [Needs confirmation]. The chapter does not provide a delete command.

## Ambassador Pod

Enter main container:

~~~bash
kubectl exec -it curl-with-ambassador -c main bash
~~~

Then:

~~~bash
curl localhost:8001
~~~

Main container uses plain HTTP to loopback; ambassador kubectl proxy handles upstream HTTPS/auth/server verification.

## Swagger UI source-era enablement

Source Minikube example:

~~~text
minikube start --extra-config=apiserver.Features.EnableSwaggerUI=true
~~~

State-changing cluster startup/configuration.

Source UI endpoint:

~~~text
http(s)://<api-server>:<port>/swagger-ui
~~~

HIGH IMPACT INTERACTIVE SURFACE:
- source says UI can submit JSON manifests;
- patch resources;
- delete resources.

Use read-only exploration unless intentional state change is required.

## Risk matrix

| Operation | Class |
|---|---|
| kubectl exec ... env/ls/cat metadata files | read-only |
| kubectl cluster-info / get svc / get job | read-only |
| kubectl proxy | local process/network listener |
| curl API GET | read-only if GET and authorized |
| reading service-account token | credential-sensitive |
| Bearer request | authenticated API operation |
| permissive clusterrolebinding | critical cluster-wide privilege change |
| Swagger UI | can become state-changing/destructive |
