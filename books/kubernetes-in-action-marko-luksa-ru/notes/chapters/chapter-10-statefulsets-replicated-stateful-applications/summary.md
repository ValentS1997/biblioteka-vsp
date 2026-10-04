# Резюме главы 10

Источник: явный раздел 10.6 Резюме, RAG chunk p0382:c01.

После главы читатель должен уметь:

- предоставлять replicated Pods individual persistent storage;
- обеспечивать stable Pod identity;
- создавать StatefulSet и соответствующую governing Service;
- масштабировать и обновлять StatefulSet;
- обнаруживать других членов StatefulSet через DNS;
- подключаться к peers по их hostnames;
- понимать условия принудительного удаления stateful Pod.

## Центральная модель

~~~text
StatefulSet
  ├─ stable ordinal identity
  ├─ stable hostname/DNS identity
  ├─ per-Pod PVC/storage
  └─ ordered lifecycle

Peer discovery:
headless Service → DNS SRV → Pod hostnames

Failure safety:
unknown old instance
  → do not create duplicate identity
  → administrator must establish old instance is dead
~~~

## Critical safety conclusion

Force deletion is not equivalent to confirmed process termination.

Source explicitly warns not to force-delete stateful Pods unless the administrator knows the old node is no longer running/reachable and will remain so.

## Provenance

- Chapter chunks: p0350:c01–p0382:c01
- Summary chunk: p0382:c01
- PDF page: 382
- Printed page: 381
- Source SHA-256: 0d50f167ed86088d0cc65d15e27f1ab397e7c0a0c8de4db3801b50439f24266f
