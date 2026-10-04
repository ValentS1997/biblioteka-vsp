# Глава 18 — резюме

Источник: RAG chunk `p0639:c01`, PDF page 639, printed page 638.

Заключительная глава показывает способы выхода за рамки встроенных возможностей Kubernetes.

По смыслу раздела 18.4:

- собственные ресурсы можно зарегистрировать на API server через `CustomResourceDefinition`;
- экземпляры custom resources можно хранить, читать, обновлять и удалять без изменения кода основного API server;
- пользовательский controller придает этим объектам operational behavior;
- дополнительные API servers можно интегрировать через API aggregation;
- Kubernetes Service Catalog позволяет provision внешних служб и связывать их с workloads в кластере;
- PaaS-платформы поверх Kubernetes упрощают создание и delivery контейнерных приложений;
- Helm позволяет разворачивать готовые приложения без ручного написания всего набора resource manifests.

Главный итог главы: Kubernetes представлен не как закрытый набор фиксированных primitives, а как расширяемая платформа, где новые abstractions строятся поверх API objects, controllers и стандартных ресурсов.
