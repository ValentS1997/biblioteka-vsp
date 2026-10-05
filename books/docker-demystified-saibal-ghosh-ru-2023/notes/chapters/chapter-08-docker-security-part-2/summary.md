# Итог главы 8

## Заключение

Глава 8 описывает security/control-plane capabilities исторической Docker Enterprise Edition platform.

Source выделяет три компонента: Docker Engine Enterprise, Universal Control Plane и Docker Trusted Registry. UCP обеспечивает centralized management and access control, DTR — enterprise registry and vulnerability scanning, Engine Enterprise — image/container runtime.

Chapter подробно проводит source-era installation flow на Ubuntu: лицензированный repository, Docker EE на двух nodes, UCP на manager, worker join в Swarm и DTR на другом node. Эти процедуры завязаны на версии 2019–2020 годов и не являются current deployment guidance.

Client Bundle закрывает authentication boundary между operator CLI и UCP. Bundle содержит client certificate/key material и scripts для конфигурации Docker CLI/Kubectl. Source подчёркивает environment variables `DOCKER_HOST`, `DOCKER_CERT_PATH` и `DOCKER_TLS_VERIFY`.

DTR vulnerability scanning использует CVE database. Source показывает online synchronization, offline tar update model, manual scanning and scan-on-push. Сравнение fresh и old BusyBox images демонстрирует, что scanner связывает vulnerabilities with image layers/components.

RBAC в UCP строится из subjects, roles и collections/resource sets. Subject может быть user, organization или team. Role задаёт permissions. Collection определяет набор resources. Grant связывает subject + role + resource set.

Source перечисляет predefined Swarm roles: View Only, Restricted Control, Scheduler, Full Control. Затем создаёт custom collection, custom role и grant для user `itops`.

## Основные тезисы источника

- Docker Enterprise includes Engine Enterprise, UCP and DTR.
- Docker Enterprise requires license in source-era workflow.
- UCP centralizes management of cluster/applications.
- DTR is enterprise image registry.
- Client Bundle authenticates authorized CLI access to UCP.
- Client Bundle sets `DOCKER_HOST`, `DOCKER_CERT_PATH`, `DOCKER_TLS_VERIFY`.
- DTR scans images against a CVE vulnerability database.
- CVE data can be synchronized online or updated offline.
- Scan-on-push can automate image scanning.
- UCP provides role-based access control.
- RBAC grant combines subject, role and resource collection.

## Ключевые термины

| Термин | Смысл главы |
|---|---|
| Docker Enterprise Edition | Source-era enterprise Docker platform |
| Docker Engine Enterprise | Enterprise runtime/engine |
| UCP | Central management/control plane |
| DTR | Enterprise image registry |
| Client Bundle | Client certificate/key + CLI configuration bundle |
| CVE database | Vulnerability knowledge base used by scanner |
| Image scanning | Analysis of image layers/components for known vulnerabilities |
| Scan on push | Automatic scan triggered by image push |
| RBAC | Role Based Access Control |
| Subject | User, organization or team receiving grant |
| Role | Permission set |
| Collection | Resource set |
| Grant | Subject + role + resource set assignment |
| Organization | Grouping of users/teams in source model |
| Team | User group within organizational model |
| Repository | DTR image repository |

## Built-in roles from source

| Role | Summary |
|---|---|
| View Only | View resources; cannot create |
| Restricted Control | Modify with restrictions on risky container/service actions |
| Scheduler | Schedule workloads and view nodes; workload viewing requires separate permission |
| Full Control | Broad control over granted resources |

## Built-in collections from source

- `/` — root/universal resource path;
- `/System` — UCP managers and DTR system services;
- `/Shared` — schedulable worker resources;
- `/Shared/Private/` — per-user private collections;
- `/Shared/Legacy/` — legacy UCP collections.

## Historical caveat

Source explicitly notes the Mirantis acquisition of Docker Enterprise in November 2019. The installation, licensing, UCP/DTR product names and versions are historical context and were not externally reconciled.

## Provenance

- Chapter RAG: `p0185:c01`–`p0212:c01`
- PDF pages: 185–212
- Printed pages: 191–218
- Source SHA-256: `7a52f7d947347a470790c7d384390f60bf49fe5426827f5829a75757b50faaa8`
