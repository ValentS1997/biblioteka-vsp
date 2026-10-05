# Ответы к контрольным материалам — глава 6

## Контрольный тест: ключ из источника

| № | Ответ |
|---:|:---:|
| 1 | A |
| 2 | A |
| 3 | C |
| 4 | D |
| 5 | C |
| 6 | B |
| 7 | D |
| 8 | A |
| 9 | B |
| 10 | D |

Ключ `1-A, 2-A, 3-C, 4-D, 5-C, 6-B, 7-D, 8-A, 9-B, 10-D` приведён в `p0150:c01`.

## Ответы на открытые вопросы

### 1. Какие networks создаются по умолчанию?

Bridge, Host и None.

### 2. Что такое network namespace container?

Isolated Linux network stack container: interfaces, addresses, routes and related state. Docker stores it under `/var/run/docker/netns`.

### 3. Какие networks появляются при Swarm?

`ingress` (overlay, swarm scope) и `docker_gwbridge` (bridge, local scope).

### 4. Что такое docker0?

Default Docker bridge based on Linux bridge. Host side veth endpoints connect containers to it.

### 5. Как выполняется port mapping?

Host port maps to container port. Source shows `-P` for automatic/random host port and `-p host:container` for explicit mapping, plus TCP/UDP variants. Outbound bridge traffic is explained through NAT/MASQUERADE.

### 6. Что такое MACVLAN и какие режимы?

MACVLAN gives a virtual interface linked to physical parent, with its own MAC/IP. Source covers bridge and trunk bridge 802.1Q modes.

### 7. Что такое veth?

Virtual Ethernet pair connecting network namespaces/bridges as a point-to-point virtual link.

### 8. Как работает overlay?

Container overlay interface connects through veth to `br0` inside overlay network namespace. VXLAN/VTEP encapsulates L2 frames into UDP packets between hosts. Source observes UDP 4789.

### 9. Что такое VXLAN?

Mechanism for L2 virtual networking over L3 infrastructure. Source describes MAC-in-UDP encapsulation, VNI segmentation and VTEP endpoints.

### 10. Как source обеспечивает ping host→MACVLAN container?

```bash
ip link add macnet0 link eth0 type macvlan mode bridge
ip addr add <ip>/<prefix> dev macnet0
ip link set macnet0 up
```

Then connectivity is verified with `ping`. Source address values are not generalized into a production-safe plan.

## Operational map

```text
single host:
container → veth → docker0 → NAT/host NIC

physical L2:
container → MACVLAN → parent NIC

multi-host:
container → veth → br0 → VXLAN/VTEP → UDP 4789 → remote host
```

## Provenance

Ответы сформированы только по chapter RAG `p0114:c01`–`p0151:c01`. External sources и model-memory не использовались.
