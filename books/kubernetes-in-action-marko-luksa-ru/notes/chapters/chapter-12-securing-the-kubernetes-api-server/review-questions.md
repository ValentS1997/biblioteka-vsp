# Упражнение главы 12

В проверенной границе найден один явно обозначенный практический RBAC exercise, начинающийся в p0436:c01.

## Упражнение 1 — Исследование Role / RoleBinding / ClusterRole / ClusterRoleBinding

### Подготовка

Source требует:
- активный RBAC;
- отсутствие permissive-binding из главы 8;
- два namespaces: foo и bar;
- test workload в каждом namespace.

Source setup:

~~~bash
kubectl delete clusterrolebinding permissive-binding

kubectl create ns foo
kubectl run test --image=luksa/kubectl-proxy -n foo

kubectl create ns bar
kubectl run test --image=luksa/kubectl-proxy -n bar
~~~

### Часть A — Namespaced Role

1. Убедиться, что foo:default не может list Services в foo.
2. Создать Role service-reader в foo с verbs get/list над Services.
3. Создать аналогичную Role в bar.
4. Связать foo:default с Role service-reader в foo через RoleBinding.
5. Проверить, что permissions действуют только в scope binding.
6. Добавить bar:default как subject в RoleBinding namespace foo и проверить cross-namespace subject binding к permissions в foo.

### Часть B — Cluster-scoped resource

1. Создать ClusterRole pv-reader с get/list для PersistentVolumes.
2. Связать её сначала через RoleBinding в foo.
3. Проверить, что это не даёт доступа к cluster-scoped PersistentVolumes.
4. Удалить RoleBinding pv-test.
5. Создать ClusterRoleBinding pv-test для той же ServiceAccount.
6. Проверить, что list PersistentVolumes теперь разрешён.

### Часть C — ClusterRole view и scope binding

1. Проверить отсутствие доступа foo:default к Pods cluster-wide и в foo.
2. Создать ClusterRoleBinding view-test → ClusterRole view → foo:default.
3. Проверить доступ к Pods в foo, bar и cluster-wide.
4. Удалить ClusterRoleBinding.
5. Создать RoleBinding view-test в foo, ссылающийся на ClusterRole view.
6. Проверить, что доступ остаётся только в foo.

## Acceptance

Exercise считается пройденным, если на практике подтверждены четыре правила:

1. Role + RoleBinding → namespaced permissions.
2. ClusterRole + RoleBinding → reusable permissions, но только namespace binding.
3. ClusterRole + ClusterRoleBinding → cluster-wide scope.
4. Cluster-scoped resources нельзя разрешить через RoleBinding.

## Safety

RBAC commands меняют authorization state реального cluster.

Особенно опасны:
- ClusterRoleBinding;
- cluster-admin bindings;
- Secret/token inspection.

Выполнять exercise только в controlled/disposable lab либо с точно известным rollback scope.

## Provenance

- Exercise explicitly introduced: p0436:c01
- Setup: p0437:c01–p0438:c01
- Role/RoleBinding: p0438:c01–p0442:c01
- ClusterRole/ClusterRoleBinding: p0443:c01–p0446:c01
- ClusterRole view scope comparison: p0450:c01–p0452:c01
