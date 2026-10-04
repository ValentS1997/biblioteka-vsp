# Упражнение главы 13

В проверенной границе найден один явно обозначенный exercise в разделе назначения разных PodSecurityPolicy пользователям: p0483:c01–p0486:c01.

## Упражнение 1 — Разные PodSecurityPolicy для Alice и Bob через RBAC

Цель:
- Alice должна иметь возможность использовать только restrictive/default PSP;
- Bob должен дополнительно иметь возможность использовать privileged PSP.

### Подготовка

Source requires:
- RBAC enabled;
- PodSecurityPolicy admission enabled;
- source-era user authentication for Alice and Bob;
- policies default and privileged.

Source lab credentials are intentionally not copied into this artifact.

### Part A — Create RBAC permissions for PSP use

Create ClusterRole psp-default:
- verb: use;
- resource: podsecuritypolicies;
- resource-name: default.

Create ClusterRole psp-privileged:
- verb: use;
- resource: podsecuritypolicies;
- resource-name: privileged.

### Part B — Bind policies

Bind psp-default to:
- group system:authenticated.

Bind psp-privileged to:
- user Bob only.

Expected authorization model:

~~~text
Alice → default PSP
Bob   → default PSP + privileged PSP
~~~

### Part C — Validate

As Alice, create privileged Pod:
- expected: Forbidden.

As Bob, create same privileged Pod:
- expected: created.

## Acceptance criteria

- Alice cannot deploy privileged Pod.
- Bob can deploy privileged Pod.
- Both identities can use default policy.
- Difference is caused by RBAC right to use a specific PSP.
- Cluster-wide binding scope is understood before execution.

## Safety

This exercise changes cluster admission and authorization behavior.

Do not run in production unless changes are intentional, reviewed and reversible.

## Provenance

- Exercise introduction: p0483:c01
- ClusterRoles: p0484:c01
- ClusterRoleBindings and users: p0485:c01
- Validation as Alice/Bob: p0486:c01
