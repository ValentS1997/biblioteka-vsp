# Ответ к упражнению главы 12

Это RAG-grounded walkthrough по practical RBAC exercise. Это не официальный издательский answer key.

## 1. Исходное состояние

После запуска test workload в foo запрос:

~~~bash
curl localhost:8001/api/v1/namespaces/foo/services
~~~

должен быть запрещён для identity:

~~~text
system:serviceaccount:foo:default
~~~

Это подтверждает, что default ServiceAccount не получает право list Services автоматически.

## 2. Role + RoleBinding

Role service-reader определяет WHAT:

~~~text
apiGroups: [""]
verbs: ["get", "list"]
resources: ["services"]
~~~

RoleBinding test определяет WHO + WHERE:
- subject: foo:default;
- namespace: foo.

Result:
- foo:default получает get/list Services в foo;
- сама Role не предоставляет permissions до появления binding.

Source also shows that RoleBinding in foo may contain subject bar:default. В этом случае bar workload получает указанные permissions на resources namespace foo.

## 3. ClusterRole + RoleBinding для cluster-scoped resource не работает

ClusterRole pv-reader:

~~~bash
kubectl create clusterrole pv-reader   --verb=get,list   --resource=persistentvolumes
~~~

RoleBinding:

~~~bash
kubectl create rolebinding pv-test   --clusterrole=pv-reader   --serviceaccount=foo:default   -n foo
~~~

не даёт доступ к PersistentVolumes.

Reason:
RoleBinding scope = namespace foo, а PersistentVolume — cluster-scoped resource.

Expected request remains denied:

~~~bash
curl localhost:8001/api/v1/persistentvolumes
~~~

## 4. ClusterRole + ClusterRoleBinding

После удаления namespaced binding:

~~~bash
kubectl delete rolebinding pv-test
~~~

source creates:

~~~bash
kubectl create clusterrolebinding pv-test   --clusterrole=pv-reader   --serviceaccount=foo:default
~~~

Теперь foo:default получает get/list PersistentVolumes at cluster scope.

## 5. ClusterRole view + ClusterRoleBinding

Source creates:

~~~bash
kubectl create clusterrolebinding view-test   --clusterrole=view   --serviceaccount=foo:default
~~~

Effect:
foo:default получает permissions ClusterRole view across namespaces.

Source verifies Pod list access:
- namespace foo;
- namespace bar;
- cluster-wide.

## 6. ClusterRole view + RoleBinding

Source deletes cluster binding:

~~~bash
kubectl delete clusterrolebinding view-test
~~~

Then:

~~~bash
kubectl create rolebinding view-test   --clusterrole=view   --serviceaccount=foo:default   -n foo
~~~

Result:
- Pods in foo: allowed;
- Pods in bar: denied;
- cluster-wide Pod list: denied.

This is the central scope lesson:

~~~text
ClusterRole defines permission set.
Binding type/scope determines where it applies.
~~~

## 7. Security interpretation

Source default view excludes Secrets and RBAC resources because Secret access may expose a more privileged token and enable privilege escalation.

Source recommends:
- separate ServiceAccounts;
- minimal permissions;
- minimal scope;
- avoid granting cluster-admin broadly.

## Acceptance criteria

Confirmed:
- RoleBinding is namespaced.
- ClusterRole is reusable in RoleBinding.
- ClusterRoleBinding expands ClusterRole cluster-wide.
- Cluster-scoped resources require ClusterRoleBinding.
- Authorization follows least-privilege logic.

## Rollback

Source provides several local cleanup commands during the walkthrough, but does not provide one canonical full-lab teardown sequence.

Full teardown: [Needs confirmation].

Do not invent a broad delete command.

## Provenance

- p0436:c01–p0452:c01
