# Резюме главы 13

Источник: явный раздел 13.5 Резюме, RAG chunk p0491:c01.

Глава закрепляет следующие положения:

- Pods могут использовать host Linux namespaces вместо собственных;
- containers могут запускаться под user/group, отличными от image defaults;
- containers могут работать privileged и получать node-device access;
- containers можно сделать read-only относительно root filesystem, сохранив writable mounted volumes;
- PodSecurityPolicy source-era resources ограничивают security-sensitive Pod settings;
- PSP можно связывать с users/groups через RBAC ClusterRole/ClusterRoleBinding;
- NetworkPolicy ограничивает ingress и/или egress traffic Pods.

## Центральная модель

~~~text
Pod spec
  ↓
securityContext
  → UID/GID
  → privileged/capabilities
  → read-only root filesystem

Pod admission
  ↓
PodSecurityPolicy + RBAC
  → permitted security envelope

Runtime communication
  ↓
NetworkPolicy
  → permitted ingress/egress paths
~~~

## Security conclusion

Node isolation and network isolation are separate boundaries.

A workload may be API-authorized yet still dangerous if it:
- joins host namespaces;
- runs privileged;
- receives powerful kernel capabilities;
- mounts unsafe volumes;
- can reach unrelated workloads/networks.

Source therefore layers:
container securityContext + admission policy + network policy.

## Provenance

- Chapter chunks: p0458:c01–p0491:c01
- Summary chunk: p0491:c01
- PDF page: 491
- Printed page: 490
- Source SHA-256: 0d50f167ed86088d0cc65d15e27f1ab397e7c0a0c8de4db3801b50439f24266f
