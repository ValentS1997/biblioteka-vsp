# Резюме главы 3

Источник: явный раздел `3.9 Резюме`, RAG chunk `p0126:c01`.

После главы формируется базовое понимание Pod как центрального building block Kubernetes.

Ключевые результаты главы:

- уметь решать, какие containers должны быть сгруппированы в один Pod, а какие должны работать раздельно;
- понимать Pod как логический host, способный выполнять несколько процессов в отдельных containers;
- создавать Pods из YAML/JSON descriptors и исследовать их specification/current state;
- использовать labels и label selectors для организации Pods и операций над группами resources;
- использовать node labels и node selectors для ограничения placement по свойствам nodes;
- использовать annotations для более крупных metadata blobs, добавляемых пользователями или tooling;
- использовать namespaces для логического разделения resources между группами пользователей;
- применять `kubectl explain` для быстрого исследования Kubernetes resource fields.

## Центральная модель

~~~text
Pod
├─ co-location boundary
├─ shared networking boundary
└─ scaling boundary

labels/selectors
└─ grouping + selection

node labels/nodeSelector
└─ placement requirement

namespaces
└─ naming/resource scope
~~~

## Provenance

- Chapter chunks: `p0095:c01`–`p0126:c01`
- Summary chunk: `p0126:c01`
- PDF page: 126
- Printed page: 125
- Source SHA-256: `0d50f167ed86088d0cc65d15e27f1ab397e7c0a0c8de4db3801b50439f24266f`
