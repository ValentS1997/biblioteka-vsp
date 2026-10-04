# Ответ к упражнению главы 13

Это RAG-grounded walkthrough, не официальный издательский answer key.

## 1. Policy model

Source has two PSP resources:

~~~text
default
  privileged: false

privileged
  privileged: true
~~~

Admission plugin evaluates policies the requesting user is authorized to use.

## 2. Create permission objects

Source creates two ClusterRoles.

Default policy:

~~~bash
kubectl create clusterrole psp-default   --verb=use   --resource=podsecuritypolicies   --resource-name=default
~~~

Privileged policy:

~~~bash
kubectl create clusterrole psp-privileged   --verb=use   --resource=podsecuritypolicies   --resource-name=privileged
~~~

These objects grant permission to use a particular PSP; they do not by themselves assign that permission to a user.

## 3. Bind default policy to authenticated users

~~~bash
kubectl create clusterrolebinding psp-all-users   --clusterrole=psp-default   --group=system:authenticated
~~~

Expected:
Alice and Bob, as authenticated users, can use default PSP.

## 4. Bind privileged policy only to Bob

~~~bash
kubectl create clusterrolebinding psp-bob   --clusterrole=psp-privileged   --user=bob
~~~

Expected:
Bob can use both default and privileged PSP.
Alice can use only default PSP.

## 5. Validate Alice

~~~bash
kubectl --user alice create -f pod-privileged.yaml
~~~

Expected:
Forbidden because no PSP Alice may use permits privileged container.

## 6. Validate Bob

~~~bash
kubectl --user bob create -f pod-privileged.yaml
~~~

Expected:
Pod created because Bob is allowed to use privileged PSP.

## 7. Security interpretation

The decisive mechanism is not a field inside the Pod and not the username alone.

It is:

~~~text
user identity
  ↓
RBAC permission: use PodSecurityPolicy/<name>
  ↓
admission plugin evaluates available PSPs
  ↓
Pod admitted or rejected
~~~

## Rollback

Source does not provide one canonical full teardown sequence for the entire exercise.

Full teardown: [Needs confirmation].

Do not invent broad delete commands.

## Provenance

- p0483:c01–p0486:c01
