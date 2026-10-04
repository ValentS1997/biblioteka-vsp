# Команды главы 5

Source policy: команды и поведение только из RAG главы 5. Read-only, workload-generating, state-changing и security-sensitive действия разделены.

## Service inspection — read-only

~~~bash
kubectl get svc
kubectl describe svc kubia
kubectl get endpoints kubia
~~~

kubectl describe svc показывает selector и текущие Endpoints.

## Test ClusterIP from inside cluster

Source example normalized:

~~~bash
kubectl exec <pod-name> -- curl -s http://<cluster-ip>
~~~

Workload-generating HTTP request внутри Pod.

Двойное тире -- source объясняет как конец параметров kubectl; параметры после него относятся к command внутри container.

## Session affinity

Source manifest fragment:

~~~yaml
apiVersion: v1
kind: Service
spec:
  sessionAffinity: ClientIP
~~~

Source-supported values: None и ClientIP.

Exact create command line для дополнительного exercise Service в RAG не приведена.

## Multi-port Service

Source conceptual manifest:

~~~text
ports:
- name: http
  port: 80
  targetPort: 8080
- name: https
  port: 443
  targetPort: 8443
~~~

RAG list markers местами извлечены типографски; fragment не объявляется validated copy-paste YAML.

## Recreate Pods to refresh Service env vars

~~~bash
kubectl delete po --all
~~~

DESTRUCTIVE / multi-resource.

Source scenario: Pods управляются ReplicationController и будут пересозданы.

Verification после replacement:

~~~bash
kubectl exec <pod-name> env
~~~

Read-only command execution. Проверяются *_SERVICE_HOST и *_SERVICE_PORT.

## Interactive shell / DNS discovery

~~~bash
kubectl exec -it <pod-name> bash
~~~

Interactive access; shell позволяет modifications, хотя source intent — inspection.

Внутри Pod source использует:

~~~bash
curl http://kubia.default.svc.cluster.local
curl http://kubia.default
curl http://kubia
cat /etc/resolv.conf
~~~

### Не использовать ping как Service check

Source demonstration:

~~~bash
ping kubia
~~~

Expected source result: DNS name resolves, но ICMP replies отсутствуют. Это не означает failure Service.

## External Service via Endpoints

Read-only:

~~~bash
kubectl describe svc kubia
kubectl get endpoints kubia
~~~

Source manifests описывают:
- Service без selector;
- Endpoints с тем же metadata.name;
- external IP/port pairs.

Exact create command lines для этих файлов в retrieved RAG не присутствуют; не реконструируются.

## ExternalName

Source resource:

~~~text
type: ExternalName
externalName: someapi.somecompany.com
~~~

DNS CNAME path; ClusterIP отсутствует.

## NodePort — read-only

~~~bash
kubectl get svc kubia-nodeport
~~~

Source example: nodePort 30123.

Получить external node IPs:

~~~bash
kubectl get nodes -o jsonpath='{.items[*].status.addresses[?(@.type=="ExternalIP")].address}'
~~~

Test:

~~~bash
curl http://<node-external-ip>:30123
~~~

For Minikube source suggests:

~~~text
minikube service <service-name> [-n <namespace>]
~~~

## NodePort firewall — state-changing / exposure risk

~~~bash
gcloud compute firewall-rules create kubia-svc-rule --allow=tcp:30123
~~~

HIGH IMPACT networking change.

Source output shows:
- source range: 0.0.0.0/0;
- protocol/port: tcp:30123.

Это открывает доступ широкой внешней аудитории в source lab scenario.

Verification: external curl to node IP:30123.

Rollback: [Needs confirmation] — delete rule command отсутствует в главе.

## LoadBalancer

Read-only:

~~~bash
kubectl get svc kubia-loadbalancer
~~~

Test:

~~~bash
curl http://<load-balancer-ip>
~~~

Source notes:
- provisioning может занять время;
- LoadBalancer extends NodePort;
- Minikube в source-era example не поддерживает provisioning external LB.

## externalTrafficPolicy

Source fragment:

~~~text
spec:
  externalTrafficPolicy: Local
~~~

Effect per source:
- external traffic направляется только local Pods на receiving node;
- avoids extra hop;
- preserves original client IP;
- может нарушить равномерность load distribution;
- connection fails/hangs if node has no local matching Pod.

## Minikube Ingress controller

Read-only:

~~~bash
minikube addons list
~~~

State-changing:

