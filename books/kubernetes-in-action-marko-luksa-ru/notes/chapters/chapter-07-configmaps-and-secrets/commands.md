# Команды главы 7

Source policy: RAG-only. Commands separated by read-only/state-changing/security-sensitive behavior.

## Docker command/args demo

~~~bash
docker run <image>
docker run <image> <arguments>
~~~

Inspect process:

~~~bash
docker exec <container-id> ps x
docker exec -it <container-id> ps x
~~~

Build/push source image:

~~~bash
docker build -t docker.io/luksa/fortune:args .
docker push docker.io/luksa/fortune:args
~~~

Local tests:

~~~bash
docker run -it docker.io/luksa/fortune:args
docker run -it docker.io/luksa/fortune:args 15
~~~

Build/push are state-changing. Push changes remote registry state.

## ConfigMap creation

Literal:

~~~bash
kubectl create configmap fortune-config --from-literal=sleep-interval=25
~~~

Empty ConfigMap:

~~~bash
kubectl create configmap myconfigmap
~~~

From manifest:

~~~bash
kubectl create -f fortune-config.yaml
~~~

From file:

~~~bash
kubectl create configmap my-config --from-file=config-file.conf
kubectl create configmap my-config --from-file=customkey=config-file.conf
~~~

From directory:

~~~bash
kubectl create configmap my-config --from-file=/path/to/dir
~~~

All are state-changing.

Read-only:

~~~bash
kubectl get configmap fortune-config -o yaml
~~~

## Delete ConfigMap

Source explicitly uses:

~~~bash
kubectl delete configmap fortune-config
~~~

DESTRUCTIVE for the resource. Pods depending on it may be affected according to consumption method.

## ConfigMap volume verification

~~~bash
kubectl port-forward fortune-configmap-volume 8080:80 &
curl -H "Accept-Encoding: gzip" -I localhost:8080
kubectl exec fortune-configmap-volume -c web-server -- ls /etc/nginx/conf.d
~~~

Port-forward/workload-generating; ls is read-only inside container.

## ConfigMap update

~~~bash
kubectl edit configmap fortune-config
~~~

State-changing.

Verify mounted file:

~~~bash
kubectl exec fortune-configmap-volume -c web-server -- cat /etc/nginx/conf.d/my-nginx-config.conf
~~~

Reload Nginx:

~~~bash
kubectl exec fortune-configmap-volume -c web-server -- nginx -s reload
~~~

State-changing inside running container/process.

Inspect atomic symlink layout:

~~~bash
kubectl exec -it fortune-configmap-volume -c web-server -- ls -lA /etc/nginx/conf.d
~~~

Read-only.

## Secret discovery — read-only

~~~bash
kubectl get secrets
kubectl describe secrets
kubectl exec mypod -- ls /var/run/secrets/kubernetes.io/serviceaccount/
~~~

Security note: describe/get metadata is less sensitive than printing Secret data, but access should still respect RBAC.

## Generate TLS material

~~~bash
openssl genrsa -out https.key 2048
openssl req -new -x509 -key https.key -out https.cert -days 3650 -subj /CN=www.kubia-example.com
echo bar > foo
~~~

State-changing local filesystem.

SECURITY:
- https.key is private-key material;
- do not commit/share it.

## Create generic Secret

Source command normalized only for line formatting:

~~~bash
kubectl create secret generic fortune-https   --from-file=https.key   --from-file=https.cert   --from-file=foo
~~~

State-changing / secret-bearing.

## Inspect Secret YAML

~~~bash
kubectl get secret fortune-https -o yaml
~~~

SECURITY-SENSITIVE READ:
- output exposes Base64-encoded secret contents;
- Base64 is reversible encoding;
- do not publish output.

## Edit ConfigMap for HTTPS

~~~bash
kubectl edit configmap fortune-config
~~~

State-changing.

## Test HTTPS Pod

~~~bash
kubectl port-forward fortune-https 8443:443 &
curl https://localhost:8443 -k
curl https://localhost:8443 -k -v
~~~

Source self-signed test only.

Risk:
- -k disables certificate verification;
- not a secure production verification pattern.

## Verify Secret volume uses tmpfs

~~~bash
kubectl exec fortune-https -c web-server -- mount | grep certs
~~~

Read-only.

## Secret through env variable

Source manifest relation:

~~~text
valueFrom:
  secretKeyRef:
    name: fortune-https
    key: foo
~~~

Source recommends Secret volume over env for sensitive values.

## Registry Secret

Source command normalized with placeholders:

~~~bash
kubectl create secret docker-registry mydockerhubsecret   --docker-username=<username>   --docker-password=<password>   --docker-email=<email>
~~~

HIGH SENSITIVITY.

Do not substitute real credentials into shared artifacts.

Potential exposure:
- shell history;
- process listing depending on environment;
- logs/screenshots.

Pod relation:

~~~text
imagePullSecrets:
- name: mydockerhubsecret
~~~

Exact Pod create command for private-pod is not explicitly present in retrieved RAG: not reconstructed.

## Safety summary

| Operation | Class |
|---|---|
| kubectl get configmap | read-only |
| kubectl get secret ... -o yaml | secret-exposing read |
| kubectl create/edit/delete configmap | state-changing |
| kubectl create secret | secret-bearing state change |
| openssl genrsa | creates private key |
| kubectl exec ... nginx -s reload | process state change |
| docker push | remote state change |
| docker-registry secret command | credential-sensitive |
