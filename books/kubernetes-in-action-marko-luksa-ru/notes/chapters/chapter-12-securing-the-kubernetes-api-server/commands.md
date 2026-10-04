# Команды главы 12

Source policy: RAG-only. Security-sensitive and privilege-changing operations are explicitly separated.

## ServiceAccount inspection

~~~bash
kubectl get sa
kubectl describe sa foo
~~~

Read-only.

## Create ServiceAccount

~~~bash
kubectl create serviceaccount foo
~~~

STATE-CHANGING.

## Inspect ServiceAccount token Secret

Source:

~~~bash
kubectl describe secret <serviceaccount-token-secret>
~~~

SECURITY-SENSITIVE READ.

Do not copy or publish the token value.

## Inspect token mounted in Pod

Source pattern:

~~~bash
kubectl exec -it curl-custom-sa -c main   cat /var/run/secrets/kubernetes.io/serviceaccount/token
~~~

CREDENTIAL-EXPOSING READ.

Avoid in shared terminals, logs, screenshots or CI output.

## API request through ambassador

~~~bash
kubectl exec -it curl-custom-sa -c main   curl localhost:8001/api/v1/pods
~~~

Authenticated API read through source-era proxy sidecar.

## Remove permissive RBAC bypass from chapter 8

~~~bash
kubectl delete clusterrolebinding permissive-binding
~~~

STATE-CHANGING authorization hardening.

Effect:
removes prior source lab binding granting broad permissions.

## Create RBAC lab namespaces and workloads

~~~bash
kubectl create ns foo
kubectl run test --image=luksa/kubectl-proxy -n foo

kubectl create ns bar
kubectl run test --image=luksa/kubectl-proxy -n bar
~~~

STATE-CHANGING.

Source-era kubectl run semantics preserved.

## Enter test workload

~~~bash
kubectl get po -n foo
kubectl exec -it <foo-test-pod> -n foo sh
~~~

First read-only, second interactive exec.

## Verify denied Service access

Inside foo test Pod:

~~~bash
curl localhost:8001/api/v1/namespaces/foo/services
~~~

Expected before RBAC grant:
Forbidden/cannot list services.

## Create Role from manifest

~~~bash
kubectl create -f service-reader.yaml -n foo
~~~

STATE-CHANGING.

## Create equivalent Role imperatively

~~~bash
kubectl create role service-reader   --verb=get --verb=list   --resource=services   -n bar
~~~

STATE-CHANGING.

## Bind Role to ServiceAccount

~~~bash
kubectl create rolebinding test   --role=service-reader   --serviceaccount=foo:default   -n foo
~~~

STATE-CHANGING authorization grant.

## Inspect/edit RoleBinding

~~~bash
kubectl get rolebinding test -n foo -o yaml
kubectl edit rolebinding test -n foo
~~~

First read-only.

Second STATE-CHANGING and may grant access to additional subjects.

Source exercise adds bar:default as another subject to RoleBinding in foo.

## GKE source admin escalation

Source command:

~~~bash
kubectl create clusterrolebinding cluster-admin-binding   --clusterrole=cluster-admin   --user=<admin-user>
~~~

CRITICAL PRIVILEGE ESCALATION.

Use only when intentionally granting full cluster administration in controlled lab/admin context.

Do not normalize this into a routine troubleshooting step.

## ClusterRole for PersistentVolumes

~~~bash
kubectl create clusterrole pv-reader   --verb=get,list   --resource=persistentvolumes
~~~

STATE-CHANGING.

Read-only inspect:

~~~bash
kubectl get clusterrole pv-reader -o yaml
~~~

## Demonstrate wrong binding scope

~~~bash
kubectl create rolebinding pv-test   --clusterrole=pv-reader   --serviceaccount=foo:default   -n foo
~~~

STATE-CHANGING but insufficient for cluster-scoped PersistentVolumes.

Verify denial inside test Pod:

~~~bash
curl localhost:8001/api/v1/persistentvolumes
~~~

Expected:
cannot list persistentvolumes at cluster scope.

## Replace with ClusterRoleBinding

~~~bash
kubectl delete rolebinding pv-test

kubectl create clusterrolebinding pv-test   --clusterrole=pv-reader   --serviceaccount=foo:default
~~~

Both STATE-CHANGING.

Second command grants cluster-scoped PV read permission to foo:default.

## Inspect default discovery role/binding

~~~bash
kubectl get clusterrole system:discovery -o yaml
kubectl get clusterrolebinding system:discovery -o yaml
~~~

Read-only.

## Source unauthenticated discovery test

~~~bash
curl https://$(minikube ip):8443/api -k
~~~

UNSAFE TLS VERIFICATION:
-k disables certificate verification.

Source-era demonstration only.

## ClusterRole view — cluster-wide binding

~~~bash
kubectl create clusterrolebinding view-test   --clusterrole=view   --serviceaccount=foo:default
~~~

STATE-CHANGING.

Effect:
view permissions for namespaced resources across namespaces.

## Replace with namespaced RoleBinding

~~~bash
kubectl delete clusterrolebinding view-test

kubectl create rolebinding view-test   --clusterrole=view   --serviceaccount=foo:default   -n foo
~~~

STATE-CHANGING.

Effect:
same ClusterRole permissions restricted to namespace foo.

## Inspect built-in roles/bindings

~~~bash
kubectl get clusterrolebindings
kubectl get clusterroles
~~~

Read-only.

Source highlights:
- view;
- edit;
- admin;
- cluster-admin.

## Risk matrix

| Operation | Class |
|---|---|
| get/describe SA/RBAC | read-only |
| describe token Secret | credential-sensitive read |
| cat mounted SA token | credential-exposing read |
| create ServiceAccount | state-changing |
| create/edit Role/RoleBinding | authorization state change |
| create ClusterRole/ClusterRoleBinding | cluster authorization state change |
| cluster-admin binding | critical privilege escalation |
| delete binding | authorization state change |
| curl -k | insecure TLS verification |
