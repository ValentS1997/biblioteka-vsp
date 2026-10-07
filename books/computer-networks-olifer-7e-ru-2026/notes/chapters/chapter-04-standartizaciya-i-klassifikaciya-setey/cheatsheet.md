# Cheatsheet — глава 4: стандартизация и классификация сетей

## Symptom / problem framing

**Проблема:** без декомпозиции сложная network interaction system плохо проектируется и тестируется, а без общих specifications независимые реализации несовместимы. Даже после стандартизации остаётся вопрос: по каким признакам сравнивать разные сети. Глава решает эти три задачи последовательно: **layering → standardization → classification**. `p0108:c01`–`p0130:c01`.

## Baseline / context

| Понятие | Что фиксирует | RAG |
| --- | --- | --- |
| Module | Отдельную функциональную подзадачу | `p0108:c01`–`p0109:c01` |
| Layer | Группу функций на одном abstraction level | `p0108:c01`–`p0110:c01` |
| Service interface | Что lower layer предоставляет соседнему upper layer | `p0109:c01`–`p0110:c01` |
| Protocol | Rules/messages между peer entities одного layer на разных nodes | `p0110:c01`–`p0112:c01` |
| Protocol stack | Иерархический набор protocols для взаимодействия узлов | `p0111:c01` |
| OSI model | 7-layer reference decomposition | `p0112:c01`–`p0121:c01` |
| Open specification | Published, publicly available agreed specification | `p0122:c01`–`p0123:c01` |
| Standard | Common specification with defined status/source | `p0123:c01`–`p0124:c01` |
| Classification axis | Один выбранный признак сети; реальная сеть имеет много таких признаков | `p0126:c01`–`p0130:c01` |

## Read-only checks

Для анализа конкретной технологии или устройства:

1. Что является **model**, что **protocol**, а что **implementation**? `p0115:c01`.
2. Какие функции действительно реализуются данным node, а какие проходят through transparently? `p0118:c01`–`p0119:c01`.
3. Какой PDU/служебная информация добавляется на каждом relevant layer? `p0112:c01`, `p0116:c01`–`p0118:c01`.
4. Это user-plane, control-plane или management-plane traffic? `p0120:c01`.
5. Specification открытая или proprietary? Standard de facto или de jure status в source? `p0122:c01`–`p0124:c01`.
6. Для TCP/IP: какие protocols выше IP и какие lower-layer technologies находятся под IP? `p0125:c01`–`p0126:c01`.
7. При classification не смешиваются ли axes: coverage, medium, switching, topology, users, functional role? `p0126:c01`–`p0130:c01`.

Фактический protocol stack, device role, RFC version, vendor certification и topology пользовательской сети: **[Needs confirmation]**.

## Interpretation

- **Layering скрывает реализацию за stable interfaces.** Это позволяет independently develop/test/replace a layer при сохранении межуровневого interface. `p0108:c01`–`p0110:c01`.
- **Protocol ≠ implementation.** Один protocol может иметь implementations разного качества, а model вообще задаёт функции ещё более абстрактно. `p0111:c01`–`p0116:c01`.
- **OSI полезна прежде всего как common reference vocabulary.** Источник прямо отмечает, что universal OSI protocol stack не стал доминирующим, но reference model сохранила роль общего языка. `p0112:c01`–`p0113:c01`.
- **Encapsulation не означает direct peer communication.** Peer entities логически взаимодействуют через services нижних layers; физически напрямую взаимодействует только physical layer. `p0116:c01`–`p0118:c01`.
- **Device layer mapping — функциональная модель, не маркировка корпуса.** Реальные communication devices могут поддерживать дополнительные upper-layer service protocols. `p0119:c01`–`p0120:c01`.
- **Control/management planes нужны, потому что “vertical” classification не описывает всё.** Routing, naming and management protocols may use upper-layer transport while serving network-control tasks. `p0120:c01`–`p0121:c01`.
- **Open standards reduce interoperability risk.** Главные результаты по source: multi-vendor composition, component replacement, inter-network coupling. `p0122:c01`–`p0123:c01`.
- **TCP/IP is not one rigid seven-layer mirror.** Source presents many upper/lower combinations and IP as the common waist. `p0125:c01`–`p0126:c01`.
- **Classification is contextual.** Например, одна сеть может одновременно быть WAN, wireless, packet-switched, corporate, tree/mesh-derived, access or backbone depending on the chosen axis. `p0126:c01`–`p0130:c01`.

## Next action

При изучении новой network technology использовать порядок:

**architecture → model/layers → peer protocols → service interfaces → node responsibilities → control/management protocols → standard/specification source → classification axes**.

Это source-grounded учебный порядок, а не vendor configuration workflow.

## Modifying action

**[Not applicable].** Глава не содержит executable configuration commands. Она упоминает remote management/configuration protocols и manual setup in other contexts, но точные actions отсутствуют.

## Verification / acceptance checks

Глава усвоена, если можно:

- объяснить разницу между service interface и peer protocol;
- различить model / protocol / implementation;
- назвать семь OSI layers и их основные scopes;
- объяснить encapsulation/decapsulation без представления, что peer layers физически разговаривают напрямую;
- отнести repeater, LAN switch и router к source-described layer scopes;
- объяснить user/control/management planes;
- объяснить, что делает system “open” в терминах главы;
- описать роль RFC/IETF и why standards matter without external additions;
- объяснить narrow-waist idea TCP/IP;
- классифицировать одну сеть сразу по нескольким независимым axes.

## Rollback

**[Not applicable].** State-changing procedure в главе не задана.
