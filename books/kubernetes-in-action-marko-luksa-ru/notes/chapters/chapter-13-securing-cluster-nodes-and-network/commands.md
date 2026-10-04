# Команды главы 13

Source policy: RAG-only. Commands classified by operational risk.

## hostNetwork verification

~~~bash
kubectl exec pod-with-host-network ifconfig
~~~

Read-only inside Pod.

Purpose:
compare interfaces visible from Pod using hostNetwork.

Creating such Pod is STATE-CHANGING and weakens network isolation.

## hostPID inspection

~~~bash
kubectl exec pod-with-host-pid-and-ipc ps aux
~~~

Read-only inside Pod, but Pod itself has high visibility into node process namespace.

## Default process identity

Source:

~~~bash
kubectl run pod-with-defaults --image alpine --restart Never -- /bin/sleep 999999
kubectl exec pod-with-defaults id
~~~

First STATE-CHANGING, second read-only.

Source result:
container runs as uid=0(root) when image/defaults do not choose another user.

## runAsUser verification

~~~bash
kubectl exec pod-as-user-guest id
~~~

Read-only.

Expected source result:
uid=405(guest).

## runAsNonRoot verification

~~~bash
kubectl get po pod-run-as-non-root
~~~

Read-only.

Source expected:
container rejected from running because image would run as root.

## Privileged container device visibility

Normal:

~~~bash
kubectl exec -it pod-with-defaults ls /dev
~~~

Privileged:

~~~bash
kubectl exec -it pod-privileged ls /dev
~~~

Read-only inspection, but privileged Pod creation itself is HIGH RISK.

## System-time capability demonstration

Source demonstrates changing node time from a container after adding SYS_TIME capability.

Risk classification: CRITICAL LAB-ONLY NODE SIDE EFFECT.

Source explicitly warns that this may make worker node unusable and may require VM restart.

Exact command is intentionally not promoted as an operational recommendation.

Verification in source uses:

~~~bash
minikube ssh date
~~~

Read-only node-time check.

## CHOWN capability demo

Normal:

~~~bash
kubectl exec pod-with-defaults chown guest /tmp
kubectl exec pod-with-defaults -- ls -la / | grep tmp
~~~

After dropping CHOWN:

~~~bash
kubectl exec pod-drop-chown-capability chown guest /tmp
~~~

Second chown is expected to fail.

## Read-only root filesystem

~~~bash
kubectl exec -it pod-with-readonly-filesystem touch /new-file
kubectl exec -it pod-with-readonly-filesystem touch /volume/newfile
kubectl exec -it pod-with-readonly-filesystem -- ls -la /volume/newfile
~~~

First write expected to fail.
Mounted volume write expected to succeed.

## fsGroup / supplementalGroups

~~~bash
kubectl exec -it pod-with-shared-volume-fsgroup -c first sh
~~~

Inside:

~~~bash
id
ls -l / | grep volume
echo foo > /volume/foo
ls -l /volume
~~~

Source demonstrates shared group access.

## PSP admission test

Create privileged Pod under restrictive PSP:

~~~bash
kubectl create -f pod-privileged.yaml
~~~

Expected source result:
Forbidden because privileged containers are not allowed.

## PSP MustRunAs test

~~~bash
kubectl create -f pod-as-user-guest.yaml
~~~

Expected:
Forbidden when runAsUser 405 violates allowed UID range.

Source also runs:

~~~bash
kubectl run run-as-5 --image luksa/kubia-run-as-user-5 --restart Never
kubectl exec run-as-5 -- id
~~~

Source result:
Pod runs as UID required by PSP rather than image USER.

## PSP forbidden capability test

~~~bash
kubectl create -f pod-add-sysadmin-capability.yaml
~~~

Expected:
Forbidden when SYS_ADMIN is disallowed by policy.

## Source Minikube PSP/RBAC lab bootstrap

The source uses a long version-specific Minikube command to enable:
- password-file authentication;
- RBAC;
- PodSecurityPolicy admission.

It also creates two lab users.

Exact bootstrap command and literal passwords are not promoted into this artifact because they are source-era, security-sensitive lab setup.

## Inspect PSPs

~~~bash
kubectl get psp
~~~

Read-only.

## Create PSP-use ClusterRoles

~~~bash
kubectl create clusterrole psp-default   --verb=use   --resource=podsecuritypolicies   --resource-name=default

kubectl create clusterrole psp-privileged   --verb=use   --resource=podsecuritypolicies   --resource-name=privileged
~~~

STATE-CHANGING authorization policy.

## Bind PSP access

All authenticated users:

~~~bash
kubectl create clusterrolebinding psp-all-users   --clusterrole=psp-default   --group=system:authenticated
~~~

Bob only:

~~~bash
kubectl create clusterrolebinding psp-bob   --clusterrole=psp-privileged   --user=bob
~~~

CLUSTER-WIDE AUTHORIZATION CHANGE.

## Configure source lab identities

Source configures Alice and Bob credentials in kubectl config.

Literal passwords are intentionally omitted.

Security:
- local kubeconfig changes credential state;
- do not reuse source lab credentials.

## PSP exercise validation

Alice:

~~~bash
kubectl --user alice create -f pod-privileged.yaml
~~~

Expected:
Forbidden.

Bob:

~~~bash
kubectl --user bob create -f pod-privileged.yaml
~~~

Expected:
created.

## NetworkPolicy

The chapter provides manifests rather than one canonical kubectl create/apply command for policy deployment.

Exact deployment command: [Needs confirmation].

Do not reconstruct it from memory.

## Safety matrix

| Operation | Class |
|---|---|
| exec/get inspection | read-only |
| create normal Pod | state-changing |
| host namespace Pod | high isolation impact |
| privileged Pod | high privilege |
| SYS_TIME demo | critical node-level side effect |
| PSP create/change | cluster admission policy change |
| ClusterRole/Binding for PSP | cluster authorization change |
| local credential configuration | local security state change |
| NetworkPolicy deployment | network connectivity policy change |
