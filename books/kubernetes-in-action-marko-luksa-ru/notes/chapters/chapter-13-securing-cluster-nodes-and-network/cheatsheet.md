# Шпаргалка: node security и NetworkPolicy

## 1. Host namespace exposure

hostNetwork:
- Pod использует network namespace worker node;
- видит node interfaces;
- процессы привязываются к портам node.

hostPID / hostIPC:
- hostPID: true → Pod видит process namespace node;
- hostIPC: true → Pod разделяет IPC namespace node.

hostPort:
- публикует один container port на конкретном node;
- не требует полного перехода Pod в host network namespace.

## 2. Process identity

~~~text
securityContext:
  runAsUser: <uid>
~~~

Source example:
UID 405 → guest user в Alpine image.

Запрет root:

~~~text
runAsNonRoot: true
~~~

Если image запускается как root, Pod не стартует.

## 3. Privileged mode

~~~text
securityContext:
  privileged: true
~~~

High privilege:
- расширенный доступ к node devices;
- широкие kernel-level возможности.

Source logic: если достаточно отдельных capabilities, полный privileged mode избыточен.

## 4. Linux capabilities

Add:

~~~text
securityContext:
  capabilities:
    add:
    - SYS_TIME
~~~

Drop:

~~~text
securityContext:
  capabilities:
    drop:
    - CHOWN
~~~

Source example:
SYS_TIME позволяет менять системное время worker node.

Это critical lab-only capability demonstration.

## 5. Read-only root filesystem

~~~text
securityContext:
  readOnlyRootFilesystem: true
~~~

Effect:
- запись в container root filesystem запрещена;
- writable mounted volumes могут оставаться доступными для записи.

## 6. Shared volume groups

Pod-level:

~~~text
securityContext:
  fsGroup: 555
  supplementalGroups: [666, 777]
~~~

Source model:
- volume получает filesystem group;
- processes получают supplementary groups;
- containers с разными UID могут совместно использовать volume.

## 7. PodSecurityPolicy model

Source-era admission flow:

~~~text
Pod create/update
  ↓
PodSecurityPolicy admission plugin
  ↓
policies, которые user имеет право use
  ↓
validation / mutation
  ↓
allow or deny
~~~

PSP может ограничивать:
- hostIPC;
- hostPID;
- hostNetwork;
- hostPorts;
- privileged;
- readOnlyRootFilesystem;
- runAsUser;
- fsGroup;
- supplementalGroups;
- SELinux;
- capabilities;
- volume types.

## 8. UID/GID policy

RunAsAny:
- ограничения отсутствуют.

MustRunAs:
- разрешён конкретный UID или диапазон;
- source показывает, что PSP может переопределить USER из image.

MustRunAsNonRoot:
- root запрещён.

## 9. Capability policy in PSP

~~~text
allowedCapabilities
  → user может явно добавить capability

defaultAddCapabilities
  → capability добавляется автоматически

requiredDropCapabilities
  → capability удаляется принудительно
~~~

Source examples:
- allow SYS_TIME;
- default add CHOWN;
- required drop SYS_ADMIN и SYS_MODULE.

## 10. PSP volume allowlist

Source example разрешает:

~~~text
emptyDir
configMap
secret
downwardAPI
persistentVolumeClaim
~~~

## 11. Assign PSP through RBAC

~~~text
ClusterRole
  verb: use
  resource: podsecuritypolicies
  resource-name: <policy>

ClusterRoleBinding
  ↓
user/group
~~~

Exercise:
- all authenticated users → default PSP;
- Bob → additionally privileged PSP;
- Alice → privileged Pod denied;
- Bob → privileged Pod allowed.

## 12. NetworkPolicy — default deny

Source:

~~~text
podSelector: {}
~~~

Пустой selector выбирает все Pods namespace.

Policy без разрешающего ingress блокирует входящие connections к выбранным Pods в source model.

Requires network plugin support.

## 13. Pod-to-Pod allow rule

Target:

~~~text
podSelector:
  matchLabels:
    app: database
~~~

Allowed source:

~~~text
ingress:
- from:
  - podSelector:
      matchLabels:
        app: webserver
  ports:
  - port: 5432
~~~

## 14. Namespace-based allow

~~~text
namespaceSelector:
  matchLabels:
    tenant: manning
~~~

Source security note:
если users могут произвольно менять namespace labels, они могут обойти selector-based isolation.

## 15. CIDR rule

~~~text
ipBlock:
  cidr: 192.168.1.0/24
~~~

Разрешает traffic из указанного address block.

## 16. Egress

Source egress example выбирает:

~~~text
app=webserver
~~~

и ограничивает destinations Pods с:

~~~text
app=database
~~~

## Acceptance model

Перед host/privileged access:
- requirement документирован;
- narrower capability alternative рассмотрен;
- node-level blast radius понятен.

Перед PSP/RBAC:
- users/groups известны;
- allowed settings проверены;
- cluster-wide binding scope проверен.

Перед NetworkPolicy:
- plugin support подтверждён;
- selectors проверены;
- rollback manifest сохранён;
- required connectivity учтена только в пределах source evidence.
