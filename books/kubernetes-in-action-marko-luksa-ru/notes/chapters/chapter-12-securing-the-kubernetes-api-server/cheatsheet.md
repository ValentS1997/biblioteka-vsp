# Шпаргалка: ServiceAccount и RBAC

## 1. Identity flow

~~~text
Pod
  ↓ serviceAccountName
ServiceAccount
  ↓ token
API request
  ↓ authentication
user = system:serviceaccount:<namespace>:<name>
  ↓ authorization
RBAC rules
~~~

## 2. Default ServiceAccount

Каждый namespace имеет default ServiceAccount.

Если Pod не задаёт serviceAccountName:
- используется default ServiceAccount его namespace.

Pod может использовать только ServiceAccount из того же namespace.

## 3. Create custom ServiceAccount

~~~bash
kubectl create serviceaccount foo
kubectl describe sa foo
~~~

State-changing + read-only verification.

Source-era token Secret создаётся автоматически.

## 4. Token handling

Source inspection:

~~~bash
kubectl describe secret <serviceaccount-token-secret>
~~~

SECURITY-SENSITIVE READ.

Secret contains:
- ca.crt;
- namespace;
- JWT token.

Base rule:
do not publish token output.

## 5. Assign ServiceAccount

Pod spec:

~~~text
spec:
  serviceAccountName: foo
~~~

Source says this is fixed at Pod creation.

## 6. ServiceAccount and Secrets

Source-era mount restriction annotation:

~~~text
kubernetes.io/enforce-mountable-secrets="true"
~~~

When enabled:
- workload may mount only Secrets listed by ServiceAccount.

ServiceAccount imagePullSecrets:

~~~text
imagePullSecrets:
- name: my-dockerhub-secret
~~~

These are automatically added to Pods using that ServiceAccount.

## 7. RBAC objects

| Object | Scope | Purpose |
|---|---|---|
| Role | namespace | permissions in one namespace |
| RoleBinding | namespace | bind subject to Role/ClusterRole in one namespace |
| ClusterRole | cluster | reusable permissions; also cluster resources/non-resource URLs |
| ClusterRoleBinding | cluster | bind ClusterRole cluster-wide |

## 8. Core RBAC equation

~~~text
Role / ClusterRole = WHAT can be done
Binding = WHO receives it
Binding scope = WHERE it applies
~~~

## 9. Namespaced access

One namespace:

~~~text
Role + RoleBinding
~~~

or reusable permissions:

~~~text
ClusterRole + RoleBinding
~~~

All namespaces:

~~~text
ClusterRole + ClusterRoleBinding
~~~

## 10. Cluster-scoped resources

For resources such as PersistentVolume:

~~~text
ClusterRole + ClusterRoleBinding
~~~

RoleBinding cannot grant cluster-scoped access even when it references ClusterRole.

## 11. Source lab Role

~~~bash
kubectl create role service-reader   --verb=get --verb=list   --resource=services   -n bar
~~~

Role defines:
- verbs get/list;
- resource services;
- namespace bar.

## 12. Bind ServiceAccount

~~~bash
kubectl create rolebinding test   --role=service-reader   --serviceaccount=foo:default   -n foo
~~~

Effect:
default ServiceAccount in foo receives service-reader permissions in foo.

## 13. Cluster-scoped PV example

~~~bash
kubectl create clusterrole pv-reader   --verb=get,list   --resource=persistentvolumes
~~~

Wrong scope attempt:

~~~bash
kubectl create rolebinding pv-test   --clusterrole=pv-reader   --serviceaccount=foo:default   -n foo
~~~

Expected:
still cannot list PersistentVolumes.

Correct source pattern:

~~~bash
kubectl create clusterrolebinding pv-test   --clusterrole=pv-reader   --serviceaccount=foo:default
~~~

## 14. Default ClusterRoles

### view

Read most namespaced resources.

Source excludes:
- Secrets;
- Roles;
- RoleBindings.

Reason: prevent privilege escalation.

### edit

Can modify ordinary namespaced resources and Secrets.

Does not manage Roles/RoleBindings.

### admin

Broad namespace control including Roles/RoleBindings.

### cluster-admin

Full control.

CRITICAL PRIVILEGE.

## 15. Scope matrix

| Required access | Role type | Binding type |
|---|---|---|
| cluster-scoped resources | ClusterRole | ClusterRoleBinding |
| non-resource URLs | ClusterRole | ClusterRoleBinding |
| namespaced resources, all namespaces | ClusterRole | ClusterRoleBinding |
| namespaced resources, one namespace, reusable permissions | ClusterRole | RoleBinding |
| namespaced resources, one namespace | Role | RoleBinding |

## 16. Least privilege

Prefer:

~~~text
workload A → ServiceAccount A → minimal role
workload B → ServiceAccount B → different minimal role
~~~

Avoid:
~~~text
default ServiceAccount → union of all workload permissions
~~~

## Acceptance

Before granting access verify:
- subject identity;
- resource scope;
- verbs;
- namespace;
- Role vs ClusterRole;
- RoleBinding vs ClusterRoleBinding;
- whether Secret/RBAC access enables privilege escalation.