~~~bash
minikube addons enable ingress
~~~

Verification:

~~~bash
kubectl get po --all-namespaces
~~~

Expected source example: ingress controller Pod appears.

## Ingress — read-only

~~~bash
kubectl get ingresses
~~~

Получить ADDRESS controller.

Source instructs map kubia.example.com to Ingress IP via DNS or hosts file; exact shell edit command is not given.

Test:

~~~bash
curl http://kubia.example.com
~~~

## TLS material — security-sensitive

Generate private key:

~~~bash
openssl genrsa -out tls.key 2048
~~~

Generate self-signed certificate:

~~~bash
openssl req -new -x509 -key tls.key -out tls.cert -days 360 -subj /CN=kubia.example.com
~~~

Security boundary:
- tls.key is secret private-key material;
- do not commit/share it.

Create Kubernetes TLS Secret:

~~~bash
kubectl create secret tls tls-secret --cert=tls.cert --key=tls.key
~~~

State-changing / secret-bearing action.

Source also shows CSR approval:

~~~bash
kubectl certificate approve <name-of-csr>
~~~

Privileged state-changing action; only meaningful when certificate signer component exists.

## Update Ingress

~~~bash
kubectl apply -f kubia-ingress-tls.yaml
~~~

State-changing.

HTTPS test from source:

~~~bash
curl -k -v https://kubia.example.com/kubia
~~~

Security note: -k disables certificate verification; suitable only for the source self-signed test scenario, not a secure verification pattern.

## Readiness probe

Edit ReplicationController:

~~~bash
kubectl edit rc kubia
~~~

State-changing.

Source readiness probe runs:

~~~text
ls /var/ready
~~~

Observe:

~~~bash
kubectl get po
kubectl get po <pod-name>
~~~

Make one Pod ready in source demo:

~~~bash
kubectl exec <pod-name> -- touch /var/ready
~~~

State-changing inside container.

Verification after probe interval:

~~~bash
kubectl get endpoints kubia-loadbalancer
~~~

Only ready Pods should be listed as endpoints.

HTTP verification:

~~~bash
curl http://<load-balancer-ip>
~~~

Repeated requests should hit only ready endpoint(s).

## Headless Service

Source fragment:

~~~text
clusterIP: None
~~~

After generic kubectl create, source says verify with kubectl get and kubectl describe; exact create/get service command line is not present in the retrieved excerpt.

Make additional Pods ready:

~~~bash
kubectl exec <pod-name> -- touch /var/ready
~~~

## DNS utility Pod

Source-era command:

~~~bash
kubectl run dnsutils --image=tutum/dnsutils --generator=run-pod/v1 --command -- sleep infinity
~~~

State-changing: creates unmanaged Pod directly.

DNS query for Headless Service:

~~~bash
kubectl exec dnsutils nslookup kubia-headless
~~~

Expected: multiple Pod IPs for ready endpoints.

Confirm Pod IPs:

~~~bash
kubectl get pods -o wide
~~~

Query normal Service:

~~~bash
kubectl exec dnsutils nslookup kubia
~~~

Expected: one ClusterIP.

## Source-era unready endpoint discovery

Source annotation:

~~~text
service.alpha.kubernetes.io/tolerate-unready-endpoints: "true"
~~~

Source explicitly marks it alpha and says a newer field publishNotReadyAddresses is intended to replace it. No modernization is performed here.

## Troubleshooting sequence

Source checklist:

1. ClusterIP must be tested from inside cluster.
2. Do not use ping Service IP.
3. Verify readiness succeeds.
4. Inspect Endpoints:
   ~~~bash
   kubectl get endpoints <service>
   ~~~
5. If DNS name fails, try ClusterIP.
6. Use Service port, not backend targetPort, from client side.
7. Test Pod IP directly.
8. If Pod IP itself fails, verify application is not bound only to localhost.

## Risk matrix

| Action | Class |
|---|---|
| kubectl get/describe | read-only |
| kubectl exec ... curl/env/nslookup | diagnostic/workload-generating |
| interactive kubectl exec -it ... bash | privileged interactive surface |
| kubectl delete po --all | destructive multi-resource |
| gcloud compute firewall-rules create ... | infrastructure/network exposure |
| minikube addons enable ingress | cluster state change |
| kubectl create secret tls ... | secret-bearing state change |
| kubectl apply -f ... | resource state change |
| kubectl exec ... touch /var/ready | container state change |
